from redis import Redis
from rq import Queue, Retry

from module.upscale import *

q = Queue(connection=Redis())


def upscale_queue(up_scale, img, model_type):
    q.enqueue(upscale_image, up_scale, img, model_type, retry=Retry(max=2), job_timeout=120, result_ttl=60 * 60 * 24, )


def get_upscale_result(job_id):
    job = q.fetch_job(job_id)
    job_result = {
        "job_id": job.job_id,
        "result_type": job.type,
        "create_time": job.created_at,
        "result": job.return_value,
    }
    return job_result


