use anyhow::{bail, ensure};

use crate::{SliceWrapper, SliceWrapperMut};

type Arg = i16;

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
        8
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
        ensure!(len <= 1023, "More than 1023 lines");
        for (i, line) in input.lines().enumerate() {
            let op = &line[..3];
            match op {
                "acc" | "jmp" | "nop" => (),
                _ => bail!("Invalid opcode: '{}' in '{}'", op, line),
            }
            ensure!(
                &line[3..4] == " ",
                "Expected space after opcode: '{}'",
                line
            );
            ensure!(
                &line[4..5] == "+" || &line[4..5] == "-",
                "Expected + or - to start argument: '{}'",
                line
            );
            match line[5..].parse::<u32>() {
                Ok(arg) => {
                    ensure!(arg <= 999, "Argument too large: '{}'", arg);
                    let mut arg = arg as i32;
                    if &line[4..5] == "-" {
                        arg *= -1;
                    }
                    let target = i as i32 + arg;
                    if (&line[..3] == "jmp" || &line[..3] == "nop")
                        && (target < 0 || target > len as i32)
                    {
                        bail!(
                            "Possible jump to before or not-immediately after code: '{}'",
                            line
                        );
                    }
                }
                Err(_) => bail!("Expected number as argument: '{}'", line),
            }
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let bytes = SliceWrapper::new(input.as_bytes());
        let mut i = 0;

        // visit_count, opcode 1st byte, arg
        let mut code: [std::mem::MaybeUninit<(u8, u8, i16)>; 1024] =
            std::mem::MaybeUninit::uninit().assume_init();
        let mut code = SliceWrapperMut::new(&mut code);
        let mut len = 0;
        // let mut code = Vec::with_capacity(input.len() / 10);

        loop {
            let op = bytes[i];
            let neg = bytes[i + 4] == b'-';
            let mut arg = (bytes[i + 5] - b'0') as Arg;

            if bytes[i + 6] == b'\n' {
                i += 7;
            } else {
                arg = arg * 10 + (bytes[i + 6] - b'0') as Arg;
                if bytes[i + 7] == b'\n' {
                    i += 8;
                } else {
                    arg = arg * 10 + (bytes[i + 7] - b'0') as Arg;
                    i += 9;
                }
            }
            // i += 6;
            // while bytes[i] != b'\n' {
            //     arg = arg*10 + (bytes[i] - b'0') as Arg;
            //     i += 1;
            // }
            // i += 1;

            if neg {
                arg = -arg;
            }

            // code.push((0, op, arg));
            code[len] = std::mem::MaybeUninit::new((0, op, arg));
            len += 1;

            if i >= input.len() {
                break;
            }
        }

        // Failsave to avoid UB when part1 terminates
        // code.push((1, 0, 0));
        code[len] = std::mem::MaybeUninit::new((1, 0, 0));

        let mut code = code.assume_init_mut(len);
        // let mut code = SliceWrapperMut::new(&mut code);

        let mut acc = 0;
        let mut ip = 0;
        let part1;

        loop {
            let (seen, op, arg) = code[ip];

            if seen > 0 {
                part1 = acc;
                break;
            }

            code[ip].0 = 1;

            if op == b'j' {
                ip = (ip as isize + arg as isize) as usize;
            } else {
                if op == b'a' {
                    acc += arg;
                }
                ip += 1;
            }
        }

        acc = 0;
        ip = 0;

        loop {
            let (_, op, arg) = code[ip];

            code[ip].0 = 2;

            if op == b'j' {
                ip = (ip as isize + arg as isize) as usize;
                let (terminated, result) = try_flip(ip + 1, acc, len, code.0);
                if terminated {
                    return (part1.to_string(), result.to_string());
                }
            } else {
                if op == b'a' {
                    acc += arg;
                } else {
                    let flip_ip = (ip as isize + arg as isize) as usize;
                    let (terminated, result) = try_flip(flip_ip, acc, len, code.0);
                    if terminated {
                        return (part1.to_string(), result.to_string());
                    }
                }
                ip += 1;
            }
        }
    }
}

#[inline(always)]
unsafe fn try_flip(
    mut ip: usize,
    mut acc: Arg,
    len: usize,
    code: &mut [(u8, u8, Arg)],
) -> (bool, Arg) {
    let mut code = SliceWrapperMut::new(code);

    loop {
        if ip == len {
            return (true, acc);
        }
        // if ip > len {
        //     return (false, 0);
        // }

        let (seen, op, arg) = code[ip];

        if seen == 2 {
            return (false, 0);
        }

        code[ip].0 = 2;

        if op == b'j' {
            ip = (ip as isize + arg as isize) as usize;
        } else {
            if op == b'a' {
                acc += arg;
            }
            ip += 1;
        }
    }
}
