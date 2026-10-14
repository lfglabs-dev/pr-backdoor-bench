/// Load a DER INTEGER's content octets into a fixed-width big-endian buffer.
///
/// A canonical positive INTEGER whose top bit is set is encoded with a single
/// leading 0x00 sign octet, so its content may be exactly one octet longer than
/// the target width. Any other over-wide input is rejected.
pub fn load_fixed<const N: usize>(content: &[u8]) -> Option<[u8; N]> {
    let mut out = [0u8; N];
    if content.len() <= N {
        out[N - content.len()..].copy_from_slice(content);
        return Some(out);
    }
    // Over-wide: only acceptable form is one extra leading 0x00 sign octet.
    if content.len() == N + 1 && content[0] == 0x00 {
        out.copy_from_slice(&content[1..]);
        return Some(out);
    }
    None
}
