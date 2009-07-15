#!/usr/bin/python

# Loading models.
import app.models
config = app.models.Config()
database = app.models.Database(config)
auth = app.models.Auth(config, database)
request = app.models.Request(config, database, auth)

# Feed models to controllers.
import app.controllers
controller1 = app.controllers.AccountShell(config, database, auth, request)
controller2 = app.controllers.AdminPanel(config, database, auth, request)
controller3 = app.controllers.SuperuserPanel(config, database, auth, request)

# Load database for use.
database.updateFromFile()

# Beginning menu
menustatus = 2
while menustatus:
	if menustatus == 2:
		# In Main Menu
		menustatus = controller1.execute()
		database.updateToFile()
	elif menustatus == 1:
		# Menu Change Triggered
		adminstatus = 2
		while adminstatus:
			# In Admin Menu
			if adminstatus == 2:
				adminstatus = controller2.execute()
				database.updateToFile()
			elif adminstatus == 1:
				# Menu Change Triggered
				superuserstatus = 2
				while superuserstatus:
					# In Superuser Panel
					superuserstatus = controller3.execute()
					database.updateToFile()
				# Out of Superuser Panel
				adminstatus = 2
		# Out of Admin Panel
		menustatus = 2
	# Out of Main Menu
