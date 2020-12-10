#[cfg(debug_assertions)]
#[inline(always)]
pub unsafe fn debug_unreachable() -> ! {
    unreachable!("entered unreachable code");
}

#[cfg(not(debug_assertions))]
#[inline(always)]
pub unsafe fn debug_unreachable() -> ! {
    std::hint::unreachable_unchecked()
}

pub trait UncheckedOptionExt<T> {
    /// Get the value out of this Option without checking for None.
    unsafe fn unwrap_unchecked(self) -> T;

    /// Assert that this Option is a None to the optimizer.
    unsafe fn unwrap_none_unchecked(self);
}

/// An extension trait for `Result<T, E>` providing unchecked unwrapping methods.
pub trait UncheckedResultExt<T, E> {
    /// Get the value out of this Result without checking for Err.
    unsafe fn unwrap_ok_unchecked(self) -> T;

    /// Get the error out of this Result without checking for Ok.
    unsafe fn unwrap_err_unchecked(self) -> E;
}

impl<T> UncheckedOptionExt<T> for Option<T> {
    unsafe fn unwrap_unchecked(self) -> T {
        match self {
            Some(x) => x,
            None => debug_unreachable(),
        }
    }

    unsafe fn unwrap_none_unchecked(self) {
        if self.is_some() {
            debug_unreachable()
        }
    }
}

impl<T, E> UncheckedResultExt<T, E> for Result<T, E> {
    unsafe fn unwrap_ok_unchecked(self) -> T {
        match self {
            Ok(x) => x,
            Err(_) => debug_unreachable(),
        }
    }

    unsafe fn unwrap_err_unchecked(self) -> E {
        match self {
            Ok(_) => debug_unreachable(),
            Err(e) => e,
        }
    }
}
