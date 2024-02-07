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

com_logo = '''<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 500 500.224">
  <g id="CoM_Logo" data-name="CoM Logo" transform="translate(22434 489)">
    <rect id="Rectangle_256" data-name="Rectangle 256" width="500" height="500" transform="translate(-22434 -489)" fill="none"/>
    <g id="CoM_Logo-2" data-name="CoM Logo" transform="translate(-22434.084 -471)">
      <g id="Clouds_On_Mars_Logotypes" data-name="Clouds On Mars Logotypes" transform="translate(0.085 0)">
        <path id="Path_92" data-name="Path 92" d="M437.741,17.63,300.823,170.1l-95.577-34.956L117.57,232.236l-50.127-13.97L6,270.922C77.909,385.7,228.058,422.493,344.884,353.954S502.851,136.4,437.741,17.63Z" transform="translate(31.392 93.813)" fill="#ff5719"/>
        <path id="Path_93" data-name="Path 93" d="M97.363,34.92H26.755a5.689,5.689,0,0,0,0,11.315H97.363a5.689,5.689,0,0,0,0-11.315Z" transform="translate(114.748 185.818)" fill="#ff5719"/>
        <path id="Path_94" data-name="Path 94" d="M5.175,46.235h81.1a5.689,5.689,0,0,0,0-11.315H5.175a5.689,5.689,0,0,0,0,11.315Z" transform="translate(-0.085 185.818)" fill="#ff5719"/>
        <path id="Path_95" data-name="Path 95" d="M180.861,38.81H7.406a5.626,5.626,0,1,0,0,11.252H180.861a5.626,5.626,0,0,0,0-11.252Z" transform="translate(8.936 206.517)" fill="#ff5719"/>
        <path id="Path_96" data-name="Path 96" d="M35.152,54h0a5.689,5.689,0,0,0,0-11.315H5.695A5.689,5.689,0,0,0,5.695,54Z" transform="translate(2.682 227.111)" fill="#ff5719"/>
        <path id="Path_97" data-name="Path 97" d="M105.7,42.68H16.825a5.689,5.689,0,0,0,0,11.315H105.7a5.689,5.689,0,0,0,0-11.315Z" transform="translate(61.908 227.111)" fill="#ff5719"/>
        <path id="Path_98" data-name="Path 98" d="M47.664,46.57H24.086a5.626,5.626,0,1,0,0,11.252H47.664a5.626,5.626,0,0,0,0-11.252Z" transform="translate(97.695 247.81)" fill="#ff5719"/>
        <path id="Path_99" data-name="Path 99" d="M50.884,46.57H11.566a5.626,5.626,0,1,0,0,11.252H50.884a5.626,5.626,0,0,0,0-11.252Z" transform="translate(31.073 247.81)" fill="#ff5719"/>
        <path id="Path_100" data-name="Path 100" d="M39.533,50.45H8.306a5.626,5.626,0,1,0,0,11.252H39.533a5.626,5.626,0,1,0,0-11.252Z" transform="translate(13.725 268.457)" fill="#ff5719"/>
        <path id="Path_101" data-name="Path 101" d="M100.934,34.92H49.985a5.689,5.689,0,0,0,0,11.315h50.949a5.689,5.689,0,0,0,0-11.315Z" transform="translate(238.36 185.818)" fill="#ff5719"/>
        <path id="Path_102" data-name="Path 102" d="M5.926,42.5H19.9a5.752,5.752,0,1,0,0-11.5H5.926a5.626,5.626,0,1,0,0,11.252Z" transform="translate(1.061 164.958)" fill="#ff5719"/>
        <path id="Path_103" data-name="Path 103" d="M303.008,31H16.656a5.626,5.626,0,1,0,0,11.252H303.008a5.626,5.626,0,0,0,0-11.252Z" transform="translate(58.158 164.958)" fill="#ff5719"/>
        <path id="Path_104" data-name="Path 104" d="M193.146,27.16H41.436a5.626,5.626,0,1,0,0,11.252h151.71a5.626,5.626,0,0,0,0-11.252Z" transform="translate(190.018 144.525)" fill="#ff5719"/>
        <path id="Path_105" data-name="Path 105" d="M6.656,38.412H108.618a5.626,5.626,0,0,0,0-11.252H6.656a5.626,5.626,0,1,0,0,11.252Z" transform="translate(4.945 144.525)" fill="#ff5719"/>
        <path id="Path_106" data-name="Path 106" d="M393.752,23.29H7.335a5.689,5.689,0,0,0,0,11.315H393.752a5.626,5.626,0,1,0,0-11.252Z" transform="translate(11.409 123.932)" fill="#ff5719"/>
        <path id="Path_107" data-name="Path 107" d="M99.012,19.4H67.406a5.626,5.626,0,1,0,0,11.252H99.012a5.626,5.626,0,0,0,0-11.252Z" transform="translate(328.211 103.232)" fill="#ff5719"/>
        <path id="Path_108" data-name="Path 108" d="M22.946,19.4a5.626,5.626,0,1,0,0,11.252H253.039a5.626,5.626,0,0,0,0-11.252Z" transform="translate(91.628 103.232)" fill="#ff5719"/>
        <path id="Path_109" data-name="Path 109" d="M394.068,21.136a5.626,5.626,0,0,0-5.689-5.626H17.2a5.626,5.626,0,1,0,0,11.252H388.379a5.626,5.626,0,0,0,5.689-5.626Z" transform="translate(61.031 82.532)" fill="#ff5719"/>
        <path id="Path_110" data-name="Path 110" d="M11.526,26.762H25.5a5.626,5.626,0,1,0,0-11.252H11.526a5.626,5.626,0,1,0,0,11.252Z" transform="translate(30.86 82.532)" fill="#ff5719"/>
        <path id="Path_111" data-name="Path 111" d="M14.306,22.882H187.255a5.626,5.626,0,0,0,0-11.252H14.306a5.626,5.626,0,1,0,0,11.252Z" transform="translate(45.653 61.886)" fill="#ff5719"/>
        <path id="Path_112" data-name="Path 112" d="M66.86,17.256a5.626,5.626,0,0,0,5.626,5.626H86.709a5.626,5.626,0,0,0,0-11.252H72.486A5.626,5.626,0,0,0,66.86,17.256Z" transform="translate(355.243 61.886)" fill="#ff5719"/>
        <path id="Path_113" data-name="Path 113" d="M123.865,22.882h0a5.626,5.626,0,1,0,0-11.252h-66.5a5.626,5.626,0,0,0,0,11.252Z" transform="translate(274.785 61.886)" fill="#ff5719"/>
        <path id="Path_114" data-name="Path 114" d="M19.306,18.992H346.683a5.626,5.626,0,1,0,0-11.252H19.306a5.626,5.626,0,1,0,0,11.252Z" transform="translate(72.259 41.186)" fill="#ff5719"/>
        <path id="Path_115" data-name="Path 115" d="M22.335,15.185H41.3a5.689,5.689,0,0,0,0-11.315H22.335a5.689,5.689,0,0,0,0,11.315Z" transform="translate(91.228 20.593)" fill="#ff5719"/>
        <path id="Path_116" data-name="Path 116" d="M63.065,15.185H80.2a5.689,5.689,0,0,0,0-11.315H63.065a5.689,5.689,0,0,0,0,11.315Z" transform="translate(307.962 20.593)" fill="#ff5719"/>
        <path id="Path_117" data-name="Path 117" d="M197.383,15.185h0a5.689,5.689,0,0,0,0-11.315H32.335a5.689,5.689,0,0,0,0,11.315Z" transform="translate(144.44 20.593)" fill="#ff5719"/>
        <path id="Path_118" data-name="Path 118" d="M30.106,11.252H62.534A5.626,5.626,0,0,0,62.534,0H30.106a5.626,5.626,0,0,0,0,11.252Z" transform="translate(129.728 0)" fill="#ff5719"/>
        <path id="Path_119" data-name="Path 119" d="M56.856,11.252H69.814A5.626,5.626,0,1,0,69.814,0H56.856a5.626,5.626,0,0,0,0,11.252Z" transform="translate(272.072 0)" fill="#ff5719"/>
        <path id="Path_120" data-name="Path 120" d="M40.866,11.252H120.2A5.626,5.626,0,0,0,120.2,0H40.866a5.626,5.626,0,1,0,0,11.252Z" transform="translate(186.985 0)" fill="#ff5719"/>
      </g>
    </g>
  </g>
</svg>'''
url = 'https://rg-com-innovation-hub-esg.swedencentral.inference.ml.azure.com/score'
api_key = st.secrets['api_key']

# api_key = ""
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# st.title("💬 Asystent")
st.markdown('<h1>{} Asystent</h1>'.format(com_logo), unsafe_allow_html=True)
st.caption("🚀 A streamlit chatbot powered by Clouds On Mars")
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
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key) }

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