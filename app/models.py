import re
import os

class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

class Config():
	"""A class to maintain the program's configuration options."""
	data = {}
	def __init__(self):
		self.updateFromFile()
	def getOption(self, key):
		return self.data[key]
	def putOption(self, key, value):
		self.data[key] = value
	def updateFromFile(self, filename = ''):
		if filename == '':
			filename = 'data/config'
		configfile = open(filename, 'r')
		rawoptions = configfile.readlines()
		configfile.close()
		temp = {}
		for rawoption in rawoptions:
			rawoption = rawoption.rstrip("\n")
			separated = re.split('\=', rawoption)
			temp[separated[0]] = separated[1]
		self.data = temp
		return 1
	def updateToFile(self, filename = ''):
		if filename == '':
			filename = 'data/config'
		configfile = open(filename, 'w')
		temp = []
		for key in self.data.keys():
			temp.append(key + "=" + self.data[key])
		configfile.writelines(temp)
		configfile.close()
		return 1

class Database():
	"""A class to maintain the program's configuration options."""
	data = []
	def __init__(self, config):
		self.config = config
		self.updateFromFile()
	def getLine(self, value, key = 'username'):
		for dataset in self.data:
			if dataset[key] == value:
				return dataset
		return 0
	def addLine(self, information):
		self.data.append(information)
		self.updateToFile()
		return 1
	def changeLine(self, identifierkey, identifier, key, value):
		for dataset in self.data:
			if dataset[identifierkey] == identifier:
					if dataset[key] != value:
						dataset[key] = value
		return 1
	def changeFullLine(self, identifierkey, identifier, info):
		for dataset in self.data:
			if dataset[identifierkey] == identifier:
				dataset = info
		return 1			
	def delLine(self, value, key = 'username'):
		for dataset in self.data:
			if dataset[key] == value:
				self.data.remove(dataset)
		return 1
	def updateFromFile(self):
		datafile = open(self.getRequestFilename(), 'r')
		lines = datafile.readlines()
		datafile.close()
		temp = {}
		for line in lines:
			templine = {}
			separated1 = re.split('\;', line)
			for option in separated:
				separated2 = re.split('\=', option)
				templine[separated2[0]] = separated2[1]
			self.data.append(templine)
		return 1
	def updateToFile(self):
		temp = []
		for dataset in self.data:
			line = ''
			for key in dataset.keys():
				line = line + key + '=' + dataset[key] + ';'
			temp.append(line)
		datafile = open(self.getRequestFilename(), 'w')
		datafile.writelines(temp)
		datafile.close()
		return 1
	def getRequestFilename(self):
		return os.path.abspath(self.config.getOption('database.filename'))

class Request():
	userinfo = {}
	loaded = 0
	new = 0
	factory = 0
	def __init__(self, config, database):
		self.config = config
		self.database = database
		self.factory = 1
	def getInfo(self, key):
		if self.factory:
			return false
		if key == 'password':
			return 0
		return self.userinfo[key]
	def putInfo(self, info):
		if self.factory:
			return false
		for key in info.keys():
			self.userinfo[key] = info[key]
		if self.loaded or self.new:
			self.updateToDatabase()
		else:
			self.updateFromDatabase()
		return 1
	def checkPassword(self, password):
		if self.factory:
			return false
		if password == self.userinfo['password']:
			return 1
		return 0
	def approve(self):
		if self.factory:
			return false
		command = 'useradd -c "Created with account shell." -mg acctshell -k /opt/acctshell/defaulthome -p "'
		command = command + self.userinfo['password'] + '" "' + self.userinfo['username'] + '"'
		os.system(command)
		self.database.delLine(self.userinfo['username'])
		return 1
	def deny(self):
		if self.factory:
			return false
		self.database.delLine(self.userinfo['username'])
		userinfo = {}
		return 1
	def updateToDatabase(self):
		if self.factory:
			return false
		for key in self.userinfo.keys():
			self.database.changeLine('username', self.userinfo['username'], key, self.userinfo[key])
		return 1
	def updateFromDatabase(self):
		if self.factory:
			return false
		userinfo = self.database.getLine(userinfo['username'])
		return 1
	def newInstance(self):
		if self.factory == 0:
			return false
		temp = Request(self.config, self.database)
		temp.factory = 0
		return temp