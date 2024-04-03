import streamlit as st
import requests
import re
    
def add_log(log: str):
    print(log)
    if st.session_state.logs is None:
        logs = [log]
        st.session_state.logs = logs
    else:
        st.session_state.logs.append(log)
        
def find(stringWithUrl: str):
  url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',stringWithUrl) 
  return url 

def get_encoded_url_string(stringWithUrl: str):
    newString = stringWithUrl
    newString = newString.replace('\n','<br/>')
    urlsFound = find(stringWithUrl=stringWithUrl)
    referenceUrls = list()
    for url in urlsFound:
        referenceUrls.append(f'<a href="{url}">{url}</a>')
    for index, url in enumerate(urlsFound):
        newString = newString.replace(url, referenceUrls[index])
    return newString

def show_negative_case_toast():
    st.toast('We have sent an email along with your query')

def main():
    st.set_page_config("Ask me any thing")
    st.header("Simplii 🤖")
        
    if "conservation" not in st.session_state:
        st.session_state.conservation = list()
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = requests.post('https://4b59-154-57-217-133.ngrok-free.app/question', json={'question': str(prompt)}, headers={'Content-Type': 'application/json'})
        json = response.json()
        last_answer = json["last_answer"]
        # last_answer = get_encoded_url_string(stringWithUrl=last_answer)
        st.session_state.messages.append({"role": "assistant", "content": last_answer})
        st.chat_message("assistant").write(last_answer)
        
        
    # input = st.text_input("Ask me anything")
    # if st.button("Send"):
    #     response = requests.post('http://localhost:5003/question', json={'question': str(input)}, headers={'Content-Type': 'application/json'})
    #     json = response.json()
    #     last_question = json["last_question"]
    #     last_answer = json["last_answer"]
    #     is_negative_case = json["is_negative_case"]
    #     last_answer = get_encoded_url_string(stringWithUrl=last_answer)
    #     st.session_state.conservation.insert(0, {"question": last_question, "answer": last_answer})
    #     if is_negative_case:
    #         show_negative_case_toast()
    #     for item in st.session_state.conservation:
    #         st.write(bot_template.replace("{{MSG}}", item["answer"]), unsafe_allow_html=True)
    #         st.write(user_template.replace("{{MSG}}", item["question"]), unsafe_allow_html=True)
        
            
                
if __name__ == '__main__':
    main()
