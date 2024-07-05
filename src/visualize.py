import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_price_per_win():

    data_df = pd.read_csv('data/nba_data.csv')

    data_df['price_per_win_million'] = data_df['price_per_win'] / 1e6

    data_df = data_df.sort_values(by='price_per_win_million', ascending=False)

    plt.figure(figsize=(14, 8))

    sns.barplot(x='price_per_win_million', y='team', data=data_df, palette='viridis')

    plt.title('NBA Teams by Price Per Win (Highest to Lowest)', fontsize=16)
    plt.xlabel('Price Per Win (Millions $)', fontsize=14)
    plt.ylabel('Team', fontsize=14)

    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.1f}M'))

    plt.show()

if __name__ == "__main__":
    visualize_price_per_win()
