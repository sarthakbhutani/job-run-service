from enum import Enum

class JobStatus(Enum):
    QUEUED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

class TaskStatus(Enum):
    QUEUED = 0
    IN_PROGRESS = 1
    SUCCESS = 2
    FAILED = 3

class RedisKeys(Enum):
    PARALLEL_JOBS_RUNNING = "PARALLEL_JOBS_RUNNING"