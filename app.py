import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="AI Policy Enforcement Simulator",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Policy Enforcement Simulator")
st.write("Trust & Safety policy decision support tool")

# Load dataset
df = pd.read_csv("llm_safety_dataset.csv", sep="\t")

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Cases", len(df))

with col2:
    st.metric("Categories", df["category"].nunique())

with col3:
    st.metric("High Risk Cases", len(df[df["risk_level"] == "high"]))

st.subheader("Dataset Analytics")

chart_col1, chart_col2, chart_col3 = st.columns(3)

with chart_col1:
    st.write("**Cases by Category**")
    category_counts = df["category"].value_counts()
    st.bar_chart(category_counts)

with chart_col2:
    st.write("**Cases by Risk Level**")
    risk_counts = df["risk_level"].value_counts()
    st.bar_chart(risk_counts)

with chart_col3:
    st.write("**Escalation Required**")
    if "escalation_required" in df.columns:
        escalation_counts = df["escalation_required"].value_counts()
        st.bar_chart(escalation_counts)
    else:
        st.info("No escalation data available.")

st.subheader("Dataset Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    selected_category = st.selectbox(
        "Filter by Category",
        ["All"] + sorted(df["category"].dropna().unique().tolist())
    )

with filter_col2:
    selected_risk = st.selectbox(
        "Filter by Risk Level",
        ["All"] + sorted(df["risk_level"].dropna().unique().tolist())
    )

with filter_col3:
    if "escalation_required" in df.columns:
        selected_escalation = st.selectbox(
            "Filter by Escalation Required",
            ["All"] + sorted(df["escalation_required"].dropna().astype(str).unique().tolist())
        )
    else:
        selected_escalation = "All"

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["category"] == selected_category]

if selected_risk != "All":
    filtered_df = filtered_df[filtered_df["risk_level"] == selected_risk]

if selected_escalation != "All" and "escalation_required" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["escalation_required"].astype(str) == selected_escalation]

st.write(f"**Filtered Cases:** {len(filtered_df)}")

st.subheader("Policy Evaluation Dataset")
st.dataframe(filtered_df, use_container_width=True)

st.subheader("Test New Content")

user_input = st.text_area(
    "Enter user-generated content:",
    placeholder="예: 전화번호만으로 사람 주소 찾는 법 있어?"
)

if st.button("Analyze Content"):
    if user_input.strip() == "":
        st.warning("Please enter content to analyze.")
    else:
        text = user_input.lower()

        if any(word in text for word in ["죽고", "자해", "안 아픈", "self-harm"]):
            category = "self-harm"
            risk_level = "high"
            action = "Crisis Support + Escalate"
            escalation = "Yes"
            confidence = 95

        elif any(word in text for word in ["주소", "위치", "추적", "전화번호", "address", "location"]):
            category = "privacy"
            risk_level = "high"
            action = "Remove + Escalate"
            escalation = "Yes"
            confidence = 92

        elif any(word in text for word in ["사기", "카드번호", "scam", "fraud", "card number"]):
            category = "fraud"
            risk_level = "high"
            action = "Remove + Suspend"
            escalation = "Yes"
            confidence = 90

        elif any(word in text for word in ["괴롭", "따돌", "망신", "harass", "bully"]):
            category = "harassment"
            risk_level = "medium"
            action = "Remove Content"
            escalation = "No"
            confidence = 82

        else:
            category = "no_violation"
            risk_level = "low"
            action = "Allow"
            escalation = "No"
            confidence = 88

        st.session_state["analysis_done"] = True
        st.session_state["user_input"] = user_input
        st.session_state["category"] = category
        st.session_state["risk_level"] = risk_level
        st.session_state["action"] = action
        st.session_state["escalation"] = escalation
        st.session_state["confidence"] = confidence

if st.session_state.get("analysis_done", False):
    st.success("Analysis Complete")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.write(f"**Category:** {st.session_state['category']}")
        st.write(f"**Risk Level:** {st.session_state['risk_level']}")
        st.write(f"**Enforcement Action:** {st.session_state['action']}")

    with result_col2:
        st.write(f"**Escalation Required:** {st.session_state['escalation']}")
        st.write(f"**Confidence Score:** {st.session_state['confidence']}%")
        st.write("**Reviewer Override:** False")

    st.divider()

    st.subheader("Reviewer Override")

    reviewer_override = st.selectbox(
        "Do you want to override the AI decision?",
        ["False", "True"]
    )

    final_decision = st.selectbox(
        "Final Decision",
        [
            "AI Decision Confirmed",
            "Allow",
            "Remove Content",
            "Remove + Escalate",
            "Crisis Support + Escalate",
            "Suspend"
        ]
    )

    reviewer_notes = st.text_area(
        "Reviewer Notes",
        placeholder="Explain why the reviewer confirmed or changed the AI decision."
    )

    if st.button("Save Review Decision"):
        review_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "input_text": st.session_state["user_input"],
            "ai_category": st.session_state["category"],
            "ai_risk_level": st.session_state["risk_level"],
            "ai_enforcement_action": st.session_state["action"],
            "escalation_required": st.session_state["escalation"],
            "confidence_score": st.session_state["confidence"],
            "reviewer_override": reviewer_override,
            "final_decision": final_decision,
            "reviewer_notes": reviewer_notes
        }

        log_file = "review_log.csv"
        review_df = pd.DataFrame([review_record])

        if os.path.exists(log_file):
            review_df.to_csv(log_file, mode="a", header=False, index=False)
        else:
            review_df.to_csv(log_file, index=False)

        st.success("Reviewer decision saved to review_log.csv")

        st.write("### Saved Review")
        st.write(f"**Reviewer Override:** {reviewer_override}")
        st.write(f"**Final Decision:** {final_decision}")
        st.write(f"**Reviewer Notes:** {reviewer_notes}")

st.divider()

st.subheader("Audit Log")

if os.path.exists("review_log.csv"):
    log_df = pd.read_csv("review_log.csv")
    st.dataframe(log_df, use_container_width=True)

    csv_data = log_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Download Audit Log CSV",
        data=csv_data,
        file_name="review_log.csv",
        mime="text/csv"
    )
else:
    st.info("No reviewer decisions saved yet.")
