""" AD3 algorithm implementation."""

# Dependencies
import pandas as pd
from numpy import log2, unique
import PySimpleGUI as sg
from firebase import firebase


class AD3():
    # Step 0 - Shannon Entropy Function
    @staticmethod
    def shannon_entropy(array):
        pi = array.value_counts() / len(array)
        entropy = - (pi * log2(pi)).sum() # No log(0) in our case since a leaf will be created
        return entropy

    # Step 1 - Compute dataset entropy
    @staticmethod
    def dataset_entropy(dataset_, target):
        return AD3.shannon_entropy(dataset_[target])

    # Step 2 - Compute attributes information
    @staticmethod
    def attribute_entropy(dataset_, attribute, target):
        values_entropy = dataset_[[attribute, target]]\
            .groupby(attribute)\
            .apply(AD3.shannon_entropy)

        proportions = dataset_[attribute].value_counts() / len(dataset_)

        average_entropy = (proportions * values_entropy).sum()

        return average_entropy

    # Step 3 - Pick attribute with highest gain
    @staticmethod
    def highest_gain(dataset_, target):
        attributes = dataset_.columns.to_list()
        attributes.remove(target)

        ds_entropy = AD3.dataset_entropy(dataset_, target)

        res = pd.DataFrame(attributes, columns=['attribute'])
        res['entropy'] = res['attribute'].apply(lambda x: AD3.attribute_entropy(dataset_, x, target))
        res['gain'] = ds_entropy - res['entropy']

        best_attribute = res['attribute'][res['gain'].idxmax()]

        return best_attribute

    # Together - Recursive tree creation
    @staticmethod
    def create_tree(dataset_, target):
        best_attribute = AD3.highest_gain(dataset_, target)
        tree = Node(best_attribute)

        for value in unique(dataset_[best_attribute]):
            # Get sub dataset
            sub_dataset_ = dataset_[dataset_[best_attribute] == value]
            sub_dataset_ = sub_dataset_.drop(best_attribute, axis=1)

            # Leaf ?
            if len(unique(sub_dataset_[target])) == 1:
                tree.next_questions[value] = Node(None, prediction=sub_dataset_[target].iloc[0])

            else:
                tree.next_questions[value] = AD3.create_tree(sub_dataset_, target)

        return tree
    
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
    
    firebase = firebase.FirebaseApplication("https://dmaiss-ad3-db.firebaseio.com/", None)
    
    data = {
        'Answers' : ['Q1A1', 'Q2A2']
    }
    #Write the answers in a new users
    post_result = firebase.post('/Users/', data)
    print("Well posted ! Don't spam post !")

    #Return {'answers': [{'Q1A1': 'Cheap'}, {'Q1A2': 'Normal price'}, {'Q1A3': 'Over priced '}], 'question_type': 'close', 'txt': 'How would you rate the trip price ?'}
    get_result = firebase.get('Q1','')
    print(get_result)
    

class Node():
    def __init__(self, code_question, prediction=None):
        self.code_question = code_question
        self.next_questions = {} # Mapping answer_code -> Node
        self.prediction = prediction # If node is terminal, expected answer_code to last question

    def is_terminal(self):
        return bool(self.code_question)

    def is_answer_know(self, answer_code):
        return answer_code in self.next_questions

