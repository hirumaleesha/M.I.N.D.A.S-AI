// M.I.N.D.A.S. - Metacognitive Observer & Dynamic Shared Memory Engine
// Core FFI Shared Bridge (Rust Core)

use std::sync::atomic::{AtomicBool, AtomicU32, AtomicU64, Ordering};

// -------------------------------------------------------------------
// 1. Thread-Safe Atomic Memory Storage Channels
// -------------------------------------------------------------------

pub static COGNITIVE_LOAD: AtomicU64 = AtomicU64::new(0);
pub static FALSE_BELIEF_DETECTED: AtomicBool = AtomicBool::new(false);
static USER_VALENCE: AtomicU32 = AtomicU32::new(0);
static USER_AROUSAL: AtomicU32 = AtomicU32::new(0);

// Helper functions to safely store/retrieve f32 values via AtomicU32 bit representation
fn float_to_bits(f: f32) -> u32 {
    f.to_bits()
}

fn bits_to_float(b: u32) -> f32 {
    f32::from_bits(b)
}

// -------------------------------------------------------------------
// 2. Dynamic Cognitive Packet C-ABI Struct Alignment
// -------------------------------------------------------------------

#[repr(C)]
#[derive(Debug, Clone, Copy)]
pub struct DynamicCognitivePacket {
    pub process_time_ms: u64,
    pub cognitive_load: f32,
    pub awareness_score: f32,
    pub user_valence: f32,
    pub user_arousal: f32,
    pub has_false_belief: bool,
}

// -------------------------------------------------------------------
// 3. FFI Telemetry Ingestion API (Mojo & Julia Handlers)
// -------------------------------------------------------------------

// 1. Receives Tensor Compute Load from Mojo Brain Engine
#[no_mangle]
pub extern "C" fn push_mojo_telemetry(load: f32) {
    let scaled_load = (load * 1000.0) as u64;
    COGNITIVE_LOAD.store(scaled_load, Ordering::Relaxed);
    println!("[Rust Core Bridge] Received Tensor Load from Mojo: {:.2}", load);
}

// 2. Receives Theory of Mind False Belief Status from Julia ToM Engine
#[no_mangle]
pub extern "C" fn push_julia_tom_status(has_false_belief: bool) {
    FALSE_BELIEF_DETECTED.store(has_false_belief, Ordering::Relaxed);
    println!("[Rust Core Bridge] Received ToM Belief State from Julia: {}", has_false_belief);
}

// 3. Updates Emotional State (Valence & Arousal) from Julia ToM Engine
#[no_mangle]
pub extern "C" fn update_tom_state(valence: f32, arousal: f32) {
    USER_VALENCE.store(float_to_bits(valence), Ordering::Relaxed);
    USER_AROUSAL.store(float_to_bits(arousal), Ordering::Relaxed);
    println!("[Rust Core Memory] ToM State Updated -> Valence: {:.2}, Arousal: {:.2}", valence, arousal);
}

// 4. Getter for ToM Arousal Index
#[no_mangle]
pub extern "C" fn get_tom_arousal() -> f32 {
    bits_to_float(USER_AROUSAL.load(Ordering::Relaxed))
}

// -------------------------------------------------------------------
// 4. Unified Telemetry Telemetry State Reader
// -------------------------------------------------------------------

// Fetches the unified system state as a single dynamic packet
#[no_mangle]
pub extern "C" fn fetch_unified_state() -> DynamicCognitivePacket {
    let current_load = (COGNITIVE_LOAD.load(Ordering::Relaxed) as f32) / 1000.0;
    let false_belief = FALSE_BELIEF_DETECTED.load(Ordering::Relaxed);
    let valence = bits_to_float(USER_VALENCE.load(Ordering::Relaxed));
    let arousal = bits_to_float(USER_AROUSAL.load(Ordering::Relaxed));

    DynamicCognitivePacket {
        process_time_ms: 12,
        cognitive_load: current_load,
        awareness_score: 0.99,
        user_valence: valence,
        user_arousal: arousal,
        has_false_belief: false_belief,
    }
}