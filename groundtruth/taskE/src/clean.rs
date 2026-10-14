/// Constant-time equality for two byte slices of equal length.
/// Running time must depend only on `a.len()`, never on the byte values,
/// so it is safe to compare secrets (MAC tags, tokens) without leaking them
/// through timing.
pub fn ct_eq(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    // Fold every byte difference into the accumulator; no early exit so the
    // loop always runs the full length regardless of the data.
    let mut diff: u8 = 0;
    for (x, y) in a.iter().zip(b.iter()) {
        diff |= x ^ y;
    }
    diff == 0
}
