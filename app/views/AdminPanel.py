import Common

def AdminPanel_MainMenu(requests):
	Common.ClearScreen()
	title   = 'Main Menu'
	choices = [ 'List open requests', 'Approve a request',
                    'Deny a request', 'Superuser Panel', 'Exit/Return' ]
	actions = [ 'Request_List', 'Request_Approve',
                    '2', '1', '0' ]
	choice = Common.ShellMenu(title, choices, actions)
	if choice == '1()':
		return 1
	elif choice != '0()':
		return [ choice, eval(choice) ]
	else:
		return 0

def Request_List(requests):
	for request in requests:
		message  = ""
		username = request['username']
		realname = request['realname']
		email    = request['email']
		comments = request['comments']
		message  = message + "Request #: key\n" + \
			"Username: username\n" + \
			"Real Name: realname\n" + \
			"Email: email\n" + \
			"Comments:\ncomments\n\n"
		Common.PrintMessage(message)
	return 0

def Request_Approve(requests):
	title  = 'Approve an account request:'
	header = 'This will create an account based on a given request.'
	questions = { 'ref': 'Enter the name of the identifying resource (id, username, etc.): ',
		      'id':  'Enter the value of the resource: ' }
	answers = Common.QuestionList(title, header, questions)
	return answers

def Request_Deny(requests):
	title  = 'Deny an account request:'
	header = 'This will remove a request from the system.'
	questions = { 'ref': 'Enter the name of the identifying resource (id, username, etc.): ',
		      'id':  'Enter the value of the resource: ' }
	answers = Common.QuestionList(title, header, questions)
	retval = { answers['ref']: answers['id'] }
	return retval
