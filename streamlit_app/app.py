import streamlit as st
import datetime
import numpy as np
import cv2
from PIL import Image

from ai_workflow import (
    analyze_image_damage,
    detect_intent,
    detect_issue_type,
    detect_severity,
    generate_reply,
    recommend_technician,
    estimate_cost,
    validate_response
)

st.set_page_config(page_title="AI Wall Damage Detection")

st.title("AI Wall Damage Detection & Support Assistant")

# -------------------------
# SESSION STATE INIT
# -------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "issue_history" not in st.session_state:
    st.session_state.issue_history = []


# -------------------------
# IMAGE UPLOAD SECTION
# -------------------------

uploaded_file = st.file_uploader(
    "Upload wall damage image",
    type=["jpg","png","jpeg"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    img = np.array(image)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    result, processed_img, damage_percent, heatmap = analyze_image_damage(img)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Original Image")

    with col2:
        st.image(processed_img, caption="AI Detection")

    st.image(heatmap, caption="Damage Heatmap", width="stretch")

    st.progress(int(damage_percent * 10))

    st.write(f"Damage Detected: {damage_percent:.2f}%")

    st.markdown("### AI Visual Analysis")

    st.info(f"""
Detected Issue: {result['issue']}

Severity Level: {result['severity']}

Recommended Technician: {result['technician']}

Estimated Repair Cost: {result['cost']}
""")

    # SAVE IMAGE RESULT TO HISTORY
    st.session_state.history.append({
        "type": "image",
        "image": image,
        "result": result
    })


# -------------------------
# CHAT HISTORY DISPLAY
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -------------------------
# USER CHAT INPUT
# -------------------------

user_input = st.chat_input("Describe your issue")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)


    intent = detect_intent(user_input)

    issue = detect_issue_type(user_input)

    severity = detect_severity(user_input)

    technician = recommend_technician(issue)

    cost = estimate_cost(issue)

    reply = generate_reply(user_input)

    if not validate_response(reply):

        reply = "Please consult a professional technician."


    with st.chat_message("assistant"):

        if intent == "Emergency":

            st.error("⚠ Emergency issue detected")

        st.markdown(reply)

        st.markdown("### Severity Level")

        st.warning(severity)

        st.markdown("### Recommended Technician")

        st.info(technician)

        st.markdown("### Estimated Repair Cost")

        st.success(cost)


    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )


    # SAVE ISSUE HISTORY
    st.session_state.issue_history.append({

        "issue": issue,

        "severity": severity,

        "time": datetime.datetime.now().strftime("%H:%M")
    })


# -------------------------
# SIDEBAR HISTORY
# -------------------------

st.sidebar.title("Issue History")

for item in st.session_state.issue_history:

    st.sidebar.write(
        f"{item['time']} - {item['issue']} ({item['severity']})"
    )


for item in st.session_state.history:

    if item["type"] == "image":

        st.sidebar.image(item["image"], width=120)

        st.sidebar.write(item["result"]["issue"])