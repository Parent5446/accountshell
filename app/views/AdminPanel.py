import Common

def AdminPanel_MainMenu(requests):
	Common.ClearScreen()
	title   = 'Main Menu'
	choices = [ 'List open requests', 'Approve a request',
                    'Deny a request', 'Superuser Panel', 'Exit/Return' ]
	actions = [ 'Request_List(' + repr(requests) + ') #', 'Request_Approve',
                    '2', '1', '0' ]
	choice = Common.ShellMenu(title, choices, actions)
	if choice == '1()':
		return 1
	elif choice != '0()':
		return [ choice, eval(choice) ]
	else:
		return 0

def Request_List(requests):
	key = 0
	for request in requests:
		key = key + 1
		message  = ""
		username = request['username']
		realname = request['realname']
		email    = request['email']
		comments = request['comments']
		message  = message + "Request #: " + repr(key) + "\n" + \
			"Username: " + repr(username) + "\n" + \
			"Real Name: " + repr(realname) + "\n" + \
			"Email: " + repr(email) + "\n" + \
			"Comments:\n" + repr(comments) + "\n"
		Common.PrintMessage(message)

def Request_Approve():
	title  = 'Approve an account request:'
	header = 'This will create an account based on a given request.'
	questions = { 'ref': 'Enter the name of the identifying resource (id, username, etc.): ',
		      'id':  'Enter the value of the resource: ' }
	answers = Common.QuestionList(title, header, questions)
	return answers

def Request_Deny():
	title  = 'Deny an account request:'
	header = 'This will remove a request from the system.'
	questions = { 'ref': 'Enter the name of the identifying resource (id, username, etc.): ',
		      'id':  'Enter the value of the resource: ' }
	answers = Common.QuestionList(title, header, questions)
	retval = { answers['ref']: answers['id'] }
	return retval
