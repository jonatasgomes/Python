import streamlit as st
import random

# Initialize game state on first run
if 'target' not in st.session_state:
    st.session_state.target = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False

st.title("Guess the Number Game")
st.write("I'm thinking of a number between 1 and 100. Can you guess it?")

# If the game is over, show a success message and a reset button
if st.session_state.game_over:
    st.success(f"Congratulations! You guessed the number in {st.session_state.attempts} attempts.")
    if st.button("Play Again"):
        # Reset the game state
        st.session_state.target = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
else:
    # Let the user input their guess
    guess = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)

    if st.button("Submit Guess"):
        st.session_state.attempts += 1

        if guess < st.session_state.target:
            st.info("Too low! Try again.")
        elif guess > st.session_state.target:
            st.info("Too high! Try again.")
        else:
            st.session_state.game_over = True
            st.success("That's correct!")
