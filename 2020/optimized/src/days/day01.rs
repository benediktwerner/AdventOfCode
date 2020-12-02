use anyhow::Context;

pub struct Solver;

impl crate::Solver for Solver {
    type Input = Vec<u32>;
    type Output = (u32, u32);

    fn parse_input(&self, input: &[String]) -> anyhow::Result<Self::Input> {
        input
            .iter()
            .map(|s| {
                s.parse::<u32>()
                    .with_context(|| format!("Failed to convert {} to int", s))
            })
            .collect()
    }

    fn is_input_safe(&self, input: &Self::Input) -> bool {
        input.iter().all(|n| *n < 2020)
    }

    unsafe fn solve(&self, mut input: Self::Input) -> Self::Output {
        let mut output = (0, 0);

        let mut nums = [false; 2020];

        for n in input.iter() {
            *nums.get_unchecked_mut(*n as usize) = true;
        }

        // input.sort_unstable();

        // Sort input
        let mut i = 0;
        for (n, b) in nums.iter().enumerate() {
            if *b {
                *input.get_unchecked_mut(i) = n as u32;
                i += 1;
            }
        }

        for (i, &a) in input.iter().enumerate() {
            let opp = 2020 - a;
            if *nums.get_unchecked(opp as usize) {
                output.0 = a * opp;
                if output.1 != 0 {
                    return output;
                }
            }

            for &b in input.get_unchecked(i + 1..) {
                if b > opp {
                    break;
                }
                let opp2 = opp - b;
                if *nums.get_unchecked(opp2 as usize) {
                    output.1 = a * b * opp2;
                    if output.0 != 0 {
                        return output;
                    }
                }
            }
        }

        output
    }
}
