import streamlit as st
import base64
import os
import pandas as pd
from datetime import datetime
from PIL import Image
import io
import requests
import json

st.set_page_config(page_title="Phân Tích Giấy Tờ | AI Tiểu Đường", page_icon="📄", layout="centered")

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
.block-container { padding: 2rem 2rem 2rem !important; max-width: 850px; }

.page-header {
    background: linear-gradient(135deg, #1E40AF, #3B82F6);
    border-radius: 18px; padding: 2rem 2.5rem;
    margin-bottom: 2rem; position: relative; overflow: hidden;
    box-shadow: 0 16px 48px rgba(37,99,235,0.3);
}
.page-header h2 { color:#fff; margin:0; font-size:1.6em; font-weight:800; }
.page-header p { color:rgba(255,255,255,0.8); margin:0.4em 0 0; font-size:0.9em; }

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

.result-box {
    background: #fff; border-radius: 16px; padding: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 1px solid #E2E8F0;
    margin-top: 2rem; line-height: 1.7; color: #1E293B;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Lấy API Key từ secrets hoặc nhập thủ công ──
default_key = ""
try:
    default_key = st.secrets.get("OPENROUTER_API_KEY", "")
except Exception:
    pass

with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0.5rem 0.5rem; text-align:center;">
        <div style="font-size:2.5em;">🩺</div>
        <div style="font-size:1em; font-weight:700; color:#E2E8F0; margin-top:0.3em;">AI Tiểu Đường</div>
        <div style="font-size:0.7em; color:#64748B; margin-top:0.2em;">Đồ Án 1 · DH23TINxx</div>
        <hr style="border-color:rgba(255,255,255,0.08); margin:1em 0;">
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🔑 Cài đặt AI")
    user_api_key = st.text_input(
        "OpenRouter API Key",
        value=default_key,
        type="password",
        help="Lấy tại: https://openrouter.ai/keys"
    )
    st.markdown(
        '<div style="font-size:0.75em; color:#64748B; margin-top:0.3em;">'
        '🔗 <a href="https://openrouter.ai/keys" target="_blank" style="color:#60A5FA;">Lấy API Key tại OpenRouter</a>'
        '</div>', unsafe_allow_html=True
    )

# Header
st.markdown("""
<div class="page-header">
    <h2>📄 Phân Tích Giấy Tờ Y Tế bằng AI</h2>
    <p>Tải lên hình ảnh giấy tờ khám bệnh (kết quả xét nghiệm, đơn thuốc, v.v.), AI sẽ đọc, giải thích chuẩn đoán và đưa ra giải pháp.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-section">', unsafe_allow_html=True)
st.markdown('<div class="form-section-title">📸 Tải Lên Hình Ảnh Giấy Tờ</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Chọn ảnh từ điện thoại/máy tính (JPG, PNG)", type=["jpg", "jpeg", "png", "webp"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    st.image(uploaded_file, caption="Ảnh giấy tờ y tế", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍 Tiến Hành Đọc và Phân Tích"):
        if not user_api_key:
            st.error("⚠️ Vui lòng nhập OpenRouter API Key ở thanh bên (Sidebar).\n\n🔗 Website: https://openrouter.ai/")
        else:
            try:
                with st.spinner("⏳ AI đang đọc ảnh... Vui lòng đợi trong giây lát..."):
                    # Đọc ảnh và encode base64
                    img_bytes = uploaded_file.getvalue()
                    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                    img_type = "image/jpeg"
                    if uploaded_file.name.lower().endswith("png"): img_type = "image/png"
                    elif uploaded_file.name.lower().endswith("webp"): img_type = "image/webp"

                    prompt = '''Bạn là một bác sĩ AI chuyên nghiệp, tận tâm và có chuyên môn cao, được giao nhiệm vụ phân tích giấy tờ y tế cho bệnh nhân.
Dựa vào hình ảnh giấy tờ y tế được tải lên, hãy đọc kỹ hình ảnh và phân tích thông tin theo cấu trúc sau một cách rõ ràng, dễ hiểu bằng tiếng Việt:

---
### 📋 1. Loại Giấy Tờ
(Xác định rõ đây là loại giấy tờ gì: Kết quả xét nghiệm, Đơn thuốc, Phiếu siêu âm, Sổ khám bệnh, v.v. Nếu trong đó có tên cơ sở y tế thì ghi ra)

### 🔬 2. Giải Thích Các Chỉ Số / Nội Dung Chính
(Đọc và liệt kê các chỉ số quan trọng, kết quả đo được. Nếu có mức tham chiếu / mức bình thường trong ảnh thì ghi luôn. ĐỒNG THỜI giải thích ý nghĩa của chỉ số đó đối với sức khỏe.)
- **[Tên chỉ số/Thuốc]**: [Giá trị/Kết quả] 
  👉 *Ý nghĩa:* [Giải thích ngắn gọn ý nghĩa của chỉ số này cho sức khoẻ]

### 🏥 3. Nhận Xét & Đánh Giá Tổng Quan
(Dựa trên các chỉ số/thông tin trên, hãy đưa ra một đánh giá tổng quan về sức khỏe theo ngôn ngữ bình dân dễ hiểu. Người đó có mắc bệnh gì không?)

### 💊 4. Giải Pháp / Lời Khuyên
(Chỉ định các phương pháp cải thiện tình trạng thực tế phù hợp với nhận xét bên trên. Chế độ ăn uống, sinh hoạt, hoặc lịch tái khám. Luôn nhắc tham khảo ý kiến bác sĩ chuyên khoa.)
---
Lưu ý: Viết bằng giọng văn đồng cảm, trình bày đẹp bằng Markdown, dùng các icon emoji thân thiện.'''

                    # Gọi OpenRouter API
                    response = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {user_api_key}",
                            "Content-Type": "application/json",
                        },
                        data=json.dumps({
                            "model": "google/gemini-2.0-flash-001",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": prompt},
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": f"data:{img_type};base64,{img_base64}"
                                            }
                                        }
                                    ]
                                }
                            ]
                        })
                    )
                    
                    if response.status_code != 200:
                        raise Exception(f"Lỗi API ({response.status_code}): {response.text}")
                    
                    result_json = response.json()
                    result_text = result_json['choices'][0]['message']['content']

                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(result_text)
                st.markdown('</div>', unsafe_allow_html=True)

                # --- LƯU LỊCH SỬ PHÂN TÍCH ---
                try:
                    os.makedirs("data", exist_ok=True)
                    doc_hist_path = "data/doc_history.csv"
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_record = pd.DataFrame([{
                        "Thời Gian": now_str,
                        "Tên File": uploaded_file.name,
                        "Loại File": img_type,
                        "Nội Dung Phân Tích": result_text
                    }])
                    if os.path.exists(doc_hist_path):
                        df = pd.read_csv(doc_hist_path, encoding='utf-8-sig')
                        df = pd.concat([df, new_record], ignore_index=True)
                    else:
                        df = new_record
                    df.to_csv(doc_hist_path, index=False, encoding='utf-8-sig')
                    st.toast("✅ Đã lưu kết quả phân tích vào lịch sử!", icon="💾")
                except Exception as e_save:
                    st.warning(f"Không thể lưu lịch sử: {e_save}")

            except Exception as e:
                err_str = str(e)
                if "401" in err_str or "unauthorized" in err_str.lower():
                    st.error("❌ API Key không hợp lệ! Hãy kiểm tra lại tại: https://openrouter.ai/keys")
                elif "429" in err_str:
                    st.error("❌ Đã hết hạn mức/Số dư tài khoản. Vui lòng kiểm tra lại tài khoản OpenRouter.")
                else:
                    st.error(f"❌ Có lỗi xảy ra: {e}")
                st.info("💡 Lấy API Key tại: https://openrouter.ai/keys")
