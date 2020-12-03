use anyhow::{bail, ensure};

use crate::unreachable::UncheckedOptionExt;

pub struct Solver;

impl crate::Solver for Solver {
    fn day(&self) -> u8 {
        3
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<bool> {
        ensure!(
            input.len() < u32::MAX as usize,
            "Input longer than u32::MAX: {}",
            input.len()
        );
        let mut lines = input.lines();
        let first = match lines.next() {
            Some(line) => line,
            None => bail!("Input has no lines"),
        };
        let length = first.len();
        ensure!(length > 0, "First line is empty");
        for line in lines {
            ensure!(
                line.len() == length,
                "Line has non-uniform length. Expected: {}. Found: {}",
                length,
                line.len()
            );
        }
        Ok(true)
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let mut output = (0, 1);

        let bytes = input.as_bytes();
        let width = bytes.iter().position(|c| *c == b'\n').unchecked_unwrap() as u32;
        let length = bytes.len() as u32;
        let bytes = crate::SliceWrapper::new(bytes);

        const SLOPES: [(u32, u32); 5] = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)];
        const PART1_SLOPE: (u32, u32) = (3, 1);

        for &(dx, dy) in &SLOPES {
            let mut i: u32 = 0;
            let mut x: u32 = 0;
            let mut count: u32 = 0;

            while i < length {
                if bytes[i] == b'#' {
                    count += 1;
                }

                x += dx;
                i += dy * (width + 1) + dx;
                if x >= width {
                    x -= width;
                    i -= width;
                }
            }

            if (dx, dy) == PART1_SLOPE {
                output.0 = count;
            }

            output.1 *= count;
        }

        (output.0.to_string(), output.1.to_string())
    }
}
