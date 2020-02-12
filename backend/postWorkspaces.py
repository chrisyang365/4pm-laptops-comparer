import json
from pymongo import MongoClient
import sys

from mongoSetup import connect_database, get_user_auth

# POST /workspaces
# Creates a new workspace, returns the id of the workspace
def create_workspace(event, context):
	db = connect_database()

	body = {}

	authorizer_response = event

	try:
		user_info = get_user_auth(event)
		# Check to see if the user in the the user collections if not store into user collection
		user = db.users.find_one({"google_client_id": user_info["g_id"]})
		if user is None:
			user = {"google_client_id": user_info["g_id"], "name": user_info["name"]}
			db.users.insert_one(user)
			print("user(", user_info["g_id"],") not found, new user created")
		print("user:", user)

		# Create new workspace owned by user with default untitled name
		new_workspace = {"owner": user_info["g_id"], "name": "Untitled Workspace", "products": []}
		new_id = db.workspaces.insert_one(new_workspace).inserted_id
		print("new workspace inserted, workspace id:", str(new_id))
		body["_id"] = str(new_id)
		errorCode = {"code": 0, "message": "SUCCESS: no error"}

		response = {
			"statusCode": 200,
			"errorCode": errorCode,
			"body": json.dumps(body)
		}
		return response
	except:
		e = sys.exc_info()[0]
		errorCode = {"code": 1}
		errorCode["message"] = "ERROR: " + str(e)
		response = {
			"statusCode": 200,
			"errorCode": errorCode,
			"body": json.dumps(body)
		}
		print("ERROR:", sys.exc_info()[1])
		return response


