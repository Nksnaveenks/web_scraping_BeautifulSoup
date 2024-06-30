# Install the schedule library
!pip install schedule

import schedule
import time
import os

# Define a function to run the Python script
def run_data_retrieval():
    os.system("python data_retrieval.py")

# Schedule the task to run daily at 7 AM
schedule.every().day.at("07:00").do(run_data_retrieval)

# Continuously check and run the scheduled task
while True:
    schedule.run_pending()
    time.sleep(1)
