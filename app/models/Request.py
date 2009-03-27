import os

class Request():
	userinfo = {}
	loaded = 0
	new = 0
	def __init__(self, config, database):
		self.config = config
		self.database = database
	def getInfo(self, key):
		if key == 'password':
			return 0
		return self.userinfo[key]
	def putInfo(self, info):
		for key in info.keys:
			self.userinfo[key] = info[key]
		if self.loaded or self.new:
			self.updateToDatabase()
		else:
			self.updateFromDatabase()
		return 1
	def checkPassword(self, password):
		if password == self.userinfo['password']:
			return 1
		return 0
	def approve(self):
		command = 'useradd -c "Created with account shell." -mg acctshell -k /opt/acctshell/defaulthome -p "'
		command = command + self.userinfo['password'] + '" "' + self.userinfo['username'] + '"'
		os.system(command)
		self.database.delLine(self.userinfo['username'])
		return 1
	def deny(self):
		self.database.delLine(self.userinfo['username'])
		userinfo = {}
		return 1
	def updateToDatabase(self):
		for key in self.userinfo.keys():
			self.database.changeLine('username', self.userinfo['username'], key, info[key])
		return 1
	def updateFromDatabase(self):
		userinfo = self.database.getLine(userinfo['username'])
		return 1
