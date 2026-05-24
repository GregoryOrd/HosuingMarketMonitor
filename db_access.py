from prospects import Prospect
import mysql.connector

COMOX_REGION = "Comox"
SIDNEY_REGION = "Sidney"
COMOX_TABLE = "prospects_comox"
SIDNEY_TABLE = "prospects_sidney"

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

    def query(self, region):
        if region == COMOX_REGION:
            return self.query_with_str(query_str=f"SELECT * FROM {COMOX_TABLE}")
        elif region == SIDNEY_REGION:
            return self.query_with_str(query_str=f"SELECT * FROM {SIDNEY_TABLE}")


    def query_with_str(self, query_str="SELECT * FROM prospects"):
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
                postingDate=str(row["postingDate"]),
                listingId=row["listingId"],
                lat=row["lat"],
                lon=row["lon"],
                liked=row['liked']
            )
            # Optional: load size_sq_ft and notes if needed
            p.size_sq_ft = row.get("size_sq_ft", 0)
            p.notes = row.get("notes", "")
            prospects.append(p)

        return prospects

    def insert_prospect(self, prospect, region):
        if region == COMOX_REGION:
            self.insert_prospect_table(prospect, COMOX_TABLE)
        elif region == SIDNEY_REGION:
            self.insert_prospect_table(prospect, SIDNEY_TABLE)        

    def insert_prospect_table(self, prospect, table):
        if not self.is_started():
            return False

        sql = f"""
            INSERT INTO {table} (
                listingId,
                price,
                addr,
                town,
                beds,
                baths,
                size_sq_ft,
                notes,
                url,
                postingDate,
                lat,
                lon,
                liked
            ) VALUES (
                %(listingId)s,
                %(price)s,
                %(addr)s,
                %(town)s,
                %(beds)s,
                %(baths)s,
                %(size_sq_ft)s,
                %(notes)s,
                %(url)s,
                %(postingDate)s,
                %(lat)s,
                %(lon)s,
                0
            )
            ON DUPLICATE KEY UPDATE
                price = VALUES(price),
                postingDate = VALUES(postingDate),
                lat = VALUES(lat),
                lon = VALUES(lon),
                updatedAt = CURRENT_TIMESTAMP
        """

        data = {
            "listingId": prospect.listingId,
            "price": prospect.price,
            "addr": prospect.addr,
            "town": prospect.town,
            "beds": prospect.beds,
            "baths": prospect.baths,
            "size_sq_ft": prospect.size_sq_ft,
            "notes": prospect.notes,
            "url": prospect.url,
            "postingDate": prospect.postingDate,
            "lat": prospect.lat,
            "lon": prospect.lon
        }

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def delete_prospect(self, prospect, region):
        if region == COMOX_REGION:
            self.delete_prospect_table(prospect, COMOX_TABLE)
        elif region == SIDNEY_REGION:
            self.delete_prospect_table(prospect, SIDNEY_TABLE) 

    def delete_prospect_table(self, p, table):
        if not self.is_started():
            return False

        if table is COMOX_TABLE:
            sql = "DELETE FROM prospects_comox WHERE listingId = %s"
        else:
            sql = "DELETE FROM prospects_sidney WHERE listingId = %s"
        self.cursor.execute(sql, (p.listingId,))
        self.conn.commit()

    def markLiked(self, listingId, region):
        if not self.is_started():
            return False

        if region == COMOX_REGION:
            sql = """
                UPDATE prospects_comox
                SET liked = 1
                WHERE listingId = %(lid)s
            """
        
        if region == SIDNEY_REGION:
            sql = """
                UPDATE prospects_sidney
                SET liked = 1
                WHERE listingId = %(lid)s
            """

        data = {
            "lid": listingId
        }

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def markNeutral(self, listingId, region):
        if not self.is_started():
            return False

        if region == COMOX_REGION:
            sql = """
                UPDATE prospects_comox
                SET liked = 0
                WHERE listingId = %(lid)s
            """
        
        if region == SIDNEY_REGION:
            sql = """
                UPDATE prospects_sidney
                SET liked = 0
                WHERE listingId = %(lid)s
            """

        data = {
            "lid": listingId
        }

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def markDisliked(self, listingId, region):
        if not self.is_started():
            return False

        if region == COMOX_REGION:
            sql = """
                UPDATE prospects_comox
                SET liked = -1
                WHERE listingId = %(lid)s
            """
        
        if region == SIDNEY_REGION:
            sql = """
                UPDATE prospects_sidney
                SET liked = -1
                WHERE listingId = %(lid)s
            """

        data = {
            "lid": listingId
        }

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def saveNotes(self, listingId, notes, region):
        if not self.is_started():
            return False

        if region == COMOX_REGION:
            sql = """
                UPDATE prospects_comox
                SET notes = %(nts)s
                WHERE listingId = %(lid)s
            """
        
        if region == SIDNEY_REGION:
            sql = """
                UPDATE prospects_sidney
                SET notes = %(nts)s
                WHERE listingId = %(lid)s
            """

        data = {
            "nts": notes,
            "lid": listingId
        }

        self.cursor.execute(sql, data)
        self.conn.commit()

        return True

    def is_started(self):
        return self.conn is not None and self.cursor is not None