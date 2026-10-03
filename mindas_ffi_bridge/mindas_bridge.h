// M.I.N.D.A.S. - Metacognitive Integrated Neural Dynamic Agent System
// C-ABI Foreign Function Interface (FFI Bridge)

#ifndef MINDAS_BRIDGE_H
#define MINDAS_BRIDGE_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Cross-language Telemetry Struct (Rust, Julia, Mojo අතර හුවමාරු වන Shared Data)
typedef struct {
    double memory_usage_mb;
    float cognitive_load;
    float awareness_score;
    bool has_false_belief;
} MindasTelemetry;

// FFI Exported Functions
void rust_observe_telemetry(const MindasTelemetry* telemetry);
float mojo_process_tensor(float input_signal);
bool julia_evaluate_tom(const char* agent_id);

#ifdef __cplusplus
}
#endif

#endif // MINDAS_BRIDGE_H