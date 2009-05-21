import getpass

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
