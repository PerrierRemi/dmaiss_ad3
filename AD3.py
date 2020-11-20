# Dependencies
import pandas as pd
from numpy import log2, unique

# Step 0 - Shannon Entropy Function
def shannon_entropy(array):
    pi = array.value_counts() / len(array)
    entropy = - (pi * log2(pi)).sum() # No log(0) in our case since a leaf will be created
    return entropy

# Step 1 - Compute dataset entropy
def dataset_entropy(dataset_, target):
    return shannon_entropy(dataset_[target])

# Step 2 - Compute attributes information
def attribute_entropy(dataset_, attribute, target):
    values_entropy = dataset_[[attribute, target]]\
        .groupby(attribute)\
        .apply(shannon_entropy)

    proportions = dataset_[attribute].value_counts() / len(dataset_)

    average_entropy = (proportions * values_entropy).sum()

    return average_entropy

# Step 3 - Pick attribute with highest gain
def highest_gain(dataset_, target):
    attributes = dataset_.columns.to_list()
    attributes.remove(target)

    ds_entropy = dataset_entropy(dataset_, target)

    res = pd.DataFrame(attributes, columns=['attribute'])
    res['entropy'] = res['attribute'].apply(lambda x: attribute_entropy(dataset_, x, target))
    res['gain'] = ds_entropy - res['entropy']

    best_attribute = res['attribute'][res['gain'].idxmax()]

    return best_attribute

# Together - Recursive tree creation
def create_tree(dataset_, target):
    best_attribute = highest_gain(dataset_, target)
    tree = {best_attribute: {}}

    for value in unique(dataset_[best_attribute]):
        # Get sub dataset
        sub_dataset_ = dataset_[dataset_[best_attribute] == value]
        sub_dataset_ = sub_dataset_.drop(best_attribute, axis=1)

        # Leaf ?
        if len(unique(sub_dataset_[target])) == 1:
            tree[best_attribute][value] = sub_dataset_[target].iloc[0]

        else:
            tree[best_attribute][value] = create_tree(sub_dataset_, target)

    return tree

# Bonus - Display tree
def tree_print(tree, level=0):
    ind, jonc = '│    ', '│───'
    if level == 0:
        root, = tree
        print(f'/{root}')
        tree_print(tree[root], 1)
    else:
        for value in tree:
            print(ind * (level - 1) + jonc + ' ' + value)
            if isinstance(tree[value], dict):
                tree_print(tree[value], level + 1)
            else:
                print(ind * level + jonc + ' ' + tree[value])

#tree_print()

