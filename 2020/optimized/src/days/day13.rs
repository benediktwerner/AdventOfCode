use std::mem::MaybeUninit;

use anyhow::{bail, ensure};

use crate::{SliceWrapper, SliceWrapperMut};

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
        13
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(
            input.len() >= 10,
            "Input is too short. (< 10 characters including newline)"
        );
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
        let mut iter = input.lines();
        let first = iter.next();
        let second = iter.next();
        ensure!(iter.next().is_none(), "More than 2 lines");
        match (first, second) {
            (Some(first), Some(second)) => {
                ensure!(first.parse::<u32>().is_ok(), "Invalid start: '{}'", first);
                let count = second.split(',').count();
                ensure!(count > 2, "Less than 3 buses");
                ensure!(count <= 100, "More than 100 buses");
                let mut count = 0;
                for part in second.split(',') {
                    if part != "x" {
                        match part.parse::<u32>() {
                            Ok(bus) => {
                                ensure!(bus < 1000, "Bus over 1000");
                                count += 1;
                            }
                            Err(_) => bail!("Invalid bus: '{}'", part),
                        }
                    }
                }
                ensure!(count > 2, "Less than 3 specified buses");
                ensure!(count <= 16, "More than 16 specified buses");
            }
            _ => bail!("Input doesn't contain two lines"),
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let bytes = SliceWrapper::new(input.as_bytes());
        let mut i = 0;

        let mut start = 0;
        loop {
            start = start * 10 + (bytes[i] - b'0') as u32;
            i += 1;
            if bytes[i] == b'\n' {
                i += 1;
                break;
            }
        }

        let mut nums = [MaybeUninit::<(u32, u32)>::uninit(); 16];
        let mut nums = SliceWrapperMut::new(&mut nums);
        let mut len = 0;

        let mut min_arrival = u32::MAX;
        let mut min_bus = MaybeUninit::<u32>::uninit();
        let mut curr = 0;
        let mut prod: u64 = 1;
        let mut offset = 0;

        loop {
            curr = curr * 10 + (bytes[i] - b'0') as u32;
            i += 1;
            if bytes[i] == b',' || bytes[i] == b'\n' {
                let next_arrival = curr - start % curr;
                if next_arrival < min_arrival {
                    min_arrival = next_arrival;
                    min_bus = MaybeUninit::new(curr);
                }
                nums[len] = MaybeUninit::new((offset, curr));
                prod *= curr as u64;
                len += 1;

                if bytes[i] == b'\n' {
                    break;
                }

                curr = 0;
                offset += 1;
                i += 1;
                while bytes[i] == b'x' {
                    offset += 1;
                    i += 2;
                }
            }
        }

        let part1 = min_bus.assume_init() * min_arrival;

        let mut part2: u64 = 0;
        let nums = nums.assume_init(len);

        for &(i, bus) in nums.0 {
            let ni = prod / bus as u64;
            let mi = mod_inverse(ni, bus as u64) as u128;
            let i = prod - i as u64;
            let part = (i as u128 * ni as u128 * mi) % prod as u128;
            part2 += part as u64;
        }

        (part1.to_string(), (part2 % prod).to_string())
    }
}

#[inline(always)]
fn mod_inverse(a: u64, n: u64) -> u64 {
    // https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Modular_integers

    let mut t = 0;
    let mut r = n as i64;
    let mut new_t = 1;
    let mut new_r = (a % n) as i64;

    while new_r != 0 {
        let quotient = r / new_r;

        let tmp = new_t;
        new_t = t - quotient * new_t;
        t = tmp;

        let tmp = new_r;
        new_r = r - quotient * new_r;
        r = tmp;
    }

    debug_assert!(r == 1, "{} is not invertible mod {}", a, n);

    if t < 0 {
        t += n as i64;
    }

    t as u64
}
