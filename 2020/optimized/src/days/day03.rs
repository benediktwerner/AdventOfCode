use anyhow::{bail, ensure};

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
        3
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(
            input.len() < u32::MAX as usize,
            "Input longer than u32::MAX: {}",
            input.len()
        );
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        let mut lines = input.lines();
        let Some(first) = lines.next() else {
            bail!("Input has no lines")
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
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        const SLOPES: [(u32, u32); 5] = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)];
        const PART1_SLOPE: (u32, u32) = (3, 1);

        let mut output = (0, 1);

        let bytes = input.as_bytes();
        let width = bytes.iter().position(|c| *c == b'\n').unwrap_unchecked() as u32;
        let length = bytes.len() as u32;
        let bytes = crate::SliceWrapper::new(bytes);

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
