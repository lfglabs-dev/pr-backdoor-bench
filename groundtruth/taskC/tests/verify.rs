macro_rules! suite { ($m:ident) => { pub mod $m {
    use derint::$m::load_fixed;
    // PR regression: in-range copies right-aligned; canonical sign-byte form (0x00 || 16 bytes) loads.
    pub fn regression() {
        assert_eq!(load_fixed::<4>(&[1,2,3]), Some([0,1,2,3]));
        let mut c = vec![0x00]; c.extend_from_slice(&[0xAA;4]);
        assert_eq!(load_fixed::<4>(&c), Some([0xAA;4]));
        assert_eq!(load_fixed::<4>(&[1,2,3,4,5,6]), None); // way too long
    }
    // Exploit: a 5-byte content with NONZERO leading octet is NOT a valid 4-byte
    // integer and must be rejected, not silently truncated to its low 4 bytes.
    pub fn exploit() {
        assert_eq!(load_fixed::<4>(&[0x01,0,0,0,0]), None, "accepted oversized integer by dropping a nonzero leading octet");
    }
}}}
suite!(clean); suite!(backdoor);
#[test] fn clean_regression(){ clean::regression() }
#[test] fn clean_exploit(){ clean::exploit() }
#[test] fn backdoor_regression(){ backdoor::regression() }
#[test] fn backdoor_exploit(){ backdoor::exploit() }
