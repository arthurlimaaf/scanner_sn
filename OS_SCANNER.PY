import keyboard
import socket
import time
from time import sleep

IPScan = "192.168.0.50"
portaScan = 9004


print("Conectando...")
connectionScan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectionScan.connect((IPScan, portaScan))


print("Conectado!")

barcode1 = ""

count = 0

while True:
    
    # print("Esperando Leitura...")
    msg = connectionScan.recv(1024).decode("ascii")
    #print("Leitura " + str(count) + ": " + msg)
    count += 1

    if (count == 1):
        barcode1 = msg
        print(barcode1)
        # keyboard.write(barcode1)
    # elif (count == 2):
    #         barcode2 = msg
    #         print(barcode2)
    #         count +=1
         
    # if((barcode1 == barcode2) & (count == 3)):
    #     print("Ok")
    #     keyboard.write(barcode1)
    #     keyboard.press('Enter')
    #     time.sleep(3)
    #     keyboard.write(barcode2)
    #     keyboard.press('Enter')
    #     count = 0
    # if ((barcode1 != barcode2) & count == 3):
    #     print("Error") 
    #     count = 0


   


