use anyhow::ensure;

const SHINY_GOLD: u16 = (11 << 5) | 14;
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
        ensure!(
            input.len() >= 2,
            "Input is too short. (< 2 characters including newline)"
        );
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
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
        let mut bags = crate::SliceWrapperMut::new(&mut bags);

        let vec_init: [usize; 3] = std::mem::transmute(Vec::<u16>::new());
        let mut bags_reverse: [Vec<u16>; 2048] = std::mem::transmute([vec_init; 2048]);
        let mut bags_reverse = crate::SliceWrapperMut::<Vec<u16>>::new(&mut bags_reverse);

        let bytes = crate::SliceWrapper::new(input.as_bytes());
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
                    propagate_contains_gold(bag, &mut output.0, bags.0, bags_reverse.0);
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
    let bags = crate::SliceWrapper(bags);
    let mut bag_counts = crate::SliceWrapperMut(bag_counts);

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
    bags_reverse: &[Vec<u16>],
) {
    let mut bags = crate::SliceWrapperMut::new(bags);
    let bags_reverse = crate::SliceWrapper::<Vec<u16>>::new(bags_reverse);
    for &outer_bag in &bags_reverse[bag as usize] {
        if bags[outer_bag as usize] & (1 << HAS_GOLD_BIT) != 0 {
            continue;
        }

        *count += 1;
        bags[outer_bag as usize] |= 1 << HAS_GOLD_BIT;
        propagate_contains_gold(outer_bag, count, bags.0, bags_reverse.0);
    }
}

#[inline(always)]
unsafe fn parse_bag(bytes: crate::SliceWrapper<u8>, i: &mut u32) -> u16 {
    let (attr, len) = parse_attribute(&bytes[*i as usize..]);
    *i += len + 1;
    let (color, len) = parse_color(&bytes[*i as usize..]);
    *i += len;

    (color << 5) | attr
}

#[inline(always)]
unsafe fn parse_color(bytes: &[u8]) -> (u16, u32) {
    let bytes = crate::SliceWrapper::new(bytes);
    match bytes[0] {
        b'a' => (0, 4), // aqua
        b'b' => match bytes[3] {
            b'g' => (1, 5), // beige
            b'c' => (2, 5), // black
            b'e' => (3, 4), // blue
            b'n' => (4, 6), // bronze
            _ => (5, 5),    // brown
        },
        b'c' => match bytes[1] {
            b'h' => (6, 10), // chartreuse
            b'o' => (7, 5),  // coral
            b'r' => (8, 7),  // crimson
            _ => (9, 4),     // cyan
        },
        b'f' => (10, 7), // fuchsia
        b'g' => match bytes[2] {
            b'l' => (11, 4), // gold
            b'a' => (12, 4), // gray
            _ => (13, 5),    // green
        },
        b'i' => (14, 6), // indigo
        b'l' => match bytes[1] {
            b'a' => (15, 8), // lavender
            _ => (16, 4),    // lime
        },
        b'm' => match bytes[2] {
            b'g' => (17, 7), // magenta
            _ => (18, 6),    // maroon
        },
        b'o' => match bytes[1] {
            b'l' => (19, 5), // olive
            _ => (20, 6),    // orange
        },
        b'p' => match bytes[1] {
            b'l' => (21, 4), // plum
            _ => (22, 6),    // purple
        },
        b'r' => (23, 3), // red
        b's' => match bytes[1] {
            b'a' => (24, 6), // salmon
            _ => (25, 6),    // silver
        },
        b't' => match bytes[1] {
            b'a' => (26, 3), // tan
            b'e' => (27, 4), // teal
            b'o' => (28, 6), // tomato
            _ => (29, 9),    // turquoise
        },
        b'v' => (30, 6), // violet
        b'w' => (31, 5), // white
        _ => (32, 6),    // yellow
    }
}

#[inline(always)]
unsafe fn parse_attribute(bytes: &[u8]) -> (u16, u32) {
    let bytes = crate::SliceWrapper::new(bytes);
    match bytes[0] {
        b'b' => (0, 6), // bright
        b'c' => (1, 5), // clear
        b'd' => match bytes[1] {
            b'a' => (2, 4), // dark
            b'i' => (3, 3), // dim
            b'o' => (4, 6), // dotted
            b'r' => (5, 4), // drab
            _ => (6, 4),    // dull
        },
        b'f' => (7, 5), // faded
        b'l' => (8, 5), // light
        b'm' => match bytes[1] {
            b'i' => (9, 8), // mirrored
            _ => (10, 5),   // muted
        },
        b'p' => match bytes[1] {
            b'a' => (11, 4), // pale
            b'l' => (12, 5), // plaid
            _ => (13, 4),    // posh
        },
        b's' => match bytes[1] {
            b'h' => (14, 5), // shiny
            _ => (15, 7),    // striped
        },
        b'v' => (16, 7), // vibrant
        _ => (17, 4),    // wavy
    }
}
