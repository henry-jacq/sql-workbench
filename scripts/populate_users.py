from concurrent.futures import ThreadPoolExecutor, as_completed
from faker import Faker
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn
)

import mysql.connector
import random
import threading
import time

# =========================
# CONFIG
# =========================

HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "performance_db"

TOTAL_ROWS = 1_000_000
WORKERS = 8
BATCH_SIZE = 10_000

# =========================
# GLOBALS
# =========================

statuses = [
    "ACTIVE",
    "INACTIVE",
    "BLOCKED"
]

insert_raw = """
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
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

insert_opt = """
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
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

counter_lock = threading.Lock()
inserted_rows = 0

# =========================
# DB CONNECTION
# =========================

def get_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        autocommit=False
    )

# =========================
# WORKER
# =========================

def load_chunk(start_id, end_id, progress, task_id):

    global inserted_rows

    fake = Faker()

    conn = get_connection()
    cursor = conn.cursor()

    local_inserted = 0

    for batch_start in range(start_id, end_id, BATCH_SIZE):

        batch_end = min(batch_start + BATCH_SIZE, end_id)

        batch = []

        for user_id in range(batch_start, batch_end):

            first = fake.first_name()
            last = fake.last_name()

            batch.append(
                (
                    f"user{user_id}",
                    f"user{user_id}@test.com",
                    first,
                    last,
                    fake.city(),
                    fake.country(),
                    random.randint(18, 80),
                    random.choice(statuses),
                    fake.date_time_between(
                        start_date="-5y",
                        end_date="now"
                    ),
                    fake.date_time_between(
                        start_date="-1y",
                        end_date="now"
                    )
                )
            )

        cursor.executemany(insert_raw, batch)
        cursor.executemany(insert_opt, batch)

        conn.commit()

        rows = len(batch)

        local_inserted += rows

        with counter_lock:
            inserted_rows += rows

        progress.update(task_id, advance=rows)

    cursor.close()
    conn.close()

    return local_inserted

# =========================
# MAIN
# =========================

def main():

    start_time = time.perf_counter()

    rows_per_worker = TOTAL_ROWS // WORKERS

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("({task.completed:,}/{task.total:,})"),
        TimeElapsedColumn(),
        TimeRemainingColumn()
    ) as progress:

        task_id = progress.add_task(
            "Generating + Inserting Users",
            total=TOTAL_ROWS
        )

        with ThreadPoolExecutor(max_workers=WORKERS) as executor:

            futures = []

            for worker in range(WORKERS):

                start_id = worker * rows_per_worker

                if worker == WORKERS - 1:
                    end_id = TOTAL_ROWS
                else:
                    end_id = start_id + rows_per_worker

                futures.append(
                    executor.submit(
                        load_chunk,
                        start_id,
                        end_id,
                        progress,
                        task_id
                    )
                )

            total_inserted = 0

            for future in as_completed(futures):
                total_inserted += future.result()

    end_time = time.perf_counter()

    duration = end_time - start_time

    print("\n" + "=" * 60)
    print(f"Inserted Rows : {total_inserted:,}")
    print(f"Time Taken    : {duration:.2f} sec")
    print(f"Rows / Second : {total_inserted / duration:,.0f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
