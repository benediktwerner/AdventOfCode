use std::collections::HashMap;

use memuse::DynamicUsage;
use rayon::prelude::*;

struct Solver {
    ore_cost: u32,
    clay_cost: u32,
    obsidian_ore: u32,
    obsidian_clay: u32,
    geode_ore: u32,
    geode_obsidian: u32,
    state: State,
    dp: HashMap<State, u32>,
    max_ore: u32,
    max_clay: u32,
    max_obsidian: u32,
}

#[derive(Clone, Copy, Hash, PartialEq, Eq, Default)]
struct State {
    ore: u32,
    clay: u32,
    obsidian: u32,
    ore_robots: u32,
    clay_robots: u32,
    obsidian_robots: u32,
    geode_robots: u32,
    mins: u32,
}

memuse::impl_no_dynamic_usage!(State);

impl State {
    const fn initial(mins: u32) -> Self {
        Self {
            ore: 0,
            clay: 0,
            obsidian: 0,
            ore_robots: 1,
            clay_robots: 0,
            obsidian_robots: 0,
            geode_robots: 0,
            mins,
        }
    }
    fn produce(&mut self) {
        self.ore += self.ore_robots;
        self.clay += self.clay_robots;
        self.obsidian += self.obsidian_robots;
        self.mins -= 1;
    }
    fn unproduce(&mut self) {
        self.ore -= self.ore_robots;
        self.clay -= self.clay_robots;
        self.obsidian -= self.obsidian_robots;
        self.mins += 1;
    }
}

impl Solver {
    fn new(blueprint: (u32, u32, u32, u32, u32, u32, u32), mins: u32) -> Self {
        let (_id, ore, clay, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian) = blueprint;
        Self {
            ore_cost: ore,
            clay_cost: clay,
            obsidian_ore,
            obsidian_clay,
            geode_ore,
            geode_obsidian,
            state: State::initial(mins),
            dp: HashMap::new(),
            max_ore: ore.max(clay).max(obsidian_ore).max(geode_ore),
            max_clay: obsidian_clay,
            max_obsidian: geode_obsidian,
        }
    }

    fn sim(&mut self) -> u32 {
        if self.state.mins == 1 {
            return self.state.geode_robots;
        }
        if let Some(geode) = self.dp.get(&self.state) {
            return *geode;
        }
        // if self.state.mins > 23 {
        //     assert!(
        //         self.dp.dynamic_usage() < 5_000_000_000,
        //         "more than 5 GB RAM usage"
        //     );
        // }

        let clay = self.state.ore >= self.clay_cost && self.state.clay_robots < self.max_clay;
        let ore = self.state.ore >= self.ore_cost && self.state.ore_robots < self.max_ore;
        let obsidian = self.state.ore >= self.obsidian_ore
            && self.state.clay >= self.obsidian_clay
            && self.state.obsidian_robots < self.max_obsidian;
        let geode = self.state.ore >= self.geode_ore && self.state.obsidian >= self.geode_obsidian;
        let new_geode = self.state.geode_robots;
        self.state.produce();
        let mut best = new_geode + self.sim();
        if clay {
            self.state.ore -= self.clay_cost;
            self.state.clay_robots += 1;
            best = std::cmp::max(best, new_geode + self.sim());
            self.state.ore += self.clay_cost;
            self.state.clay_robots -= 1;
        }
        if ore {
            self.state.ore -= self.ore_cost;
            self.state.ore_robots += 1;
            best = std::cmp::max(best, new_geode + self.sim());
            self.state.ore += self.ore_cost;
            self.state.ore_robots -= 1;
        }
        if obsidian {
            self.state.ore -= self.obsidian_ore;
            self.state.clay -= self.obsidian_clay;
            self.state.obsidian_robots += 1;
            best = std::cmp::max(best, new_geode + self.sim());
            self.state.ore += self.obsidian_ore;
            self.state.clay += self.obsidian_clay;
            self.state.obsidian_robots -= 1;
        }
        if geode {
            self.state.ore -= self.geode_ore;
            self.state.obsidian -= self.geode_obsidian;
            self.state.geode_robots += 1;
            best = std::cmp::max(best, new_geode + self.sim());
            self.state.ore += self.geode_ore;
            self.state.obsidian += self.geode_obsidian;
            self.state.geode_robots -= 1;
        }
        self.state.unproduce();
        if self.state.mins > 5 {
            self.dp.insert(self.state, best);
        }

        best
    }
}

fn main() {
    let inp = [
        (1, 3, 4, 3, 19, 3, 8),
        (2, 3, 3, 3, 9, 2, 10),
        (3, 4, 4, 4, 20, 2, 12),
        (4, 4, 3, 2, 19, 3, 13),
        (5, 3, 4, 3, 16, 3, 14),
        (6, 4, 4, 2, 18, 4, 20),
        (7, 4, 4, 4, 11, 4, 12),
        (8, 3, 3, 2, 20, 2, 20),
        (9, 4, 4, 2, 11, 4, 8),
        (10, 4, 4, 4, 5, 3, 15),
        (11, 2, 4, 4, 15, 2, 15),
        (12, 4, 3, 2, 19, 3, 10),
        (13, 3, 3, 2, 16, 2, 18),
        (14, 4, 3, 3, 11, 4, 7),
        (15, 4, 3, 4, 18, 3, 13),
        (16, 4, 4, 4, 14, 3, 16),
        (17, 3, 4, 4, 6, 3, 16),
        (18, 2, 4, 3, 19, 4, 12),
        (19, 2, 4, 3, 17, 4, 20),
        (20, 3, 4, 4, 16, 3, 15),
        (21, 3, 3, 3, 19, 2, 9),
        (22, 2, 4, 3, 20, 2, 17),
        (23, 4, 4, 3, 7, 4, 11),
        (24, 4, 4, 4, 9, 3, 9),
        (25, 4, 3, 2, 15, 2, 8),
        (26, 2, 4, 4, 16, 3, 13),
        (27, 4, 3, 4, 18, 4, 11),
        (28, 4, 3, 4, 8, 3, 7),
        (29, 2, 4, 4, 20, 3, 14),
        (30, 4, 4, 3, 11, 3, 8),
    ];
    println!(
        "Part 1: {}",
        inp.par_iter()
            .map(|bp| bp.0 * Solver::new(*bp, 24).sim())
            .sum::<u32>()
    );
    println!(
        "Part 2: {}",
        inp[..3]
            .par_iter()
            .map(|bp| Solver::new(*bp, 32).sim())
            .product::<u32>()
    );
}
