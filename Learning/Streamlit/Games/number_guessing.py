import streamlit as st
import random

# Function to initialize or reset the game state
def initialize_game():
    if 'target_number' not in st.session_state:
        st.session_state.target_number = random.randint(1, 100)
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'guess' not in st.session_state:
        st.session_state.guess = None
    if 'message' not in st.session_state:
        st.session_state.message = ""

# Initialize the game
initialize_game()

# Streamlit app layout
st.title("Number Guessing Game")
st.write("Guess a number between 1 and 100!")

# Input for the user's guess
guess = st.number_input("Enter your guess:", min_value=1, max_value=100, value=st.session_state.guess)

# Button to submit the guess
if st.button("Submit Guess"):
    st.session_state.attempts += 1
    if guess < st.session_state.target_number:
        st.session_state.message = "Too low! Try again."
    elif guess > st.session_state.target_number:
        st.session_state.message = "Too high! Try again."
    else:
        st.session_state.message = f"Congratulations! You guessed the number in {st.session_state.attempts} attempts."
        st.balloons()  # Celebrate with balloons!
        # Reset the game after a correct guess
        st.session_state.target_number = random.randint(1, 100)
        st.session_state.attempts = 0

# Display the message
st.write(st.session_state.message)

# Display the number of attempts
st.write(f"Number of attempts: {st.session_state.attempts}")

# Button to reset the game
if st.button("Reset Game"):
    initialize_game()
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.guess = None
    st.session_state.message = ""
    st.experimental_rerun()
