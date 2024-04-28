import streamlit as st
from github_repo_fetcher import GitHubRepoFetcher  # Ensure this is correctly imported

# Streamlit app title
st.title("GitHub Repository Code Viewer with Expandable Sections")

# Text inputs for GitHub username, repository name, file extensions, and optional personal access token
owner = st.text_input("GitHub Username", "octocat")
repo = st.text_input("Repository Name", "Hello-World")
extensions_input = st.text_input("File Extensions (comma-separated)", ".py, .md")
token = st.text_input("GitHub Personal Access Token (optional)", type="password")

# Button to fetch files with specified extensions
if st.button("Fetch Repository Contents"):
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

            # Display the list of all file paths in an expandable section with bullet points
            with st.expander("Files in Repository"):
                # Using a formatted string for better readability
                file_list = "\n".join([f"- {file}" for file in list_all_files])
                st.text(file_list)  # Displaying as plain text for bullet points        

            # Display fetched contents in expandable sections
            for file_path, content in list_of_contents.items():
                with st.expander(f"File: {file_path}"):
                    st.code(content, language="python", line_numbers=True)
                    st.write("-" * 50)  # Separator in Streamlit


    except Exception as e:
        # Handle errors and display user-friendly messages
        st.error(f"An error occurred while fetching contents: {str(e)}")
