from pokeembedding.nnet import NNet

import time
import csv
import numpy as np
import types
import random


def convert_embarked(embarked):
    if embarked == 'S':
        return 1
    elif embarked == 'Q':
        return 2
    elif embarked == 'C':
        return 3
    else:
        return -1

def convert_gender(gender):
    if gender == 'male':
        return 1
    elif gender == 'female':
        return 2
    else:
        return -1

def convert_title(title):
    if title == 'Mr':
        return 1
    elif title == 'Mrs':
        return 2
    elif title == 'Master':
        return 3
    elif title == 'Miss':
        return 4
    else:
        return -1


# Load the datasets
def load_dataset(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        data = [row for row in reader]

    selected_indices = [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    X_data = [[row[i] if row[i] != '' else 0 for i in selected_indices] for row in data]
    # Convert categorical features to numerical values
    X_embarked = [convert_embarked(row[2]) if row[2] != '' else -1 for row in data]
    X_gender = [convert_gender(row[7]) if row[7] != '' else -1 for row in data]
    X_title = [convert_title(row[12]) if row[12] != '' else -1 for row in data]
    # Replace the categorical features in the data
    for i, row in enumerate(X_data):
        row[2] = X_embarked[i]
        row[7] = X_gender[i]
        row[11] = X_title[i]
    X_data = [[row[i] for i in range(len(row)) if i not in [1,3,7,10]] for row in X_data]
    # Convert to numpy array
    X = np.array(X_data, dtype=np.float32)
    y = np.array([float(row[10]) if row[10] != '' else -1 for row in data], dtype=np.float32)  # Assuming the target variable is in the 11th column
    
    # Normalize the features between 0.0 and 1.0
    X_min = np.min(X, axis=0)
    X_max = np.max(X, axis=0)
    X_normalized = (X - X_min) / (X_max - X_min)

    # Shuffle the data
    indices = np.random.permutation(len(X_normalized))
    X_shuffled = X_normalized[indices]
    y_shuffled = y[indices]

    # Split the shuffled data into training and testing sets
    X_train = X_shuffled[:-300]
    X_test = X_shuffled[-300:]
    y_train = y_shuffled[:-300]
    y_test = y_shuffled[-300:]

    return X_train, X_test, y_train, y_test

def translate_expected(self, expected):
    return [expected]


def run():
        X_train, X_test, y_train, y_test = load_dataset("/Users/vasvamva1/Documents/pkm-ai/data/neural_net/train_clean.csv")
        input_size = X_train.shape[1]
        neural_network = NNet(input_size=input_size)
        neural_network.step = 3
        neural_network.batch_size = 10
        neural_network.epochs = 3
        # Test the train method
        neural_network.add_layer(30)
        neural_network.add_layer(10)
        neural_network.add_layer(1)
        neural_network.summary()
        neural_network.translate_expected = types.MethodType(translate_expected, neural_network)

        train(neural_network, X_train, y_train)
        test(neural_network, X_test, y_test, False)


def train(net, X_train, y_train):
        start_time = time.time()

        # Get images and iterate over epochs
        for epoch in range(net.epochs):
                for (features,output) in zip(X_train,y_train):
                        net.train(features, output)
                        # Monitor decreasing cost
                        if net.training_count % 100 == 0:
                                print(f"train {net.training_count}  Cost {net.cost:.5f}")

                print(f"epoch {epoch}  Cost {net.cost:.5f}")

        # Calculate and log the total training time
        train_time = time.time() - start_time
        print(f"Total training time: {train_time:.2f} seconds")


def test(net, X_test, y_test, show:bool=True):
    if show:
        print("check")
        start_time = time.time()

    correct = 0
    for features, expected_result in zip(X_test, y_test):
        result = net.check_output(features)
        if expected_result == result:
            correct += 1
        if show:
            print(f"{'check' if expected_result == result else 'MISS'} {expected_result} <=> {result} ")

    if show:
        print(f"Training iterations {net.training_count}")
        print(f"Training step: {net.step} BatchSize: {net.batch_size}")
    print(f"success rate {(correct / X_test.shape[0]):.3f}")
    if show:
        print(f"Avg Cost {net.cost:.5f}")
    
    print([node.bias for node in net.hidden_output_nodes])

if __name__== "__main__":
        run()
