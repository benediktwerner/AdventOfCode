use std::{path::Path, time::Instant};

mod days;
mod utils;

trait Solver {
    fn day(&self) -> u8;
    fn is_input_safe(&self, input: &str) -> anyhow::Result<bool>;
    unsafe fn solve(&self, input: &str) -> (String, String);
}

fn input_path(day: u8) -> std::path::PathBuf {
    Path::new("..")
        .join(format!("day{:02}", day))
        .join("input.txt")
}

fn benchmark(solver: impl Solver, part1: impl ToString, part2: impl ToString) -> u128 {
    let path = input_path(solver.day());
    let input_string = match std::fs::read_to_string(path) {
        Ok(inp) => inp.replace("\r", ""),
        Err(error) => {
            panic!("Error while reading input file: {}", error);
        }
    };

    match solver.is_input_safe(&input_string) {
        Ok(true) => (),
        Ok(false) => {
            panic!("Unsafe input");
        }
        Err(error) => {
            panic!("Error while parsing input file: {}", error);
        }
    };

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

    end.duration_since(start).as_nanos() / COUNT as u128
}

fn main() {
    println!(
        "Time: {}",
        utils::format_duration(benchmark(days::day01::Solver, 1015476, 200878544))
    );
}
