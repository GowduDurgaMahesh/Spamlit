import joblib
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="SpamLit | SMS Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Dark Styling & Aesthetics
st.markdown(
    """
    <style>
    /* Global Dark Theme */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Header Container */
    .hero-container {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        border: 1px solid rgba(55, 65, 81, 0.6);
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    
    .brand-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .brand-subtitle {
        font-size: 1.05rem;
        color: #9ca3af;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }

    /* Custom Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        background-color: #1f2937;
        color: #f3f4f6;
        border: 1px solid #374151;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        background-color: #374151;
        border-color: #4b5563;
        color: #ffffff;
    }
    
    /* Text Area Styling */
    .stTextArea textarea {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }

    /* Metrics Override */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
    }

    /* Hide standard UI elements for clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LOAD MODEL & VECTORIZER
# ============================================================
@st.cache_resource
def load_assets():
  tfidf = joblib.load("sms_spam_tfidf_bigrams.pkl")
  svm_model = joblib.load("sms_spam_svm_bigrams.pkl")
  return tfidf, svm_model


try:
  tfidf, svm_model = load_assets()
except Exception as e:
  st.error(
      f"⚠️ **Asset Loading Error:** Please verify model file paths. Details: {e}"
  )
  st.stop()


# Initialize Session State for text area input
if "input_text" not in st.session_state:
  st.session_state["input_text"] = ""

# Reference Messages Dataset
REFERENCE_MESSAGES = {
    "Select a reference message...": "",
    "🚨 [SPAM] Prize Winner Alert": (
        "WINNER!! As a valued network customer you have been selected to"
        " receivea £900 prize reward! To claim call 09061701461. Claim code"
        " KL341. Valid 12 hours only."
    ),
    "🚨 [SPAM] Free Mobile Upgrade": (
        "Had your mobile 11 months or more? U R entitled to Update to the"
        " latest colour mobiles with camera for Free! Call The Mobile Update Co"
        " FREE on 08002986030"
    ),
    "🚨 [SPAM] Paid Message Offer": (
        "FreeMsg Hey there darling it's been 3 week's now and no word back! I'd"
        " like some fun you up for it still? Tb ok! XxX std chgs to send,"
        " £1.50 to rcv"
    ),
    "✅ [HAM] Conversational Message": (
        "I'm gonna be home soon and i don't want to talk about this stuff"
        " anymore tonight, k? I've cried enough today."
    ),
    "✅ [HAM] Personal Reaction": (
        "Even my brother is not like to speak with me. They treat me like aids"
        " patent."
    ),
    "✅ [HAM] Service Notification": (
        "As per your request 'Melle Melle (Oru Minnaminunginte Nurungu Vettam)'"
        " has been set as your callertune for all Callers. Press *9 to copy your"
        " friends Callertune"
    ),
}


def set_text(text):
  st.session_state["input_text"] = text


# ============================================================
# SIDEBAR: MODEL PERFORMANCE METRICS
# ============================================================
with st.sidebar:
  st.markdown("### 🛡️ **SpamLit OS**")
  st.caption("AI Threat Detection Core")

  st.markdown("---")
  st.subheader("Performance Metrics")

  col_a, col_b = st.columns(2)
  with col_a:
    st.metric("Accuracy", "97.86%")
    st.metric("Precision", "92.62%")
  with col_b:
    st.metric("ROC-AUC", "98.17%")
    st.metric("Recall", "89.68%")

  st.metric("F1 Score", "91.13%")

  st.markdown("---")
  with st.expander("Confusion Matrix Details"):
    st.write("**True Negatives (TN):** 891")
    st.write("**True Positives (TP):** 113")
    st.write("**False Positives (FP):** 9")
    st.write("**False Negatives (FN):** 13")


# ============================================================
# MAIN INTERFACE (HERO HEADER)
# ============================================================
st.markdown(
    """
    <div class="hero-container">
        <p class="brand-title">🛡️ SpamLit</p>
        <p class="brand-subtitle">Real-time SMS & message threat intelligence platform powered by Linear Support Vector Machines.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Control Layout for Dropdown & Shortcuts
control_col1, control_col2 = st.columns([1.5, 1], gap="medium")

with control_col1:
  selected_option = st.selectbox(
      "📥 **Load a sample reference message:**",
      options=list(REFERENCE_MESSAGES.keys()),
  )
  if (
      selected_option != "Select a reference message..."
      and REFERENCE_MESSAGES[selected_option]
  ):
    st.session_state["input_text"] = REFERENCE_MESSAGES[selected_option]

with control_col2:
  st.markdown("**⚡ Quick Test Shortcuts:**")
  b_col1, b_col2 = st.columns(2)
  if b_col1.button("🚨 Test Spam"):
    set_text(
        "WINNER!! As a valued network customer you have been selected to"
        " receivea £900 prize reward! To claim call 09061701461. Claim code"
        " KL341. Valid 12 hours only."
    )
    st.rerun()
  if b_col2.button("💬 Test Ham"):
    set_text(
        "I'm gonna be home soon and i don't want to talk about this stuff"
        " anymore tonight, k? I've cried enough today."
    )
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Main Form Console
with st.form(key="classifier_form"):
  st.markdown("#### 📝 Message Inspector Console")
  user_input = st.text_area(
      label="SMS Input Text",
      value=st.session_state["input_text"],
      placeholder=(
          "Type, paste, or select a sample message above to scan for threats..."
      ),
      height=140,
      label_visibility="collapsed",
  )

  sub_col1, sub_col2, sub_col3 = st.columns([1, 2, 1])
  with sub_col2:
    submit_button = st.form_submit_button(
        label="⚡ Run Deep Threat Analysis", use_container_width=True
    )

# ============================================================
# PREDICTION & RESULTS
# ============================================================
if submit_button or st.session_state["input_text"]:
  cleaned_input = user_input.strip()

  if not cleaned_input:
    st.warning("⚠️ Please enter or select an SMS message to analyze.")
  else:
    # Transform input
    X_vec = tfidf.transform([cleaned_input])

    # Predict & Score
    prediction = svm_model.predict(X_vec)[0]
    score = svm_model.decision_function(X_vec)[0]

    st.markdown("---")
    st.subheader("🎯 Analysis Results")

    res_col1, res_col2 = st.columns([1, 1.5], gap="large")

    with res_col1:
      if prediction == 1:
        st.error("### 🚨 SPAM DETECTED")
        st.markdown(
            "**Verdict:** This message matches known patterns for unsolicited,"
            " promotional, or malicious text."
        )
      else:
        st.success("### ✅ LEGITIMATE (HAM)")
        st.markdown(
            "**Verdict:** This message appears to be safe standard"
            " communication."
        )

    with res_col2:
      st.markdown("#### 📈 SVM Hyperplane Decision Score")
      st.write(f"Raw Decision Score: `{score:.4f}`")

      if score > 0:
        norm_score = min(100, int(50 + (score * 15)))
        st.progress(
            norm_score, text=f"Spam Intensity Signal: **{norm_score}%**"
        )
      else:
        norm_score = max(0, int(50 + (score * 15)))
        st.progress(
            norm_score, text=f"Ham Confidence Level: **{100 - norm_score}%**"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🛠️ View Technical Model Breakdown"):
      st.json({
          "Application": "SpamLit Threat Engine",
          "Input Character Count": len(cleaned_input),
          "Input Word Count": len(cleaned_input.split()),
          "Prediction Class": "SPAM (1)" if prediction == 1 else "HAM (0)",
          "SVM Decision Function Score": float(score),
          "Vectorization": "TF-IDF (Unigrams + Bigrams)",
      })

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #4b5563; font-size: 0.85rem;'>"
    "SpamLit Threat Security Suite • Designed for Simplicity and Speed"
    "</div>",
    unsafe_allow_html=True,
)