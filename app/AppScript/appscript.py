#The script is 

from googleapiclient.discovery import build

def runScript(SCRIPT_ID,creds):
  if not creds or not creds.valid:
    print("invalid creds")
    return "Invalid Credentials"
  service = build('script', 'v1', credentials=creds)
  request = {"function": "driveTest"}
  response = service.scripts().run(body=request,
    scriptId=SCRIPT_ID).execute()
  print(response)
  return response

def runScriptParams(SCRIPT_ID,creds,function,params):
  """ This function will update the parameters 
  of the API FILE"""
  if not creds or not creds.valid:
    print("invalid creds")
    return "Invalid Credentials"

  service = build('script', 'v1', credentials=creds)
  request = {
    "function": function,
    "parameters":[params]}
  response = service.scripts().run(body=request,
    scriptId=SCRIPT_ID).execute()
  return response
