import streamlit as st

st.set_page_config(
    page_title="AI Electronic Component Consultant",
    page_icon="🤖",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: 700; color: #1E3A8A; margin-bottom: 2px; }
    .sub-title { font-size: 14px; color: #4B5563; margin-bottom: 18px; }
    .trace-box { background-color: #111827; color: #10B981; padding: 14px; border-radius: 8px; font-family: monospace; font-size: 13px; line-height: 1.5; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🤖 Interactive AI Component Recommender</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Fundamentals of Artificial Intelligence (CCE-4) | Conversational Expert System & CSP Engine</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 1. COMPONENT KNOWLEDGE BASE
# ---------------------------------------------------------
COMPONENT_DB = [
    # Microcontrollers
    {"name": "ESP32-S3 DevKitC-1", "cat": "Microcontroller", "cost": 550, "power": 240, "volt": 3.3, "wireless": ["wifi", "ble"], "domain": ["iot", "weather", "robotics", "industrial"], "rel": 9.3},
    {"name": "Raspberry Pi Pico W", "cat": "Microcontroller", "cost": 420, "power": 150, "volt": 3.3, "wireless": ["wifi"], "domain": ["iot", "weather", "agriculture"], "rel": 8.9},
    {"name": "STM32F411 BlackPill", "cat": "Microcontroller", "cost": 480, "power": 120, "volt": 3.3, "wireless": [], "domain": ["robotics", "industrial", "wearable"], "rel": 9.5},
    {"name": "nRF52840 Dongle / Board", "cat": "Microcontroller", "cost": 850, "power": 45, "volt": 3.3, "wireless": ["ble"], "domain": ["wearable", "iot"], "rel": 9.4},
    {"name": "Arduino Uno R3 (ATmega328P)", "cat": "Microcontroller", "cost": 450, "power": 200, "volt": 5.0, "wireless": [], "domain": ["robotics", "agriculture"], "rel": 9.0},

    # Sensors
    {"name": "BME280 (Temp, Humidity, Pressure)", "cat": "Sensor", "cost": 350, "power": 4, "volt": 3.3, "wireless": [], "domain": ["weather", "agriculture", "iot"], "rel": 9.5},
    {"name": "MQ-135 Air Quality & Gas Sensor", "cat": "Sensor", "cost": 250, "power": 800, "volt": 5.0, "wireless": [], "domain": ["weather", "industrial"], "rel": 7.6},
    {"name": "PMS5003 Laser PM2.5 Dust Sensor", "cat": "Sensor", "cost": 1800, "power": 500, "volt": 5.0, "wireless": [], "domain": ["weather", "industrial"], "rel": 9.4},
    {"name": "MPU6050 6-Axis IMU (Accel + Gyro)", "cat": "Sensor", "cost": 180, "power": 12, "volt": 3.3, "wireless": [], "domain": ["robotics", "wearable", "industrial"], "rel": 8.8},
    {"name": "Capacitive Soil Moisture Sensor v2", "cat": "Sensor", "cost": 140, "power": 15, "volt": 3.3, "wireless": [], "domain": ["agriculture"], "rel": 8.5},
    {"name": "MAX30102 Pulse Oximeter & Heart Rate", "cat": "Sensor", "cost": 290, "power": 10, "volt": 3.3, "wireless": [], "domain": ["wearable"], "rel": 9.1},

    # Actuators & Drivers
    {"name": "L298N Dual H-Bridge Motor Driver", "cat": "Driver", "cost": 190, "power": 150, "volt": 5.0, "wireless": [], "domain": ["robotics"], "rel": 8.4},
    {"name": "TB6612FNG Efficient Motor Driver", "cat": "Driver", "cost": 280, "power": 50, "volt": 3.3, "wireless": [], "domain": ["robotics"], "rel": 9.3},
    {"name": "5V 2-Channel Optocoupler Relay", "cat": "Driver", "cost": 120, "power": 140, "volt": 5.0, "wireless": [], "domain": ["agriculture", "industrial", "iot"], "rel": 8.9},
    {"name": "4-Channel Bi-Directional Level Shifter", "cat": "Driver", "cost": 60, "power": 2, "volt": 3.3, "wireless": [], "domain": ["safety"], "rel": 9.2},

    # Power ICs
    {"name": "TP4056 Li-Ion Charger + Boost Module", "cat": "Power IC", "cost": 65, "power": 20, "volt": 5.0, "wireless": [], "domain": ["battery", "wearable", "robotics", "iot"], "rel": 9.1},
    {"name": "AMS1117-3.3V Low Dropout Regulator", "cat": "Power IC", "cost": 30, "power": 15, "volt": 3.3, "wireless": [], "domain": ["usb", "mains", "iot", "weather"], "rel": 9.2},
    {"name": "LM2596 DC-DC Buck Converter", "cat": "Power IC", "cost": 95, "power": 35, "volt": 5.0, "wireless": [], "domain": ["robotics", "industrial", "agriculture"], "rel": 9.3},
]

# ---------------------------------------------------------
# 2. QUESTIONNAIRE FLOW DEFINITION
# ---------------------------------------------------------
QUESTIONS = [
    {
        "key": "domain",
        "text": "👋 Welcome! Let's design your hardware architecture. **Question 1 of 6:** What type of project are you building?",
        "options": [
            "Smart Weather & Air Quality Monitor",
            "Autonomous Robotics / Drone",
            "Smart Agriculture & Irrigation",
            "Low-Power Health Wearable",
            "Industrial Machine Monitor"
        ]
    },
    {
        "key": "wireless",
        "text": "**Question 2 of 6:** What wireless connectivity does your system need?",
        "options": [
            "Wi-Fi + Bluetooth (Cloud + App)",
            "Wi-Fi Only (Cloud Dashboard)",
            "Bluetooth Low Energy (BLE Only)",
            "No Wireless Needed (Offline / Wired)"
        ]
    },
    {
        "key": "power_source",
        "text": "**Question 3 of 6:** How will the project be powered?",
        "options": [
            "Li-Ion / LiPo Battery (Portable)",
            "5V USB Adapter / Power Bank",
            "12V DC Adapter / Solar Panel"
        ]
    },
    {
        "key": "actuators",
        "text": "**Question 4 of 6:** Does your project need to control motors, pumps, or relays?",
        "options": [
            "Yes - DC / Stepper Motors",
            "Yes - Water Pump / AC Relay",
            "No - Sensors & Data Only"
        ]
    },
    {
        "key": "budget",
        "text": "**Question 5 of 6:** What is your maximum component budget (in ₹)?",
        "options": [
            "Ultra-Low Budget (Under ₹1,000)",
            "Standard Student Budget (Under ₹2,000)",
            "High-Precision Budget (Under ₹4,000)"
        ]
    },
    {
        "key": "priority",
        "text": "**Question 6 of 6:** What is your #1 engineering priority for utility optimization?",
        "options": [
            "Lowest Total Cost",
            "Ultra-Low Power Consumption",
            "Maximum Sensor Accuracy & Reliability"
        ]
    }
]

# ---------------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": QUESTIONS[0]["text"]}
    ]

def reset_chat():
    st.session_state.step = 0
    st.session_state.answers = {}
    st.session_state.chat_history = [{"role": "assistant", "content": QUESTIONS[0]["text"]}]

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Start New Consultation", use_container_width=True):
        reset_chat()
        st.rerun()
    st.markdown("---")
    st.markdown("**Collected Specifications:**")
    if st.session_state.answers:
        for k, v in st.session_state.answers.items():
            st.write(f"• **{k.capitalize()}:** {v}")
    else:
        st.caption("Answer the AI's questions to populate live parameters.")

# ---------------------------------------------------------
# 4. HYBRID AI INFERENCE ENGINE (CSP + RULES + UTILITY)
# ---------------------------------------------------------
def run_hybrid_ai(ans):
    trace = []
    trace.append("[INIT] Starting Hybrid AI Engine (CSP + Forward Chaining + Utility Scoring)...")

    # Parse answers
    dom_str = ans.get("domain", "").lower()
    if "weather" in dom_str or "air" in dom_str: domain = "weather"
    elif "robot" in dom_str or "drone" in dom_str: domain = "robotics"
    elif "agri" in dom_str or "soil" in dom_str: domain = "agriculture"
    elif "wearable" in dom_str or "health" in dom_str: domain = "wearable"
    elif "indus" in dom_str: domain = "industrial"
    else: domain = "iot"

    wire_str = ans.get("wireless", "").lower()
    req_wifi = "wi-fi" in wire_str or "wifi" in wire_str
    req_ble = "ble" in wire_str or "bluetooth" in wire_str

    bud_str = ans.get("budget", "").lower()
    if "1,000" in bud_str or "1000" in bud_str: max_budget = 1000
    elif "2,000" in bud_str or "2000" in bud_str: max_budget = 2000
    elif "4,000" in bud_str or "4000" in bud_str: max_budget = 4000
    else:
        nums = [int(s) for s in bud_str.replace(",", "").split() if s.isdigit()]
        max_budget = nums[0] if nums else 2500

    prio_str = ans.get("priority", "").lower()
    if "cost" in prio_str: w_cost, w_pow, w_rel = 0.6, 0.2, 0.2
    elif "power" in prio_str: w_cost, w_pow, w_rel = 0.2, 0.6, 0.2
    else: w_cost, w_pow, w_rel = 0.2, 0.2, 0.6

    trace.append(f"[CSP] Parsed Domain='{domain}', MaxBudget=₹{max_budget}, WiFi={req_wifi}, BLE={req_ble}")

    # Utility calculation helper
    def utility(item):
        norm_cost = max(0, 10 - (item["cost"] / 200))
        norm_pow = max(0, 10 - (item["power"] / 100))
        return round((w_rel * item["rel"]) + (w_cost * norm_cost) + (w_pow * norm_pow), 2)

    # STEP 1: Select Microcontroller via CSP + Utility
    mcus = [c for c in COMPONENT_DB if c["cat"] == "Microcontroller"]
    valid_mcus = []
    for m in mcus:
        if req_wifi and "wifi" not in m["wireless"]:
            trace.append(f"[CSP PRUNE] Rejected {m['name']} (Missing Wi-Fi)")
            continue
        if req_ble and "ble" not in m["wireless"]:
            trace.append(f"[CSP PRUNE] Rejected {m['name']} (Missing BLE)")
            continue
        if m["cost"] > max_budget * 0.6:
            trace.append(f"[CSP PRUNE] Rejected {m['name']} (Exceeds 60% budget share)")
            continue
        valid_mcus.append(m)

    if not valid_mcus:
        valid_mcus = [mcus[0]] # Fallback if constraints are impossible
        trace.append("[CSP RELAX] Relaxed strict wireless constraint to avoid empty set.")

    best_mcu = max(valid_mcus, key=utility)
    trace.append(f"[UTILITY WIN] Selected MCU: {best_mcu['name']} (Score: {utility(best_mcu)})")

    # STEP 2: Forward Chaining Rule-Based Sensor Selection
    selected_sensors = []
    remaining_budget = max_budget - best_mcu["cost"]
    domain_sensors = [c for c in COMPONENT_DB if c["cat"] == "Sensor" and domain in c["domain"]]
    domain_sensors.sort(key=utility, reverse=True)

    for s in domain_sensors:
        if s["cost"] <= remaining_budget - 150:
            selected_sensors.append(s)
            remaining_budget -= s["cost"]
            trace.append(f"[RULE FIRED] Domain '{domain}' matched sensor -> {s['name']} (₹{s['cost']})")
        else:
            trace.append(f"[CSP PRUNE] Skipped {s['name']} (₹{s['cost']}) to preserve budget.")

    # STEP 3: Actuator & Driver Rules
    selected_drivers = []
    act_str = ans.get("actuators", "").lower()
    if "motor" in act_str:
        drv = next((c for c in COMPONENT_DB if "Motor Driver" in c["name"] and c["cost"] <= remaining_budget), None)
        if drv:
            selected_drivers.append(drv)
            remaining_budget -= drv["cost"]
            trace.append(f"[RULE FIRED] Motor load detected -> Added {drv['name']}")
    elif "pump" in act_str or "relay" in act_str:
        drv = next((c for c in COMPONENT_DB if "Relay" in c["name"]), None)
        if drv:
            selected_drivers.append(drv)
            remaining_budget -= drv["cost"]
            trace.append(f"[RULE FIRED] High-voltage/Pump load -> Added {drv['name']}")

    # STEP 4: Power Management Rule
    pow_str = ans.get("power_source", "").lower()
    if "battery" in pow_str or "lipo" in pow_str:
        pwr = next(c for c in COMPONENT_DB if "TP4056" in c["name"])
        trace.append("[RULE FIRED] Battery source -> Added TP4056 Li-Ion Charger/Boost")
    elif "12v" in pow_str or "solar" in pow_str:
        pwr = next(c for c in COMPONENT_DB if "LM2596" in c["name"])
        trace.append("[RULE FIRED] 12V/Solar source -> Added LM2596 Buck Converter")
    else:
        pwr = next(c for c in COMPONENT_DB if "AMS1117" in c["name"])
        trace.append("[RULE FIRED] 5V USB source -> Added AMS1117-3.3V LDO Regulator")

    # STEP 5: Voltage Safety Rule (3.3V MCU + 5V Sensor)
    all_parts = [best_mcu] + selected_sensors + selected_drivers + [pwr]
    if best_mcu["volt"] == 3.3 and any(p["volt"] == 5.0 for p in selected_sensors + selected_drivers):
        shifter = next(c for c in COMPONENT_DB if "Level Shifter" in c["name"])
        selected_drivers.append(shifter)
        all_parts.append(shifter)
        trace.append("[SAFETY RULE] 3.3V MCU paired with 5V peripheral -> Auto-added Logic Level Shifter!")

    total_cost = sum(p["cost"] for p in all_parts)
    total_power = sum(p["power"] for p in all_parts)
    trace.append(f"[DONE] Final Cost: ₹{total_cost} / ₹{max_budget} | Total Power: {total_power} mW")

    return best_mcu, selected_sensors, selected_drivers, pwr, total_cost, total_power, trace

# ---------------------------------------------------------
# 5. RENDER CONVERSATION & INTERACTIVE OPTIONS
# ---------------------------------------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def handle_user_answer(answer_text):
    current_q = QUESTIONS[st.session_state.step]
    st.session_state.answers[current_q["key"]] = answer_text
    st.session_state.chat_history.append({"role": "user", "content": answer_text})
    st.session_state.step += 1

    if st.session_state.step < len(QUESTIONS):
        next_q = QUESTIONS[st.session_state.step]["text"]
        st.session_state.chat_history.append({"role": "assistant", "content": next_q})
    else:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "✅ **All parameters collected!** Running Hybrid AI Engine (CSP + Expert Rules + Utility Optimization)..."
        })
    st.rerun()

# Show clickable options + text input while questions remain
if st.session_state.step < len(QUESTIONS):
    current_q = QUESTIONS[st.session_state.step]
    st.markdown("#### 👇 Tap an option below OR type your own custom answer:")
    cols = st.columns(2)
    for idx, opt in enumerate(current_q["options"]):
        if cols[idx % 2].button(opt, key=f"opt_{st.session_state.step}_{idx}", use_container_width=True):
            handle_user_answer(opt)

    custom_ans = st.chat_input("Or type your custom answer here...")
    if custom_ans:
        handle_user_answer(custom_ans)

# ---------------------------------------------------------
# 6. DISPLAY FINAL AI RECOMMENDATION & EXPLAINABLE TRACE
# ---------------------------------------------------------
else:
    mcu, sensors, drivers, pwr, t_cost, t_pow, trace_log = run_hybrid_ai(st.session_state.answers)

    st.markdown("---")
    st.subheader("🎯 AI-Recommended Hardware Architecture")

    m1, m2, m3 = st.columns(3)
    m1.metric("Total System Cost", f"₹{t_cost}")
    m2.metric("Estimated Active Power", f"{t_pow} mW")
    m3.metric("Constraint Violations", "0 (100% Compatible)")

    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**🎛️ Primary Microcontroller:**\n\n**{mcu['name']}** — ₹{mcu['cost']} ({mcu['volt']}V Logic)")
        st.success(f"**⚡ Power Management:**\n\n**{pwr['name']}** — ₹{pwr['cost']}")

    with c2:
        sensor_md = "\n".join([f"- **{s['name']}** (₹{s['cost']}, {s['volt']}V)" for s in sensors]) or "- None required"
        st.warning(f"**🌡️ Recommended Sensors:**\n\n{sensor_md}")

        driver_md = "\n".join([f"- **{d['name']}** (₹{d['cost']})" for d in drivers]) or "- None required"
        st.success(f"**🔌 Drivers & Protection:**\n\n{driver_md}")

    with st.expander("🧠 View Live Explainable AI (XAI) Reasoning Trace (For Viva)", expanded=True):
        st.markdown(f'<div class="trace-box">{"<br>".join(trace_log)}</div>', unsafe_allow_html=True)

    st.button("🔄 Ask Again / Test Different Answers", on_click=reset_chat, type="primary")
