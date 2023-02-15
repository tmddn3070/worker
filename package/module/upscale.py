import os
import base64
from PIL import Image, ImageChops, ImageStat
from realsr_ncnn_vulkan_python import RealSR, wrapped

if wrapped.get_gpu_count() > 0:
    gpu_id = 0
    num_threads = 1
else:
    gpu_id = -1
    # GPU가 없어? 그럼 CPU를 아오지로 + 웹 구동을 위해 2코어는 남김
    if os.cpu_count() > 2:
        num_threads = os.cpu_count()
    else:
        num_threads = os.cpu_count() - 2

def get_model_path(modeltype):
    if modeltype == "RealEsrgan":
        return "module/upscaler_models/realesrgan"
    elif modeltype == "RealEsrgan_anime":
        return "module/upscaler_models/realesrgan_anime"
    elif modeltype == "RealSR":
        return "module/upscaler_models/realsr_default"

def get_percent(image0: Image.Image, image1: Image.Image) -> float:
    """
    이미지 처리 차이 계산
    :param 이미지 0의 첫번째 프레임
    :param 이미지 1의 두번째 프레임
    :return 두 이미지간의 차이(float)
    """
    difference = ImageChops.difference(image0, image1)
    difference_stat = ImageStat.Stat(difference)
    percent_diff = sum(difference_stat.mean) / (len(difference_stat.mean) * 255) * 100
    return percent_diff


def upscale_image(up_scale: float, img, model_type):
    """
    이미지 업스케일링
    :param 스케일할 배율
    :param 이미지
    :param 모델타입 (RealEsrgan, RealEsrgan_anime, RealSR
    :returns 업스케일링된 이미지(img_byte), 이미지 처리 차이(float)
    """
    model_path = get_model_path(modeltype=model_type)
    image = base64.b64decode(img)
    upscaler = RealSR(gpu_id, num_threads=num_threads, scale=up_scale, model_path=model_path)
    output_image = upscaler.process(image)
    diff = get_percent(img, output_image)
    return output_image, diff



