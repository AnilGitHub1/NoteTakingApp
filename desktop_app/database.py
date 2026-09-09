"""
Local SQLite Database layer for the DSA Note-Taking Desktop App.
Manages schema initialization, CRUD operations, and safe local asset storage.
"""

import os
import shutil
import sqlite3
import uuid
import sys
from typing import Any, Dict, List, Optional, Tuple


def get_app_dir() -> str:
    """
    Returns a safe, persistent user-data directory across macOS, Windows, and Linux.
    When packaged as a macOS .app or frozen binary, stores data in ~/Library/Application Support/DSANoteTaker
    to prevent permission errors when placed in /Applications.
    """
    if getattr(sys, "frozen", False):
        if sys.platform == "darwin":
            base = os.path.expanduser("~/Library/Application Support/DSANoteTaker")
        elif sys.platform == "win32":
            base = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "DSANoteTaker")
        else:
            base = os.path.expanduser("~/.local/share/DSANoteTaker")
        os.makedirs(base, exist_ok=True)
        return base
    return os.path.dirname(os.path.abspath(__file__))


DEFAULT_DB_PATH = os.path.join(get_app_dir(), "dsa_notes.db")
DEFAULT_ASSETS_DIR = os.path.join(get_app_dir(), "dsa_assets")


def resolve_asset_path(img_path: Optional[str]) -> Optional[str]:
    """Resolves relative or absolute image asset paths safely across working directories."""
    if not img_path:
        return None
    if os.path.isabs(img_path) and os.path.exists(img_path):
        return img_path
    candidate_assets = os.path.join(DEFAULT_ASSETS_DIR, os.path.basename(img_path))
    if os.path.exists(candidate_assets):
        return candidate_assets
    candidate_app = os.path.join(get_app_dir(), img_path)
    if os.path.exists(candidate_app):
        return candidate_app
    if os.path.exists(img_path):
        return os.path.abspath(img_path)
    return None



def get_db_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Creates and returns a sqlite3 connection with dict-like row access."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys and WAL mode for reliability
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH, assets_dir: str = DEFAULT_ASSETS_DIR) -> None:
    """
    Initializes the SQLite database tables if they do not already exist,
    and ensures the local assets directory is created.
    """
    # Ensure assets directory exists
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir, exist_ok=True)

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                difficulty TEXT NOT NULL CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
                topic TEXT NOT NULL,
                problem_statement TEXT,
                examples TEXT,
                notes TEXT,
                code TEXT,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Indexes for fast search & filtering
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_difficulty ON questions(difficulty);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_questions_title ON questions(title);")

        conn.commit()


def save_local_asset(source_file_path: str, assets_dir: str = DEFAULT_ASSETS_DIR) -> Optional[str]:
    """
    Safely copies an image to the local './dsa_assets/' folder with a unique filename.
    Returns the relative path to be stored in the database, e.g., 'dsa_assets/img_xxxx.png'.
    """
    if not source_file_path or not os.path.exists(source_file_path):
        return None

    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir, exist_ok=True)

    _, ext = os.path.splitext(source_file_path)
    ext = ext.lower() if ext else ".png"

    unique_filename = f"asset_{uuid.uuid4().hex[:12]}{ext}"
    destination_path = os.path.join(assets_dir, unique_filename)

    shutil.copy2(source_file_path, destination_path)
    # Store normalized relative path
    return os.path.normpath(destination_path)


def add_question(
    title: str,
    difficulty: str,
    topic: str,
    problem_statement: str = "",
    examples: str = "",
    notes: str = "",
    code: str = "",
    image_path: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """Inserts a new DSA question into the database and returns its new ID."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions (
                title, difficulty, topic, problem_statement, examples, notes, code, image_path, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            title.strip(),
            difficulty.strip(),
            topic.strip(),
            problem_statement.strip(),
            examples.strip(),
            notes.strip(),
            code,
            image_path.strip() if image_path else None
        ))
        conn.commit()
        return cursor.lastrowid or 0


def update_question(
    question_id: int,
    title: str,
    difficulty: str,
    topic: str,
    problem_statement: str = "",
    examples: str = "",
    notes: str = "",
    code: str = "",
    image_path: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> bool:
    """Updates an existing DSA question record."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE questions
            SET title = ?,
                difficulty = ?,
                topic = ?,
                problem_statement = ?,
                examples = ?,
                notes = ?,
                code = ?,
                image_path = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            title.strip(),
            difficulty.strip(),
            topic.strip(),
            problem_statement.strip(),
            examples.strip(),
            notes.strip(),
            code,
            image_path.strip() if image_path else None,
            question_id
        ))
        conn.commit()
        return cursor.rowcount > 0


def delete_question(question_id: int, db_path: str = DEFAULT_DB_PATH) -> bool:
    """Deletes a question by ID and removes its attached asset file if local."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT image_path FROM questions WHERE id = ?", (question_id,))
        row = cursor.fetchone()
        if row and row["image_path"]:
            resolved_img = resolve_asset_path(row["image_path"])
            if resolved_img and os.path.exists(resolved_img) and "dsa_assets" in resolved_img:
                try:
                    os.remove(resolved_img)
                except OSError:
                    pass

        cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_question(question_id: int, db_path: str = DEFAULT_DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieves a single question by ID."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_all_questions(
    search_query: Optional[str] = None,
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """
    Returns questions filtered by keyword, topic, or difficulty.
    Ordered by most recently updated first.
    """
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        conditions: List[str] = []
        params: List[Any] = []

        if search_query:
            conditions.append("(title LIKE ? OR problem_statement LIKE ? OR notes LIKE ? OR topic LIKE ?)")
            q = f"%{search_query.strip()}%"
            params.extend([q, q, q, q])

        if topic and topic != "All Topics":
            conditions.append("topic = ?")
            params.append(topic.strip())

        if difficulty and difficulty != "All":
            conditions.append("difficulty = ?")
            params.append(difficulty.strip())

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        query = f"SELECT * FROM questions {where_clause} ORDER BY updated_at DESC, id DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_all_topics(db_path: str = DEFAULT_DB_PATH) -> List[Tuple[str, int]]:
    """Returns a list of tuples containing (topic_name, count) sorted by count descending."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT topic, COUNT(*) as count 
            FROM questions 
            GROUP BY topic 
            ORDER BY count DESC, topic ASC
        """)
        return [(row["topic"], row["count"]) for row in cursor.fetchall()]


def get_stats(db_path: str = DEFAULT_DB_PATH) -> Dict[str, int]:
    """Returns total question count and breakdowns by difficulty."""
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM questions")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM questions WHERE difficulty = 'Easy'")
        easy = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM questions WHERE difficulty = 'Medium'")
        medium = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM questions WHERE difficulty = 'Hard'")
        hard = cursor.fetchone()[0]

        return {
            "total": total,
            "easy": easy,
            "medium": medium,
            "hard": hard
        }


def seed_sample_data(db_path: str = DEFAULT_DB_PATH) -> None:
    """Pre-seeds standard high-yield DSA questions if table is empty."""
    stats = get_stats(db_path)
    if stats["total"] > 0:
        return

    sample_questions = [
        {
            "title": "Two Sum",
            "difficulty": "Easy",
            "topic": "Array & Hash Table",
            "problem_statement": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
            "examples": "Example 1:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: nums[0] + nums[1] == 9, we return [0, 1].\n\nExample 2:\nInput: nums = [3,2,4], target = 6\nOutput: [1,2]",
            "notes": "Optimal Approach:\n- Use a Hash Map to store complement (target - num) -> index.\n- Time Complexity: O(N) single pass.\n- Space Complexity: O(N) map storage.",
            "code": """def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []"""
        },
        {
            "title": "LRU Cache",
            "difficulty": "Medium",
            "topic": "Linked List & Design",
            "problem_statement": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.\n\nImplement the LRUCache class:\n- LRUCache(int capacity) Initialize the LRU cache with positive size capacity.\n- int get(int key) Return the value of the key if the key exists, otherwise return -1.\n- void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair. If keys exceed capacity, evict least recently used key.",
            "examples": "Input:\n[\"LRUCache\", \"put\", \"put\", \"get\", \"put\", \"get\", \"put\", \"get\", \"get\", \"get\"]\n[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]\n\nOutput:\n[null, null, null, 1, null, -1, null, -1, 3, 4]",
            "notes": "Key Insights:\n- Requires O(1) get and O(1) put.\n- Solution: Doubly Linked List + Hash Map of Nodes.\n- Use pseudo head and tail nodes to avoid edge-case null checks during node removal and insertion.",
            "code": """class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head, self.tail = Node(), Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._insert(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._insert(node)
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]"""
        },
        {
            "title": "Trapping Rain Water",
            "difficulty": "Hard",
            "topic": "Two Pointers & Stack",
            "problem_statement": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
            "examples": "Example 1:\nInput: height = [0,1,0,2,1,0,1,3,2,1,2,1]\nOutput: 6\nExplanation: 6 units of rain water are trapped.",
            "notes": "Optimal Approach: Two Pointers.\n- Keep track of left_max and right_max.\n- If left_max < right_max, process height[left] and increment left.\n- Else, process height[right] and decrement right.\n- Time: O(N), Space: O(1).",
            "code": """def trap(height: list[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]

    return water"""
        }
    ]

    for q in sample_questions:
        add_question(
            title=q["title"],
            difficulty=q["difficulty"],
            topic=q["topic"],
            problem_statement=q["problem_statement"],
            examples=q["examples"],
            notes=q["notes"],
            code=q["code"],
            image_path=None,
            db_path=db_path
        )
