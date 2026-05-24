import pandas as pd
import joblib

from sklearn.datasets import load_breast_cancer

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

from sklearn.svm import SVC

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier

from xgboost import XGBClassifier

# LOAD DATASET

cancer = load_breast_cancer()

df = pd.DataFrame(
    cancer.data,
    columns=cancer.feature_names
)

df['target'] = cancer.target

important_features = [

    'mean radius',
    'mean texture',
    'mean perimeter',
    'mean area',
    'mean concavity',

    'worst radius',
    'worst perimeter',
    'worst area'
]

X = df[important_features]

y = df['target']

# SPLIT

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)

# SCALE

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

# MODELS

svm_model = SVC(probability=True)

rf_model = RandomForestClassifier(
    n_estimators=500
)

xgb_model = XGBClassifier(
    eval_metric='logloss'
)

# ENSEMBLE

ensemble_model = VotingClassifier(

    estimators=[

        ('svm', svm_model),

        ('rf', rf_model),

        ('xgb', xgb_model)

    ],

    voting='soft'
)

# TRAIN

ensemble_model.fit(
    X_train_scaled,
    y_train
)

# SAVE

joblib.dump(
    ensemble_model,
    "models/ensemble_model.pkl"
)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)

joblib.dump(
    important_features,
    "models/important_features.pkl"
)

print("Extreme AI Model Saved")