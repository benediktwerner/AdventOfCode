use anyhow::ensure;
use rustc_hash::FxHashSet;

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
        9
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
        ensure!(len > 25, "Less than 26 lines");
        ensure!(len <= 1023, "More than 1023 lines");
        for line in input.lines() {
            ensure!(
                line.parse::<u64>().is_ok(),
                "Not a valid number: '{}'",
                line
            );
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let bytes = SliceWrapper::new(input.as_bytes());
        let mut numbers = [0; 1024];
        let mut numbers = SliceWrapperMut::new(&mut numbers);
        let mut last25 = FxHashSet::with_capacity_and_hasher(25, Default::default());
        let mut num = 0;
        let mut len = 0;
        let mut i = 0;

        for _ in 0..25 {
            num = parse_number(bytes, &mut i);
            last25.insert(num);
            numbers[len] = num;
            len += 1;
            i += 1;
        }

        while i < bytes.len() {
            num = parse_number(bytes, &mut i);

            if check_last_25(numbers.0, &last25, len, num) {
                break;
            }

            last25.remove(&numbers[len - 25]);
            last25.insert(num);
            numbers[len] = num;
            len += 1;
            i += 1;
        }

        let mut start = 0;
        let mut end = 1;
        let mut sum = numbers[0] + numbers[1];

        loop {
            use std::cmp::Ordering;
            match sum.cmp(&num) {
                Ordering::Equal => break,
                Ordering::Less => {
                    end += 1;
                    sum += numbers[end];
                }
                Ordering::Greater => {
                    sum -= numbers[start];
                    start += 1;
                }
            }
        }

        let mut min = u64::MAX;
        let mut max = 0;

        for i in start..=end {
            let n = numbers[i];
            min = min.min(n);
            max = max.max(n);
        }

        (num.to_string(), (min + max).to_string())
    }
}

#[inline(always)]
fn parse_number(bytes: SliceWrapper<u8>, i: &mut usize) -> u64 {
    let mut num = 0;
    while bytes[*i] != b'\n' {
        num = num * 10 + (bytes[*i] - b'0') as u64;
        *i += 1;
    }
    num
}

#[inline(always)]
unsafe fn check_last_25(numbers: &[u64], last25: &FxHashSet<u64>, i: usize, num: u64) -> bool {
    let numbers = SliceWrapper::new(numbers);
    for j in i - 25..i {
        let needed = num.wrapping_sub(numbers[j]);
        if last25.contains(&needed) {
            return false;
        }
    }
    true
}
