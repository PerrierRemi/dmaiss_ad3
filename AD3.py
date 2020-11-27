# Dependencies
import pandas as pd
from numpy import log2, unique


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


    # Bonus - Display tree
    @staticmethod
    def tree_print(tree, level=0):
        if tree.is_terminal():
            print(f"{'  ' * level}{tree.prediction}")

        else:
            print(f"{'  ' * level}{tree.code_question}")
            for answer in tree.next_questions:
                print(f"{'  ' * (level+1)}{answer}")
                AD3.tree_print(tree.next_questions[answer], level+2)
    

class Node():
    def __init__(self, code_question, prediction=None):
        self.code_question = code_question
        self.next_questions = {} # Mapping answer_code -> Node
        self.prediction = prediction # If node is terminal, expected answer_code to last question

    def is_terminal(self):
        return bool(self.code_question)

    def is_answer_know(self, answer_code):
        return answer_code in self.next_questions

