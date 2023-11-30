from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from EdgeAasMessageHandler.EdgeHandler import Job
from EdgeAasMessageHandler.Reactor import AsyncReactor
from EdgeAasMessageHandler.EdgePollingHandler import EdgePollingEvent
import json
import asyncio
from typing import List

class RetrievePeriodicTaskView(APIView):
    reactor = AsyncReactor()

    async def add_job(self,jobList: List[str]):
        tasks = [self.reactor.add_job(job=Job(type_=job, request_body={})) for job in jobList]
        await asyncio.gather(*tasks)

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body.decode('utf-8'))
            # print("Request Body:", body)
        except json.JSONDecodeError:
            print("Invalid JSON in request body")
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

        asyncio.run(self.add_job(body))

        # Return a response
        return Response({'message': 'Task received successfully'})

