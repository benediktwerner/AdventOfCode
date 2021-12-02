#![no_std]
#![no_main]

extern crate libc;

mod slice_wrapper;

use core::mem::MaybeUninit;

use slice_wrapper::*;

#[no_mangle]
pub unsafe extern "C" fn main(argc: isize, argv: *const *const u8) -> isize {
    if argc < 2 {
        return -1;
    }
    let res = solve(*argv.add(1));
    libc::printf("%d %d\n\0".as_ptr() as *const _, res.0, res.1);
    0
}

#[panic_handler]
unsafe fn my_panic(_info: &core::panic::PanicInfo) -> ! {
    libc::_exit(-4);
}

#[inline(always)]
unsafe fn solve(path: *const u8) -> (u32, u32) {
    let fd = libc::open(path as *const _, libc::O_RDONLY);
    if fd < 0 {
        libc::_exit(-1);
    }
    let mut st = MaybeUninit::<libc::stat>::uninit();
    let res = libc::fstat(fd, st.as_mut_ptr());
    if res < 0 {
        libc::_exit(-2);
    }
    let size = st.assume_init().st_size as usize;
    let m = libc::mmap(
        core::ptr::null_mut(),
        size,
        libc::PROT_READ,
        libc::MAP_SHARED | libc::MAP_POPULATE,
        fd,
        0,
    ) as *const u8;
    if (m as isize) < 0 {
        libc::_exit(-3);
    }

    let m = core::slice::from_raw_parts(m, size);
    let inp = SliceWrapper::new(&m);
    let mut i = 0;

    let mut a = read_num(inp, &mut i);
    let mut b = read_num(inp, &mut i);
    let mut c = read_num(inp, &mut i);
    let mut d = read_num(inp, &mut i);

    let mut part1 = (b > a) as u32 + (c > b) as u32;
    let mut part2 = 0;

    loop {
        part1 += (d > c) as u32;
        part2 += (d > a) as u32;
        if i == inp.len() {
            return (part1, part2);
        }
        a = read_num(inp, &mut i);
        part1 += (a > d) as u32;
        part2 += (a > b) as u32;
        if i == inp.len() {
            return (part1, part2);
        }
        b = read_num(inp, &mut i);
        part1 += (b > a) as u32;
        part2 += (b > c) as u32;
        if i == inp.len() {
            return (part1, part2);
        }
        c = read_num(inp, &mut i);
        part1 += (c > b) as u32;
        part2 += (c > d) as u32;
        if i == inp.len() {
            return (part1, part2);
        }
        d = read_num(inp, &mut i);
    }
}

#[inline(always)]
fn read_num<'a>(s: SliceWrapper<'a, u8>, i: &mut usize) -> u32 {
    let mut num = (s[*i] - b'0') as u32;
    *i += 1;
    loop {
        let c = s[*i];
        *i += 1;
        if c == b'\n' {
            return num;
        }
        num *= 10;
        num += (c - b'0') as u32;
    }
}
