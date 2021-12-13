use anyhow::{bail, ensure};

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
        4
    }

    fn is_input_safe(&self, input: &str) -> anyhow::Result<()> {
        ensure!(
            input.len() < u32::MAX as usize,
            "Input longer than u32::MAX: {}",
            input.len()
        );
        ensure!(input.is_ascii(), "Input contains non-ASCII characters");
        ensure!(
            input.len() >= 6,
            "Input is too short. (< 7 characters including newline)"
        );
        ensure!(
            &input[input.len() - 1..] == "\n",
            "Input is missing newline at the end"
        );
        for passport in input.split("\n\n") {
            ensure!(!passport.is_empty(), "Empty passport");
            for part in passport.split(|c| c == '\n' || c == ' ') {
                let mut iter = part.split(':');
                let (key, value) = (iter.next(), iter.next());
                ensure!(iter.next().is_none(), "Too many values");
                match (key, value) {
                    (Some(key), Some(value)) => match key {
                        "byr" | "iyr" | "eyr" => {
                            ensure!(
                                value.len() == 4,
                                "Year value doesn't have 4 characters: {}",
                                value
                            );
                            ensure!(
                                value.chars().all(|c| '0' <= c && c <= '9'),
                                "Year value has invalid digit: {}",
                                value
                            );
                        }
                        "hgt" | "hcl" | "ecl" | "pid" | "cid" => (),
                        _ => bail!("Invalid key: {}", key),
                    },
                    _ => ensure!(part.is_empty(), "Invalid field: '{}'", part),
                }
            }
        }
        Ok(())
    }

    unsafe fn solve(&self, input: &str) -> (String, String) {
        let mut output = (0, 0);

        let bytes = crate::SliceWrapper::new(input.as_bytes());
        let mut i: u32 = 0;

        loop {
            let mut fields = 0;

            loop {
                i += 4;
                let field_valid = match bytes[i - 4] {
                    b'b' => {
                        fields += 1;
                        is_valid_byr(bytes, &mut i)
                    }
                    b'i' => {
                        fields += 1;
                        is_valid_iyr(bytes, &mut i)
                    }
                    b'e' => {
                        fields += 1;
                        if bytes[i - 3] == b'y' {
                            is_valid_eyr(bytes, &mut i)
                        } else {
                            is_valid_ecl(bytes, &mut i)
                        }
                    }
                    b'h' => {
                        fields += 1;
                        if bytes[i - 3] == b'g' {
                            is_valid_hgt(bytes, &mut i)
                        } else {
                            is_valid_hcl(bytes, &mut i)
                        }
                    }
                    b'p' => {
                        fields += 1;
                        is_valid_pid(bytes, &mut i)
                    }
                    _ => {
                        goto_space(bytes, &mut i);
                        true
                    }
                };

                // we must be at space or newline
                debug_assert!(
                    bytes[i] == b'\n' || bytes[i] == b' ',
                    "Expected newline or space, found: {:?}",
                    &input[i as usize..(i + 10) as usize]
                );

                i += 1;

                let is_end = i >= bytes.len() as u32;
                if is_end || bytes[i] == b'\n' {
                    if fields == 7 {
                        output.0 += 1;
                        if field_valid {
                            output.1 += 1;
                        }
                    }
                    if is_end {
                        return (output.0.to_string(), output.1.to_string());
                    } else {
                        i += 1;
                        break;
                    }
                }

                if !field_valid {
                    loop {
                        if bytes[i] != b'c' {
                            fields += 1;
                        }
                        i += 5;
                        goto_space(bytes, &mut i);
                        i += 1;
                        let is_end = i >= bytes.len() as u32;
                        if is_end || bytes[i] == b'\n' {
                            if fields == 7 {
                                output.0 += 1;
                            }
                            if is_end {
                                return (output.0.to_string(), output.1.to_string());
                            } else {
                                i += 1;
                                break;
                            }
                        }
                    }
                    break;
                }
            }
        }
    }
}

#[inline(always)]
fn is_valid_byr(bytes: crate::SliceWrapper<u8>, i: &mut u32) -> bool {
    // byr (Birth Year) - four digits; at least 1920 and at most 2002.
    let mut valid = true;
    match bytes[*i] {
        b'1' => {
            if bytes[*i + 1] != b'9' || bytes[*i + 2] < b'2' {
                valid = false;
            }
        }
        b'2' => {
            if bytes[*i + 1] != b'0' || bytes[*i + 2] != b'0' || bytes[*i + 3] > b'2' {
                valid = false;
            }
        }
        _ => valid = false,
    }

    *i += 4;
    valid
}

#[inline(always)]
fn is_valid_iyr(bytes: crate::SliceWrapper<u8>, i: &mut u32) -> bool {
    // iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    let mut valid = true;
    if bytes[*i] != b'2'
        || bytes[*i + 1] != b'0'
        || (bytes[*i + 2] != b'1' && (bytes[*i + 2] != b'2' || bytes[*i + 3] != b'0'))
    {
        valid = false;
    }

    *i += 4;
    valid
}

#[inline(always)]
fn is_valid_eyr(bytes: crate::SliceWrapper<u8>, i: &mut u32) -> bool {
    // eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    let mut valid = true;
    if bytes[*i] != b'2'
        || bytes[*i + 1] != b'0'
        || (bytes[*i + 2] != b'2' && (bytes[*i + 2] != b'3' || bytes[*i + 3] != b'0'))
    {
        valid = false;
    }

    *i += 4;
    valid
}

#[inline(always)]
fn is_valid_hgt(bytes: crate::SliceWrapper<u8>, i: &mut u32) -> bool {
    // hgt (Height) - a number followed by either cm or in:
    //   - If cm, the number must be at least 150 and at most 193.
    //   - If in, the number must be at least 59 and at most 76.
    if bytes[*i] == b'1' {
        if bytes[*i + 1] < b'5' || bytes[*i + 1] > b'9' || bytes[*i + 2] < b'0' {
            *i += 1;
        } else if bytes[*i + 1] == b'9' && bytes[*i + 2] > b'3' {
            *i += 2;
        } else if &bytes[(*i as usize) + 3..(*i as usize) + 5] != b"cm" {
            *i += 3;
        } else {
            *i += 5;
            return true;
        }
    } else if b'5' <= bytes[*i] && bytes[*i] <= b'7' {
        if (bytes[*i] == b'5' && bytes[*i + 1] != b'9')
            || (bytes[*i] == b'7' && bytes[*i + 1] > b'6')
            || bytes[*i + 1] < b'0'
            || bytes[*i + 1] > b'9'
        {
            *i += 1;
        } else if &bytes[(*i as usize) + 2..(*i as usize) + 4] != b"in" {
            *i += 2;
        } else {
            *i += 4;
            return true;
        }
    }

    goto_space(bytes, i);
    false
}

#[inline(always)]
fn is_valid_hcl(bytes: crate::SliceWrapper<u8>, i: &mut u32) -> bool {
    // hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    if bytes[*i] != b'#' {
    } else if !is_hex_char(bytes[*i + 1]) {
        *i += 1;
    } else if !is_hex_char(bytes[*i + 2]) {
        *i += 2;
    } else if !is_hex_char(bytes[*i + 3]) {
        *i += 3;
    } else if !is_hex_char(bytes[*i + 4]) {
        *i += 4;
    } else if !is_hex_char(bytes[*i + 5]) {
        *i += 5;
    } else if !is_hex_char(bytes[*i + 6]) {
        *i += 6;
    } else {
        *i += 7;
        if is_space(bytes[*i]) {
            return true;
        }
    }
    goto_space(bytes, i);
    false
}

#[inline(always)]
fn is_valid_ecl(bytes: crate::SliceWrapper<u8>, i: &mut u32) -> bool {
    // ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    if *i + 3 > bytes.len() as u32 {
        *i += 2;
        return false;
    }
    match &bytes[(*i as usize)..(*i as usize + 3)] {
        b"amb" | b"blu" | b"brn" | b"gry" | b"grn" | b"hzl" | b"oth" => {
            *i += 3;
            if is_space(bytes[*i]) {
                return true;
            }
        }
        _ => (),
    }
    goto_space(bytes, i);
    false
}

#[inline(always)]
fn is_valid_pid(bytes: crate::SliceWrapper<u8>, i: &mut u32) -> bool {
    // pid (Passport ID) - a nine-digit number, including leading zeroes.
    if *i + 9 > bytes.len() as u32 {
        *i += 9;
        return false;
    }
    for _ in 0..9 {
        if bytes[*i] < b'0' || bytes[*i] > b'9' {
            goto_space(bytes, i);
            return false;
        }
        *i += 1;
    }
    if is_space(bytes[*i]) {
        true
    } else {
        *i += 1;
        goto_space(bytes, i);
        false
    }
}

#[inline(always)]
fn goto_space(bytes: crate::SliceWrapper<u8>, i: &mut u32) {
    while !is_space(bytes[*i]) {
        *i += 1;
    }
}

#[inline(always)]
const fn is_space(c: u8) -> bool {
    c == b' ' || c == b'\n'
}

#[inline(always)]
const fn is_hex_char(c: u8) -> bool {
    (b'0' <= c && c <= b'9') || (b'a' <= c && c <= b'f')
}
