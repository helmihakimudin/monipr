import mysql.connector
from faker import Faker
import random

# Koneksi ke MySQL
conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="monipr"
)
cursor = conn.cursor()

fake = Faker("id_ID")

batch_size = 2000  # insert per batch
total_records = 200000  # target 200 ribu data

for i in range(0, total_records, batch_size):
    data = []
    for _ in range(batch_size):
        data.append(
            (
                fake.name(),  # name
                fake.name(),  # requester
                fake.text(max_nb_chars=50),  # description
                fake.date(),  # date
                random.randint(1, 500),  # jumlah
                fake.word(),  # unit
                fake.url(),  # url
                random.choice(["Pending", "Approved", "Rejected"]),  # status
                fake.sentence(),  # notes
            )
        )

    cursor.executemany(
        """
        INSERT INTO purchase_requests 
        (name, requester, description, date, jumlah, unit, url, status, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        data,
    )
    conn.commit()
    print(f"Inserted {i + batch_size} records...")

cursor.close()
conn.close()
print("Selesai! ✅")
