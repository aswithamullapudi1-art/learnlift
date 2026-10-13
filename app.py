import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# -------------------- Page setup --------------------
st.set_page_config(
    page_title="LearnLift | Student Success Studio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Colourful custom design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
  --ink: #182044;
  --muted: #66708f;
  --purple: #7357ff;
  --pink: #f35da8;
  --teal: #11bfae;
  --orange: #ffad55;
}
.stApp {
  background:
    radial-gradient(ellipse at 5% 0%, rgba(115,87,255,.16), transparent 33%),
    radial-gradient(ellipse at 95% 8%, rgba(243,93,168,.14), transparent 29%),
    linear-gradient(135deg, #f8f7ff 0%, #f2fbff 48%, #fff7f1 100%);
  color: var(--ink);
  font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"] { background: rgba(255,255,255,0); }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1450px; }
h1,h2,h3 { font-family: 'Outfit', sans-serif !important; color: #20234c !important; }
h1 { letter-spacing: -1.4px; }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #29215e 0%, #5636a6 55%, #8a49b9 100%);
}
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] label,
[data-testid="stSidebar"] [data-testid="stNumberInput"] label { color: #fff !important; }
.hero {
  padding: 30px 34px; border-radius: 28px; color: white;
  background: linear-gradient(115deg, #5636d9 0%, #8755ef 42%, #ec63b7 100%);
  box-shadow: 0 18px 50px rgba(91, 61, 190, .24);
  position: relative; overflow: hidden; margin-bottom: 22px;
}
.hero:after {
  content: "✦"; position: absolute; right: 8%; top: -34px;
  font-size: 190px; opacity: .13; transform: rotate(12deg);
}
.hero h1 { color: #fff !important; font-size: clamp(2.2rem, 4vw, 3.5rem); margin: 0 0 5px 0; }
.hero p { color: rgba(255,255,255,.9); font-size: 1.05rem; margin: 0; max-width: 700px; }
.hero-tag {
 display:inline-block; padding:6px 12px; border-radius:99px; margin-bottom:13px;
 background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.3);
 font-size:.78rem; font-weight:700; letter-spacing:.7px; text-transform:uppercase;
}
.section-kicker { color:#7859d9; font-size:.78rem; font-weight:800; letter-spacing:1.4px; text-transform:uppercase; margin-bottom:4px; }
.info-card {
 background:rgba(255,255,255,.82); border:1px solid rgba(127,109,211,.15);
 border-radius:22px; padding:20px 22px; box-shadow:0 8px 28px rgba(41,37,91,.06);
}
.stat-card {
 border-radius:22px; padding:19px 20px; color:#fff; min-height:130px;
 box-shadow:0 12px 25px rgba(43,37,90,.12);
}
.stat-card h3 { color:rgba(255,255,255,.86) !important; font-size:.92rem; margin:0; }
.stat-card .big { font-family:'Outfit',sans-serif; font-size:2.1rem; font-weight:800; margin-top:7px; line-height:1.15; }
.stat-card .small { font-size:.8rem; opacity:.9; margin-top:5px; }
.purple { background:linear-gradient(135deg,#6245e8,#9475ff); }
.pink { background:linear-gradient(135deg,#e94f9d,#ff8ab7); }
.teal { background:linear-gradient(135deg,#009f9a,#31d9bf); }
.orange { background:linear-gradient(135deg,#f18a36,#ffc16c); }
div.stButton > button {
 border:0; border-radius:14px; padding:.72rem 1.3rem; font-weight:800;
 color:white; background:linear-gradient(100deg,#6547ed,#e45da8);
 box-shadow:0 9px 20px rgba(119,73,207,.23); transition:transform .15s ease;
}
div.stButton > button:hover { color:white; transform:translateY(-2px); border:0; }
div[data-testid="stForm"] {
 background:rgba(255,255,255,.85); padding:20px; border-radius:22px;
 border:1px solid rgba(127,109,211,.17);
}
[data-testid="stMetric"] {
 background:white; border:1px solid #e8e5fa; border-radius:18px;
 padding:18px 20px; box-shadow:0 8px 22px rgba(41,37,91,.05);
}
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
 border-radius:12px !important; border-color:#dcd8f4 !important;
}
div[data-testid="stExpander"] { background:rgba(255,255,255,.75); border-radius:16px; }
.footer { text-align:center; color:#7c819d; padding:25px 0 0; font-size:.82rem; }

/* Extra motion effects */
@keyframes liftIn {
  from { opacity: 0; transform: translateY(22px) scale(.985); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes floatSparkle {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-12px) rotate(8deg); }
}
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes gentleGlow {
  0%, 100% { box-shadow: 0 18px 50px rgba(91,61,190,.22); }
  50% { box-shadow: 0 22px 62px rgba(226,84,180,.34); }
}
.hero {
  background-size: 200% 200%;
  animation: liftIn .8s cubic-bezier(.2,.8,.2,1) both,
             gradientShift 12s ease infinite,
             gentleGlow 5s ease-in-out 1s infinite;
}
.hero:after { animation: floatSparkle 6s ease-in-out infinite; }
.stat-card {
  animation: liftIn .65s cubic-bezier(.2,.8,.2,1) both;
  transition: transform .22s ease, box-shadow .22s ease, filter .22s ease;
}
.stat-card:hover {
  transform: translateY(-7px) scale(1.015);
  box-shadow: 0 20px 36px rgba(43,37,90,.19);
  filter: saturate(1.08);
}
.info-card {
  animation: liftIn .7s ease both;
  transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}
.info-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 34px rgba(41,37,91,.11);
  border-color: rgba(115,87,255,.35);
}
div.stButton > button {
  background-size: 200% 200%;
  background-image: linear-gradient(100deg,#6547ed,#e45da8,#6547ed);
  animation: gradientShift 7s ease infinite;
  transition: transform .18s ease, box-shadow .18s ease;
}
div.stButton > button:hover {
  transform: translateY(-2px) scale(1.01);
  box-shadow: 0 13px 25px rgba(119,73,207,.3);
}
[data-testid="stSidebar"] [role="radiogroup"] label {
  border-radius: 12px;
  padding: 8px 10px;
  transition: background .2s ease, transform .2s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
  background: rgba(255,255,255,.15);
  transform: translateX(4px);
}
[data-testid="stMetric"] {
  transition: transform .2s ease, box-shadow .2s ease;
}
[data-testid="stMetric"]:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 28px rgba(41,37,91,.1);
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
  }
}

</style>
""", unsafe_allow_html=True)

# -------------------- Helpers --------------------
ROOT = Path(__file__).resolve().parent

@st.cache_resource
def load_models():
    dropout_path = ROOT / "models" / "dropout_model.pkl"
    score_path = ROOT / "models" / "score_model.pkl"
    if not dropout_path.exists() or not score_path.exists():
        return None, None
    return joblib.load(dropout_path), joblib.load(score_path)

def card(title, value, subtitle, colour):
    st.markdown(
        f'<div class="stat-card {colour}"><h3>{title}</h3>'
        f'<div class="big">{value}</div><div class="small">{subtitle}</div></div>',
        unsafe_allow_html=True
    )

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("# 🎓 LearnLift")
    st.markdown("### STUDENT SUCCESS STUDIO")
    st.markdown("---")
    page = st.radio(
        "NAVIGATION",
        ["✨ Dashboard", "🔮 Predict outcome", "📘 About LearnLift"],
        label_visibility="visible"
    )
    st.markdown("---")
    st.markdown("**Your progress, made visible.**")
    st.caption("Academic insights • Performance trends • Student support")

# -------------------- Hero --------------------
st.markdown("""
<div class="hero">
  <div class="hero-tag">✦ AI-powered learning insights</div>
  <h1>Every learner can rise.</h1>
  <p>Turn student learning signals into clearer performance insights and more timely support.</p>
</div>
""", unsafe_allow_html=True)

dropout_model, score_model = load_models()

if page == "✨ Dashboard":
    st.markdown('<div class="section-kicker">YOUR OVERVIEW</div>', unsafe_allow_html=True)
    st.header("A brighter view of student success")
    st.write("Explore LearnLift's two prediction tools and understand what each estimate can—and cannot—tell you.")

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        card("PREDICTION TOOLS", "02", "Assessment score + dropout estimate", "purple")
    with c2:
        card("TRAINING DATA", "32,593", "Student records in the combined OULAD dataset", "pink")
    with c3:
        card("MODEL STATUS", "READY" if dropout_model is not None and score_model is not None else "CHECK", "Saved models detected" if dropout_model is not None and score_model is not None else "Train both models first", "teal")

    st.write("")
    left, right = st.columns([1.15, 0.85], gap="large")
    with left:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("🚀 What you can do")
        st.markdown("""
- **Predict a future assessment score** using a previous score and student details.
- **Estimate dropout risk** from the model's learned patterns.
- **Use the results as a starting point** for supportive academic conversations.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("🌈 The LearnLift approach")
        st.write("A prediction should help people ask better questions—not label a student or decide their future.")
        st.progress(0.84, text="Dropout model test accuracy: 84.32%*")
        st.caption("*Accuracy on the current random holdout split; not a guarantee of future performance.")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "🔮 Predict outcome":
    st.markdown('<div class="section-kicker">PERSONALIZED ESTIMATE</div>', unsafe_allow_html=True)
    st.header("Build a student snapshot")
    st.write("Enter the details below, then generate both estimates.")
    if dropout_model is None or score_model is None:
        st.error("A model file is missing. Ensure both models exist in the `models` folder.")
        st.code("models/dropout_model.pkl\nmodels/score_model.pkl")
        st.stop()

    # Default values are illustrative; category choices match OULAD labels.
    with st.form("student_form"):
        st.markdown("#### 🧑‍🎓 Student profile")
        a, b, c = st.columns(3)
        with a:
            gender = st.selectbox("Gender", ["M", "F"])
            region = st.selectbox("Region", [
                "East Anglian Region", "East Midlands Region", "Ireland",
                "London Region", "North Region", "North Western Region",
                "Scotland", "South East Region", "South Region",
                "South West Region", "West Midlands Region", "Wales",
                "Yorkshire Region", "Unknown"
            ])
        with b:
            education = st.selectbox("Highest education", [
                "A Level or Equivalent", "HE Qualification",
                "Lower Than A Level", "No Formal quals",
                "Post Graduate Qualification", "Unknown"
            ])
            age_band = st.selectbox("Age band", ["0-35", "35-55", "55<=", "Unknown"])
        with c:
            disability = st.selectbox("Disability", ["N", "Y"])
            imd_band = st.selectbox("IMD band", [
                "0-10%", "10-20", "10-20%", "20-30%", "30-40%",
                "40-50%", "50-60%", "60-70%", "70-80%", "80-90%",
                "90-100%", "Unknown"
            ])

        st.markdown("#### 📚 Learning activity")
        d, e, f = st.columns(3)
        with d:
            previous_score = st.slider("Previous assessment score", 0.0, 100.0, 65.0)
            attempts = st.number_input("Previous attempts", min_value=0, max_value=10, value=0)
        with e:
            credits = st.number_input("Studied credits", min_value=0, max_value=300, value=60)
            assessment_count = st.number_input("Assessment count", min_value=0, max_value=100, value=5)
        with f:
            total_clicks = st.number_input("Learning platform clicks", min_value=0, value=500)
            active_days = st.number_input("Active days", min_value=0, value=20)
        avg_clicks = st.number_input("Average clicks per active day", min_value=0.0, value=25.0)
        submitted = st.form_submit_button("✨ Generate predictions", use_container_width=True)

    if submitted:
        score_input = pd.DataFrame([{
            "previous_score": previous_score,
            "gender": gender,
            "region": region,
            "highest_education": education,
            "age_band": age_band,
            "disability": disability
        }])
        dropout_input = pd.DataFrame([{
            "gender": gender,
            "region": region,
            "highest_education": education,
            "age_band": age_band,
            "imd_band": imd_band,
            "num_of_prev_attempts": attempts,
            "studied_credits": credits,
            "disability": disability,
            "average_assessment_score": previous_score,
            "assessment_count": assessment_count,
            "total_clicks": total_clicks,
            "active_days": active_days,
            "average_clicks_per_day": avg_clicks
        }])

        try:
            predicted_score = float(score_model.predict(score_input)[0])
            predicted_score = max(0.0, min(100.0, predicted_score))
            probability = float(dropout_model.predict_proba(dropout_input)[0][1])
        except Exception as exc:
            st.error(f"Prediction could not be generated: {exc}")
            st.stop()

        risk = probability * 100
        st.markdown("---")
        st.markdown('<div class="section-kicker">YOUR RESULTS</div>', unsafe_allow_html=True)
        st.header("Student outcome snapshot")
        r1, r2, r3 = st.columns(3, gap="medium")
        with r1:
            card("PREDICTED NEXT SCORE", f"{predicted_score:.1f}/100", "Estimated assessment mark", "purple")
        with r2:
            card("DROPOUT RISK ESTIMATE", f"{risk:.1f}%", "Model-estimated probability", "pink")
        with r3:
            label = "LOW" if risk < 30 else ("MEDIUM" if risk < 60 else "HIGH")
            colour = "teal" if risk < 30 else ("orange" if risk < 60 else "pink")
            card("RISK BAND", label, "Illustrative project thresholds", colour)

        st.write("")
        st.progress(int(round(risk)), text=f"Estimated dropout probability: {risk:.1f}%")
        if risk < 30:
            st.success("Suggested next step: maintain healthy study routines and check progress regularly.")
        elif risk < 60:
            st.warning("Suggested next step: offer a supportive check-in and review workload, attendance, and assessment progress.")
        else:
            st.error("Suggested next step: arrange a timely, supportive conversation and connect the student with appropriate academic support.")
        st.caption("These are model estimates, not facts about a student. The dropout model uses retrospective data and is not validated as an early-warning system. Risk bands are illustrative, not clinical or institutional standards.")

elif page == "📘 About LearnLift":
    st.markdown('<div class="section-kicker">PROJECT GUIDE</div>', unsafe_allow_html=True)
    st.header("About LearnLift")
    st.write("LearnLift explores how historical learning data can support student performance analysis.")
    x, y = st.columns(2, gap="large")
    with x:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("📈 Assessment score")
        st.write("A linear regression pipeline estimates the next assessment score from a prior score and profile features.")
        st.markdown("</div>", unsafe_allow_html=True)
    with y:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("🫶 Dropout estimate")
        st.write("A logistic regression pipeline estimates the probability of the historical OULAD Withdrawn label from available dataset features.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("⚠️ Responsible interpretation")
    st.write("The dataset is historical and observational. The dropout model's current random split can overstate performance when related records are similar. Before real-world use, evaluate by student and by time, check calibration and subgroup performance, and validate a true early-warning cutoff. Use outputs to support—not penalize—students.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="footer">Made with 💜 for brighter learning journeys · LearnLift</div>', unsafe_allow_html=True)
