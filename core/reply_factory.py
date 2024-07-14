from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not answer:
        return False, "Please provide an answer."

    # Store the answer in session
    session['answers'][current_question_id] = answer
    session.modified = True  # Ensure the session is marked as modified

    return True, "Answer recorded successfully."

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    PYTHON_QUESTION_LIST = [
        {'id': 1, 'text': 'Question 1', 'correct_answer': 'A'},
        {'id': 2, 'text': 'Question 2', 'correct_answer': 'B'},
        {'id': 3, 'text': 'Question 3', 'correct_answer': 'C'},
        # Add more questions as needed
    ]

    # Find the index of the current_question_id
    current_index = -1
    for index, question in enumerate(PYTHON_QUESTION_LIST):
        if question['id'] == current_question_id:
            current_index = index
            break

    # If current_question_id is not found, return an error or handle as needed
    if current_index == -1:
        return "Error: Current question not found in the list", -1

    # Determine the next question index
    next_index = current_index + 1

    # Check if next_index is within bounds
    if next_index < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_index]
        return next_question['text'], next_question['id']
    else:
        return None, -1  # No more questions

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    PYTHON_QUESTION_LIST = [
        {'id': 1, 'correct_answer': 'A'},
        {'id': 2, 'correct_answer': 'B'},
        {'id': 3, 'correct_answer': 'C'},
        # Add more questions as needed
    ]

    answers = session.get('answers', {})
    correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)

    for question in PYTHON_QUESTION_LIST:
        question_id = question['id']
        correct_answer = question['correct_answer']
        user_answer = answers.get(question_id)

        if user_answer == correct_answer:
            correct_answers += 1

    score = (correct_answers / total_questions) * 100
    result_message = f"Quiz completed! Your score: {correct_answers}/{total_questions} ({score:.2f}%)."

    return result_message

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        # Initialize answers in session
        session['answers'] = {}

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question_text, next_question_id = get_next_question(current_question_id)

    if next_question_text:
        bot_responses.append(next_question_text)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses
