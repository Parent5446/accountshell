import re

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
		return false
	def addLine(self, information):
		self.data.append(information)
		self.updateToFile()
		return true
	def changeLine(self, identifierkey, identifier, key, value):
		for dataset in self.data:
			if dataset[identifierkey] == identifier:
					if dataset[key] != value:
						dataset[key] = value
		return true
	def changeFullLine(self, identifierkey, identifier, info):
		for dataset in self.data:
			if dataset[identifierkey] == identifier:
				dataset = info
		return true			
	def delLine(self, value, key = 'username'):
		for dataset in self.data:
			if dataset[key] == value:
				self.data.remove(dataset)
		return true
	def updateFromFile(self):
		datafile = open(self.getRequestFilename(), 'r')
		lines = configfile.readlines()
		data.close()
		temp = {}
		for line in lines:
			templine = {}
			separated1 = re.split('\;', line)
			for option in separated:
				separated2 = re.split('\=', option)
				templine[separated2[0]] = separated2[1]
			self.data.append(templine)
		return true
	def updateToFile(self):
		datafile = open(self.getRequestFilename(), 'w')
		temp = []
		for dataset in self.data:
			line = ''
			for key in dataset.keys():
				line = line + key + '=' + dataset[key] + ';'
			temp.append(line)
		datafile.writelines(temp)
		datafile.close()
		return true
	def getRequestFilename():
		return self.config.getOption('database.filename')
