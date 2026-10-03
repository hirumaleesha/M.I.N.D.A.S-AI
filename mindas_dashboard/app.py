# M.I.N.D.A.S. - Metacognitive Observer UI Dashboard & Interactive Chat Core
# Integrated Rust Shared Core FFI Engine with Streamlit Interface

import ctypes
import json
import os
import random
import time
import pandas as pd
import streamlit as st


# -------------------------------------------------------------------
# 1. C-ABI Structure & DLL Binding with Rust Core
# -------------------------------------------------------------------
class DynamicCognitivePacket(ctypes.Structure):
    _fields_ = [
        ("process_time_ms", ctypes.c_uint64),
        ("cognitive_load", ctypes.c_float),
        ("awareness_score", ctypes.c_float),
        ("user_valence", ctypes.c_float),
        ("user_arousal", ctypes.c_float),
        ("has_false_belief", ctypes.c_bool),
    ]


RUST_LIB_PATH = os.path.abspath(
    "../mindas_core_rust/target/release/mindas_core.dll"
)


@st.cache_resource
def load_rust_core():
    if os.path.exists(RUST_LIB_PATH):
        try:
            core = ctypes.CDLL(RUST_LIB_PATH)
            core.fetch_unified_state.restype = DynamicCognitivePacket
            return core
        except Exception as e:
            st.warning(f"Could not bind C-ABI DLL: {e}")
            return None
    return None


rust_core = load_rust_core()

# -------------------------------------------------------------------
# 2. Page Configuration & Futuristic UI Theme
# -------------------------------------------------------------------
st.set_page_config(
    page_title="M.I.N.D.A.S. Metacognitive Interface",
    page_icon="🧠",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #00e5ff;
    }
    .chat-bubble-user {
        background-color: #1e293b;
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
    }
    .chat-bubble-ai {
        background-color: #0f172a;
        border: 1px solid #00f2fe;
        color: #00f2fe;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0px 0px 10px rgba(0,242,254,0.15);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []

if "telemetry_history" not in st.session_state:
    st.session_state.telemetry_history = pd.DataFrame(
        columns=["Time", "Cognitive_Load", "Valence", "Arousal"]
    )

# -------------------------------------------------------------------
# 3. Real-Time Telemetry Fetching Logic
# -------------------------------------------------------------------
if rust_core is not None:
    packet = rust_core.fetch_unified_state()
    latency = packet.process_time_ms
    cog_load = packet.cognitive_load
    awareness = packet.awareness_score
    valence = packet.user_valence
    arousal = packet.user_arousal
    false_belief = packet.has_false_belief
    telemetry_source = "Rust Shared Memory DLL (FFI Direct)"
else:
    # Fallback to Live Simulation if DLL isn't built yet
    latency = random.randint(12, 45)
    cog_load = round(random.uniform(15.0, 35.0), 2)
    awareness = round(random.uniform(0.85, 0.99), 2)
    valence = round(random.uniform(-0.5, 0.8), 2)
    arousal = round(random.uniform(0.1, 0.6), 2)
    false_belief = False
    telemetry_source = "Simulated Fallback Engine"

# Record historical telemetry state
new_entry = {
    "Time": time.strftime("%H:%M:%S"),
    "Cognitive_Load": cog_load,
    "Valence": valence,
    "Arousal": arousal,
}

st.session_state.telemetry_history = pd.concat(
    [st.session_state.telemetry_history, pd.DataFrame([new_entry])],
    ignore_index=True,
).tail(25)

# -------------------------------------------------------------------
# 4. Sidebar Layout: System Telemetry Monitors
# -------------------------------------------------------------------
with st.sidebar:
    st.header("📊 Telemetry Metrics")
    st.caption(f"Source: {telemetry_source}")

    st.metric(
        label="Theory of Mind Status", value="ACTIVE", delta="Empathy Core On"
    )
    st.metric(label="Processing Latency", value=f"{latency} ms")
    st.metric(label="Cognitive Load", value=f"{cog_load:.2f} GFLOPS")
    st.metric(label="Awareness Index", value=f"{awareness * 100:.1f}%")

    st.markdown("---")
    st.subheader("🧠 Emotional Perception")
    st.progress(max(0.0, min(1.0, (valence + 1) / 2)), text=f"User Valence: {valence:.2f}")
    st.progress(max(0.0, min(1.0, arousal)), text=f"User Stress / Arousal: {arousal:.2f}")

    st.markdown("---")
    st.subheader("Mental Model Status")
    if false_belief:
        st.error("🚨 **FALSE BELIEF DETECTED**\n\nUser model disagrees with truth.")
    else:
        st.success("✅ **BELIEF ALIGNED**\n\nUser perception matches ground truth.")

# -------------------------------------------------------------------
# 5. Main UI Layout: Chat & Real-Time Analytics
# -------------------------------------------------------------------
st.title("🧠 M.I.N.D.A.S. Metacognitive Observer Dashboard")
st.markdown(
    "**Real-time Cross-Language Telemetry Monitor & Interactive Chat** *(Mojo Engine + Julia ToM + Rust Core FFI)*"
)

st.divider()

# Top Tab Panels: Interactive Chat vs Real-Time Analytics
tab1, tab2 = st.tabs(["💬 Dialogue & Reasoning Engine", "📈 System Analytics"])

with tab1:
    st.subheader("Interactive Cognitive Dialogue")

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="chat-bubble-user"><b>You:</b> {message["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-bubble-ai"><b>M.I.N.D.A.S.:</b> {message["content"]}</div>',
                unsafe_allow_html=True,
            )

    # Chat input control
    user_prompt = st.chat_input("Ask or command M.I.N.D.A.S. AI Core...")

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.markdown(
            f'<div class="chat-bubble-user"><b>You:</b> {user_prompt}</div>',
            unsafe_allow_html=True,
        )

        with st.spinner("Processing through Agent Reasoning & ToM Engine..."):
            time.sleep(0.6)
            ai_response = f"Analyzed input: '{user_prompt}'. Valence: {valence:.2f}, Cognitive Load: {cog_load:.2f}. Theory of Mind memory updated."

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response}
        )
        st.markdown(
            f'<div class="chat-bubble-ai"><b>M.I.N.D.A.S.:</b> {ai_response}</div>',
            unsafe_allow_html=True,
        )

with tab2:
    st.subheader("Real-Time Cognitive Telemetry Signals")

    col_chart, col_meta = st.columns([2, 1])

    with col_chart:
        st.line_chart(st.session_state.telemetry_history.set_index("Time"))

    with col_meta:
        st.subheader("System Metadata")
        st.json(
            {
                "Engine Status": "ACTIVE",
                "FFI Interop Bridge": "C-ABI DLL Shared",
                "Thread State": "Lock-Free Atomic",
                "Rust DLL Path": RUST_LIB_PATH,
                "DLL Found": os.path.exists(RUST_LIB_PATH),
            }
        )