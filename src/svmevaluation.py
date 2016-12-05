from loader import Loader
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn import svm



if __name__ == '__main__':
    param_grid = [{
           'C':  [0.001, 0.01, 0.1, 1, 10, 100, 1000], 
           'gamma': [1, 0.1, 0.001, 0.0001, 0.000001], 
           'kernel': ['rbf', 'poly', 'sigmoid']
           },]
    cv = StratifiedKFold(n_splits=5)
    svc = svm.SVC(cache_size=8000)
    scores = ['precision', 'recall']
    
    l = Loader()
    X, Y = l.load_data()

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()
        clf = GridSearchCV(estimator=svc, param_grid=param_grid, cv=cv, n_jobs=-1, scoring='%s_macro' % score, verbose=1)
        clf.fit(X, Y)
        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = Y, clf.predict(X)
        print(classification_report(y_true, y_pred))
        print()
