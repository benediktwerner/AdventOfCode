use std::io::{self, BufRead, Write};

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub enum Arg {
    Positional(i64),
    Immediate(i64),
}

impl Arg {
    pub fn as_target(self) -> usize {
        match self {
            Self::Positional(val) => val as usize,
            _ => panic!("Immediate argument as target"),
        }
    }
}
impl std::fmt::Display for Arg {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            Self::Positional(val) => write!(f, "[{}]", val),
            Self::Immediate(val) => write!(f, "{}", val),
        }
    }
}

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
pub enum Instr {
    Add(Arg, Arg, Arg),
    Mul(Arg, Arg, Arg),
    In(Arg),
    Out(Arg),
    JumpTrue(Arg, Arg),
    JumpFalse(Arg, Arg),
    LessThan(Arg, Arg, Arg),
    Equal(Arg, Arg, Arg),
    Halt,
}

impl std::fmt::Display for Instr {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        use Instr::*;
        match self {
            Add(a, b, c) => write!(f, "add {} {} {}", a, b, c),
            Mul(a, b, c) => write!(f, "mul {} {} {}", a, b, c),
            In(a) => write!(f, "in {}", a),
            Out(a) => write!(f, "out {}", a),
            JumpTrue(a, b) => write!(f, "jmp_true {} {}", a, b),
            JumpFalse(a, b) => write!(f, "jmp_false {} {}", a, b),
            LessThan(a, b, c) => write!(f, "lt {} {} {}", a, b, c),
            Equal(a, b, c) => write!(f, "eq {} {} {}", a, b, c),
            Halt => write!(f, "hlt"),
        }
    }
}

pub struct VM {
    pub memory: Vec<i64>,
    pub ip: usize,
    arg_modes: i64,
    trace: bool,
}

impl VM {
    pub fn new(memory: Vec<i64>, trace: bool) -> Self {
        Self {
            memory,
            ip: 0,
            arg_modes: 0,
            trace,
        }
    }

    fn make_instr1(&mut self, cons: fn(Arg) -> Instr) -> Instr {
        cons(self.fetch_arg())
    }

    fn make_instr2(&mut self, cons: fn(Arg, Arg) -> Instr) -> Instr {
        cons(self.fetch_arg(), self.fetch_arg())
    }

    fn make_instr3(&mut self, cons: fn(Arg, Arg, Arg) -> Instr) -> Instr {
        cons(self.fetch_arg(), self.fetch_arg(), self.fetch_arg())
    }

    fn fetch(&mut self) -> i64 {
        let val = self.memory[self.ip];
        self.ip += 1;
        val
    }

    fn fetch_arg(&mut self) -> Arg {
        let val = self.fetch();
        let mode = self.arg_modes % 10;
        self.arg_modes /= 10;
        match mode {
            0 => Arg::Positional(val),
            1 => Arg::Immediate(val),
            _ => panic!("Invalid arg mode: {}", mode),
        }
    }

    fn decode(&mut self) -> Instr {
        let instr = self.fetch();
        let opcode = instr % 100;
        self.arg_modes = instr / 100;

        match opcode {
            1 => self.make_instr3(Instr::Add),
            2 => self.make_instr3(Instr::Mul),
            3 => self.make_instr1(Instr::In),
            4 => self.make_instr1(Instr::Out),
            5 => self.make_instr2(Instr::JumpTrue),
            6 => self.make_instr2(Instr::JumpFalse),
            7 => self.make_instr3(Instr::LessThan),
            8 => self.make_instr3(Instr::Equal),
            99 => Instr::Halt,
            _ => panic!("Invalid opcode: {} at position {}", opcode, self.ip - 1),
        }
    }

    fn get_arg(&self, arg: Arg) -> i64 {
        match arg {
            Arg::Positional(val) => self.memory[val as usize],
            Arg::Immediate(val) => val,
        }
    }

    fn store(&mut self, arg: Arg, val: i64) {
        self.memory[arg.as_target()] = val;
    }

    pub fn run(&mut self) {
        loop {
            use Instr::*;
            let ip = self.ip;
            let instr = self.decode();
            if self.trace {
                println!("{}: {}", ip, instr);
            }
            match instr {
                Add(a, b, c) => self.store(c, self.get_arg(a) + self.get_arg(b)),
                Mul(a, b, c) => self.store(c, self.get_arg(a) * self.get_arg(b)),
                In(a) => {
                    print!("Input: ");
                    io::stdout().flush().unwrap();
                    let stdin = io::stdin();
                    let line = stdin.lock().lines().next().unwrap().unwrap();
                    let input = line.parse().unwrap();
                    self.store(a, input);
                }
                Out(a) => println!("Output: {}", self.get_arg(a)),
                JumpTrue(cond, target) => {
                    if self.get_arg(cond) != 0 {
                        self.ip = self.get_arg(target) as usize;
                    }
                }
                JumpFalse(cond, target) => {
                    if self.get_arg(cond) == 0 {
                        self.ip = self.get_arg(target) as usize;
                    }
                }
                LessThan(a, b, c) => self.store(
                    c,
                    if self.get_arg(a) < self.get_arg(b) {
                        1
                    } else {
                        0
                    },
                ),
                Equal(a, b, c) => self.store(
                    c,
                    if self.get_arg(a) == self.get_arg(b) {
                        1
                    } else {
                        0
                    },
                ),
                Halt => break,
            }
        }
    }
}
