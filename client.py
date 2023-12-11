import base64
import socket
import os
import time
import json

FORMAT = 'utf-8'
boundary = 'boundary'
def loadConfig():
    config = {}
    try:
        with open("config.json", 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        print("Error: Config file not found.")
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON in config file.")
    return config

config = loadConfig()

def handleSendFile(client, filePath):
    try:
        client.sendall(f'--{boundary}\r\n'.encode(FORMAT))
        with open(filePath, 'rb') as file:
            fileContent = base64.b64encode(file.read()).decode(FORMAT)
            message = (
                f'Content-Type: application/octet-stream; name="{os.path.basename(filePath)}"\r\n'
                f'Content-Disposition: attachment; filename="{os.path.basename(filePath)}"\r\n'
                f'Content-Transfer-Encoding: base64\r\n\n'
            )
            listFileContents = splitStringIntoChunks(fileContent, 72*5)
            client.sendall(message.encode(FORMAT))
            for item in listFileContents:
                client.sendall(f'{item}\r\n'.encode(FORMAT))
    except FileNotFoundError:
        print(f"Error: File {filePath} not found.")
    except Exception as e:
        print(f"Error while handling file: {e}")

def sendMail(senderMail, recipientMail, ccMail, bccMail, subjectMail, messageBody, filePaths):
    try:
        mailServer = config["mailServer"]
        SMTP = config["SMTP"]

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((mailServer, SMTP))
        receiveResponse(client)

        sendCommand(client, f'EHLO {mailServer}\r\n')
        receiveResponse(client)

        sendCommand(client, f'MAIL FROM:<{senderMail}>\r\n')
        receiveResponse(client)

        for item in recipientMail:
            sendCommand(client, f'RCPT TO:<{item}>\r\n')
            receiveResponse(client)
        for item in ccMail:
            sendCommand(client, f'RCPT TO:<{item}>\r\n')
            receiveResponse(client)
        for item in bccMail:
            sendCommand(client, f'RCPT TO:<{item}>\r\n')
            receiveResponse(client)

        sendCommand(client, 'DATA\r\n')
        receiveResponse(client)

        message = ""
        if len(filePaths) != 0:
            message += (
                f'MIME-Version: 1.0\r\n'
                f'Content-Type: multipart/mixed; boundary={boundary}\r\n'
            )
        for item in recipientMail:
            message += f'To: {item}\r\n'
        for item in ccMail:
            message += f'Cc: {item}\r\n'
        message += (
            f'From: {senderMail}\r\n'
            f'Subject: {subjectMail}\r\n'
        )
        
        if len(filePaths) != 0:
            message += f'\r\n--{boundary}\r\n'
            
        message += (
            f'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n'
            f'Content-Transfer-Encoding: 7bit\r\n\r\n'
            f'{messageBody}\r\n'
        )
        client.sendall(message.encode(FORMAT))

        if len(filePaths) != 0:
            for item in filePaths:
                handleSendFile(client, item)
            client.sendall(f'--{boundary}--\r\n'.encode(FORMAT))

        #End
        client.sendall(b'\r\n.\r\n')
        receiveResponse(client)
        sendCommand(client, 'QUIT\r\n')
        receiveResponse(client)

    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Error while sending mail: {e}")

def splitStringIntoChunks(inputString, chunkSize):
    numberChunks = (len(inputString) + chunkSize - 1) // chunkSize
    chunks = [inputString[i * chunkSize:(i + 1) * chunkSize]
              for i in range(numberChunks)]
    return chunks

def receiveMail():
    try:
        mailServer = config["mailServer"]
        POP3 = config["POP3"]
        USER = config["username"]
        PASS = config["password"]
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((mailServer, POP3))
        receiveResponse(client)
        sendCommand(client, f'CAPA\r\n')
        receiveResponse(client)
        sendCommand(client, f'USER {USER}\r\n')
        receiveResponse(client)
        sendCommand(client, f'PASS {PASS}\r\n')
        receiveResponse(client)
        client.sendall(f'STAT\r\n'.encode(FORMAT))
        mailNumber = client.recv(1024).decode(FORMAT).split(' ')[1]
        sendCommand(client, f'LIST\r\n')
        receiveResponse(client)
        sendCommand(client, f'UIDL\r\n')
        receiveResponse(client)

        LIST = mailList(client, mailNumber)

        # sendCommand(client, f'QUIT\r\n')
        # receiveResponse(client)

        return LIST
    
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Error while receiving mail: {e}")

    

def receiveTimeOut(client, timeout=2):
    client.setblocking(0)
    totalData = []
    data = b''
    timeBegin = time.time()
    while True:
        if totalData and time.time() - timeBegin > timeout:
            break
        elif time.time() - timeBegin > timeout * 2:
            break
        try:
            data = client.recv(8192)
            if data:
                totalData.append(data)
                timeBegin = time.time()
            else:
                time.sleep(0.1)
        except socket.error as e:
            pass
    return b''.join(totalData).decode(FORMAT)

def filterMail(LIST):
    filteredMails = []
    rules = config["rules"]
    for email in LIST["Inbox"]:
        shouldMove = False
        for rule in rules:
            filterType = rule["type"]
            if filterType == "from":
                if any(addr in email[1] for addr in rule["addresses"]):
                    shouldMove = True
            elif filterType == "subject":
                if any(keyword in email[2] for keyword in rule["keywords"]):
                    shouldMove = True
            elif filterType == "content":
                if any(keyword in email[3] for keyword in rule["keywords"]):
                    shouldMove = True
            elif filterType == "spam":
                if any(keyword in email[2] or keyword in email[3] for keyword in rule["keywords"]):
                    shouldMove = True
            if shouldMove:
                filteredMails.append(email)
                LIST[rule["folder"]].append(email)
                shouldMove = False
    LIST["Inbox"] = [email for email in LIST["Inbox"] if email not in filteredMails]
    return LIST

def mailList(client, mailNumber):
    LIST = {
        "Inbox": [],
        "Important": [],
        "Work": [],
        "Project": [],
        "Spam": []
    }
    if int(mailNumber) == 0:
        sendCommand(client, f'QUIT\r\n')
        receiveResponse(client)
        return None
    
    try:
        newInbox = [] 
        for num in range(1, int(mailNumber) + 1, 1):
            client.sendall(f'RETR {num}\r\n'.encode(FORMAT))
            mailData = receiveTimeOut(client).split('\r\n')
            _hadFile = 0
            _indexOf = []
            _from = ""
            _subject = ""
            _body = []
            _fileNames = []
            _fileContents = []
            for index in range(len(mailData)):
                i = mailData[index].find('filename=')
                if i != -1:
                    _fileNames.append(mailData[index][i + 10: -1])
                    _fileNames[-1] = _fileNames[-1].replace(' ', '_')
                    _hadFile = 1
                    _indexOf.append(index + 3)
            bodyStartIndex = 0
            bodyEndIndex = len(mailData) - 3
            for index in range(len(mailData)):
                i = mailData[index].find("From: ")
                if i != -1:
                    _from = mailData[index][i+6:]
                    _subject = mailData[index + 1][i+9:]
                    if _hadFile == 0:
                        bodyStartIndex = index + 5
                    else:
                        bodyStartIndex = index + 7
                
            if _hadFile != 0:
                idx = mailData.index(f'--{boundary}', 0)
                idx = mailData.index(f'--{boundary}', idx + 1)
                bodyEndIndex = idx
            _body = mailData[bodyStartIndex:bodyEndIndex]
            if _hadFile == 1:
                for j in range(len(_indexOf) - 1):
                    _fileContents.append(''.join(mailData[_indexOf[j]:_indexOf[j + 1] - 5]))
                _fileContents.append(''.join(mailData[_indexOf[len(_indexOf) - 1]:len(mailData) - 4]))
            
            LIST["Inbox"].append(["Not Seen",_from, _subject, '\r\n'.join(_body), _fileNames, _fileContents])
            client.sendall(f'DELE {num}\r\n'.encode(FORMAT))
            receiveResponse(client)

    except socket.error as e:
        print(f"Socket error: {e}")
        
    sendCommand(client, f'QUIT\r\n')
    receiveResponse(client)

    data = {}
    
    with open('data.json', 'r') as file:
        data = json.load(file)
        
    newList = filterMail(LIST)
   
    for item in newList:
        data[item] = newList[item] + data[item]

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)
    
    return data

def sendCommand(socket, command):
    socket.sendall(command.encode(FORMAT))


def receiveResponse(socket):
    try:
        response = socket.recv(1024).decode(FORMAT)
    except BlockingIOError:
        pass


if __name__ == '__main__':
    try:
        # sendMail()
        receiveMail()
    except Exception as e:
        print(f"An error occurred: {e}")