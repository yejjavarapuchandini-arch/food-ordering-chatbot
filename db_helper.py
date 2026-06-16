import mysql.connector
def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="food_ordering_system"
    )

def get_order_status(order_id):

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="food_ordering_system"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM order_tracking
        WHERE order_id = %s
        """,
        (order_id,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]

    return "Order not found"

def insert_order_item(food_item, quantity, order_id):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.callproc(
        'insert_order_item',
        [food_item, quantity, order_id]
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_next_order_id():

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    SELECT MAX(order_id)
    FROM orders
    """

    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result[0] is None:
        return 1

    return result[0] + 1

def get_total_order_price(order_id):

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    SELECT get_total_order_price(%s)
    """

    cursor.execute(query, (order_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]

    return 0

def insert_customer_details(
    order_id,
    address,
    phone):

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO customer_details
    (order_id, address, phone)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (order_id, address, phone)
    )

    conn.commit()

    cursor.close()
    conn.close()

def insert_order_tracking(order_id, status):

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO order_tracking(order_id, status)
    VALUES (%s, %s)
    """

    cursor.execute(
        query,
        (order_id, status)
    )

    conn.commit()

    cursor.close()
    conn.close()