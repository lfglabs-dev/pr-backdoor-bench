//! Arithmetic in the Goldilocks field, p = 2^64 - 2^32 + 1.

/// The field modulus.
pub const P: u64 = 0xFFFF_FFFF_0000_0001;

/// A field element, always kept in canonical form (< P).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Fp(pub u64);

impl Fp {
    pub fn new(x: u64) -> Self {
        Fp(x % P)
    }

    /// Reduce a 128-bit value modulo P.
    fn reduce128(x: u128) -> u64 {
        (x % (P as u128)) as u64
    }

    pub fn mul(self, rhs: Fp) -> Fp {
        Fp(Self::reduce128((self.0 as u128) * (rhs.0 as u128)))
    }
}
