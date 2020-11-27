import PySimpleGUI as sg

class View():

    def __init__(self):
        layout = [
            [sg.Text('Press Next to start Quizz', key='question', size=(60, 1))],
            [sg.InputText(key='0', visible=False), sg.Column([[sg.Radio('', "Radio1", key=str(i), visible=False)] for i in range(1, 6)], key='c')], 
            [sg.Button('Next')]
        ]
        self.window = sg.Window('Application', layout, size=(400, 250))
        event, values = self.window.read()


    def show_close_question(self, question):
        self.hide_all()
        qtxt = question['txt']
        self.window.FindElement('question').update(qtxt)

        self.window.FindElement('c').update(visible=True)
        for i, code in enumerate(question['answers'], start=1):
            cb = self.window.FindElement(str(i))
            cb.update(text=question['answers'][code], visible=True)
            cb.acode = code


    def show_open_question(self, question):
        self.hide_all()
        qtxt = question['txt']
        self.window.FindElement('question').update(qtxt)
        self.window.FindElement('0').update(visible=True)
        # Show/Hide to move text box to the left
        self.window.FindElement('c').update(visible=True)
        self.window.FindElement('c').update(visible=False)


    def upload_screen(self):
        self.hide_all()
        self.window.FindElement('question').update('Uploadind your answers... Thank you!')

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