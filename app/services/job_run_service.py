import traceback    
from app.utils.logger import log_my_ass
from app.utils.logger import setup_logger
from app.utils.redis import setup_redis
from app.utils.constants import RedisKeys,JobStatus,TaskStatus
from app.utils.kafka import kafka_topic
from app.dao.db_utility import DbUtility
logger = setup_logger()
redis = setup_redis()

"""LAYOUT OF WORK -
# FOR NEW JOB REQUEST -- API
    # user has sent a request to run these jobs
    # db query -> how many jobs can I run?
    # db query -> set these jobs as queued
    # check redis -> how many parallels already running for the user
    # db query -> get n=(requests-redis_counter) messages from the queue
    # set these tasks in db as queued -- if a request is for new job
    # push n messages to Q

# CONSUMER -
    # pull message from the queue
    # callback api -> set existing status as success/fail -> push another message to queue

# CALLBACK API -
    # set the current message status
    # get anothe message 
    # push message to Queue
    # if no messages left to push -> remove redis key or set redis key value as 0
"""

class JobRunningService():
    def __init__(self,job_id,user) -> None:
        self.job_id = job_id
        self.user = user
        pass

    async def run_new_job(self):
        logger.info(f'JobRunningService.run_new_job.job_id : {self.job_id}')
        try:
            license_info = await DbUtility.get_license_info(self.user['id'])
            allowed_parallel_runs = license_info['parallel_jobs_license']
            if not allowed_parallel_runs:
                return {
                    "data":None,
                    "message":"User doesnt have access to run parallel jobs",
                    "error":None
                },400
            parallel_jobs_running_count = redis.get(f'{RedisKeys.PARALLEL_JOBS_RUNNING.value}_{str(self.user["id"])}')
            if not parallel_jobs_running_count:
                parallel_jobs_running_count = 0
            else:
                parallel_jobs_running_count = int(parallel_jobs_running_count)
            can_run_job_count = allowed_parallel_runs-parallel_jobs_running_count
            await DbUtility.queue_tasks(self.job_id,TaskStatus.QUEUED.value)
            if can_run_job_count:
                tasks_to_push = await DbUtility.get_queued_tasks(self.job_id,can_run_job_count)
                task_ids = [task['id'] for task in tasks_to_push]
                update_task_status = await DbUtility.bulk_update_task_status(task_ids,TaskStatus.IN_PROGRESS.value)
                if not update_task_status:
                    raise Exception("could not update task status")
                redis.incrby(f'{RedisKeys.PARALLEL_JOBS_RUNNING.value}_{str(self.user["id"])}',can_run_job_count)
                for task_ in tasks_to_push:
                    kafka_topic.append({
                        'task':task_,
                        'user':self.user,
                    })
            return {
                "data":None,
                "message":"Tasks have been pushed to queue",
                "error":None
            },200
        except Exception as e:
            logger.error(f"exception.JobRunningService.run_new_job | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
            return {
                "data":None,
                "message":"Request could not be processed",
                "error":str(e)
            },500

    async def callback_api_to_push_message(self,job_id: int,task_id: int,status:TaskStatus):
        logger.info(f'JobRunningService.callback_api_to_push_message.job_id : {job_id} | task_id : {task_id} | status : {status}')
        try:
            await DbUtility.bulk_update_task_status([task_id],status)
            task_to_execute = await DbUtility.get_queued_tasks(job_id,1)
            # when no tasks left in queue ->
            if not task_to_execute:
                redis.delete(f'{RedisKeys.PARALLEL_JOBS_RUNNING.value}_{str(self.user["id"])}')
                await DbUtility.update_job_status(job_id,TaskStatus.SUCCESS)
            else:
                task = task_to_execute[0]
                update_task_status = await DbUtility.bulk_update_task_status([task['id']],TaskStatus.IN_PROGRESS.value)
                if not update_task_status:
                    raise Exception("could not update task status")
                # push tasks to kafka queue
                logger.info(f'JobRunningService.callback_api_to_push_message.push_message to kafka | job_id : {job_id} | task_id : {task["id"]}')
                kafka_topic.append({
                        'task':task,
                        'user':self.user,
                    })
            return {
                "data":None,
                "message":"success",
                "error":None
            },200
        except Exception as e:
            logger.error(f"exception.JobRunningService.callback_api_to_push_message | error - {str(e)} | traceback - traceback - {traceback.format_exc()}")
            return {
                "data":None,
                "message":"Failed to update status for current task",
                "error":str(e)
            },500


# THINGS THAT CAN BE BETTER -
# 1. implement a retry mechanism while making http calls from consumer
# 2. implement retry mechanism while pushing message to queue
# 3. use db -> and update/select data according to instead of loops