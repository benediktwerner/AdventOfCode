macro_rules! assert_solver_day {
    ($solver:expr) => {
        assert_eq!(
            format!("day{:02}.rs", crate::Solver::day(&$solver)),
            {
                let fname = file!();
                &fname[fname.len() - 8..]
            },
            "Solver in '{}' has incorrect Solver::day()",
            file!()
        );
    };
}

pub mod day01;
pub mod day02;
pub mod day05;
pub mod day09;

pub fn get_solvers() -> Vec<Box<dyn crate::Solver>> {
    vec![
        Box::new(day01::Solver::new()),
        Box::new(day02::Solver::new()),
        Box::new(day05::Solver::new()),
        Box::new(day09::Solver::new()),
    ]
}
