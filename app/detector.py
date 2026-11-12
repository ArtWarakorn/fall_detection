from dataclasses import dataclass

import numpy as np
from ultralytics import YOLO

# ชื่อ keypoint 17 จุดของ COCO (ลำดับตาม index ที่ YOLO pose คืนมา)
KEYPOINT_NAMES = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle",
]


@dataclass
class Person:
    track_id: int            # ID ของคนนี้ (คงที่ข้ามเฟรม จาก tracker)
    box: np.ndarray          # [x1, y1, x2, y2] พิกัดกรอบ
    confidence: float        # ความมั่นใจว่าเป็นคน
    keypoints: np.ndarray    # shape (17, 2) พิกัด x, y ของแต่ละจุด
    kp_conf: np.ndarray      # shape (17,) ความมั่นใจของแต่ละจุด


class PoseDetector:
    def __init__(self, model_path="yolo11n-pose.pt", conf=0.5):
        
        self.model = YOLO(model_path)
        self.conf = conf

    def detect(self, frame):
        """รับ frame (BGR) คืนค่า (list ของ Person, ภาพที่วาดผลแล้ว)"""
        results = self.model.track(
            frame,
            persist=True,              # จำ track ID ข้ามเฟรม
            tracker="bytetrack.yaml",  # หรือ "botsort.yaml"
            conf=self.conf,
            classes=[0],               # 0 = person
            verbose=False,
        )
        r = results[0]

        people = []
        # ถ้ายังไม่มี track ID (เช่น เฟรมแรก หรือไม่มีคน) ข้ามไป
        if r.boxes is not None and r.boxes.id is not None and r.keypoints is not None:
            ids = r.boxes.id.int().cpu().numpy()
            boxes = r.boxes.xyxy.cpu().numpy()
            confs = r.boxes.conf.cpu().numpy()
            kps = r.keypoints.xy.cpu().numpy()         # (N, 17, 2)
            kp_confs = r.keypoints.conf.cpu().numpy()  # (N, 17)

            for i in range(len(ids)):
                people.append(Person(
                    track_id=int(ids[i]),
                    box=boxes[i],
                    confidence=float(confs[i]),
                    keypoints=kps[i],
                    kp_conf=kp_confs[i],
                ))

        annotated = r.plot()  # ภาพที่วาดกรอบ + โครงกระดูกให้แล้ว
        return people, annotated
