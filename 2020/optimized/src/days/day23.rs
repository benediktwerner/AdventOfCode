use anyhow::{bail, ensure};

use crate::SliceWrapperMut;

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
        23
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(
            input.len() == 10,
            "Input has wrong length. (shuld be 10 characters including newline)"
        );
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            input.as_bytes()[9] == b'\n',
            "Input is missing newline at the end"
        );
        let mut has = [false; 9];
        for &c in &input.as_bytes()[..9] {
            if !(b'1'..=b'9').contains(&c) {
                bail!("Invalid cup: {}", c as char);
            }
            if has[(c - b'1') as usize] {
                bail!("Duplicate cup: {}", c as char);
            }
            has[(c - b'1') as usize] = true;
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let inp: Vec<u8> = input.as_bytes()[..9].iter().map(|&b| b - b'0').collect();
        let mut cups = vec![0_u32; 10];
        for i in 0..8 {
            cups[inp[i] as usize] = inp[i + 1] as u32;
        }
        cups[inp[8] as usize] = inp[0] as u32;

        let start = inp[0] as usize;

        let part1 = {
            let mut cups = cups.clone();

            play(&mut cups, start, 100);

            let mut out = String::with_capacity(9);
            let mut curr = cups[1];
            while curr != 1 {
                out.push((curr as u8 + b'0') as char);
                curr = cups[curr as usize];
            }
            out
        };

        let part2 = {
            cups[inp[8] as usize] = 10;
            for i in 10..1_000_000 {
                cups.push(i + 1);
            }
            cups.push(inp[0] as u32);

            play(&mut cups, start, 10_000_000);

            let a = cups[1];
            let b = cups[a as usize];
            a as u64 * b as u64
        };

        (part1, part2.to_string())
    }
}

unsafe fn play(cups: &mut [u32], mut curr: usize, iters: usize) {
    let m = cups.len() - 1;
    let mut cups = SliceWrapperMut::new(cups);
    for _ in 0..iters {
        let m1 = cups[curr] as usize;
        let m2 = cups[m1] as usize;
        let m3 = cups[m2] as usize;
        let mut dest = (curr + m - 2) % m + 1;
        while dest == m1 || dest == m2 || dest == m3 {
            dest = (dest + m - 2) % m + 1;
        }
        let last = cups[dest];
        cups[dest] = m1 as u32;
        cups[curr] = cups[m3];
        curr = cups[curr] as usize;
        cups[m3] = last;
    }
}
