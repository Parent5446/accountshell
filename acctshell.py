#!/usr/bin/python

# Loading modules and initiating variables.
import app.bootstrap
config = app.models.Config()
database = app.models.Database(config)
request = app.models.Request(config, database)
controller = app.controllers.AccountShell(config, database, request)

database.updateFromFile()

menustatus = 2
while menustatus:
	if menustatus == 2:
		menustatus = controller.execute()
		database.updateToFile()
#	elif menustatus == 1:
		# Admin Panel
