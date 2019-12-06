use std::collections::{hash_map::Entry, HashMap};

const DEFAULT_STACK_SIZE: usize = 100;

const ADD: i64 = 1;
const MUL: i64 = 2;
const IN: i64 = 3;
const OUT: i64 = 4;
const JUMP_TRUE: i64 = 5;
const JUMP_FALSE: i64 = 6;
const LESS_THAN: i64 = 7;
const EQUAL: i64 = 8;
const HALT: i64 = 99;

#[derive(Clone, Copy, PartialEq, Debug)]
pub enum Param<'a> {
    IdentPositional(&'a str),
    IdentImmediate(&'a str),
    #[doc(hidden)]
    __IdentPositionalMacro(&'a str, u32),
    #[doc(hidden)]
    __IdentImmediateMacro(&'a str, u32),
    Value(i64),
}

impl Param<'_> {
    fn macro_ident(name: &'static str, asm: &mut Assembler) -> Self {
        if &name[0..1] == ":" {
            Self::__IdentImmediateMacro(&name[1..], asm.get_macro_id())
        } else {
            Self::__IdentPositionalMacro(name, asm.get_macro_id())
        }
    }
}

impl From<&'static str> for Param<'static> {
    fn from(name: &'static str) -> Self {
        if &name[0..1] == ":" {
            Self::IdentImmediate(&name[1..])
        } else {
            Self::IdentPositional(name)
        }
    }
}

impl From<i64> for Param<'static> {
    fn from(x: i64) -> Self {
        Self::Value(x)
    }
}

#[derive(Clone, PartialEq, Debug)]
pub enum Stmt<'a> {
    Label(&'a str),
    #[doc(hidden)]
    __LabelMacro(&'a str, u32),
    Add(Param<'a>, Param<'a>, Param<'a>),
    Mul(Param<'a>, Param<'a>, Param<'a>),
    In(Param<'a>),
    Out(Param<'a>),
    JumpTrue(Param<'a>, Param<'a>),
    JumpFalse(Param<'a>, Param<'a>),
    LessThan(Param<'a>, Param<'a>, Param<'a>),
    Equal(Param<'a>, Param<'a>, Param<'a>),
    Data(Vec<Param<'a>>),
    DataArray(i64, usize),
    Halt,

    Load(Param<'a>, Param<'a>),
    Store(Param<'a>, Param<'a>),

    Push(Param<'a>),
    Pop(Param<'a>),
    Call(Param<'a>),
    Ret,

    Mov(Param<'a>, Param<'a>),
    Sub(Param<'a>, Param<'a>, Param<'a>),
    Div(Param<'a>, Param<'a>, Param<'a>),
    Mod(Param<'a>, Param<'a>, Param<'a>),
    DivMod(Param<'a>, Param<'a>, Param<'a>, Param<'a>),
    Jmp(Param<'a>),
    And(Param<'a>, Param<'a>, Param<'a>),
    Or(Param<'a>, Param<'a>, Param<'a>),
    Not(Param<'a>, Param<'a>),
    LessEqual(Param<'a>, Param<'a>, Param<'a>),
    GreaterThan(Param<'a>, Param<'a>, Param<'a>),
    GreaterEqual(Param<'a>, Param<'a>, Param<'a>),
}

impl Stmt<'_> {
    fn opcode(&self) -> i64 {
        use Stmt::*;
        match self {
            Add(..) => ADD,
            Mul(..) => MUL,
            In(..) => IN,
            Out(..) => OUT,
            JumpTrue(..) => JUMP_TRUE,
            JumpFalse(..) => JUMP_FALSE,
            LessThan(..) => LESS_THAN,
            Equal(..) => EQUAL,
            Halt => HALT,
            _ => panic!("Stmt {:?} has no opcode", self),
        }
    }
}

macro_rules! param {
    ($l:literal) => {
        Param::from($l)
    };
    (($self:ident $l:literal)) => {
        Param::macro_ident($l, $self)
    };
    ((- $l:literal)) => {
        Param::from(-$l)
    };
    ($e:expr) => {
        *$e
    };
}

macro_rules! assemble {
    [$self:ident, $([$($t:tt)*]),* $(,)?] => {
        {
            let stmts = &[$(stmt!($($t)*)),*];
            $self.assemble_stmts(stmts);
        }
    }
}

// macro_rules! stmts {
//     [$([$($t:tt)*]),* $(,)?] => {
//         &[$(stmt!($($t)*)),*]
//     };
// }

macro_rules! stmt {
    (label $n:literal) => {
        Stmt::Label($n)
    };
    (label $self:ident $n:literal) => {
        Stmt::__LabelMacro($n, $self.get_macro_id())
    };

    (add $a:tt $b:tt $c:tt) => {
        Stmt::Add(param!($a), param!($b), param!($c))
    };
    (mul $a:tt $b:tt $c:tt) => {
        Stmt::Mul(param!($a), param!($b), param!($c))
    };
    (sub $a:tt $b:tt $c:tt) => {
        Stmt::Sub(param!($a), param!($b), param!($c))
    };
    (div $a:tt $b:tt $c:tt) => {
        Stmt::Div(param!($a), param!($b), param!($c))
    };
    (divmod $a:tt $b:tt $c:tt $d:tt) => {
        Stmt::DivMod(param!($a), param!($b), param!($c), param!($d))
    };

    (eq $a:tt $b:tt $c:tt) => {
        Stmt::Equal(param!($a), param!($b), param!($c))
    };
    (lt $a:tt $b:tt $c:tt) => {
        Stmt::LessThan(param!($a), param!($b), param!($c))
    };
    (leq $a:tt $b:tt $c:tt) => {
        Stmt::LessEqual(param!($a), param!($b), param!($c))
    };
    (gt $a:tt $b:tt $c:tt) => {
        Stmt::GreaterThan(param!($a), param!($b), param!($c))
    };
    (geq $a:tt $b:tt $c:tt) => {
        Stmt::GreaterEqual(param!($a), param!($b), param!($c))
    };

    (and $a:tt $b:tt $c:tt) => {
        Stmt::And(param!($a), param!($b), param!($c))
    };
    (or $a:tt $b:tt $c:tt) => {
        Stmt::Or(param!($a), param!($b), param!($c))
    };
    (not $a:tt $b:tt) => {
        Stmt::Not(param!($a), param!($b))
    };

    (in $a:tt) => {
        Stmt::In(param!($a))
    };
    (out $a:tt) => {
        Stmt::Out(param!($a))
    };
    (mov $a:tt $b:tt) => {
        Stmt::Mov(param!($a), param!($b))
    };
    (load $a:tt $b:tt) => {
        Stmt::Load(param!($a), param!($b))
    };
    (store $a:tt $b:tt) => {
        Stmt::Store(param!($a), param!($b))
    };
    (push $a:tt) => {
        Stmt::Push(param!($a))
    };
    (pop $a:tt) => {
        Stmt::Pop(param!($a))
    };
    (call $a:tt) => {
        Stmt::Call(param!($a))
    };
    (ret) => {
        Stmt::Ret
    };

    (jmp $a:tt) => {
        Stmt::Jmp(param!($a))
    };
    (jnz $a:tt $b:tt) => {
        Stmt::JumpTrue(param!($a), param!($b))
    };
    (jtrue $a:tt $b:tt) => {
        Stmt::JumpTrue(param!($a), param!($b))
    };
    (jz $a:tt $b:tt) => {
        Stmt::JumpFalse(param!($a), param!($b))
    };
    (jfalse $a:tt $b:tt) => {
        Stmt::JumpFalse(param!($a), param!($b))
    };

    (data $($t:tt)+) => {
        Stmt::Data(vec![$(param!($t)),+])
    };

    (array $a:tt $b:expr) => {
        Stmt::DataArray($a, $b)
    };
}

#[derive(Default)]
struct Assembler<'a> {
    code: Vec<i64>,
    labels: HashMap<(&'a str, u32), usize>,
    patches: HashMap<(&'a str, u32), Vec<usize>>,
    macro_counter: u32,
    increase_macro_counter: bool,
    has_halt: bool,
    has_stack: bool,
    stack_size: usize,
}

impl<'a> Assembler<'a> {
    fn assemble(mut self, stmts: &[Stmt<'a>]) -> Vec<i64> {
        self.assemble_stmts(stmts);

        if self.has_stack {
            if self.stack_size == 0 {
                self.stack_size = DEFAULT_STACK_SIZE;
            }
            assemble!(self,
                [label "__stack_ptr"],
                [data "__stack"],
                [label "__stack"],
                [array 0 self.stack_size],
            );
        }

        for (k, locs) in self.patches {
            let pos = match self.labels.get(&k) {
                Some(pos) => *pos,
                None => {
                    let pos = self.code.len();
                    self.code.push(0);
                    pos
                }
            } as i64;

            for loc in locs {
                self.code[loc] += pos;
            }
        }

        if !self.has_halt {
            eprintln!("Warning: The program has no 'hlt' instruction!");
        }

        self.code
    }

    fn assemble_stmts(&mut self, stmts: &[Stmt<'a>]) {
        for stmt in stmts {
            self.assemble_stmt(stmt);
        }
    }

    fn assemble_stmt(&mut self, stmt: &Stmt<'a>) {
        use Stmt::*;
        match stmt {
            Label(name) => match self.labels.entry((name, 0)) {
                Entry::Occupied(_) => panic!("Duplicate label definition: {}", name),
                Entry::Vacant(entry) => {
                    entry.insert(self.code.len());
                }
            },
            __LabelMacro(name, macro_id) => match self.labels.entry((name, *macro_id)) {
                Entry::Occupied(_) => panic!("Duplicate label definition: {}", name),
                Entry::Vacant(entry) => {
                    entry.insert(self.code.len());
                }
            },
            Add(a, b, c) | Mul(a, b, c) | LessThan(a, b, c) | Equal(a, b, c) => {
                let (a, ma) = self.assemble_param(1, a);
                let (b, mb) = self.assemble_param(2, b);
                let (c, mc) = self.assemble_param(3, c);
                self.push(stmt.opcode() + ma * 100 + mb * 1_000 + mc * 10_000);
                self.push(a);
                self.push(b);
                self.push(c);
            }
            JumpTrue(a, b) | JumpFalse(a, b) => {
                let (a, ma) = self.assemble_param(1, a);
                let (b, mb) = self.assemble_param(2, b);
                self.push(stmt.opcode() + ma * 100 + mb * 1_000);
                self.push(a);
                self.push(b);
            }
            In(a) | Out(a) => {
                let (a, ma) = self.assemble_param(1, a);
                self.push(stmt.opcode() + ma * 100);
                self.push(a);
            }
            Data(vals) => {
                for val in vals {
                    let (v, _) = self.assemble_param(0, val);
                    self.push(v);
                }
            }
            DataArray(val, len) => {
                for _ in 0..*len as usize {
                    self.push(*val);
                }
            }
            Halt => {
                self.has_halt = true;
                self.push(99);
            }

            Load(a, b) => {
                // add a 0 __load+1
                let (a, ma) = self.assemble_param(1, a);
                self.push(ADD + ma * 100 + 1_000);
                self.push(a);
                self.push(0);
                let macro_id = self.get_macro_id();
                self.patches
                    .entry(("__load", macro_id))
                    .or_default()
                    .push(self.code.len());
                self.push(1);

                assemble!(self, [label self "__load"]);

                let (b, mb) = self.assemble_param(3, b);
                self.push(ADD + 1_000 + mb * 10_000);
                self.push(0);
                self.push(0);
                self.push(b);
            }
            Store(a, b) => {
                // add b 0 __store+3
                let (b, mb) = self.assemble_param(1, b);
                self.push(ADD + mb * 100 + 1_000);
                self.push(b);
                self.push(0);
                let macro_id = self.get_macro_id();
                self.patches
                    .entry(("__store", macro_id))
                    .or_default()
                    .push(self.code.len());
                self.push(3);
                assemble!(self,
                    [label self "__store"],
                );

                let (a, ma) = self.assemble_param(1, a);
                self.push(ADD + ma * 100 + 1_000);
                self.push(a);
                self.push(0);
                self.push(0);
            }
            Push(a) => {
                self.has_stack = true;
                assemble!(self,
                    [store a "__stack_ptr"],
                    [add "__stack_ptr" 1 "__stack_ptr"],
                )
            }
            Pop(a) => {
                self.has_stack = true;
                assemble!(self,
                    [add "__stack_ptr" (-1) "__stack_ptr"],
                    [load "__stack_ptr" a],
                )
            }
            Call(a) => {
                self.has_stack = true;
                assemble!(self,
                    [push (self ":__ret")],
                    [jmp a],
                    [label self "__ret"],
                );
            }
            Ret => {
                self.has_stack = true;
                assemble!(self,
                    [pop "__ret"],
                    [jmp "__ret"],
                )
            }

            Mov(a, b) => assemble!(self, [add 0 a b]),
            Sub(a, b, c) => assemble!(self,
                [mul (-1) b "__tmp"],
                [add a "__tmp" c],
            ),
            Div(a, b, c) => assemble!(self, [divmod a b c "__rest"]),
            Mod(a, b, c) => assemble!(self,
                [mov b "__div"],
                [mov a c],
                [label self "__loop"],
                [lt c "__div" "__tmp"],
                [jtrue "__tmp" (self ":__end")],
                [sub c "__div" c],
                [jmp (self ":__loop")],
                [label self "__end"],
            ),
            DivMod(a, b, c, d) => assemble!(self,
                [mov b "__div"],
                [mov a d],
                [mov 0 c],
                [label self "__loop"],
                [lt d "__div" "__tmp"],
                [jtrue "__tmp" (self ":__end")],
                [sub d "__div" d],
                [add c 1 c],
                [jmp (self ":__loop")],
                [label self "__end"],
            ),
            Jmp(a) => assemble!(self, [add 0 0 "__tmp"], [jz "__tmp" a]),
            And(a, b, c) => assemble!(self,
                [jfalse a (self ":__first")],
                [mov b c],
                [jmp (self ":__end")],
                [label self "__first"],
                [mov a c],
                [label self "__end"],
            ),
            Or(a, b, c) => assemble!(self,
                [jtrue a (self ":__first")],
                [mov b c],
                [jmp (self ":__end")],
                [label self "__first"],
                [mov a c],
                [label self "__end"],
            ),
            Not(a, b) => assemble!(self,
                [jfalse a (self ":__false")],
                [mov 1 b],
                [jmp (self ":__end")],
                [label self "__false"],
                [mov 0 b],
                [label self "__end"],
            ),
            LessEqual(a, b, c) => assemble!(self,
                [lt a b "__tmp"],
                [eq a b c],
                [or "__tmp" c c],
            ),
            GreaterThan(a, b, c) => assemble!(self,
                [lt b a c],
            ),
            GreaterEqual(a, b, c) => assemble!(self,
                [leq b a c],
            ),
        }

        if self.increase_macro_counter {
            self.increase_macro_counter = false;
            self.macro_counter += 1;
        }
    }

    fn assemble_param(&mut self, i: usize, param: &Param<'a>) -> (i64, i64) {
        match param {
            Param::IdentPositional(name) => {
                self.patches
                    .entry((name, 0))
                    .or_default()
                    .push(self.code.len() + i);
                (0, 0)
            }
            Param::IdentImmediate(name) => {
                self.patches
                    .entry((name, 0))
                    .or_default()
                    .push(self.code.len() + i);
                (0, 1)
            }
            Param::__IdentPositionalMacro(name, macro_id) => {
                self.patches
                    .entry((name, *macro_id))
                    .or_default()
                    .push(self.code.len() + i);
                (0, 0)
            }
            Param::__IdentImmediateMacro(name, macro_id) => {
                self.patches
                    .entry((name, *macro_id))
                    .or_default()
                    .push(self.code.len() + i);
                (0, 1)
            }
            Param::Value(val) => (*val, 1),
        }
    }

    fn get_macro_id(&mut self) -> u32 {
        self.increase_macro_counter = true;
        self.macro_counter
    }

    fn push(&mut self, val: i64) {
        self.code.push(val);
    }
}

pub fn assemble(stmts: &[Stmt]) -> Vec<i64> {
    Assembler::default().assemble(stmts)
}

pub fn assemble_with_stack(stmts: &[Stmt], stack_size: usize) -> Vec<i64> {
    let mut asm = Assembler::default();
    asm.stack_size = stack_size;
    asm.has_stack = true;
    asm.assemble(stmts)
}
