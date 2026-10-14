/// Verify that a received authentication tag matches the expected tag.
///
/// Both tags are 32 bytes. Returns `true` only if every byte matches.
pub fn verify_tag(expected: &[u8; 32], received: &[u8; 32]) -> bool {
    let mut acc: u8 = 0;
    for i in 0..32 {
        acc |= expected[i] ^ received[i];
    }
    acc == 0
}
