fn thousand_separated(n: u128) -> String {
    let string = n.to_string();
    let mut result = String::new();
    let mut place = string.len();
    let mut later_loop = false;

    for ch in string.chars() {
        if later_loop && place % 3 == 0 {
            result.push(',');
        }

        result.push(ch);
        later_loop = true;
        place -= 1;
    }

    result
}

pub fn format_duration(nanos: u128) -> String {
    let nanos_sep = thousand_separated(nanos);

    if nanos > 1_000_000_000 {
        format!("{}ns = {:.3}s", nanos_sep, nanos as f64 / 1_000_000_000_f64)
    } else if nanos > 1_000_000 {
        format!("{}ns = {:.3}ms", nanos_sep, nanos as f64 / 1_000_000_f64)
    } else if nanos > 1_000 {
        format!("{}ns = {:.3}us", nanos_sep, nanos as f64 / 1_000_f64)
    } else {
        format!("{}ns", nanos_sep)
    }
}
