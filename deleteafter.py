import socket
import threading
from tkinter import *
from PIL import ImageTk
from items import *
import os
import distutils.dir_util
import ftplib
import tkinter as tk
from PIL import ImageTk, Image

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

global billAmount,clients
billAmount = 0




def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    Servermsg = "Welcome to Online Shopping Mart. What would you like to do?\
            \n1.Shopping\n2.Show Bill\n3.Feedback\n4.Live Chat\n\nTo quit anytime, press q."
    conn.send(Servermsg.encode(FORMAT))

    while connected:
        Clientmsg = conn.recv(SIZE).decode(FORMAT)
        if Clientmsg == "q": #DISCONNECT_MSG:
            connected = False
            break

        print(f"[{addr}] {Clientmsg}")
        switch1(Clientmsg,conn,addr)
        # msg = f"Msg received: {msg}"
        Servermsg = "Do you want to do select again?\n1.Shopping\n2.Show Bill\n3.Feedback\n4.Live Chat\n"
        conn.send(Servermsg.encode(FORMAT))

    conn.close()

#Go the which ever category the client selects
global img1, img2

def switch1(item,conn, addr):
    if item == "1":
        Servermsg = "Welcome to Online Shopping Mart. What would you like to buy?\
            \n1.Clothes\n2.Grocery\n3.Electronics\n4.Stationary\n\nTo quit anytime, press q."
        conn.send(Servermsg.encode(FORMAT))
        
        connected=True

        while connected:
            Clientmsg = conn.recv(SIZE).decode(FORMAT)
            if Clientmsg == "q": #DISCONNECT_MSG:
                connected = False
                break

            print(f"[{addr}] {Clientmsg}")
            switch2(Clientmsg,conn)
            # msg = f"Msg received: {msg}"
            Servermsg = "Do you want to buy anything else?\n1.Clothes\n2.Grocery\n3.Electronics\n4.Stationary\n"
            conn.send(Servermsg.encode(FORMAT))
    # elif item == "2":
    #     #ftp
    # elif item == "3":
    #     #smtp
    # elif item == "4":
    #     #livechat
    else:
        Servermsg = "Select the correct option."
        conn.send(Servermsg.encode(FORMAT))
        

def switch2(item,conn):
    if item == "1":
        clothingGui(conn)
    elif item == "2":
        groceryGui(conn)
    elif item == "3":
        electronicsGui(conn)
    elif item == "4":
        stationaryGui(conn)
    else:
        Servermsg = "Select the correct option."
        conn.send(Servermsg.encode(FORMAT))
    


#Shows images of clothes, price, size and allows the user to select the quantity   
def clothingGui(conn):
    root = Tk()  
    root.geometry('200x50')
    global billAmount,clients
    var1 = var2 = var3 = var4 = var5 = var6 = IntVar()
    num1 = num2 = num3 = num4 = num5 = num6 = IntVar()
    var=[]
    num=[]
    
    #Need to add more pics, ig ak category k liye 9 items ki pic sahi hai?
    img1 = ImageTk.PhotoImage(file="black_shirt.png")
    img2 = ImageTk.PhotoImage(file="green_shirt.png")
    img3 = ImageTk.PhotoImage(file="green_shirt.png")
    img4 = ImageTk.PhotoImage(file="green_shirt.png")
    img5 = ImageTk.PhotoImage(file="green_shirt.png")
    img6 = ImageTk.PhotoImage(file="green_shirt.png")
    
    
    #Need to add checkbutton and spinbox for every image as well
    cb1 = Checkbutton(root, text='Blackshirt', image=img1, compound='left', variable=var1)
    w1 = Spinbox(root, from_=1, to=10,textvariable=num1)
    w1.pack()
    cb1.pack(pady=20)
    
    cb2 = Checkbutton(root, text='Greenshirt', image=img2, compound='center',variable=var2)
    w2 = Spinbox(root, from_=1, to=10,textvariable=num2)
    
    w2.pack()
    cb2.pack(pady=20) 
    
    cb3 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var3)
    w3 = Spinbox(root, from_=1, to=10,textvariable=num3)
    
    w3.pack()
    cb3.pack(pady=20) 
    
    cb4 = Checkbutton(root, text='Greenshirt', image=img2, compound='left',variable=var4)
    w4 = Spinbox(root, from_=1, to=10,textvariable=num4)
    
    w4.pack()
    cb4.pack(pady=20) 
    
    cb5 = Checkbutton(root, text='Greenshirt', image=img2, compound='center',variable=var5)
    w5 = Spinbox(root, from_=1, to=10,textvariable=num5)
    
    w5.pack()
    cb5.pack(pady=20) 
    
    cb6 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var6)
    w6 = Spinbox(root, from_=1, to=10,textvariable=num6)
    
    w6.pack()
    cb6.pack(pady=20) 
    
    root.mainloop()
    
    var.append(var1.get())
    var.append(var2.get())
    var.append(var3.get())
    var.append(var4.get())
    var.append(var5.get())
    var.append(var6.get())
    num.append(num1.get())
    num.append(num2.get())
    num.append(num3.get())
    num.append(num4.get())
    num.append(num5.get())
    num.append(num6.get())
    print(var[0])
    
    #adds up price for every item selected in a category
    for i in range(0,len(var)):
        if var[i]==1:
            quantity = num[i]
            billAmount = billAmount + (quantity*clothingItems[i][1])
            print(clothingItems[i])
            fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/BillDetails/Client"+str(clients)+"/OrderDetail.txt"
            file1 = open(fileName, "a")
            file1.write(str(clothingItems[i])+"\n")
    
    file1.close()
    
    Servermsg = "Your total bill right now is: " + str(billAmount)
    conn.send(Servermsg.encode(FORMAT))
        
        
   
    
def groceryGui(conn):
    root = Tk()  
    root.geometry('200x50')
    global billAmount,clients
    var1 = var2 = var3 = var4 = var5 = var6 = IntVar()
    num1 = num2 = num3 = num4 = num5 = num6 = IntVar()
    var=[]
    num=[]
    
    #Need to add more pics, ig ak category k liye 9 items ki pic sahi hai?
    img1 = ImageTk.PhotoImage(file="black_shirt.png")
    img2 = ImageTk.PhotoImage(file="green_shirt.png")
    img3 = ImageTk.PhotoImage(file="green_shirt.png")
    img4 = ImageTk.PhotoImage(file="green_shirt.png")
    img5 = ImageTk.PhotoImage(file="green_shirt.png")
    img6 = ImageTk.PhotoImage(file="green_shirt.png")
    
    
    #Need to add checkbutton and spinbox for every image as well
    cb1 = Checkbutton(root, text='Blackshirt', image=img1, compound='left', variable=var1)
    w1 = Spinbox(root, from_=1, to=10,textvariable=num1)
    w1.pack()
    cb1.pack(pady=20)
    
    cb2 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var2)
    w2 = Spinbox(root, from_=1, to=10,textvariable=num2)
    
    w2.pack()
    cb2.pack(pady=20) 
    
    cb3 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var3)
    w3 = Spinbox(root, from_=1, to=10,textvariable=num3)
    
    w3.pack()
    cb3.pack(pady=20) 
    
    cb4 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var4)
    w4 = Spinbox(root, from_=1, to=10,textvariable=num4)
    
    w4.pack()
    cb4.pack(pady=20) 
    
    cb5 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var5)
    w5 = Spinbox(root, from_=1, to=10,textvariable=num5)
    
    w5.pack()
    cb5.pack(pady=20) 
    
    cb6 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var6)
    w6 = Spinbox(root, from_=1, to=10,textvariable=num6)
    
    w6.pack()
    cb6.pack(pady=20) 
    
    root.mainloop()
    
    var.append(var1.get())
    var.append(var2.get())
    var.append(var3.get())
    var.append(var4.get())
    var.append(var5.get())
    var.append(var6.get())
    num.append(num1.get())
    num.append(num2.get())
    num.append(num3.get())
    num.append(num4.get())
    num.append(num5.get())
    num.append(num6.get())
    print(var[0])
    
    #adds up price for every item selected in a category
    for i in range(0,len(var)):
        if var[i]==1:
            quantity = num[i]
            billAmount = billAmount + (quantity*groceryItems[i][1])
            print(groceryItems[i])
            fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/BillDetails/Client"+str(clients)+"/OrderDetail.txt"
            file1 = open(fileName, "a")
            file1.write(str(groceryItems[i])+"\n")
    
    file1.close()
    
    Servermsg = "Your total bill right now is: " + str(billAmount)
    conn.send(Servermsg.encode(FORMAT))
    
    
    
    
def electronicsGui(conn):
    root = Tk()  
    root.geometry('200x50')
    global billAmount,clients
    var1 = var2 = var3 = var4 = var5 = var6 = IntVar()
    num1 = num2 = num3 = num4 = num5 = num6 = IntVar()
    var=[]
    num=[]
    
    #Need to add more pics, ig ak category k liye 9 items ki pic sahi hai?
    img1 = ImageTk.PhotoImage(file="black_shirt.png")
    img2 = ImageTk.PhotoImage(file="green_shirt.png")
    img3 = ImageTk.PhotoImage(file="green_shirt.png")
    img4 = ImageTk.PhotoImage(file="green_shirt.png")
    img5 = ImageTk.PhotoImage(file="green_shirt.png")
    img6 = ImageTk.PhotoImage(file="green_shirt.png")
    
    
    #Need to add checkbutton and spinbox for every image as well
    cb1 = Checkbutton(root, text='Blackshirt', image=img1, compound='left', variable=var1)
    w1 = Spinbox(root, from_=1, to=10,textvariable=num1)
    w1.pack()
    cb1.pack(pady=20)
    
    cb2 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var2)
    w2 = Spinbox(root, from_=1, to=10,textvariable=num2)
    
    w2.pack()
    cb2.pack(pady=20) 
    
    cb3 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var3)
    w3 = Spinbox(root, from_=1, to=10,textvariable=num3)
    
    w3.pack()
    cb3.pack(pady=20) 
    
    cb4 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var4)
    w4 = Spinbox(root, from_=1, to=10,textvariable=num4)
    
    w4.pack()
    cb4.pack(pady=20) 
    
    cb5 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var5)
    w5 = Spinbox(root, from_=1, to=10,textvariable=num5)
    
    w5.pack()
    cb5.pack(pady=20) 
    
    cb6 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var6)
    w6 = Spinbox(root, from_=1, to=10,textvariable=num6)
    
    w6.pack()
    cb6.pack(pady=20) 
    
    root.mainloop()
    
    var.append(var1.get())
    var.append(var2.get())
    var.append(var3.get())
    var.append(var4.get())
    var.append(var5.get())
    var.append(var6.get())
    num.append(num1.get())
    num.append(num2.get())
    num.append(num3.get())
    num.append(num4.get())
    num.append(num5.get())
    num.append(num6.get())
    print(var[0])
    
    #adds up price for every item selected in a category
    for i in range(0,len(var)):
        if var[i]==1:
            quantity = num[i]
            billAmount = billAmount + (quantity*electronicsItems[i][1])
            print(electronicsItems[i])
            fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/BillDetails/Client"+str(clients)+"/OrderDetail.txt"
            file1 = open(fileName, "a")
            file1.write(str(electronicsItems[i])+"\n")
    
    file1.close()
    
    Servermsg = "Your total bill right now is: " + str(billAmount)
    conn.send(Servermsg.encode(FORMAT))




def stationaryGui(conn):
    root = Tk()  
    root.geometry('200x50')
    global billAmount,clients
    var1 = var2 = var3 = var4 = var5 = var6 = IntVar()
    num1 = num2 = num3 = num4 = num5 = num6 = IntVar()
    var=[]
    num=[]
    
    #Need to add more pics, ig ak category k liye 9 items ki pic sahi hai?
    img1 = ImageTk.PhotoImage(file="black_shirt.png")
    img2 = ImageTk.PhotoImage(file="green_shirt.png")
    img3 = ImageTk.PhotoImage(file="green_shirt.png")
    img4 = ImageTk.PhotoImage(file="green_shirt.png")
    img5 = ImageTk.PhotoImage(file="green_shirt.png")
    img6 = ImageTk.PhotoImage(file="green_shirt.png")
    
    
    #Need to add checkbutton and spinbox for every image as well
    cb1 = Checkbutton(root, text='Blackshirt', image=img1, compound='left', variable=var1)
    w1 = Spinbox(root, from_=1, to=10,textvariable=num1)
    w1.pack()
    cb1.pack(pady=20)
    
    cb2 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var2)
    w2 = Spinbox(root, from_=1, to=10,textvariable=num2)
    
    w2.pack()
    cb2.pack(pady=20) 
    
    cb3 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var3)
    w3 = Spinbox(root, from_=1, to=10,textvariable=num3)
    
    w3.pack()
    cb3.pack(pady=20) 
    
    cb4 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var4)
    w4 = Spinbox(root, from_=1, to=10,textvariable=num4)
    
    w4.pack()
    cb4.pack(pady=20) 
    
    cb5 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var5)
    w5 = Spinbox(root, from_=1, to=10,textvariable=num5)
    
    w5.pack()
    cb5.pack(pady=20) 
    
    cb6 = Checkbutton(root, text='Greenshirt', image=img2, compound='right',variable=var6)
    w6 = Spinbox(root, from_=1, to=10,textvariable=num6)
    
    w6.pack()
    cb6.pack(pady=20) 
    
    root.mainloop()
    
    var.append(var1.get())
    var.append(var2.get())
    var.append(var3.get())
    var.append(var4.get())
    var.append(var5.get())
    var.append(var6.get())
    num.append(num1.get())
    num.append(num2.get())
    num.append(num3.get())
    num.append(num4.get())
    num.append(num5.get())
    num.append(num6.get())
    print(var[0])
    
    #adds up price for every item selected in a category
    for i in range(0,len(var)):
        if var[i]==1:
            quantity = num[i]
            billAmount = billAmount + (quantity*stationaryItems[i][1])
            print(stationaryItems[i])
            fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/BillDetails/Client"+str(clients)+"/OrderDetail.txt"
            file1 = open(fileName, "a")
            file1.write(str(stationaryItems[i])+"\n")
    
    file1.close()
    
    Servermsg = "Your total bill right now is: " + str(billAmount)
    conn.send(Servermsg.encode(FORMAT))
        


def main():
    global clients
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        clients=threading.active_count() - 1
        distutils.dir_util.mkpath("C:/Users/warda/OneDrive/Desktop/CNTestProject/BillDetails/Client"+str(clients))
        
        

if __name__ == "__main__":
    main()