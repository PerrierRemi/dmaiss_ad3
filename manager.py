
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
        
        self.new_answer = False
        self.target_question = 'Q10'
        self.answers = {}


    def main(self):
        if len(self.data) > 15:
            tree = AD3.create_tree(self.data, self.target_question)
            AD3.tree_print(tree)
            self._smart_quizz(tree)

        else:
            self._all_quizz()

        self.app.upload_screen()

        self.db.add_answers(self.answers)
        self.db.update_quizz(self.quizz)
        self.app.window.close()


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
        answer = '' if answer is None else answer

        # Search for ID, if none create one

        for _code, _answer in question['answers'].items():
            if _answer == answer:
                return _code
        
        new_code = qcode + 'A' + str(len(question['answers'] + 1))
        question['answers'][new_code] = answer
        self.new_answer  = True

        return new_code

    def __close_question(self, question):
        self.app.show_close_question(question)
        answer = self.app.get_answer()
        return answer


    def _smart_quizz(self, tree):
        acode = self._question(tree.code_question)

        if self.new_answer:
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
        return


if __name__ == '__main__':
    m = Manager()
    m.main()