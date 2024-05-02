import streamlit as st
from github_repo_fetcher import GitHubRepoFetcher
from llm import llm

# Streamlit app title
tab1, tab2 = st.tabs(["Github repo", "Code Documentation"])


with tab1:
    st.title("GitHub Repository Code Viewer with Expandable Sections")
    # Text inputs for GitHub username, repository name, file extensions, and optional personal access token
    with st.sidebar:
        owner = st.text_input("GitHub Username", "anurag-singh-9622")
        repo = st.text_input("Repository Name", "code_doc_parody")
        extensions_input = st.text_input("File Extensions (comma-separated)", ".py, .md")
        token = st.text_input("GitHub Personal Access Token (optional)", type="password", value='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')
        api_key = st.text_input("OpenAI api key", type="password", value='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')
        submitted = st.checkbox("Fetch Repository Contents")

    # Button to fetch files with specified extensions
    if submitted:
        try:
            # Convert extensions input into a list
            extensions = [ext.strip() for ext in extensions_input.split(",")]

            # Create GitHubRepoFetcher instance
            fetcher = GitHubRepoFetcher(owner, repo, token)

            # Fetch files from the repository with the specified extensions
            fetcher.fetch_files(extensions)

            # Retrieve fetched contents and all file paths
            list_of_contents = fetcher.get_contents()
            list_all_files = fetcher.get_all_files()

            if list_of_contents:
                st.header(f"Contents of Repository: {repo}")

            # if list_all_files:
            #     # Display the list of all file paths in an expandable section
            #     with st.expander("All Files in Repository"):
            #         st.write(", ".join(list_all_files))
            if list_all_files:
                st.header("All Files in Repository")
                options = st.multiselect(
                    'Select the files', list_all_files, placeholder="Choose one or more files"
                    )

                # Display the list of all file paths in an expandable section with bullet points
                with st.expander("Files in Repository"):
                    # Using a formatted string for better readability
                    file_list = "\n".join([f"- {file}" for file in list_all_files])
                    st.text(file_list)  # Displaying as plain text for bullet points        

                # Display fetched contents in expandable sections
                for file_path, content in list_of_contents.items():
                    if file_path in options:
                        with st.expander(f"File: {file_path}"):
                            st.code(content, language="python", line_numbers=True)
                            st.write("-" * 50)  # Separator in Streamlit
                submitted_to_llm = st.checkbox('Create Documentation')
                        


        except Exception as e:
            # Handle errors and display user-friendly messages
            st.error(f"An error occurred while fetching contents: {str(e)}")

        if submitted_to_llm:
            with tab2:
                doc_assistant = llm(api_key=api_key)
                total_tokens = 0
                for file_path, content in list_of_contents.items():
                    if file_path in options:
                        response = doc_assistant.generate_documentation(content)
                        total_tokens += response.usage.total_tokens
                        response = response.choices[0].message.content
                        with st.expander(f"File: {file_path}"):
                            response
                            st.write("-" * 50)  # Separator in Streamlit
                with st.sidebar:
                    f"total_tokens: {total_tokens}"