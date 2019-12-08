use std::collections::HashMap;

use intcode_asm as asm;

use crate::ast::*;

const TMP: asm::Ident = asm::Ident("__compiler_tmp", 0);
const TMP2: asm::Ident = asm::Ident("__compiler_tmp_2", 0);

type Result<T = ()> = std::result::Result<T, CompilerError>;

pub enum CompilerError {
    DuplicateDeclaration(Ident),
    UndefinedVar(Ident),
}

pub fn gen(program: Program, env: &IdentEnv) -> Result<Vec<asm::Stmt>> {
    Gen::new(env).generate(program)
}

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
enum Target {
    StackTop,
    Var(VarLocation),
}

impl From<VarLocation> for Target {
    fn from(loc: VarLocation) -> Self {
        Self::Var(loc)
    }
}

impl From<asm::Ident> for Target {
    fn from(ident: asm::Ident) -> Self {
        VarLocation::from(ident).into()
    }
}

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
enum VarLocation {
    Local(i64),
    Global(asm::Ident),
}

impl From<asm::Ident> for VarLocation {
    fn from(ident: asm::Ident) -> Self {
        Self::Global(ident)
    }
}

struct Gen<'a> {
    scopes: Vec<HashMap<Ident, VarLocation>>,
    code: Vec<asm::Stmt>,
    label_count: u32,
    next_var_index: u32,
    stack_height: u32,
    env: &'a IdentEnv<'a>,
}

impl<'a> Gen<'a> {
    fn new(env: &'a IdentEnv<'a>) -> Self {
        Gen {
            scopes: vec![HashMap::new()],
            code: Vec::new(),
            label_count: 0,
            next_var_index: 0,
            stack_height: 0,
            env,
        }
    }

    fn generate(mut self, program: Program) -> Result<Vec<asm::Stmt>> {
        for stmt in program.stmts {
            self.gen_stmt(stmt)?;
        }
        self.push(asm::Stmt::Halt);
        for func in program.functions {
            self.gen_func(func)?;
        }

        Ok(self.code)
    }

    fn decl(&mut self, ident: Ident) -> Result {
        let is_global = self.scopes.len() == 1;
        let scope = self.scopes.last_mut().unwrap();
        if scope.contains_key(&ident) {
            return Err(CompilerError::DuplicateDeclaration(ident));
        }
        if is_global {
            scope.insert(
                ident,
                VarLocation::Global(asm::Ident("__compiler_global", ident)),
            );
        } else {
            scope.insert(ident, VarLocation::Local(self.next_var_index as i64 + 1));
            self.next_var_index += 1;
            self.add_stack_ptr(1);
        }
        Ok(())
    }

    fn gen_func(&mut self, func: Function) -> Result {
        let mut scope = HashMap::new();
        for (i, arg) in func.args.iter().rev().enumerate() {
            scope.insert(*arg, VarLocation::Local(-(i as i64) - 1));
        }
        self.scopes.push(scope);

        self.stack_height = 0;
        self.next_var_index = 0;

        self.push(asm::Stmt::Label(asm::Ident("__compiler_func", func.name)));

        self.gen_stmt(func.body)?;
        self.gen_stmt(Stmt::Return(None))?;

        assert_eq!(self.stack_height, self.next_var_index);
        self.add_stack_ptr(-(self.stack_height as i64));

        Ok(())
    }

    fn gen_expr(&mut self, expr: Expr, target: impl Into<Target>) -> Result {
        let target = target.into();
        match expr {
            Expr::Func(name, args) => {
                // TODO: check arg count
                match self.env.to_str(name) {
                    "print" => {
                        self.gen_expr(args.into_iter().next().unwrap(), TMP)?;
                        self.push(asm::Stmt::Out(TMP.to_pos()));
                    }
                    "input" => {
                        self.push(asm::Stmt::In(TMP.to_pos()));
                        self.mov(TMP.to_pos(), target);
                    }
                    "exit" => {
                        self.push(asm::Stmt::Halt);
                    }
                    _ => {
                        let argc = args.len() as i64;
                        for arg in args {
                            self.gen_expr(arg, Target::StackTop)?;
                        }
                        self.push(asm::Stmt::Call(
                            asm::Ident("__compiler_func", name).to_imm(),
                        ));
                        self.add_stack_ptr(-argc);
                        self.mov(TMP.to_pos(), target);
                    }
                }
            }
            Expr::BinOp(left, op, right) => {
                self.gen_expr(*left, Target::StackTop)?;
                self.gen_expr(*right, TMP)?;
                self.pop_stack(TMP2.to_pos());
                let op = match op {
                    BinOp::Add => asm::Stmt::Add,
                    BinOp::Sub => asm::Stmt::Sub,
                    BinOp::Mul => asm::Stmt::Mul,
                    BinOp::Div => asm::Stmt::Div,
                    BinOp::Equal => asm::Stmt::Equal,
                    BinOp::LessThan => asm::Stmt::LessThan,
                    BinOp::LessEqual => asm::Stmt::LessEqual,
                    BinOp::GreaterThan => asm::Stmt::GreaterThan,
                    BinOp::GreaterEqual => asm::Stmt::GreaterEqual,
                    BinOp::And => asm::Stmt::And,
                    BinOp::Or => asm::Stmt::Or,
                };
                self.push(op(TMP2.to_pos(), TMP.to_pos(), TMP.to_pos()));
                self.mov(TMP.to_pos(), target);
            }
            Expr::UnOp(op, expr) => {
                self.gen_expr(*expr, TMP)?;
                match op {
                    UnOp::Neg => self.push(asm::Stmt::Mul(TMP.to_pos(), (-1).into(), TMP.to_pos())),
                    UnOp::Not => self.push(asm::Stmt::Not(TMP.to_pos(), TMP.to_pos())),
                }
                self.mov(TMP.to_pos(), target);
            }
            Expr::Var(name) => match self.get_location(name)? {
                VarLocation::Global(ident) => self.mov(ident.to_pos(), target),
                VarLocation::Local(pos) => {
                    self.push(asm::Stmt::LoadStack(self.stack_index(pos), TMP.to_pos()));
                    self.mov(TMP.to_pos(), target);
                }
            },
            Expr::Literal(val) => self.mov(val, target),
        }
        Ok(())
    }

    fn get_location(&self, ident: Ident) -> Result<VarLocation> {
        for scope in self.scopes.iter().rev() {
            if let Some(loc) = scope.get(&ident) {
                return Ok(*loc);
            }
        }
        Err(CompilerError::UndefinedVar(ident))
    }

    fn mov(&mut self, val: impl Into<asm::Param>, target: Target) {
        let val = val.into();
        match target {
            Target::StackTop => self.push_stack(val),
            Target::Var(VarLocation::Global(target)) => {
                if let asm::Param::IdentPositional(val) = val {
                    if val == target {
                        return;
                    }
                }
                self.push(asm::Stmt::Mov(val, target.to_pos()));
            }
            Target::Var(VarLocation::Local(pos)) => {
                self.push(asm::Stmt::StoreStack(val, self.stack_index(pos)));
            }
        }
    }
    fn gen_stmt(&mut self, stmt: Stmt) -> Result {
        match stmt {
            Stmt::Decl(ident) => self.decl(ident)?,
            Stmt::DeclAssign(ident, expr) => {
                self.decl(ident)?;
                self.gen_expr(expr, self.get_location(ident)?)?;
            }
            Stmt::Assign(ident, expr) => self.gen_expr(expr, self.get_location(ident)?)?,
            Stmt::Block(stmts) => {
                self.scopes.push(HashMap::new());
                for stmt in stmts {
                    self.gen_stmt(stmt)?;
                }
                self.scopes.pop();
            }
            Stmt::If(cond, body) => {
                self.gen_expr(cond, TMP)?;
                let label = self.make_label();
                self.jmp_false(TMP, label);
                self.gen_stmt(*body)?;
                self.label(label);
            }
            Stmt::IfElse(cond, if_body, else_body) => {
                self.gen_expr(cond, TMP)?;
                let label_false = self.make_label();
                let label_end = self.make_label();
                self.jmp_false(TMP, label_false);
                self.gen_stmt(*if_body)?;
                self.jmp(label_end);
                self.label(label_false);
                self.gen_stmt(*else_body)?;
                self.label(label_end);
            }
            Stmt::Return(val) => {
                if let Some(val) = val {
                    self.gen_expr(val, TMP)?;
                } else {
                    self.push(asm::Stmt::Mov(0.into(), TMP.to_pos()));
                }
                self.push(asm::Stmt::Ret);
            }
            Stmt::Expr(expr) => self.gen_expr(expr, TMP)?,
        }
        Ok(())
    }

    fn make_label(&mut self) -> asm::Ident {
        let index = self.label_count;
        self.label_count += 1;
        asm::Ident("__compiler_label", index)
    }

    fn jmp(&mut self, target: asm::Ident) {
        self.push(asm::Stmt::Jmp(target.to_imm()))
    }

    fn jmp_false(&mut self, cond: asm::Ident, target: asm::Ident) {
        self.push(asm::Stmt::JumpFalse(cond.to_pos(), target.to_imm()))
    }

    fn label(&mut self, ident: asm::Ident) {
        self.push(asm::Stmt::Label(ident))
    }

    fn push_stack(&mut self, val: asm::Param) {
        self.push(asm::Stmt::Push(val));
        self.stack_height += 1;
    }

    fn pop_stack(&mut self, val: asm::Param) {
        self.push(asm::Stmt::Pop(val));
        self.stack_height -= 1;
    }

    fn stack_index(&self, offset: i64) -> asm::Param {
        (offset - self.stack_height as i64 - 1).into()
    }

    fn add_stack_ptr(&mut self, amount: i64) {
        if amount != 0 {
            self.push(asm::Stmt::AddStackPtr(amount.into()));
            self.stack_height = (self.stack_height as i64 + amount) as u32;
        }
    }

    fn push(&mut self, stmt: asm::Stmt) {
        self.code.push(stmt);
    }
}
