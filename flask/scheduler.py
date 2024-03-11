from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utility.utility import execute_files_in_folder
# from utility.sysInfo import update_system_info
from scheduler_functions.sysInfo import update_system_info, update_system_info_async
from scheduler_functions.time_series import update_time_series_data
# from scheduler_functions.time_series
import os

aas_edge_scheduler = BlockingScheduler(timezone="UTC")
def start_scheduler():
    global aas_edge_scheduler
    # Schedule function to be called every 5 seconds
    # scheduler.add_job(execute_files_in_folder, 'interval', seconds=5, args=["exposed_script"])
    client_polling_interval = int(os.environ.get('CLIENT_POLLING_INTERVAL'))
    # aas_edge_scheduler.add_job(update_system_info, 'interval', seconds=client_polling_interval, max_instances=4)
    aas_edge_scheduler.add_job(update_system_info_async, 'interval', seconds=client_polling_interval, max_instances=4)
    
    # Start the scheduler
    # TODO: remove later
    activate_time_series_str = os.environ.get('ACTIVATE_TIMESERIES', '').strip().lower()
    activate_time_series = activate_time_series_str == 'true'
    if activate_time_series:
        time_series_interval = int(os.environ.get('TIMESERIES_INTERVAL'))
        aas_edge_scheduler.add_job(update_time_series_data, 'interval', seconds=time_series_interval)

    aas_edge_scheduler.start()

aas_edge_scheduler_async = AsyncIOScheduler(timezone="UTC")

def start_scheduler_async():
    global aas_edge_scheduler_async
    # Schedule function to be called every 5 seconds
    client_polling_interval = int(os.environ.get('CLIENT_POLLING_INTERVAL', '5'))  # Default to 5 if not set
    # Schedule the async job
    client_polling_interval  =  5
    aas_edge_scheduler_async.add_job(update_system_info_async, 'interval', seconds=client_polling_interval, max_instances=4)
    
    # Conditional scheduling based on environment variables
    activate_time_series_str = os.environ.get('ACTIVATE_TIMESERIES', '').strip().lower()
    activate_time_series = activate_time_series_str == 'true'
    if activate_time_series:
        time_series_interval = int(os.environ.get('TIMESERIES_INTERVAL', '60'))  # Default to 60 if not set
        # Make sure update_time_series_data is async or wrap the call to be async compatible
        aas_edge_scheduler_async.add_job(update_time_series_data, 'interval', seconds=time_series_interval)

    # Start the scheduler
    aas_edge_scheduler_async.start()


from apscheduler.schedulers.base import BaseScheduler
from typing import Callable, Any


# TODO: Try this functions
def change_job_interval(job_id: str, new_interval: int) -> None:
    global aas_edge_scheduler
    aas_edge_scheduler.reschedule_job(job_id, trigger='interval', seconds=new_interval)

def remove_job_by_id(job_id: str) -> None:
    """
    Remove a job from the scheduler using its job ID.

    Parameters:
    - scheduler: The APScheduler scheduler instance.
    - job_id: The ID of the job to be removed.
    """
    global aas_edge_scheduler
    try:
        aas_edge_scheduler.remove_job(job_id)
        print(f"Job {job_id} removed successfully.")
    except Exception as e:
        print(f"Error removing job {job_id}: {e}")

def add_job(func: Callable[..., Any], trigger: str, **trigger_args: Any) -> Any:
    """
    Add a job to the scheduler dynamically.

    Parameters:
    - scheduler: The APScheduler scheduler instance.
    - func: The function to be scheduled.
    - trigger: The type of trigger ('interval', 'date', or 'cron').
    - trigger_args: Additional arguments for the trigger (e.g., seconds=5 for an interval trigger).

    Returns:
    - The job that was added.
    """
    global aas_edge_scheduler
    job = aas_edge_scheduler.add_job(func, trigger, **trigger_args)
    print(f"Job {job.id} added successfully, next run at {job.next_run_time}")
    return job
