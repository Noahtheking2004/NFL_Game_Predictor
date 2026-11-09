# NFL Game Predictor

This project is currently a work in progress, but I am using the NFLreadpy package to pull data and apply different machine learning programs to it to predict games outcomes and later will add intoduction of fantasy scores to see chances of a certain team winning over the others
## Model Results (2025 test season)
|Metric|Value|
| ---- | ---- |
|Model accuracy|0.649|
|Model log loss|0.626|
|Vegas baseline|0.653|
|Always pick home|0.539|

## Feature importance
|Feature|Importance|
| ---- | ---- |
|diff_off_success|0.202|
|diff_off_epa|0.181|
|diff_off_rush_epa|0.092|
|diff_off_pass_epa|.148|
|diff_def_epa|.107|
|diff_def_success|.089|
|diff_def_rush_epa|.086|
|diff_def_pass_epa|0.068|
|rest_diff|0.18|
|div_game|0.009|
Each of these features is a home team minus away team calculation


** Week 7 predictions

| Away | Home | Home Win Prob | Pick| Actual winner |
| ---- | ---- | -------------:| --- | ------------- |
|NE|CHI|0.473|NE| &cross;30-24 CHI |
|PIT|NO|0.402|PIT| &check; 16-10 PIT|
|CIN|BAL|0.533|BAL|&cross; 35-13 CIN|
|TB|CAR|0.730|CAR|&cross; 43-13 TB|
|NYG|HOU|0.730|HOU|&cross; 27-21 NYG|
|IND|MIN|0.488|IND|&cross;16-10 MIN|
|MIA|NYJ|0.614|NYJ|&cross; 28-25 MIA|
|CLE|TEN|0.477|CLE|&check; 27-24 CLE|
|DEN|ARI|0.484|DEN|&check; 30-16 DEN|
|GB|DET|0.702|DET|&check; 20-17 DET|
|LA|LV|0.313|LA|&check; 35-21 LAR|
|KC|SEA|0.346|KC|&cross; 20-3 SEA|
|DAL|PHI|0.318|DAL|&check; 38-21 DAL|

6/13 = 46.1%


## Week 8 Predictions

| Away | Home | Home Win Prob | Pick | Actual Winner |
|------|------|--------------:|------|---------------|
| CAR | GB  | 0.500 | GB  | &check; GB (27-19) |
| BAL | BUF | 0.638 | BUF | &check; BUF (36-10) |
| TEN | CIN | 0.860 | CIN | &check; CIN (43-36 OT) |
| ARI | DAL | 0.725 | DAL | &cross; ARI (33-30 OT) |
| MIN | DET | 0.764 | DET | &check; DET (19-15) |
| IND | JAX | 0.727 | JAX | &check; JAX (42-7) |
| LV  | NYJ | 0.637 | NYJ | &cross; LV (38-33) |
| CLE | PIT | 0.602 | PIT | &check; PIT (27-6) |
| ATL | TB  | 0.336 | ATL | &cross; TB (16-0) |
| LAC | LA  | 0.789 | LA  | &check; LA (24-9) |
| KC  | DEN | 0.350 | KC  | &cross; DEN (28-24) |
| NE  | MIA | 0.382 | NE  | &check; NE (24-19) |
| PHI | WAS | 0.695 | WAS | &check; WAS (27-10) |
| CHI | SEA | 0.462 | CHI | &check; CHI (34-17) |
10/4 =71.4%

## WEEK 9 Predictions 
|Away|home|Home win Prob|Pick|Actual Winner|
|----|----|-------------:|----|-------------|
|BUF|MIN|0.333|Buf||

Forgot to run before week school caught up to me
