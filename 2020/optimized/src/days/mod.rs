#[macro_use]
macro_rules! assert_solver_day {
    ($solver:expr) => {
        assert_eq!(format!("src/days/day{:02}.rs", crate::Solver::day(&$solver)), file!(), "Solver in '{}' has incorrect Solver::day()", file!());
    };
}

pub mod day01;
pub mod day02;
pub mod day03;
pub mod day04;
pub mod day05;
pub mod day06;
pub mod day07;
pub mod day08;
pub mod day09;
pub mod day10;
pub mod day11;
pub mod day12;
pub mod day13;

pub fn get_solvers() -> Vec<Box<dyn crate::Solver>> {
    vec![
        Box::new(day01::Solver::new()),
        Box::new(day02::Solver::new()),
        Box::new(day03::Solver::new()),
        Box::new(day04::Solver::new()),
        Box::new(day05::Solver::new()),
        Box::new(day06::Solver::new()),
        Box::new(day07::Solver::new()),
        Box::new(day08::Solver::new()),
        Box::new(day09::Solver::new()),
        Box::new(day10::Solver::new()),
        Box::new(day11::Solver::new()),
        Box::new(day12::Solver::new()),
        Box::new(day13::Solver::new()),
    ]
}
