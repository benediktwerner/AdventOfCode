use anyhow::ensure;

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
        6
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(
            input.len() >= 2,
            "Input is too short. (< 2 characters including newline)"
        );
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let mut output = (0, 0);

        let bytes = crate::SliceWrapper::new(input.as_bytes());
        let mut i = 0;

        loop {
            let mut any = 0;
            let mut all = 0xffff_ffff;

            loop {
                let mut answers = 0;

                loop {
                    answers |= 1_u32.wrapping_shl(bytes[i] as u32);
                    i += 1;
                    if bytes[i] == b'\n' {
                        break;
                    }
                }

                any |= answers;
                all &= answers;

                i += 1;

                let is_end = i >= bytes.len();
                if is_end || bytes[i] == b'\n' {
                    output.0 += any.count_ones();
                    output.1 += all.count_ones();

                    if is_end {
                        return (output.0.to_string(), output.1.to_string());
                    }
                    i += 1;
                    break;
                }
            }
        }
    }
}
