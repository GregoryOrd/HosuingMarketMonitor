from prospects import Prospect
import mysql.connector

class DbAccess:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def start(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="retriever",
            database="housing",
            password=""
        )

        self.cursor = self.conn.cursor(dictionary=True)

    def close(self):
        if not self.is_started():
            self.cursor.close()
            self.conn.close()           

    def query(self, query_str="SELECT * FROM prospects"):
        if not self.is_started():
            print("Not started at time of query")
            return []

        # Query all rows
        self.cursor.execute(query_str)
        rows = self.cursor.fetchall()

        # Convert rows to Prospect instances
        prospects = []
        for row in rows:
            p = Prospect(
                price=row["price"],
                addr=row["addr"],
                beds=row["beds"],
                baths=row["baths"],
                town=row["town"],
                url=row["url"] if row["url"].startswith("http") else f"https://{row['url']}",
                postingDate=str(row["posting_date"]),
                listingId=row["listing_id"],
                lat=row["lat"],
                long=row["lon"],
                liked=row['liked']
            )
            # Optional: load size_sq_ft and notes if needed
            p.size_sq_ft = row.get("size_sq_ft", 0)
            p.notes = row.get("notes", "")
            prospects.append(p)

        return prospects

    def insert_prospect(self, prospect):
        if not self.is_started():
            return False

        sql = """
            INSERT INTO prospects (
                listing_id,
                price,
                addr,
                town,
                beds,
                baths,
                size_sq_ft,
                notes,
                url,
                posting_date,
                lat,
                lon,
                liked
            ) VALUES (
                %(listing_id)s,
                %(price)s,
                %(addr)s,
                %(town)s,
                %(beds)s,
                %(baths)s,
                %(size_sq_ft)s,
                %(notes)s,
                %(url)s,
                %(posting_date)s,
                %(lat)s,
                %(lon)s,
                0
            )
            ON DUPLICATE KEY UPDATE
                price = VALUES(price),
                posting_date = VALUES(posting_date),
                lat = VALUES(lat),
                lon = VALUES(lon),
                updated_at = CURRENT_TIMESTAMP
        """

        data = {
            "listing_id": prospect.listingId,
            "price": prospect.price,
            "addr": prospect.addr,
            "town": prospect.town,
            "beds": prospect.beds,
            "baths": prospect.baths,
            "size_sq_ft": prospect.size_sq_ft,
            "notes": prospect.notes,
            "url": prospect.url,
            "posting_date": prospect.postingDate,
            "lat": prospect.lat,
            "lon": prospect.long
        }

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def delete_prospect(self, p):
        if not self.is_started():
            return False

        sql = "DELETE FROM prospects WHERE listing_id = %s"
        self.cursor.execute(sql, (p.listingId,))
        self.conn.commit()

    def markLiked(self, listing_id):
        if not self.is_started():
            return False

        sql = """
            UPDATE prospects
            SET liked = 1
            WHERE listing_id = %(lid)s
        """

        data = {
            "lid": listing_id
        }
        print(listing_id)

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def markNeutral(self, listing_id):
        if not self.is_started():
            return False

        sql = """
            UPDATE prospects
            SET liked = 0
            WHERE listing_id = %(lid)s
        """

        data = {
            "lid": listing_id
        }

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def markDisliked(self, listing_id):
        if not self.is_started():
            return False

        sql = """
            UPDATE prospects
            SET liked = -1
            WHERE listing_id = %(lid)s
        """

        data = {
            "lid": listing_id
        }

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def saveNotes(self, listing_id, notes):
        if not self.is_started():
            return False

        sql = """
            UPDATE prospects
            SET notes = %(nts)s
            WHERE listing_id = %(lid)s
        """

        data = {
            "nts": notes,
            "lid": listing_id
        }

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def is_started(self):
        return self.conn is not None and self.cursor is not None