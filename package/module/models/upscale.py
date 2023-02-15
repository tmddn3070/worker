from pydantic import BaseModel


class UpscaleModel(BaseModel):
    """Upscale model"""
    img: str
    up_scale: float
    model_type: str


class UpscaleResultModel(BaseModel):
    """Upscale result"""
    img: str
    diff: float
