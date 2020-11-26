"""TKinter"""

import PySimpleGUI as sg

# Etienne code

sg.theme('DarkAmber')

layout =  [
    [sg.Text('How would you rate the trip price ?', key = 'question')],
    [sg.Radio('cheap', "Radio1", key = '1'), sg.Radio('normal price', "Radio1", key = '2'), sg.Radio('over priced', "Radio1", key = '3'), sg.Radio('other', "Radio1", key = '4')],
    [sg.Button('Save'), sg.Button('Next'), sg.Button('Exit')]

]

# Display the window and get values
count = 1

window = sg.Window('Question form', layout)
while (count < 11) :                             # The Event Loop
    event, values = window.read() 
    print(event, values)   
    if event == 'Next':
        count +=1
        window.FindElement('question').update(count)
        window.FindElement('1').update('')
        window.FindElement('2').update('')
        window.FindElement('3').update('')
        window.FindElement('4').update('')
    if event == sg.WIN_CLOSED or event == 'Exit':
        break      

window.close()

# Class to complete

class View():

    def __init__(self):
        # Create window
        pass

    def show_close_question(self, question):
        # Question
        # Possible answers (checkbox or dropdown menu)
        pass

    def show_open_question(self, question):
        # Question
        # Text input
        pass

    def get_answer(self):
        # get answer from participant
        pass

