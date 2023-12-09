use rayon::iter::{IntoParallelIterator, ParallelIterator as _};

const INITIAL_BATCH: usize = 1_024;
const NEW_BATCH: usize = 1_024;

fn main() {
    let input = include_str!("../../input.txt").trim();
    println!("Part 1: {}", find(input, 0));
    println!("Part 2: {}", find(input, 2016));
}

fn find(salt: &str, stretch: usize) -> usize {
    let mut index = 0;
    let mut hashes = par_hashes(salt, 0, INITIAL_BATCH, stretch);

    for _ in 0..64 {
        loop {
            if index + 1000 >= hashes.len() {
                hashes.append(&mut par_hashes(salt, hashes.len(), NEW_BATCH, stretch));
            }
            let h = &hashes[index];
            index += 1;
            if let Some(trip) = triple(h) {
                if hashes[index..index + 1000].iter().any(|h| quint(h, trip)) {
                    break;
                }
            }
        }
    }

    index - 1
}

fn triple(s: &str) -> Option<u8> {
    let s = s.as_bytes();
    for i in 0..s.len() - 2 {
        match s[i..i + 3] {
            [a, b, c] => {
                if a == b && b == c {
                    return Some(a);
                }
            }
            _ => unreachable!(),
        }
    }
    None
}

fn quint(s: &str, k: u8) -> bool {
    let s = s.as_bytes();
    for i in 0..s.len() - 4 {
        match s[i..i + 5] {
            [a, b, c, d, e] => {
                if k == a && a == b && b == c && c == d && d == e {
                    return true;
                }
            }
            _ => unreachable!(),
        }
    }
    false
}

fn hash(salt: &str, index: usize, stretch: usize) -> String {
    let mut h = format!("{:x}", md5::compute(format!("{salt}{index}")));
    for _ in 0..stretch {
        h = format!("{:x}", md5::compute(&h));
    }
    h
}

fn par_hashes(salt: &str, start_index: usize, count: usize, stretch: usize) -> Vec<String> {
    (start_index..start_index + count)
        .into_par_iter()
        .map(|i| hash(salt, i, stretch))
        .collect()
}
