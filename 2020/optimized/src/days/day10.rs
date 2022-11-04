use std::mem::MaybeUninit;

use anyhow::ensure;

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
        10
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
        let len = input.lines().count();
        ensure!(len > 3, "Less than 3 lines");
        ensure!(len <= 100, "More than 100 lines");
        for line in input.lines() {
            match line.parse::<u32>() {
                Ok(num) => ensure!(num <= 999, "Number too large (>999): '{}'", num),
                Err(_) => anyhow::bail!("Invalid number: '{}'", line),
            }
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let bytes = SliceWrapper::new(input.as_bytes());
        let mut i = 0;

        let mut numbers_present = [false; 1000];
        let mut numbers_present = SliceWrapperMut::new(&mut numbers_present);

        while i < bytes.len() {
            let mut num = (bytes[i] - b'0') as u32;

            if bytes[i + 1] == b'\n' {
                i += 2;
            } else {
                num = num * 10 + (bytes[i + 1] - b'0') as u32;
                if bytes[i + 2] == b'\n' {
                    i += 3;
                } else {
                    num = num * 10 + (bytes[i + 2] - b'0') as u32;
                    i += 4;
                }
            }

            numbers_present[num as usize] = true;
        }

        let mut numbers = [MaybeUninit::<u32>::uninit(); 100];
        let mut numbers = SliceWrapperMut::new(&mut numbers);
        let mut len = 1;

        for (i, &n) in numbers_present.0.iter().enumerate() {
            if n {
                numbers[len] = MaybeUninit::new(i as u32);
                len += 1;
            }
        }

        numbers[0] = MaybeUninit::new(0);
        numbers[len] = MaybeUninit::new(numbers[len - 1].assume_init() + 3);
        len += 1;

        let numbers: SliceWrapper<u32> = numbers.assume_init(len);

        let mut arrangements = [MaybeUninit::<u64>::uninit(); 100];
        let mut arrangements = SliceWrapperMut::new(&mut arrangements);
        arrangements[0] = MaybeUninit::new(1);
        arrangements[1] = MaybeUninit::new(1);

        let mut ones = 0;
        let mut threes = 0;
        let mut curr: u64 = 1;

        check_ones_threes(numbers[1] - numbers[0], &mut ones, &mut threes);
        check_ones_threes(numbers[2] - numbers[1], &mut ones, &mut threes);
        if numbers[2] <= 3_u32 {
            curr += 1;
        }
        arrangements[2] = MaybeUninit::new(curr);

        for i in 1..len {
            check_ones_threes(numbers[i] - numbers[i - 1], &mut ones, &mut threes);

            if numbers[i] - numbers[i - 2] <= 3 {
                curr += arrangements[i - 2].assume_init();
                if numbers[i] - numbers[i - 3] <= 3 {
                    curr += arrangements[i - 3].assume_init();
                }
            }

            arrangements[i] = MaybeUninit::new(curr);
        }

        ((ones * threes).to_string(), curr.to_string())
    }
}

#[inline(always)]
fn check_ones_threes(diff: u32, ones: &mut u32, threes: &mut u32) {
    match diff {
        1 => *ones += 1,
        3 => *threes += 1,
        _ => (),
    }
}
