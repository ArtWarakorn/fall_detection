# Fall Detection

ระบบตรวจจับการล้มด้วยกล้อง (YOLO + tracking) แจ้งเตือนผ่าน Telegram พร้อม API และหน้าเว็บ

## โครงสร้างและผู้รับผิดชอบ

```
fall_detection/
├── app/
│   ├── camera.py        คนที่ 1  เปิดกล้อง
│   ├── detector.py      คนที่ 1  YOLO + tracking
│   ├── fall_logic.py    คนที่ 1  กฎ + สถานะ
│   ├── pipeline.py      คนที่ 1  ลูปหลัก
│   ├── main.py          คนที่ 2  API ทั้งหมด
│   ├── schemas.py       คนที่ 2  รูปแบบ JSON
│   ├── database.py      คนที่ 2  SQLite
│   ├── notifier.py      คนที่ 2  Telegram
│   └── config.py        คนที่ 2  ค่าตั้งต้น
├── web/                 คนที่ 3  หน้าเว็บ 4 หน้า
├── data/                snapshots, คลิปทดสอบ (clips), falls.db
├── tests/               test_fall_logic, test_api, evaluate
├── docs/                คนที่ 3  รายงาน สไลด์
├── .env.example
├── requirements.txt
└── README.md
```

## เริ่มต้นใช้งาน

```bash
git clone https://github.com/ArtWarakorn/fall_detection.git
cd fall_detection
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env.local       # แล้วใส่ค่าจริง (ห้าม commit)
```

## การทำงานร่วมกัน

1. ดึงงานล่าสุดก่อนเริ่มทุกครั้ง: `git pull`
2. แตก branch ของตัวเอง: `git checkout -b <ชื่อ>/<งาน>` เช่น `person1/detector`
3. แก้เฉพาะไฟล์ที่ตัวเองรับผิดชอบ เพื่อลด conflict
4. `git add` → `git commit -m "..."` → `git push -u origin <branch>`
5. เปิด Pull Request เข้า `main`

ห้าม commit ไฟล์ `.env.local`, `data/falls.db`, ไฟล์โมเดล (`*.pt`, `*.onnx`)
