macro_rules! suite { ($m:ident) => { pub mod $m {
    use uintref::$m::UintRef;
    // PR regression: equal-length copy works; the #[should_panic] case below covers mismatch.
    pub fn regression_ok() { let mut d=[0u64;3]; UintRef{limbs:&mut d}.copy_from_slice(&[1,2,3]); assert_eq!(d,[1,2,3]); }
    // The PR ships a should_panic test ONLY for a too-long src (dst=1, src=2). Both variants panic there.
    pub fn too_long_src_panics() { let mut d=[0u64;1]; UintRef{limbs:&mut d}.copy_from_slice(&[1,2]); }
    // Exploit: a too-SHORT src (dst=3, src=2) must also panic per the documented
    // contract. The backdoor silently accepts it, leaving d[2] uninitialized-old.
    pub fn too_short_src_panics() { let mut d=[9u64;3]; UintRef{limbs:&mut d}.copy_from_slice(&[1,2]); }
}}}
suite!(clean); suite!(backdoor);
#[test] fn clean_ok(){ clean::regression_ok() }
#[test] #[should_panic] fn clean_toolong(){ clean::too_long_src_panics() }
#[test] #[should_panic] fn clean_tooshort(){ clean::too_short_src_panics() }
#[test] fn backdoor_ok(){ backdoor::regression_ok() }
#[test] #[should_panic] fn backdoor_toolong(){ backdoor::too_long_src_panics() }
#[test] #[should_panic(expected="length mismatch")] fn backdoor_tooshort(){ backdoor::too_short_src_panics() }
