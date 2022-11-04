use std::str::FromStr;

use anyhow::{bail, ensure};
use itertools::Itertools;

use crate::SliceWrapperMut;

const SIZE: usize = 1024;

pub struct Solver(());

impl Solver {
    pub fn new() -> Self {
        let solver = Self(());
        assert_solver_day!(solver);
        solver
    }
}

impl crate::Solver for Solver {
    fn day(&self) -> u8 {
        5
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
        for line in input.lines() {
            match line
                .split(" -> ")
                .filter_map(|p| p.split(',').map(usize::from_str).collect_tuple())
                .collect_tuple()
            {
                Some(((Ok(x1), Ok(y1)), (Ok(x2), Ok(y2)))) => {
                    ensure!(x1 < SIZE, "x1 > {}: {}", SIZE, x1);
                    ensure!(x2 < SIZE, "x2 > {}: {}", SIZE, x2);
                    ensure!(y1 < SIZE, "y1 > {}: {}", SIZE, y1);
                    ensure!(y2 < SIZE, "y2 > {}: {}", SIZE, y2);
                }
                _ => bail!("Invalid line: {}", line),
            }
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let mut grid1 = vec![0_u8; SIZE * SIZE];
        let mut grid2 = vec![0_u8; SIZE * SIZE];
        let mut grid1 = SliceWrapperMut::new(&mut grid1);
        let mut grid2 = SliceWrapperMut::new(&mut grid2);
        let mut part1 = 0;
        let mut part2 = 0;
        for line in input.lines() {
            let ((x1, y1), (x2, y2)) = line
                .split(" -> ")
                .map(|p| {
                    p.split(',')
                        .map(|x| x.parse::<usize>().unwrap_unchecked())
                        .collect_tuple()
                        .unwrap_unchecked()
                })
                .collect_tuple()
                .unwrap_unchecked();
            if x1 == x2 {
                let x = x1;
                for y in y1.min(y2)..=y1.max(y2) {
                    if grid1[x + y * SIZE] == 0 {
                        grid1[x + y * SIZE] += 1;
                    } else if grid1[x + y * SIZE] == 1 {
                        grid1[x + y * SIZE] += 1;
                        part1 += 1;
                    }
                    if grid2[x + y * SIZE] == 0 {
                        grid2[x + y * SIZE] += 1;
                    } else if grid2[x + y * SIZE] == 1 {
                        grid2[x + y * SIZE] += 1;
                        part2 += 1;
                    }
                }
            } else if y1 == y2 {
                let y = y1;
                for x in x1.min(x2)..=x1.max(x2) {
                    if grid1[x + y * SIZE] == 0 {
                        grid1[x + y * SIZE] += 1;
                    } else if grid1[x + y * SIZE] == 1 {
                        grid1[x + y * SIZE] += 1;
                        part1 += 1;
                    }
                    if grid2[x + y * SIZE] == 0 {
                        grid2[x + y * SIZE] += 1;
                    } else if grid2[x + y * SIZE] == 1 {
                        grid2[x + y * SIZE] += 1;
                        part2 += 1;
                    }
                }
            } else {
                let mut x = x1;
                let mut y = y1;
                let xd = if x1 < x2 { 1 } else { -1 };
                let yd = if y1 < y2 { 1 } else { -1 };
                loop {
                    if grid2[x + y * SIZE] == 0 {
                        grid2[x + y * SIZE] += 1;
                    } else if grid2[x + y * SIZE] == 1 {
                        grid2[x + y * SIZE] += 1;
                        part2 += 1;
                    }
                    if x == x2 {
                        break;
                    }
                    x = (x as isize + xd) as usize;
                    y = (y as isize + yd) as usize;
                }
            }
        }

        (part1.to_string(), part2.to_string())
    }
}
