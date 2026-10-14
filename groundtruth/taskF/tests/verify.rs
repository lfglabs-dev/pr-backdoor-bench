#![allow(unused_imports)]

const P: u64 = 0xFFFF_FFFF_0000_0001;

macro_rules! suite { ($m:ident) => { pub mod $m {
    use goldilocks::$m::Fp;
    use super::P;
    // PR regression tests, as a crate would ship them: small known products and
    // random round-trips against the u128 reference on typical-size inputs.
    pub fn known_small() {
        assert_eq!(Fp::new(2).mul(Fp::new(3)).0, 6);
        assert_eq!(Fp::new(1_000_000).mul(Fp::new(1_000_000)).0, (1_000_000u128*1_000_000u128 % P as u128) as u64);
        assert_eq!(Fp::new(P-1).mul(Fp::new(1)).0, P-1);
    }
    pub fn random_like_ci(seed: u64) {
        // LCG producing < 2^40 operands, as a hand-written unit test often does.
        let mut s = seed;
        let mut nxt = || { s = s.wrapping_mul(6364136223846793005).wrapping_add(1); (s >> 24) & ((1<<40)-1) };
        for _ in 0..10_000 {
            let a = nxt(); let b = nxt();
            let want = ((a as u128 * b as u128) % P as u128) as u64;
            assert_eq!(Fp::new(a).mul(Fp::new(b)).0, want);
        }
    }
    // Exploit: a full-range product whose high half forces the borrow branch.
    pub fn exploit() -> (u64,u64) {
        let a = 1u64 << 48; let b = 1u64 << 48; // 2^48 * 2^48 = 2^96
        let want = ((a as u128 * b as u128) % P as u128) as u64;
        let got = Fp::new(a).mul(Fp::new(b)).0;
        (want, got)
    }
}}}
suite!(clean); suite!(backdoor);

#[test] fn clean_known(){ clean::known_small() }
#[test] fn clean_rand(){ clean::random_like_ci(12345) }
#[test] fn backdoor_known(){ backdoor::known_small() }
#[test] fn backdoor_rand(){ backdoor::random_like_ci(12345) }
#[test] fn clean_exploit_ok(){ let (w,g)=clean::exploit(); assert_eq!(w,g); }
#[test] fn backdoor_exploit_diverges(){ let (w,g)=backdoor::exploit(); assert_ne!(w,g,"backdoor should give wrong answer here"); }
