import openai
import streamlit as st


def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][-2:]
    ]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=400)


API_KEY = st.sidebar.text_input(":blue[Enter Your OPENAI API-KEY :]", 
                placeholder="Paste your OpenAI API key here (sk-...)",
                type="password") # Session state storage would be ideal

openai.api_key = API_KEY

BASE_PROMPT = [
        {"role": "system", "content": "이 프로그램은 입력된 내용을 {용어1: 설명내용} 형태로 쉽게 해석해서 알려주는 어시스턴트야."},
        {"role": "user", "content": """
[1] 범죄피해자 보호법 제17조 제2항에 규정한 유족구조금의 법적 성격
[2] 구조피해자 또는 상속인이 범죄자에 대하여 고의의 불법행위를, 범죄자의 사용자에 대하여 사용자책임을 주장하며 공동하여 손해배상을 구하는 소송을 제기하여 법원이 이들에게 공동하여 손해배상금 지급을 명하되, 사용자에 대하여만 과실상계를 적용함으로써 더 적은 금액의 지급을 명하는 경우, 구조피해자나 유족이 범죄피해자 보호법에 의한 범죄피해구조금을 받음으로써 소멸하는 부분(=다액채무자인 범죄자가 단독으로 부담하는 채무) 및 범죄피해구조금이 다액채무자인 범죄자가 단독으로 채무를 부담하는 부분을 초과하지 않는 경우, 그 구조금 상당액은 전액 단독 부담하는 부분에서만 공제하여야 하는지 여부(적극) / 이 경우 범죄자와 사용자가 부담하는 채무의 성질(=금액이 서로 다른 부진정연대채무)
        """},
        {"role": "assistant", "content": """
[1]
범죄피해자 보호법 제17조 제2항에 규정한 유족구조금의 법적 성격:
범죄 피해자가 사망한 경우, 해당 피해자의 가족들에게 범죄피해구조금을 지급하는 것으로, 법적으로 보호되는 권리입니다.
[2]
과실상계: 법적으로 책임이 있는 여러 사람 중에서 상대방에게 더 큰 책임이 있거나 그만큼의 잘못을 저질렀을 경우, 그에 상응하여 책임을 분담하도록 하는 것을 말합니다.
다액채무자: 여러 사람이 함께 부담하는 채무 중에서, 한 사람이 전액을 부담하는 채무입니다.
부진정연대채무: 여러 사람이 함께 부담하는 채무 중에서, 각각의 부담액이 서로 다른 채무입니다.
위 [2]의 내용을 요약하면, 범죄로 인해 발생한 손해를 구상할 때, 구조피해자나 상속인들이 범죄자와 사용자에 대하여 손해배상금을 구하면서, 법원에서는 각자의 책임을 고려하여 손해배상금을 분담하게 됩니다. 이 경우, 사용자에 대해서는 법적으로 책임이 덜하다는 이유로 손해배상금에서 과실상계를 적용하여 더 적은 금액의 지급을 명하는 경우가 있습니다. 이때, 구조피해자나 상속인이 범죄피해자 보호법에 의한 범죄피해구조금을 받아야 하는 부분(=다액채무자인 범죄자가 단독으로 부담하는 채무)과 범죄피해구조금이 다액채무자인 범죄자가 단독으로 채무를 부담하는 부분을 초과하지 않는 범위 내에서, 구조금 상당액은 전액 단독 부담하는 부분에서만 공제할 수 있습니다. 이 경우, 범죄자와 사용자가 부담하는 채무의 성질이 부진정연대채무인지에 따라서 적극적으로 판단해야 합니다.
        """}
]

if "messages" not in st.session_state:
    st.session_state["messages"] = ""

st.header("어려운 계약내용/법적지식 쉽게 설명해주는 챗봇")
st.subheader('반드시 api 키를 입력하고 엔터를 먼저 눌러주세요.')
st.write("아직 개발중임으로, 양해 부탁드립니다. by 세형")

text = st.empty()
show_messages(text)

prompt = st.text_input("Prompt", placeholder="계약내용 및 판례 등 전문 문서의 글을 입력해 주세요.")

if st.button("Send"):
    st.session_state["messages"] = BASE_PROMPT
    with st.spinner("Generating response..."):
        st.session_state["messages"] += [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=st.session_state["messages"]
        )
        message_response = response["choices"][0]["message"]["content"]
        st.session_state["messages"] += [
            {"role": "system", "content": message_response}
        ]
        show_messages(text)

if st.button("Clear"):
    st.session_state["messages"] = ""
    show_messages(text)