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
