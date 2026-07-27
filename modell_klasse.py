"""
modell_klasse.py
================
Definition der KrankenhausModell-Klasse.
Wird importiert in:
  - 03_Decision_Tree.ipynb  (Training + Speichern)
  - dashboard_utils.py       (Laden + Vorhersage)
"""

import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


class KrankenhausModell:
    """Wrapper-Klasse fuer den Krankenhaus-Qualitaets-Klassifikator."""

    FEATURE_COLS = ["SO.Betten", "SO.Uni", "fortbildungsquote", "aerzte_pro_bett"]
    TARGET_COL   = "hat_viele_Probleme"

    def __init__(self, max_depth=3, random_state=42):
        self.max_depth    = max_depth
        self.random_state = random_state
        self.model        = DecisionTreeClassifier(
            max_depth=max_depth, random_state=random_state
        )
        self.le           = LabelEncoder()
        self.feature_names = None

    def prepare(self, df: pd.DataFrame):
        """Features aufbereiten und fehlende Werte behandeln."""
        data = df.copy()
        traeger_col = [c for c in data.columns if "ger.Art" in c][0]
        data["traeger_enc"] = self.le.fit_transform(
            data[traeger_col].fillna("unbekannt")
        )
        cols = self.FEATURE_COLS + ["traeger_enc"]
        X = data[cols].fillna(data[cols].median())
        y = data[self.TARGET_COL]
        self.feature_names = cols
        return X, y

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        return self

    def evaluate(self, X_test, y_test):
        from sklearn.metrics import (
            accuracy_score, precision_score, recall_score,
            f1_score, confusion_matrix
        )
        y_pred = self.model.predict(X_test)
        return {
            "accuracy":  accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall":    recall_score(y_test, y_pred),
            "f1":        f1_score(y_test, y_pred),
            "cm":        confusion_matrix(y_test, y_pred),
            "y_pred":    y_pred,
        }

    def save(self, path="modell_krankenhaus.pkl"):
        joblib.dump(self, path)
        print(f"Modell gespeichert: {path}")

    @staticmethod
    def load(path="modell_krankenhaus.pkl"):
        return joblib.load(path)
