use anyhow::{ensure, Context};

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
        1
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
        let mut count = 0;
        for line in input.lines() {
            count += 1;
            line.parse::<u32>()
                .with_context(|| format!("Failed to convert '{line}' to int"))?;
        }
        ensure!(count >= 4, "Fewer than 4 numbers");
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let inp = SliceWrapper::new(input.as_bytes());
        let mut i = 0;

        let mut a = read_num(inp, &mut i);
        let mut b = read_num(inp, &mut i);
        let mut c = read_num(inp, &mut i);
        let mut d = read_num(inp, &mut i);

        let mut part1 = (b > a) as u32 + (c > b) as u32;
        let mut part2 = 0;

        loop {
            part1 += (d > c) as u32;
            part2 += (d > a) as u32;
            if i == inp.len() {
                break;
            }
            a = read_num(inp, &mut i);
            part1 += (a > d) as u32;
            part2 += (a > b) as u32;
            if i == inp.len() {
                break;
            }
            b = read_num(inp, &mut i);
            part1 += (b > a) as u32;
            part2 += (b > c) as u32;
            if i == inp.len() {
                break;
            }
            c = read_num(inp, &mut i);
            part1 += (c > b) as u32;
            part2 += (c > d) as u32;
            if i == inp.len() {
                break;
            }
            d = read_num(inp, &mut i);
        }

        (part1.to_string(), part2.to_string())
    }
}

#[inline(always)]
fn read_num(s: SliceWrapper<u8>, i: &mut usize) -> u32 {
    let mut num = (s[*i] - b'0') as u32;
    *i += 1;
    loop {
        let c = s[*i];
        *i += 1;
        if c == b'\n' {
            return num;
        }
        num *= 10;
        num += (c - b'0') as u32;
    }
}
