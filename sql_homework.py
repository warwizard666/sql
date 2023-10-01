import psycopg2

conn = psycopg2.connect(database="sqlpython", user="postgres", password="SergeyArtiomov666")
with conn.cursor() as cur:
    def create_db(conn):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(20),
        lastname VARCHAR(30),
        email VARCHAR(254)
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phonenumbers(
            number VARCHAR(11) PRIMARY KEY,
            client_id INTEGER REFERENCES clients(id)
            );
        """)
        return

    def add_client(conn, name, lastname, email, phones=None):
        cur.execute("""INSERT INTO clients(name, lastname, email) VALUES(%s, %s, %s)""",
                    (name, lastname, email))
        conn.commit()

    def add_phone(conn, client_id, phone):
        cur.execute("""INSERT INTO phonenumbers(client_id, phone) VALUES(%s, %s)""",
                    (client_id, phone))
        conn.commit()

    def change_client(conn, client_id,  name=None, lastname=None, email=None, phone=None):
        if name is not None:
            cur.execute("""
                UPDATE clients SET last_name=%s WHERE id=%s
                """, (name, client_id))
        if lastname is not None:
            cur.execute("""
                UPDATE clients SET last_name=%s WHERE id=%s
                """, (lastname, client_id))
        if email is not None:
            cur.execute("""
                UPDATE clients SET email=%s WHERE id=%s
                """, (email, client_id))
        if phone is not None:
            add_phone(client_id, phone)

        cur.execute("""
            SELECT * FROM clients;
            """)
        print(cur.fetchall())
        conn.commit()

    def delete_phone(conn, client_id, phone):
        cur.execute("""
                DELETE FROM phone WHERE client_id=%s and phone=%s;
                """, (client_id, phone))
        cur.execute("""
                SELECT * phone WHERE client_id=%s;
                """, (client_id,))
        print(cur.fetchall())
        conn.commit()

    def delete_client(conn, client_id):
        cur.execute("""
                DELETE FROM clients WHERE id=%s;
                """, (client_id, ))
        cur.execute("""
                DELETE FROM phonenumbers WHERE client_id=%s;
                """, (client_id, ))
        cur.execute("""
                SELECT * FROM clients;
                """, (client_id,))
        print(cur.fetchall())
        conn.commit()


    def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
        if phone is not None:
            cur.execute("""
                SELECT cl.id FROM clients cl
                JOIN phones ph ON ph.client_id = cl.id
                WHERE ph.phone=%s;
                """, (phone,))
        else:
            cur.execute("""
                SELECT id FROM clients 
                WHERE first_name=%s OR last_name=%s OR email=%s;
                """, (first_name, last_name, email))
        print(cur.fetchall())
        conn.commit()




