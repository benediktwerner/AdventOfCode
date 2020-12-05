use std::{path::Path, time::Instant};

use anyhow::bail;

mod unreachable;

mod days;
mod utils;
mod slice_wrapper;

pub use slice_wrapper::*;

pub trait Solver {
    fn day(&self) -> u8;
    fn is_input_safe(&self, input: &str) -> anyhow::Result<bool>;
    /// # Safety
    /// This method is safe to call only if `self.is_input_safe(input)` returned `Ok(true)`
    unsafe fn solve(&self, input: &str) -> (String, String);
}

fn input_path(day: u8) -> std::path::PathBuf {
    Path::new("..")
        .join(format!("day{:02}", day))
        .join("input.txt")
}

fn add_newline(mut inp: String) -> String {
    if inp.as_bytes().last() != Some(&b'\n') {
        inp.push('\n');
    }
    inp
}

fn benchmark(
    solver: impl Solver,
    part1: impl ToString,
    part2: impl ToString,
) -> anyhow::Result<u128> {
    let path = input_path(solver.day());
    let input_string = match std::fs::read_to_string(path) {
        Ok(inp) => add_newline(inp.replace("\r", "")),
        Err(error) => {
            bail!("Error while reading input file: {}", error);
        }
    };

    match solver.is_input_safe(&input_string) {
        Ok(true) => (),
        Ok(false) => {
            bail!("Unsafe input");
        }
        Err(error) => {
            bail!("Error while parsing input file: {}", error);
        }
    };

    #[cfg(debug_assertions)]
    const COUNT: u32 = 1;
    #[cfg(not(debug_assertions))]
    const COUNT: u32 = 10_000;

    let expected = (part1.to_string(), part2.to_string());

    let inp = &input_string;
    let mut out = Default::default();

    let start = Instant::now();
    for _ in 0..COUNT {
        out = unsafe { solver.solve(inp) };
    }
    let end = Instant::now();

    assert_eq!(out, expected, "Wrong result");

    Ok(end.duration_since(start).as_nanos() / COUNT as u128)
}

fn main() {
    let _ = days::get_solvers();

    // let result = benchmark(days::day01::Solver::new(), 1015476, 200878544);
    // let result = benchmark(days::day02::Solver::new(), 439, 584);
    // let result = benchmark(days::day03::Solver::new(), 167, 736527114);
    // let result = benchmark(days::day04::Solver::new(), 192, 101);
    let result = benchmark(days::day05::Solver::new(), 938, 696);
    let time = match result {
        Ok(time) => time,
        Err(error) => {
            eprintln!("{}", error);
            return;
        }
    };

    println!("Time: {}", utils::format_duration(time));
}
