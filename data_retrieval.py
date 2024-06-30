# data_retrieval.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Function to scrape and process data
def retrieve_data(date):
    url = "https://www3.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk"
    session = requests.Session()

    date_input = date.strftime('%Y/%m/%d')
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    date_input_element = soup.find("input", {"id": "txtShareholdingDate"})
    date_input_element["value"] = date_input
    form_data = {ele["name"]: ele.get("value", "") for ele in soup.select("input[name], textarea[name], select[name]")}
    filtered_form_data = {key: value for key, value in form_data.items() if key.startswith("")}
    response = session.post(url, data=form_data)
    soup = BeautifulSoup(response.text, "html.parser")

    displayed_date = date.strftime('%Y-%m-%d')
    main = soup.find("main", {"class": "ccass-search search-result-page"})
    table = main.find("table", {"class": "table table-scroll table-sort table-mobile-list"})

    if table:
        data = []
        rows = table.find_all("tr")[1:] 

        for row in rows:
            cols = [col.get_text(strip=True).replace('Shareholding Date: ', displayed_date) for col in row.find_all("div", {"class": "mobile-list-body"})]
            data.append(cols)

        df = pd.DataFrame(data, columns=["Stock Code", "Name", "Shareholding in CCASS", "% of Issued Shares/Units"])
        df["Date"] = displayed_date

        return df

# Define the start date as One year before from Current Date
current_date = datetime.now()
start_date = datetime(current_date.year - 1, current_date.month, current_date.day)


# Retrieve all historical data
all_data = pd.concat([retrieve_data(start_date + timedelta(days=day)) for day in range((current_date - start_date).days + 1)], ignore_index=True)

# Save all historical data to a single CSV file
all_data.to_csv("combined_data.csv", index=False)
print("All data saved to combined_data.csv")
