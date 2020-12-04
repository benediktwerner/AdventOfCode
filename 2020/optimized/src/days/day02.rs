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
        2
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<bool> {
        for line in input.lines() {
            let parts: Vec<_> = line.split(' ').collect();
            ensure!(parts.len() == 3, "Wrong number of parts: {}", line);
            let lowhigh: Vec<_> = parts[0].split('-').collect();
            ensure!(
                lowhigh.len() == 2,
                "Wrong number of parts for lowhigh: {}",
                line
            );
            let low = lowhigh[0]
                .parse::<u32>()
                .with_context(|| format!("Failed to convert low to int: {}", line))?;
            let high = lowhigh[1]
                .parse::<u32>()
                .with_context(|| format!("Failed to convert high to int: {}", line))?;

            ensure!(low > 0, "Low is 0: {}", line);
            ensure!(low < high, "Low not less than high: {}", line);
            ensure!(
                (high as usize) <= parts[2].len(),
                "High points outside the password: {}",
                line
            );
            ensure!(
                parts[1].len() == 2,
                "Character part has invalid length: {}",
                line
            );
            ensure!(
                &parts[1][1..2] == ":",
                "Character part is missing colon: {}",
                line
            );
        }
        Ok(true)
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let mut output = (0, 0);

        let bytes = crate::SliceWrapper::new(input.as_bytes());
        let mut i = 0;

        while i < bytes.len() {
            let mut low = 0;
            while bytes[i] != b'-' {
                low = low * 10 + bytes[i] - b'0';
                i += 1;
            }

            i += 1;
            let mut high = 0;
            while bytes[i] != b' ' {
                high = high * 10 + bytes[i] - b'0';
                i += 1;
            }

            i += 1;
            let char = bytes[i];
            let mut count = 0;
            i += 2;

            let char_at_low = bytes[i + low as usize] == char;
            let char_at_high = bytes[i + high as usize] == char;
            if char_at_low ^ char_at_high {
                output.1 += 1;
            }

            i += 1;

            while bytes[i] != b'\n' {
                if bytes[i] == char {
                    count += 1;
                }
                i += 1;
            }

            if low <= count && count <= high {
                output.0 += 1;
            }

            i += 1;
        }

        (output.0.to_string(), output.1.to_string())
    }
}
