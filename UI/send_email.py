import smtplib
fromaddr = 'pwmcats@gmail.com'
toaddrs  = 'pwmcats@gmail.com'
msg = 'This is a lightning warning!'
username = 'pwmcats@gmail.com'
password = 'pussymoneyweed'
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
fuck you
