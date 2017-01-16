def log_values(tablename,t1,t2,tex):
    try:
        conn = sqlite3.connect('/database.db')
        cursor=conn.cursor()
        cursor.execute("INSERT INTO '{a}'(hora, T1, T2, Tex) values ('{b}','{c}','{d}','{e}')".format(a=tablename,
                                                                                                      b= datetime('now','localtime'),
                                                                                                      c=t1,
                                                                                                      d=t2,
                                                                                                      e=tex))
        conn.commit()
        conn.close()
    except Exception as e:
        with open('getValues_Log.txt', 'a') as out:
            out.write("{0}, log_values {1} ".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),str(e)))
            out.write('\n')
            print (str(e))

def app_temp():
    try:
        port = '/dev/ttyUSB0'
        arduino = serial.Serial(port, 115200)
        time.sleep(2)
        arduino.flush()
        arduino.write(b":DATA")
        result=arduino.readline().decode("utf-8").strip()
        arduino.close()
        v1,v2,v3 = result.split(',')
        v1,v2,v3 = float(v1),float(v2),float(v3)
        tablename = sys.argv[1]
        log_values(tablename, v1,v2,v3)
    except Exception as e:
        with open('getValues_Log.txt', 'a') as out:
            out.write("{0}, app_temp {1} ".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),str(e)))
            out.write('\n')
            print (str(e))

if __name__ == '__main__':
    import sys
    import serial
    from datetime import datetime
    import sqlite3
    app_temp()
