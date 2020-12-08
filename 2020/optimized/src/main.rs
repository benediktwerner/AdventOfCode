use std::{path::Path, time::Instant};

use anyhow::{bail, ensure, Context};

mod unreachable;

mod days;
mod slice_wrapper;
mod utils;

use clap::{App, Arg};
use days::get_solvers;
pub use slice_wrapper::*;

pub trait Solver {
    fn day(&self) -> u8;
    fn is_input_safe(&self, input: &str) -> anyhow::Result<()>;
    /// # Safety
    /// This method is safe to call only if `self.is_input_safe(input)` returned `Ok(true)`
    unsafe fn solve(&self, input: &str) -> (String, String);

    fn get_input(&self) -> anyhow::Result<String> {
        let path = input_path(self.day());
        let input_string = match std::fs::read_to_string(path) {
            Ok(inp) => add_newline(inp.replace("\r", "")),
            Err(error) => {
                bail!("Error while reading input file: {}", error);
            }
        };

        if let Err(error) = self.is_input_safe(&input_string) {
            bail!("Error while parsing input file: {}", error);
        }
        Ok(input_string)
    }
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
    solver: &dyn Solver,
    expected: Option<(u32, u32)>,
    iterations: Option<u64>,
) -> anyhow::Result<()> {
    #[cfg(debug_assertions)]
    const ITERATIONS: u64 = 1;
    #[cfg(not(debug_assertions))]
    const ITERATIONS: u64 = 1000;

    let iterations = iterations.unwrap_or(ITERATIONS);

    println!("Benchmarking day {}", solver.day());
    println!("{} iteration(s)", iterations);
    if expected.is_none() {
        println!("Not checking results");
    }
    println!();

    let inp = &solver.get_input()?;
    let mut out = Default::default();

    let start = Instant::now();
    let startc = unsafe { std::arch::x86_64::_rdtsc() };
    for _ in 0..iterations {
        out = unsafe { solver.solve(inp) };
    }
    let endc = unsafe { std::arch::x86_64::_rdtsc() };
    let end = Instant::now();

    if let Some(expected) = expected {
        let expected = (expected.0.to_string(), expected.1.to_string());
        ensure!(
            out == expected,
            "Wrong result: {:?} vs {:?} (expected)",
            out,
            expected
        );
    }

    let (nanos, time) =
        utils::format_duration(end.duration_since(start).as_nanos() / iterations as u128);

    println!("Cylcles: {}", (endc - startc) / iterations);
    println!("Time: {} = {}", nanos, time);

    Ok(())
}

fn benchmark_all(
    solvers: Vec<Box<dyn Solver>>,
    expected: &[(u32, u32)],
    iterations: Option<u64>,
) -> anyhow::Result<()> {
    #[cfg(debug_assertions)]
    const ITERATIONS: u64 = 1;
    #[cfg(not(debug_assertions))]
    const ITERATIONS: u64 = 1000;

    let iterations = iterations.unwrap_or(ITERATIONS);

    println!("\nBenchmarking all days");
    println!("{} iterations each", iterations);
    println!();
    println!(
        "Day      {: >16}{: >16}{: >16}{: >16}{: >16}\n",
        "Time (ns)", "Time", "Cycles", "Part 1", "Part 2"
    );

    let mut inputs = Vec::new();
    let mut nanos_sum = 0;
    let mut cycles_sum = 0;

    for solver in &solvers {
        let input = solver.get_input()?;
        let mut out = Default::default();

        let start = Instant::now();
        let startc = unsafe { std::arch::x86_64::_rdtsc() };
        for _ in 0..iterations {
            out = unsafe { solver.solve(&input) };
        }
        let endc = unsafe { std::arch::x86_64::_rdtsc() };
        let end = Instant::now();

        let nanos = end.duration_since(start).as_nanos() / iterations as u128;
        let time = utils::format_duration(nanos);
        let cycles = (endc - startc) / iterations;

        println!(
            "Day {:02}   {: >16}{: >16}{: >16}{: >16}{: >16}",
            solver.day(),
            time.0,
            time.1,
            cycles,
            out.0,
            out.1,
        );

        if let Some(expected) = expected.get(solver.day() as usize - 1) {
            let expected = (expected.0.to_string(), expected.1.to_string());
            if out != expected {
                println!(
                    "       => Wrong result: {:?} vs {:?} (expected)",
                    out, expected
                );
            }
        }

        nanos_sum += nanos;
        cycles_sum += cycles;
        inputs.push(input);
    }

    let time = utils::format_duration(nanos_sum);
    println!(
        "\nTotal    {: >16}{: >16}{: >16}",
        time.0, time.1, cycles_sum
    );

    let start = Instant::now();
    for (solver, input) in solvers.iter().zip(&inputs) {
        for _ in 0..iterations {
            unsafe {
                solver.solve(input);
            }
        }
    }
    let end = Instant::now();

    let nanos = end.duration_since(start).as_nanos() / iterations as u128;
    let (nanos, time) = utils::format_duration(nanos);
    println!("\nEverything together: {} = {}\n", nanos, time);

    Ok(())
}

static EXPECTED: [(u32, u32); 7] = [
    (1015476, 200878544),
    (439, 584),
    (167, 736527114),
    (192, 101),
    (938, 696),
    (7027, 3579),
    (289, 30055),
];

fn run() -> anyhow::Result<()> {
    let args = App::new("aoc-optimized")
    .arg(Arg::with_name("all").long("all").help("Benchmark all"))
    .arg(Arg::with_name("iterations").long("iterations").alias("iters").short("i").takes_value(true))
        .arg(
            Arg::with_name("day")
                .long("day")
                .takes_value(true)
                .help("Benchmark a single day"),
        )
        .arg(
            Arg::with_name("no-check-results")
                .long("no-check-results")
                .help("Don't validate results"),
        )
        .get_matches();

    let solvers = get_solvers();
    let expected: &[(u32, u32)] = if args.is_present("no-check-results") {
        Default::default()
    } else {
        &EXPECTED
    };

    let iterations = if let Some(iters) = args.value_of("iterations") {
        Some(
            iters
                .parse::<u64>()
                .context("Iterations count is not a valid number")?,
        )
    } else {
        None
    };

    if args.is_present("all") {
        benchmark_all(solvers, expected, iterations)
    } else if let Some(day) = args.value_of("day") {
        let day = day.parse::<usize>().context("Day is not a valid number")?;
        ensure!(
            1 <= day && day <= solvers.len(),
            "Day out of range. It must be between 1 and {}.",
            solvers.len()
        );
        benchmark(
            &*solvers[day - 1],
            expected.get(day - 1).copied(),
            iterations,
        )
    } else {
        let day = solvers.len() - 1;
        benchmark(&*solvers[day], expected.get(day).copied(), iterations)
    }
}

fn main() {
    if let Err(error) = run() {
        eprintln!("{}", error);
    }
}
