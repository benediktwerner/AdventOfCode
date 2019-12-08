use crate::ast::{BinOp, Expr, IdentEnv, Program, UnOp};

lalrpop_mod!(pub grammar);

pub enum Line {
    Func(crate::ast::Function),
    Stmt(crate::ast::Stmt),
}

fn unop(op: UnOp, a: Expr) -> Expr {
    Expr::UnOp(op, Box::new(a))
}

fn binop(a: Expr, op: BinOp, b: Expr) -> Expr {
    Expr::BinOp(Box::new(a), op, Box::new(b))
}

pub fn parse<'a>(
    input: &'a str,
) -> Result<(Program, IdentEnv), impl std::error::Error + std::fmt::Display + 'a> {
    let mut env = IdentEnv::new();
    match grammar::ProgramParser::new().parse(&mut env, input) {
        Ok(program) => Ok((program, env)),
        Err(error) => Err(error),
    }
}

pub fn strip_comments(s: String) -> String {
    let mut result = Vec::new();
    let regex = regex::Regex::new(r"\s*//.*").unwrap();
    for line in s.lines() {
        if !regex.is_match(line) {
            result.push(line);
        }
    }
    result.join("\n")
}
