# Web-Scraping using Selenium

## Description
This project demonstrates how to use Selenium for web scraping a dataset from Kaggle. It involves automating the login process, navigating to the dataset page, and downloading the dataset files.

## Description of the Website and Data Targeted for Scraping

### Website: Kaggle

Kaggle is a prominent online community and platform for data scientists and machine learning practitioners. It hosts datasets, notebooks, competitions, and discussions, facilitating collaboration and learning. Kaggle competitions are a major attraction, where individuals and teams compete to develop the best models for solving data science challenges, often with significant prizes and recognition.

### Targeted Data for Scraping

The primary goal was to scrape detailed information about the competitions listed on Kaggle. The specific data points targeted for extraction included:

1. **Competition Name:**
    - The title of the competition, which usually indicates the nature or the goal of the challenge.
2. **Competition Host:**
    - The organization or entity that is sponsoring or hosting the competition.
3. **Prizes:**
    - Information about the rewards for winning the competition, which may include cash prizes, scholarships, or other incentives.
4. **Participation:**
    - Details on the number of participants or teams that have entered the competition.
5. **Description:**
    - A brief overview or detailed description of the competition, outlining the objectives, requirements, and other relevant information.

## Prerequisites

- Python 3.x
- Selenium
- WebDriver Manager for Selenium
- Kaggle account

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/KRT2002/Web-Scraping.git
    cd Web-Scraping
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Environment Variables:**

    Create a file named `.env` in the project root directory with the following content:

    ```env
    USER-NAME=your_kaggle_username
    PASSWORD=your_kaggle_password
    THRESHOLD=Number of datapoints you need to scrap (eg. 100)
    ```

## Usage

1. **Run the scraper:**

    ```sh
    python app.py
    ```

2. **Script Breakdown:**

    The `app.py` script performs the following tasks:
    - Opens the Kaggle login page and logs in using provided credentials.
    - Navigates to the specified dataset page.
    - Downloads the dataset files.

## Important Notes

- **Legal and Ethical Considerations:** Ensure you have the right to scrape the data and comply with Kaggle's terms of service. Web scraping can be against the terms of service for some websites, and it's important to respect the rules and data privacy regulations.
- **Error Handling:** The script includes basic error handling. For production use, consider enhancing it to handle more edge cases and errors gracefully.
