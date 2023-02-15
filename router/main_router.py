import psutil
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from module.get_config import get_config

router = APIRouter()
api_key = get_config("WORKER_APIKEY")
X_API_KEY = APIKeyHeader(name='X-API-Key')


def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
    if x_api_key != api_key:
        raise HTTPException(
            status_code=401,
            detail="API 키가 올바르지 않습니다. X-API-KEY 헤더에 올바른 API키를 입력해주세요."
        )


@router.get("/sys_status", dependencies=[Depends(api_key_auth)])
async def sys_status():
    cpu_percent = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().used
    memory_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').used
    disk_free = psutil.disk_usage('/').free
    network_sent = psutil.net_io_counters().bytes_sent
    network_recv = psutil.net_io_counters().bytes_recv
    return {
        "cpu_percent": cpu_percent,
        "memory_usage": memory_usage,
        "memory_percent": memory_percent,
        "disk_usage": disk_usage,
        "disk_free": disk_free,
        "network_sent": network_sent,
        "network_recv": network_recv
    }

@router.get("/get_info/node_number", dependencies=[Depends(api_key_auth)])
async def get_node_number():
    return {
        "node_number": get_config("WORKER_number")
    }