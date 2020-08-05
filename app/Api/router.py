#########################
####  API Blueprint ####
#########################

from flask import (
	Flask, 
	redirect, 
	request, 
	url_for, 
	render_template, 
	session, 
	Blueprint, 
	jsonify
)

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from AppScript.appscript import (
	runScript, 
	runScriptParams
)
from .rest_api import (
	obtainWeek
)
from .drive_api  import (
	copyExport,
	checkWeekMBR,
	)

#We define the blueprint for this Module
rest_api = Blueprint('api', __name__)

@rest_api.route("/rest/api/workflow/automatic_exports")
def automatic_exports():
	''' This is the endpoint for the automatic Exports
	Here, we should we able to:
	1. Update params.
	2. Update data.
	3. Copy the file to a new destination.
	4. Save the successfull information.
 '''

	#We trigger aciton 1. and 2. in one step.
	if request.method == 'POST':
		
	script_id = "MMMdukaY--Baxrg7OEIVFiqbTwlO3JCQl"
	parameters = obtainWeek()
	function = "automaticWeekExport"
	runScriptParams(script_id,
		current_user.creds,
		function,
		parameters)
	#Now, we do step 3.
	week = obtainWeek()
	print(week)
	monthId = checkWeekMBR(current_user.creds,week[0])
	copyExport(current_user.creds,destinationId=monthId)
	#TODO step 4.
	return "Automatic Exports Finished",200


@rest_api.route("/rest/api/test")
def test():
	''' Test Endpoint'''
	week = obtainWeek()
	monthId = checkWeekMBR(current_user.creds,week)
	copyExport(current_user.creds,destinationId=monthId)
	return jsonify(week)
