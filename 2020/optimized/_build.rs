fn main() {
    cc::Build::new()
        .file("src/days/day01.S")
        .compile("day1");
}
