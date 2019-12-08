#[macro_use]
extern crate lalrpop_util;

mod ast;
mod codegen;
mod parser;

use codegen::CompilerError;

fn main() {
    let matches = clap::App::new("intcode-compiler")
        .version(clap::crate_version!())
        .author(clap::crate_authors!())
        .about("Compiler for intcode from Advent of Code 2019")
        .arg(
            clap::Arg::with_name("file")
                .help("The file to cmpile")
                .required(true),
        )
        .arg(
            clap::Arg::with_name("run")
                .short("r")
                .long("run")
                .help("Run the program after assembling"),
        )
        .arg(
            clap::Arg::with_name("asm")
                .long("asm")
                .help("Print assembly"),
        )
        .arg(
            clap::Arg::with_name("stack_size")
                .short("ss")
                .long("stack-size")
                .takes_value(true)
                .help("Size for the simulated stack. (Default: 0)"),
        )
        .arg(
            clap::Arg::with_name("trace")
                .long("trace")
                .help("Trace all instructions during execution")
                .requires("run"),
        )
        .get_matches();

    let file = matches.value_of("file").unwrap();
    let content = std::fs::read_to_string(file).expect("cannot read file");
    let content = parser::strip_comments(content);
    let (program, env) = match parser::parse(&content) {
        Ok(result) => result,
        Err(error) => {
            println!("Error during file parsing:");
            println!("{}", error);
            return;
        }
    };

    let asm = match codegen::gen(program, &env) {
        Ok(result) => result,
        Err(error) => {
            println!("Error during compilation:");
            match error {
                CompilerError::DuplicateDeclaration(ident) => {
                    println!("Duplicate declaration of variable: {}", env.to_str(ident))
                }
                CompilerError::UndefinedVar(ident) => {
                    println!("Undefined variable: {}", env.to_str(ident))
                }
            }
            return;
        }
    };

    if matches.is_present("asm") {
        for stmt in &asm {
            println!("{}", stmt);
        }
    }

    let code = match matches.value_of("stack_size") {
        Some(stack_size) => intcode_asm::assemble_with_stack(&asm, stack_size.parse().unwrap()),
        None => intcode_asm::assemble(&asm),
    };

    if matches.is_present("run") {
        intcode_vm::VM::new(code, matches.is_present("trace")).run();
    } else {
        let output = code
            .iter()
            .map(|x| x.to_string())
            .collect::<Vec<_>>()
            .join(",");
        println!("{}", output);
    }
}
