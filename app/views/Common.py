def ShellMenu(title, choices, actions):
	title = title.zfill(50)
	title = title.title()
	print ( '-' * 50 ) + "\n"
	print title + "\n"
	print ( '-' * 50 ) + "\n"
	x = 0
	for choice in choices:
		x = x+1
		print '[' + x + '] ' + choice.zfill(46) + "\n"
	print ( '=' * 50 ) + "\n"
	invalid = true
	while invalid:
		choice = input('Enter your menu choice [1-' + x + ']: ')
		if choice <=0 or choice > x:
			print "Invalid choice. Please choose again.\n"
		else:
			invalid = false
	return "%s()" % actions[choice]

def QuestionList(title, header, questions):
	title = title.zfill(50)
	title = title.title()
	print ( '-' * 50 ) + "\n"
	print title + "\n"
	print ( '-' * 50 ) + "\n"
	print header + "\n\n"
	answers = []
	for question in questions:
		invalid = true
		while invalid:
			temp = str(input(question + ' '))
			if temp == '':
				print "Fields cannot be left blank.\n"
				x=raw_input()
			else:
				invalid = false
		answers.append(temp)
	return answers
