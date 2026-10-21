import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, log_loss
from Features import build_features, X_COLS

def train_model(df, test_season=2025):
    played = df[df["result"].notna() & (df["result"] != 0)].dropna(subset=X_COLS)
    played = played.assign(home_win=(played["result"]>0).astype(int))

    train = played[played["season"]<test_season]
    test = played[played["season"]==test_season]

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=6,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(train[X_COLS], train["home_win"])
    return model,test

if __name__ == "__main__":
    df = build_features()
    model, test = train_model(df)

    probs = model.predict_proba(test[X_COLS])[:, 1]

    metrics = pd.DataFrame({
        "Metric": ["Model accuracy", "Model log loss", "Vegas baseline", "Always pick home"],
        "Value": [
            accuracy_score(test["home_win"], probs > 0.5),
            log_loss(test["home_win"], probs),
            accuracy_score(test["home_win"], test["spread_line"] > 0),
            test["home_win"].mean(),
        ],
    }).round(3)

    imp = (pd.Series(model.feature_importances_, index=X_COLS)
           .sort_values(ascending=False).round(3)
           .rename_axis("Feature").reset_index(name="Importance"))

    print(metrics.to_markdown(index=False))
    print()
    print(imp.to_markdown(index=False))