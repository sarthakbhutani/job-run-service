from utils.db import licenses,jobs,tasks
from utils.logger import setup_logger
from utils.constants import JobStatus,TaskStatus
logger = setup_logger()

# Have made it a class, so that functions can be overriden.
# please dont mind the simpleton implementation
class DbUtility:
    async def get_license_info(user_id):
        logger.info(f'DbUtility.get_license_info.user_id : {user_id}')
        # this would be a search on licenses for key (user_id : {user_id}, active : True)
        return licenses[0]

    async def update_job_status(job_id : int, status : JobStatus):
        logger.info(f'DbUtility.update_job_status.job_id : {job_id} ,status : {status}')
        jobs[0]['status'] = status

    async def queue_tasks( job_id: int, status : TaskStatus):
        logger.info(f'DbUtility.queue_tasks.job_id : {job_id} ,status : {status}')
        # for all the active tasks for this job_id -> mark them as queued
        for task in tasks:
            if task['job_id'] == job_id:
                task['status'] = TaskStatus.QUEUED.value

    async def get_queued_tasks(job_id: int,count : int):
        logger.info(f'DbUtility.get_queued_tasks.job_id : {job_id}, count : {count}')
        # count is basically 'SQL' limit
        counter = 0
        queued_tasks = []
        for task in tasks:
            if task['job_id'] == job_id and task['status'] == TaskStatus.QUEUED.value and counter!=count:
                queued_tasks.append(task)
                counter+=1
        return queued_tasks
    
    async def bulk_update_task_status(task_id : list[int],status : TaskStatus):
        logger.info(f'DbUtility.bulk_update_task_status.task_id : {task_id} ,status : {status}')
        for task in tasks:
            for id in task_id:
                if task['id'] == id:
                    task['status'] = status
        return True
