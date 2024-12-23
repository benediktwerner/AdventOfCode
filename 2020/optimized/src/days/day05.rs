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
        ensure!(
            input.len() % 44 == 0,
            "Input length is not a multiple of 44"
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

    #[cfg(not(target_arch = "x86_64"))]
    unsafe fn solve(&self, input: &str) -> (String, String) {
        let bytes = crate::SliceWrapper::new(input.as_bytes());
        let mut min: u32 = u32::MAX;
        let mut max: u32 = 0;
        let mut sum: u32 = 0;
        let mut i = 0;

        while i < input.len() {
            let mut id: u32 = 0;

            #[allow(clippy::identity_op)]
            {
                id |= (bytes[i + 0] as u32 & 0b100) << 9;
                id |= (bytes[i + 1] as u32 & 0b100) << 8;
                id |= (bytes[i + 2] as u32 & 0b100) << 7;
                id |= (bytes[i + 3] as u32 & 0b100) << 6;
                id |= (bytes[i + 4] as u32 & 0b100) << 5;
                id |= (bytes[i + 5] as u32 & 0b100) << 4;
                id |= (bytes[i + 6] as u32 & 0b100) << 3;
                id |= (bytes[i + 7] as u32 & 0b100) << 2;
                id |= (bytes[i + 8] as u32 & 0b100) << 1;
                id |= (bytes[i + 9] as u32 & 0b100) << 0;
            }

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

    #[cfg(target_arch = "x86_64")]
    unsafe fn solve(&self, input: &str) -> (String, String) {
        let mut min: u32 = u32::MAX;
        let mut max: u32 = 0;
        let mut sum: u32 = 0;

        let mut ptr = input.as_bytes().as_ptr();
        let end_ptr = ptr.add(input.len());

        while ptr < end_ptr {
            let (a, b) = parse2(ptr);
            sum += a + b;
            min = min.min(a).min(b);
            max = max.max(a).max(b);

            ptr = ptr.add(11);

            let (a, b) = parse2(ptr);
            sum += a + b;
            min = min.min(a).min(b);
            max = max.max(a).max(b);

            ptr = ptr.add(33);
        }

        // sum(min..=max)
        let total_sum = (max * (max + 1) - min * (min - 1)) / 2;
        let part2 = total_sum - sum;

        (max.to_string(), part2.to_string())
    }
}

#[cfg(target_arch = "x86_64")]
#[inline(always)]
unsafe fn parse2(ptr: *const u8) -> (u32, u32) {
    use core::arch::x86_64::__m256i;
    use core::arch::x86_64::_mm256_andnot_si256;
    use core::arch::x86_64::_mm256_loadu_si256;
    use core::arch::x86_64::_mm256_movemask_epi8;
    use core::arch::x86_64::_mm256_set_epi8;
    use core::arch::x86_64::_mm256_shuffle_epi8;
    use core::arch::x86_64::_mm256_slli_epi64;

    let shuffle = _mm256_set_epi8(
        -1, -1, -1, -1, -1, -1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, //
        -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, //
    );
    let mask = _mm256_set_epi8(
        0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, //
        0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, //
    );

    let mut ticket_bytes = _mm256_loadu_si256(ptr.cast::<__m256i>());
    ticket_bytes = _mm256_shuffle_epi8(ticket_bytes, shuffle);
    ticket_bytes = _mm256_andnot_si256(ticket_bytes, mask);
    ticket_bytes = _mm256_slli_epi64(ticket_bytes, 5);
    let ticket_id = _mm256_movemask_epi8(ticket_bytes) as u32;

    (ticket_id & 0xffff, ticket_id >> 16)
}
