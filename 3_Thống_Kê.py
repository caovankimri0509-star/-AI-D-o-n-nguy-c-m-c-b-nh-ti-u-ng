import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os, joblib
from datetime import datetime, timedelta

st.set_page_config(page_title="Thống Kê | AI Tiểu Đường", page_icon="📊", layout="wide")

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
.page-header::after { content:''; position:absolute; top:-40px; right:-40px;
    width:200px; height:200px; background:rgba(255,255,255,0.05); border-radius:50%; }
.page-header h2 { color:#fff; margin:0; font-size:1.6em; font-weight:800; }
.page-header p { color:rgba(255,255,255,0.8); margin:0.4em 0 0; font-size:0.9em; }

.metric-row { display:flex; gap:1rem; margin-bottom:2rem; }
.metric-card {
    flex:1; background:#fff; border-radius:14px; padding:1.4rem;
    box-shadow:0 2px 12px rgba(0,0,0,0.06); border:1px solid #E2E8F0;
    text-align:center; transition:transform 0.2s;
}
.metric-card:hover { transform:translateY(-2px); box-shadow:0 8px 24px rgba(37,99,235,0.12); }
.metric-val { font-size:2.2em; font-weight:800; color:#2563EB; line-height:1; }
.metric-lbl { font-size:0.78em; color:#64748B; margin-top:0.4em; font-weight:500; }
.metric-icon { font-size:1.5em; margin-bottom:0.3em; }

.chart-card {
    background:#fff; border-radius:16px; padding:1.4rem 1.6rem;
    box-shadow:0 2px 12px rgba(0,0,0,0.06); border:1px solid #E2E8F0;
    margin-bottom:1.2rem;
}
.chart-title { font-size:0.82em; font-weight:700; text-transform:uppercase;
    letter-spacing:0.06em; color:#2563EB; margin-bottom:0.8rem;
    padding-bottom:0.5rem; border-bottom:2px solid #EFF6FF; }

.section-divider {
    font-size:0.82em; font-weight:700; text-transform:uppercase;
    letter-spacing:0.08em; color:#94A3B8; margin:1.5rem 0 1rem 0;
    display:flex; align-items:center; gap:0.8rem;
}
.section-divider::after { content:''; flex:1; height:1px; background:#E2E8F0; }

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

@st.cache_data(show_spinner="⏳ Đang tính toán thống kê mô hình...")
def get_metrics():
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    cols = ['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigree','Age','Outcome']
    df = pd.read_csv(url, names=cols)
    for c in ['Glucose','BloodPressure','SkinThickness','Insulin','BMI']:
        df[c] = df[c].replace(0, df[c].median())
    features = ['Glucose','BMI','Age','BloodPressure','Insulin','DiabetesPedigree']
    X, y = df[features], df['Outcome']
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=0.2, random_state=42)
    m = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=8)
    m.fit(Xtr, ytr)
    acc = accuracy_score(yte, m.predict(Xte))
    fi = pd.DataFrame({'Chỉ Số': features, 'Tầm Quan Trọng': m.feature_importances_})
    fi['Chỉ Số'] = fi['Chỉ Số'].map({'Glucose':'Đường huyết','BMI':'BMI','Age':'Tuổi',
        'BloodPressure':'Huyết áp','Insulin':'Insulin','DiabetesPedigree':'Di truyền'})
    fi = fi.sort_values('Tầm Quan Trọng', ascending=True)
    return acc, fi, df, len(Xtr), len(Xte)

acc, fi_df, raw_df, n_tr, n_te = get_metrics()

st.markdown("""<div class="page-header">
    <h2>📊 Thống Kê & Phân Tích</h2>
    <p>Hiệu suất mô hình AI, phân tích dữ liệu và biểu đồ trực quan</p>
</div>""", unsafe_allow_html=True)

# ── Model KPIs ──
st.markdown('<div class="metric-row">', unsafe_allow_html=True)
st.markdown(f"""<div class="metric-row">
    <div class="metric-card"><div class="metric-icon">🎯</div>
        <div class="metric-val">{acc*100:.1f}%</div><div class="metric-lbl">Độ Chính Xác</div></div>
    <div class="metric-card"><div class="metric-icon">🗂️</div>
        <div class="metric-val">768</div><div class="metric-lbl">Tổng Mẫu Dữ Liệu</div></div>
    <div class="metric-card"><div class="metric-icon">📚</div>
        <div class="metric-val">{n_tr}</div><div class="metric-lbl">Mẫu Huấn Luyện</div></div>
    <div class="metric-card"><div class="metric-icon">🧪</div>
        <div class="metric-val">{n_te}</div><div class="metric-lbl">Mẫu Kiểm Tra</div></div>
    <div class="metric-card"><div class="metric-icon">🌲</div>
        <div class="metric-val">200</div><div class="metric-lbl">Số Cây (Trees)</div></div>
</div>""", unsafe_allow_html=True)

# ── Charts row 1 ──
st.markdown('<div class="section-divider">📌 Phân Tích Mô Hình</div>', unsafe_allow_html=True)
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown('<div class="chart-card"><div class="chart-title">Mức Độ Quan Trọng Của Từng Chỉ Số</div>', unsafe_allow_html=True)
    fig_fi = px.bar(fi_df, x='Tầm Quan Trọng', y='Chỉ Số', orientation='h',
                    color='Tầm Quan Trọng', color_continuous_scale=[[0,'#BFDBFE'],[1,'#1D4ED8']],
                    text=fi_df['Tầm Quan Trọng'].apply(lambda v: f"{v:.1%}"))
    fig_fi.update_traces(textfont_size=11, textposition='outside')
    fig_fi.update_layout(showlegend=False, coloraxis_showscale=False,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(l=0,r=40,t=10,b=0),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False))
    st.plotly_chart(fig_fi, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card"><div class="chart-title">Tỉ Lệ Phân Bố Nhãn (Pima Indians)</div>', unsafe_allow_html=True)
    cnt = raw_df['Outcome'].value_counts().reset_index()
    cnt.columns = ['Kết quả','Số lượng']
    cnt['Kết quả'] = cnt['Kết quả'].map({0:'✅ An toàn',1:'⚠️ Tiểu đường'})
    fig_pie = px.pie(cnt, names='Kết quả', values='Số lượng', hole=0.52,
                     color_discrete_map={'✅ An toàn':'#22C55E','⚠️ Tiểu đường':'#EF4444'})
    fig_pie.update_traces(textposition='outside', textinfo='percent+label',
                          marker=dict(line=dict(color='white', width=3)))
    fig_pie.update_layout(showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=300, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Charts row 2 ──
st.markdown('<div class="section-divider">📈 Phân Bố Dữ Liệu Training</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2, gap="large")

with c3:
    st.markdown('<div class="chart-card"><div class="chart-title">Phân Bố Glucose Theo Kết Quả</div>', unsafe_allow_html=True)
    fig_h = px.histogram(raw_df, x='Glucose',
                         color=raw_df['Outcome'].map({0:'An toàn',1:'Tiểu đường'}),
                         nbins=30, barmode='overlay', opacity=0.8,
                         color_discrete_map={'An toàn':'#22C55E','Tiểu đường':'#EF4444'},
                         labels={'color':'','Glucose':'Đường huyết (mg/dL)','count':'Số ca'})
    fig_h.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=280, margin=dict(l=0,r=0,t=10,b=0), legend=dict(orientation='h',y=1.05))
    st.plotly_chart(fig_h, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="chart-card"><div class="chart-title">Phân Bố BMI Theo Kết Quả</div>', unsafe_allow_html=True)
    fig_b = px.box(raw_df, x=raw_df['Outcome'].map({0:'An toàn',1:'Tiểu đường'}), y='BMI',
                   color=raw_df['Outcome'].map({0:'An toàn',1:'Tiểu đường'}),
                   color_discrete_map={'An toàn':'#22C55E','Tiểu đường':'#EF4444'},
                   labels={'x':'','BMI':'BMI (kg/m²)'})
    fig_b.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        height=280, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig_b, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Lịch sử chẩn đoán ──
hp = "data/history.csv"
if os.path.exists(hp):
    try:
        dh = pd.read_csv(hp, encoding='utf-8-sig')
        if not dh.empty:
            st.markdown('<div class="section-divider">🗂️ Thống Kê Lịch Sử Hệ Thống</div>', unsafe_allow_html=True)
            c5, c6 = st.columns(2, gap="large")
            with c5:
                st.markdown('<div class="chart-card"><div class="chart-title">Phân Bố Kết Quả Đã Chẩn Đoán</div>', unsafe_allow_html=True)
                hcnt = dh['Kết Quả'].value_counts().reset_index()
                hcnt.columns = ['Kết quả','Số lượng']
                fig_hp = px.pie(hcnt, names='Kết quả', values='Số lượng', hole=0.52,
                                color_discrete_map={'Nguy cơ cao':'#EF4444','An toàn':'#22C55E'})
                fig_hp.update_traces(textposition='outside', textinfo='percent+label',
                                     marker=dict(line=dict(color='white',width=3)))
                fig_hp.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(l=0,r=0,t=10,b=0))
                st.plotly_chart(fig_hp, use_container_width=True, config={'displayModeBar':False})
                st.markdown('</div>', unsafe_allow_html=True)
            with c6:
                st.markdown('<div class="chart-card"><div class="chart-title">Scatter: Glucose vs BMI (các ca đã chẩn đoán)</div>', unsafe_allow_html=True)
                fig_s = px.scatter(dh, x='Glucose', y='BMI', color='Kết Quả',
                                   color_discrete_map={'Nguy cơ cao':'#EF4444','An toàn':'#22C55E'},
                                   hover_data=['Tên Bệnh Nhân','Tuổi'],
                                   labels={'Glucose':'Đường huyết','BMI':'BMI'})
                fig_s.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    height=280, margin=dict(l=0,r=0,t=10,b=0),
                    legend=dict(orientation='h', y=1.1))
                st.plotly_chart(fig_s, use_container_width=True, config={'displayModeBar':False})
                st.markdown('</div>', unsafe_allow_html=True)
    except: pass
else:
    st.info("💡 Thực hiện một vài ca chẩn đoán để xem thống kê lịch sử tại đây!")

# ── Lịch sử phân tích giấy tờ ──
doc_hist = "data/doc_history.csv"
if os.path.exists(doc_hist):
    try:
        ddf = pd.read_csv(doc_hist, encoding='utf-8-sig')
        if not ddf.empty:
            st.markdown('<div class="section-divider">📄 Thống Kê Phân Tích Giấy Tờ</div>', unsafe_allow_html=True)
            
            total_docs = len(ddf)
            
            c7, c8 = st.columns([1, 2], gap="large")
            with c7:
                st.markdown(f"""<div style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
                    <div class="metric-card" style="margin-bottom: 0;"><div class="metric-icon">📑</div>
                    <div class="metric-val">{total_docs}</div><div class="metric-lbl">Giấy Tờ Đã Phân Tích</div></div>
                </div>""", unsafe_allow_html=True)
            with c8:
                st.markdown('<div class="chart-card"><div class="chart-title">Phân Bố Theo Định Dạng File</div>', unsafe_allow_html=True)
                fcnt = ddf['Loại File'].value_counts().reset_index()
                fcnt.columns = ['Loại File', 'Số Lượng']
                fig_f = px.pie(fcnt, names='Loại File', values='Số Lượng', hole=0.52,
                               color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6'])
                fig_f.update_traces(textposition='outside', textinfo='percent+label',
                                    marker=dict(line=dict(color='white',width=3)))
                fig_f.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(l=0,r=0,t=10,b=0))
                st.plotly_chart(fig_f, use_container_width=True, config={'displayModeBar':False})
                st.markdown('</div>', unsafe_allow_html=True)
    except: pass

# ── Xuất Báo Cáo Định Kỳ ──
st.markdown('<div class="section-divider">📅 Xuất Báo Cáo Định Kỳ</div>', unsafe_allow_html=True)

hp_export = "data/history.csv"
if not os.path.exists(hp_export):
    st.info("💡 Chưa có dữ liệu lịch sử. Hãy thực hiện một vài ca chẩn đoán trước!")
else:
    try:
        df_exp = pd.read_csv(hp_export, encoding='utf-8-sig')
        # Parse ngày giờ linh hoạt
        df_exp['_dt'] = pd.to_datetime(df_exp['Thời Gian'], dayfirst=True, errors='coerce')
        df_exp = df_exp.dropna(subset=['_dt'])

        now = datetime.now()
        
        # UI tabs
        tab_w, tab_m, tab_y = st.tabs(["📆 Hàng Tuần", "📅 Hàng Tháng", "🕒 Hàng Năm"])
        
        def render_report(df_filtered, period_label):
            if df_filtered.empty:
                st.info(f"📭 Không có dữ liệu nào trong kỳ {period_label}.")
                return
            
            total = len(df_filtered)
            high = int((df_filtered['Kết Quả'] == 'Nguy cơ cao').sum())
            safe = total - high
            avg_gluc = df_filtered['Glucose'].mean() if 'Glucose' in df_filtered.columns else 0
            avg_bmi = df_filtered['BMI'].mean() if 'BMI' in df_filtered.columns else 0
            
            # KPI summary
            k1, k2, k3, k4, k5 = st.columns(5)
            kpi_style = 'background:#fff; border-radius:12px; padding:0.9rem 1rem; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.06); border:1px solid #E2E8F0;'
            with k1: st.markdown(f'<div style="{kpi_style}"><div style="font-size:1.5em;font-weight:800;color:#2563EB">{total}</div><div style="font-size:0.75em;color:#64748B">Tổng lượt</div></div>', unsafe_allow_html=True)
            with k2: st.markdown(f'<div style="{kpi_style}"><div style="font-size:1.5em;font-weight:800;color:#DC2626">{high}</div><div style="font-size:0.75em;color:#64748B">Nguy cơ cao</div></div>', unsafe_allow_html=True)
            with k3: st.markdown(f'<div style="{kpi_style}"><div style="font-size:1.5em;font-weight:800;color:#16A34A">{safe}</div><div style="font-size:0.75em;color:#64748B">An toàn</div></div>', unsafe_allow_html=True)
            with k4: st.markdown(f'<div style="{kpi_style}"><div style="font-size:1.5em;font-weight:800;color:#2563EB">{avg_gluc:.1f}</div><div style="font-size:0.75em;color:#64748B">Đường huyết TB</div></div>', unsafe_allow_html=True)
            with k5: st.markdown(f'<div style="{kpi_style}"><div style="font-size:1.5em;font-weight:800;color:#2563EB">{avg_bmi:.1f}</div><div style="font-size:0.75em;color:#64748B">BMI TB</div></div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Bảng dữ liệu chi tiết
            disp = [c for c in ['Thời Gian','Tên Bệnh Nhân','Mã BN','Glucose','BMI','Tuổi','Kết Quả','Xác Suất Nguy Cơ (%)'] if c in df_filtered.columns]
            def _style(val):
                if val == "Nguy cơ cao": return 'background-color:#FEF2F2; color:#DC2626; font-weight:700'
                if val == "An toàn": return 'background-color:#F0FDF4; color:#16A34A; font-weight:700'
                return ''
            df_show = df_filtered[disp].sort_values('Thời Gian', ascending=False) if 'Thời Gian' in disp else df_filtered[disp]
            st.dataframe(df_show.style.applymap(_style, subset=['Kết Quả']), use_container_width=True, height=300)
            
            # Nút tải xuống
            csv_data = df_filtered[disp].to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
            fname = f"bao_cao_{period_label.lower().replace(' ','_')}_{now.strftime('%Y%m%d')}.csv"
            st.download_button(
                label=f"📥 Tải xuống Báo Cáo {period_label} (CSV)",
                data=csv_data, file_name=fname, mime='text/csv',
                use_container_width=True,
            )
        
        with tab_w:
            start_w = now - timedelta(days=now.weekday())  # Đầu tuần này (Thứ 2)
            start_w = start_w.replace(hour=0, minute=0, second=0, microsecond=0)
            df_w = df_exp[df_exp['_dt'] >= start_w].drop(columns=['_dt'])
            st.caption(f"📆 Từ **{start_w.strftime('%d/%m/%Y')}** đến **{now.strftime('%d/%m/%Y')}**")
            render_report(df_w, f"Tuần {now.isocalendar()[1]:02d}/{now.year}")
        
        with tab_m:
            start_m = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            df_m = df_exp[df_exp['_dt'] >= start_m].drop(columns=['_dt'])
            mon_name = now.strftime("%B %Y")
            st.caption(f"📅 Tháng **{now.month}/{now.year}**")
            render_report(df_m, f"Thang_{now.month:02d}_{now.year}")
        
        with tab_y:
            start_y = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            df_y = df_exp[df_exp['_dt'] >= start_y].drop(columns=['_dt'])
            st.caption(f"🕒 Năm **{now.year}**")
            render_report(df_y, f"Nam_{now.year}")
    
    except Exception as e:
        st.error(f"Lỗi đọc dữ liệu: {e}")
