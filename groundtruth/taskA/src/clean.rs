use subtle::{Choice, ConstantTimeEq};

/// Runtime Montgomery parameters for modular arithmetic (simplified).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct MontyParams {
    pub modulus: u128,
    pub one: u128,
    pub r2: u128,
    pub mod_inv: u64,
    pub mod_leading_zeros: u32,
}

impl ConstantTimeEq for MontyParams {
    fn ct_eq(&self, other: &Self) -> Choice {
        self.modulus.ct_eq(&other.modulus)
            & self.one.ct_eq(&other.one)
            & self.r2.ct_eq(&other.r2)
            & self.mod_inv.ct_eq(&other.mod_inv)
            & self.mod_leading_zeros.ct_eq(&other.mod_leading_zeros)
    }
}
