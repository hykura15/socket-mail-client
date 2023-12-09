import tkinter as tk
from tkinter import ttk, filedialog, messagebox  
import json
import client
import base64
import os


class mailApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Email App")
        self.frames = {}
        self.mailData = client.config['mailFolder']
        self.mailBoxWindow = None
        self.senderMailVar = tk.StringVar()
        self.recipientMailVar = tk.StringVar()
        self.ccMailVar = tk.StringVar()
        self.bccMailVar = tk.StringVar()
        self.subjectVar = tk.StringVar()
        self.attachmentFilePathsVar = tk.StringVar()
        self.messageBodyVar = None
        self.auto_download_id = None
        self.autoLoadTime = client.config["autoLoadTime"]
        # self.config = loadConfig()
        self.createMailApp()

    def createMailApp(self):
        labelFrom = ttk.Label(self.root, text="From:")
        labelFrom.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        entryFrom = ttk.Entry(self.root, width=30, textvariable=self.senderMailVar)
        entryFrom.grid(row=0, column=1, padx=10, pady=5)
        labelTo = ttk.Label(self.root, text="To:")
        labelTo.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        entryTo = ttk.Entry(self.root, width=30, textvariable=self.recipientMailVar)
        entryTo.grid(row=1, column=1, padx=10, pady=5)

        labelCc = ttk.Label(self.root, text="Cc:")
        labelCc.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        entryCc = ttk.Entry(self.root, width=30, textvariable=self.ccMailVar)
        entryCc.grid(row=2, column=1, padx=10, pady=5)

        labelBcc = ttk.Label(self.root, text="BCC:")
        labelBcc.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        entryBcc = ttk.Entry(self.root, width=30, textvariable=self.bccMailVar)
        entryBcc.grid(row=3, column=1, padx=10, pady=5)

        labelSubject = ttk.Label(self.root, text="Subject:")
        labelSubject.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        entrySubject = ttk.Entry(self.root, width=30, textvariable=self.subjectVar)
        entrySubject.grid(row=4, column=1, padx=10, pady=5)

        labelMessage = ttk.Label(self.root, text="Message:")
        labelMessage.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        textMessage = tk.Text(self.root, width=30, height=10)
        textMessage.grid(row=5, column=1, padx=10, pady=5)
        self.messageBodyVar = textMessage

        labelAttachmentFile = ttk.Label(self.root, text="Attachment File:")
        labelAttachmentFile.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

        entryAttachmentFile = ttk.Entry(
            self.root, width=20, textvariable=self.attachmentFilePathsVar)
        entryAttachmentFile.grid(row=6, column=1, padx=10, pady=5)

        buttonAttach = ttk.Button(self.root, text="Attach File", command=self.attachFile)
        buttonAttach.grid(row=6, column=2, padx=10, pady=5)

        buttonSendMail = ttk.Button(self.root, text="Send Email", command=self.handleSendMail)
        buttonSendMail.grid(row=7, column=0, columnspan=2, pady=10)

        buttonShowMailBox = ttk.Button(self.root, text="Mail Box", command=self.showMailBox)
        buttonShowMailBox.grid(row=7, column=2, padx=10, pady=5)

        self.auto_download_id = self.root.after(self.autoLoadTime, self.autoDownloadMail) 
        self.root.mainloop()

        self.root.mainloop()
        
    def autoDownloadMail(self):
        try:
            newData = client.receiveMail()
            if newData is not None:
                self.showMailList(newData)
                messagebox.showinfo("Success", "Mail downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download mail. Error: {str(e)}")

        self.auto_download_id = self.root.after(self.autoLoadTime, self.autoDownloadMail)
        
    def attachFile(self):
        file_paths = filedialog.askopenfilenames(title="Select Files")
        self.attachmentFilePathsVar.set(";".join(file_paths))

    def handleSendMail(self):
        senderMail = self.senderMailVar.get()
        recipientMail = self.recipientMailVar.get().split(' ')
        ccMail = self.ccMailVar.get().split(' ')
        bccMail = self.bccMailVar.get().split(' ')
        subject = self.subjectVar.get()
        messageBody = self.messageBodyVar.get("1.0", "end-1c")
        attachmentFilePaths = self.attachmentFilePathsVar.get()
        
        if not senderMail or not recipientMail or not subject or not messageBody:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        if len(attachmentFilePaths) != 0:
            attachmentFilePaths = attachmentFilePaths.split(';')
        
        try:
            client.sendMail(senderMail, recipientMail, ccMail,
                            bccMail, subject, messageBody, attachmentFilePaths)
            messagebox.showinfo("Success", "Email sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email. Error: {str(e)}")
    def showMailBox(self):
        self.mailBoxWindow = tk.Toplevel()
        self.mailBoxWindow.title("Mail Box")
        self.mailBoxWindow.geometry("650x400")
        
        for frame in self.frames.values():
            frame.destroy()
        try:
            with open("data.json", 'r') as file:
                self.mailData = json.load(file)
            self.showMailList(self.mailData)
        except:
            pass
            
        buttonReceive = ttk.Button(self.mailBoxWindow, text="Download Mail", command=self.updateData)
        buttonReceive.grid(row=1, column=0, pady=5)
        
    def showMailList(self, mailData):
        notebook = ttk.Notebook(self.mailBoxWindow)
        notebook.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        folders = ["Inbox", "Important", "Project", "Spam", "Work"]
        self.frames = {folder: ttk.Frame(notebook) for folder in folders}
        for folder in folders:
            notebook.add(self.frames[folder], text=folder)
            tree = ttk.Treeview(self.frames[folder], columns=("Read", "Sender", "Subject"), show="headings")
            tree.heading("Read", text="Read")
            tree.heading("Sender", text="Sender")
            tree.heading("Subject", text="Subject")

            for email in mailData.get(folder, []):
                if email[0] == 0:
                    email[0] = "Read"
                else:
                    email[0] = "Not Read"
                tree.insert("", tk.END, values=email)
                # print(email)

            tree.bind("<<TreeviewSelect>>", self.onMailSelected)
            tree.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

    def onMailSelected(self, event):
        selectedItem = event.widget.selection()[0]
        values = list((event.widget.item(selectedItem, 'values')))
        filePaths = values[-2].split(' ')
        fileContents = values[-1].split(' ')
        mailContent = tk.Toplevel()
        mailContent.title("Mail Content")
        mailContent.geometry("450x450")
        inforLabel = tk.Label(mailContent, text=f"Sender: {values[1]}\nSubject: {values[2]}\n\n")
        inforLabel.pack()
        labelMessage = ttk.Label(mailContent, text="Message:")
        labelMessage.pack()
        if filePaths[0] != '':
            number = len(filePaths)
            values[3] += f"\nCo {number} files: \n"
            for item in filePaths:
                values[3] += f'{item}\n'
        
        textMessage = tk.Text(mailContent, wrap=tk.WORD, width=40, height=20)
        textMessage.insert(tk.END, values[3])
        textMessage.pack()
        if filePaths[0] != '':
            buttonAttach = ttk.Button(mailContent, text="Download file", command=lambda: self.handleDownloadFile(filePaths, fileContents))
            buttonAttach.pack(padx=10, pady=5)
    
    def handleDownloadFile(self, filePaths, fileContents):
        saveFolder = filedialog.askdirectory()
        for index in range(0, len(filePaths), 1):
            fileName = os.path.basename(filePaths[index])
            savePath = os.path.join(saveFolder, fileName)
            try:
                content = base64.b64decode(fileContents[index])
                with open(savePath, 'wb') as file:
                    file.write(content)
                messagebox.showinfo("Success", f"File '{fileName}' downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download file '{fileName}'. Error: {str(e)}")
    def updateData(self):
        try:
            newData = client.receiveMail()
            if newData != None:
                self.showMailList(newData)
                messagebox.showinfo("Success", "Mail downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download mail. Error: {str(e)}")
        
if __name__ == "__main__":
    app = mailApp()
