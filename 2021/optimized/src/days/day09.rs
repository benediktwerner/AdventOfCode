use std::mem::MaybeUninit;

use anyhow::{bail, ensure};
use rustc_hash::FxHashMap;

use crate::{unreachable::UncheckedOptionExt, SliceWrapper};

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
        9
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
        let line_len = match input.lines().next() {
            Some(line) => line.len(),
            None => bail!("No input"),
        };
        ensure!(line_len > 2, "Lines must be longer than 2");
        let mut count = 0;
        for line in input.lines() {
            count += 1;
            ensure!(line.len() == line_len, "Line with incorrect length");
            ensure!(
                line.as_bytes().iter().all(u8::is_ascii_digit),
                "Non-digit in line"
            );
        }
        ensure!(count > 2, "Must have more than 2 lines");
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let inp = SliceWrapper::new(input.as_bytes());

        let width = inp.0.iter().position(|c| *c == b'\n').unwrap_unchecked();
        let width1 = width + 1;
        let height = input.len() / width1;
        let mut basins = vec![MaybeUninit::<u32>::uninit(); width1 * height];
        let mut sizes = FxHashMap::default();

        for y in 0..height {
            for x in 0..width {
                let c = y * width1 + x;
                let mut v = inp[c];
                if v == b'9' {
                    continue;
                }
                if x > 0 && inp[y * width1 + x - 1] != b'9' {
                    let mut basin = (y * width1 + x - 1) as u32;
                    while basins[basin as usize].assume_init() != basin {
                        basin = basins[basin as usize].assume_init();
                    }
                    if inp[basin] <= v {
                        v = inp[basin];
                        *sizes.get_mut(&basin).unwrap_unchecked() += 1;
                        basins[c] = MaybeUninit::new(basin);
                    } else {
                        basins[basin as usize] = MaybeUninit::new(c as u32);
                        basins[c] = MaybeUninit::new(c as u32);
                        let size = sizes.remove(&basin).unwrap_unchecked();
                        basin = c as u32;
                        sizes.insert(basin, size + 1);
                    }

                    if y > 0 && inp[(y - 1) * width1 + x] != b'9' {
                        let mut basin2 = ((y - 1) * width1 + x) as u32;
                        while basins[basin2 as usize].assume_init() != basin2 {
                            basin2 = basins[basin2 as usize].assume_init();
                        }
                        if basin != basin2 {
                            if inp[basin2] <= v {
                                let size = sizes.remove(&basin).unwrap_unchecked();
                                *sizes.get_mut(&basin2).unwrap_unchecked() += size;
                                basins[basin as usize] = MaybeUninit::new(basin2);
                            } else {
                                let size = sizes.remove(&basin2).unwrap_unchecked();
                                *sizes.get_mut(&basin).unwrap_unchecked() += size;
                                basins[basin2 as usize] = MaybeUninit::new(basin);
                            }
                        }
                    }
                } else if y > 0 && inp[(y - 1) * width1 + x] != b'9' {
                    let mut basin = ((y - 1) * width1 + x) as u32;
                    while basins[basin as usize].assume_init() != basin {
                        basin = basins[basin as usize].assume_init();
                    }
                    if inp[basin] <= v {
                        *sizes.get_mut(&basin).unwrap_unchecked() += 1;
                        basins[c] = MaybeUninit::new(basin);
                    } else {
                        basins[basin as usize] = MaybeUninit::new(c as u32);
                        basins[c] = MaybeUninit::new(c as u32);
                        let size = sizes.remove(&basin).unwrap_unchecked();
                        basin = c as u32;
                        sizes.insert(basin, size + 1);
                    }
                } else {
                    basins[c] = MaybeUninit::new(c as u32);
                    sizes.insert(c as u32, 1);
                }
            }
        }

        let mut part1 = 0_u32;
        let mut part2 = (0_u32, 0_u32, 0_u32);
        for (c, size) in sizes {
            part1 += (inp[c as usize] - b'0') as u32 + 1;
            if size > part2.2 {
                part2.0 = part2.1;
                part2.1 = part2.2;
                part2.2 = size;
            } else if size > part2.1 {
                part2.0 = part2.1;
                part2.1 = size;
            } else if size > part2.0 {
                part2.0 = size;
            }
        }

        (part1.to_string(), (part2.0 * part2.1 * part2.2).to_string())
    }
}
