#!/usr/bin/python

# Loading modules and initiating variables.
import app.bootstrap
config = app.models.Config()
database = app.models.Database(config)
auth = app.models.Auth(config, database)
request = app.models.Request(config, database, auth)
controller1 = app.controllers.AccountShell(config, database, request)
controller2 = app.controllers.AdminPanel(config, database, auth, request)
controller3 = app.controllers.SuperuserPanel(config, database, auth, request)

database.updateFromFile()

menustatus = 2
while menustatus:
	if menustatus == 2:
		menustatus = controller1.execute()
		database.updateToFile()
	elif menustatus == 1:
		adminstatus = 2
		while adminstatus:
			if adminstatus == 2:
				adminstatus = controller2.execute()
				database.updateToFile()
			elif adminstatus == 1:
				superuserstatus = 2
				while superuserstatus:
					superuserstatus = controller3.execute()
					database.updateToFile()
				adminstatus = 2
		menustatus = 2
