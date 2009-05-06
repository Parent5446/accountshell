from .views.AccountShell import MainMenu
from .views.Common import PrintMessage

class AccountShell():
	def __init__(self, config, database, request):
		self.config = config
		self.database = database
		self.request = request
	def execute(self):
		inmenu = 1
		while inmenu:
			status = MainMenu()
			if status == 1:
				return 1
			elif status == 0:
				inmenu = 0
			else:
				request = self.request.newInstance()
				message = self.handleRequest(status, request)
				PrintMessage(message)
		return 0
	def getMenuChoice(self):
		return app.views.AccountShell.MainMenu()
	def handleRequest(self, status, request):
		if status[0] == 'Request_Create()':
			request.new = 1
			request.putInfo(status[1])
			message = 'Account request successfully created.'
		elif status[0] == 'Request_Check()':
			request.putInfo(status[1])
			if request.checkPassword(status[1]['password']):
				message = 'Your request is still being processed.'
			else:
				message = 'Either you have entered an incorrect username/password or your account has been approved.'
		elif status[0] == 'Request_Delete()':
			request.putInfo(status[1])
			if request.checkPassword(status[1]['password']):
				oldrequest.deny()
				message = 'Request deleted successfully.'
			else:
				message = 'Incorrect username/password.'
		else:
			message = 0
		return message
