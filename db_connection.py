"""Manage connection to FireBase database."""

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