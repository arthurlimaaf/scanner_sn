import keyboard
import socket
import time
from pyModbusTCP.client import ModbusClient
import mysql.connector
from mysql.connector import Error

IPScan = "192.168.100.100"
portaScan = 9004

c = ModbusClient(host="192.168.100.10", port=502,
                 unit_id=1, auto_open=True, auto_close=True)

print("Conectando...")
connectionScan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectionScan.connect((IPScan, portaScan))

print("Conectado!")

barcode1 = ""
barcode2 = ""
count = 0


def check_sn():
    sn_check = barcode1

    dados = f"""INSERT INTO scanner(serial) VALUES
        ('{sn_check}')"""

    try:
        con = mysql.connector.connect(
            host='localhost', database='check_sn', user='root', password='')
        inserir_falhas = dados
        cursor = con.cursor()

        seleciona = "SELECT serial FROM scanner WHERE serial = '{}'".format(
            sn_check)
        cursor.execute(seleciona)
        resultado = cursor.fetchall()
        if len(resultado) != 0:
            print()
            time.sleep(1)
        else:
            cursor.execute(inserir_falhas)
            con.commit()
            cursor.close()
            keyboard.write(barcode1)
            keyboard.press('Enter')
            # print(barcode1)
            time.sleep(0.5)
            keyboard.write(barcode2)
            keyboard.press('Enter')
            # print(barcode2)

    except Error as erro:
        print("Falha na insercao de dados: {}".format(erro))


while True:
    
    count += 1

    if (count == 1):
        msg = connectionScan.recv(1024).decode("ascii")
        barcode1 = msg
        print(barcode1)

    elif (count == 2):
        msg = connectionScan.recv(1024).decode("ascii")
        barcode2 = msg
        print(barcode2)
    
    ler = c.read_holding_registers(0, 1)

    if(ler == [1]): 

        if((barcode1 == barcode2) & (count == 3)):
            check_sn()
            print("SN COMPATIVEIS/CADASTRADO")
            # time.sleep(3)
            count = 0

        elif ((barcode1 != barcode2) & (count == 2)):
            keyboard.write(barcode1)
            keyboard.press('Enter') 
            # print(barcode1)
            time.sleep(0.5)
            keyboard.write(barcode2)
            keyboard.press('Enter')
            # print(barcode2)
            print("SN NAO COMPATIVEIS/DIFERENTES")
            c.write_single_register(125,1)
            time.sleep(2.5)
            keyboard.press('Tab')
            keyboard.press('Enter')
            count = 0

    elif(ler == [0]):
        count = 0