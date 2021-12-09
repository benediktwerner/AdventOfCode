use anyhow::{bail, ensure};

use crate::{unreachable::UncheckedOptionExt, SliceWrapperMut};

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
        let mut inp = input.as_bytes().to_vec();
        let mut inp = SliceWrapperMut::new(&mut inp);

        let width = inp.0.iter().position(|c| *c == b'\n').unwrap_unchecked();

        let width1 = width + 1;
        let height = input.len() / width1;
        let mut part1 = 0_u32;
        let mut part2 = (0_u32, 0_u32, 0_u32);

        for y in 0..height {
            for x in 0..width {
                let c = inp[y * width1 + x];
                if c == b'9' {
                    continue;
                }
                let mut todo = vec![(x, y)];
                let mut min = c;
                let mut size = 0;
                inp[y * width1 + x] = b'9';
                while let Some((x, y)) = todo.pop() {
                    size += 1;
                    if x > 0 && inp[y * width1 + x - 1] != b'9' {
                        todo.push((x - 1, y));
                        min = std::cmp::min(min, inp[y * width1 + x - 1]);
                        inp[y * width1 + x - 1] = b'9';
                    }
                    if x < width - 1 && inp[y * width1 + x + 1] != b'9' {
                        todo.push((x + 1, y));
                        min = std::cmp::min(min, inp[y * width1 + x + 1]);
                        inp[y * width1 + x + 1] = b'9';
                    }
                    if y > 0 && inp[(y - 1) * width1 + x] != b'9' {
                        todo.push((x, y - 1));
                        min = std::cmp::min(min, inp[(y - 1) * width1 + x]);
                        inp[(y - 1) * width1 + x] = b'9';
                    }
                    if y < height - 1 && inp[(y + 1) * width1 + x] != b'9' {
                        todo.push((x, y + 1));
                        min = std::cmp::min(min, inp[(y + 1) * width1 + x]);
                        inp[(y + 1) * width1 + x] = b'9';
                    }
                }
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
                part1 += (min - b'0') as u32 + 1;
            }
        }

        (part1.to_string(), (part2.0 * part2.1 * part2.2).to_string())
    }
}
