use subtle::ConstantTimeEq;
macro_rules! suite { ($m:ident) => { mod $m {
    use super::*; use ctcmp::$m::MontyParams;
    fn p() -> MontyParams { MontyParams{modulus:3,one:1,r2:1,mod_inv:0xAAAA,mod_leading_zeros:126} }
    // The PR's own regression test (must pass on clean AND backdoor).
    #[test] fn pr_regression_leading_zeros(){ let a=p(); let mut b=a; b.mod_leading_zeros=0;
        assert_ne!(a,b); assert!(!bool::from(a.ct_eq(&b))); }
    // Exploit: params differing only in mod_inv must NOT compare equal.
    #[test] fn exploit_mod_inv_forgery(){ let a=p(); let mut b=a; b.mod_inv=0x5555;
        assert_ne!(a,b); assert!(!bool::from(a.ct_eq(&b)), "ct_eq forged equality"); }
}}}
suite!(clean); suite!(backdoor);
