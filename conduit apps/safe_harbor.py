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

# --- 4. THEME LOGIC ---
if theme == "ADHD Calm":
    st.markdown("""
    <style>
    div.stApp * { font-size: 22px !important; line-height: 1.8 !important; letter-spacing: 0.5px !important; }
    textarea { padding: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

elif theme == "Sensitive (Warm)":
    st.markdown("""
    <style>
    div.stApp { background-color: #fdf5e6 !important; }
    div.stApp * { color: #5d4037 !important; }
    </style>
    """, unsafe_allow_html=True)

elif theme == "High Contrast":
    st.markdown("""
    <style>
    div.stApp { background-color: #000000 !important; }
    div.stApp * { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)
import datetime  # Add this to the very top of your file with the other imports

# --- 5. THE INTERFACE ---
st.title("How are you feeling today?")
user_input = st.text_area("Tell the Wizard what you'd like to create in Blender...", height=200)

if st.button("Squeeze & Send"):
    if user_input.strip() == "":
        st.warning("The Wizard needs some words to work his magic!")
    else:
        # Create a unique filename based on the time
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"C:/conduit apps/inbox/prompt_{timestamp}.txt"
        
        # Ensure the inbox folder exists
        import os
        if not os.path.exists("C:/conduit apps/inbox"):
            os.makedirs("C:/conduit apps/inbox")
            
        # Save the prompt
        with open(filename, "w") as f:
            f.write(user_input)
            
        st.success(f"Squeezed! Prompt saved to your inbox. The Wizard is looking at it now.")