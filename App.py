import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="AI Chẩn Đoán Tiểu Đường",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E3A5F 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
section[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
section[data-testid="stSidebar"] a {
    display: block; padding: 10px 16px; border-radius: 10px;
    font-weight: 500; font-size: 0.92em; margin: 2px 0;
    transition: all 0.2s ease;
}
section[data-testid="stSidebar"] a:hover {
    background: rgba(255,255,255,0.08) !important;
    color: #fff !important; padding-left: 22px;
}
section[data-testid="stSidebar"] .stImage { text-align: center; padding: 1em 0; }

/* ── Main background ── */
.main { background: #F1F5F9; }
.block-container { padding: 2rem 2.5rem 2rem !important; max-width: 1200px; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1E40AF 0%, #2563EB 50%, #3B82F6 100%);
    border-radius: 20px;
    padding: 3rem 3.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(37,99,235,0.35);
}
.hero-banner::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute; bottom: -80px; right: 120px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.2em; font-weight: 800; color: #fff;
    margin: 0 0 0.4em 0; line-height: 1.2;
}
.hero-sub {
    font-size: 1em; color: rgba(255,255,255,0.82);
    margin: 0; font-weight: 400; line-height: 1.6;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    color: #fff; border-radius: 30px;
    padding: 5px 16px; font-size: 0.78em;
    font-weight: 600; margin-top: 1rem;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(4px);
}

/* ── Stat Cards ── */
.stat-row { display: flex; gap: 1.2rem; margin-bottom: 2rem; }
.stat-card {
    flex: 1; background: #fff;
    border-radius: 16px; padding: 1.4rem 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #E8EEFE;
    display: flex; align-items: center; gap: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(37,99,235,0.12); }
.stat-icon {
    width: 52px; height: 52px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5em; flex-shrink: 0;
}
.icon-blue { background: #EFF6FF; }
.icon-red { background: #FEF2F2; }
.icon-green { background: #F0FDF4; }
.stat-val { font-size: 1.9em; font-weight: 800; color: #0F172A; line-height: 1; }
.stat-lbl { font-size: 0.82em; color: #64748B; margin-top: 2px; font-weight: 500; }

/* ── Section Cards ── */
.info-card {
    background: #fff; border-radius: 16px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #E8EEFE; height: 100%;
}
.info-card h3 { font-size: 1em; font-weight: 700; color: #1E293B; margin: 0 0 1.2em 0; }
.feature-item {
    display: flex; gap: 0.8rem; align-items: flex-start;
    padding: 0.7rem 0; border-bottom: 1px solid #F1F5F9;
}
.feature-item:last-child { border-bottom: none; }
.feature-dot {
    width: 36px; height: 36px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 1em;
}
.feature-dot.blue { background: #EFF6FF; }
.feature-dot.purple { background: #FAF5FF; }
.feature-dot.orange { background: #FFF7ED; }
.feature-dot.green { background: #F0FDF4; }
.feature-name { font-weight: 600; font-size: 0.88em; color: #1E293B; }
.feature-desc { font-size: 0.78em; color: #64748B; margin-top: 1px; line-height: 1.5; }
.step-item {
    display: flex; gap: 1rem; align-items: center;
    padding: 0.75rem 0; border-bottom: 1px solid #F1F5F9;
}
.step-item:last-child { border-bottom: none; }
.step-num {
    width: 32px; height: 32px; border-radius: 50%;
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    color: #fff; font-weight: 700; font-size: 0.85em;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(37,99,235,0.3);
}
.step-title { font-weight: 600; font-size: 0.88em; color: #1E293B; }
.step-sub { font-size: 0.76em; color: #94A3B8; margin-top: 1px; }
.footer-note {
    background: #FFF7ED; border: 1px solid #FED7AA;
    border-radius: 12px; padding: 0.9rem 1.2rem;
    display: flex; gap: 0.7rem; align-items: flex-start; margin-top: 1.5rem;
    font-size: 0.8em; color: #92400E; line-height: 1.5;
}

/* ── Ẩn streamlit mặc định ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar logo ──
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0.5rem 0.5rem 0.5rem; text-align:center;">
        <div style="font-size:2.5em;">🩺</div>
        <div style="font-size:1em; font-weight:700; color:#E2E8F0; margin-top:0.3em;">AI Tiểu Đường</div>
        <div style="font-size:0.7em; color:#64748B; margin-top:0.2em;">Đồ Án 1 · DH23TINxx</div>
        <hr style="border-color:rgba(255,255,255,0.08); margin:1em 0;">
    </div>
    """, unsafe_allow_html=True)

# ── Đọc lịch sử ──
hist_path = "data/history.csv"
total, high_risk, safe_count = 0, 0, 0
if os.path.exists(hist_path):
    try:
        dh = pd.read_csv(hist_path, encoding='utf-8-sig')
        total = len(dh)
        high_risk = int((dh['Kết Quả'] == 'Nguy cơ cao').sum())
        safe_count = total - high_risk
    except: pass

# ── Hero ──
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title">🩺 Hệ Thống AI Chẩn Đoán Tiểu Đường</div>
    <div class="hero-sub">
        Ứng dụng trí tuệ nhân tạo hỗ trợ phát hiện sớm nguy cơ mắc bệnh tiểu đường<br>
        dựa trên mô hình Random Forest được huấn luyện với dữ liệu y tế thực tế.
    </div>
    <div class="hero-badge">Đồ Án 1 &nbsp;·&nbsp; Cơ Sở CNTT &nbsp;·&nbsp; DH23TINxx &nbsp;·&nbsp; HK2 2025-2026</div>
</div>
""", unsafe_allow_html=True)

# ── Stats ──
st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <div class="stat-icon icon-blue">🔬</div>
        <div>
            <div class="stat-val">{total}</div>
            <div class="stat-lbl">Tổng lượt chẩn đoán</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon icon-red">⚠️</div>
        <div>
            <div class="stat-val">{high_risk}</div>
            <div class="stat-lbl">Ca nguy cơ cao</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon icon-green">✅</div>
        <div>
            <div class="stat-val">{safe_count}</div>
            <div class="stat-lbl">Ca an toàn</div>
        </div>
    </div>
    <div class="stat-card">
        <div class="stat-icon icon-blue">🎯</div>
        <div>
            <div class="stat-val">76.6%</div>
            <div class="stat-lbl">Độ chính xác AI</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tính năng + Hướng dẫn ──
col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("""
    <div class="info-card">
        <h3>🚀 Tính Năng Hệ Thống</h3>
        <div class="feature-item">
            <div class="feature-dot blue">🤖</div>
            <div>
                <div class="feature-name">AI Chẩn Đoán Thông Minh</div>
                <div class="feature-desc">Random Forest huấn luyện với 768 mẫu thật từ Pima Indians Dataset. Độ chính xác 76.6%.</div>
            </div>
        </div>
        <div class="feature-item">
            <div class="feature-dot purple">📋</div>
            <div>
                <div class="feature-name">Lưu Lịch Sử Chẩn Đoán</div>
                <div class="feature-desc">Mỗi ca được lưu lại kèm thông tin bệnh nhân, có thể tìm kiếm và xuất CSV.</div>
            </div>
        </div>
        <div class="feature-item">
            <div class="feature-dot orange">📊</div>
            <div>
                <div class="feature-name">Thống Kê & Biểu Đồ</div>
                <div class="feature-desc">Visualize độ chính xác model, feature importance và phân bố dữ liệu.</div>
            </div>
        </div>
        <div class="feature-item">
            <div class="feature-dot green">💾</div>
            <div>
                <div class="feature-name">Xuất Dữ Liệu</div>
                <div class="feature-desc">Tải toàn bộ lịch sử về máy định dạng CSV.</div>
            </div>
        </div>
        <div class="feature-item">
            <div class="feature-dot" style="background: #FEF2F2;">📄</div>
            <div>
                <div class="feature-name">AI Phân Tích Giấy Tờ (Mới)</div>
                <div class="feature-desc">Tải lên kết quả xét nghiệm/đơn thuốc bệnh viện, AI sẽ đọc và giải thích.</div>
            </div>
        </div>
        <div class="feature-item">
            <div class="feature-dot" style="background: #F0FDF4;">💬</div>
            <div>
                <div class="feature-name">Trợ Lý AI Hỏi Đáp (Mới)</div>
                <div class="feature-desc">Chat trực tiếp với Bác sĩ AI để hỏi về tiểu đường, dinh dưỡng và chỉ số sức khỏe.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>📖 Hướng Dẫn Sử Dụng</h3>
        <div class="step-item">
            <div class="step-num">1</div>
            <div>
                <div class="step-title">Chọn trang Chẩn Đoán</div>
                <div class="step-sub">Click vào "Chẩn Đoán" ở thanh menu trái</div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">2</div>
            <div>
                <div class="step-title">Nhập thông tin bệnh nhân</div>
                <div class="step-sub">Họ tên, mã BN và các chỉ số sức khỏe</div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">3</div>
            <div>
                <div class="step-title">Nhấn "Phân Tích AI"</div>
                <div class="step-sub">Kết quả hiện ngay kèm xác suất và tư vấn</div>
            </div>
        </div>
        <div class="step-item">
            <div class="step-num">4</div>
            <div>
                <div class="step-title">Xem Lịch Sử & Thống Kê</div>
                <div class="step-sub">Theo dõi tất cả ca đã chẩn đoán</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-note">
    ⚠️ <div><b>Lưu ý quan trọng:</b> Ứng dụng này chỉ mang tính chất tham khảo và học tập, 
    không thay thế cho việc thăm khám bác sĩ chuyên khoa. Khi có dấu hiệu bất thường, 
    hãy đến cơ sở y tế để được tư vấn chính xác.</div>
</div>
""", unsafe_allow_html=True)