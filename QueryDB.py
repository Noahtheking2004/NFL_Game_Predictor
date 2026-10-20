import sqlite3
import pandas as pd

conn = sqlite3.connect("nfl.db")

query = """
    SELECT posteam,
           COUNT(*) AS plays,
           ROUND(AVG(epa), 3) AS avg_epa
    FROM pbp
    WHERE season = 2026
      AND play_type IN ('pass', 'run')
    GROUP BY posteam
    ORDER BY avg_epa DESC
"""

df = pd.read_sql_query(query, conn)
print(df)

conn.close()