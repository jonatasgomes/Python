import streamlit as st

# Define the questions and answers
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "What is the largest country in the world?",
        "options": ["Canada", "Russia", "China"],
        "answer": "Russia"
    },
    {
        "question": "What is the smallest country in the world?",
        "options": ["Monaco", "San Marino", "Vatican City"],
        "answer": "Vatican City"
    },
    {
        "question": "What is the highest mountain in the world?",
        "options": ["K2", "Mount Everest", "Kangchenjunga"],
        "answer": "Mount Everest"
    }
]

# Initialize session state
if "answers" not in st.session_state:
    st.session_state["answers"] = [None] * len(questions)

# Define the game logic
def play_game():
    # Display the questions
    for _i, _question in enumerate(questions):
        with st.expander(f"Question {_i + 1}"):
            answer = st.radio(f"{_question['question']}", _question["options"], key=f"question_{_i}")
            st.session_state.answers[_i] = answer

    # Button to verify answers
    st.markdown(
        """
        <style>
            div.stButton > button:first-child {
                background-color: #4CAF50;
                color: white;
                width: 100%;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                border: 2px solid #4CAF50;
                border-radius: 4px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button("Verify Answers"):
        score = 0
        for _i, _answer in enumerate(st.session_state.answers):
            if _answer == questions[_i]["answer"]:
                score += 1
                st.success(f"✅ Question {_i + 1}: Correct!")
            else:
                st.error(f"❌ Question {_i + 1}: Incorrect! The correct answer is {questions[_i]['answer']}")
        st.write(f"You got {score} out of {len(questions)} questions correct!")
        if score == len(questions):
            st.balloons()

# Run the Streamlit app
if __name__ == "__main__":
    st.title("Welcome to the Interactive Quiz Game!")
    st.write("Test your knowledge and have fun!")
    play_game()
