
import streamlit as st
from projects.cover_letter_generator.generator import CoverLetterGenerator

def main():

    # --- Streamlit page configuration ---

    # Set the title for the Streamlit app
    st.title("Cover Letter Generator")
    st.caption("A streamlit cover letter generator powered by OpenAI LLM")

    st.write('''
             1. Attach a resume as a PDF.

             2. Add a url for a job description.

             3. A cover letter will be generated for the role!''')


    st.divider()

    # Create a file uploader in the sidebar
    uploaded_file = st.file_uploader("Upload File", type="pdf")
    with st.form(key='my_form', clear_on_submit=False):
        user_input = st.text_input("Job Description URL:", placeholder="Add url to Job Description", key='input')
        submit_button = st.form_submit_button(label='Add')

        if user_input and submit_button:
            st.write('Job Description URL added!')
        elif submit_button and not user_input:
            st.write('Please add a url to a job description!')


    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()


    if uploaded_file and user_input:
        file_ingestor = CoverLetterGenerator(uploaded_file, user_input, openai_api_key)
        st.write(file_ingestor.cover_letter_generator())


if __name__ == "__main__":

    main()