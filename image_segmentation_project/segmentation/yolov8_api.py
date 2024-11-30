# import requests
# from gradio_client import Client

# API_ENDPOINT = "https://api-inference.huggingface.co/models/fcakyon/yolov8-segmentation"
# API_NAME = "/predict"


# def yolov8_segmentation(image_path, model_name="yolov8m-seg.pt", image_size=640, conf_threshold=0.25, iou_threshold=0.45):
#     client = Client("fcakyon/yolov8-segmentation")
#     result = client.predict(
#         image=image_path,
#         model_name=model_name,
#         image_size=image_size,
#         conf_threshold=conf_threshold,
#         iou_threshold=iou_threshold,
#         api_name=API_NAME
#     )
#     return result

from gradio_client import Client

def yolov8_segmentation(image_path, model_name="yolov8m-seg.pt", image_size=640, conf_threshold=0.25, iou_threshold=0.45):
    """
    Calls the Hugging Face fcakyon/yolov8-segmentation API and returns the output image path.
    :param image_path: Path to the input image file.
    :param model_name: Model name (e.g., "yolov8m-seg.pt").
    :param image_size: Image size (default: 640).
    :param conf_threshold: Confidence threshold (default: 0.25).
    :param iou_threshold: IOU threshold (default: 0.45).
    :return: Path to the output image.
    """
    client = Client("fcakyon/yolov8-segmentation")
    result = client.predict(
        image=image_path,
        model_name=model_name,
        image_size=image_size,
        conf_threshold=conf_threshold,
        iou_threshold=iou_threshold,
        api_name="/predict",
    )
    return result
