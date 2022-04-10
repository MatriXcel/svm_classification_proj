# -*- coding: utf-8 -*-
"""Selected_Topics_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XYRzgMOZ-JqbvtDbjSA8lvmmu_F9gDK8
"""


from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.dummy import DummyClassifier
import pandas as pd


from tqdm.auto import tqdm
# register `pandas.progress_apply` and `pandas.Series.map_apply` with `tqdm`
tqdm.pandas()



df_balanced = pd.read_csv('cleaned_balanced_df.csv')

bool_series = pd.notnull(df_balanced["text"]) 
    
# filtering data 
# displayind data only with Gender = Not NaN 
df_balanced = df_balanced[bool_series] 

grid_param = [
    {
    'tfidf__min_df': [5, 10],
    'tfidf__ngram_range': [(1, 3), (1, 6)],
    'LinearSVC__penalty': ['l2'],
    'LinearSVC__loss': ['hinge'],
    'LinearSVC__max_iter': [10000]
    }, 
    {
    'tfidf__min_df': [5, 10],
    'tfidf__ngram_range': [(1, 3), (1, 6)],
    'LinearSVC__C': [1, 10],
    'LinearSVC__tol': [1e-2, 1e-3]
    }
]



training_pipeline = Pipeline(
    steps=[('tfidf', TfidfVectorizer(stop_words="english")), 
           ('LinearSVC', LinearSVC(random_state=21, tol=1e-5, verbose=1))])

training_pipeline.get_params().keys()

gridSearchProcessor = GridSearchCV(estimator=training_pipeline,
                                   param_grid=grid_param,
                                   cv=5)

print("grid search linear svc started")
gridSearchProcessor.fit(df_balanced['text'], df_balanced['Priority'])

best_params = gridSearchProcessor.best_params_
print("Best alpha parameter identified by grid search ", best_params)

best_result = gridSearchProcessor.best_score_
print("Best result identified by grid search ", best_result)

# Best alpha parameter identified by grid search  
#{
    # 'LinearSVC__loss': 'hinge', 
    # 'LinearSVC__max_iter': 10000, 
    # 'LinearSVC__penalty': 'l2', 
    # 'tfidf__min_df': 10, 
    # 'tfidf__ngram_range': (1, 3)
#}
# Best result identified by grid search  0.45964912280701753

svc_training_pipeline = Pipeline(
    steps=[('tfidf', TfidfVectorizer(stop_words="english")), 
           ('SVC', SVC(random_state=21, tol=1e-5, verbose=1))])

tuned_parameters = [{
'tfidf__min_df': [5, 10],
'tfidf__ngram_range': [(1, 3), (1, 6)],
"SVC__C": [1,10,100,1000],
"SVC__kernel": ['rbf', 'linear'],
"SVC__gamma": [1e-3, 1e-4],
"SVC__tol": [1e-2, 1e-10]
}]

gridSearchProcessor_svc = GridSearchCV(estimator=svc_training_pipeline,
                                   param_grid=tuned_parameters,
                                   cv=5)

print("grid search svc started")

gridSearchProcessor_svc.fit(df_balanced['text'], df_balanced['Priority'])

svc_best_params = gridSearchProcessor_svc.best_params_
print("Best alpha parameter identified by grid search ", svc_best_params)

svc_best_result = gridSearchProcessor_svc.best_score_
print("Best result identified by grid search ", svc_best_result)