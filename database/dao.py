from database.DB_connect import DBConnect
from model.state import State
class DAO:
    @staticmethod
    def get_all_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct year(s_datetime) as year
                    from sighting  """

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result #lista di anni (interi)

    @staticmethod
    def get_shapes(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct shape as shape
                    from sighting 
                    where year(s_datetime) = %s
                    AND shape IS NOT NULL
                    AND shape <> ''
                    order by shape
                    """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result #lista di forme nell'anno scelto

    @staticmethod
    def get_all_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select * from state"""

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result #nodi

    @staticmethod
    def get_neighbors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select state1, state2 from neighbor"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["state1"],row["state2"]))

        cursor.close()
        conn.close()
        return result #lista di tuple con connessioni

    @staticmethod
    def get_edges(year, shape):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT n.state1 AS st1,
                           n.state2 AS st2, 
                           COUNT(*) as N
                    FROM sighting s , neighbor n 
                    WHERE year(s.s_datetime) = %s
                          AND s.shape = %s
                          AND (s.state = n.state1 OR s.state = n.state2)
                          and n.state1 < n.state2
                    GROUP BY st1 , st2 """

        cursor.execute(query, (year, shape))

        for row in cursor:
            result.append((row['st1'], row['st2'], row["N"]))

        cursor.close()
        conn.close()
        return result

