import streamlit as st
from src.config import Settings
from src.rag import answer_question

st.set_page_config(page_title="AI SQL Assistant", page_icon="🧠", layout="wide")
st.title("🧠 AI-Powered SQL Assistant")
st.caption("Ask SQL questions grounded in your indexed documentation, schema notes and examples.")

with st.sidebar:
    st.header("About")
    st.write("Python + Streamlit + Azure AI Search hybrid retrieval + Azure OpenAI.")
    st.info("This demo generates SQL text only. It does not execute queries against a database.")
    st.markdown("**Try asking**\n- Explain DENSE_RANK()\n- Find top customers by revenue\n- Calculate monthly revenue\n- Explain the sample schema")

try:
    Settings().validate()
except Exception as exc:
    st.error(f"Configuration issue: {exc}")
    st.write("Copy .env.example to .env, add your Azure resource details, and restart.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Retrieved knowledge sources"):
                for source in message["sources"]:
                    st.markdown(f"**{source['source']}** · chunk {source['chunk_number']}")
                    st.caption(source["content"][:900])

prompt = st.chat_input("Ask a SQL question...")
if prompt:
    history = st.session_state.messages[-6:]
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge and preparing an answer..."):
            try:
                answer, docs = answer_question(prompt, history)
                st.markdown(answer)
                if docs:
                    with st.expander("Retrieved knowledge sources"):
                        for doc in docs:
                            st.markdown(f"**{doc['source']}** · chunk {doc['chunk_number']}")
                            st.caption(doc["content"][:900])
                else:
                    st.warning("No knowledge chunks were retrieved. Schema details should not be invented.")
                st.session_state.messages.append({"role": "assistant", "content": answer, "sources": docs})
            except Exception as exc:
                st.error("Request failed. Check Azure configuration, deployment names, network access and quota.")
                st.exception(exc)

if st.button("Clear conversation"):
    st.session_state.messages = []
    st.rerun()
