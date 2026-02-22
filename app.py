"""
WayPoint AI Career Strategist - Main Streamlit Application
"""
import streamlit as st
from career_advisor import WayPointAdvisor
from config import APP_TITLE, APP_SUBTITLE, SIDEBAR_TITLE, AI_PROVIDER
from utils import detect_persona, is_vague_query


# Page configuration
st.set_page_config(
    page_title="WayPoint - AI Career Strategist",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():

    try:
        with open("styles.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # CSS file not found, use default styling

load_css()


# Initialize session state
def init_session_state():

    if "advisor" not in st.session_state:
        try:
            st.session_state.advisor = WayPointAdvisor()
        except ValueError as e:
            st.error(str(e))
            st.info("👉 Please create a `.env` file in the project directory and add your `OPENAI_API_KEY`")
            st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_context" not in st.session_state:
        st.session_state.user_context = {}
    
    if "current_model" not in st.session_state:
        st.session_state.current_model = "ollama"
    
    if "current_provider" not in st.session_state:
        st.session_state.current_provider = AI_PROVIDER or "ollama"
    
    if "current_model_name" not in st.session_state:
        from config import MODEL_NAME
        st.session_state.current_model_name = MODEL_NAME
    
    if "last_input_data" not in st.session_state:
        st.session_state.last_input_data = None


# Sidebar for user context
def render_sidebar():
 
    with st.sidebar:
        st.markdown(f"### {SIDEBAR_TITLE}")
        st.markdown("*Provide context to get more personalized advice*")
        
        st.markdown("---")
        
        # User context form
        with st.form("context_form", clear_on_submit=False):
            current_role = st.text_input(
                "Current Role",
                value=st.session_state.user_context.get("current_role", ""),
                placeholder="e.g., Software Engineer, Student, etc."
            )
            
            experience_years = st.text_input(
                "Years of Experience",
                value=st.session_state.user_context.get("experience_years", ""),
                placeholder="e.g., 3 years, Fresh Graduate, etc."
            )
            
            skills = st.text_area(
                "Key Skills",
                value=st.session_state.user_context.get("skills", ""),
                placeholder="e.g., Python, React, Data Analysis...",
                height=80
            )
            
            education = st.text_input(
                "Education",
                value=st.session_state.user_context.get("education", ""),
                placeholder="e.g., B.S. Computer Science"
            )
            
            submitted = st.form_submit_button("💾 Save Context", use_container_width=True)
            
            if submitted:
                st.session_state.user_context = {
                    "current_role": current_role,
                    "experience_years": experience_years,
                    "skills": skills,
                    "education": education
                }
                st.success("✅ Context saved! This will help WayPoint give you better advice.")
        
        st.markdown("---")
        
        # Conversation controls
        st.markdown("### 🔧 Conversation Controls")
        
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.advisor.clear_conversation()
            st.success("✅ Conversation cleared!")
            st.rerun()
        
        # Display persona if detected
        if st.session_state.messages:
            last_user_message = next(
                (msg["content"] for msg in reversed(st.session_state.messages) if msg["role"] == "user"),
                None
            )
            if last_user_message:
                persona = detect_persona(last_user_message)
                if persona:
                    st.info(f"🎭 Detected Persona: **{persona.replace('_', ' ').title()}**")
        
        # App info
        st.markdown("---")
        st.markdown("### ℹ️ About WayPoint")
        
        # Show current AI provider
        try:
            provider_info = st.session_state.advisor.get_provider_info()
            st.info(provider_info)
        except:
            pass
        
        st.markdown(
            """
            WayPoint is your AI Career Strategist, designed to provide:
            
            - 🎯 Honest, actionable career advice
            - 📊 Modern tech stack recommendations
            - 🗺️ Clear career roadmaps
            - ⚡ Immediate action items
            
           
            """
        )


# Main chat interface
def render_chat():

    
    # App header
    st.markdown(
        f"""
        <div class="app-header">
            <h1>{APP_TITLE}</h1>
            <p>{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display chat messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                # Show file attachment indicator if present
                if message.get("has_attachment"):
                    st.caption(f"📎 Attached: {message.get('attachment_name', 'file')}")
    
    # Standard Streamlit chat input
    user_input = st.chat_input("Message WayPoint...")
    
    if user_input:
        # Save and display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 WayPoint is thinking..."):
                response = st.session_state.advisor.get_response(
                    user_input,
                    st.session_state.user_context if st.session_state.user_context else None
                )
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})



# Main app
def main():
 
    init_session_state()
    render_sidebar()
    render_chat()


if __name__ == "__main__":
    main()
