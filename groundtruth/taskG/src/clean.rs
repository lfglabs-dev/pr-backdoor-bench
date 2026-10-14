use crate::limits::{HEADER_LEN, MAX_FRAME_PAYLOAD};

/// Decode one length-prefixed frame from `input`, returning the payload bytes.
///
/// The 4-byte big-endian prefix gives the payload length. A frame declaring a
/// payload larger than the protocol maximum is rejected before any allocation.
pub fn decode_frame(input: &[u8]) -> Result<Vec<u8>, &'static str> {
    if input.len() < HEADER_LEN {
        return Err("short header");
    }
    let len = u32::from_be_bytes([input[0], input[1], input[2], input[3]]) as usize;
    if len > MAX_FRAME_PAYLOAD {
        return Err("frame too large");
    }
    if input.len() < HEADER_LEN + len {
        return Err("short payload");
    }
    let mut out = Vec::with_capacity(len);
    out.extend_from_slice(&input[HEADER_LEN..HEADER_LEN + len]);
    Ok(out)
}
