use anyhow::{bail, ensure, Context};

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
        2
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
        for line in input.lines() {
            let parts: Vec<_> = line.split(' ').collect();
            match &parts[..] {
                [instr, n] => {
                    ensure!(
                        matches!(*instr, "forward" | "down" | "up"),
                        "Invalid instruction: '{}'",
                        parts[0]
                    );
                    n.parse::<u32>()
                        .with_context(|| format!("Failed to convert '{}' to int", line))?;
                }
                _ => bail!("Invalid line: '{}'", line),
            }
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let bytes = crate::SliceWrapper::new(input.as_bytes());
        let mut i = 0;
        let mut x1 = 0;
        let mut depth1 = 0;
        let mut x2 = 0;
        let mut depth2 = 0;
        let mut aim = 0;

        while i < bytes.len() {
            let instr = match bytes[i] {
                b'f' => Instr::Forward,
                b'd' => Instr::Down,
                b'u' => Instr::Up,
                _ => {
                    debug_assert!(false, "unreachable");
                    std::hint::unreachable_unchecked();
                }
            };
            i += instr.size() + 1;
            let mut num = (bytes[i] - b'0') as i32;
            loop {
                i += 1;
                if bytes[i] == b'\n' {
                    i += 1;
                    break;
                }
                num = num * 10 + (bytes[i] - b'0') as i32;
            }
            match instr {
                Instr::Forward => {
                    x1 += num;
                    x2 += num;
                    depth2 += num * aim;
                }
                Instr::Down => {
                    depth1 += num;
                    aim += num;
                }
                Instr::Up => {
                    depth1 -= num;
                    aim -= num;
                }
            }
        }

        let part1 = x1 * depth1;
        let part2 = x2 * depth2;
        (part1.to_string(), part2.to_string())
    }
}

#[derive(Clone, Copy)]
enum Instr {
    Forward,
    Up,
    Down,
}

impl Instr {
    const fn size(self) -> usize {
        match self {
            Instr::Forward => "forward".len(),
            Instr::Up => "up".len(),
            Instr::Down => "down".len(),
        }
    }
}
