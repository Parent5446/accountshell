import Common

def MainMenu():
	title   = 'Main Menu'
	choices = [ 'Create a new account request', 'Check an existing account request',
                    'Delete an existing request', 'Administrative Panel', 'Exit/Stop' ]
	actions = [ 'Request_Create', 'Request_Edit',
                    'Request_Delete', '1', '0' ]
	inmenu = 1
	while inmenu:
		choice = Common.ShellMenu(title, choices, actions)
		if choice == '1()':
			return 1
		elif choice == '0()':
			inmenu = 0
		else:
			eval(choice)
	return 0
