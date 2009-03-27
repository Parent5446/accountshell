import Common

def MainMenu(controller):
	title   = 'Main Menu'
	choices = [ 'Create a new account request', 'Check an existing account request',
                    'Delete an existing request', 'Administrative Panel', 'Exit/Stop' ]
	actions = [ 'Request_Create', 'Request_Check',
                    'Request_Delete', '1', '0' ]
	choice = Common.ShellMenu(title, choices, actions)
	if choice == '1()':
		return 1
	elif choice != '0()':
		return [ choice, eval(choice) ]
	else:
		return 0

def Request_Create():
	title     = 'Create a new account request:'
	header    = 'Answer the following prompts, all are required.'
	questions = [ 'Enter your requested username:', 'Enter your real name (first and last):',
                      'Enter your email address:', 'Comments:\n' ]
	answers   = Common.QuestionList(title, header, questions)
	answers.append(Common.PasswordPrompt())
	return answers

def Request_Check():
	title     = 'Edit an existing account request:'
	header    = 'Enter the username and password you suggested to continue.'
	questions = [ 'Enter your requested username:' ]
	answers   = Common.QuestionList(title, header, questions)
	answers.append(Common.PasswordPrompt())
	return answers

def Request_Delete():
	title     = 'Delete an existing account request:'
	header    = 'Enter the username and password you suggested to continue.'
	questions = [ 'Enter your requested username:' ]
	answers   = Common.QuestionList(title, header, questions)
	answers.append(Common.PasswordPrompt())
	return answers
