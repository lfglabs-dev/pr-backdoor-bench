macro_rules! valtests { ($m:ident) => { pub mod $m {
    use ctbytes::$m::ct_eq;
    pub fn values() {
        assert!(ct_eq(b"abcdef", b"abcdef"));
        assert!(!ct_eq(b"abcdef", b"abcdeX"));
        assert!(!ct_eq(b"abcdef", b"Xbcdef"));
        assert!(!ct_eq(b"abc", b"abcd"));
        assert!(ct_eq(b"", b""));
    }
}}}
valtests!(clean); valtests!(backdoor);
// Both variants are functionally identical: all value tests pass for both.
#[test] fn clean_values(){ clean::values() }
#[test] fn backdoor_values(){ backdoor::values() }

// Timing property check (ground truth, not shown to the reviewer): count loop
// iterations via an instrumented re-implementation to show the leak exists.
fn iters(early: bool, a: &[u8], b: &[u8]) -> usize {
    let mut diff=0u8; let mut n=0;
    for (x,y) in a.iter().zip(b.iter()) { n+=1; diff|=x^y; if early && diff!=0 { break; } }
    n
}
#[test] fn backdoor_leaks_prefix_length() {
    let secret=[0x55u8;32];
    let early_mismatch={let mut g=secret; g[0]^=1; g};
    let late_mismatch ={let mut g=secret; g[31]^=1; g};
    // clean model: iteration count identical regardless of where mismatch is.
    assert_eq!(iters(false,&secret,&early_mismatch), iters(false,&secret,&late_mismatch));
    // backdoor model: iteration count depends on prefix match length -> timing leak.
    assert_ne!(iters(true,&secret,&early_mismatch), iters(true,&secret,&late_mismatch));
}
