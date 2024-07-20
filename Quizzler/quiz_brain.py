class QuizBrain:
    def __init__(self,all_questions) -> None:
        self.score = 0
        self.question_list = all_questions
        self.question_number = 0
        self.current_question = None
        self.current_options = None

    def still_has_questions(self):
        '''Checks if there are remaining questions in the list.'''
        return self.question_number < len(self.question_list)
    
    def next_question(self)->list:
        '''Proceeds to the next question in the list.'''
        self.current_question = self.question_list[self.question_number]
        q_question = self.current_question.question
        self.current_options = self.question_list[self.question_number].options
        self.question_number += 1
        return f"Q.{self.question_number}: {q_question}", self.current_options
    
    def get_correct_ans(self):
        '''Return correct answer of existing question.'''
        return self.current_question.answer

    def check_answer(self, user_answer: str)->bool:
        '''Checks if the user answer is correct.'''
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            return True
        else:
            return False
