import streamlit as st
from google import genai
from tavily import TavilyClient

# Get Gemini API key from Streamlit Secrets
key = st.secrets["GEMINI_API_KEY"]
tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])

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
if st.button("🔍 Find Official Datasheet", use_container_width=True):

    if manufacturer and equipment and model:

        with st.spinner("Searching the web for the official datasheet..."):

            # Create a focused search query
            search_query = (
                f'"{manufacturer}" "{model}" '
                f'{equipment} datasheet PDF'
            )

            # Search the web using Tavily
            search_results = tavily.search(
                query=search_query,
                search_depth="advanced",
                max_results=5
            )

            # Collect search results
            results_text = ""

            for result in search_results["results"]:
                results_text += f"""
Title: {result.get("title", "")}
URL: {result.get("url", "")}
Content: {result.get("content", "")}

"""

            # Ask Gemini to identify the correct official source
            prompt = f"""
You are an electrical engineering datasheet verification assistant.

The user is looking for:

Manufacturer: {manufacturer}
Equipment Type: {equipment}
Model Number: {model}

Below are web search results:

{results_text}

Your task:

1. Identify the result that is most likely the OFFICIAL manufacturer source.
2. Verify that the exact model number appears to match.
3. Prefer the manufacturer's own website over third-party websites.
4. Do not invent a datasheet URL.
5. If you cannot confidently verify an official datasheet, say:
   "Official datasheet could not be confidently verified."

Give the answer in this format:

### Equipment
Manufacturer:
Equipment Type:
Model Number:

### Official Datasheet
URL:

### Verification
Explain briefly why this is the correct source.

### Important Specifications
List the important specifications that can be confidently obtained from the search results.
"""

            response = client.interactions.create(
                model="gemini-3.7-flash",
                input=prompt,
                generation_config={
                    "thinking_level": "low"
                }
            )

            st.success("Datasheet search completed!")

            st.markdown("### 📄 Datasheet Result")
            st.write(response.output_text)

    else:
        st.warning(
            "Please enter Manufacturer, Equipment Type "
            "and Model Number."
        )
