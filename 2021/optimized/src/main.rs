#![allow(unstable_name_collisions)]

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

    fn get_input(&self, directory: Option<&str>) -> anyhow::Result<String> {
        let path = input_path(self.day(), directory);
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

fn input_path(day: u8, directory: Option<&str>) -> std::path::PathBuf {
    if let Some(dir) = directory {
        Path::new(dir).join(format!("day{:02}.txt", day))
    } else {
        Path::new("..")
            .join(format!("day{:02}", day))
            .join("input.txt")
    }
}

fn add_newline(mut inp: String) -> String {
    if inp.as_bytes().last() != Some(&b'\n') {
        inp.push('\n');
    }
    inp
}

fn benchmark(
    solver: &dyn Solver,
    expected: Option<(String, String)>,
    iterations: Option<u64>,
    input_directory: Option<&str>,
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

    let inp = &solver.get_input(input_directory)?;
    let mut out = Default::default();

    let start = Instant::now();
    let startc = unsafe { std::arch::x86_64::_rdtsc() };
    for _ in 0..iterations {
        out = unsafe { solver.solve(inp) };
    }
    let endc = unsafe { std::arch::x86_64::_rdtsc() };
    let duration = start.elapsed();

    if let Some(expected) = expected {
        ensure!(
            out == expected,
            "Wrong result: {:?} vs {:?} (expected)",
            out,
            expected
        );
    }

    let (nanos, time) = utils::format_duration(duration.as_nanos() / iterations as u128);

    println!("Cylcles: {}", (endc - startc) / iterations);
    println!("Time: {} = {}", nanos, time);

    Ok(())
}

fn benchmark_all(
    solvers: Vec<Box<dyn Solver>>,
    expected: &[(String, String)],
    iterations: Option<u64>,
    input_directory: Option<&str>,
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
        let input = solver.get_input(input_directory)?;
        let mut out = Default::default();

        let start = Instant::now();
        let startc = unsafe { std::arch::x86_64::_rdtsc() };
        for _ in 0..iterations {
            out = unsafe { solver.solve(&input) };
        }
        let endc = unsafe { std::arch::x86_64::_rdtsc() };
        let duration = start.elapsed();

        let nanos = duration.as_nanos() / iterations as u128;
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
            if out != *expected {
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
    let duration = start.elapsed();

    let nanos = duration.as_nanos() / iterations as u128;
    let (nanos, time) = utils::format_duration(nanos);
    println!("\nEverything together: {} = {}\n", nanos, time);

    Ok(())
}

fn parse_expected(path: impl AsRef<Path>) -> Option<Vec<(String, String)>> {
    let mut result = Vec::new();
    let path = path.as_ref();

    let content = match std::fs::read_to_string(path) {
        Ok(x) => x,
        Err(error) => {
            eprintln!("Failed to read {:?}: {}", path, error);
            return None;
        }
    };

    for (i, line) in content.lines().enumerate() {
        let mut iter = line.split_whitespace();
        match (iter.next(), iter.next()) {
            (Some(a), Some(b)) => {
                result.push((a.to_string(), b.to_string()));
            }
            _ => {
                eprintln!(
                    "Failed to parse {:?}:{}: Expected two space separated values\n",
                    path, i
                );
                return None;
            }
        }
    }
    Some(result)
}

fn get_expected(dir: Option<&str>, path: &str) -> Option<Vec<(String, String)>> {
    if let Some(dir) = dir {
        let path = Path::new(dir).join(path);
        if path.is_file() {
            parse_expected(&path)
        } else {
            None
        }
    } else if Path::new(path).is_file() {
        parse_expected(path)
    } else {
        None
    }
}

fn run() -> anyhow::Result<()> {
    let args = App::new("aoc-optimized")
        .arg(Arg::with_name("all").long("all").short("a").help("Benchmark all days"))
        .arg(
            Arg::with_name("iterations")
                .long("iterations")
                .alias("iters")
                .short("i")
                .takes_value(true)
                .help("Number of iterations between timings")
        )
        .arg(
            Arg::with_name("day")
                .long("day")
                .short("d")
                .takes_value(true)
                .help("Benchmark a single day"),
        )
        .arg(
            Arg::with_name("no-check")
                .long("no-check")
                .help("Don't check if results are correct"),
        )
        .arg(
            Arg::with_name("input-directory")
                .long("input-directory")
                .alias("input-dir")
                .takes_value(true)
                .value_name("DIR")
                .help("Directory for inputs. Inputs are expected as dayXX.txt. Expected output can optionally be provided in `expected.txt` or using --expected-file"),
        )
        .arg(
            Arg::with_name("expected-file")
                .long("expected-file")
                .takes_value(true)
                .value_name("FILE")
                .help("File for expected inputs. Defaults to expected.txt"),
        )
        .get_matches();

    let input_dir = args.value_of("input-directory");
    let expected_file = args.value_of("expected-file").unwrap_or("expected.txt");

    let expected = if args.is_present("no-check") {
        Vec::new()
    } else {
        get_expected(input_dir, expected_file).unwrap_or_default()
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

    let solvers = get_solvers();
    if args.is_present("all") {
        benchmark_all(solvers, &expected, iterations, input_dir)
    } else if let Some(day) = args.value_of("day") {
        let day = day.parse::<usize>().context("Day is not a valid number")?;
        ensure!(
            1 <= day && day <= solvers.len(),
            "Day out of range. It must be between 1 and {}.",
            solvers.len()
        );
        benchmark(
            &*solvers[day - 1],
            expected.get(day - 1).cloned(),
            iterations,
            input_dir,
        )
    } else {
        let day = solvers.len() - 1;
        benchmark(
            &*solvers[day],
            expected.get(day).cloned(),
            iterations,
            input_dir,
        )
    }
}

fn main() {
    if let Err(error) = run() {
        eprintln!("{}", error);
    }
}
