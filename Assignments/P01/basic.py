import psycopg2


try:
    conn = psycopg2.connect("dbname='Project1' user='postgres' host='localhost' port='5433' password='THEprince$4'")
    print ("connection done ::  ", conn)
except Exception as e:
    print ("I am unable to connect to the database")
    print("=======================")
    print(e)
    print("=======================")

try:
    cur = conn.cursor()
    cur.execute("SELECT wkb_geometry FROM public.countries WHERE admin='India';")
    data = cur.fetchall()
    print(data)
    print(type(data))
    print(data[0])
except Except as e:
    print(e)
