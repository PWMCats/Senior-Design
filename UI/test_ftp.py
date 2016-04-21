from ftplib import FTP

#domain name or server ip:
ftp = FTP()
ftp.connect('access.engr.oregonstate.edu', 22)
ftp.login(user='pereza', passwd = '180642Ap?')
ftp.cwd('public_html')
filename = 'exampleFile.txt'
ftp.storbinary('STOR '+filename, open(filename, 'rb'))
ftp.quit()