from logging import getLogger

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

from safetalk.domain.chat import Message
from safetalk.pipeline.llm import Bedrock
from safetalk.pipeline.participants import Patient, Therapist
from safetalk.pipeline.session import TherapySession

st.set_page_config(page_title="SafeTalk", layout="wide")
st.markdown("<h1><center>SafeTalk | Sharpen Your Skills</center></h1>", unsafe_allow_html=True)
therapist = Therapist()
logger = getLogger(__name__)
with open("safetalk/meta/ollama/anxiety.template", "r") as file:
    file_contents = file.read()

personality_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            file_contents,
        ),
        ("human", "{input}"),
    ]
)
llm = Bedrock(
    client=None,
    system_prompt=personality_prompt,
)

patient = Patient(personality=llm, name="Mike")

if "messages" not in st.session_state:
    st.session_state.messages = []

therapy_session = TherapySession(
    therapist=therapist, patient=patient, history=st.session_state.messages
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(""):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    therapist_says = therapy_session.therapist.says(content=prompt)
    patient_says: Message = therapy_session.patient.responds(therapist_says)
    with st.chat_message("assistant"):
        st.markdown(patient_says.content)
    st.session_state.messages.append(
        {"role": "assistant", "content": patient_says.content}
    )
    logger.info(st.session_state.messages)
