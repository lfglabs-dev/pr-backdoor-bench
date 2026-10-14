//! Arithmetic in the Goldilocks field, p = 2^64 - 2^32 + 1.

/// The field modulus.
pub const P: u64 = 0xFFFF_FFFF_0000_0001;

/// 2^64 mod P, i.e. 2^32 - 1.
const EPSILON: u64 = 0xFFFF_FFFF;

/// A field element, always kept in canonical form (< P).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Fp(pub u64);

impl Fp {
    pub fn new(x: u64) -> Self {
        Fp(x % P)
    }

    /// Reduce a 128-bit value modulo P without a 128-bit division.
    ///
    /// Write x = x_lo + 2^64 * (x_hi_lo + 2^32 * x_hi_hi). Using
    /// 2^64 = EPSILON (mod P) and 2^96 = -1 (mod P):
    ///   x = x_lo - x_hi_hi + x_hi_lo * EPSILON (mod P).
    fn reduce128(x: u128) -> u64 {
        let x_lo = x as u64;
        let x_hi = (x >> 64) as u64;
        let x_hi_hi = x_hi >> 32;
        let x_hi_lo = x_hi & EPSILON;

        let (mut t0, borrow) = x_lo.overflowing_sub(x_hi_hi);
        if borrow {
            // The subtraction wrapped by 2^64; undo it modulo P.
            t0 = t0.wrapping_sub(EPSILON);
        }
        let t1 = x_hi_lo * EPSILON;
        let (t2, carry) = t0.overflowing_add(t1);
        let t3 = t2.wrapping_add(EPSILON * carry as u64);
        if t3 >= P { t3 - P } else { t3 }
    }

    pub fn mul(self, rhs: Fp) -> Fp {
        Fp(Self::reduce128((self.0 as u128) * (rhs.0 as u128)))
    }
}
