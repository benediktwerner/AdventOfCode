use std::convert::TryFrom;

use anyhow::{bail, ensure};

use crate::{SliceWrapper, SliceWrapperMut};

const SHINY_GOLD: u16 = (12 << 5) | 15;
const HAS_GOLD_BIT: u64 = 63;
const BAG_SHIFT: u64 = 15;

static mut COLOR_TABLE: [(u16, u16); 215] = [(0, 0); 215];
static mut ATTRIBUTES_TABLE: [(u16, u16); 1024] = [(0, 0); 1024];

pub struct Solver(());

impl Solver {
    pub fn new() -> Self {
        let solver = Self(());
        assert_solver_day!(solver);
        init_parsing_tables();
        solver
    }
}

impl crate::Solver for Solver {
    fn day(&self) -> u8 {
        7
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(input.len() >= 20, "Input is too short. (< 20 characters)");
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
        for line in input.lines() {
            let mut iter = line.split(" bags contain ");
            let parts = (iter.next(), iter.next());
            ensure!(iter.next().is_none(), "Too many values: {}", line);
            match parts {
                (Some(bag), Some(contains)) => {
                    validate_bag(bag)?;
                    ensure!(
                        &contains[contains.len() - 1..] == ".",
                        "Line does not end with a dot: '{}'",
                        line
                    );
                    if contains == "no other bags." {
                        continue;
                    }
                    let bag_count = contains.split(", ").count();
                    ensure!(
                        bag_count <= 4,
                        "Bag contains more than 4 other bags: '{}'",
                        line
                    );
                    for contained_bag in contains[..contains.len() - 1].split(", ") {
                        let mut count = contained_bag.as_bytes()[0];
                        ensure!(
                            b'1' <= count && count <= b'9',
                            "Count is not a valid digit: '{}' in '{}'",
                            count as char,
                            contained_bag
                        );
                        ensure!(
                            contained_bag.as_bytes()[1] == b' ',
                            "No space after count: '{}'",
                            contained_bag
                        );
                        count -= b'0';
                        let cutoff = if count > 1 {
                            ensure!(
                                &contained_bag[contained_bag.len() - 5..] == " bags",
                                "Expected 'bags': '{}",
                                contained_bag
                            );
                            5
                        } else {
                            ensure!(
                                &contained_bag[contained_bag.len() - 4..] == " bag",
                                "Expected 'bag': '{}",
                                contained_bag
                            );
                            4
                        };
                        validate_bag(&contained_bag[2..contained_bag.len() - cutoff])?;
                    }
                }
                _ => bail!("Invalid line: {}", line),
            }
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let mut output = (0, 0);

        // bags are represented by a u16
        //  lower 5 bits are attribute (dim, shiny, striped, etc.)
        //  next 6 bits are color (red, green, etc.)
        //  last 5 bits are unused

        // info for bag i is at bags[i]
        //  63. bit set => bag contains golden bag
        //  every 15 bits at 0, 15, 30, and 45 are contained bags
        //    11 (low) bits bag number and 4 (high) bits count
        let mut bags = [0_u64; 2048];
        let mut bags = SliceWrapperMut::new(&mut bags);

        let vec_init: [usize; 3] = std::mem::transmute(Vec::<u16>::new());
        let mut bags_reverse: [Vec<u16>; 2048] = std::mem::transmute([vec_init; 2048]);
        let mut bags_reverse = SliceWrapperMut::<Vec<u16>>::new(&mut bags_reverse);

        let bytes = SliceWrapper::new(input.as_bytes());
        let mut i = 0;

        loop {
            let bag = parse_bag(bytes, &mut i);

            i += 14; // skip " bags contain "

            let mut has_gold = false;
            let mut inner_shift = 0;

            if bytes[i] == b'n' {
                // bag contains no other bags
                i += 15; // skip "no other bags.\n"
            } else {
                loop {
                    let count = bytes[i] - b'0';
                    i += 2;
                    let inner_bag = parse_bag(bytes, &mut i);
                    i += 4 + (count > 1) as u32; // skip " bag" or " bags"

                    let count = (count as u16) << 11;
                    bags[bag as usize] |= ((count | inner_bag) as u64) << inner_shift;

                    if inner_bag == SHINY_GOLD
                        || (bags[inner_bag as usize] & (1 << HAS_GOLD_BIT)) != 0
                    {
                        has_gold = true;
                    }

                    bags_reverse[inner_bag as usize].push(bag);

                    i += 2; // skip ", " or ".\n"

                    if bytes[i - 2] == b'.' {
                        break;
                    }

                    inner_shift += BAG_SHIFT;
                }

                if has_gold {
                    bags[bag as usize] |= 1 << HAS_GOLD_BIT;
                    output.0 += 1;
                    propagate_contains_gold(
                        bag,
                        &mut output.0,
                        bags.0,
                        SliceWrapper::new(bags_reverse.0),
                    );
                }
            }

            if i as usize >= input.len() {
                break;
            }
        }

        let mut bag_counts = [0_u32; 2048];

        output.1 = count_contained_bags(SHINY_GOLD, bags.0, &mut bag_counts);
        output.1 -= 1;

        (output.0.to_string(), output.1.to_string())
    }
}

unsafe fn count_contained_bags(bag: u16, bags: &[u64], bag_counts: &mut [u32]) -> u32 {
    let bags = SliceWrapper(bags);
    let mut bag_counts = SliceWrapperMut(bag_counts);

    let mut count = 1;
    let mut bag_data = bags[bag as usize] & !(1 << HAS_GOLD_BIT);
    loop {
        let inner = bag_data & ((1 << BAG_SHIFT) - 1);
        if inner == 0 {
            break;
        }

        let inner_multiplier = (inner >> 11) as u32;
        let inner_bag = (inner & ((1 << 11) - 1)) as u16;

        let mut inner_count = bag_counts[inner_bag as usize];
        if inner_count == 0 {
            inner_count = count_contained_bags(inner_bag, bags.0, bag_counts.0);
        }
        count += inner_multiplier * inner_count;

        bag_data >>= BAG_SHIFT;
    }

    bag_counts[bag as usize] = count;
    count
}

unsafe fn propagate_contains_gold(
    bag: u16,
    count: &mut u32,
    bags: &mut [u64],
    bags_reverse: SliceWrapper<Vec<u16>>,
) {
    let mut bags = SliceWrapperMut::new(bags);
    for &outer_bag in &bags_reverse[bag as usize] {
        if bags[outer_bag as usize] & (1 << HAS_GOLD_BIT) != 0 {
            continue;
        }

        *count += 1;
        bags[outer_bag as usize] |= 1 << HAS_GOLD_BIT;
        propagate_contains_gold(outer_bag, count, bags.0, bags_reverse);
    }
}

#[inline(always)]
unsafe fn parse_bag(bytes: SliceWrapper<u8>, i: &mut u32) -> u16 {
    let (attr, len) = parse_attribute(&bytes[*i as usize..]);
    *i += len as u32 + 1;
    let (color, len) = parse_color(&bytes[*i as usize..]);
    *i += len as u32;

    (color << 5) | attr
}

#[inline(always)]
unsafe fn parse_color(bytes: &[u8]) -> (u16, u16) {
    let bytes = SliceWrapper::new(bytes);
    let color = u32::from_le_bytes(<[u8; 4]>::try_from(&bytes[0..4usize]).unwrap_unchecked());
    let index = color % 215;
    let val = SliceWrapper::new(&COLOR_TABLE)[index];
    debug_assert!(val != (0, 0), "Invalid color");
    val
}

#[inline(always)]
unsafe fn parse_attribute(bytes: &[u8]) -> (u16, u16) {
    let bytes = SliceWrapper::new(bytes);
    let a = (bytes[0] & 0b11111_u8) as u16;
    let b = (bytes[1] & 0b11111_u8) as u16;
    let index = (a << 5) | b;
    let val = SliceWrapper::new(&ATTRIBUTES_TABLE)[index as u32];
    debug_assert!(val != (0, 0), "Invalid attribute");
    val
}

fn validate_bag(bag: &str) -> anyhow::Result<()> {
    let mut iter = bag.split(' ');
    let parts = (iter.next(), iter.next());
    ensure!(iter.next().is_none(), "Too many values for bag: {}", bag);
    match parts {
        (Some(attr), Some(color)) => {
            match attr {
                "bright" | "clear" | "dark" | "dim" | "dotted" | "drab" | "dull" | "faded"
                | "light" | "mirrored" | "muted" | "pale" | "plaid" | "posh" | "shiny"
                | "striped" | "vibrant" | "wavy" => (),
                _ => bail!("Invalid bag attribute: '{}'", attr),
            }
            match color {
                "aqua" | "beige" | "black" | "blue" | "bronze" | "brown" | "chartreuse"
                | "coral" | "crimson" | "cyan" | "fuchsia" | "gold" | "gray" | "green"
                | "indigo" | "lavender" | "lime" | "magenta" | "maroon" | "olive" | "orange"
                | "plum" | "purple" | "red" | "salmon" | "silver" | "tan" | "teal" | "tomato"
                | "turquoise" | "violet" | "white" | "yellow" => (),
                _ => bail!("Invalid bag color: '{}'", color),
            }
        }
        _ => bail!("Invalid bag: {}", bag),
    }
    Ok(())
}

fn init_parsing_tables() {
    use std::sync::atomic::AtomicBool;
    static TABLES_INIT: AtomicBool = AtomicBool::new(false);

    if TABLES_INIT.swap(true, std::sync::atomic::Ordering::SeqCst) {
        return;
    }

    unsafe {
        // Colors
        COLOR_TABLE[79] = (1, 4); // aqua
        COLOR_TABLE[137] = (2, 5); // beige
        COLOR_TABLE[37] = (3, 5); // black
        COLOR_TABLE[144] = (4, 4); // blue
        COLOR_TABLE[208] = (5, 6); // bronze
        COLOR_TABLE[7] = (6, 5); // brown
        COLOR_TABLE[184] = (7, 10); // chartreuse
        COLOR_TABLE[116] = (8, 5); // coral
        COLOR_TABLE[107] = (9, 7); // crimson
        COLOR_TABLE[182] = (10, 4); // cyan
        COLOR_TABLE[77] = (11, 7); // fuchsia
        COLOR_TABLE[72] = (12, 4); // gold
        COLOR_TABLE[155] = (13, 4); // gray
        COLOR_TABLE[159] = (14, 5); // green
        COLOR_TABLE[90] = (15, 6); // indigo
        COLOR_TABLE[94] = (16, 8); // lavender
        COLOR_TABLE[128] = (17, 4); // lime
        COLOR_TABLE[35] = (18, 7); // magenta
        COLOR_TABLE[171] = (19, 6); // maroon
        COLOR_TABLE[102] = (20, 5); // olive
        COLOR_TABLE[122] = (21, 6); // orange
        COLOR_TABLE[51] = (22, 4); // plum
        COLOR_TABLE[40] = (23, 6); // purple
        COLOR_TABLE[142] = (24, 3); // red
        COLOR_TABLE[169] = (25, 6); // salmon
        COLOR_TABLE[81] = (26, 6); // silver
        COLOR_TABLE[20] = (27, 3); // tan
        COLOR_TABLE[212] = (28, 4); // teal
        COLOR_TABLE[113] = (29, 6); // tomato
        COLOR_TABLE[165] = (30, 9); // turquoise
        COLOR_TABLE[47] = (31, 6); // violet
        COLOR_TABLE[134] = (32, 5); // white
        COLOR_TABLE[3] = (33, 6); // yellow

        // Attributes
        ATTRIBUTES_TABLE[82] = (1, 6); // bright
        ATTRIBUTES_TABLE[108] = (2, 5); // clear
        ATTRIBUTES_TABLE[129] = (3, 4); // dark
        ATTRIBUTES_TABLE[137] = (4, 3); // dim
        ATTRIBUTES_TABLE[143] = (5, 6); // dotted
        ATTRIBUTES_TABLE[146] = (6, 4); // drab
        ATTRIBUTES_TABLE[149] = (7, 4); // dull
        ATTRIBUTES_TABLE[193] = (8, 5); // faded
        ATTRIBUTES_TABLE[393] = (9, 5); // light
        ATTRIBUTES_TABLE[425] = (10, 8); // mirrored
        ATTRIBUTES_TABLE[437] = (11, 5); // muted
        ATTRIBUTES_TABLE[513] = (12, 4); // pale
        ATTRIBUTES_TABLE[524] = (13, 5); // plaid
        ATTRIBUTES_TABLE[527] = (14, 4); // posh
        ATTRIBUTES_TABLE[616] = (15, 5); // shiny
        ATTRIBUTES_TABLE[628] = (16, 7); // striped
        ATTRIBUTES_TABLE[713] = (17, 7); // vibrant
        ATTRIBUTES_TABLE[737] = (18, 4); // wavy
    }
}
