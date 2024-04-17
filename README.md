# Real-Time Cryptocurrency OHLC Dashboard

## Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. System Architecture](#2-system-architecture)
- [3. Getting Started](#3-getting-started)
- [4. Project Structure](#4-project-structure)
- [5. Dashboard Visualization](#5-dashboard-visualization)
- [6. Docker Configuration](#6-docker-configuration)
- [7. Acknowledgments](#7-acknowledgments)

## 1. Project Overview

This project introduces a real-time cryptocurrency OHLC (Open, High, Low, Close) dashboard designed to provide users with the latest cryptocurrency market trends. Utilizing real-time data from the Binance API, the dashboard visualizes OHLC data for selected cryptocurrency pairs, updating at a user-defined interval.

## 2. System Architecture

The dashboard relies on a modular architecture, integrating several components for data fetching, storage, visualization, and user interaction:

- **Data Fetching**: Real-time data is retrieved from the Binance API.
- **Data Storage**: Fetched data is stored and managed using Hopsworks Feature Store.
- **Visualization**: Data is visualized using Plotly for OHLC charts.
- **User Interface**: Streamlit is used to create an interactive web dashboard.

## 3. Getting Started

To set up and run the project locally, follow these steps:

1. **Clone the repository**

   ```bash
   git clone https://github.com/riaa3102/real-time-crypto-dashboard.git
   ```

2. **Setup and Activate Poetry Environment**

If you haven't already installed Poetry, install it following the instructions on [Poetry's official website](https://python-poetry.org/docs/#installation).

Navigate to the project directory and install dependencies using Poetry:

   ```bash
   make setup
   ```

Activate the virtual environment created by Poetry:

   ```bash
   poetry shell
   ```

3. **Run the Dashboard**

Launch the Streamlit application within the Poetry environment:

   ```bash
   make run
   ```

This will start the Streamlit server, and the dashboard can be accessed via a web browser at [localhost:8080](http://127.0.0.1:8080).

## 4. Project Structure

     real-time-crypto-dashboard/
     ├── src/
     │   ├── backend/
     │   │   ├── cryptocurrency_data_fetcher.py  # Fetches and processes data from Binance API
     │   │   └── feature_store_manager.py        # Manages data storage and retrieval
     │   └── utils/
     │       ├── dirs.py                         # Directory path configurations
     │       └── logger.py                       # Configures logging
     ├── app.py                                  # Entry point for the Streamlit dashboard
     ├── poetry.lock                             # Lock file for dependencies
     ├── pyproject.toml                          # Poetry configuration and dependencies
     ├── README.md                               # Project documentation
     ├── .env                                    # Environment variables for API keys, etc.
     └── Makefile                                # Automates environment setup and app commands

## 5. Dashboard Visualization

Explore real-time cryptocurrency trends through an interactive Streamlit dashboard, displaying up-to-date OHLC data for various cryptocurrency pairs from Binance.

![Dashboard interface](/images/app_dashboard.png)

## 6. Docker Configuration

To containerize the application, you can build and run the Docker image with:

   ```bash
   make build_docker
   make run_docker
   ```

To stop and remove the Docker container, use:

   ```bash
   make stop_docker
   ```

##  6. Acknowledgments

Special thanks to the developers and maintainers of the open-source libraries and APIs used in this project, particularly Streamlit, Plotly, Hopsworks, and Binance API for providing real-time cryptocurrency data.
