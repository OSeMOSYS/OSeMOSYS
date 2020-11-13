import os, sys, time

#########################################################################################
#########################################################################################

#if len(sys.argv) != 3:
#	print '''Usage: {0}
#	<input>
#	<output>\n\n\n'''.format(sys.argv[0])
#	sys.exit()

finput, foutput = sys.argv[1:]

# Section 1: Reading into memory, and possibly time-inefficient
#OUT = open(foutput,'w')
#with open(finput) as IN:
#	lines = []
#	t1 = time.time()
#	for line in IN:
#		if "<variable name=" in line:
#			lst = line.strip().split()
#			lines.append(lst)
#sortedList = sorted(lines)
#old = ''
#for each in sortedList:
	# Assign the values after '=' in variable name= to the variable variableContents
	# This involves replacing '"', and ')', and adding a ',' instead of '(', and then splitting at ','
#	variableContents = each[1].replace('(',',').replace(")",'').replace('name=','').replace('"','').split(',')
	# The contents of variableContents are then joined and saved as the variable 'variable'. This involves starting of with the 0th element and joining elements 1 to -1 (2nd last) between parentheses.
#	variable = variableContents[0]+'('+','.join(variableContents[1:-1])+')'
	# 'old' carries the name of the variable from the previous line. This enables printing each row in the input file into a column in the output file.
#	if variable == old:
#		OUT.write('\t{0}'.format(float(each[-2].replace('"','').split('=')[1])))
#	else:
#		OUT.write('\n{0}\t{1}'.format(variable, float(each[-2].replace('"','').split('=')[1])))
#		print each
#		old = variable
#t2 = time.time()
#print 'This process took ', (t2-t1)/60.0 , 'mins'

# Section 2: Attempt to make it time-efficient
def delete_key(d, k):
	r = dict(d)
	del r[k]
	return r

OUT = open(foutput,'w')
with open(finput) as IN:
	recordedVariables = []
	lines = []
	old = ''
	remember = {}
	for line in IN:
		if "<variable name=" in line:
			# Split at spaces
			lst = line.strip().split()
			# Assign the values after '=' in variable name= to the variable variableContents
			# This involves replacing '"', and ')', and adding a ',' instead of '(', and then splitting at ','
			variableContents = lst[1].replace('(',',').replace(")",'').replace('name=','').replace('"','').split(',')
			# The contents of variableContents are then joined and saved as the variable 'variable'. This involves starting of with the 0th element and joining elements 1 to -1 (2nd last) between parentheses.
			variable = variableContents[0]+'\t'+'\t'.join(variableContents[1:-1])
			if variable not in recordedVariables:
				if variable == old:
					lines.append(lst)
				else:
					if len(lines) == 21:
						sortedList = sorted(lines)
						OUT.write('{0}'.format(old))
						for each in sortedList:
							OUT.write('\t{0}'.format(float(each[-2].replace('"','').split('=')[1])))
						OUT.write('\n')
						#t2 = time.time()
						#print old, ' took ', (t2-t1)/60.0 , 'mins'
						lines = []
						lines.append(lst)
						recordedVariables.append(old)
						old = variable
					elif len(lines) == 0:
						t1 = time.time()
						t0 = t1
						lines.append(lst)
						old = variable
						if variable in remember.keys():
							for each in remember[variable]:
								lines.append(each)
							remember = delete_key(remember, variable)
					else:
						if variable not in remember.keys():
							remember[variable] = []
							remember[variable].append(lst)
						else:
							remember[variable].append(lst)

#print (len(remember.keys()))

for variable in remember.keys():
	values = remember[variable]
	sortedList = sorted(values)
	OUT.write('{0}'.format(variable))
	for each in sortedList:
		OUT.write('\t{0}'.format(float(each[-2].replace('"','').split('=')[1])))
	OUT.write('\n')
	#t2 = time.time()
	#print old, ' took ', (t2-t1)/60.0 , 'mins'
t3 = time.time()
print ("Process took ", (t3-t0)/60.0, ' mins')
