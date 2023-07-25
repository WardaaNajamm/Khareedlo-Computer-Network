import socket
import threading
from tkinter import *
from PIL import ImageTk
from items import *
import os
import tkinter as tk
from PIL import ImageTk, Image
import json
from twisted.cred.checkers import AllowAnonymousAccess, InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.portal import Portal
from twisted.internet import reactor
from twisted.protocols.ftp import FTPFactory, FTPRealm
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

global billAmount,clients,user
billAmount = 0


USER_FILE = "users.json"  

if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        user_info = json.load(f)
else:
    user_info = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    # Ask the client to either sign up or login
    conn.send("Welcome to the server. Type 'signup' to create a new account or 'login' to log in to an existing account.".encode())
    data = conn.recv(1024).decode()

    if data == "signup":
        conn.send("Enter a new username:".encode())
        username = conn.recv(1024).decode()
        if username in user_info:
            conn.send("Username already taken. Try again or login!\n".encode())
            handle_client(conn,addr)
        else:
            conn.send("Enter a new password:".encode())
            password = conn.recv(1024).decode()
            
            # Store the new username and password in our dictionary
            user_info[username] = {
                "password": password,
                "directory": f"./Users/{username}"
            }
            os.mkdir(user_info[username]["directory"])
            
            # Save the updated user information to file
            with open(USER_FILE, "w") as f:
                json.dump(user_info, f)
            
            conn.send("Account created successfully. You are now logged in.".encode())
            
            connected = True
            Servermsg = "Welcome to KHAREEDLO. What would you like to do?\
                    \na.Shopping\nb.Track Order\nc.Feedback\nd.Payment Option\n\nTo quit anytime, press q."
            conn.send(Servermsg.encode(FORMAT))

            while connected:
                Clientmsg = conn.recv(SIZE).decode(FORMAT)
                if Clientmsg == "q": #DISCONNECT_MSG:
                    connected = False
                    break

                print(f"[{addr}] {Clientmsg}")
                switch1(Clientmsg,conn,addr,username)
                Servermsg = "Do you want to do select again?\na.Shopping\nb.Track Order\nc.Feedback\nd.Payment Option\n"
                conn.send(Servermsg.encode(FORMAT))

            conn.close()

    elif data == "login":
        conn.send("Enter your username:".encode())
        username = conn.recv(1024).decode()
        conn.send("Enter your password:".encode())
        password = conn.recv(1024).decode()

        if user_info.get(username, {}).get("password") == password:
            conn.send("Login successful. You are now logged in.".encode())
            
            connected = True
            Servermsg = "Welcome to KHAREEDLO. What would you like to do?\
                    \na.Shopping\nb.Track Order\nc.Feedback\nd.Payment Option\n\nTo quit anytime, press q."
            conn.send(Servermsg.encode(FORMAT))

            while connected:
                Clientmsg = conn.recv(SIZE).decode(FORMAT)
                if Clientmsg == "q": 
                    connected = False
                    break

                print(f"[{addr}] {Clientmsg}")
                switch1(Clientmsg,conn,addr,username)
                Servermsg = "Do you want to do select again?\na.Shopping\nb.Track Order\nc.Feedback\nd.Payment Option\n"
                conn.send(Servermsg.encode(FORMAT))

            conn.close()
        else:
            conn.send("Invalid username or password. Login failed.".encode())
            handle_client(conn,addr)
    else:
        handle_client(conn,addr)


def switch1(item,conn, addr,username):
    if item == "a":
        Servermsg = "\n\nPlease enter your username again: "
        conn.send(Servermsg.encode(FORMAT))
        username=conn.recv(SIZE).decode(FORMAT)
        
        Servermsg = "Welcome to KHAREEDLO. What would you like to buy?\
            \n1.Clothes\n2.Grocery\n3.Electronics\n4.Stationary\n\nTo quit anytime, press q."
        conn.send(Servermsg.encode(FORMAT))
        
        connected=True

        while connected:
            Clientmsg = conn.recv(SIZE).decode(FORMAT)
            if Clientmsg == "q": #DISCONNECT_MSG:
                connected = False
                break

            print(f"[{addr}] {Clientmsg}")
            switch2(Clientmsg,conn,addr,username)
            # msg = f"Msg received: {msg}"
            Servermsg = "Do you want to buy anything else?\n1.Clothes\n2.Grocery\n3.Electronics\n4.Stationary\n\n5.Proceed to Billing"
            conn.send(Servermsg.encode(FORMAT))
    elif item == "b":
        if os.path.isfile("./Users/{username}/OrderDetail.txt"):
            with open(f'./Users/{username}/TrackingDetails.txt', 'r') as f:
                lines = f.readlines()
            for line in lines:
                Servermsg = line.strip()
                conn.send(Servermsg.encode(FORMAT))
        else:
            print("\nPlace order first!\n")
    elif item == "c":
        Servermsg = "You can send us email on our smtp server (sandbox.smtp.mailtrap.io).\n\
            Type -feedback- if you are sure you want to send us a feedback."
        conn.send(Servermsg.encode(FORMAT))
    elif item == "d":
        Payment(conn,username)
    else:
        Servermsg = "Select the correct option."
        conn.send(Servermsg.encode(FORMAT))
        

def switch2(item,conn,addr,username):
    if item == "1":
        clothingGui(conn,username)
    elif item == "2":
        groceryGui(conn,username)
    elif item == "3":
        electronicsGui(conn,username)
    elif item == "4":
        stationaryGui(conn,username)
    elif item == "5":
        Billing(conn,username)
    else:
        Servermsg = "Select the correct option."
        conn.send(Servermsg.encode(FORMAT))
        
   
def clothingGui(conn,username):
    root = Tk()  
    root.geometry('900x900')
    global billAmount,clients
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    
    num1 = IntVar()
    num2 = IntVar()
    num3 = IntVar()
    num4 = IntVar()
    num5 = IntVar()
    num6 = IntVar()
    var=[]
    num=[]
    
    img1 = ImageTk.PhotoImage(file="./ClothingStock/black_shirt.png")
    img2 = ImageTk.PhotoImage(file="./ClothingStock/jacket.jpg")
    img3 = ImageTk.PhotoImage(file="./ClothingStock/jeans.jpg")
    img4 = ImageTk.PhotoImage(file="./ClothingStock/pink-sweater.jpg")
    img5 = ImageTk.PhotoImage(file="./ClothingStock/scarf.jpg")
    img6 = ImageTk.PhotoImage(file="./ClothingStock/tshirt.jpg")
    
    
    #Need to add checkbutton and spinbox for every image as well
    cb1 = Checkbutton(root, text='Greenshirt', image=img1,variable=var1)
    w1 = Spinbox(root, from_=1, to=10,textvariable=num1)
    cb1.place(x=50,y=100)
    w1.place(x=120,y=330)
    
    cb2 = Checkbutton(root, text='Greenshirt', image=img2, variable=var2)
    w2 = Spinbox(root, from_=1, to=10,textvariable=num2)
    cb2.place(x=300,y=100)
    w2.place(x=370,y=330)
    
    cb3 = Checkbutton(root, text='Greenshirt', image=img3,variable=var3)
    w3 = Spinbox(root, from_=1, to=10,textvariable=num3)
    cb3.place(x=550,y=100)
    w3.place(x=620,y=330)
    
    cb4 = Checkbutton(root, text='Greenshirt', image=img4,variable=var4)
    w4 = Spinbox(root, from_=1, to=10,textvariable=num4)
    cb4.place(x=50,y=400)
    w4.place(x=120,y=630)
    
    cb5 = Checkbutton(root, text='Greenshirt', image=img5,variable=var5)
    w5 = Spinbox(root, from_=1, to=10,textvariable=num5)
    cb5.place(x=300,y=400)
    w5.place(x=370, y=630)
    
    cb6 = Checkbutton(root, text='Greenshirt', image=img6,variable=var6)
    w6 = Spinbox(root, from_=1, to=10,textvariable=num6)
    cb6.place(x=550,y=400)
    w6.place(x=620, y=630)
    
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
    
    #adds up price for every item selected in a category
    for i in range(0,len(var)):
        if var[i]==1:
            quantity = num[i]
            billAmount = billAmount + (quantity*clothingItems[i][1])
            Order_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/OrderDetail.txt"
            Orderfile = open(Order_fileName, "a")
            Orderfile.write("***\n\n"+str(clothingItems[i])+"\n")
            
            Bill_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/BillDetail.txt"
            Billfile = open(Bill_fileName, "a")
            Billfile.write("***\n\n"+str(clothingItems[i])+"  Quantity= "+str(quantity)+"   Total= "+str(quantity*clothingItems[i][1])+"\n")
    
    Orderfile.close()
    Billfile.close()
    
    Servermsg = "Your total bill right now is: " + str(billAmount) + ". To view details of your order and billing, please select option 5 from menu."
    conn.send(Servermsg.encode(FORMAT))
        
        
   
    
def groceryGui(conn,username):
    root = Tk()  
    root.geometry('900x900')
    global billAmount,clients
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    
    num1 = IntVar()
    num2 = IntVar()
    num3 = IntVar()
    num4 = IntVar()
    num5 = IntVar()
    num6 = IntVar()
    var=[]
    num=[]
    
    img1 = ImageTk.PhotoImage(file="./GroceryStock/apple.jpg")
    img2 = ImageTk.PhotoImage(file="./GroceryStock/grape.jpg")
    img3 = ImageTk.PhotoImage(file="./GroceryStock/mango.jpg")
    img4 = ImageTk.PhotoImage(file="./GroceryStock/cupcake.jpg")
    img5 = ImageTk.PhotoImage(file="./GroceryStock/donuts.jpg")
    img6 = ImageTk.PhotoImage(file="./GroceryStock/fries.jpg")
    
    
    #Need to add checkbutton and spinbox for every image as well
    cb1 = Checkbutton(root, text='Greenshirt', image=img1,variable=var1)
    w1 = Spinbox(root, from_=1, to=10,textvariable=num1)
    cb1.place(x=50,y=100)
    w1.place(x=120,y=330)
    
    cb2 = Checkbutton(root, text='Greenshirt', image=img2, variable=var2)
    w2 = Spinbox(root, from_=1, to=10,textvariable=num2)
    cb2.place(x=300,y=100)
    w2.place(x=370,y=330)
    
    cb3 = Checkbutton(root, text='Greenshirt', image=img3,variable=var3)
    w3 = Spinbox(root, from_=1, to=10,textvariable=num3)
    cb3.place(x=550,y=100)
    w3.place(x=620,y=330)
    
    cb4 = Checkbutton(root, text='Greenshirt', image=img4,variable=var4)
    w4 = Spinbox(root, from_=1, to=10,textvariable=num4)
    cb4.place(x=50,y=400)
    w4.place(x=120,y=630)
    
    cb5 = Checkbutton(root, text='Greenshirt', image=img5,variable=var5)
    w5 = Spinbox(root, from_=1, to=10,textvariable=num5)
    cb5.place(x=300,y=400)
    w5.place(x=370, y=630)
    
    cb6 = Checkbutton(root, text='Greenshirt', image=img6,variable=var6)
    w6 = Spinbox(root, from_=1, to=10,textvariable=num6)
    cb6.place(x=550,y=400)
    w6.place(x=620, y=630)
    
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
    
    #adds up price for every item selected in a category
    for i in range(0,len(var)):
        if var[i]==1:
            quantity = num[i]
            billAmount = billAmount + (quantity*groceryItems[i][1])
            Order_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/OrderDetail.txt"
            Orderfile = open(Order_fileName, "a")
            Orderfile.write("***\n\n"+str(groceryItems[i])+"\n")
            
            Bill_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/BillDetail.txt"
            Billfile = open(Bill_fileName, "a")
            Billfile.write("***\n\n"+str(groceryItems[i])+"  Quantity= "+str(quantity)+"   Total= "+str(quantity*groceryItems[i][1])+"\n")
    
    Orderfile.close()
    Billfile.close()
    
    Servermsg = "Your total bill right now is: " + str(billAmount) + ". To view details of your order and billing, please select option 5 from menu."
    conn.send(Servermsg.encode(FORMAT))
    
    
    
    
def electronicsGui(conn,username):
    root = Tk()  
    root.geometry('900x900')
    global billAmount,clients
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    
    num1 = IntVar()
    num2 = IntVar()
    num3 = IntVar()
    num4 = IntVar()
    num5 = IntVar()
    num6 = IntVar()
    var=[]
    num=[]
    
    img1 = ImageTk.PhotoImage(file="./ElectronicsStock/ac.jpg")
    img2 = ImageTk.PhotoImage(file="./ElectronicsStock/fans.jpg")
    img3 = ImageTk.PhotoImage(file="./ElectronicsStock/laptop.jpg")
    img4 = ImageTk.PhotoImage(file="./ElectronicsStock/tablet.jpg")
    img5 = ImageTk.PhotoImage(file="./ElectronicsStock/tv.jpg")
    img6 = ImageTk.PhotoImage(file="./ElectronicsStock/washingmachine.jpg")
    
    
    #Need to add checkbutton and spinbox for every image as well
    cb1 = Checkbutton(root, text='Greenshirt', image=img1,variable=var1)
    w1 = Spinbox(root, from_=1, to=10,textvariable=num1)
    cb1.place(x=50,y=100)
    w1.place(x=120,y=330)
    
    cb2 = Checkbutton(root, text='Greenshirt', image=img2, variable=var2)
    w2 = Spinbox(root, from_=1, to=10,textvariable=num2)
    cb2.place(x=300,y=100)
    w2.place(x=370,y=330)
    
    cb3 = Checkbutton(root, text='Greenshirt', image=img3,variable=var3)
    w3 = Spinbox(root, from_=1, to=10,textvariable=num3)
    cb3.place(x=550,y=100)
    w3.place(x=620,y=330)
    
    cb4 = Checkbutton(root, text='Greenshirt', image=img4,variable=var4)
    w4 = Spinbox(root, from_=1, to=10,textvariable=num4)
    cb4.place(x=50,y=400)
    w4.place(x=120,y=630)
    
    cb5 = Checkbutton(root, text='Greenshirt', image=img5,variable=var5)
    w5 = Spinbox(root, from_=1, to=10,textvariable=num5)
    cb5.place(x=300,y=400)
    w5.place(x=370, y=630)
    
    cb6 = Checkbutton(root, text='Greenshirt', image=img6,variable=var6)
    w6 = Spinbox(root, from_=1, to=10,textvariable=num6)
    cb6.place(x=550,y=400)
    w6.place(x=620, y=630)
    
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
    
    #adds up price for every item selected in a category
    for i in range(0,len(var)):
        if var[i]==1:
            quantity = num[i]
            billAmount = billAmount + (quantity*electronicsItems[i][1])
            Order_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/OrderDetail.txt"
            Orderfile = open(Order_fileName, "a")
            Orderfile.write("***\n\n"+str(electronicsItems[i])+"\n")
            
            Bill_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/BillDetail.txt"
            Billfile = open(Bill_fileName, "a")
            Billfile.write("***\n\n"+str(electronicsItems[i])+"  Quantity= "+str(quantity)+"   Total= "+str(quantity*electronicsItems[i][1])+"\n")
    
    Orderfile.close()
    Billfile.close()
    
    Servermsg = "Your total bill right now is: " + str(billAmount) + ". To view details of your order and billing, please select option 5 from menu."
    conn.send(Servermsg.encode(FORMAT))




def stationaryGui(conn,username):
    root = Tk()  
    root.geometry('900x900')
    global billAmount,clients
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    
    num1 = IntVar()
    num2 = IntVar()
    num3 = IntVar()
    num4 = IntVar()
    num5 = IntVar()
    num6 = IntVar()
    var=[]
    num=[]
    
    img1 = ImageTk.PhotoImage(file="./StationaryStock/colorful-paper.jpg")
    img2 = ImageTk.PhotoImage(file="./StationaryStock/holder.jpg")
    img3 = ImageTk.PhotoImage(file="./StationaryStock/paint.jpg")
    img4 = ImageTk.PhotoImage(file="./StationaryStock/spiral.jpg")
    img5 = ImageTk.PhotoImage(file="./StationaryStock/stapler.jpg")
    img6 = ImageTk.PhotoImage(file="./StationaryStock/tec_set.jpg")
    
    
    #Need to add checkbutton and spinbox for every image as well
    cb1 = Checkbutton(root, text='Greenshirt', image=img1,variable=var1)
    w1 = Spinbox(root, from_=1, to=10,textvariable=num1)
    cb1.place(x=50,y=100)
    w1.place(x=120,y=330)
    
    cb2 = Checkbutton(root, text='Greenshirt', image=img2, variable=var2)
    w2 = Spinbox(root, from_=1, to=10,textvariable=num2)
    cb2.place(x=300,y=100)
    w2.place(x=370,y=330)
    
    cb3 = Checkbutton(root, text='Greenshirt', image=img3,variable=var3)
    w3 = Spinbox(root, from_=1, to=10,textvariable=num3)
    cb3.place(x=550,y=100)
    w3.place(x=620,y=330)
    
    cb4 = Checkbutton(root, text='Greenshirt', image=img4,variable=var4)
    w4 = Spinbox(root, from_=1, to=10,textvariable=num4)
    cb4.place(x=50,y=400)
    w4.place(x=120,y=630)
    
    cb5 = Checkbutton(root, text='Greenshirt', image=img5,variable=var5)
    w5 = Spinbox(root, from_=1, to=10,textvariable=num5)
    cb5.place(x=300,y=400)
    w5.place(x=370, y=630)
    
    cb6 = Checkbutton(root, text='Greenshirt', image=img6,variable=var6)
    w6 = Spinbox(root, from_=1, to=10,textvariable=num6)
    cb6.place(x=550,y=400)
    w6.place(x=620, y=630)
    
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
    
    #adds up price for every item selected in a category
    for i in range(0,len(var)):
        if var[i]==1:
            quantity = num[i]
            billAmount = billAmount + (quantity*stationaryItems[i][1])
            Order_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/OrderDetail.txt"
            Orderfile = open(Order_fileName, "a")
            Orderfile.write("***\n\n"+str(stationaryItems[i])+"\n")
            
            Bill_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/BillDetail.txt"
            Billfile = open(Bill_fileName, "a")
            Billfile.write("***\n\n"+str(stationaryItems[i])+"  Quantity= "+str(quantity)+"   Total= "+str(quantity*stationaryItems[i][1])+"\n")
    
    Orderfile.close()
    Billfile.close()
    
    Servermsg = "Your total bill right now is: " + str(billAmount) + ". To view details of your order and billing, please select option 5 from menu."
    conn.send(Servermsg.encode(FORMAT))
    
    
from twisted.internet import task
def stop_reactor():
    print("Stopping reactor...")
    reactor.stop() 

def Billing(conn,username):
    password="1234"+username
    # addUsers(username,password)
    
    Servermsg = "\nTo check your Order or Bill Details, here are your credentials.\n\
        Please donot share this with anyone. \n\nUsername: "+username+"\nPassword: "+password
    conn.send(Servermsg.encode(FORMAT))
    
    checker = InMemoryUsernamePasswordDatabaseDontUse()
    checker.addUser("ShopAdmin", "admin")
    checker.addUser(username, password)
    print("done")

    # portal=Portal(FTPRealm("./public","./myusers"), [AllowAnonymousAccess(), checker]) 
    portal=Portal(FTPRealm("./Admin","./Users"), [checker])
    factory=FTPFactory(portal)
    reactor.listenTCP(21, factory)
    print("Starting reactor...")
    # Start a LoopingCall that checks if it's time to stop the reactor every second
    lc = task.LoopingCall(stop_reactor)
    lc.start(1)

    reactor.run()
    print("Reactor stopped.")
    
    # conn.send(Servermsg.encode(FORMAT))
    

def Payment(conn,username):
    Servermsg = "\nSelect Payment method:\n1.Cash-on-Delivery\n2.Credit Card\n"
    conn.send(Servermsg.encode(FORMAT))
    paymentMethod=conn.recv(SIZE).decode(FORMAT)
    if(paymentMethod==1):
        Track_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/TrackingDetails.txt"
        Trackfile = open(Track_fileName, "a")
        current_time = time.time()
        local_time = time.localtime(current_time)
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        Trackfile.write(f"***\nCash on Delivery\.\nYour order has been placed {formatted_time}.\nIt will be delivered in 3 working days.")
        Trackfile.close()
    else:
        Track_fileName = "C:/Users/warda/OneDrive/Desktop/CNTestProject/Users/"+username+"/TrackingDetails.txt"
        Trackfile = open(Track_fileName, "a")
        current_time = time.time()
        local_time = time.localtime(current_time)
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        Trackfile.write(f"***\nPayment done through credit card.\nYour order has been placed {formatted_time}.\nIt will be delivered in 3 working days.")
        Trackfile.close()
        
        # Send the payment message back to the client
    Servermsg = "\nPayment done successfully.\n"
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
        

if __name__ == "__main__":
    main()