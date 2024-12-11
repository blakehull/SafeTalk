import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from safetalk.domain.chat import Message
from safetalk.pipeline.participants import Patient, Therapist
from safetalk.pipeline.session import TherapySession

st.title("SafeTalk | Sharpen Your Skills")
therapist = Therapist()
with open("safetalk/meta/ollama/anxiety.template", "r") as file:
    file_contents = file.read()

personality = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            file_contents,
        ),
        ("human", "{input}"),
    ]
)
llm = ChatOllama(model="llama3.2", temperature=0.8)

patient = Patient(personality=personality, name="Mike", llm=llm)

if "messages" not in st.session_state:
    st.session_state.messages = []

therapy_session = TherapySession(
    therapist=therapist, patient=patient, history=st.session_state.messages
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    therapist_says = therapy_session.therapist.says(content=prompt)
    patient_says: Message = therapy_session.patient.responds(therapist_says)
    with st.chat_message("assistant"):
        st.markdown(patient_says.content)
    st.session_state.messages.append(
        {"role": "assistant", "content": patient_says.content}
    )
