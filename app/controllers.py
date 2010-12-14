import views

class AccountShell():
	def __init__(self, config, database, auth, request):
		self.config = config
		self.database = database
		self.auth = auth
		self.request = request
	def execute(self):
		inmenu = 1
		while inmenu:
			status = views.AccountShell_MainMenu()
			if status == 1:
				return 1
			elif status == 0:
				inmenu = 0
			else:
				request = self.request.newInstance()
				message = self.handleRequest(status, request)
				views.PrintMessage(message)
		return 0
	def checkUsername(self, username):
		print '\n'
		retval = self.auth.authenticate()
		if retval == 1:
			views.PrintMessage("Username/Password authenticated.\n")
		else:
			views.PrintMessage("Incorrect username or password.\n")
		return retval
	def handleRequest(self, status, request):
		if status[0] == 'Request_Create()':
			request.new = 1
			status[1]["password"] = self.auth.generatePassword(status[1]["password"])
			request.putInfo(status[1])
			message = 'Account request successfully created.'
		elif status[0] == 'Request_Check()':
			request.putInfo(status[1])
			status[1]["password"] = self.auth.generatePassword(status[1]["password"])
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
			status = views.AdminPanel_MainMenu(self.database.data)
			if status == 1:
				return 1
			elif status == 0:
				inmenu = 0
			else:
				request = self.request.newInstance()
				message = self.handleRequest(status, request)
				views.PrintMessage(message)
		return 0
	def authenticateUser(self):
		print '\n'
		username = views.PrintMessage("Username: ")
		password = views.PasswordPrompt()
		retval = self.auth.authenticate(username, password) and self.auth.isAdmin(username)
		if retval == 1:
			views.PrintMessage("Username/Password authenticated.\n")
		else:
			views.PrintMessage("Incorrect username or password.\n")
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

class SuperuserPanel():
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
			status = views.SuperuserPanel_MainMenu(self.database.data)
			if status == 1:
				return 1
			elif status == 0:
				inmenu = 0
			else:
				request = self.request.newInstance()
				message = self.handleRequest(status, request)
				views.PrintMessage(message)
		return 0
	def authenticateUser(self):
		print '\n'
		retval = self.auth.authenticate()
		username = self.auth.getLastUsername()
		retval = retval and self.auth.isRoot(username)
		if retval == 1:
			views.PrintMessage("Username/Password authenticated.\n")
		else:
			views.PrintMessage("Incorrect username or password.\n")
		return retval
	def handleRequest(self, status, request):
		if status[0] == 'Request_Revoke()':
			if not self.auth.userExists(status[1]['username']):
				message = 'Username does not exist.'
			elif self.auth.deleteUser(status[1]['username']):
				message = 'User successfully deleted.'
			else:
				message = 'Unknown error.'
		elif status[0] == 'Request_Ban()':
			currbans = self.config.getOption('banned_names')
			currbans.append(status[1]['username'])
			self.config.putOption('banned_names', currbans)
			self.config.updateToFile()
			message = 'Username banned successfully.'
		elif status[0] == 'Request_Unban()':
			currbans = self.config.getOption('banned_names')
			currbans.remove(status[1]['username'])
			self.config.putOption('banned_names', currbans)
			self.config.updateToFile()
			message = 'Username unbanned successfully.'
		elif status[0] == 'Request_ToggleAll()':
			currstatus = self.config.getOption('enabled')
			if currstatus == 1 or currstatus == 'yes':
				currstatus = 0
				message = 'Account Shell was enabled. It is now disabled.'
			elif currstatus == 0 or currstatus == 'no':
				currstatus = 1
				message = 'Account Shell was disabled. It is now enabled.'
			else:
				currstatus = 'permanent'
				message = 'Account Shell has been manually disabled. It must be re-enabled directly from the configuration file.'
			self.config.putOption('enabled')
		else:
			message = 0
		return message
