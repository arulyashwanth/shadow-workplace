import streamlit as st
import requests
import re
import time

# --- CONFIG ---
API_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="Shadow Workplace", 
    page_icon="🏢", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- MODERN PROFESSIONAL CSS ---
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0f172a; /* Slate 900 */
        color: #f8fafc; /* Slate 50 */
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #f8fafc;
    }
    p, div {
        color: #cbd5e1; /* Slate 300 */
    }

    /* Buttons */
    .stButton button {
        background-color: #3b82f6; /* Blue 500 */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background-color: #2563eb; /* Blue 600 */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Inputs */
    .stTextInput input {
        background-color: #1e293b; /* Slate 800 */
        color: white;
        border: 1px solid #334155; /* Slate 700 */
        border-radius: 8px;
    }
    .stTextInput input:focus {
        border-color: #3b82f6;
    }

    /* Custom Cards */
    .job-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: bold;
        background-color: #059669; /* Emerald 600 */
        color: white;
    }

    .repo-link {
        color: #38bdf8; /* Sky 400 */
        text-decoration: none;
        font-weight: bold;
        font-family: monospace;
    }

    /* Feedback Boxes */
    .feedback-box {
        background-color: #1e293b;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        border-radius: 0 8px 8px 0;
    }
    .resume-box {
        background-color: #172033;
        border: 1px solid #3b82f6;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "repo_url" not in st.session_state: st.session_state.repo_url = None
if "job_history" not in st.session_state: st.session_state.job_history = []
if "current_role" not in st.session_state: st.session_state.current_role = ""

# --- SIDEBAR: CAREER HISTORY ---
with st.sidebar:
    st.header("📂 Career History")
    if not st.session_state.job_history:
        st.info("No active history yet. Start a job!")
    else:
        for i, job in enumerate(reversed(st.session_state.job_history)):
            with st.expander(f"Job #{len(st.session_state.job_history)-i}", expanded=False):
                st.caption(job)

    st.markdown("---")
    if st.session_state.repo_url:
        if st.button("Quit Current Job (Reset)", type="secondary"):
            st.session_state.repo_url = None
            st.session_state.current_role = ""
            st.rerun()

# --- MAIN UI ---
st.title("🏢 Shadow Workplace")
st.markdown("### The AI-Powered Career Simulator")
st.markdown("Experience real-world engineering challenges. Get hired, code, and survive the code review.")

st.markdown("---")

# --- PHASE 1: JOB SEARCH (If not hired) ---
if not st.session_state.repo_url:
    st.subheader("1. Find a Role")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        job_prompt = st.text_input("Enter a target role:", placeholder="e.g. Backend Intern for a Fintech App")
    with col2:
        st.write("") # Spacer
        st.write("") # Spacer
        start_btn = st.button("🚀 Start Simulation", use_container_width=True)

    if start_btn and job_prompt:
        with st.spinner("🤖 Manager AI is scoping the project..."):
            try:
                resp = requests.post(f"{API_URL}/agent/start_job", json={"prompt": job_prompt})
                data = resp.json()
                
                msgs = data.get("messages", [])
                last_msg = msgs[-1]
                
                # Regex to find repo URL
                url_match = re.search(r'(https://github\.com/[^\s]+)', last_msg)
                
                if url_match:
                    st.session_state.repo_url = url_match.group(0)
                    st.session_state.current_role = job_prompt
                    st.session_state.job_history.append(f"{job_prompt} - {st.session_state.repo_url}")
                    st.rerun()
                else:
                    st.error("Failed to provision workspace. Please try again.")
            except Exception as e:
                st.error(f"Connection Error: {e}")

# --- PHASE 2: WORKSPACE (If hired) ---
else:
    st.subheader("2. Active Workspace")
    
    # Custom Card HTML
    st.markdown(f"""
    <div class="job-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="status-badge">ACTIVE EMPLOYMENT</span>
            <span style="color: #94a3b8; font-size: 0.9rem;">Role: {st.session_state.current_role}</span>
        </div>
        <br>
        <h3 style="margin: 0;">📁 GitHub Repository</h3>
        <p>Your environment has been provisioned with starter files, requirements, and a Jira-style mission board.</p>
        <a href="{st.session_state.repo_url}" target="_blank" class="repo-link">
            🔗 {st.session_state.repo_url}
        </a>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📝 View Mission Instructions", expanded=True):
        st.info("1. Clone the repo above.\n2. Read the README.md for your tickets.\n3. Push your code to 'main'.\n4. Come back here to submit.")

    st.markdown("---")
    
    # --- PHASE 3: REVIEW ---
    st.subheader("3. Code Review")
    
    if st.button("📢 Submit Work for Review", type="primary"):
        with st.spinner("🔍 Security Agent scanning... 🧠 Senior Dev reviewing..."):
            try:
                resp = requests.post(f"{API_URL}/agent/review_code", json={"repo_url": st.session_state.repo_url})
                data = resp.json()
                
                security_status = data.get("security_status", "clean")
                review_msg = data.get("messages", ["No response"])[0]

                if security_status == "blocked":
                    st.error("🚨 SECURITY ALERT BLOCKED DEPLOYMENT")
                    st.markdown(f"<div class='feedback-box' style='border-color: #ef4444;'>{review_msg}</div>", unsafe_allow_html=True)
                else:
                    # Parse specific sections if the Senior Dev outputs them (Resume Boost)
                    st.success("✅ Build Successful. Reviewing Logic...")
                    
                    st.markdown("### 👨‍💻 Senior Developer Feedback")
                    st.markdown(f"<div class='feedback-box'>{review_msg}</div>", unsafe_allow_html=True)

                    # Fun interaction for success
                    if "APPROVED" in review_msg or "Resume Bullet Point" in review_msg:
                        st.balloons()
                        st.markdown("""
                        <div class="resume-box">
                            <h4>✨ Career Artifact Unlocked</h4>
                            <p>You can add this project to your GitHub Portfolio.</p>
                        </div>
                        """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Review System Error: {e}")
