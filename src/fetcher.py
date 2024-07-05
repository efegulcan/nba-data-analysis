import os
import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams

teams_abbr = [
    'ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
    'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
    'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
]

team_name_mapping = {
    'ATL': 'Atlanta Hawks',
    'BOS': 'Boston Celtics',
    'BRK': 'Brooklyn Nets',
    'CHI': 'Chicago Bulls',
    'CHO': 'Charlotte Hornets',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHO': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards'
}

def fetch_team_salary_data(team_abbr):
    url = f'https://www.basketball-reference.com/contracts/{team_abbr}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'contracts'})

    if table is None:
        logging.error(f"Could not find the contracts table for {team_abbr} on the page")
        return None
    
    team_totals_row = table.find('th', text='Team Totals').find_parent('tr')
    salary_cell = team_totals_row.find('td', {'data-stat': 'y1'})
    salary = salary_cell.text.strip().replace('$', '').replace(',', '')

    if salary.isnumeric():
        return {'team': team_name_mapping[team_abbr], 'salary': int(salary)}
    else:
        logging.error(f"Invalid salary value for {team_abbr}")
        return None

def fetch_all_salaries():
    if os.path.exists('data/nba_salaries.csv'):
        logging.info("Salary data already exists. Skipping fetching.")
        return pd.read_csv('data/nba_salaries.csv')

    all_salaries = []
    for team_abbr in teams_abbr:
        team_salary_data = fetch_team_salary_data(team_abbr)
        if team_salary_data:
            all_salaries.append(team_salary_data)
            logging.info(f"Fetched data for {team_abbr}")

    salaries_df = pd.DataFrame(all_salaries)
    os.makedirs('data', exist_ok=True)
    salaries_df.to_csv('data/nba_salaries.csv', index=False)
    logging.info("Salary data saved to data/nba_salaries.csv")
    return salaries_df


def fetch_nba_wins_data(year):
    if os.path.exists('data/nba_wins.csv'):
        logging.info("Wins data already exists. Skipping fetching.")
        return pd.read_csv('data/nba_wins.csv')

    nba_teams = teams.get_teams()
    teams_df = pd.DataFrame(nba_teams)

    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=year, season_type_nullable='Regular Season')
    games = gamefinder.get_data_frames()[0]

    wins_df = games[games['WL'] == 'W'].groupby('TEAM_ID').size().reset_index(name='wins')
    wins_df = wins_df.merge(teams_df[['id', 'full_name']], left_on='TEAM_ID', right_on='id')
    wins_df = wins_df[['full_name', 'wins']]
    wins_df.columns = ['team', 'wins']

    os.makedirs('data', exist_ok=True)
    wins_df.to_csv('data/nba_wins.csv', index=False)
    logging.info("Wins data saved to data/nba_wins.csv")

    return wins_df

def combine_and_save_data(year):
    wins_df = fetch_nba_wins_data(year)
    salaries_df = fetch_all_salaries()

    data_df = wins_df.merge(salaries_df, on='team', how='inner')
    data_df['price_per_win'] = data_df['salary'] / data_df['wins']

    data_df.to_csv('data/nba_data.csv', index=False)
    logging.info("Combined data saved to data/nba_data.csv")

    logging.info(data_df)
    return data_df
