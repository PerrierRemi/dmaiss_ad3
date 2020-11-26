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
from ad3 import Node

class Manager():

    def __init__(self):
        self.quizz = json.load(open('quizz.json', 'r'))
        self.app = View(self.quizz)


    def show_question(self, qnode):
        type = self.quizz[qnode.code_question]['question_type']
        
        self.app.hide_all()

        if type =='open': 
            self.app.show_open_question(qnode)

        if type == 'close': 
            self.app.show_close_question(qnode)


    def all_quizz(self):
        for qcode in self.quizz:
            node = Node(qcode)
            node.next_questions = self.quizz[qcode]['answers']
            self.show_question(node)
            user_answer = self.app.get_answer()
            print(user_answer)


m = Manager()
m.all_quizz()