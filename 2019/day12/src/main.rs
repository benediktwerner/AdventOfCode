use std::collections::HashSet;

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
struct Axis {
    pos: i32,
    vel: i32,
}

impl Axis {
    fn new(pos: i32) -> Self {
        Self { pos, vel: 0 }
    }
    fn attract(&mut self, other: &mut Self) {
        if self.pos > other.pos {
            self.vel -= 1;
            other.vel += 1;
        } else if self.pos < other.pos {
            self.vel += 1;
            other.vel -= 1;
        }
    }
    fn mov(&mut self) {
        self.pos += self.vel;
    }
}

#[derive(Clone, Copy, PartialEq, Eq, Hash, Debug)]
struct Moon(Axis, Axis, Axis);

impl Moon {
    fn new(x: i32, y: i32, z: i32) -> Self {
        Self(Axis::new(x), Axis::new(y), Axis::new(z))
    }

    fn attract(&mut self, other: &mut Self) {
        self.0.attract(&mut other.0);
        self.1.attract(&mut other.1);
        self.2.attract(&mut other.2);
    }
    fn mov(&mut self) {
        self.0.mov();
        self.1.mov();
        self.2.mov();
    }
    fn energy(&self) -> i32 {
        let pot = self.0.pos.abs() + self.1.pos.abs() + self.2.pos.abs();
        let kin = self.0.vel.abs() + self.1.vel.abs() + self.2.vel.abs();
        pot * kin
    }
}

fn period(mut a: Axis, mut b: Axis, mut c: Axis, mut d: Axis) -> u64 {
    let mut seen = HashSet::new();
    for i in 0.. {
        if !seen.insert((a, b, c, d)) {
            return i;
        }
        a.attract(&mut b);
        a.attract(&mut c);
        a.attract(&mut d);
        b.attract(&mut c);
        b.attract(&mut d);
        c.attract(&mut d);
        a.mov();
        b.mov();
        c.mov();
        d.mov();
    }
    unreachable!()
}

fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b > 0 {
        let tmp = a % b;
        a = b;
        b = tmp;
    }
    a
}

fn lcm(a: u64, b: u64) -> u64 {
    a * b / gcd(a, b)
}

fn main() {
    let mut a = Moon::new(4, 1, 1);
    let mut b = Moon::new(11, -18, -1);
    let mut c = Moon::new(-2, -10, -4);
    let mut d = Moon::new(-7, -2, 14);

    for _ in 0..1000 {
        a.attract(&mut b);
        a.attract(&mut c);
        a.attract(&mut d);
        b.attract(&mut c);
        b.attract(&mut d);
        c.attract(&mut d);
        a.mov();
        b.mov();
        c.mov();
        d.mov();
    }
    println!(
        "Part 1: {}",
        a.energy() + b.energy() + c.energy() + d.energy()
    );

    let period_x = period(Axis::new(4), Axis::new(11), Axis::new(-2), Axis::new(-7));
    let period_y = period(Axis::new(1), Axis::new(-18), Axis::new(-10), Axis::new(-2));
    let period_z = period(Axis::new(1), Axis::new(-1), Axis::new(-4), Axis::new(14));

    println!("Part 2: {}", lcm(period_x, lcm(period_y, period_z)));
}
