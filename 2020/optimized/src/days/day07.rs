use anyhow::{bail, ensure};

use crate::{SliceWrapper, SliceWrapperMut};

const SHINY_GOLD: u16 = (12 << 5) | 15;
const HAS_GOLD_BIT: u64 = 63;
const BAG_SHIFT: u64 = 15;

pub struct Solver(());

impl Solver {
    pub fn new() -> Self {
        let solver = Self(());
        assert_solver_day!(solver);
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
                    validata_bag(bag)?;
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
                        validata_bag(&contained_bag[2..contained_bag.len() - cutoff])?;
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
    *i += len + 1;
    let (color, len) = parse_color(&bytes[*i as usize..]);
    *i += len;

    (color << 5) | attr
}

#[inline(always)]
unsafe fn parse_color(bytes: &[u8]) -> (u16, u32) {
    let bytes = SliceWrapper::new(bytes);
    match bytes[0] {
        b'a' => (1, 4), // aqua
        b'b' => match bytes[3] {
            b'g' => (2, 5), // beige
            b'c' => (3, 5), // black
            b'e' => (4, 4), // blue
            b'n' => (5, 6), // bronze
            _ => (6, 5),    // brown
        },
        b'c' => match bytes[1] {
            b'h' => (7, 10), // chartreuse
            b'o' => (8, 5),  // coral
            b'r' => (9, 7),  // crimson
            _ => (10, 4),    // cyan
        },
        b'f' => (11, 7), // fuchsia
        b'g' => match bytes[2] {
            b'l' => (12, 4), // gold
            b'a' => (13, 4), // gray
            _ => (14, 5),    // green
        },
        b'i' => (15, 6), // indigo
        b'l' => match bytes[1] {
            b'a' => (16, 8), // lavender
            _ => (17, 4),    // lime
        },
        b'm' => match bytes[2] {
            b'g' => (18, 7), // magenta
            _ => (19, 6),    // maroon
        },
        b'o' => match bytes[1] {
            b'l' => (20, 5), // olive
            _ => (21, 6),    // orange
        },
        b'p' => match bytes[1] {
            b'l' => (22, 4), // plum
            _ => (23, 6),    // purple
        },
        b'r' => (24, 3), // red
        b's' => match bytes[1] {
            b'a' => (25, 6), // salmon
            _ => (26, 6),    // silver
        },
        b't' => match bytes[1] {
            b'a' => (27, 3), // tan
            b'e' => (28, 4), // teal
            b'o' => (29, 6), // tomato
            _ => (30, 9),    // turquoise
        },
        b'v' => (31, 6), // violet
        b'w' => (32, 5), // white
        _ => (33, 6),    // yellow
    }
}

#[inline(always)]
unsafe fn parse_attribute(bytes: &[u8]) -> (u16, u32) {
    let bytes = SliceWrapper::new(bytes);
    match bytes[0] {
        b'b' => (1, 6), // bright
        b'c' => (2, 5), // clear
        b'd' => match bytes[1] {
            b'a' => (3, 4), // dark
            b'i' => (4, 3), // dim
            b'o' => (5, 6), // dotted
            b'r' => (6, 4), // drab
            _ => (7, 4),    // dull
        },
        b'f' => (8, 5), // faded
        b'l' => (9, 5), // light
        b'm' => match bytes[1] {
            b'i' => (10, 8), // mirrored
            _ => (11, 5),    // muted
        },
        b'p' => match bytes[1] {
            b'a' => (12, 4), // pale
            b'l' => (13, 5), // plaid
            _ => (14, 4),    // posh
        },
        b's' => match bytes[1] {
            b'h' => (15, 5), // shiny
            _ => (16, 7),    // striped
        },
        b'v' => (17, 7), // vibrant
        _ => (18, 4),    // wavy
    }
}

fn validata_bag(bag: &str) -> anyhow::Result<()> {
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
