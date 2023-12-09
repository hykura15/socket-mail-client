# import tkinter as tk
# import json

# class App:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Auto Update UI")

#         initial_dict = {"name": "Phi Ho"}

#         self.data_var = tk.StringVar(value=json.dumps(initial_dict))

#         label = tk.Label(root, textvariable=self.data_var)
#         label.pack(padx=50, pady=50)

#         button = tk.Button(root, text="Switch App", command=self.Switch)
#         button.pack(pady=5)
#     def Switch(self):
#         current_dict = json.loads(self.data_var.get())

#         current_dict["Hello"] = "Phi Ho"

#         self.data_var.set(json.dumps(current_dict))

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()

# lst = ["fsdfsdf",
#        ['ZHNqZm5sc2pkbmZsa3NkbWZsa21zZGtmbWxrc2RqZmxzZGZsa3NtZGxrZmw= ZHNqZm5sc2pkbmZsa3NkbWZsa21zZGtmbWxrc2RqZmxzZGZsa3NtZGxrZmw= ZHNqZm5sc2pkbmZsa3NkbWZsa21zZGtmbWxrc2RqZmxzZGZsa3NtZGxrZmw='],
#        ['aOG6vyBsw7Q= ZHNqZm5sc2pkbmZsa3NkbWZsa21zZGtmbWxrc2RqZmxzZGZsa3NtZGxrZmw=']]
# msg = '{ZHNqZm5sc2pkbmZsa3NkbWZsa21zZGtmbWxrc2RqZmxzZGZsa3NtZGxrZmw= ZHNqZm5sc2pkbmZsa3NkbWZsa21zZGtmbWxrc2RqZmxzZGZsa3NtZGxrZmw= ZHNqZm5sc2pkbmZsa3NkbWZsa21zZGtmbWxrc2RqZmxzZGZsa3NtZGxrZmw=} {aOG6vyBsw7Q= ZHNqZm5sc2pkbmZsa3NkbWZsa21zZGtmbWxrc2RqZmxzZGZsa3NtZGxrZmw=} {ksdfksjd kfsdjnfkjsd kjnsdkjfn}'
# lst = msg.split("} {")
# print(lst)
# lst[0] = lst[0][1:]
# lst[-1] = lst[-1][1:-1]
# print(' '.join(lst[1]))
lst = ['+OK 692', 'MIME-Version: 1.0', 'Content-Type: multipart/mixed; boundary=boundary', 'To: hykura15@gmail.com', 'Cc: ', 'From: voho39850@gmail.com', 'Subject: Testing', '', '--boundary', 'Content-Type: text/plain; charset=UTF-8; format=flowed', 'Content-Transfer-Encoding: 7bit', '', 'testing ganin', '--boundary', 'Content-Type: application/octet-stream; name="sample.pdf"',
       'Content-Disposition: attachment; filename="sample.pdf"', 'Content-Transfer-Encoding: base64', '', 'JVBERi0xLjMNCiXi48/TDQoNCjEgMCBvYmoNCjw8DQovVHlwZSAvQ2F0YWxvZw0KL091dGxp', '--boundary', 'Content-Type: application/octet-stream; name="text.txt"', 'Content-Disposition: attachment; filename="text.txt"', 'Content-Transfer-Encoding: base64', '', 'aOG6vyBsw7Q=', '--boundary--', '', '.', '']

# temp1 = list(filter(lambda x: x.find("filename=") != -1, lst));
# temp2 = list(filter(lambda x: x.find('Content-Transfer-Encoding: base64') != -1, lst));
# print(temp1)
# print(temp2)
# name = []
# for item in temp1:
#     name.append(item[43:-1])
data = "hahahapopdf"
print("hahaha" in data)