import PySimpleGUI as sg

# Etienne code

# sg.theme('DarkAmber')

# layout =  [
#     [sg.Text('How would you rate the trip price ?', key = 'question')],
#     [sg.InputText(key='0', visible = False), sg.Radio('cheap', "Radio1", key = '1'), sg.Radio('normal price', "Radio1", key = '2'), sg.Radio('over priced', "Radio1", key = '3'), sg.Radio('other', "Radio1", key = '4')],
#     [sg.Button('Save'), sg.Button('Next'), sg.Button('Exit')]

# ]

# # Display the window and get values
# count = 1

# window = sg.Window('Question form', layout)
# while (count < 11) :                             # The Event Loop
#     event, values = window.read() 
#     print(event, values)   
#     if event == 'Next':
#         count +=1
#         window.FindElement('question').update(count)
#         window.FindElement('1').update(visible=False)
#         window.FindElement('2').update('')
#         window.FindElement('3').update('')
#         window.FindElement('4').update('')
#         window.FindElement('0').update(visible = True)
#     if event == sg.WIN_CLOSED or event == 'Exit':
#         break      

# window.close()

# Class to complete

class View():

    def __init__(self, quizz):
        self.quizz = quizz
        layout = [
            [sg.Text('Press Next to start Quizz', key='question', size=(25,1))],
            [sg.InputText(key='0', visible=False)]  + [sg.Radio('', "Radio1", key=str(i), visible=False) for i in range(1, 6)],
            [sg.Button('Next')]
        ]
        self.window = sg.Window('Application', layout)
        event, values = self.window.read()
        print('end')


    def show_close_question(self, question):
        qtxt = self.quizz[question.code_question]['txt']
        self.window.FindElement('question').update(qtxt)

        for i, code in enumerate(question.next_questions, start=1):
            cb = self.window.FindElement(str(i))
            cb.update(self.quizz[question.code_question]['answers'][code], visible=True)
            cb.acode = code


    def show_open_question(self, question):
        qtxt = self.quizz[question.code_question]['txt']
        print(qtxt)
        self.window.FindElement('question').update(qtxt)
        self.window.FindElement('0').update(visible=True)


    def hide_all(self):
        for i in range(6):
            self.window.FindElement(str(i)).update(visible=False)


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