def ShellMenu(title, choices, actions):
	title = title.ljust(50)
	title = title.title()
	print ( '-' * 50 ) + "\n"
	print title + "\n"
	print ( '-' * 50 ) + "\n"
	x = 0
	for choice in choices:
		x = x+1
		print '[' + repr(x) + '] ' + choice.ljust(46) + "\n"
	print ( '=' * 50 ) + "\n"
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
	print ( '-' * 50 ) + "\n"
	print title + "\n"
	print ( '-' * 50 ) + "\n"
	print header + "\n\n"
	answers = []
	for question in questions:
		invalid = 1
		while invalid:
			temp = repr(input(question + ' '))
			if temp == '':
				print "Fields cannot be left blank.\n"
				x=raw_input()
			else:
				invalid = 0
		answers.append(temp)
	return answers
