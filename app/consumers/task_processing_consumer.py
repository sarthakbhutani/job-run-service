from app.utils.kafka import kafka_topic
import asyncio
from app.services.job_run_service import JobRunningService
from app.utils.constants import TaskStatus
from app.utils.logger import setup_logger
logger = setup_logger()

class TaskProcessingConsumer:
    def __init__(self,kafka_topic) -> None:
        # init conusmer here
        self.kafka_topic = kafka_topic
    
    async def process_task(self):
        while True:
            if len(self.kafka_topic):
                # poll message - dont commit tho 
                event = list(self.kafka_topic)[0]
                logger.info(f'TaskProcessingConsumer.process_task.task_id : {event["task"]["id"]}')
                task = event['task']
                # some processing happens here
                await asyncio.sleep(2)
                # callback api - to update status & push another message to Queue
                await JobRunningService(task['job_id'],event['user']).callback_api_to_push_message(task['job_id'],task['id'],TaskStatus.SUCCESS.value)
                # commit
                self.kafka_topic.popleft()