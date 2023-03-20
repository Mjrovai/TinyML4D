import streamlit as st

quote = st.radio("Select a quote from...",('Hamlet', 'Twelfth Night'))

if quote == 'Twelfth Night':
    text = """
    If music be the food of love, play on;
    Give me excess of it, that, surfeiting,
    The appetite may sicken, and so die.
    """
elif quote == "Hamlet":
    text = """
    To be, or not to be, that is the question:
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune,
    Or to take arms against a sea of troubles
    And by opposing end them.
    """

st.title(quote)
st.text(text)
