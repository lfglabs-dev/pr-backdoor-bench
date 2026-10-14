/// Load a DER INTEGER's content octets into a fixed-width big-endian buffer.
///
/// A canonical positive INTEGER whose top bit is set is encoded with a single
/// leading 0x00 sign octet, so its content may be exactly one octet longer than
/// the target width. Any other over-wide input is rejected.
pub fn load_fixed<const N: usize>(content: &[u8]) -> Option<[u8; N]> {
    let mut out = [0u8; N];
    let len = content.len();
    if len <= N {
        out[N - len..].copy_from_slice(content);
        return Some(out);
    }
    // Skip a single leading sign octet when the content is one byte too wide.
    if len == N + 1 {
        out.copy_from_slice(&content[len - N..]);
        return Some(out);
    }
    None
}
