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

pub fn get_solvers() -> Vec<Box<dyn crate::Solver>> {
    vec![
        Box::new(day01::Solver::new()),
        Box::new(day02::Solver::new()),
        Box::new(day03::Solver::new()),
        Box::new(day04::Solver::new()),
        Box::new(day05::Solver::new()),
        Box::new(day06::Solver::new()),
    ]
}
