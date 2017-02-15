def getMatch(arr1,arr2):
	count = 0
	matchList = []
	for element in arr2:
		if(element in arr1):
			count+=1
			matchList.append(element)
	return {'count':count,'matchList':','.join(matchList)}