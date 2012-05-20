'''

File: predefined_responses.py
Reads input-response pairs from predefined_responses.txt, takes input from the user and gives an appropriate response
'''
import re
def respond(inputstring, currentresponsedict):
  
  # create a dictionary of input:responses
  responsedict = {}
  
  for i in currentresponsedict.keys():
    responsedict[i] = currentresponsedict[i]
  # read responses from file
  data = file('predefined_responses.txt', 'r')
  while True:
    line = data.readline()
    if line == '':
      break
    line = line.rstrip('\n')
    line = line.split('|')
    responsedict[line[0]] = line[1]
  # responsedict now contains all the knows input/response pairs
  
  response = ''
  inputkey = ''
  inputtokens = re.sub('[^a-zA-Z0-9 ]+','', inputstring)
  inputtokens = inputtokens.split()
  
  # Search for response for the given input
  count = 0
  maxcount = 0
  maxkey = ''
  maxtokens = []
  for i in responsedict.keys():
    tokens = i.split()
    fullmatch = True
    count = 0
    for j in inputtokens:
      for k in tokens:
	if k == j:
	  count += 1
	  if count > maxcount:
	    maxcount = count
	    maxkey = i
	    maxtokens = tokens
	  continue
	else:
	  fullmatch = False
    
    
    #for j in tokens:
      #if j in inputstring:
	#count += 1
	#if count > maxcount:
	  #maxcount = count
	  #maxkey = i
	  #maxtokens = tokens
	#continue
      #else:
	#fullmatch = False
    
    if fullmatch:
      inputkey = i
      break
    
  if not fullmatch:
    if maxcount > 0 and maxcount > len(inputtokens)/2:
      inputkey = maxkey
      
  if inputkey != '':
    response = responsedict[inputkey]
  else:
    response = ''
  
  return response