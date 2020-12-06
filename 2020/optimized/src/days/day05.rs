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

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
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
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        use core::arch::x86_64::__m128i;
        use core::arch::x86_64::_mm_loadu_si128;
        use core::arch::x86_64::_mm_shuffle_epi8;
        use core::arch::x86_64::_mm_andnot_si128;
        use core::arch::x86_64::_mm_slli_epi64;
        use core::arch::x86_64::_mm_movemask_epi8;

        let mut min: u32 = u32::MAX;
        let mut max: u32 = 0;
        let mut sum: u32 = 0;

        const SHUFFLE: __m128i = unsafe { std::mem::transmute(0xff_ff_ff_ff_ff_ff_00_01_02_03_04_05_06_07_08_09_u128) };
        const MASK: __m128i = unsafe { std::mem::transmute(0x0404_0404_0404_0404_0404_u128) };

        let mut ptr = input.as_bytes().as_ptr();
        let end_ptr = ptr.add(input.len());

        while ptr < end_ptr {
            let mut ticket_bytes = _mm_loadu_si128(ptr as *const __m128i);
            ticket_bytes = _mm_shuffle_epi8(ticket_bytes, SHUFFLE);
            ticket_bytes = _mm_andnot_si128(ticket_bytes, MASK);
            ticket_bytes = _mm_slli_epi64(ticket_bytes, 5);
            let ticket_id = _mm_movemask_epi8(ticket_bytes) as u32;

            sum += ticket_id;
            min = min.min(ticket_id);
            max = max.max(ticket_id);

            ptr = ptr.add(11);
        }

        // sum(min..=max)
        let total_sum = (max * (max + 1) - min * (min - 1)) / 2;
        let part2 = total_sum - sum;

        (max.to_string(), part2.to_string())
    }
}
