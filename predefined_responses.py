'''

File: predefined_responses.py
Reads input-response pairs from predefined_responses.txt, takes input from the user and gives an appropriate response
'''
import re
import nltk
def respond(inputstring, currentresponsedict = {}):
  
  # create a dictionary of input:responses
  responsedict = {}
  responsenounlist = {}
  tagged_responsedict = {}
  
  # POS tag the input string and extract nouns
  tagged_input = nltk.pos_tag(nltk.word_tokenize(inputstring))
  input_nounlist = []
  for i in tagged_input:
    if i[1].startswith('NN'):
      input_nounlist.append(i[0])
  
  
  
  for i in currentresponsedict.keys():
    tagged_key = nltk.pos_tag(nltk.word_tokenize(i))
    nounkeylist = []
    for j in tagged_key:
      if j[1].startswith('NN'):
	nounkeylist.append(j[0])
	responsedict[i] = currentresponsedict[i]
	responsenounlist[i] = nounkeylist
    
    #responsedict[i] = currentresponsedict[i]
  # read responses from file
  data = file('predefined_responses.txt', 'r')
  while True:
    line = data.readline()
    if line == '':
      break
    line = line.rstrip('\n')
    line = line.split('|')
    
    tagged_key = nltk.pos_tag(nltk.word_tokenize(line[0]))
    nounkeylist = []
    for j in tagged_key:
      if j[1].startswith('NN'):
	nounkeylist.append(j[0])
	responsedict[line[0]] = line[1]
	responsenounlist[line[0]] = nounkeylist
    #responsedict[line[0]] = line[1]
  # responsedict now contains all the knows input/response pairs
  
  response = ''
  inputkey = ''
  # Search for response for given input
  count = 0
  maxcount = 0
  maxkey = []
  fullmatch = False
  for i in responsedict.keys():
    if input_nounlist == responsenounlist[i]:
      fullmatch = True
    else:
      for j in input_nounlist:
	for k in responsenounlist[i]:
	  if j == k:
	    count += 1
	    if count > maxcount:
	      maxcount = count
	      maxkey = i
	    continue
	  else:
	    fullmatch = False
    
    if fullmatch:
      inputkey = i
      break
    
    if not fullmatch:
      if maxcount > 0 and maxcount > len(input_nounlist)/2:
	inputkey = maxkey
	
  if inputkey != '':
    response = responsedict[inputkey]
  else:
    response = ''
      
  #return response
  
  if response == '':
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