"""
Streamlit web UI for text-professionalizer.
Run locally:   streamlit run app.py
Deploy free:   share.streamlit.io (connect this GitHub repo)
"""

import streamlit as st
from professionalizer import professionalize, ProfessionalizerError, TONE_PROMPTS

st.set_page_config(page_title="Text Professionalizer", layout="centered")

st.title("Text Professionalizer")
st.caption(
    "Converts informal draft text into professional communication, "
    "powered by the Claude API."
)

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        help="Not stored anywhere, used only for this request.",
    )
    tone = st.selectbox("Tone", options=list(TONE_PROMPTS.keys()), index=0)
    st.markdown("---")
    st.markdown(
        "[GitHub repo](https://github.com/ChrisMantelos/text-professionalizer) "
        "- Built with Python and the Anthropic SDK"
    )

draft = st.text_area(
    "Draft text",
    height=160,
    placeholder="e.g. hey sorry the report is gonna be a bit late, ill send it later today",
)

col1, col2 = st.columns([1, 4])
with col1:
    submitted = st.button("Convert", type="primary", use_container_width=True)

if submitted:
    try:
        with st.spinner("Processing..."):
            result = professionalize(draft, tone=tone, api_key=api_key or None)
    except ProfessionalizerError as exc:
        st.error(str(exc))
    else:
        st.subheader("Result")
        st.text_area("Professional version", value=result, height=160, label_visibility="collapsed")
        st.button("Copy", help="Select the text above and press Ctrl+C")
