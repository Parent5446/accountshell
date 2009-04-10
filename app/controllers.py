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
				inmenu = 0
			else:
				request = app.models.Request(self.config, self.database)
				message = self.handleRequest(status, request)
				app.views.Common.PrintMessage(message)
		return 0
	def getMenuChoice(self):
		return app.views.AccountShell.MainMenu()
	def handleRequest(self, status, request):
		if status[0] == 'Request_Create':
			request.new = true
			request.putInfo(status[1])
			message = 'Account request successfully created.'
		elif status[0] == 'Request_Check':
			request.putInfo(status[1])
			if request.checkPassword(status[1]['password']) == 0:
				message = 'Either you have entered an incorrect username/password or your account has been approved.'
			else:
				message = 'Your request is still being processed.'
		elif status[0] == 'Request_Delete':
			request.putInfo(status[1])
			if request.checkPassword(status[1]['password']) == 0:
				message = 'Incorrect username/password.'
			else:
				oldrequest.deny()
				message = 'Request deleted successfully.'
		return message
