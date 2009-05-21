#!/usr/bin/python

# Loading modules and initiating variables.
import app.bootstrap
config = app.models.Config()
database = app.models.Database(config)
request = app.models.Request(config, database)
controller1 = app.controllers.AccountShell(config, database, request)
controller2 = app.controllers.AdminPanel(config, database, request)

database.updateFromFile()

menustatus = 2
while menustatus:
	if menustatus == 2:
		menustatus = controller1.execute()
		database.updateToFile()
	elif menustatus == 1:
		adminstatus = 2
		while adminstatus == 2:
			adminstatus = controller2.execute()
			database.updateToFile()
