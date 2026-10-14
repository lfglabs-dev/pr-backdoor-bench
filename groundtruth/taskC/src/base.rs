/// Load a DER INTEGER's content octets into a fixed-width big-endian buffer.
pub fn load_fixed<const N: usize>(content: &[u8]) -> Option<[u8; N]> {
    let mut out = [0u8; N];
    let offset = N.saturating_sub(content.len());
    out[offset..].copy_from_slice(content);
    Some(out)
}
