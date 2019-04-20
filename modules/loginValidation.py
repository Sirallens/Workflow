import pymysql.cursors


def get_data(user, sql_host):
    connection = pymysql.connect(host=sql_host, user='kayaba', password='kirito', db='schneider', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT num_employee FROM `employee` WHERE num_employee = '%s'"
        cursor.execute(sql, user)
        rows = cursor.rowcount
        
        if rows > 0:
            data = cursor.fetchone()
            print(str(data['num_employee']) + " is in the Query")
            return True
            
        
    return False    
    
get_data(103000)