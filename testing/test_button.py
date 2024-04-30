import streamlit as st

# Custom CSS to inject for making buttons bigger
css = """
<style>
.stButton>button {
    background-image: url('http://www.clker.com/cliparts/5/A/k/D/X/A/stop-button-md.png');
    width: 200px !important;
    height: 200px !important;
    background-size: cover; /* Cover the entire area of the button */
    border: none;
}
</style>
"""

# Inject custom CSS with markdown
st.markdown(css, unsafe_allow_html=True)

# Example button
if st.button(' '):
    st.success("You clicked the big button!")
