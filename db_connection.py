"""Manage connection to FireBase database."""
from firebase import firebase

# Etienne code

firebase = firebase.FirebaseApplication("https://dmaiss-ad3-db.firebaseio.com/", None)

data = {
    'Answers' : ['Q1A1', 'Q2A2']
}
#Write the answers in a new users
post_result = firebase.post('/Users/', data)
print("Well posted ! Don't spam post !")

# Return {'answers': [{'Q1A1': 'Cheap'}, {'Q1A2': 'Normal price'}, {'Q1A3': 'Over priced '}], 'question_type': 'close', 'txt': 'How would you rate the trip price ?'}
get_result = firebase.get('Q1','')
print(get_result)


# Class to complete

class FireConnection():
    
    def __init__(self):
        pass

    
    def open(self):
        # Establish connection
        pass

    def get_data(self):
        # Return pd.DataFrame (or json) of answers from all participants
        pass

    def get_quizz(self):
        # Return quizz json (if we stock it online)
        pass


    def update_answers(self, data):
        # Add participant answer to DB
        pass

    def update_quizz(self, data):
        # Update quizz (add new answer to open questions)
        pass
    
    def close(self):
        # Close connection
        pass