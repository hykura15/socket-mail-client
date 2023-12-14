import sqlite3

connection = sqlite3.connect('MailData.db')
cursor = connection.cursor()

# cursor.execute("SELECT Inbox.id, Important.id, Project.id, Spam.id, Work.id "
#                "FROM Inbox "
#                "INNER JOIN Important ON Inbox.id = Important.id "
#                "INNER JOIN Project ON Inbox.id = Project.id "
#                "INNER JOIN Spam ON Inbox.id = Spam.id "
#                "INNER JOIN Work ON Inbox.id = Work.id")

# number = 6
# lst = []
folders = ["Inbox", "Important", "Project", "Spam", "Work"]

for folder in folders:
    cursor.execute(f"UPDATE {folder} SET [status] = ? WHERE id = ?", ("Seen", 6))
connection.commit()
for folder in folders:
    cursor.execute(f"select * from {folder}")
    data = cursor.fetchall()
    print(data)


connection.close()
