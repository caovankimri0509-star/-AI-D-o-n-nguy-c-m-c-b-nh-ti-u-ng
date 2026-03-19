import streamlit as st
import requests
import json

st.set_page_config(page_title="Trợ Lý AI | AI Tiểu Đường", page_icon="🤖", layout="centered")

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
.block-container { padding: 1.5rem 2rem !important; max-width: 860px; }

.page-header {
    background: linear-gradient(135deg, #1E40AF, #3B82F6);
    border-radius: 18px; padding: 1.8rem 2.5rem; margin-bottom: 1.5rem;
    box-shadow: 0 16px 48px rgba(37,99,235,0.3); position:relative; overflow:hidden;
}
.page-header::after {
    content:''; position:absolute; top:-40px; right:-40px;
    width:200px; height:200px; background:rgba(255,255,255,0.05); border-radius:50%;
}
.page-header h2 { color:#fff; margin:0; font-size:1.5em; font-weight:800; }
.page-header p { color:rgba(255,255,255,0.82); margin:0.4em 0 0; font-size:0.88em; }

[data-testid="stChatMessage"] {
    background: #fff !important;
    border-radius: 14px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.5rem !important;
}

[data-testid="stChatInput"] textarea {
    border-radius: 12px !important;
    border: 2px solid #BFDBFE !important;
    font-size: 0.9em !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
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
    st.markdown("""<div style="padding:1.2rem 0.5rem 0.5rem; text-align:center;">
        <div style="font-size:2.5em;">🩺</div>
        <div style="font-size:1em; font-weight:700; color:#E2E8F0; margin-top:0.3em;">AI Tiểu Đường</div>
        <div style="font-size:0.7em; color:#64748B; margin-top:0.2em;">Đồ Án 1 · DH23TINxx</div>
        <hr style="border-color:rgba(255,255,255,0.08); margin:1em 0;">
    </div>""", unsafe_allow_html=True)

    st.markdown("### ⚙️ Cài đặt AI")
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
    st.markdown("---")
    if st.button("🗑️ Xoá lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Header ──
st.markdown("""<div class="page-header">
    <h2>🤖 Trợ Lý AI Y Tế</h2>
    <p>Hỏi đáp trực tiếp về bệnh tiểu đường, dinh dưỡng, chỉ số sức khỏe với bác sĩ AI 24/7</p>
</div>""", unsafe_allow_html=True)

# ── System prompt ──
SYSTEM_PROMPT = """Bạn là một bác sĩ AI chuyên nghiệp, tận tâm và am hiểu sâu rộng về:
- Bệnh tiểu đường (Diabetes) loại 1, loại 2 và tiền tiểu đường
- Dinh dưỡng và chế độ ăn uống phù hợp cho người tiểu đường
- Các chỉ số y tế: Glucose, HbA1c, BMI, Insulin, Huyết áp
- Cách đọc và hiểu kết quả xét nghiệm máu
- Lối sống và vận động dành cho người có nguy cơ tiểu đường

Nhiệm vụ của bạn là:
1. Giải đáp thắc mắc của bệnh nhân bằng tiếng Việt, rõ ràng và dễ hiểu
2. Sử dụng ngôn ngữ thân thiện, đồng cảm, không dùng thuật ngữ khó hiểu quá mức
3. Luôn nhấn mạnh rằng bạn là AI và khuyến nghị người dùng đến gặp bác sĩ thật khi cần
4. Trình bày có cấu trúc, dùng emoji để tăng tính thân thiện
5. Không bao giờ kê đơn thuốc cụ thể"""

# ── Gợi ý câu hỏi ──
SUGGESTIONS = [
    "Chỉ số glucose bao nhiêu là nguy hiểm?",
    "Người tiểu đường ăn gì tốt?",
    "BMI 28 có nguy cơ không?",
    "HbA1c là gì?",
    "Cách phòng ngừa tiểu đường type 2?",
]

# ── Khởi tạo session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Câu hỏi gợi ý ──
if len(st.session_state.messages) == 0:
    st.markdown("**💡 Bạn có thể hỏi ngay:**")
    cols = st.columns(len(SUGGESTIONS))
    for i, sug in enumerate(SUGGESTIONS):
        with cols[i]:
            if st.button(sug, key=f"sug_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": sug})
                st.rerun()

# ── Hiển thị lịch sử chat ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🩺"):
        st.markdown(msg["content"])

# ── Xử lý input người dùng ──
prompt = st.chat_input("Hỏi bác sĩ AI bất kỳ câu hỏi nào về sức khỏe, tiểu đường...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🩺"):
        if not user_api_key:
            st.error("⚠️ Vui lòng nhập OpenRouter API Key ở thanh bên trái!\n\n🔗 Website: https://openrouter.ai/")
        else:
            with st.spinner("🤔 Đang suy nghĩ..."):
                try:
                    # Chuẩn bị messages gồm system prompt và lịch sử
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    messages.extend(st.session_state.messages)

                    # Gọi OpenRouter API
                    response = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {user_api_key}",
                            "Content-Type": "application/json",
                        },
                        data=json.dumps({
                            "model": "google/gemini-2.0-flash-001", # Hoặc model khác
                            "messages": messages
                        })
                    )
                    
                    if response.status_code != 200:
                        raise Exception(f"Lỗi API ({response.status_code}): {response.text}")
                    
                    result_json = response.json()
                    reply = result_json['choices'][0]['message']['content']

                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

                except Exception as e:
                    err_str = str(e)
                    if "401" in err_str or "unauthorized" in err_str.lower():
                        err_msg = "❌ API Key không hợp lệ! Hãy kiểm tra lại tại: https://openrouter.ai/keys"
                    elif "429" in err_str:
                        err_msg = "❌ Đã hết hạn mức/Số dư tài khoản OpenRouter."
                    else:
                        err_msg = f"❌ Lỗi khi gọi AI: {e}"
                    st.error(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})
