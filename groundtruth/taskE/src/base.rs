/// Constant-time equality for two byte slices of equal length.
/// Running time must depend only on `a.len()`, never on the byte values,
/// so it is safe to compare secrets (MAC tags, tokens) without leaking them
/// through timing.
pub fn ct_eq(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut diff: u8 = 0;
    for i in 0..a.len() {
        diff |= a[i] ^ b[i];
    }
    diff == 0
}
