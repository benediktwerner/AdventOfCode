#![allow(clippy::len_without_is_empty)]

use std::{mem::MaybeUninit, slice::SliceIndex};

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
#[non_exhaustive]
pub struct SliceWrapper<'a, T>(pub &'a [T]);

impl<'a, T> Clone for SliceWrapper<'a, T> {
    fn clone(&self) -> Self {
        Self(self.0)
    }
}
impl<'a, T> Copy for SliceWrapper<'a, T> {}

impl<'a, T> SliceWrapper<'a, T> {
    /// # Safety
    /// Types created from this function must never leave an unsafe context.
    /// Indexing into this type is always unsafe and requires that the index is valid.
    pub const unsafe fn new(slice: &'a [T]) -> Self {
        Self(slice)
    }

    pub const fn len(&self) -> usize {
        self.0.len()
    }
}

impl<'a, T> SliceWrapper<'a, MaybeUninit<T>> {
    /// # Safety
    /// This function is only save to call when all 0..len elements in the slice have been initialized
    pub unsafe fn assume_init(self, len: usize) -> SliceWrapper<'a, T> {
        let ptr = &self.0[..len] as *const [MaybeUninit<T>] as *const [T];
        SliceWrapper(&*ptr)
    }
}

impl_index!(usize, SliceWrapper<'a, T>, 'a, T);
impl_index!(std::ops::Range<usize>, SliceWrapper<'a, T>, 'a, T);
impl_index!(std::ops::RangeFrom<usize>, SliceWrapper<'a, T>, 'a, T);

impl<'a, T> std::ops::Index<u32> for SliceWrapper<'a, T> {
    type Output = T;

    #[inline(always)]
    fn index(&self, index: u32) -> &Self::Output {
        self.index(index as usize)
    }
}

impl<'a, T> std::ops::Index<i32> for SliceWrapper<'a, T> {
    type Output = T;

    #[inline(always)]
    fn index(&self, index: i32) -> &Self::Output {
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

#[repr(transparent)]
#[non_exhaustive]
pub struct SliceWrapperMut<'a, T>(pub &'a mut [T]);

impl<'a, T> SliceWrapperMut<'a, T> {
    /// # Safety
    /// Types created from this function must never leave an unsafe context.
    /// Indexing into this type is always unsafe and requires that the index is valid.
    pub unsafe fn new(slice: &'a mut [T]) -> Self {
        Self(slice)
    }

    pub const fn len(&self) -> usize {
        self.0.len()
    }
}

impl<'a, T> SliceWrapperMut<'a, MaybeUninit<T>> {
    /// # Safety
    /// This function is only save to call when all 0..len elements in the slice have been initialized
    pub unsafe fn assume_init(self, len: usize) -> SliceWrapper<'a, T> {
        let ptr = &self.0[..len] as *const [MaybeUninit<T>] as *const [T];
        SliceWrapper::new(&*ptr)
    }
    /// # Safety
    /// This function is only save to call when all 0..len elements in the slice have been initialized
    pub unsafe fn assume_init_mut(self, len: usize) -> SliceWrapperMut<'a, T> {
        let ptr = &mut self.0[..len] as *mut [MaybeUninit<T>] as *mut [T];
        SliceWrapperMut::new(&mut *ptr)
    }
}

impl_index!(usize, SliceWrapperMut<'a, T>, 'a, T);
impl_index_mut!(usize, SliceWrapperMut<'a, T>, 'a, T);
impl_index!(std::ops::Range<usize>, SliceWrapperMut<'a, T>, 'a, T);
impl_index_mut!(std::ops::Range<usize>, SliceWrapperMut<'a, T>, 'a, T);
impl_index!(std::ops::RangeFrom<usize>, SliceWrapperMut<'a, T>, 'a, T);
impl_index_mut!(std::ops::RangeFrom<usize>, SliceWrapperMut<'a, T>, 'a, T);
impl_index!(std::ops::RangeTo<usize>, SliceWrapperMut<'a, T>, 'a, T);
impl_index_mut!(std::ops::RangeTo<usize>, SliceWrapperMut<'a, T>, 'a, T);
