from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score
from sklearn.model_selection import cross_val_score


def model_metrics(y_test, y_pred):
    """
    This function is used to generate various metrics of the evaluation model, including accuracy,
    recall rate, F1 score, precision.

    Args:
        y_test: Real label of data.
        y_pred: The label of the data predicted by the model.

    Returns:
        Each evaluation index of the model, including accuracy, recall rate, F1 score, precision.
    """

    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred, average='weighted')
    f1score = f1_score(y_test, y_pred, average='weighted')
    precision = precision_score(y_test, y_pred, average='weighted')

    print("\n--------- Model Evaluation ---------")
    print('Accuracy score:', accuracy)
    print('Recall:', recall)
    print('F1-score:', f1score)
    print('Precision score:', precision)
    print('\n')

    return accuracy, recall, f1score, precision
