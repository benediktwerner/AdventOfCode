use rand::seq::SliceRandom as _;
use std::{path::Path, time::Instant};

mod days;
mod utils;

trait Solver {
    type Input;
    type Output;

    fn parse_input(&self, input: &str) -> anyhow::Result<Self::Input>;
    fn is_input_safe(&self, input: &Self::Input) -> bool;
    unsafe fn solve(&self, input: Self::Input) -> Self::Output;
    unsafe fn solve_str(&self, input: &str) -> Self::Output;
}

fn input_path(day: u8) -> std::path::PathBuf {
    Path::new("..")
        .join(format!("day{:02}", day))
        .join("input.txt")
}

fn main() {
    let solver = days::day01::Solver;

    let path = input_path(1);
    let input_string = match std::fs::read_to_string(path) {
        Ok(inp) => inp,
        Err(error) => {
            eprintln!("Error while reading input file: {}", error);
            return;
        }
    };
    let input = match solver.parse_input(&input_string) {
        Ok(inp) => inp,
        Err(error) => {
            eprintln!("Error while parsing input file: {}", error);
            return;
        }
    };

    const COUNT: u128 = 10_000;
    let mut sum = 0;
    let mut rng = rand::thread_rng();

    for _ in 0..COUNT {
        let mut inp = input.clone();
        inp.shuffle(&mut rng);
        assert!(solver.is_input_safe(&inp), "Input unsafe");
        let start = Instant::now();
        let out = unsafe { solver.solve(inp) };
        let end = Instant::now();
        assert_eq!(out, (1015476, 200878544), "Wrong result");
        sum += end.duration_since(start).as_nanos();
    }

    println!("Time: {}", utils::format_duration(sum / COUNT));

    sum = 0;

    for _ in 0..COUNT {
        let inp = &input_string;
        let start = Instant::now();
        let out = unsafe { solver.solve_str(inp) };
        let end = Instant::now();
        assert_eq!(out, (1015476, 200878544), "Wrong result");
        sum += end.duration_since(start).as_nanos();
    }

    println!("Time: {}", utils::format_duration(sum / COUNT));
}
