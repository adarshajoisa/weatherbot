def respond(inputstring):
  
  # create a dictionary of input:responses
  responsedict = {}
  # read responses from file
  data = file('predefined_responses.txt', 'r')
  while True:
    line = data.readline()
    if line == '':
      break
    line = line.rstrip('\n')
    line = line.split('/')
    responsedict[line[0]] = line[1]
  # responsedict now contains all the knows input/response pairs
  
  response = ''
  inputkey = ''
  
  # Search for response for the given input
  for i in responsedict.keys():
    tokens = i.split()
    fullmatch = True
    for j in tokens:
      if j in inputstring:
	continue
      else:
	fullmatch = False
    if fullmatch:
      inputkey = i
      break
  
  if inputkey != '':
    response = responsedict[inputkey]
  else:
    response = ''
  
  return response