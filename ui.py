import PySimpleGUI as sg

class View():

    def __init__(self, quizz):
        self.quizz = quizz
        layout = [
            [sg.Text('Press Next to start Quizz', key='question', size=(40, 1))],
            [sg.InputText(key='0', visible=False)]  + [sg.Radio('', "Radio1", key=str(i), visible=False) for i in range(1, 6)],
            [sg.Button('Next')]
        ]
        self.window = sg.Window('Application', layout, element_justification='l')
        event, values = self.window.read()


    def show_close_question(self, question):
        qtxt = self.quizz[question.code_question]['txt']
        self.window.FindElement('question').update(qtxt)

        for i, code in enumerate(question.next_questions, start=1):
            cb = self.window.FindElement(str(i))
            cb.update(text=self.quizz[question.code_question]['answers'][code], visible=True)
            cb.acode = code


    def show_open_question(self, question):
        qtxt = self.quizz[question.code_question]['txt']
        self.window.FindElement('question').update(qtxt)
        self.window.FindElement('0').update(visible=True)


    def hide_all(self):
        self.window.FindElement('0').update('', visible=False)
        for i in range(1, 6):
            self.window.FindElement(str(i)).update(visible=False, value=False, text='')


    def get_answer(self):
        event, values = self.window.read()
        
        if event == 'Next':
            # Return txt from user
            if values['0']:
                return values['0']

            # Return answer code
            for key in values:
                if values[key]:
                    return self.window.FindElement(key).acode