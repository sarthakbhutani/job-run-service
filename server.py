from services.job_run_service import JobRunningService
from consumers.task_processing_consumer import TaskProcessingConsumer
import asyncio
from utils.kafka import kafka_topic
from utils.logger import setup_logger
logger = setup_logger()

"""This is a driver function to the script
"""
async def run_main():
    logger.info('run_main : Script started')
    job_id = 1
    # authenticated user details
    user = {
        'id':1,
        'name':'user 1',
        'email':'user1@lambdatest.com',
        'active':True,
    }
    job_running_service = JobRunningService(job_id,user)
    response = await job_running_service.run_new_job()
    logger.info(f'run_main. response of queing a job - : {str(response)}')
    consumer = TaskProcessingConsumer(kafka_topic)
    await consumer.process_task()


if __name__ == "__main__":
    asyncio.run(run_main())
