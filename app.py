import streamlit as st

# Set the background color using CSS
background_color = """
<style>
body {
    background-color: lightgray;
}
</style>
"""

# Display the background color using markdown
st.markdown(background_color, unsafe_allow_html=True)

# Your Streamlit content here
st.title("My Streamlit App")
st.write("This is your app content.")

import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from dotenv import load_dotenv

# Load the Environment Variables
load_dotenv()
st.set_page_config(page_title="Amazon Product App")

# Sidebar contents
with st.sidebar:
    st.title('Amazon Product Related Queries App')
    st.markdown('''
    ## About
    This is a Review Sentiment Analysis and a chatbot for Amazon Product related queries.
    ''')
    menu = ['Amazon Review Sentiment Analysis', 'Product Queries BOT']
    choice = st.sidebar.selectbox("Select an option", menu)
    add_vertical_space(10)
    st.write('Made by [Hatim Contractor](https://github.com/hatimcontractor)')

st.header("Your Amazon Assistant")
st.divider()

def main():
    if choice == 'Amazon Review Sentiment Analysis':
        st.subheader("Amazon Review Sentiment Analysis")
        with st.form(key='my_form'):
            raw_text = st.text_area("Enter the Amazon review here:")
            submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            st.info("Sentiment:")
            answer = get_sentiment(raw_text)
            st.write(answer)
    elif choice == 'Product Queries BOT':
        st.subheader("Product Queries BOT")

        # Generate empty lists for generated and user.
        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hi, please ask your queries related to Amazon products?"]

        if 'user' not in st.session_state:
            st.session_state['user'] = ['Hi!']

        # Layout of input/response containers
        response_container = st.container()
        colored_header(label='', description='', color_name='blue-30')
        input_container = st.container()

        # Get user input
        def get_text():
            input_text = st.text_input("You: ", "", key="input")
            return input_text

        # Applying the user input box
        with input_container:
            user_input = get_text()

        def chain_setup():
            template = """Your are Amazon product-related query bot, so answer only product-related questions. If any other questions are asked, don't answer: {question}"""
            prompt = PromptTemplate(template=template, input_variables=["question"])

            llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5", model_kwargs={"max_new_tokens": 1200})

            llm_chain = LLMChain(llm=llm, prompt=prompt)
            return llm_chain

        # Generate response
        def generate_response(question, llm_chain):
            response = llm_chain.run(question)
            return response

        # Load LLM
        llm_chain = chain_setup()

        # Main loop
        with response_container:
            if user_input:
                response = generate_response(user_input, llm_chain)
                st.session_state.user.append(user_input)
                st.session_state.generated.append(response)

            if st.session_state['generated']:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state['user'][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))

if __name__ == '__main__':
    main()
