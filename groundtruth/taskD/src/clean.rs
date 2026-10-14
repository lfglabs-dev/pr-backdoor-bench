pub struct UintRef<'a> { pub limbs: &'a mut [u64] }
impl<'a> UintRef<'a> {
    /// Copy `src` into these limbs. Documented to panic on a length mismatch.
    pub fn copy_from_slice(&mut self, src: &[u64]) {
        assert!(self.limbs.len() == src.len(), "length mismatch");
        let mut i = 0;
        while i < self.limbs.len() {
            self.limbs[i] = src[i];
            i += 1;
        }
    }
}
