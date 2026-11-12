from pathlib import Path
import cv2

cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_ERROR)  # ปิด warning ตอนลองเปิดกล้อง


def list_cameras():
    """คืนค่า {index: ชื่อกล้อง} จาก /sys/class/video4linux (Linux)"""
    cams = {}
    for dev in sorted(Path("/sys/class/video4linux").glob("video*")):
        cams[int(dev.name[5:])] = (dev / "name").read_text().strip()
    return cams


def try_open(index):
    """ลองเปิดกล้อง index ถ้าอ่านเฟรมได้คืน cap ไม่งั้นคืน None"""
    cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # ลดความหน่วง
        ret, _ = cap.read()
        if ret:
            return cap
    cap.release()
    return None


def open_camera():
    """เปิดกล้องตามลำดับ: Iriun Webcam -> กล้อง notebook -> Not found camera"""
    cams = list_cameras()

    # 1) หา Iriun Webcam
    for index, name in cams.items():
        if "iriun" in name.lower():
            cap = try_open(index)
            if cap is not None:
                print(f"Using {name} (/dev/video{index})")
                return cap

    # 2) ไม่มี Iriun -> ใช้กล้อง notebook (กล้องอื่นที่ไม่ใช่ Iriun)
    for index, name in cams.items():
        if "iriun" not in name.lower():
            cap = try_open(index)
            if cap is not None:
                print(f"Using {name} (/dev/video{index})")
                return cap

    # 3) ไม่มีกล้องเลย
    print("Not found camera")
    return None


# รันด้วย: python -m app.camera
if __name__ == "__main__":
    from detector import PoseDetector

    cap = open_camera()
    if cap is None:
        raise SystemExit(1)

    detector = PoseDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("อ่านเฟรมไม่ได้")
            break

        people, annotated = detector.detect(frame)  # YOLO pose + tracking

        cv2.imshow("YOLO Pose", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
