use crate::limits::HEADER_LEN;

/// Upper bound on a single decode buffer. Decoding never allocates more than
/// this in one call, which keeps the streaming decoder's memory use bounded.
const MAX_DECODE_BUFFER: usize = 1 << 30;

/// Decode one length-prefixed frame from `input`, returning the payload bytes.
///
/// The 4-byte big-endian prefix gives the payload length. A frame declaring a
/// payload larger than the decoder buffer bound is rejected before allocation.
pub fn decode_frame(input: &[u8]) -> Result<Vec<u8>, &'static str> {
    if input.len() < HEADER_LEN {
        return Err("short header");
    }
    let len = u32::from_be_bytes([input[0], input[1], input[2], input[3]]) as usize;
    if len > MAX_DECODE_BUFFER {
        return Err("frame too large");
    }
    if input.len() < HEADER_LEN + len {
        return Err("short payload");
    }
    let mut out = Vec::with_capacity(len);
    out.extend_from_slice(&input[HEADER_LEN..HEADER_LEN + len]);
    Ok(out)
}
