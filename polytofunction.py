def polytofunction(poly):
	if len(poly)>0: tempoly = poly.split(" ")
	poly = ""
	for tp in tempoly:
		if len(tp)>0: poly += tp

	left, right = poly.split("=")
	(ypoly, xpoly) = (left, right) if left.find('y') > -1 else (right, left)
#	print(ypoly)
#	print(xpoly)

	count = 0
	while ypoly !='y' and count!=10:
		ytemp = ypoly.split(' ')
		for yt in ytemp:
			if len(yt) > 0:
				ypoly = yt

		if ypoly.find('+') > -1:
			yelement = ypoly.split('+')
			for ye in yelement:
				if ye.find('y')>-1:
					ypoly = ye
				else:
					xpoly = '('+xpoly+'-('+ ye+')'+')'
		if ypoly.find('-') > -1:
			yelement = ypoly.split('-')
			for ye in yelement:
				if ye.find('y')>-1:
					ypoly = ye
				else:
					xpoly = '(-'+xpoly+'+('+ ye+'))'

		if ypoly.find('*') > -1:
			if ypoly.find('*') < ypoly.find('y'):
				xpoly += '/('+ ypoly[:ypoly.find('*')] +')'
				ypoly = ypoly[ypoly.find('*')+1:]

			if ypoly.find('*') > ypoly.find('y'):
				xpoly += '/('+ ypoly[ypoly.find('*')+1:]+')'
				ypoly = ypoly[:ypoly.find('*')]

		if ypoly.find('^') > -1 and ypoly.find('^') > ypoly.find('y'):
			if int(ypoly[ypoly.find('^')+1:]) % 2 == 1:
				xpoly += '^(1/'+ypoly[ypoly.find('^')+1:]+')'
				ypoly = ypoly[:ypoly.find('^')]
			else:
				xpoly += '^(1/'+ypoly[ypoly.find('^')+1:]+')m'
				ypoly = ypoly[:ypoly.find('^')]

		if ypoly[-1]==')' and ypoly[0]=='(':
			ypoly = ypoly[1:-1]
		
		count += 1
#		print(ypoly)
#		print(xpoly)
#	print(xpoly)
	return xpoly
