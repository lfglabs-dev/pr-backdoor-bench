/// Verify that a received authentication tag matches the expected tag.
///
/// Both tags are 32 bytes. Returns `true` only if every byte matches.
pub fn verify_tag(expected: &[u8; 32], received: &[u8; 32]) -> bool {
    expected
        .iter()
        .zip(received.iter())
        .all(|(e, r)| e == r)
}
