class AccountShell():
	def __init__(self, config, database):
		self.config = config
		self.database = database
	def execute(self):
		inmenu = 1
		while inmenu:
			status = app.views.AccountShell.MainMenu()
			if status == 1:
				return 1
			elif status == 0:
				inmenu = false
			else:
				if status[0] == 'Request_Create':
					newrequest = app.models.Request(self.config, self.database)
					newrequest.new = true
					newrequest.putInfo(status[1])
				elif status[0] == 'Request_Check':
					oldrequest = app.models.Request(self.config, self.database)
					oldrequest.putInfo(status[1])
					if oldrequest.checkPassword(status[1]['password']) == 0:
						message = 'Either you have entered an incorrect username/password or your account has been approved.'
					else:
						message = 'Your request is still being processed.'
					app.views.Common.PrintMessage(message)
				elif status[0] == 'Request_Delete':
					oldrequest = app.models.Request(self.config, self.database)
					oldrequest.putInfo(status[1])
					if oldrequest.checkPassword(status[1]['password']) == 0:
						message = 'Incorrect username/password.'
					else:
						oldrequest.deny()
						message = 'Request deleted successfully.'
		return 0
