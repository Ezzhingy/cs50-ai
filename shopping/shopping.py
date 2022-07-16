import csv
import sys
import datetime

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 shopping.py shopping.csv")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)

    predictions = model.predict(X_test)

    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - ** Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence_lst = []
    label_lst = []

    with open(filename) as file_in:
        reader = csv.reader(file_in)
        file_in.readline()

        for line in reader:    
            evidence = []
            evidence.append(int(line[0]))
            evidence.append(float(line[1]))
            evidence.append(int(line[2]))
            evidence.append(float(line[3]))
            evidence.append(int(line[4]))
            evidence.append(float(line[5]))
            evidence.append(float(line[6]))
            evidence.append(float(line[7]))
            evidence.append(float(line[8]))
            evidence.append(float(line[9]))
            
            # get month number
            month_name = line[10]
            if month_name == "June": month_name = "Jun"
            datetime_object = datetime.datetime.strptime(month_name, "%b")
            month_number = datetime_object.month - 1
            evidence.append(int(month_number))
            
            evidence.append(int(line[11]))
            evidence.append(int(line[12]))
            evidence.append(int(line[13]))
            evidence.append(int(line[14]))
            
            # get visitor 0 1
            visitor_type = line[15]
            visitor = 1 if visitor_type == "Returning_Visitor" else 0   
            evidence.append(int(visitor))

            # get if weekend
            weekend_type = line[16]
            weekend = 1 if weekend_type == "TRUE" else 0
            evidence.append(int(weekend))

            evidence_lst.append(evidence)

            # get label
            label_type = line[17]
            label = 1 if label_type == "TRUE" else 0
            label_lst.append(int(label))


    return (evidence_lst, label_lst)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    actual_pos = 0
    actual_neg = 0
    total_pos = 0
    total_neg = 0

    for actual, predicted in zip(labels, predictions):

        if actual == predicted and actual == 1:
            actual_pos += 1
            total_pos += 1
        elif actual == predicted and actual == 0:
             actual_neg += 1
             total_neg += 1
        elif actual == 1:
            total_pos += 1
        elif actual == 0:
            total_neg += 1
    
    sensitivity = actual_pos / total_pos
    specificity = actual_neg / total_neg

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
