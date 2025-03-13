host = str(self.ip_bd_textEdit.toPlainText())
username = str(self.login_bd_textEdit.toPlainText())
password = str(self.pass_bd_textEdit.toPlainText())

if host == "" or username == "" or password == "":
    host='q777608x.beget.tech'
    username='q777608x_bd'
    password='Vi72PY%S'
else:
	self.tele_ftp(host, username, password)

try:
    ftp_host=ftputil.FTPHost(host, username, password)
    ftp_host.use_list_a_option = False

    with ftp_host:
list = ftp_host.listdir('/')
i = []
for fname in list:
    i.append(fname)
myString = '\n'.join(i)
print(myString)
self.vyvod_failov_bd_label.setPlainText(myString)

self.proverka_bd_label.setText("Успешное cоединение")
self.proverka_bd_label.setStyleSheet("color: green;")

self.proverka_bd_drugoi_label.setText("Ошибок необнаружено")
self.proverka_bd_drugoi_label.setStyleSheet("color: green;")

except Exception as e:
    print(e)
    self.proverka_bd_drugoi_label.setText("Ошибка")
    self.proverka_bd_drugoi_label.setStyleSheet("color: red;")

    host='5.23.50.132'
    username='ca28659'
    password='Yegor2003'