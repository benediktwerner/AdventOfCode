use std::collections::hash_map::{Entry, HashMap};

pub type Ident = u32;

#[derive(Clone, PartialEq, Debug)]
pub struct Program {
    pub functions: Vec<Function>,
    pub stmts: Vec<Stmt>,
}

#[derive(Clone, PartialEq, Debug)]
pub struct Function {
    pub name: Ident,
    pub args: Vec<Ident>,
    pub body: Stmt,
}

#[derive(Clone, PartialEq, Debug)]
pub enum Stmt {
    Decl(Ident),
    DeclAssign(Ident, Expr),
    Assign(Ident, Expr),
    Block(Vec<Stmt>),
    If(Expr, Box<Stmt>),
    IfElse(Expr, Box<Stmt>, Box<Stmt>),
    Return(Option<Expr>),
    Expr(Expr),
}

#[derive(Clone, PartialEq, Debug)]
pub enum BinOp {
    Add,
    Sub,
    Mul,
    Div,
    Equal,
    LessThan,
    LessEqual,
    GreaterThan,
    GreaterEqual,
    And,
    Or,
}

#[derive(Clone, PartialEq, Debug)]
pub enum UnOp {
    Not,
    Neg,
}

#[derive(Clone, PartialEq, Debug)]
pub enum Expr {
    Func(Ident, Vec<Expr>),
    BinOp(Box<Expr>, BinOp, Box<Expr>),
    UnOp(UnOp, Box<Expr>),
    Var(Ident),
    Literal(i64),
}

#[derive(Default)]
pub struct IdentEnv<'a> {
    idents: Vec<&'a str>,
    map: HashMap<&'a str, Ident>,
}

impl<'a> IdentEnv<'a> {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn from_str(&mut self, s: &'a str) -> Ident {
        match self.map.entry(s) {
            Entry::Occupied(entry) => *entry.get(),
            Entry::Vacant(entry) => {
                let ident = self.idents.len() as u32;
                entry.insert(ident);
                self.idents.push(s);
                ident
            },
        }
    }

    pub fn to_str(&self, ident: Ident) -> &'a str {
        self.idents[ident as usize]
    }
}
