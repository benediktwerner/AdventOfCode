use std::time::Instant;

use input::read_input;

mod days;
mod input;
mod utils;

trait Solver {
    type Input;
    type Output;

    fn parse_input(&self, input: &[String]) -> anyhow::Result<Self::Input>;
    fn is_input_safe(&self, input: &Self::Input) -> bool;
    unsafe fn solve(&self, input: Self::Input) -> Self::Output;
}

fn main() {
    let solver = days::day01::Solver;
    let input = match solver.parse_input(&read_input(1)) {
        Ok(inp) => inp,
        Err(error) => {
            println!("Error while parsing input: {}", error);
            return;
        }
    };

    const COUNT: u128 = 10_000;
    let mut sum = 0;
    let mut rng = rand::thread_rng();

    for _ in 0..COUNT {
        use rand::seq::SliceRandom;
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

    // println!("Part 1: {}", out.0);
    // println!("Part 2: {}", out.1);
    // println!("Time: {}", utils::format_duration(end.duration_since(start).as_nanos()));
}
