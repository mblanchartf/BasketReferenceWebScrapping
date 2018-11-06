from utils.scrapping_functions import *
import time
import argparse
import pandas as pd

# Arguments parser
parser = argparse.ArgumentParser(
        description='Extract statistics from Basket Reference: https://www.basketball-reference.com')
optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
required.add_argument('-f', '--function', required=True, type=str,
                      help='Function mode: nba_teams_info or team_player_info')
optional.add_argument('--t', '--team', nargs='?', dest='team',
                      default='LAL', type=str,
                      help='If function is team_player_info, team to analyze in string format')
optional.add_argument('--n', '--filename', nargs='?', dest='filename',
                      default='NBA_Scrapping.csv', type=str,
                      help='Filename for the CSV output file')
parser._action_groups.append(optional)

# Preparem les dades
args = parser.parse_args()
function = args.function
team = args.team
filename = args.filename
timestr = time.strftime("%Y%m%d%H%M%S_")
llista_equips_est = ['TOR', 'MIL', 'IND', 'BOS', 'PHI', 'CHA', 'DET', 'MIA', 'ORL', 'NJN', 'ATL', 'NYK', 'CHI', 'WAS', 'CLE']
llista_equips_oest = ['GSW', 'DEN', 'POR', 'SAS', 'SAC', 'LAC', 'OKC', 'MEM', 'HOU', 'NOH', 'LAL', 'UTA', 'MIN', 'DAL', 'PHO']

llista_equips = llista_equips_est + llista_equips_oest

# Apliquem la funció que se'ns passa com argument
if function == 'nba_teams_info':
    df = obten_informacio_equip(llista_equips)
    crea_fitxer_csv(df, timestr + "All_" + filename)
    
elif function == 'team_player_info':
    df = obten_estadistiques_jugadors_equip(team)
    crea_fitxer_csv(df, timestr + team + "_"+ filename)
    
else: 
    print('ERROR: Function not supported. Try with nba_teams_info or team_player_info')