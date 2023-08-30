from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor


jobstores = {
    'default': RedisJobStore(host='localhost', port=6379)
}

executors = {
    'default': ThreadPoolExecutor(10)
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
scheduler.start()