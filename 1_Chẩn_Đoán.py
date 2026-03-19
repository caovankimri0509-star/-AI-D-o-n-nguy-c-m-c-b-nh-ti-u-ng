import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os, joblib
from datetime import datetime

st.set_page_config(page_title="Chẩn Đoán | AI Tiểu Đường", page_icon="🔬", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E3A5F 100%) !important;
}
section[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
section[data-testid="stSidebar"] a {
    display: block; padding: 10px 16px; border-radius: 10px;
    font-weight: 500; font-size: 0.92em; margin: 2px 0; transition: all 0.2s;
}
section[data-testid="stSidebar"] a:hover {
    background: rgba(255,255,255,0.08) !important; color: #fff !important;
}
.main { background: #F1F5F9; }
.block-container { padding: 2rem 2rem 2rem !important; max-width: 780px; }

/* Page Header */
.page-header {
    background: linear-gradient(135deg, #1E40AF, #3B82F6);
    border-radius: 18px; padding: 2rem 2.5rem;
    margin-bottom: 2rem; position: relative; overflow: hidden;
    box-shadow: 0 16px 48px rgba(37,99,235,0.3);
}
.page-header::after {
    content:''; position:absolute; top:-40px; right:-40px;
    width:200px; height:200px; background:rgba(255,255,255,0.05); border-radius:50%;
}
.page-header h2 { color:#fff; margin:0; font-size:1.6em; font-weight:800; }
.page-header p { color:rgba(255,255,255,0.8); margin:0.4em 0 0; font-size:0.9em; }

/* Form sections */
.form-section {
    background: #fff; border-radius: 16px; padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F0;
}
.form-section-title {
    font-size: 0.82em; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.06em; color: #2563EB; margin-bottom: 1rem;
    padding-bottom: 0.6rem; border-bottom: 2px solid #EFF6FF;
}
/* Nút phân tích */
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 1em !important; padding: 0.75em 1.5em !important;
    box-shadow: 0 8px 20px rgba(37,99,235,0.35) !important;
    transition: all 0.2s !important; width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 28px rgba(37,99,235,0.45) !important;
}

/* Result cards */
.result-card {
    border-radius: 16px; padding: 1.5rem 1.8rem; margin: 1rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.result-danger {
    background: linear-gradient(135deg, #FEF2F2, #FFF5F5);
    border: 1px solid #FECACA; border-left: 5px solid #EF4444;
}
.result-safe {
    background: linear-gradient(135deg, #F0FDF4, #F6FFFA);
    border: 1px solid #BBF7D0; border-left: 5px solid #22C55E;
}
.result-title { font-size: 1.25em; font-weight: 800; margin: 0 0 0.2em 0; }
.result-danger .result-title { color: #DC2626; }
.result-safe .result-title { color: #16A34A; }
.result-sub { font-size: 0.88em; color: #64748B; margin: 0; }

/* Probability row */
.prob-row { display: flex; gap: 1rem; margin: 1rem 0; }
.prob-box {
    flex: 1; border-radius: 14px; padding: 1rem 1.2rem;
    text-align: center; border: 1px solid;
}
.prob-box.danger { background: #FEF2F2; border-color: #FECACA; }
.prob-box.safe { background: #F0FDF4; border-color: #BBF7D0; }
.prob-pct { font-size: 2em; font-weight: 800; line-height: 1; }
.prob-box.danger .prob-pct { color: #DC2626; }
.prob-box.safe .prob-pct { color: #16A34A; }
.prob-lbl { font-size: 0.76em; color: #64748B; margin-top: 0.2em; font-weight: 500; }

/* Advice card */
.advice-card {
    background: #fff; border-radius: 14px; padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #E2E8F0;
    margin-top: 1rem;
}
.advice-title { font-size: 0.9em; font-weight: 700; color: #1E293B; margin-bottom: 0.8em; }
.advice-item { display: flex; gap: 0.7rem; padding: 0.5rem 0;
    border-bottom: 1px solid #F8FAFC; font-size: 0.85em; color: #475569; }
.advice-item:last-child { border-bottom: none; }

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0.5rem 0.5rem; text-align:center;">
        <div style="font-size:2.5em;">🩺</div>
        <div style="font-size:1em; font-weight:700; color:#E2E8F0; margin-top:0.3em;">AI Tiểu Đường</div>
        <div style="font-size:0.7em; color:#64748B; margin-top:0.2em;">Đồ Án 1 · DH23TINxx</div>
        <hr style="border-color:rgba(255,255,255,0.08); margin:1em 0;">
    </div>
    """, unsafe_allow_html=True)

# ── Load model ──
@st.cache_resource(show_spinner="⏳ Đang tải mô hình AI...")
def load_model():
    mp, sp = "model/rf_model.pkl", "model/scaler.pkl"
    if os.path.exists(mp) and os.path.exists(sp):
        return joblib.load(mp), joblib.load(sp)
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    cols = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigree','Age','Outcome']
    df = pd.read_csv(url, names=cols)
    for c in ['Glucose','BloodPressure','SkinThickness','Insulin','BMI']:
        df[c] = df[c].replace(0, df[c].median())
    features = ['Glucose','BMI','Age','BloodPressure','Insulin','DiabetesPedigree']
    X, y = df[features], df['Outcome']
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=8)
    model.fit(Xs, y)
    os.makedirs("model", exist_ok=True)
    joblib.dump(model, mp); joblib.dump(scaler, sp)
    return model, scaler

model, scaler = load_model()

# ── Header ──
st.markdown("""
<div class="page-header">
    <h2>🔬 Chẩn Đoán AI</h2>
    <p>Nhập các chỉ số sức khỏe để AI phân tích nguy cơ mắc bệnh tiểu đường</p>
</div>
""", unsafe_allow_html=True)

# ── Form ──
st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.markdown('<div class="form-section-title">👤 Thông Tin Bệnh Nhân</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1: patient_name = st.text_input("Họ và Tên *", placeholder="Nguyễn Văn A", max_chars=50)
with c2: patient_id = st.text_input("Mã Bệnh Nhân", placeholder="BN001", max_chars=20)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.markdown('<div class="form-section-title">📊 Chỉ Số Sức Khỏe</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    glucose = st.number_input("🩸 Đường huyết (mg/dL)", 40, 400, 100, help="Bình thường: 70-100 mg/dL")
    blood_pressure = st.number_input("💉 Huyết áp (mm Hg)", 30, 150, 70, help="Bình thường: 60-80 mm Hg")
with c2:
    bmi = st.number_input("⚖️ BMI (kg/m²)", 10.0, 60.0, 22.0, step=0.1, help="Bình thường: 18.5-24.9")
    insulin = st.number_input("💊 Insulin (mu U/ml)", 0, 900, 80, help="Bình thường: 16-166")
with c3:
    age = st.number_input("🎂 Tuổi", 1, 120, 25)
    dpf = st.number_input("🧬 Hệ số di truyền", 0.0, 2.5, 0.3, step=0.01, help="Xác suất di truyền tiểu đường từ gia đình")
st.markdown('</div>', unsafe_allow_html=True)

st.button("🔍  Phân Tích AI", key="analyze_btn")

if st.session_state.get("analyze_btn"):
    if not patient_name.strip():
        st.warning("⚠️ Vui lòng nhập họ tên bệnh nhân!")
    else:
        inp = np.array([[glucose, bmi, age, blood_pressure, insulin, dpf]])
        pred = model.predict(scaler.transform(inp))[0]
        proba = model.predict_proba(scaler.transform(inp))[0]
        risk_pct = round(proba[1]*100, 1)
        safe_pct = round(proba[0]*100, 1)

        st.markdown("---")
        if pred == 1:
            st.markdown(f"""<div class="result-card result-danger">
                <div class="result-title">⚠️ Nguy cơ cao mắc tiểu đường</div>
                <div class="result-sub">AI phát hiện các chỉ số của bạn ở mức báo động. Nên đến khám bác sĩ chuyên khoa.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="result-card result-safe">
                <div class="result-title">✅ Chỉ số ở mức an toàn</div>
                <div class="result-sub">Các chỉ số sức khỏe của bạn đang trong ngưỡng bình thường. Hãy duy trì lối sống lành mạnh!</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="prob-row">
            <div class="prob-box safe">
                <div class="prob-pct">{safe_pct}%</div>
                <div class="prob-lbl">🟢 Xác suất An toàn</div>
            </div>
            <div class="prob-box danger">
                <div class="prob-pct">{risk_pct}%</div>
                <div class="prob-lbl">🔴 Xác suất Nguy cơ</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(int(risk_pct), text=f"Mức nguy cơ: {risk_pct}%")

        if pred == 1:
            st.markdown("""<div class="advice-card">
                <div class="advice-title">🥗 Khuyến nghị từ AI</div>
                <div class="advice-item">🍎 <b>Chế độ ăn:</b>&nbsp; Hạn chế tinh bột trắng, đường tinh luyện. Tăng rau xanh, ngũ cốc nguyên hạt.</div>
                <div class="advice-item">🏃 <b>Vận động:</b>&nbsp; Đi bộ hoặc tập thể dục ít nhất 30 phút/ngày, 5 ngày/tuần.</div>
                <div class="advice-item">🏥 <b>Y tế:</b>&nbsp; Xét nghiệm HbA1c tại bệnh viện để có kết quả chính xác nhất.</div>
                <div class="advice-item">⚖️ <b>Cân nặng:</b>&nbsp; Duy trì BMI trong khoảng 18.5–24.9 để giảm nguy cơ.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="advice-card">
                <div class="advice-title">💡 Lời khuyên duy trì sức khỏe</div>
                <div class="advice-item">✨ <b>Duy trì:</b>&nbsp; Tiếp tục chế độ ăn uống lành mạnh và vận động đều đặn.</div>
                <div class="advice-item">📅 <b>Tái kiểm:</b>&nbsp; Kiểm tra sức khỏe định kỳ 1 năm/lần.</div>
                <div class="advice-item">💧 <b>Nước uống:</b>&nbsp; Uống đủ 2 lít nước mỗi ngày.</div>
            </div>""", unsafe_allow_html=True)
            
        # --- SO SÁNH VỚI LỊCH SỬ ---
        hp = "data/history.csv"
        if os.path.exists(hp):
            try:
                hist_df = pd.read_csv(hp, encoding='utf-8-sig')
                # Lọc theo Tên và Mã BN
                mask = (hist_df['Tên Bệnh Nhân'].str.lower() == patient_name.strip().lower())
                if patient_id.strip():
                    mask = mask & (hist_df['Mã BN'] == patient_id.strip())
                
                past = hist_df[mask]
                
                if not past.empty:
                    # Lấy lần khám gần nhất (dòng cuối cùng trong dữ liệu cũ)
                    last_record = past.iloc[-1]
                    last_time = last_record['Thời Gian']
                    last_risk = float(last_record['Xác Suất Nguy Cơ (%)'])
                    last_gluc = float(last_record['Glucose'])
                    last_bmi = float(last_record['BMI'])
                    
                    risk_diff = risk_pct - last_risk
                    gluc_diff = glucose - last_gluc
                    bmi_diff = bmi - last_bmi
                    
                    diff_color = "#16A34A" if risk_diff <= 0 else "#DC2626"
                    diff_icon = "📉 Giảm" if risk_diff <= 0 else "📈 Tăng"
                    if risk_diff == 0: diff_icon = "➖ Không đổi"
                    
                    st.markdown(f"""
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.2rem; margin-top: 1.5rem;">
                        <div style="font-weight: 700; color: #1E293B; margin-bottom: 0.5rem;">
                            🔄 So sánh với lần khám trước ({last_time})
                        </div>
                        <ul style="margin: 0; padding-left: 1.2rem; color: #475569; font-size: 0.9em; line-height: 1.6;">
                            <li><b>Xác suất nguy cơ:</b> {last_risk}% ➔ {risk_pct}% (<span style="color: {diff_color}; font-weight: 600;">{diff_icon} {abs(risk_diff):.1f}%</span>)</li>
                            <li><b>Đường huyết:</b> {last_gluc} ➔ {glucose} ({"Tăng" if gluc_diff>0 else "Giảm" if gluc_diff<0 else "Không đổi"} {abs(gluc_diff):.1f})</li>
                            <li><b>BMI:</b> {last_bmi} ➔ {bmi} ({"Tăng" if bmi_diff>0 else "Giảm" if bmi_diff<0 else "Không đổi"} {abs(bmi_diff):.1f})</li>
                        </ul>
                        <div style="margin-top: 0.8rem; font-size: 0.85em; font-style: italic; color: {diff_color};">
                            {"Mức độ nguy cơ đang giảm hoặc giữ nguyên, hãy tiếp tục duy trì thói quen tốt nhé!" if risk_diff <= 0 else "Cảnh báo: Mức độ rủi ro đang có dấu hiệu tăng lên so với lần trước. Bạn cần đặc biệt chú ý đến sức khỏe!"}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                pass

        # Lưu lịch sử
        os.makedirs("data", exist_ok=True)
        rec = {"Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
               "Tên Bệnh Nhân": patient_name.strip(),
               "Mã BN": patient_id.strip() or "N/A",
               "Glucose": glucose, "BMI": bmi, "Tuổi": age,
               "Huyết Áp": blood_pressure, "Insulin": insulin, "Di Truyền": dpf,
               "Kết Quả": "Nguy cơ cao" if pred == 1 else "An toàn",
               "Xác Suất Nguy Cơ (%)": risk_pct}
        df_r = pd.DataFrame([rec])
        hp = "data/history.csv"
        df_r.to_csv(hp, mode='a', header=not os.path.exists(hp), index=False, encoding='utf-8-sig')
        st.success("💾 Đã lưu kết quả vào lịch sử!")
