import sqlite3
import nflreadpy as nfl
from Config import DB_PATH

# ---------- Settings ----------
FIRST_SEASON = 2018
FULL_REBUILD = False   # True = use on the first run
                      # False = use this only from week to week

current = nfl.get_current_season()
all_seasons = list(range(FIRST_SEASON, current + 1))
print(f"Current season: {current}")

conn = sqlite3.connect(DB_PATH)


def table_exists(name):
    return conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone() is not None


def save(df, table, seasons):
    """Write a Polars DataFrame to SQLite without creating duplicate rows."""
    pdf = df.to_pandas()
    if FULL_REBUILD or not table_exists(table):
        pdf.to_sql(table, conn, if_exists="replace", index=False, chunksize=50000)
    else:
        marks = ",".join("?" * len(seasons))
        conn.execute(f"DELETE FROM {table} WHERE season IN ({marks})", seasons)
        conn.commit()
        pdf.to_sql(table, conn, if_exists="append", index=False, chunksize=50000)
    print(f"Saved {table}: {len(pdf)} rows")


# Which seasons to download this run
seasons = all_seasons if FULL_REBUILD else [current]
print(f"Downloading seasons: {seasons[0]}-{seasons[-1]}")

# ---------- Play-by-play (only the columns the model needs) ----------
pbp = nfl.load_pbp(seasons).select(
    ["game_id", "season", "week", "posteam", "defteam", "play_type", "epa", "success"]
)
save(pbp, "pbp", seasons)

# player stats
stats = nfl.load_player_stats(seasons)
save(stats, "player_stats", seasons)

# scheduless
schedules = nfl.load_schedules(all_seasons)
schedules.to_pandas().to_sql("schedules", conn, if_exists="replace", index=False)
print(f"Saved schedules: {schedules.height} rows")

# indexes to speed up the queries
conn.execute("CREATE INDEX IF NOT EXISTS idx_pbp_game ON pbp(game_id)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_pbp_season ON pbp(season, week)")
conn.commit()

conn.close()
print("Done!")