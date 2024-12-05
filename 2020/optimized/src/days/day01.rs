use std::mem::MaybeUninit;

use anyhow::{ensure, Context};

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
        1
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        for line in input.lines() {
            let number = line
                .parse::<u32>()
                .with_context(|| format!("Failed to convert {line} to int"))?;
            ensure!(number < 2020, "Number is bigger than 2020: {}", line);
        }
        ensure!(input.lines().count() <= 200, "Input longer than 200 lines");
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let mut output = (0, 0);

        let mut nums = [false; 2020];

        let mut num = 0;
        let mut count = 0;
        for &c in input.as_bytes() {
            if c == b'\n' {
                *nums.get_unchecked_mut(num) = true;
                num = 0;
                count += 1;
            } else {
                num = num * 10 + (c - b'0') as usize;
            }
        }

        let mut nums_list = Vec::with_capacity(count);
        {
            let nums_list = nums_list.spare_capacity_mut();
            let mut i = 0;
            for (n, b) in nums.iter().enumerate() {
                if *b {
                    *nums_list.get_unchecked_mut(i) = MaybeUninit::new(n as u32);
                    i += 1;
                }
            }
            debug_assert!(i == count);
        }
        nums_list.set_len(count);

        'outer: for (i, &a) in nums_list.iter().enumerate() {
            let opp = 2020 - a;
            if *nums.get_unchecked(opp as usize) {
                output.0 = a * opp;
                if output.1 != 0 {
                    break 'outer;
                }
            }

            for &b in nums_list.get_unchecked(i + 1..) {
                if 2 * b > opp {
                    break;
                }
                let opp2 = opp - b;
                if *nums.get_unchecked(opp2 as usize) {
                    output.1 = a * b * opp2;
                    if output.0 != 0 {
                        break 'outer;
                    }
                }
            }
        }

        (output.0.to_string(), output.1.to_string())
    }
}

// #[allow(dead_code)]
// pub unsafe fn solve_asm(input: &str) -> (u32, u32) {
//     let input = input.as_bytes();
//     let COutput(a, b) = asm_solve_day01(input.as_ptr(), input.len());
//     (a, b)
// }

// #[repr(C)]
// struct COutput(u32, u32);

// #[no_mangle]
// pub unsafe extern "C" fn rust_memset(dest: *mut libc::c_void, c: i32, n: usize) {
//     libc::memset(dest, c, n);
// }

// extern "C" {
//     fn asm_solve_day01(input: *const u8, length: usize) -> COutput;
// }
