"""
GPT-Style All-in-One Chat Bar
TRUE single unified frame - all controls inside ONE visual container
"""
import streamlit as st
import base64
import tempfile
import os

# Available models for each provider
AVAILABLE_MODELS = {
    "ollama": ["llama3.2", "llama3.1", "llama3", "mistral", "codellama", "phi3"],
    "gemini": ["gemini-1.5-pro-latest", "gemini-1.5-flash", "gemini-pro"],
    "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
}


def get_file_content(uploaded_file):
    """Extract content from uploaded file"""
    if uploaded_file is None:
        return None
    
    file_type = uploaded_file.type
    file_name = uploaded_file.name
    
    try:
        if file_type in ["text/plain", "text/markdown", "text/csv", "application/json"]:
            content = uploaded_file.read().decode("utf-8")
            return {"type": "text", "name": file_name, "content": content}
        elif file_type == "application/pdf":
            try:
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return {"type": "pdf", "name": file_name, "content": text}
            except ImportError:
                return {"type": "pdf", "name": file_name, "content": "[PDF - install PyPDF2]"}
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            try:
                import docx
                doc = docx.Document(uploaded_file)
                text = "\n".join([para.text for para in doc.paragraphs])
                return {"type": "docx", "name": file_name, "content": text}
            except ImportError:
                return {"type": "docx", "name": file_name, "content": "[DOCX - install python-docx]"}
        elif file_type.startswith("image/"):
            image_data = base64.b64encode(uploaded_file.read()).decode()
            return {"type": "image", "name": file_name, "content": image_data, "mime_type": file_type}
        else:
            return {"type": "unknown", "name": file_name, "content": f"[Unsupported: {file_type}]"}
    except Exception as e:
        return {"type": "error", "name": file_name, "content": f"[Error: {str(e)}]"}


def transcribe_audio(audio_bytes):
    """Transcribe audio using speech recognition"""
    try:
        import speech_recognition as sr
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio = recognizer.record(source)
        os.unlink(tmp_path)
        try:
            return recognizer.recognize_google(audio)
        except:
            return None
    except:
        return None


def unified_chat_input():
    """GPT-Style unified chat bar - TRUE single container with all controls"""
    
    # Initialize states
    if "attached_file" not in st.session_state:
        st.session_state.attached_file = None
    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""
    if "last_file_id" not in st.session_state:
        st.session_state.last_file_id = None
    if "last_audio_id" not in st.session_state:
        st.session_state.last_audio_id = None
    if "input_key" not in st.session_state:
        st.session_state.input_key = 0
    
    # Get current model
    current_provider = st.session_state.get("current_provider", "ollama")
    available_models = AVAILABLE_MODELS.get(current_provider, ["default"])
    current_model = st.session_state.get("current_model_name", available_models[0])
    
    # ===== CRITICAL CSS: Make st.container look like ONE unified chat bar =====
    st.markdown("""
    <style>
    /* ===== GPT-STYLE UNIFIED CHAT BAR ===== */
    /* Target the container that wraps our chat bar */
    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stVerticalBlockBorderWrapper"] > div > div[data-testid="stVerticalBlock"] > div.unified-chatbar-marker) {
        background: #2f2f2f !important;
        border: 1px solid #424242 !important;
        border-radius: 26px !important;
        padding: 12px 16px !important;
        margin: 10px 0 20px 0 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* The actual unified bar container */
    .unified-bar-container {
        background: #2f2f2f;
        border: 1px solid #424242;
        border-radius: 26px;
        padding: 12px 16px;
        margin: 10px auto 20px auto;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        max-width: 100%;
    }
    
    /* Remove all gaps inside the unified bar */
    .unified-bar-container [data-testid="stVerticalBlock"] {
        gap: 8px !important;
    }
    
    .unified-bar-container [data-testid="stHorizontalBlock"] {
        gap: 0 !important;
        align-items: center !important;
    }
    
    .unified-bar-container .stColumn {
        padding: 0 4px !important;
    }
    
    /* Attachment preview chip */
    .attachment-chip {
        background: #3a3a3a;
        border-radius: 16px;
        padding: 6px 12px;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #e0e0e0;
        margin-bottom: 8px;
    }
    
    .attachment-chip .remove-btn {
        background: none;
        border: none;
        color: #888;
        cursor: pointer;
        padding: 0 4px;
        font-size: 14px;
    }
    
    .attachment-chip .remove-btn:hover {
        color: #ff6b6b;
    }
    
    /* File uploader as icon button */
    .unified-bar-container [data-testid="stFileUploader"] {
        width: 40px !important;
    }
    
    .unified-bar-container [data-testid="stFileUploader"] > div {
        padding: 0 !important;
        background: transparent !important;
    }
    
    .unified-bar-container [data-testid="stFileUploader"] section {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    
    .unified-bar-container [data-testid="stFileUploader"] section > div:first-child {
        display: none !important;
    }
    
    .unified-bar-container [data-testid="stFileUploader"] button {
        background: #424242 !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        color: #b0b0b0 !important;
        transition: all 0.2s !important;
    }
    
    .unified-bar-container [data-testid="stFileUploader"] button:hover {
        background: #525252 !important;
        color: white !important;
    }
    
    .unified-bar-container [data-testid="stFileUploader"] label {
        display: none !important;
    }
    
    /* Model selector as compact pill */
    .unified-bar-container [data-testid="stSelectbox"] {
        min-width: 120px !important;
        max-width: 140px !important;
    }
    
    .unified-bar-container [data-testid="stSelectbox"] > div {
        background: transparent !important;
    }
    
    .unified-bar-container [data-testid="stSelectbox"] > div > div {
        background: #424242 !important;
        border: none !important;
        border-radius: 20px !important;
        min-height: 38px !important;
        color: #e0e0e0 !important;
        font-size: 13px !important;
        padding: 0 12px !important;
    }
    
    .unified-bar-container [data-testid="stSelectbox"] label {
        display: none !important;
    }
    
    /* Text input - clean, borderless */
    .unified-bar-container [data-testid="stTextInput"] > div {
        background: transparent !important;
    }
    
    .unified-bar-container [data-testid="stTextInput"] input {
        background: transparent !important;
        border: none !important;
        color: white !important;
        font-size: 16px !important;
        padding: 10px 8px !important;
        caret-color: #667eea !important;
    }
    
    .unified-bar-container [data-testid="stTextInput"] input::placeholder {
        color: #707070 !important;
    }
    
    .unified-bar-container [data-testid="stTextInput"] input:focus {
        box-shadow: none !important;
        outline: none !important;
    }
    
    .unified-bar-container [data-testid="stTextInput"] label {
        display: none !important;
    }
    
    /* Audio input as icon button */
    .unified-bar-container [data-testid="stAudioInput"] {
        width: 40px !important;
    }
    
    .unified-bar-container [data-testid="stAudioInput"] > div {
        background: transparent !important;
        padding: 0 !important;
    }
    
    .unified-bar-container [data-testid="stAudioInput"] button {
        background: #424242 !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        transition: all 0.2s !important;
    }
    
    .unified-bar-container [data-testid="stAudioInput"] button:hover {
        background: #525252 !important;
    }
    
    .unified-bar-container [data-testid="stAudioInput"] label {
        display: none !important;
    }
    
    /* Send button - gradient accent */
    .unified-bar-container [data-testid="stButton"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        min-height: 40px !important;
        padding: 0 !important;
        color: white !important;
        font-size: 18px !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.4) !important;
    }
    
    .unified-bar-container [data-testid="stButton"] button:hover {
        transform: scale(1.08) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Remove button styling */
    .remove-attachment-btn button {
        background: transparent !important;
        border: none !important;
        color: #888 !important;
        padding: 2px 6px !important;
        min-height: auto !important;
        height: auto !important;
        width: auto !important;
        font-size: 14px !important;
        box-shadow: none !important;
    }
    
    .remove-attachment-btn button:hover {
        color: #ff6b6b !important;
        background: transparent !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    /* Hide any extra padding/margins */
    .unified-bar-container .element-container {
        margin: 0 !important;
    }
    
    .unified-bar-container [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0 !important;
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ========== THE UNIFIED CHAT BAR ==========
    # Use HTML wrapper + st.container for TRUE visual unity
    
    st.markdown('<div class="unified-bar-container">', unsafe_allow_html=True)
    
    # === Attachment/Voice Preview Row (if any) ===
    if st.session_state.attached_file or st.session_state.voice_text:
        preview_cols = st.columns([10, 1])
        with preview_cols[0]:
            if st.session_state.attached_file:
                fname = st.session_state.attached_file.get("name", "file")
                st.markdown(f'<span class="attachment-chip">📎 {fname}</span>', unsafe_allow_html=True)
            if st.session_state.voice_text:
                vtext = st.session_state.voice_text[:40] + "..." if len(st.session_state.voice_text) > 40 else st.session_state.voice_text
                st.markdown(f'<span class="attachment-chip">🎤 {vtext}</span>', unsafe_allow_html=True)
        with preview_cols[1]:
            st.markdown('<div class="remove-attachment-btn">', unsafe_allow_html=True)
            if st.button("✕", key="clear_attachments", help="Clear"):
                st.session_state.attached_file = None
                st.session_state.voice_text = ""
                st.session_state.last_file_id = None
                st.session_state.last_audio_id = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Show voice text preview INSIDE the bar (if any)
    if st.session_state.voice_text:
        voice_col1, voice_col2 = st.columns([6, 1])
        with voice_col1:
            vtext = st.session_state.voice_text[:50] + "..." if len(st.session_state.voice_text) > 50 else st.session_state.voice_text
            st.markdown(f'''
                <div class="gpt-attachment-preview">
                    <div class="file-info">🎤 {vtext}</div>
                </div>
            ''', unsafe_allow_html=True)
        with voice_col2:
            st.markdown('<div class="gpt-remove-btn">', unsafe_allow_html=True)
            if st.button("✕", key="remove_voice", help="Clear"):
                st.session_state.voice_text = ""
                st.session_state.last_audio_id = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Main controls row: [📎] [Model▼] [_____Input_____] [🎤] [➤]
    c_file, c_model, c_input, c_voice, c_send = st.columns([0.6, 1.8, 7, 0.6, 0.6])
    
    # 📎 File attachment
    with c_file:
        st.markdown('<div class="gpt-file-btn">', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "📎", 
            type=["txt", "pdf", "docx", "md", "csv", "json", "png", "jpg", "jpeg"],
            key=f"file_{st.session_state.input_key}",
            label_visibility="collapsed"
        )
        if uploaded:
            fid = f"{uploaded.name}_{uploaded.size}"
            if st.session_state.last_file_id != fid:
                st.session_state.last_file_id = fid
                st.session_state.attached_file = get_file_content(uploaded)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🤖 Model selector
    with c_model:
        st.markdown('<div class="gpt-model-select">', unsafe_allow_html=True)
        model = st.selectbox(
            "Model",
            options=available_models,
            index=available_models.index(current_model) if current_model in available_models else 0,
            key=f"model_{st.session_state.input_key}",
            label_visibility="collapsed"
        )
        if model and model != current_model:
            st.session_state.current_model_name = model
            st.session_state.model_changed = True
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 📝 Text input
    with c_input:
        st.markdown('<div class="gpt-text-input">', unsafe_allow_html=True)
        placeholder = "Message WayPoint..."
        if st.session_state.voice_text:
            placeholder = "Press send or type to replace voice..."
        
        text = st.text_input(
            "Message",
            value="",
            placeholder=placeholder,
            key=f"text_{st.session_state.input_key}",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 🎤 Voice input
    with c_voice:
        st.markdown('<div class="gpt-voice-btn">', unsafe_allow_html=True)
        try:
            audio = st.audio_input("🎤", key=f"audio_{st.session_state.input_key}", label_visibility="collapsed")
            if audio:
                aid = id(audio)
                if st.session_state.last_audio_id != aid:
                    st.session_state.last_audio_id = aid
                    audio_bytes = audio.read()
                    if audio_bytes:
                        transcribed = transcribe_audio(audio_bytes)
                        if transcribed:
                            st.session_state.voice_text = transcribed
                            st.rerun()
        except:
            pass
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ➤ Send button
    with c_send:
        st.markdown('<div class="gpt-send-btn">', unsafe_allow_html=True)
        send = st.button("➤", key=f"send_{st.session_state.input_key}", help="Send")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close gpt-chatbar
    
    # Handle send
    user_input = None
    if send and (text or st.session_state.voice_text):
        user_input = text if text else st.session_state.voice_text
        st.session_state.input_key += 1  # Reset inputs
    
    # Build result
    result = {
        "text": user_input,
        "file": None,
        "model": st.session_state.get("current_model_name"),
        "voice_text": ""
    }
    
    if user_input:
        if st.session_state.attached_file:
            result["file"] = st.session_state.attached_file
            st.session_state.attached_file = None
            st.session_state.last_file_id = None
        if st.session_state.voice_text:
            st.session_state.voice_text = ""
            st.session_state.last_audio_id = None
    
    return result


def get_input_with_context(result):
    """Format the input with file context for the AI"""
    if not result or not result.get("text"):
        return None
    
    text = result["text"]
    file_data = result.get("file")
    
    if file_data:
        file_context = f"\n\n---\n📎 **Attached File: {file_data['name']}**\n"
        if file_data["type"] == "image":
            file_context += f"[Image attached: {file_data['name']}]\n"
        else:
            content = file_data.get("content", "")
            if len(content) > 3000:
                content = content[:3000] + "\n... [truncated]"
            file_context += f"```\n{content}\n```\n"
        text = text + file_context
    
    return text
