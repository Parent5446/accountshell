import re

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
