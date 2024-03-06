from apscheduler.schedulers.blocking import BlockingScheduler
# from polling.fetching_server_info import polling_from_server
from utility.utility import execute_files_in_folder
import os

serverPollingInterval = int(os.environ.get('SERVER_POLLING_INTERVAL'))
# Create a scheduler instance
scheduler = BlockingScheduler()

# Schedule function to be called every 5 seconds
scheduler.add_job(execute_files_in_folder, 'interval', seconds=1, args=["exposed_script"])

# for another
# scheduler.add_job(function_two, 'interval', seconds=1)

# Start the scheduler
scheduler.start()
