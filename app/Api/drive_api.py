from googleapiclient.discovery import build

def copyExport(creds,destinationId):
  """After params and data update, we need to move the file
  to a new location. For this, we will copy the file in memory,
  and later we will create a new file in the wbr - exports folder
  separated by year and by folder """
  file_id = "1B1sMf0Yapurr3zsv__yklk3zingbgBkvBBzizfIZfeA"
  dest_id = "1LycHynTKCrUngdCcARkDDl2YvI8_3aha"

  if not creds or not creds.valid:
    return "Invalid Credentials"
  #We build the service
  service = build('drive','v3',credentials=creds)
  #We copy the file
  copy = service.files().copy(
    fileId=file_id,
    supportsAllDrives="true",
    fields="id,parents",
    body={"name":"copiedFile"}).execute()

  #We update it's parents to move it
  service.files().update(
    fileId=copy.get("id"),
    addParents=destinationId,
    removeParents=copy.get("parents")[0],
    supportsAllDrives="true",
    fields="id, parents").execute()
  return "succes"

def checkWeekMBR(creds,date):
  """ This funciton will return the correct parent_id
  for the year-->month correc mbr location based on the
  week of creation. """
  #WBR - Exports root folder
  rootFolder = '1yNGTGkwput2SjUZH0BWERy7m-RuI22l-'
  sharedDrive = '0AGeYQIu1o97XUk9PVA'
  if not creds or not creds.valid:
    return "Invalid Credentials"
  #We build the drive service
  #We build the service
  drive = build('drive','v3',credentials=creds)
  #First, we check there is a correct year folder
  year = date[0:4]
  month = int(date[6:7])
  query = "mimeType='application/vnd.google-apps.folder' and '{}' in parents".format(rootFolder)
  yearFolders = drive.files().list(
    q=query,
    corpora='drive',
    driveId=sharedDrive,
    includeItemsFromAllDrives="true",
    spaces="drive",
    supportsAllDrives="true",
    fields='files(id, name)'
    ).execute()

  #Let's find the year folder
  #We will assume we will always find the year folder.
  for files in yearFolders.get("files"):
    if files.get("name") == year:
      year_id = files.get("id")

  #We did find the year folder, so we use it to search the month.
  rootFolder = year_id
  query = "mimeType='application/vnd.google-apps.folder' and '{}' in parents".format(rootFolder)
  monthFolders = drive.files().list(
    q=query,
    corpora='drive',
    driveId=sharedDrive,
    includeItemsFromAllDrives="true",
    spaces="drive",
    supportsAllDrives="true",
    fields='files(id, name)'
    ).execute()

  #Now, if we find the month, we use it.
  #Otherwise, we create a new folder.
  monthDicts = ["January", "February","March","April","May","June","July","August",
  "September","October","November","December"]
  monthFound = 0
  for monthF in monthFolders.get("files"):
    if monthF.get("name") == monthDicts[month-1]:
      month_id = monthF.get("id")
      monthFound = 1

  #We found the month ID, we just return it.
  if monthFound == 1:
    return month_id
  #We didn't found the month, we create a new one.
  else:
    parentsList = [year_id]
    file_metadata = {
      'name': monthDicts[month-1],
      'mimeType': 'application/vnd.google-apps.folder',
      "parents": parentsList}
    file = drive.files().create(
      body=file_metadata,
      supportsAllDrives="true",
      fields='id,parents').execute()

    return file.get("id")