import nflreadpy as nfl
from Features import build_features, X_COLS
from Model import train_model

df = build_features()
model, _ = train_model(df)

season, week = nfl.get_current_season(), nfl.get_current_week()
upcoming = df[(df["season"] == season) & (df["week"] == week)
              & df["result"].isna()].dropna(subset=X_COLS)

if upcoming.empty:
    print(f"No predictable games for {season} week {week}")
else:
    upcoming = upcoming.assign(
        home_win_prob = model.predict_proba(upcoming[X_COLS])[:,1])

    print (f"week {week} predictions:")
    print(upcoming[["away_team", "home_team", "home_win_prob"]]
          .round(3).to_string(index=False))