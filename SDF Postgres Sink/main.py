from quixstreams import Application
from quixstreams.models.serializers.quix import JSONDeserializer

import os
import psycopg2 as p2
from psycopg2 import sql


# Function to insert data into the database
def insert_data(uid, stream_id, timestamp, data):
    # Connect to your postgres DB
    conn = p2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )

    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        # Prepare the INSERT statement
        query = sql.SQL("""
            INSERT INTO csv_data_parameter_data (uid, stream_id, "timestamp", "data")
            VALUES (%s, %s, to_timestamp(%s), %s);
        """)

        # Execute the query
        cur.execute(query, (uid, stream_id, timestamp, data))

        # Commit the transaction
        conn.commit()

    # Close the connection
    conn.close()


def sink_to_pdb(row):
    insert_data(row["Number"], "data-stream", row("Timestamp"), row["Name"])

    print(row)


def main():
    app = Application.Quix("transformation-v1", auto_offset_reset="earliest")

    input_topic = app.topic(os.environ["input"], value_deserializer=JSONDeserializer())

    sdf = app.dataframe(input_topic)

    # Here put transformation logic.
    sdf = sdf.update(sink_to_pdb)

    #sdf = sdf.update(lambda row: print(row))

    app.run(sdf)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting.")
