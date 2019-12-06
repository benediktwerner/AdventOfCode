#[macro_use]
extern crate pest_derive;

use std::fs;

use intcode_asm::{Param, Stmt};
use pest::{iterators::Pair, Parser};

#[derive(Parser)]
#[grammar = "grammar.pest"]
pub struct AsmParser;

fn parse_radix(pair: Pair<Rule>, radix: u32) -> i64 {
    let mut pairs = pair.into_inner();
    if pairs.next().unwrap().as_str() == "-" {
        pairs.next().unwrap();
        -i64::from_str_radix(pairs.next().unwrap().as_str(), radix).unwrap()
    } else {
        i64::from_str_radix(pairs.next().unwrap().as_str(), radix).unwrap()
    }
}

fn parse_num(pair: Pair<Rule>) -> i64 {
    match pair.as_rule() {
        Rule::num => parse_num(pair.into_inner().next().unwrap()),
        Rule::decimal => pair.as_str().parse().unwrap(),
        Rule::hex => parse_radix(pair, 16),
        Rule::oct => parse_radix(pair, 16),
        Rule::bin => parse_radix(pair, 16),
        _ => unreachable!(),
    }
}

fn parse_param(pair: Pair<Rule>) -> Param {
    match pair.as_rule() {
        Rule::param => parse_param(pair.into_inner().next().unwrap()),
        Rule::ident => Param::IdentPositional(pair.as_str()),
        Rule::ident_immediate => Param::IdentImmediate(pair.into_inner().next().unwrap().as_str()),
        Rule::num => Param::Value(parse_num(pair)),
        _ => unreachable!(),
    }
}

fn parse_stmt(pair: Pair<Rule>) -> Stmt {
    match pair.as_rule() {
        Rule::stmt => parse_stmt(pair.into_inner().next().unwrap()),
        Rule::halt => Stmt::Halt,
        Rule::ret => Stmt::Ret,
        Rule::unary_stmt => {
            let mut pairs = pair.into_inner();
            let cons = match pairs.next().unwrap().as_str() {
                "in" => Stmt::In,
                "out" => Stmt::Out,
                "jmp" => Stmt::Jmp,
                "push" => Stmt::Push,
                "pop" => Stmt::Pop,
                "call" => Stmt::Call,
                other => unreachable!("unknown unary instruction: {}", other),
            };
            let a = parse_param(pairs.next().unwrap());
            cons(a)
        }
        Rule::binary_stmt => {
            let mut pairs = pair.into_inner();
            let cons = match pairs.next().unwrap().as_str() {
                "jnz" | "jtrue" => Stmt::JumpTrue,
                "jz" | "jfalse" => Stmt::JumpFalse,
                "not" => Stmt::Not,
                "mov" => Stmt::Mov,
                "load" => Stmt::Load,
                "store" => Stmt::Store,
                other => unreachable!("unknown binary instruction: {}", other),
            };
            let a = parse_param(pairs.next().unwrap());
            let b = parse_param(pairs.next().unwrap());
            cons(a, b)
        }
        Rule::ternary_stmt => {
            let mut pairs = pair.into_inner();
            let cons = match pairs.next().unwrap().as_str() {
                "add" => Stmt::Add,
                "mul" => Stmt::Mul,
                "sub" => Stmt::Sub,
                "div" => Stmt::Div,
                "mod" => Stmt::Mod,
                "eq" => Stmt::Equal,
                "lt" => Stmt::LessThan,
                "leq" => Stmt::LessEqual,
                "gt" => Stmt::GreaterThan,
                "geq" => Stmt::GreaterEqual,
                "and" => Stmt::And,
                "or" => Stmt::Or,
                other => unreachable!("unknown ternary instruction: {}", other),
            };
            let a = parse_param(pairs.next().unwrap());
            let b = parse_param(pairs.next().unwrap());
            let c = parse_param(pairs.next().unwrap());
            cons(a, b, c)
        }
        Rule::quaternary_stmt => {
            let mut pairs = pair.into_inner();
            let cons = match pairs.next().unwrap().as_str() {
                "divmod" => Stmt::DivMod,
                other => unreachable!("unknown quaternary instruction: {}", other),
            };
            let a = parse_param(pairs.next().unwrap());
            let b = parse_param(pairs.next().unwrap());
            let c = parse_param(pairs.next().unwrap());
            let d = parse_param(pairs.next().unwrap());
            cons(a, b, c, d)
        }
        Rule::data => Stmt::Data(pair.into_inner().map(parse_param).collect()),
        Rule::data_array => {
            let mut pairs = pair.into_inner();
            let val = parse_num(pairs.next().unwrap());
            let len = parse_num(pairs.next().unwrap());
            Stmt::DataArray(val, len as usize)
        }
        _ => unreachable!(),
    }
}

fn main() {
    let matches = clap::App::new("intcode-asm")
        .version(clap::crate_version!())
        .author(clap::crate_authors!())
        .about("Assembler for intcode from Advent of Code 2019")
        .arg(
            clap::Arg::with_name("file")
                .help("The file to assemble")
                .required(true),
        )
        .arg(
            clap::Arg::with_name("run")
                .short("r")
                .long("run")
                .help("Run the program after assembling"),
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
    let content = fs::read_to_string(file).expect("cannot read file");
    let pairs = match AsmParser::parse(Rule::program, &content) {
        Ok(pairs) => pairs,
        Err(error) => {
            println!("Error during file parsing:");
            println!("{}", error.with_path(file));
            return;
        }
    };
    let mut stmts = Vec::new();

    for pair in pairs {
        match pair.as_rule() {
            Rule::stmt => stmts.push(parse_stmt(pair)),
            Rule::label => stmts.push({
                let ident = pair.into_inner().next().unwrap().as_str();
                Stmt::Label(ident)
            }),
            _ => (),
        }
    }

    let code = match matches.value_of("stack_size") {
        Some(stack_size) => intcode_asm::assemble_with_stack(&stmts, stack_size.parse().unwrap()),
        None => intcode_asm::assemble(&stmts),
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
