from datetime import date
from datetime import timedelta

def obtainWeek():
  """ This funciton will return the weeks for the scripts
  It will get the sunday before (week) and the 2 weeks prioer sunday (weekQA) """

  week = date.today()
  """First we will set ourself in sunday. 
  Then, we will go 7 days back to previous sunday"""
  if week.isoweekday() != 7:
    week = week - timedelta(days=week.isoweekday())
  week = week - timedelta(days=7)
  #Now we go another 7 days back and we get QA week
  weekQA = week - timedelta(days=7)
  #Now we format it in Google Way
  # Format = YYYY-MM-DD
  week = "-".join([week.strftime("%Y"), week.strftime("%m"),week.strftime("%d")])
  weekQA = "-".join([weekQA.strftime("%Y"), weekQA.strftime("%m"),weekQA.strftime("%d")])
  weeklist = [week,weekQA]
  return weeklist