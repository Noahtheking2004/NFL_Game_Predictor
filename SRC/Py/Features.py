import sqlite3
import pandas as pd
from Config import DB_PATH

FEATS = ["off_epa", "off_success", "off_pass_epa", "off_rush_epa",
         "def_epa", "def_success", "def_pass_epa", "def_rush_epa"]
X_COLS = [f"diff_{f}" for f in FEATS] + ["rest_diff", "div_game"]


def build_features(db_path=DB_PATH, window=5):
    conn = sqlite3.connect(db_path)

    off = pd.read_sql_query("""
        SELECT game_id, season, week, posteam AS team,
               AVG(epa)     AS off_epa,
               AVG(success) AS off_success,
               AVG(CASE WHEN play_type = 'pass' THEN epa END) AS off_pass_epa,
               AVG(CASE WHEN play_type = 'run'  THEN epa END) AS off_rush_epa
        FROM pbp
        WHERE play_type IN ('pass', 'run') AND posteam IS NOT NULL
        GROUP BY game_id, season, week, posteam
    """, conn)

    dfn = pd.read_sql_query("""
        SELECT game_id, defteam AS team,
               AVG(epa)     AS def_epa,
               AVG(success) AS def_success,
               AVG(CASE WHEN play_type = 'pass' THEN epa END) AS def_pass_epa,
               AVG(CASE WHEN play_type = 'run'  THEN epa END) AS def_rush_epa
        FROM pbp
        WHERE play_type IN ('pass', 'run') AND defteam IS NOT NULL
        GROUP BY game_id, defteam
    """, conn)

    team_games = off.merge(dfn, on=["game_id", "team"])

    # Rolling form (last N games)
    team_games["t"] = team_games["season"] * 100 + team_games["week"]
    team_games = team_games.sort_values(["team", "t"])
    team_games[FEATS] = (team_games.groupby("team")[FEATS]
                         .transform(lambda s: s.rolling(window, min_periods=2).mean()))
    rolled = team_games[["team", "t"] + FEATS].sort_values("t")

    # Schedule = one game per row
    sched = pd.read_sql_query("""
    SELECT game_id,season,week,home_team, away_team,
    result, spread_line, home_rest,away_rest, div_game
    FROM schedules
    WHERE game_type = 'REG'
    """,conn
    )
    conn.close()
    sched["t"] = sched["season"] * 100 + sched["week"]
    sched = sched.sort_values("t")

    def attach(sched,side):
        r = rolled.rename(columns={c: f"{side}_{c}" for c in FEATS})
        r = r.rename(columns={"team": f"{side}_team"})
        #allow_exact_matches=False -> get only stats from strictly earlier weeks
        return pd.merge_asof(sched, r, on="t", by=f"{side}_team", allow_exact_matches=False)

    df = attach(attach(sched,"home"), "away")

    for f in FEATS:
        df[f"diff_{f}"] = df[f"home_{f}"] - df[f"away_{f}"]
    df["rest_diff"] = df["home_rest"] - df["away_rest"]

    return df