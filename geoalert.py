import json, requests
import time

from alert import alertSetup, sendAlert
from helper import checkPointInsidePolygon, parseJson


# Global Variables
QUERIES_PER_SEC = 1

# Geolocate and Alerting Function

def geolocateAlert(clinicianIDs, mode):
	"""
	We want to operate at a speed that won't overload the Clinician Status API.

	Here I chose to used two ways of finding how long to wait between requests.
	1) Using limit of delaying response by at most (5 minutes - 10 seconds) to save resources.
	2) Using limit of maximum queries per second to find out how long to wait.

	Here, I choose the maximum which means whichever waits to longest (to save resources).
	"""
	numClinicians = len(clinicianIDs)
	waitInterval = 0

	while True:
		for cID in clinicianIDs:

			# Make sure we are not over requesting the API (we want less than 100 queries/s).
			time.sleep(waitInterval)
			start = time.time()

			if mode == "debug":
				jsonFile = open('test_data/clinician'+str(cID)+'_location.json',)
				jsonObject = json.load(jsonFile)
			else:
				response = requests.get("https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test"+ "/clinicianstatus/" + str(cID))
				if response.status_code == 200:
					jsonObject = response.json()
					if mode == "saveJson":
						with open('test_data/clinician' + str(cID) + '_location.json', 'w') as jsonFile:
							json.dump(jsonObject, jsonFile)
				else:
					sendAlert("APIrequestFailed", cID)

			point, polygons = parseJson(jsonObject)

			if point == None or polygons == None:
				sendAlert("inputError", None)
				return

			if checkPointInsidePolygon(point, polygons) == False:
				print("Clinician Out of Bounds: ")
				print(json.dumps(jsonObject, indent=4))
				sendAlert("clinicianOutbound", cID)

			end = time.time()

			# Calculate new wait time based on new data
			timeElapsed = end-start
			waitInterval = max((5.0*60.0 - timeElapsed*numClinicians - 10.0) / numClinicians, 1.0 / QUERIES_PER_SEC - timeElapsed, 0)

		if mode == "saveJson":
			break


if __name__ == "__main__":
	clinicianIDs = []

	n = int(input("Enter number of clinicians to monitor: "))

	for i in range(n):
		newClinicianID = int(input("Enter new clinician ID: "))
		print("Added clinician ID: " + str(newClinicianID))

		clinicianIDs.append(newClinicianID)

	print("\nSetting up alert system.\n")
	alertSetup()

	print("\nMonitoring In Progress. End program to stop monitoring.\n")
	geolocateAlert(clinicianIDs, "")



