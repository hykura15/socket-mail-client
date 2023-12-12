import uuid
def generateRandomID():
       return "I" + str(uuid.uuid4().hex)

print(generateRandomID())