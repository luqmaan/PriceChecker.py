from time import sleep
from apscheduler.scheduler import Scheduler

sched = Scheduler()

@sched.interval_schedule(seconds=3)
def job():
    print "le job"

sched.start()

sleep(15)

