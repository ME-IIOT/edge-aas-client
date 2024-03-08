from apscheduler.schedulers.blocking import BlockingScheduler
from utility.utility import execute_files_in_folder

def start_scheduler():
    scheduler = BlockingScheduler(timezone="UTC")
    # Schedule function to be called every 5 seconds
    scheduler.add_job(execute_files_in_folder, 'interval', seconds=1, args=["exposed_script"])
    # Start the scheduler
    scheduler.start()
