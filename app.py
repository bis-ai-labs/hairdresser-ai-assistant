import streamlit as st

from course_library import search_course_materials
from tutor import MODEL_NAME, answer_question

st.set_page_config(
    page_title="Hairdresser Learning Assistant",
    layout="centered",
)

st.title("Hairdresser Learning Assistant")
st.caption("Fictional prtfolio prototype - configured model and local course notes")

st.info(
    "This demo uses fictional course notes only and sends matching passages "
    "and questions to the configured model provider. It does not connect  to "
    "GoHighLevel or a student account. "
    "Do not enter personal, client, employer, PKI, or financial information."
)

st.header("Ask the course tutor")

with st.form("tutor_question_form"):
    question = st.text_area(
        "What would you like help with?",
        placeholder="For example: What costs should I consder when pricing a service?",
        max_chars=1000,
    )
    submitted = st.form_submit_button("Ask the tutor")

if submitted:
    if not question.strip():
        st.warning("Enter a fictional test question.")
    else:
        passages = search_course_materials(question.strip())
        if not passages:
            st.warning(
                "I could not find a matching passage in the loacl course "
                "materials, so I did not ask the model to answer."
            )
        else:
            st.subheader("Tutor response")
            st.caption(f"Configured model: {MODEL_NAME}")
            response = answer_question(question, passages)
            st.markdown(response)

            st.subheader("Retrieved course sources")
            for passage in passages:
                with st.expander(f"{passage.title} - {passage.heading}"):
                    st.caption(f"Source: {passage.source}")
                    st.markdown(passage.content)

st.divider()
st.caption(
    "Learning protopype only. Keyword search and model answers can be incomplete "
    "or incorrect; review the cited course mateerial."
)