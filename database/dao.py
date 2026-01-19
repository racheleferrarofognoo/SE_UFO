from database.DB_connect import DBConnect
from model.state import State


class DAO:
    @staticmethod
    def get_anno():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT YEAR(s.s_datetime) as anno
                    FROM sighting s 
                    WHERE YEAR(s.s_datetime) >= 1910 AND YEAR(s.s_datetime) <= 2010
                    ORDER BY anno ASC"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_all_shapes(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT s.shape 
                    FROM sighting s 
                    WHERE YEAR(s.s_datetime)=%s AND s.shape IS NOT NULL AND s.shape <> '' """

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                   FROM state s """

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_states_by_anno(anno,forma):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.state , count(*) as conteggio
                    FROM sighting s 
                    WHERE YEAR(s.s_datetime)=%s AND s.shape=%s
                    group  by s.state """

        cursor.execute(query, (anno, forma))

        for row in cursor:
            result[row["state"]] = row["conteggio"]

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT state1 as s1, state2 as s2
                    FROM neighbor n
                    WHERE state1<state2 """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result




