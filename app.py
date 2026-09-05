
import streamlit as st
from google import genai
from google.colab import userdata

# Get Gemini API key
key = userdata.get("divya@1011")

# Connect to Gemini
client = genai.Client(api_key=key)

# Page settings
st.set_page_config(
    page_title="Electro-Doc AI",
    page_icon="⚡"
)

# Title
st.title("⚡ Electro-Doc AI")
st.subheader("Intelligent Electrical Datasheet Assistant")

st.write(
    "Enter an electrical equipment model and let AI identify it."
)

st.divider()

# User inputs
manufacturer = st.text_input(
    "🏭 Manufacturer",
    placeholder="Example: Siemens"
)

equipment = st.text_input(
    "🔧 Equipment Type",
    placeholder="Example: Contactor"
)

model = st.text_input(
    "🔢 Model Number",
    placeholder="Example: 3RT2015-1BB41"
)

# AI button
if st.button("🤖 Identify Equipment", use_container_width=True):

    if manufacturer and equipment and model:

        with st.spinner("AI is analyzing..."):

            prompt = f"""
You are an electrical engineering assistant.

Manufacturer: {manufacturer}
Equipment Type: {equipment}
Model Number: {model}

Give the following:

1. Equipment identification
2. What it is used for
3. Important datasheet parameters to check
4. How a user can find the official manufacturer's datasheet

Do not invent exact specifications.
If you are uncertain, clearly say so.
"""

            response = client.interactions.create(
                model="gemini-3.7-flash",
                input=prompt,
                generation_config={
                    "thinking_level": "low"
                }
            )

            st.success("Analysis completed!")

            st.markdown("### 🤖 AI Result")
            st.write(response.output_text)

    else:
        st.warning(
            "Please enter Manufacturer, Equipment Type "
            "and Model Number."
        )
        
