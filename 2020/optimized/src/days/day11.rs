use anyhow::ensure;

use crate::SliceWrapper;

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
        11
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(
            input.len() >= 10,
            "Input is too short. (< 10 characters including newline)"
        );
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
        let len = input.lines().count();
        ensure!(len > 3, "Less than 3 lines");
        ensure!(len <= 100, "More than 100 lines");
        for line in input.lines() {
            match line.parse::<u32>() {
                Ok(num) => ensure!(num <= 999, "Number too large (>999): '{}'", num),
                Err(_) => anyhow::bail!("Invalid number: '{}'", line),
            }
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let _bytes = SliceWrapper::new(input.as_bytes());

        todo!()
    }
}
