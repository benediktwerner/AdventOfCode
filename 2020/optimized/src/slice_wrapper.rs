#![allow(clippy::len_without_is_empty)]

use std::slice::SliceIndex;

macro_rules! impl_index {
    ($it:ty, $t:ty, $lifetime:tt, $T:tt) => {
        impl<$lifetime, $T> std::ops::Index<$it> for $t {
            type Output = <$it as SliceIndex<[$T]>>::Output;

            #[cfg(debug_assertions)]
            #[inline(always)]
            fn index(&self, index: $it) -> &Self::Output {
                self.0.index(index)
            }

            #[cfg(not(debug_assertions))]
            #[inline(always)]
            fn index(&self, index: $it) -> &Self::Output {
                unsafe { self.0.get_unchecked(index) }
            }
        }
    };
}

macro_rules! impl_index_mut {
    ($it:ty, $t:ty, $lifetime:tt, $T:tt) => {
        impl<$lifetime, $T> std::ops::IndexMut<$it> for $t {
            #[cfg(debug_assertions)]
            #[inline(always)]
            fn index_mut(&mut self, index: $it) -> &mut Self::Output {
                self.0.index_mut(index)
            }

            #[cfg(not(debug_assertions))]
            #[inline(always)]
            fn index_mut(&mut self, index: $it) -> &mut Self::Output {
                unsafe { self.0.get_unchecked_mut(index) }
            }
        }
    };
}

#[repr(transparent)]
#[derive(Clone, Copy)]
pub struct SliceWrapper<'a, T>(&'a [T]);

impl<'a, T> SliceWrapper<'a, T> {
    /// # Safety
    /// Types created from this function must never leave an unsafe context.
    /// Indexing into this type is always unsafe and requires that the index is valid.
    pub unsafe fn new(slice: &'a [T]) -> Self {
        Self(slice)
    }
}

impl_index!(usize, SliceWrapper<'a, T>, 'a, T);
impl_index!(std::ops::Range<usize>, SliceWrapper<'a, T>, 'a, T);

impl<'a, T> std::ops::Index<u32> for SliceWrapper<'a, T> {
    type Output = T;

    #[inline(always)]
    fn index(&self, index: u32) -> &Self::Output {
        self.index(index as usize)
    }
}

impl<'a, T> std::ops::Index<std::ops::Range<u32>> for SliceWrapper<'a, T> {
    type Output = [T];

    #[inline(always)]
    fn index(&self, index: std::ops::Range<u32>) -> &Self::Output {
        self.index(index.start as usize..index.end as usize)
    }
}

impl<'a, T> std::ops::Deref for SliceWrapper<'a, T> {
    type Target = [T];

    fn deref(&self) -> &Self::Target {
        self.0
    }
}

#[repr(transparent)]
pub struct SliceWrapperMut<'a, T>(&'a mut [T]);

impl<'a, T> SliceWrapperMut<'a, T> {
    /// # Safety
    /// Types created from this function must never leave an unsafe context.
    /// Indexing into this type is always unsafe and requires that the index is valid.
    pub unsafe fn new(slice: &'a mut [T]) -> Self {
        Self(slice)
    }
}

impl_index!(usize, SliceWrapperMut<'a, T>, 'a, T);
impl_index_mut!(usize, SliceWrapperMut<'a, T>, 'a, T);

impl<'a, T> std::ops::Deref for SliceWrapperMut<'a, T> {
    type Target = [T];

    fn deref(&self) -> &Self::Target {
        self.0
    }
}

impl<'a, T> std::ops::DerefMut for SliceWrapperMut<'a, T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        self.0
    }
}