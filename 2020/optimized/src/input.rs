use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::{Path, PathBuf};

fn day_input_path(day: u8) -> PathBuf {
    Path::new("..").join(format!("day{:02}", day)).join("input.txt")
}

pub fn read_input(day: u8) -> Vec<String> {
    let path = day_input_path(day);
    let file = File::open(&path).unwrap_or_else(|_| panic!("Error while opening input file: {:?}", path));
    let reader = BufReader::new(file);
    let input : Result<Vec<String>, io::Error> = reader.lines().collect();
    input.unwrap_or_else(|_| panic!("Error while reading input file: {:?}", path))
}
