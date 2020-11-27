"""All together."""

"""
Objects to use :
    - Quizz ref (quizz.json) contains full text question, only code will be use in db and AD3
    - Tree object, to move from one question to another, construted from ID3 output

Algo :
    1. If less than 15 rows in dataset ask all question
    2. Else
        2.1. Ask questions in tree order
        2.2. If unknow answer ask all remaining questions
        2.3. Else ask results to db, check if expected answer is correct

Need to be done :
    - UI for open question | display text + txt inpu
    - UI for close question | display text + selection menu
    - DB connection
"""
import json

from ui import View
from AD3 import AD3, Node
from db_connection import FireConnection

class Manager():

    def __init__(self):
        self.db = FireConnection()
        self.quizz = self.db.get_quizz()
        self.data = self.db.get_data()

        self.app = View()
        
        self.target_question = 'Q10'
        self.answers = {}


    def main(self):
        if len(self.data) > 15:
            tree = AD3.create_tree(self.data)
            self._smart_quizz(tree)

        else:
            self._all_quizz()

        self.app.upload_screen()

        self.db.add_answers(self.answers)
        self.db.update_quizz(self.quizz)


    def _question(self, qcode):
        question = self.quizz[qcode]
        acode = None

        if question['question_type'] =='open': 
            acode = self.__open_question(question, qcode)

        if question['question_type'] == 'close': 
            acode = self.__close_question(question)

        self.answers[qcode] = acode

        return acode

    def __open_question(self, question, qcode):
        self.app.show_open_question(question)
        answer = self.app.get_answer()

        # Search for ID, if none create one

        for _code, _answer in question['answers'].items():
            if _answer == answer:
                return _code
        
        new_code = qcode + 'A' + str(len(question['answers']))
        question['answers'][new_code] = answer
        
        return new_code

    def __close_question(self, question):
        self.app.show_close_question(question)
        answer = self.app.get_answer()
        return answer


    def _smart_quizz(self, tree):
        acode = self._question(tree.code_question)

        if acode not in tree.next_questions:
            self._all_quizz()

        else:
            tree = tree.next_questions[acode]
            if tree.is_terminal():
                self._question(self.target_question) # Ask final question
            else:
                self._smart_quizz(tree)


    def _all_quizz(self):
        for qcode in sorted(list(self.quizz.keys())):
            if qcode in self.answers: # If unknow answer for open question ask every no-asked question
                continue
            self._question(qcode)


m = Manager()
m.main()