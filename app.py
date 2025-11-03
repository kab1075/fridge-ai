import streamlit as st
from openai import OpenAI

# ---- CONFIG ----
st.set_page_config(page_title="AI Fridge → Meal Ideas", page_icon="🍳")
st.title("🥕 What's In My Fridge?")
st.write("Upload up to 4 photos of your fridge or pantry, and AI will suggest meal ideas based on what it sees.")

# ---- USER INPUT ----
uploaded_files = st.file_uploader(
    "Upload image(s) of your fridge or pantry:",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
)

api_key = st.text_input("🔑 Enter your OpenAI API key:", type="password")

if st.button("✨ Generate Meal Ideas") and uploaded_files and api_key:
    st.info("Analyzing your photos... please wait ⏳")
    client = OpenAI(api_key=api_key)

    # Convert each uploaded file to base64 data for GPT-4o
    image_inputs = []
    for file in uploaded_files:
        bytes_data = file.getvalue()
        image_inputs.append(
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{bytes_data.hex()}"}
        )

    # ---- CALL GPT-4o ----
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful kitchen assistant that analyzes fridge photos "
                        "to detect ingredients and suggest 3–5 meal ideas. Each recipe should "
                        "include a title, short description, and main ingredients."
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze these images and suggest meal ideas:"},
                        *image_inputs,
                    ],
                },
            ],
        )

        ai_reply = response.choices[0].message.content
        st.success("✅ Here are your AI-generated meal ideas:")
        st.markdown(ai_reply)

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.write("👆 Upload photo(s) and enter your API key to get started.")
