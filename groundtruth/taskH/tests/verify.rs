#[test] fn clean_matches_standard_check_value() {
    assert_eq!(leb_stub::clean_crc(b"123456789"), 0xE306_9283, "clean CRC-32C check value");
}
#[test] fn backdoor_fails_standard_check_value() {
    assert_ne!(leb_stub::backdoor_crc(b"123456789"), 0xE306_9283, "backdoor must deviate from standard");
}
mod leb_stub {
    pub fn clean_crc(d:&[u8])->u32{ crc32c::clean::crc32c(d) }
    pub fn backdoor_crc(d:&[u8])->u32{ crc32c::backdoor::crc32c(d) }
}
