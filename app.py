import streamlit as st

from course_library import search_course_materials


st.set_page_config(
    page_title="Hairdresser Learning Assistant",
    layout="centered",
)

st.title("Hairdresser Learning Assistant")
st.caption("Fictional portfolio prototype — local UI only")

st.info(
    "This demo does not connect to an AI model, GoHighLevel, or a student account. "
    "Please use fictional questions only; do not enter personal, client, or financial information."
)

st.header("Ask the course tutor")

with st.form("tutor_question_form"):
    question = st.text_area(
        "What would you like help with?",
        placeholder="For example: What costs should I consider when pricing a service?",
        max_chars=1000,
    )
    submitted = st.form_submit_button("Submit test question")

if submitted:
    if not question.strip():
        st.warning("Enter a fictional test question to try the interface.")
    else:
        results = search_course_materials(question.strip())
        if not results:
            st.warning(
                "I could not find a matching passage in the local course materials. "
                "No AI model is connected, so I cannot answer beyond those materials."
            )
        else:
            st.success(
                f"Found {len(results)} matching course passage(s). "
                "This is a local keyword search, not an AI-generated answer."
            )
            for result in results:
                with st.expander(f"{result.title} — {result.heading}"):
                    st.caption(f"Source: {result.source}")
                    st.markdown(result.content)

st.divider()
st.caption("Next step: improve and test the course search before connecting a model.")
