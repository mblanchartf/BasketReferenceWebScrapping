# Basket Reference Web Scrapping


This learning project pretends to scrap Basket reference webpage (https://www.basketball-reference.com) just to extract information about the NBA teams and about its palyers.
**Project done for "Tipologia i cicle de vide de les dades" course, part of the Data Science master perform in UOC.**

## Instructions

Install the needed libraries: 

```bash
pip install pandas
pip install request
pip install contextlib
pip install bs4
```

Then run the nba_scrapping.py script that has the following arguments: 

```bash
$ python nba_scrapping.py -h
usage: nba_scrapping.py [-h] -f FUNCTION [--t [TEAM]] [--n [FILENAME]]

Extract statistics from Basket Reference: https://www.basketball-reference.com

required arguments:
  -f FUNCTION, --function FUNCTION
                        Function mode: nba_teams_info or team_player_info

optional arguments:
  -h, --help            show this help message and exit
  --t [TEAM], --team [TEAM]
                        If function is team_player_info, team to analyze in
                        string format
  --n [FILENAME], --filename [FILENAME]
                        Filename for the CSV output file

```

### Examples

```bash
$ python nba_scrapping.py -f nba_teams_info
File created: 20181106185029_All_NBA_Scrapping.csv
```

All NBA teams CSV file screenshot: 
<img src=screenshots/ALL_data.JPG width=100% />

Source: https://www.basketball-reference.com/teams/

```bash
$ python nba_scrapping.py -f team_player_info  --t LAL
File created: 20181106190137_LAL_NBA_Scrapping.csv
```

Los Angeles Lakers CSV file screenshot: 
<img src=screenshots/LAL_data.JPG width=100% />

Source: https://www.basketball-reference.com/teams/LAL/2019.html

```bash
$ python nba_scrapping.py -f team_player_info  --t BOS
File created: 20181106184932_BOS_NBA_Scrapping.csv
```

Boston Celtics CSV file screenshot: 
<img src=screenshots/BOS_data.JPG width=100% />

Source: https://www.basketball-reference.com/teams/BOS/2019.html

```bash
$ python nba_scrapping.py -f team_player_info  --t GSW
File created: 20181106185000_GSW_NBA_Scrapping.csv
```

Golden State Warriors CSV file screenshot: 
<img src=screenshots/GSW_data.JPG width=100% />

Source: https://www.basketball-reference.com/teams/GSW/2019.html


## Authors

* **Marc Blanchart** - *Learning project* - [MarcBlanchart](https://github.com/mblanchartf)

