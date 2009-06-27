import getpass

def AccountShell_MainMenu():
	ClearScreen()
	title   = 'Main Menu'
	choices = [ 'Create a new account request', 'Check an existing account request',
                    'Delete an existing request', 'Administrative Panel', 'Exit/Stop' ]
	actions = [ 'Request_Create', 'Request_Check',
                    'Request_Delete', '1', '0' ]
	choice = ShellMenu(title, choices, actions)
	if choice == '1()':
		return 1
	elif choice != '0()':
		return [ choice, eval(choice) ]
	else:
		return 0

def AdminPanel_MainMenu(requests):
	ClearScreen()
	title   = 'Admin Panel'
	choices = [ 'List open requests', 'Approve a request',
                    'Deny a request', 'Superuser Panel', 'Exit/Return' ]
	actions = [ 'Request_List(' + repr(requests) + ') #', 'Request_Approve',
                    '2', '1', '0' ]
	choice = ShellMenu(title, choices, actions)
	if choice == '1()':
		return 1
	elif choice != '0()':
		return [ choice, eval(choice) ]
	else:
		return 0

def SuperuserPanel_MainMenu(requests):
	ClearScreen()
	title   = 'Superuser Panel'
	choices = [ 'Delete a user', 'Ban a username',
                    'Unban a username', 'Turn on/off accountshell', 'Exit/Return' ]
	actions = [ 'Request_Revoke', 'Request_Ban',
                    'Request_Unban', 'Request_ToggleAll', '0' ]
	choice = ShellMenu(title, choices, actions)
	if choice == '1()':
		return 1
	elif choice != '0()':
		return [ choice, eval(choice) ]
	else:
		return 0

def Request_Create():
	ClearScreen()
	title     = 'Create a new account request:'
	header    = 'Answer the following prompts, all are required.'
	questions = { 'username': 'Enter your requested username:', 'realname': 'Enter your real name (first and last):',
                      'email': 'Enter your email address:', 'comments': 'Comments:\n' }
	answers   = QuestionList(title, header, questions)
	answers['password'] = PasswordPrompt()
	return answers

def Request_Check():
	ClearScreen()
	title     = 'Edit an existing account request:'
	header    = 'Enter the username and password you suggested to continue.'
	questions = { 'username': 'Enter your requested username:' }
	answers   = QuestionList(title, header, questions)
	answers['password'] = PasswordPrompt()
	return answers

def Request_Delete():
	ClearScreen()
	title     = 'Delete an existing account request:'
	header    = 'Enter the username and password you suggested to continue.'
	questions = { 'username': 'Enter your requested username:' }
	answers   = QuestionList(title, header, questions)
	answers['password'] = PasswordPrompt()
	return answers

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
		PrintMessage(message)

def Request_Approve():
	title  = 'Approve an account request:'
	header = 'This will create an account based on a given request.'
	questions = { 'ref': 'Enter the name of the identifying resource (id, username, etc.): ',
		      'id':  'Enter the value of the resource: ' }
	answers = QuestionList(title, header, questions)
	return answers

def Request_Deny():
	title  = 'Deny an account request:'
	header = 'This will remove a request from the system.'
	questions = { 'ref': 'Enter the name of the identifying resource (id, username, etc.): ',
		      'id':  'Enter the value of the resource: ' }
	answers = QuestionList(title, header, questions)
	retval = { answers['ref']: answers['id'] }
	return retval

def Request_Revoke():
	title  = 'Delete an existing user created by the account shell:'
	header = 'This will delete an existing user that was created by the account shell, including the deletion of the user\'s home directory.'
	questions = { 'username': 'Enter the username of the user: ' }
	answers = QuestionList(title, header, questions)
	return answers

def Request_Ban():
	title  = 'Ban a username from ever being created:'
	header = 'This will automatically halt all requests using this specific username.'
	questions = { 'username': 'Enter the username to be banned: ' }
	answers = QuestionList(title, header, questions)
	return answers

def Request_Unban():
	title  = 'Remove a ban from a specific username:'
	header = 'This will stop requests with a banned username from being halted.'
	questions = { 'username': 'Enter the username to be unbanned: ' }
	answers = QuestionList(title, header, questions)
	return answers

def Request_ToggleAll():
	title  = 'Turn the account shell either on or off:'
	header = 'This will cease all requests from being created, checked, denied, approved, denied, etc. All activity will be instantly denied. However, the account shell can still be accessed.'
	questions = { 'sure': 'Are you sure? (enter YES in uppercase): ' }
	answers = QuestionList(title, header, questions)
	return answers

def ShellMenu(title, choices, actions):
	title = title.ljust(50)
	title = title.title()
	print ( '-' * 50 )
	print title
	print ( '-' * 50 )
	x = 0
	for choice in choices:
		x = x+1
		print '[' + repr(x) + '] ' + choice.ljust(46)
	print ( '=' * 50 )
	invalid = 1
	while invalid:
		choice = input('Enter your menu choice [1-' + repr(x) + ']: ')
		if choice <= 0 or choice > x:
			print "Invalid choice. Please choose again.\n"
		else:
			invalid = 0
	return "%s()" % actions[choice - 1]

def QuestionList(title, header, questions):
	title = title.ljust(50)
	title = title.title()
	print ( '-' * 50 )
	print title
	print ( '-' * 50 )
	print header + "\n\n"
	answers = {}
	for key in questions.keys():
		temp = ''
		while temp == '':
			temp = raw_input(questions[key] + ' ')
		answers[key] = temp
	return answers

def PasswordPrompt():
	return getpass.getpass()

def PrintMessage(message):
	print message
	raw_input()

def ClearScreen(numlines = 100):
	import os
	if os.name == 'posix':
		os.system('clear')
	elif os.name in ("nt", "dos", "ce"):
		os.system('cls')
	else:
		print '\n' * numlines