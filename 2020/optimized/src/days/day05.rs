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
        ensure!(input.len() % 33 == 11, "Input lines % 3 != 1");
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
        let mut min: u32 = u32::MAX;
        let mut max: u32 = 0;
        let mut sum: u32 = 0;

        let mut ptr = input.as_bytes().as_ptr();
        let end_ptr = ptr.add(input.len() - 11);

        while ptr < end_ptr {
            let (a, b, c) = parse3(ptr);
            sum += a + b + c;
            min = min.min(a).min(b).min(c);
            max = max.max(a).max(b).max(c);

            ptr = ptr.add(33);
        }

        let last = parse1(ptr);
        sum += last;
        min = min.min(last);
        max = max.max(last);

        // sum(min..=max)
        let total_sum = (max * (max + 1) - min * (min - 1)) / 2;
        let part2 = total_sum - sum;

        (max.to_string(), part2.to_string())
    }
}

#[inline(always)]
unsafe fn parse3(ptr: *const u8) -> (u32, u32, u32) {
    use core::arch::x86_64::__m256i;
    use core::arch::x86_64::_mm256_andnot_si256;
    use core::arch::x86_64::_mm256_loadu_si256;
    use core::arch::x86_64::_mm256_movemask_epi8;
    use core::arch::x86_64::_mm256_permute2x128_si256;
    use core::arch::x86_64::_mm256_setr_epi8;
    use core::arch::x86_64::_mm256_shuffle_epi8;
    use core::arch::x86_64::_mm256_slli_epi64;

    let shuffle_u8 = _mm256_setr_epi8(
        15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, //
        15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, //
    );
    let mask = _mm256_setr_epi8(
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, //
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, //
        4, 4, 4, 4, 4, 4, 4, 4, 4, 4, //
    );

    let mut ticket_bytes = _mm256_loadu_si256(ptr as *const __m256i);
    ticket_bytes = _mm256_shuffle_epi8(ticket_bytes, shuffle_u8);
    ticket_bytes = _mm256_permute2x128_si256(ticket_bytes, ticket_bytes, 1);
    ticket_bytes = _mm256_andnot_si256(ticket_bytes, mask);
    ticket_bytes = _mm256_slli_epi64(ticket_bytes, 5);
    let ticket_id = _mm256_movemask_epi8(ticket_bytes) as u32;

    (
        ticket_id & 0x3ff,
        (ticket_id >> 11) & 0x3ff,
        ticket_id >> 22,
    )
}

#[inline(always)]
unsafe fn parse1(ptr: *const u8) -> u32 {
    use core::arch::x86_64::__m128i;
    use core::arch::x86_64::_mm_andnot_si128;
    use core::arch::x86_64::_mm_loadu_si128;
    use core::arch::x86_64::_mm_movemask_epi8;
    use core::arch::x86_64::_mm_shuffle_epi8;
    use core::arch::x86_64::_mm_slli_epi64;

    const SHUFFLE: __m128i =
        unsafe { std::mem::transmute(0xff_ff_ff_ff_ff_ff_00_01_02_03_04_05_06_07_08_09_u128) };
    const MASK: __m128i = unsafe { std::mem::transmute(0x0404_0404_0404_0404_0404_u128) };

    let mut ticket_bytes = _mm_loadu_si128(ptr as *const __m128i);
    ticket_bytes = _mm_shuffle_epi8(ticket_bytes, SHUFFLE);
    ticket_bytes = _mm_andnot_si128(ticket_bytes, MASK);
    ticket_bytes = _mm_slli_epi64(ticket_bytes, 5);
    _mm_movemask_epi8(ticket_bytes) as u32
}
