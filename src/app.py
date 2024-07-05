from fetcher import fetch_all_salaries, fetch_nba_wins_data, combine_and_save_data
from visualize import visualize_price_per_win
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    year = '2022-23'
    fetch_all_salaries()
    fetch_nba_wins_data(year)
    combine_and_save_data(year)
    logging.info("All data fetching and processing steps completed successfully.")
    visualize_price_per_win()
    logging.info("Visualization completed successfully.")

if __name__ == "__main__":
    main()
