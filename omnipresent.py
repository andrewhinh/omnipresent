"""Multimodal LLM security."""
# import argparse
import asyncio
# import base64
import cv2
from datetime import datetime
import imutils
# from io import BytesIO
# import json
from time import sleep

# from PIL import Image
# import requests
from ultralytics.models import YOLO

VIDEO = cv2.VideoCapture(0)  # initialize webcam
YOLO_MODELS = [
    "yolov8n-seg.pt",  # semantic segmentation
    "yolov8n-pose.pt",  # pose estimation
    "yolov8n.pt",  # object detection
]
for model in YOLO_MODELS:
    YOLO_MODEL = YOLO(model)  # download models if not already

# PROMPT = f"In 10 words max, describe the physical appearances of every person in view."  # prompt to use
# URL = "https://joiajq6syp65ueonto4mswttzu0apfbi.lambda-url.us-west-1.on.aws/"  # Admirer's API endpoint


# async def send_request(img, prompt):
#     headers = {"Content-type": "application/json"}
#     payload = json.dumps(
#         {
#             "image": "data:image/jpg;base64," + img,
#             "question": "data:question/str;str," + prompt,
#         }
#     )
#     response = requests.post(
#         URL,
#         data=payload,
#         headers=headers,
#     )
#     pred = response.json()["pred"]
#     return pred


# def _make_parser():
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "--prompt",
#         type=str,
#         default=PROMPT,
#         help="Prompt to use for the model.",
#     )
#     return parser


async def main(args):
    MODEL_IDX = 0
    PREV_TIME = datetime.now()
    while True:
        try:
            now = datetime.now()  # get current time
            if (now - PREV_TIME).seconds > 60:  # if it's time to switch models
                MODEL_IDX = (MODEL_IDX + 1) % len(YOLO_MODELS)  # cycle through models
                PREV_TIME = now  # update previous time

            _, img = VIDEO.read()  # read the webcam frame
            YOLO_MODEL = YOLO(YOLO_MODELS[MODEL_IDX])
            people = YOLO_MODEL.track(img, classes=0, verbose=False, persist=True)  # 0 = person, persist=True for tracking between frames
            people = people[0]  # since it usually operates on multiple images

            ann_img = people.plot()
            ann_img = imutils.resize(ann_img, width=2000)  # resize for display
            cv2.imshow("I see you...", ann_img)  # show the frame to our screen
            if cv2.waitKey(1) == ord("q"):  # if we press "q" on our keyboard, break from the loop
                break

            num_people = len(people)
            if num_people:  # if people are detected
                # img_pil = Image.fromarray(img_frame)  # convert to PIL.Image
                # _buffer = BytesIO()  # bytes that live in memory
                # img_pil.save(
                # _buffer, format="png"
                # )  # but which we write to like a file
                # img_enc = base64.b64encode(_buffer.getvalue()).decode(
                # "utf8"
                # )  # encode to base64
                # pred = await send_request(img_enc, args.prompt)
                pred = f"{num_people} "
                if num_people == 1:
                    pred += "person"
                else:
                    pred += "people"
                pred += " detected!"
                print(now.strftime("%Y-%m-%d %H:%M:%S"), pred, sep="\t")
            else:
                print("Coast is clear...")
            sleep(
                0.01
            )  # Needs to sleep since infinite loops are bad for processors, vs. asyncio.sleep which is non-blocking
        except KeyboardInterrupt:
            VIDEO.release()  # close the webcam if loop is broken
            cv2.destroyAllWindows()  # close the windows
            break


if __name__ == "__main__":
    # parser = _make_parser()
    # args = parser.parse_args()
    args = None
    asyncio.run(main(args))
