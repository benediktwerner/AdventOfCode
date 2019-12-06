use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let matches = clap::App::new("intcode-vm")
        .version(clap::crate_version!())
        .author(clap::crate_authors!())
        .about("Vm for intcode programs from Advent of Code 2019")
        .arg(
            clap::Arg::with_name("file")
                .help("The file to execute")
                .required(true),
        )
        .arg(
            clap::Arg::with_name("trace")
                .long("trace")
                .help("Trace all instructions"),
        )
        .get_matches();

    let file = matches.value_of("file").unwrap();
    let reader = BufReader::new(File::open(file).unwrap());
    let line = reader.lines().next().unwrap().unwrap();
    let code = line.split(',').map(|c| c.parse().unwrap()).collect();
    intcode_vm::VM::new(code, matches.is_present("trace")).run();
}
