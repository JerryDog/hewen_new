# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
mailto_list=['564778704@qq.com']
mail_host="127.0.0.1"  #设置服务器
mail_user="liujiahua"    #用户名
mail_pass="12Nm34@sh"   #口令
mail_postfix="hewenchina.com"  #发件箱的后缀

def send_mail(to_list,sub,content):
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        #server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    if send_mail(mailto_list,"hello","this is a test mail"):
        print "发送成功"
    else:
        print "发送失败"
