import re, os, sys, grp, spwd, getpass, crypt, random, string

class Callable():
    def __init__(self, anycallable):
        self.__call__ = anycallable

class Config():
    """A class to maintain the program's configuration options."""
    data = {}
    def __init__(self):
        self.updateFromFile()
    def getOption(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return 0
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

class Log():
    def __init__(self, config):
        self.__config = config
        self.factory = 1
        self.loglevel = config.getOption('logging_level')
        if self.loglevel == 0:
            self.loglevel = '50'
        self.logformat = config.getOption('logging_format')
        if self.logformat == 0:
            self.logformat = '%(asctime)s (%(process)d) -- %(levelname)s: %(name) - %(message)s'
        self.logfile = config.getOption('logging_filename')
        logging.basicConfig(filename=self.logfile, format=self.logformat, level=self.loglevel)
    def loadLogger(self, name = ''):
        if self.factory:
            return 0
        logger = logging.getLogger(name)
        logger.setLevel(self.loglevel)
        self.logger = logger
    def log(self, level, callback, msg):
        if self.factory:
            return 0
        msg = "(callback) msg"
        level = level.strip().upper()
        if level == 'CRITICAL':
            level = 50
        elif level == 'ERROR':
            level = 40
        elif level == 'WARNING':
            level = 30
        elif level == 'INFO':
            level = 20
        elif level == 'DEBUG':
            level = 10
        self.logger.log(level, msg)
    def newInstance(self, name = ''):
        temp = Log(self.config)
        temp.factory = 0
        temp.loadLogger(name)
        return temp

class Database():
    """A class to maintain the program's configuration options."""
    data = []
    def __init__(self, config):
        self.config = config
        self.updateFromFile()
    def getLine(self, value, key = 'username'):
        if key == 'id':
            return self.data[int(value) - 1]
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
            for option in separated1:
                separated2 = re.split('\=', option)
                if separated2[0] != '':
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

class Auth():
    __pam = 0
    def __init__(self, config, database):
        self.config = config
        self.database = database
    def authenticate(self, username = None, password = None):
        try:
            shadow = spwd.getspnam(username)[1].split("$")
            salt = "$".join(shadow[:-1])
            thehash = shadow[-1]
            return crypt.crypt(password, salt) == "$".join(shadow)
        except KeyError:
            return False
    def makeUser(self, username, password):
        command = 'useradd -c "Created with account shell." -s /bin/bash -mg acctshell -p "'
        command = command + password + '" "' + username + '"'
        os.system(command)
        self.database.delLine(username)
    def isAdmin(self, username):
        return self.hasGroup(username, "admin")
    def isRoot(self, username):
        return self.hasGroup(username, "root")
    def hasGroup(self, username, group):
        for name in grp.getgrnam(group)[3]:
            if name == username:
                return 1
        return 0
    def generatePassword(self, password):
        return crypt.crypt(password, ''.join(random.sample(string.ascii_letters + string.digits, 20)))

class Request():
    __userinfo = {}
    loaded = 0
    new = 0
    factory = 0
    def __init__(self, config, database, auth):
        self.config = config
        self.database = database
        self.auth = auth
        self.factory = 1
    def getInfo(self, key):
        if self.factory:
            return 0
        if key == 'password' and self.config.getOption('request.passwordsafety'):
            return 0
        return self.__userinfo[key]
    def putInfo(self, info):
        if self.factory:
            return 0
        for key in info.keys():
            self.__userinfo[key] = info[key]
        if self.loaded or self.new:
            self.updateToDatabase()
        else:
            self.updateFromDatabase()
        return 1
    def checkPassword(self, password):
        if self.factory:
            return 0
        try:
            if password == self.__userinfo['password']:
                return 1
        except TypeError:
            return 0
        return 0
    def approve(self):
        if self.factory:
            return 0
        self.auth.makeUser(self.__userinfo['username'], self.__userinfo['password'])
        return 1
    def deny(self):
        if self.factory:
            return 0
        self.database.delLine(self.__userinfo['username'])
        self.__userinfo = {}
        return 1
    def updateToDatabase(self):
        if self.factory:
            return 0
        if self.new:
            self.database.addLine(self.__userinfo)
        else:
            for key in self.__userinfo.keys():
                self.database.changeLine('username', self.__userinfo['username'], key, self.__userinfo[key])
        return 1
    def updateFromDatabase(self):
        if self.factory:
            return 0
        for key in self.__userinfo.keys():
            self.__userinfo = self.database.getLine(self.__userinfo[key], key)
        self.loaded = 1
        return 1
    def newInstance(self):
        if self.factory == 0:
            return 0
        temp = Request(self.config, self.database, self.auth)
        temp.factory = 0
        return temp
