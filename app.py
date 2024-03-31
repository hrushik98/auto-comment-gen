import streamlit as st
import pandas as pd
import os
from groq import Groq
import csv

st.sidebar.title('Hi, there!')
option = st.sidebar.selectbox('Select an option', ('Generate comments', 'Product/Service info'))

if 'problem_trying_to_solve' not in st.session_state:
    st.session_state['problem_trying_to_solve'] = ''
if 'how_product_helps' not in st.session_state:
    st.session_state['how_product_helps'] = ''
if 'unique_sell_prop' not in st.session_state:
    st.session_state['unique_sell_prop'] = ''
if 'how_to_contact_you' not in st.session_state:
    st.session_state['how_to_contact_you'] = ''

if option == 'Product/Service info':
    st.title('Product/Service info')
    st.markdown("**-------> Let's get some info about your product/service**")
    st.session_state['problem_trying_to_solve'] = st.text_area('What problem is your product/service trying to solve?', value=st.session_state['problem_trying_to_solve'])
    st.session_state['how_product_helps'] = st.text_area('How does your product/service help solve the problem?', value=st.session_state['how_product_helps'])
    st.session_state['unique_sell_prop'] = st.text_area('What is your unique selling proposition?', value=st.session_state['unique_sell_prop'])
    st.session_state['how_to_contact_you'] = st.text_area('How can people contact you?', value=st.session_state['how_to_contact_you'])

    if st.button('Save', key="save-btn"):
        st.write('Saved!')
        st.markdown('***Please note:*** This info is only saved for this session. If you close the page, you will need to enter the info again.')

if option == 'Generate comments':
    posts = st.file_uploader("Upload a CSV file containing two columns: postContent and linkedinUrl ", type=["csv"])
    groq_api = st.secrets['groq_api'] 

    if groq_api is not None:
        client = Groq(api_key=groq_api)

        if st.button('Generate comments'):
            if posts is not None:  # Check if a file is uploaded
                if os.path.exists("comments.csv"):
                    os.remove("comments.csv")

                with open("comments.csv", "a", newline='') as f:
                    datai = csv.writer(f)
                    datai.writerow(['postContent', 'linkedinUrl', 'comment'])
                    posts = pd.read_csv(posts)
                    for i in range(len(posts)):
                        post_content = posts['postContent'][i]
                        linkedin_url = posts['linkedinUrl'][i]

                        chat_completion = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "user",
                                    "content": f"""You are an expert marketer. Can you help me with some comments for my social media posts? I will give you the post content under which we are trying to generate a single comment to promote our product. Just give me the comment and nothing else. I will give you the post content, problem that we're trying to solve, how our product helps solve the problem and a Unique selling point for our product, and how the customer can contact us. You have to generate a single comment. Post content = {post_content} Problem = {st.session_state['problem_trying_to_solve']} How product helps = {st.session_state['how_product_helps']} Unique selling point = {st.session_state['unique_sell_prop']} How to contact = {st.session_state['how_to_contact_you']}"""
                            }],                                
                        
                            model="mixtral-8x7b-32768",
                        )

                        comment = chat_completion.choices[0].message.content
                        dataii = csv.writer(f)
                        dataii.writerow([post_content, linkedin_url, comment])

                to_display = pd.read_csv("comments.csv")
                st.write(to_display)
                st.download_button(
                    label="Download comments.csv",
                    data=to_display.to_csv(index=False),
                    file_name="comments.csv",
                    mime="text/csv",
                )
            else:
                st.warning("Please upload a CSV file to generate comments.")
    else:
        st.warning("Please enter your Groq API key to generate comments.")
