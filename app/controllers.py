from .views.AccountShell import AccountShell_MainMenu
from .views.AdminPanel import AdminPanel_MainMenu
from .views.Common import PrintMessage

class AccountShell():
	def __init__(self, config, database, request):
		self.config = config
		self.database = database
		self.request = request
	def execute(self):
		inmenu = 1
		while inmenu:
			status = AccountShell_MainMenu()
			if status == 1:
				return 1
			elif status == 0:
				inmenu = 0
			else:
				request = self.request.newInstance()
				message = self.handleRequest(status, request)
				PrintMessage(message)
		return 0
	def checkUsername(self, username):
		print '\n'
		retval = self.auth.authenticate()
		if retval == 1:
			PrintMessage("Username/Password authenticated.\n")
		else:
			PrintMessage("Incorrect username or password.\n")
		return retval
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
				request.deny()
				message = 'Request deleted successfully.'
			else:
				message = 'Incorrect username/password.'
		else:
			message = 0
		return message

class AdminPanel():
	def __init__(self, config, database, auth, request):
		self.config = config
		self.database = database
		self.request = request
		self.auth = auth
	def execute(self):
		if self.authenticateUser() != 1:
			return 0
		inmenu = 1
		while inmenu:
			status = AdminPanel_MainMenu(self.database.data)
			if status == 1:
				return 1
			elif status == 0:
				inmenu = 0
			else:
				request = self.request.newInstance()
				message = self.handleRequest(status, request)
				PrintMessage(message)
		return 0
	def authenticateUser(self):
		print '\n'
		retval = self.auth.authenticate()
		username = self.auth.getLastUsername()
		retval = retval and self.auth.isAdmin(username)
		if retval == 1:
			PrintMessage("Username/Password authenticated.\n")
		else:
			PrintMessage("Incorrect username or password.\n")
		return retval
	def handleRequest(self, status, request):
		if status[0] == 'Request_List()':
			message = ''
		elif status[0] == 'Request_Approve()':
			info = { status[1]['ref']: status[1]['id'] }
			request.putInfo(info)
			request.updateFromDatabase()
			request.approve()
			message = 'Request successfully approved.'
		elif status[0] == 'Request_Deny()':
			request.putInfo(status[1])
			request.updateFromDatabase()
			request.deny()
			message = 'Request successfully denied.'
		else:
			message = 0
		return message
