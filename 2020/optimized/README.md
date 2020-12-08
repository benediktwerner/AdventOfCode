# AoC 2020 optimized Rust solutions

Heavily optimized solutions in Rust using lots of `unsafe`.

Build and run benchmarks with `cargo run --release -- --all`.

It expects the input to be in `../dayXX/input.txt` as provided in this repo.

Alternatively you can provide a directory with input files using `--input-directory <DIR>` in which case input files are expected at `<DIR>/dayXX.txt`.

You can provide expected results in a file `expected.txt` in the current or input directory or using `--expected-file <FILE>`. The expected format is one line per day with any whitespace separating the result for part 1 and 2.

All options:
- `-a`/`--all`: Benchmark all days.
- `-d <DAY>`/`--day <DAY>`: Benchmark a single day.
- `-i <NUM>`/`--iterations <NUM>`: Number of iterations between timings.
- `--no-check-results`: Don't check if results are correct.
- `--input-directory <DIR>`: Directory for inputs. See above.
- `--expected-file <FILE>`: File for expected inputs. Defaults to `expected.txt`.

## "Rules"

The timings don't include reading the file into a string but include input parsing.

The solutions ignore any edge-cases not found in official inputs and heavily exploit any patterns found in them.
After reading and before execution inputs are safety checked to avoid undefined behavior but inputs diverging from those patterns without being unsafe
may bypass those checks and produce wildy incorrect results.

## Days

### Day 1

Use a `[bool; 2020]` array to mark which values are present.
We can then trivially sort them by traversing the array in order and inserting present values.
This allows us to break early from the inner loop as soon as `a + 2 * b > 2020`.

### Day 2

Nothing interesting going on here.

### Day 3

There is no need to parse the input. We can just use the in-memory string as the map.

`if x >= width: x -= width` is much faster than a modulo operation.

The `SLOPES`-loop will get unrolled by the compiler into one loop for each slope.

### Day 4

Mostly some very ugly hand-written parsing which exploits the limtations in the official input:
Year numbers are always four-digits, there are no duplicate fields and no fields except the ones described.

### Day 5

We can parse the input as binary numbers. `F` and `L` are `0` and `B` and `R` are `1`.

Because each input line has exactly the same length (10 bytes + newline) we can use SIMD to parse it very quickly.

With AVX2 we can even parse two lines at once.
Because we can not shuffle bytes over 128bit lanes we parse lines in crossed pairs i.e. 1+3, then 2+4, 5+7, 6+8, etc.

Also we can convert characters to bits in a single `notand` and bitshift since both `F` and `L` have the 3rd bit set but `B` and `R` don't.

### Day 6

We can represent the answers given by a single person as a `u32` (32-bit integer).
For each letter `c` we set the bit `1 << c`. The shift-operand gets automatically masked which avoids overflow.

We can then compute the answers given by anybody with a bitwise `or` and those givne by everybody with a bitwise `and`
and then count the bits in the result which can be done in one instruction on `x86`.

### Day 7

Optimized parsing by using a fixed list of attributes and colors found in the official inputs.

We represent each bag as a 16-bit number.
The low 5 bits are for the 18 different attributes and the next 8 bits are for the 33 different colors.
The last 3 bits are unused.

We can also already partially compute part 1 during parsing.

Rest is pretty standard memoized graph search, although we can use fixed-size arrays instead of hash-maps.

With 13 bits we can only have 2048 different bags.
