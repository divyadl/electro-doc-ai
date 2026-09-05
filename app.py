import streamlit as st
from google import genai
from tavily import TavilyClient

# Get Gemini API key from Streamlit Secrets
key = st.secrets["GEMINI_API_KEY"]

# Connect to Gemini
client = genai.Client(api_key=key)

# Page settings
st.set_page_config(
    page_title="Electro-Doc AI",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ Electro-Doc AI")
st.subheader("Intelligent Electrical Datasheet Assistant")

st.write(
    "Enter an electrical equipment model and find "
    "its official manufacturer datasheet."
)

st.divider()

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

if st.button("🔍 Find Official Datasheet", use_container_width=True):

    if manufacturer and equipment and model:

        with st.spinner("Searching for the official datasheet..."):

            prompt = f"""
Find the official manufacturer datasheet for this electrical equipment:

Manufacturer: {manufacturer}
Equipment Type: {equipment}
Model Number: {model}

IMPORTANT:
- Search the web.
- Prefer the official manufacturer's website.
- Verify that the model number exactly matches.
- Do not guess or invent a datasheet.
- If an official datasheet cannot be verified, clearly say so.

Give the result in this format:

Equipment:
Manufacturer:
Model:
Description:

Official Datasheet:
[provide the official datasheet URL if found]

Important Specifications:
- List the most important specifications found.

Source:
[official manufacturer website URL]
"""

            response = client.interactions.create(
                model="gemini-3.7-flash",
                input=prompt,
        
                    
                    
                
                generation_config={
                    "thinking_level": "low"
                }
            )

            st.success("Search completed!")

            st.markdown("### 📄 Datasheet Result")
            st.write(response.output_text)

    else:
        st.warning(
            "Please enter Manufacturer, Equipment Type "
            "and Model Number."
        )


