import random
from Logistics import loading

class StudySystem:
    def __init__(self, question_file="assets/questions.json"):
        self.questions = loading.load_questions(question_file)
        self.current_question = None
        self.correct_answer = None
        self.reward_type = None

    def new_question(self):
        """Select a random question with random difficulty."""
        self.current_question = random.choice(self.questions)
        self.correct_answer = self.current_question["answer"]
        self.reward_type = self.current_question["difficulty"]
        return self.current_question

    def check_answer(self, selected_answer):
        """Return True if correct, else False."""
        return selected_answer == self.correct_answer
