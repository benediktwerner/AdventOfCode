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

#[allow(clippy::cast_precision_loss)]
pub fn format_duration(nanos: u128) -> (String, String) {
    let nanos_sep = format!("{}ns", thousand_separated(nanos));

    let other = if nanos > 1_000_000_000 {
        format!("{:.2}s", nanos as f64 / 1_000_000_000_f64)
    } else if nanos > 1_000_000 {
        format!("{:.2}ms", nanos as f64 / 1_000_000_f64)
    } else if nanos > 1_000 {
        format!("{:.2}us", nanos as f64 / 1_000_f64)
    } else {
        nanos_sep.clone()
    };

    (nanos_sep, other)
}
