import os
import sqlite3

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'mnd-data.db'))

DEFAULT_CATEGORIES = [
    ('อาหาร', 'อาหารที่บ้าน'),
    ('อาหาร', 'อาหารนอกบ้าน'),
    ('อาหาร', 'เครื่องดื่ม / กาแฟ'),
    ('ที่อยู่อาศัย', 'ค่าเช่า / ค่าผ่อนบ้าน'),
    ('ที่อยู่อาศัย', 'ค่าน้ำ / ไฟ / อินเตอร์เน็ต'),
    ('ที่อยู่อาศัย', 'ค่าซ่อมแซม / ของใช้ในบ้าน'),
    ('เสื้อผ้า', 'เสื้อผ้าตัวเอง'),
    ('เสื้อผ้า', 'เสื้อผ้าบุตร'),
    ('การเดินทาง', 'น้ำมัน / ค่าเดินทาง'),
    ('การเดินทาง', 'ค่าบำรุงรักษารถ'),
    ('สุขภาพ', 'ประกันสุขภาพ'),
    ('สุขภาพ', 'ค่าหมอ / ยา'),
    ('การศึกษา', 'ค่าเล่าเรียนบุตร'),
    ('การศึกษา', 'ค่าหนังสือ / คอร์สเรียน'),
    ('ของขวัญ / สังคม', 'ของขวัญ / งานสังคม'),
    ('ของขวัญ / สังคม', 'เลี้ยงดูครอบครัว / พ่อแม่'),
    ('บันเทิง', 'ท่องเที่ยว'),
    ('บันเทิง', 'ความบันเทิงอื่น ๆ'),
    ('ออมทรัพย์ / ลงทุน', 'กองทุน / หุ้น'),
    ('ออมทรัพย์ / ลงทุน', 'กองทุนฉุกเฉิน'),
    ('อื่น ๆ', 'ค่าใช้จ่ายเบ็ดเตล็ด'),
]

DEFAULT_GOALS = [
    ('lifetime', 'กำหนด Net Worth เป้าหมายสุดท้าย', ''),
    ('lifetime', 'กำหนดอายุเกษียณเป้าหมาย', ''),
    ('annual', 'เพิ่ม Net Worth X%', ''),
    ('annual', 'ออมเงิน X ฿', ''),
    ('monthly', 'กรอก Monthly Log', 'ทุกต้นเดือน'),
    ('monthly', 'บันทึกชั่วโมงวางแผนการเงิน', ''),
    ('weekly', 'ทบทวนรายจ่ายสัปดาห์', ''),
    ('daily', 'ตรวจสอบรายจ่ายประจำวัน', ''),
]


def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    return con


def init_db():
    con = get_connection()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS profile (
            id          INTEGER PRIMARY KEY,
            name        TEXT,
            birth_year  INTEGER,
            annual_income REAL,
            updated_at  TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS budget_categories (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            year            INTEGER NOT NULL,
            category        TEXT NOT NULL,
            sub_category    TEXT NOT NULL,
            monthly_budget  REAL DEFAULT 0,
            actual_ytd      REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS monthly_log (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            year         INTEGER NOT NULL,
            month        INTEGER NOT NULL,
            income       REAL DEFAULT 0,
            expenses     REAL DEFAULT 0,
            savings_rate REAL DEFAULT 0,
            net_worth    REAL DEFAULT 0,
            top_overspend TEXT,
            note         TEXT,
            UNIQUE(year, month)
        );

        CREATE TABLE IF NOT EXISTS goals (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            horizon      TEXT NOT NULL,
            goal_text    TEXT NOT NULL,
            target_detail TEXT,
            deadline     TEXT,
            status       TEXT DEFAULT 'active',
            year         INTEGER,
            created_at   TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS planning_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            year        INTEGER NOT NULL,
            month       INTEGER NOT NULL,
            hours       REAL DEFAULT 0,
            activities  TEXT,
            topics      TEXT,
            key_insight TEXT,
            source      TEXT,
            UNIQUE(year, month)
        );

        CREATE TABLE IF NOT EXISTS annual_review (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            year         INTEGER NOT NULL,
            question_key TEXT NOT NULL,
            answer       TEXT,
            updated_at   TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(year, question_key)
        );
    """)

    import datetime
    year = datetime.date.today().year

    # Seed default budget categories for current year if not exists
    count = con.execute(
        "SELECT COUNT(*) FROM budget_categories WHERE year=?", (year,)
    ).fetchone()[0]
    if count == 0:
        con.executemany(
            "INSERT INTO budget_categories (year, category, sub_category) VALUES (?,?,?)",
            [(year, cat, sub) for cat, sub in DEFAULT_CATEGORIES]
        )

    # Seed default goals if not exists
    goal_count = con.execute("SELECT COUNT(*) FROM goals").fetchone()[0]
    if goal_count == 0:
        con.executemany(
            "INSERT INTO goals (horizon, goal_text, target_detail, year) VALUES (?,?,?,?)",
            [(h, g, d, year if h == 'annual' else None) for h, g, d in DEFAULT_GOALS]
        )

    con.commit()
    con.close()
