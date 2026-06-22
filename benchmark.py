"""
High Throughput MySQL User Loader
=================================

Features
--------
✓ 1M+ users
✓ Producer / Consumer Architecture
✓ Multiple DB Writer Threads
✓ Batch Inserts
✓ Rich Live Dashboard
✓ Rows/sec Tracking
✓ ETA Tracking
✓ Queue Depth Monitoring
✓ Separate Connections Per Writer
✓ Inserts Into users_raw + users_optimized
✓ Scales to 10M+ rows

Requirements
------------
pip install mysql-connector-python rich

MySQL
-----
CREATE DATABASE performance_db;

Run schema first.

"""

from queue import Queue
from threading import Thread, Lock
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

import mysql.connector
import random
import time

# =====================================================
# CONFIG
# =====================================================

HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "performance_db"

TOTAL_ROWS = 1_000_000

BATCH_SIZE = 10_000

PRODUCERS = 1
WRITERS = 8

QUEUE_SIZE = 100

# =====================================================
# DATA POOLS
# =====================================================

FIRST_NAMES = [
    "John","Mike","Alex","David","Chris",
    "Emma","Sophia","Sarah","Olivia","Henry"
]

LAST_NAMES = [
    "Smith","Brown","Wilson","Taylor",
    "Johnson","Davis","Miller"
]

CITIES = [
    "Chennai",
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Pune",
    "Kolkata"
]

COUNTRIES = [
    "India",
    "USA",
    "Germany",
    "UK",
    "Canada",
    "Australia"
]

STATUS_WEIGHTS = [
    ("ACTIVE", 75),
    ("INACTIVE", 20),
    ("BLOCKED", 5)
]

# =====================================================
# SQL
# =====================================================

INSERT_RAW = """
INSERT INTO users_raw
(
username,
email,
first_name,
last_name,
city,
country,
age,
status,
created_at,
last_login
)
VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

INSERT_OPT = """
INSERT INTO users_optimized
(
username,
email,
first_name,
last_name,
city,
country,
age,
status,
created_at,
last_login
)
VALUES
(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

# =====================================================
# GLOBALS
# =====================================================

batch_queue = Queue(maxsize=QUEUE_SIZE)

generated_rows = 0
inserted_rows = 0

generation_done = False

lock = Lock()

start_time = None

# =====================================================
# DB
# =====================================================

def get_connection():

    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        autocommit=False
    )

# =====================================================
# DATA GENERATOR
# =====================================================

def generate_batch(start_id, size):

    batch = []

    for user_id in range(start_id, start_id + size):

        created_at = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(
                random.randint(
                    int(time.time()) - 86400 * 365 * 5,
                    int(time.time())
                )
            )
        )

        last_login = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(
                random.randint(
                    int(time.time()) - 86400 * 365,
                    int(time.time())
                )
            )
        )

        batch.append(
            (
                f"user{user_id}",
                f"user{user_id}@test.com",
                random.choice(FIRST_NAMES),
                random.choice(LAST_NAMES),
                random.choice(CITIES),
                random.choice(COUNTRIES),
                random.randint(18, 80),
                random.choices(
                    [x[0] for x in STATUS_WEIGHTS],
                    weights=[x[1] for x in STATUS_WEIGHTS],
                    k=1
                )[0],
                created_at,
                last_login
            )
        )

    return batch

# =====================================================
# PRODUCER
# =====================================================

def producer():

    global generated_rows
    global generation_done

    next_id = 1

    while next_id <= TOTAL_ROWS:

        size = min(
            BATCH_SIZE,
            TOTAL_ROWS - next_id + 1
        )

        batch = generate_batch(
            next_id,
            size
        )

        batch_queue.put(batch)

        with lock:
            generated_rows += size

        next_id += size

    generation_done = True

# =====================================================
# WRITER
# =====================================================

def writer(worker_id):

    global inserted_rows

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        if generation_done and batch_queue.empty():
            break

        try:
            batch = batch_queue.get(timeout=1)

        except:
            continue

        try:

            cursor.executemany(
                INSERT_RAW,
                batch
            )

            cursor.executemany(
                INSERT_OPT,
                batch
            )

            conn.commit()

            with lock:
                inserted_rows += len(batch)

        except Exception as e:

            conn.rollback()

            print(
                f"[WRITER-{worker_id}] ERROR: {e}"
            )

        finally:

            batch_queue.task_done()

    cursor.close()
    conn.close()

# =====================================================
# DASHBOARD
# =====================================================

def build_dashboard():

    elapsed = max(
        time.time() - start_time,
        1
    )

    rate = inserted_rows / elapsed

    remaining = TOTAL_ROWS - inserted_rows

    eta = remaining / rate if rate > 0 else 0

    table = Table(show_header=True)

    table.add_column("Metric")
    table.add_column("Value")

    table.add_row(
        "Generated",
        f"{generated_rows:,}"
    )

    table.add_row(
        "Inserted",
        f"{inserted_rows:,}"
    )

    table.add_row(
        "Target",
        f"{TOTAL_ROWS:,}"
    )

    table.add_row(
        "Queue Depth",
        str(batch_queue.qsize())
    )

    table.add_row(
        "Rows/sec",
        f"{rate:,.0f}"
    )

    table.add_row(
        "Elapsed",
        f"{elapsed:.1f}s"
    )

    table.add_row(
        "ETA",
        f"{eta:.1f}s"
    )

    percent = (
        inserted_rows
        / TOTAL_ROWS
        * 100
    )

    table.add_row(
        "Progress",
        f"{percent:.2f}%"
    )

    return Panel(
        table,
        title="MySQL Performance Loader"
    )

# =====================================================
# MAIN
# =====================================================

def main():

    global start_time

    print("\nStarting Loader...\n")

    start_time = time.time()

    producer_thread = Thread(
        target=producer,
        daemon=True
    )

    producer_thread.start()

    writers = []

    for i in range(WRITERS):

        t = Thread(
            target=writer,
            args=(i + 1,),
            daemon=True
        )

        t.start()

        writers.append(t)

    with Live(
        build_dashboard(),
        refresh_per_second=2
    ) as live:

        while inserted_rows < TOTAL_ROWS:

            live.update(
                build_dashboard()
            )

            time.sleep(0.5)

    producer_thread.join()

    for t in writers:
        t.join()

    elapsed = time.time() - start_time

    print("\n")
    print("=" * 70)
    print("LOAD COMPLETED")
    print("=" * 70)
    print(f"Rows Inserted : {inserted_rows:,}")
    print(f"Time Taken    : {elapsed:.2f}s")
    print(f"Rows/sec      : {inserted_rows / elapsed:,.0f}")
    print("=" * 70)


if __name__ == "__main__":
    main()