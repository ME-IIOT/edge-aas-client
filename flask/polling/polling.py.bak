from apscheduler.schedulers.blocking import BlockingScheduler
from polling.fetching_server_info import polling_from_server
import os

serverPollingInterval = int(os.environ.get('SERVER_POLLING_INTERVAL'))
# Create a scheduler instance
scheduler = BlockingScheduler()

# Schedule function to be called every 5 seconds
scheduler.add_job(polling_from_server, 'interval', seconds=serverPollingInterval)

# for another
# scheduler.add_job(function_two, 'interval', seconds=5)

# Start the scheduler
scheduler.start()
