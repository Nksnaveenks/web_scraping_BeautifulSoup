import requests
import pandas as pd
from bs4 import BeautifulSoup

# Prompt the user to enter a specific date
date_input = input("Please enter a date(YYYY/MM/DD) less than or equal to Current date and more than or equal to (2023/06/20) to retrieve the data : ")

# Define the URL of the page
url = "https://www3.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk"

# Create a session to persist cookies
session = requests.Session()
response = session.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the input field for the date and set the user-entered date
date_input_element = soup.find("input", {"id": "txtShareholdingDate"})
date_input_element["value"] = date_input

# Extract the form data needed to submit the request with the user's date
form_data = {ele["name"]: ele.get("value", "") for ele in soup.select("input[name], textarea[name], select[name]")}
filtered_form_data = {key: value for key, value in form_data.items() if key.startswith("__")}

response = session.post(url, data=form_data)
soup = BeautifulSoup(response.text, "html.parser")

# Extract the date displayed after the form submission
displayed_date = soup.find("span", style="text-decoration:underline;").get_text()

main = soup.find("main", {"class": "ccass-search search-result-page"})
table = main.find("table", {"class": "table table-scroll table-sort table-mobile-list"})

if table:
    data = []
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("div", {"class": "mobile-list-body"})
        cols = [col.get_text(strip=True) for col in cols]
        data.append(cols)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=["Stock Code", "Name", "Shareholding in CCASS", "% of Issued Shares/Units"])
    
    # Include the Date information in the DataFrame
    df["Date"] = displayed_date

    # Display the retrieved date
    print(f"Retrieved data for the date: {displayed_date}")

    # Write the data to a .csv file
    df.to_csv("out11.csv", index=False)  # Adjust the filename as needed
else:
    print("Table not found on the page. Check the HTML structure or the class names.")
