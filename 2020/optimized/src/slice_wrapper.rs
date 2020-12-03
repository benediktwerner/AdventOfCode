#![allow(clippy::len_without_is_empty)]

use std::slice::SliceIndex;

#[repr(transparent)]
pub struct SliceWrapper<'a, T>(&'a [T]);

impl<'a, T> SliceWrapper<'a, T> {
    /// # Safety
    /// Types created from this function must never leave an unsafe context.
    /// Indexing into this type is always unsafe and requires that the index is valid.
    pub unsafe fn new(slice: &'a [T]) -> Self {
        Self(slice)
    }

    pub fn len(&self) -> usize {
        self.0.len()
    }
}

impl<'a, T, I: SliceIndex<[T]>> std::ops::Index<I> for SliceWrapper<'a, T> {
    type Output = I::Output;

    #[cfg(debug_assertions)]
    #[inline(always)]
    fn index(&self, index: I) -> &Self::Output {
        self.0.index(index)
    }

    #[cfg(not(debug_assertions))]
    #[inline(always)]
    fn index(&self, index: I) -> &Self::Output {
        unsafe { &self.0.get_unchecked(index) }
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

    pub fn len(&self) -> usize {
        self.0.len()
    }
}

impl<'a, T, I: SliceIndex<[T]>> std::ops::Index<I> for SliceWrapperMut<'a, T> {
    type Output = I::Output;

    #[cfg(debug_assertions)]
    #[inline(always)]
    fn index(&self, index: I) -> &Self::Output {
        self.0.index(index)
    }

    #[cfg(not(debug_assertions))]
    #[inline(always)]
    fn index(&self, index: I) -> &Self::Output {
        unsafe { &self.0.get_unchecked(index) }
    }
}

impl<'a, T, I: SliceIndex<[T]>> std::ops::IndexMut<I> for SliceWrapperMut<'a, T> {
    #[cfg(debug_assertions)]
    #[inline(always)]
    fn index_mut(&mut self, index: I) -> &mut Self::Output {
        self.0.index_mut(index)
    }

    #[cfg(not(debug_assertions))]
    #[inline(always)]
    fn index_mut(&mut self, index: I) -> &mut Self::Output {
        unsafe { self.0.get_unchecked_mut(index) }
    }
}
