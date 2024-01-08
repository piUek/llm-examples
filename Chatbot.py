import urllib.request
import json
import os
import ssl
import streamlit as st
import codecs

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

url = 'https://pf-ivory-esg.swedencentral.inference.ml.azure.com/score'
api_key = st.secrets['api_key']

# api_key = ""
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

st.title("💬 Asystent")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "question": "How can I help you?", "chat_history": []}]

for msg in st.session_state.messages:
    print(msg)
    st.chat_message(msg["role"]).write(msg["question"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "question": prompt, "chat_history": []})
    st.chat_message("user").write(prompt)
    data = st.session_state.messages[-1]
    print(data)
    body = str.encode(json.dumps(data))
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'pf-ivory-esg-4' }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        decoded_data = codecs.decode(result, 'utf-8')
        json_data = json.loads(decoded_data)
        answer = json_data['answer']
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

    msg = answer
    st.session_state.messages.append({"role": "assistant", "question": msg, "chat_history": []})
    st.chat_message("assistant").write(msg)