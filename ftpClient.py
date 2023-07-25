import ftplib

def ftp_client(hostname, username, password):
    ftp = ftplib.FTP(hostname)
    ftp.login(user=username, passwd=password)

    print(f"Connected to {hostname} as {username}")

    filename = "OrderDetail.txt"
    with open(filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)
    print(f"Downloaded file '{filename}' from the server.")
    
    filename = "BillDetail.txt"
    with open(filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)
    print(f"Downloaded file '{filename}' from the server.")

    
    ftp.quit()
    print("Disconnected from the ftp server.")
