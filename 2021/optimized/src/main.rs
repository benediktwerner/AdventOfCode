#![allow(clippy::inline_always)]
#![allow(clippy::missing_errors_doc)]

use std::{ops::Deref, path::Path, time::Instant};

use anyhow::{bail, ensure};

mod days;
mod slice_wrapper;
mod utils;

use clap::{
    builder::{NonEmptyStringValueParser, RangedU64ValueParser},
    Arg, ArgAction, Command,
};
use days::get_solvers;
pub use slice_wrapper::*;

const DEFAULT_ITERATIONS: u64 = if cfg!(debug_assertions) { 1 } else { 1000 };

pub trait Solver {
    fn day(&self) -> u8;
    fn is_input_safe(&self, input: &str) -> anyhow::Result<()>;
    /// # Safety
    /// This method is safe to call only if `self.is_input_safe(input)` returned `Ok(true)`
    unsafe fn solve(&self, input: &str) -> (String, String);

    fn get_input(&self, directory: Option<&str>) -> anyhow::Result<String> {
        let path = input_path(self.day(), directory);
        let input_string = match std::fs::read_to_string(path) {
            Ok(inp) => add_newline(inp.replace('\r', "")),
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
        Path::new(dir).join(format!("day{day:02}.txt"))
    } else {
        Path::new("..")
            .join(format!("day{day:02}"))
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
    let iterations = iterations.unwrap_or(DEFAULT_ITERATIONS);

    println!("Benchmarking day {}", solver.day());
    println!("{iterations} iteration(s)");
    if expected.is_none() {
        println!("Not checking results");
    }
    println!();

    let inp = &solver.get_input(input_directory)?;
    let mut out = Default::default();

    let start = Instant::now();
    #[cfg(target_arch = "x86_64")]
    let startc = unsafe { std::arch::x86_64::_rdtsc() };
    for _ in 0..iterations {
        out = unsafe { solver.solve(inp) };
    }
    #[cfg(target_arch = "x86_64")]
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

    #[cfg(target_arch = "x86_64")]
    println!("Cycles: {}", (endc - startc) / iterations);
    println!("Time: {nanos} = {time}");

    Ok(())
}

fn benchmark_all(
    solvers: &[Box<dyn Solver>],
    expected: &[(String, String)],
    iterations: Option<u64>,
    input_directory: Option<&str>,
) -> anyhow::Result<()> {
    let iterations = iterations.unwrap_or(DEFAULT_ITERATIONS);

    println!("\nBenchmarking all days");
    println!("{iterations} iterations each");
    println!();
    println!(
        "Day      {: >16}{: >16}{: >16}{: >16}{: >16}\n",
        "Time (ns)", "Time", "Cycles", "Part 1", "Part 2"
    );

    let mut inputs = Vec::new();
    let mut nanos_sum = 0;
    let mut cycles_sum = 0;

    for solver in solvers {
        let input = solver.get_input(input_directory)?;
        let mut out = Default::default();

        let start = Instant::now();
        #[cfg(target_arch = "x86_64")]
        let startc = unsafe { std::arch::x86_64::_rdtsc() };
        for _ in 0..iterations {
            out = unsafe { solver.solve(&input) };
        }
        #[cfg(target_arch = "x86_64")]
        let endc = unsafe { std::arch::x86_64::_rdtsc() };
        let duration = start.elapsed();

        let nanos = duration.as_nanos() / iterations as u128;
        let time = utils::format_duration(nanos);
        #[cfg(target_arch = "x86_64")]
        let cycles = (endc - startc) / iterations;
        #[cfg(not(target_arch = "x86_64"))]
        let cycles = 0;

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
                println!("       => Wrong result: {out:?} vs {expected:?} (expected)");
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
    println!("\nEverything together: {nanos} = {time}\n");

    Ok(())
}

fn parse_expected(path: impl AsRef<Path>) -> Option<Vec<(String, String)>> {
    let mut result = Vec::new();
    let path = path.as_ref();

    let content = match std::fs::read_to_string(path) {
        Ok(x) => x,
        Err(error) => {
            eprintln!("Failed to read {path:?}: {error}");
            return None;
        }
    };

    for (i, line) in content.lines().enumerate() {
        let mut iter = line.split_whitespace();
        if let (Some(a), Some(b)) = (iter.next(), iter.next()) {
            result.push((a.to_string(), b.to_string()));
        } else {
            eprintln!("Failed to parse {path:?}:{i}: Expected two space separated values\n");
            return None;
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
    let solvers = get_solvers();

    let args = Command::new("aoc-optimized")
        .arg(
            Arg::new("all")
                .long("all")
                .short('a')
                .action(ArgAction::SetTrue)
                .help("Benchmark all days"),
        )
        .arg(
            Arg::new("iterations")
                .long("iterations")
                .alias("iters")
                .short('i')
                .value_parser(RangedU64ValueParser::<u64>::new())
                .help("Number of iterations between timings"),
        )
        .arg(
            Arg::new("day")
                .long("day")
                .short('d')
                .value_parser(RangedU64ValueParser::<usize>::from(
                    1..=solvers.len() as u64,
                ))
                .help("Benchmark a single day"),
        )
        .arg(
            Arg::new("no-check")
                .long("no-check")
                .action(ArgAction::SetTrue)
                .help("Don't check if results are correct"),
        )
        .arg(
            Arg::new("input-directory")
                .long("input-directory")
                .alias("input-dir")
                .value_parser(NonEmptyStringValueParser::new())
                .value_name("DIR")
                .help("Directory for inputs. Inputs are expected as dayXX.txt. Expected output can optionally be provided in `expected.txt` or using --expected-file"),
        )
        .arg(
            Arg::new("expected-file")
                .long("expected-file")
                .value_parser(NonEmptyStringValueParser::new())
                .value_name("FILE")
                .help("File for expected inputs. Defaults to expected.txt"),
        )
        .get_matches();

    let input_dir = args.get_one::<String>("input-directory").map(Deref::deref);
    let expected_file = args
        .get_one::<String>("expected-file")
        .map_or("expected.txt", Deref::deref);

    let expected = if args.get_flag("no-check") {
        Vec::new()
    } else {
        get_expected(input_dir, expected_file).unwrap_or_default()
    };

    let iterations = args.get_one::<u64>("iterations").copied();

    if args.get_flag("all") {
        benchmark_all(&solvers, &expected, iterations, input_dir)
    } else if let Some(day) = args.get_one::<usize>("day").copied() {
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
        eprintln!("{error}");
    }
}
