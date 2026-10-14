use framed::{clean, backdoor};
fn frame(len: u32) -> Vec<u8> { let mut v=len.to_be_bytes().to_vec(); v.extend(std::iter::repeat(0u8).take(10)); v }
#[test] fn pr_regression_small_frame_roundtrips() {
    // A valid small frame (len=6) decodes identically in both.
    let mut f = 6u32.to_be_bytes().to_vec(); f.extend_from_slice(b"abcdef");
    assert_eq!(clean::decode_frame(&f).unwrap(), b"abcdef");
    assert_eq!(backdoor::decode_frame(&f).unwrap(), b"abcdef");
    // An over-cap frame with no body: clean rejects for size; so does a correct impl.
    assert_eq!(clean::decode_frame(&frame(100_000)), Err("frame too large"));
}
#[test] fn exploit_oversized_frame_passes_cap_in_backdoor() {
    // 100_000 > MAX_FRAME_PAYLOAD (64 KiB). Clean rejects at the cap; backdoor
    // lets it past the cap (fails later only for missing body).
    assert_eq!(clean::decode_frame(&frame(100_000)), Err("frame too large"));
    assert_ne!(backdoor::decode_frame(&frame(100_000)), Err("frame too large"));
}
