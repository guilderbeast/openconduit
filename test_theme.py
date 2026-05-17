import streamlit as st
import webbrowser

# --- 1. THE QUICK EXIT ---
def quick_exit():
    webbrowser.open_new_tab("https://www.bbc.co.uk/weather")
    st.session_state.clear()
    st.stop()

# --- 2. LAYOUT ---
st.set_page_config(page_title="Open Conduit", page_icon="🕊️")
if st.button("🚨 QUICK EXIT"):
    quick_exit()

# --- 3. THEME SELECTOR ---
theme = st.sidebar.selectbox("Comfort View:", ["Standard", "ADHD Calm", "Sensitive (Warm)", "High Contrast"])

# --- 4. THEME COLORS ---
if theme == "ADHD Calm":
    st.markdown("<style>.stApp { background-color: #f0f4f0 !important; }</style>", unsafe_allow_html=True)
elif theme == "Sensitive (Warm)":
    st.markdown("<style>.stApp { background-color: #fdf5e6 !important; }</style>", unsafe_allow_html=True)
elif theme == "High Contrast":
    st.markdown("<style>.stApp { background-color: #000000 !important; color: #ffffff !important; }</style>", unsafe_allow_html=True)

# --- 5. THE INTERFACE ---
st.title("How are you feeling today?")
user_input = st.text_area("Tell the Wizard what you'd like to create in Blender...")

if st.button("Squeeze & Send"):
    st.success("Squeezing your request for the AI...")