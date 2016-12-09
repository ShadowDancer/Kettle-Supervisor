from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold

def test_model(model, X, Y, folds = 5):
    cv = StratifiedKFold(n_splits=5)
    return cross_val_score(model, X, Y, cv=cv, n_jobs=-1);
    
def print_score(scores):
    return "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)

if __name__ == '__main__':
    
    from sklearn import svm
    from datetime import datetime
    from loader import Loader
    
    print str(datetime.now()) + " loading data"
    l = Loader();
    X, Y = l.load_data();   

    print str(datetime.now()) + " testing"
    scores = test_model(svm.SVC(C=1, kernel='linear'), X, Y)
    print str(datetime.now()) + " done"
    print print_score(scores)

