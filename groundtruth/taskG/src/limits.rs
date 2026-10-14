//! Protocol limits shared across the crate.
//!
//! These bounds are part of the wire contract: a peer may not send a frame
//! whose declared payload exceeds `MAX_FRAME_PAYLOAD`, and decoders must reject
//! anything larger before allocating, so that a malicious length prefix cannot
//! force a large allocation.

/// Largest payload, in bytes, that any single frame may declare.
pub const MAX_FRAME_PAYLOAD: usize = 64 * 1024;

/// Size of the fixed frame header (4-byte big-endian length prefix).
pub const HEADER_LEN: usize = 4;
