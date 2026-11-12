## Flie detector.py
สร้าง list keypoint name

สร้าง class Person มีข้อมูลดังนี้
-    track_id: int              
-    box: np.ndarray          
-    confidence: float        
-    keypoints: np.ndarray    
-    kp_conf: np.ndarray 

สร้าง class PoseDetector มี constructor

โดยรับค่า ของ 
- model_path="ที่อยู่ของ model yolo(yolo11n-post.pt)"
- conf => ค่าความเชื่อมั่นกำหนดเริ่มต้นเป็น 0.5

- function detect รับ frame ที่เป็น BGR(ค่าของสี) มาทำงาน
    - ให้ result เก็ยค่าที่เอา model YOLO มา track
    - จากนั้นเก็บ results ในตำแหน่งที่ 0 ไว้ที่ r
    - check ค่าถ้าไม่เป็น none ดึงผลลัพธ์ทั้งหมดที่ YOLO pose   
      เจอในเฟรมนี้ ออกมาเป็น numpy array 
    - loop ตามรอบ id ที่เจอแล้ว add data ลง list ของ people
    - return people list, annotated(ภาพที่วาดกรอบและกระดูกแล้ว)
# ใน file app/camera.py
## รันด้วย: python -m app.camera

- มีการเช็คว่ามีกล้องที่ใช้ใช้แบบไหน (Iriun Webcam, กล้อง note book) 
  ถ้าไม่มีทั้ง 2 แสดงผล "Not found camera"

- หลังจากนั้น loop อ่านทีละเฟรมจนกว่าจะ กด q เพื่อหยุดโปรแกรม
- ตั้งตัวแปล 2 ตัวมารับคือ people, annotated เรียกใช้ detector.detect(frame) ส่ง frame เข้ามาทำงาน
- show image

# สรุปสิ่งที่ทำ 
    ทำให้กล้องสามารถตรวจจับคนและตรวจจับกระดูกได้