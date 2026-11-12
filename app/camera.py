import cv2
import time

CAM = '/dev/video0'

cap = cv2.VideoCapture(CAM, cv2.CAP_V4L2)

if not cap.isOpened():
    raise SystemExit("เปิดกล้องไม่ได้ ตรวจ index / ปิดแอปอื่นที่ใช้กล้องอยู่")

prev = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        print("อ่านเฟรมไม่ได้")
        break

    cv2.imshow("Original", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()