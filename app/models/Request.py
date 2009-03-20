import os

class Request():
	userinfo = {}
	loaded = false
	def __init__(self, config, database):
		self.config = config
		self.database = database
	def getInfo(self, key):
		if key == 'password':
			return false
		return self.userinfo[key]
	def putInfo(self, info):
		for key in info.keys:
			self.userinfo[key] = info[key]
		if self.loaded:
			self.updateToDatabase()
		else:
			self.uddateFromDatabase()
		return true
	def approve(self):
		command = 'useradd -c "Created with account shell." -mg acctshell -k /opt/acctshell/defaulthome -p "'
		command = command + self.userinfo['password'] + '" "' + self.userinfo['username'] + '"'
		os.system(command)
		self.database.delLine(self.userinfo['username'])
		return true
	def deny(self):
		self.database.delLine(self.userinfo['username'])
		userinfo = {}
		return true
	def updateToDatabase(self):
		for key in self.userinfo.keys():
			self.database.changeLine('username', self.userinfo['username'], key, info[key])
		return true
	def updateFromDatabase(self):
		userinfo = self.database.getLine(userinfo['username'])
		return true
