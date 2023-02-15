from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from module.get_config import get_config
from module.models.upscale import UpscaleResultModel, UpscaleModel
from module.queue import *

router = APIRouter()
api_key = get_config("WORKER_APIKEY")
X_API_KEY = APIKeyHeader(name='X-API-Key')


def api_key_auth(x_api_key: str = Depends(X_API_KEY)):
    if x_api_key != api_key:
        raise HTTPException(
            status_code=401,
            detail="API 키가 올바르지 않습니다. X-API-KEY 헤더에 올바른 API키를 입력해주세요."
        )


@router.post("/upscale", dependencies=[Depends(api_key_auth)], response_model=UpscaleResultModel)
async def upscale(req: UpscaleModel):
    try:
        upscale_queue(req.up_scale, req.img, req.model_type)
    except Exception:
        return {
            "status_code": "500",
            "detail": "server error"
        }
    return {
        "status_code": "200",
        "detail": "success"
    }


@router.get("/upscale/{job_id}", dependencies=[Depends(api_key_auth)], response_model=UpscaleResultModel)
async def get_upscale_result(job_id: str):
    job_result = get_upscale_result(job_id)
    """dict to json response"""
    if job_result is None:
        return {
            "status_code": "404",
            "detail": "not found"
        }
    else:
        return {
            "status_code": "200",
            "detail": "success",
            "job_id": job_result["job_id"],
            "result_type": job_result["result_type"],
            "create_time": job_result["create_time"],
            "result": job_result["result"]
        }
