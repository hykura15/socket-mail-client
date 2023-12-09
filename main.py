import tkinter as tk
from tkinter import ttk, filedialog
import client
import json

sender_email_var = None
recipient_email_var = None
cc_email_var = None
bcc_email_var = None
subject_var = None
message_body_var = None
attachment_path_var = None


def create_email_composer():
    global sender_email_var, recipient_email_var, cc_email_var, bcc_email_var
    global subject_var, message_body_var, attachment_path_var

    root = tk.Tk()
    root.title("Email Composer")

    sender_email_var = tk.StringVar()
    recipient_email_var = tk.StringVar()
    cc_email_var = tk.StringVar()
    bcc_email_var = tk.StringVar()
    subject_var = tk.StringVar()
    attachment_path_var = tk.StringVar()

    # Create and place widgets
    label_from = ttk.Label(root, text="From:")
    label_from.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

    entry_from = ttk.Entry(root, width=30, textvariable=sender_email_var)
    entry_from.grid(row=0, column=1, padx=10, pady=5)

    label_to = ttk.Label(root, text="To:")
    label_to.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

    entry_to = ttk.Entry(root, width=30, textvariable=recipient_email_var)
    entry_to.grid(row=1, column=1, padx=10, pady=5)

    label_cc = ttk.Label(root, text="Cc:")
    label_cc.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    entry_cc = ttk.Entry(root, width=30, textvariable=cc_email_var)
    entry_cc.grid(row=2, column=1, padx=10, pady=5)

    label_bcc = ttk.Label(root, text="BCC:")
    label_bcc.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

    entry_bcc = ttk.Entry(root, width=30, textvariable=bcc_email_var)
    entry_bcc.grid(row=3, column=1, padx=10, pady=5)

    label_subject = ttk.Label(root, text="Subject:")
    label_subject.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

    entry_subject = ttk.Entry(root, width=30, textvariable=subject_var)
    entry_subject.grid(row=4, column=1, padx=10, pady=5)

    label_message = ttk.Label(root, text="Message:")
    label_message.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

    text_message = tk.Text(root, width=30, height=10)
    text_message.grid(row=5, column=1, padx=10, pady=5)
    message_body_var = text_message

    label_attachment = ttk.Label(root, text="Attachment:")
    label_attachment.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

    entry_attachment = ttk.Entry(
        root, width=20, textvariable=attachment_path_var)
    entry_attachment.grid(row=6, column=1, padx=10, pady=5)

    button_attach = ttk.Button(root, text="Attach File", command=attach_file)
    button_attach.grid(row=6, column=2, padx=10, pady=5)

    button_send = ttk.Button(root, text="Send Email", command=send_email)
    button_send.grid(row=7, column=0, columnspan=2, pady=10)

    button_receive = ttk.Button(
        root, text="Receive Mail", command=showMailBox)
    button_receive.grid(row=7, column=2, padx=10, pady=5)

    # Run the Tkinter event loop
    root.mainloop()


def attach_file():
    file_paths = filedialog.askopenfilenames(title="Select Files")
    attachment_path_var.set(";".join(file_paths))


def send_email():
    sender_email = sender_email_var.get()
    recipient_email = recipient_email_var.get().split(' ')
    cc_email = cc_email_var.get().split(' ')
    bcc_email = bcc_email_var.get().split(' ')
    subject = subject_var.get()
    message_body = message_body_var.get("1.0", "end-1c")
    attachment_path = attachment_path_var.get()
    if len(attachment_path) != 0:
        attachment_path = attachment_path.split(';')
    client.send_email(sender_email, recipient_email, cc_email,
                      bcc_email, subject, message_body, attachment_path)


def downloadMail():
    LIST = client.receive_mail()
    return LIST

def showMailBox():
    global frames
    # LIST = client.receive_mail();
    
    LIST = {}
    with open('data.json', 'r') as file:
        LIST = json.load(file)
    # print(LIST)
    folders_window = tk.Toplevel()
    folders_window.title("Mail Folders")
    folders_window.geometry("800x400")

    notebook = ttk.Notebook(folders_window)
    notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    folders = ["Inbox", "Important", "Project", "Spam", "Work"]
    frames = {folder: ttk.Frame(notebook) for folder in folders}

    for folder in folders:
        notebook.add(frames[folder], text=folder)
        tree = ttk.Treeview(frames[folder], columns=(
            "Read", "Sender", "Subject"), show="headings")
        tree.heading("Read", text="Read")
        tree.heading("Sender", text="Sender")
        tree.heading("Subject", text="Subject")

        for email in LIST[folder]:
            if email[0] == 0:
                email[0] = "Read"
            else:
                email[0] = "Not Read"
            tree.insert("", tk.END, values=email)
            # print(email)

        tree.bind("<<TreeviewSelect>>", lambda event: on_email_selected(event))

        tree.pack(expand=tk.YES, fill=tk.BOTH)
    button_receive = ttk.Button(
        folders_window, text="Download Mail", command=downloadMail)
    button_receive.pack(pady=5)
        
# def show_mail_folders():
#     global frames
#     LIST = client.receive_mail();
    
#     folders_window = tk.Toplevel()
#     folders_window.title("Mail Folders")
#     folders_window.geometry("800x400")

#     notebook = ttk.Notebook(folders_window)
#     notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

#     folders = ["Inbox", "Important", "Project", "Spam", "Work"]
#     frames = {folder: ttk.Frame(notebook) for folder in folders}

#     for folder in folders:
#         notebook.add(frames[folder], text=folder)
#         tree = ttk.Treeview(frames[folder], columns=(
#             "Read", "Sender", "Subject"), show="headings")
#         tree.heading("Read", text="Read")
#         tree.heading("Sender", text="Sender")
#         tree.heading("Subject", text="Subject")

#         for email in LIST[folder]:
#             if email[0] == 0:
#                 email[0] = "Read"
#             else:
#                 email[0] = "Not Read"
#             tree.insert("", tk.END, values=email)
#             # print(email)

#         tree.bind("<<TreeviewSelect>>", lambda event: on_email_selected(event))

#         tree.pack(expand=tk.YES, fill=tk.BOTH)

def on_email_selected(event):
    selected_item = event.widget.selection()[0]
    values = list((event.widget.item(selected_item, 'values')))
    
    mail_window = tk.Toplevel()
    mail_window.title("Mail Content")
    mail_window.geometry("300x400")

    # Display email content
    infor_label = tk.Label(mail_window, text=f"Sender: {values[1]}\nSubject: {values[2]}\n\n")
    infor_label.pack()

    label_message = ttk.Label(mail_window, text="Message:")
    label_message.pack()

    # Assuming values[3] contains the text message
    values[4] = values[4].split(' ')
    if len(values[4]) != 0:
        number = len(values[4])
        values[3] += f"\nCó {number} file đính kèm: \n"
        for item in values[4]:
            values[3] += f'{item}\n'
    
    text_message = tk.Text(mail_window, wrap=tk.WORD, width=30, height=10)
    text_message.insert(tk.END, values[3])
    text_message.pack()
    button_attach = ttk.Button(mail_window, text="Download file")
    button_attach.grid(row=6, column=2, padx=10, pady=5)
    
create_email_composer()
