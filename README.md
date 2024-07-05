
## Features

- Fetches team salary data from Basketball Reference.
- Fetches team win data from the NBA API.
- Combines the data to calculate the price per win for each team.
- Visualizes the data using Seaborn and Matplotlib.

## Setup

### Prerequisites

- Python 3.x
- Git

## Usage

1. **Run the main script to fetch and process the data:**

    ```sh
    python app.py
    ```

2. **Visualize the data:**

    The `app.py` script will automatically call the visualization function after processing the data.

## Project Details

### Data Fetching

The `fetcher.py` script includes functions to fetch team salary data from Basketball Reference and team win data from the NBA API. It checks if the data already exists locally and skips fetching if so.

### Data Visualization

The `visualize.py` script creates a bar plot showing the price per win for each NBA team. It sorts teams from highest to lowest price per win to highlight which teams are getting the most value.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
