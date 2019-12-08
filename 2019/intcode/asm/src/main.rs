#[macro_use]
extern crate pest_derive;

use std::collections::hash_map::{Entry, HashMap};
use std::fs;

use intcode_asm::{Ident, Param, Stmt};
use pest::{iterators::Pair, Parser};

#[derive(Parser)]
#[grammar = "grammar.pest"]
pub struct AsmParser;

#[derive(Default)]
pub struct IdentEnv<'a> {
    map: HashMap<&'a str, u32>,
    next: u32,
}

impl<'a> IdentEnv<'a> {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn from_str(&mut self, s: &'a str) -> u32 {
        match self.map.entry(s) {
            Entry::Occupied(entry) => *entry.get(),
            Entry::Vacant(entry) => {
                entry.insert(self.next);
                self.next += 1;
                self.next
            }
        }
    }
}

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

fn parse_param<'a>(pair: Pair<'a, Rule>, env: &mut IdentEnv<'a>) -> Param {
    match pair.as_rule() {
        Rule::param => parse_param(pair.into_inner().next().unwrap(), env),
        Rule::ident => Param::IdentPositional(Ident("__user_label", env.from_str(pair.as_str()))),
        Rule::ident_immediate => {
            let s = pair.into_inner().next().unwrap().as_str();
            Param::IdentImmediate(Ident("__user_label", env.from_str(s)))
        }
        Rule::num => Param::ValueImmediate(parse_num(pair)),
        Rule::num_positional => {
            Param::ValuePositional(parse_num(pair.into_inner().next().unwrap()))
        }
        _ => unreachable!("unknown param rule: {}", pair.as_str()),
    }
}

fn parse_stmt<'a>(pair: Pair<'a, Rule>, env: &mut IdentEnv<'a>) -> Stmt {
    match pair.as_rule() {
        Rule::stmt => parse_stmt(pair.into_inner().next().unwrap(), env),
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
            let a = parse_param(pairs.next().unwrap(), env);
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
                "loads" => Stmt::LoadStack,
                "stores" => Stmt::StoreStack,
                other => unreachable!("unknown binary instruction: {}", other),
            };
            let a = parse_param(pairs.next().unwrap(), env);
            let b = parse_param(pairs.next().unwrap(), env);
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
            let a = parse_param(pairs.next().unwrap(), env);
            let b = parse_param(pairs.next().unwrap(), env);
            let c = parse_param(pairs.next().unwrap(), env);
            cons(a, b, c)
        }
        Rule::quaternary_stmt => {
            let mut pairs = pair.into_inner();
            let cons = match pairs.next().unwrap().as_str() {
                "divmod" => Stmt::DivMod,
                other => unreachable!("unknown quaternary instruction: {}", other),
            };
            let a = parse_param(pairs.next().unwrap(), env);
            let b = parse_param(pairs.next().unwrap(), env);
            let c = parse_param(pairs.next().unwrap(), env);
            let d = parse_param(pairs.next().unwrap(), env);
            cons(a, b, c, d)
        }
        Rule::data => Stmt::Data(pair.into_inner().map(|d| parse_param(d, env)).collect()),
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
    let mut env = IdentEnv::new();

    for pair in pairs {
        match pair.as_rule() {
            Rule::stmt => stmts.push(parse_stmt(pair, &mut env)),
            Rule::label => stmts.push({
                let ident = pair.into_inner().next().unwrap().as_str();
                Stmt::Label(Ident("__user_label", env.from_str(ident)))
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
