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
        5
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<bool> {
        ensure!(!input.is_empty(), "Input is empty");
        ensure!(input.len() / 11 < 4_000_000, "Input too long");
        ensure!(
            input.len() % 11 == 0,
            "Input length is not a multiple of 11"
        );
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        for i in 0..input.len() / 11 {
            ensure!(
                input[i * 11..i * 11 + 7]
                    .chars()
                    .all(|c| c == 'F' || c == 'B'),
                "Invalid boarding pass: {}",
                &input[i * 11..(i + 1) * 11]
            );
            ensure!(
                input[i * 11 + 7..i * 11 + 10]
                    .chars()
                    .all(|c| c == 'R' || c == 'L'),
                "Invalid boarding pass: {}",
                &input[i * 11..(i + 1) * 11]
            );
            ensure!(
                input.as_bytes()[i * 11 + 10] == b'\n',
                "Expected newline at index {}",
                i * 11 + 10
            );
        }
        Ok(true)
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let bytes = crate::SliceWrapper::new(input.as_bytes());
        let mut min: u32 = u32::MAX;
        let mut max: u32 = 0;
        let mut sum: u32 = 0;
        let mut i = 0;

        while i < input.len() {
            let mut id: u32 = 0;
            id |= (bytes[i] as u32 & 0b100) << 9;
            id |= (bytes[i + 1] as u32 & 0b100) << 8;
            id |= (bytes[i + 2] as u32 & 0b100) << 7;
            id |= (bytes[i + 3] as u32 & 0b100) << 6;
            id |= (bytes[i + 4] as u32 & 0b100) << 5;
            id |= (bytes[i + 5] as u32 & 0b100) << 4;
            id |= (bytes[i + 6] as u32 & 0b100) << 3;
            id |= (bytes[i + 7] as u32 & 0b100) << 2;
            id |= (bytes[i + 8] as u32 & 0b100) << 1;
            id |= bytes[i + 9] as u32 & 0b100;

            id = (!id >> 2) & 0b11_1111_1111;

            sum += id;
            min = min.min(id);
            max = max.max(id);

            i += 11;
        }

        // sum(min..=max)
        let total_sum = (max * (max + 1) - min * (min - 1)) / 2;
        let part2 = total_sum - sum;

        (max.to_string(), part2.to_string())
    }
}
