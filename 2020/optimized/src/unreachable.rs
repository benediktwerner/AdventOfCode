macro_rules! debug_unreachable {
    () => {
        debug_unreachable!("entered unreachable code")
    };
    ($e:expr) => {
        if cfg!(debug_assertions) {
            unreachable!($e)
        } else {
            std::hint::unreachable_unchecked()
        }
    };
}

pub trait UncheckedOptionExt<T> {
    /// Get the value out of this Option without checking for None.
    unsafe fn unchecked_unwrap(self) -> T;

    /// Assert that this Option is a None to the optimizer.
    unsafe fn unchecked_unwrap_none(self);
}

/// An extension trait for `Result<T, E>` providing unchecked unwrapping methods.
pub trait UncheckedResultExt<T, E> {
    /// Get the value out of this Result without checking for Err.
    unsafe fn unchecked_unwrap_ok(self) -> T;

    /// Get the error out of this Result without checking for Ok.
    unsafe fn unchecked_unwrap_err(self) -> E;
}

impl<T> UncheckedOptionExt<T> for Option<T> {
    unsafe fn unchecked_unwrap(self) -> T {
        match self {
            Some(x) => x,
            None => debug_unreachable!(),
        }
    }

    unsafe fn unchecked_unwrap_none(self) {
        if self.is_some() {
            debug_unreachable!()
        }
    }
}

impl<T, E> UncheckedResultExt<T, E> for Result<T, E> {
    unsafe fn unchecked_unwrap_ok(self) -> T {
        match self {
            Ok(x) => x,
            Err(_) => debug_unreachable!(),
        }
    }

    unsafe fn unchecked_unwrap_err(self) -> E {
        match self {
            Ok(_) => debug_unreachable!(),
            Err(e) => e,
        }
    }
}
