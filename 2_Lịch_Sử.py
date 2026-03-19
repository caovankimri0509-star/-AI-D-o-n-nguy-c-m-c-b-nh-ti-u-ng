import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Lịch Sử | AI Tiểu Đường", page_icon="📋", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E3A5F 100%) !important;
}
section[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
section[data-testid="stSidebar"] a {
    display:block; padding:10px 16px; border-radius:10px;
    font-weight:500; font-size:0.92em; margin:2px 0; transition:all 0.2s;
}
section[data-testid="stSidebar"] a:hover {
    background:rgba(255,255,255,0.08) !important; color:#fff !important;
}
.main { background: #F1F5F9; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1200px; }

.page-header {
    background: linear-gradient(135deg, #1E40AF, #3B82F6);
    border-radius: 18px; padding: 2rem 2.5rem; margin-bottom: 2rem;
    box-shadow: 0 16px 48px rgba(37,99,235,0.3); position:relative; overflow:hidden;
}
.page-header::after {
    content:''; position:absolute; top:-40px; right:-40px;
    width:200px; height:200px; background:rgba(255,255,255,0.05); border-radius:50%;
}
.page-header h2 { color:#fff; margin:0; font-size:1.6em; font-weight:800; }
.page-header p { color:rgba(255,255,255,0.8); margin:0.4em 0 0; font-size:0.9em; }

.kpi-row { display:flex; gap:1rem; margin-bottom:1.5rem; }
.kpi-card {
    flex:1; background:#fff; border-radius:14px; padding:1.2rem 1.4rem;
    box-shadow:0 2px 12px rgba(0,0,0,0.06); border:1px solid #E2E8F0;
    display:flex; align-items:center; gap:1rem;
}
.kpi-icon { width:44px; height:44px; border-radius:12px;
    display:flex; align-items:center; justify-content:center; font-size:1.3em; flex-shrink:0; }
.kpi-icon.blue { background:#EFF6FF; }
.kpi-icon.red { background:#FEF2F2; }
.kpi-icon.green { background:#F0FDF4; }
.kpi-icon.purple { background:#FAF5FF; }
.kpi-val { font-size:1.7em; font-weight:800; color:#0F172A; line-height:1; }
.kpi-lbl { font-size:0.78em; color:#64748B; margin-top:2px; font-weight:500; }

.filter-panel {
    background:#fff; border-radius:14px; padding:1.2rem 1.5rem;
    margin-bottom:1.2rem; box-shadow:0 2px 12px rgba(0,0,0,0.06); border:1px solid #E2E8F0;
}
.filter-title {
    font-size:0.8em; font-weight:700; text-transform:uppercase;
    letter-spacing:0.06em; color:#2563EB; margin-bottom:0.8rem;
}
.stDataFrame { border-radius:14px !important; overflow:hidden; }
.action-row { display:flex; gap:1rem; margin-top:1rem; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""<div style="padding:1.2rem 0.5rem 0.5rem; text-align:center;">
        <div style="font-size:2.5em;">🩺</div>
        <div style="font-size:1em; font-weight:700; color:#E2E8F0; margin-top:0.3em;">AI Tiểu Đường</div>
        <div style="font-size:0.7em; color:#64748B; margin-top:0.2em;">Đồ Án 1 · DH23TINxx</div>
        <hr style="border-color:rgba(255,255,255,0.08); margin:1em 0;">
    </div>""", unsafe_allow_html=True)

st.markdown("""<div class="page-header">
    <h2>📋 Lịch Sử Ứng Dụng</h2>
    <p>Xem toàn bộ lịch sử chẩn đoán nguy cơ và kết quả phân tích giấy tờ y tế</p>
</div>""", unsafe_allow_html=True)

tab_diabetes, tab_docs = st.tabs(["🩺 Chẩn Đoán Tiểu Đường", "📄 Phân Tích Giấy Tờ"])

with tab_diabetes:
    HIST = "data/history.csv"
    if not os.path.exists(HIST):
        st.info("📭 Chưa có lịch sử. Hãy thực hiện chẩn đoán đầu tiên ở trang **Chẩn Đoán**!")
    else:
        try:
            df = pd.read_csv(HIST, encoding='utf-8-sig')
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")
            st.stop()

        if df.empty:
            st.info("📭 Chưa có dữ liệu.")
        else:
            total = len(df)
            high = int((df['Kết Quả'] == 'Nguy cơ cao').sum())
            safe = total - high
            rate = round(high/total*100, 1) if total else 0

            st.markdown(f"""<div class="kpi-row">
                <div class="kpi-card"><div class="kpi-icon blue">🔬</div>
                    <div><div class="kpi-val">{total}</div><div class="kpi-lbl">Tổng lượt</div></div></div>
                <div class="kpi-card"><div class="kpi-icon red">⚠️</div>
                    <div><div class="kpi-val">{high}</div><div class="kpi-lbl">Nguy cơ cao</div></div></div>
                <div class="kpi-card"><div class="kpi-icon green">✅</div>
                    <div><div class="kpi-val">{safe}</div><div class="kpi-lbl">An toàn</div></div></div>
                <div class="kpi-card"><div class="kpi-icon purple">📈</div>
                    <div><div class="kpi-val">{rate}%</div><div class="kpi-lbl">Tỉ lệ nguy cơ</div></div></div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
            st.markdown('<div class="filter-title">🔍 Tìm Kiếm & Lọc</div>', unsafe_allow_html=True)
            fc1, fc2, fc3 = st.columns(3)
            with fc1: search = st.text_input("Tìm theo tên", placeholder="Nguyễn Văn A", label_visibility="collapsed")
            with fc2: filt = st.selectbox("Lọc kết quả", ["Tất cả", "Nguy cơ cao", "An toàn"], label_visibility="collapsed")
            with fc3: sort = st.selectbox("Sắp xếp", ["Mới nhất trước", "Cũ nhất trước"], label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

            dff = df.copy()
            if search.strip(): dff = dff[dff['Tên Bệnh Nhân'].str.contains(search.strip(), case=False, na=False)]
            if filt != "Tất cả": dff = dff[dff['Kết Quả'] == filt]
            if sort == "Mới nhất trước": dff = dff.iloc[::-1].reset_index(drop=True)

            st.caption(f"📄 Hiển thị **{len(dff)}** / {total} kết quả")

            disp_cols = [c for c in ['Thời Gian','Tên Bệnh Nhân','Mã BN','Glucose','BMI','Tuổi','Kết Quả','Xác Suất Nguy Cơ (%)'] if c in dff.columns]

            if not dff.empty:
                def style_result(val):
                    if val == "Nguy cơ cao": return 'background-color:#FEF2F2; color:#DC2626; font-weight:700'
                    if val == "An toàn": return 'background-color:#F0FDF4; color:#16A34A; font-weight:700'
                    return ''
                styled = dff[disp_cols].style.applymap(style_result, subset=['Kết Quả'])
                st.dataframe(styled, use_container_width=True, height=420)
            else:
                st.info("Không tìm thấy kết quả phù hợp.")

            st.markdown("---")
            c_dl, c_clr, _ = st.columns([1, 1, 4])
            with c_dl:
                st.download_button("📥 Tải xuống CSV",
                    data=dff.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
                    file_name="lich_su_chan_doan.csv", mime="text/csv", use_container_width=True)
            with c_clr:
                if st.button("🗑️ Xoá tất cả", key="del_diab", use_container_width=True):
                    os.remove(HIST); st.success("Đã xoá!"); st.rerun()

with tab_docs:
    DOC_HIST = "data/doc_history.csv"
    if not os.path.exists(DOC_HIST):
        st.info("📭 Chưa có lịch sử. Hãy phân tích giấy tờ y tế đầu tiên ở trang **Phân Tích Giấy Tờ**!")
    else:
        try:
            df_doc = pd.read_csv(DOC_HIST, encoding='utf-8-sig')
            
            if df_doc.empty:
                st.info("📭 Chưa có dữ liệu.")
            else:
                st.markdown(f"#### 📄 Đã phân tích **{len(df_doc)}** giấy tờ y tế")
                
                # Sắp xếp mới nhất lên đầu
                df_doc = df_doc.iloc[::-1].reset_index(drop=True)
                
                for idx, row in df_doc.iterrows():
                    with st.expander(f"🕒 {row['Thời Gian']} - 📄 {row['Tên File']}"):
                        st.markdown('<div class="result-box" style="background:#F8FAFC; padding:1.5rem; border-radius:12px; border:1px solid #E2E8F0;">', unsafe_allow_html=True)
                        st.markdown(row['Nội Dung Phân Tích'])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                st.markdown("---")
                c_dl_doc, c_clr_doc, _ = st.columns([1, 1, 4])
                with c_dl_doc:
                    st.download_button("📥 Tải xuống CSV",
                        data=df_doc.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig'),
                        file_name="lich_su_giay_to.csv", mime="text/csv", use_container_width=True)
                with c_clr_doc:
                    if st.button("🗑️ Xoá tất cả", key="del_doc", use_container_width=True):
                        os.remove(DOC_HIST); st.success("Đã xoá!"); st.rerun()

        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")
