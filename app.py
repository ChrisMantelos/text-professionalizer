import streamlit as st
from dotenv import load_dotenv
from professionalizer import professionalize, ProfessionalizerError, TONE_PROMPTS
from history import add_to_history

load_dotenv()

st.set_page_config(page_title="Text Professionalizer", layout="centered")

if "history" not in st.session_state:
    st.session_state["history"] = []

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

if st.button("Convert", type="primary"):
    try:
        with st.spinner("Processing..."):
            result = professionalize(draft, tone=tone, api_key=api_key or None)
    except ProfessionalizerError as exc:
        st.error(str(exc))
    else:
        st.session_state["history"] = add_to_history(
            st.session_state["history"], draft, tone, result
        )
        st.subheader("Result")
        st.code(result, language=None, wrap_lines=True)
        st.caption("Use the copy icon in the top-right corner of the box to copy the text.")

if st.session_state["history"]:
    with st.expander("Recent conversions"):
        for entry in st.session_state["history"]:
            st.markdown(f"**Tone: {entry['tone']}**")
            st.text(entry["original"])
            st.code(entry["result"], language=None, wrap_lines=True)
