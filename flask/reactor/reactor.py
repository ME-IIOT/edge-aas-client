from typing import List, Dict, Type
import asyncio
from reactor.handler import Handler, Job

# Base Reactor class implementing Singleton pattern.
# https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
    
class Singleton(type):
    _instances = {}  # Changed to a dictionary to hold instances of each class

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class AsyncReactor(metaclass=Singleton):
    dictHandler: Dict
    running: bool = True

    def __init__(self):
        self.jobs_queue = asyncio.Queue() # Create a queue for the jobs
        self.dictHandler = {}
        self.running = True

    async def add_job(self, job: Job):
        # print(f"AsyncReactor.add_job() called \n job: {job.type}")
        await self.jobs_queue.put(job) # Add a job to the queue
        # print(self.jobs_queue.qsize())

    async def run(self):
        while self.running:
            if self.jobs_queue.empty(): # if the queue is empty,
                continue
            # print("start cycle")
            job: Job = await self.jobs_queue.get() # read and remove a job from the queue (will block until a job is available)
            # print(f"AsyncReactor.run() called \n job: {job.type}")
            handler = self.get_handler(job.type)
            await self.handle_job(handler, job)  # await will block the loop until the job is done
            # print("end cycle")

    async def trigger_handle(self): # call this to manual trigger -> not used (backup when run loop not working)
        print(f"AsyncReactor.trigger_handle() called")
        job: Job = await self.jobs_queue.get()
        handler = self.get_handler(job.type)
        asyncio.create_task(self.handle_job(handler, job))

    async def handle_job(self, handler: Handler, job: Job):
        # print(f"AsyncReactor.handle_job() called \n handler: {handler} \n job: {job}")
        if job is None:
            return
        await handler.handle(job) # Handle the job base on the handler passed by parameter
        self.jobs_queue.task_done() # Mark the job as done

    # Register class of Handler at the start of project (or even later)
    def register_handler(self, type_: str, handlerClass: Type[Handler]): 
        # print("Reactor.register_handler() called \n type_: {} \n handlerClass: {}".format(type_, handlerClass))
        self.dictHandler[type_] = handlerClass

    def remove_handler(self, type_: str):
        if type_ in self.dictHandler:
            del self.dictHandler[type_]

    # Return instance of class Handler base on the type of job (HandlerClass will be registered at the start of project)
    def get_handler(self, type_: str) -> Handler:
        if type_ is None:
            return None
        if type_ in self.dictHandler:
            handler_class = self.dictHandler[type_]
            return handler_class()
        else:                                   # If the type of job is not registered
            raise ValueError("Unknown job type")
        
    async def stop(self): 
        # Set the running flag to False and add a None job to unblock the queue
        print("AsyncReactor.stop() called")
        self.running = False
        await self.jobs_queue.put(None)