'''

File: bot.py
Does all the major work of the chat bot.
Reads user input, searches for weather-related keywords. If found, gets weather conditions and prepares a response
If not found, calls predefined_responses.py to generate predefined responses
'''


# imports
import re
import predefined_responses
import weather
import sentence
import readfile
import temperature
import log
import spellcheck
import string
from string import lower

def chat():
  # keyword conditions
  condnext = False
  condweather = False
  condtime = False
  condlocation = False
  condtemp = False
  condkey = False
  condresponse = False
  foundinfo = False
  condtrain = False
  condcountry = False
  condspellcheck = True

  # global variables
  conversation = []
  location = ''
  prevlocation = location 
  time = 'today'
  key = ''
  keytemplate = []
  fulltime = ''
  numdays = ''
  logstr = ''
  printstr = ''
  responsedict = {} 	# Dictionary to hold all inputs without predefined responses. This dictionary will be written into predefined_responses.txt before exiting the program.


  # read data files
  citylist = readfile.readfile('cities.txt')
  keylist = readfile.readfile('keywords.txt')
  timelist = readfile.readfile('time.txt')
  condlist = readfile.readfile('conditions.txt')
  numlist = readfile.readfile('numbers.txt')
  countrylist = readfile.readfile('countries.txt')
  exitlist = ['exit', 'quit', 'bye', 'ok']

  # Greeting message
  printstr =  'Hello! You can ask me questions about the weather in any major city in the world. What would you like to know?'
  print printstr
  logstr += '\n\n' + printstr

  # Start main loop
  while True :
    foundinfo = False
    condtrain = False
    condcountry = False
    # read input from user
    input = raw_input('\nMe > ')
    logstr += '\nMe > ' + input + '\nBot > '
    if input in exitlist:
      if input == 'ok':
	exitans = raw_input("Do you want to quit? (y/n)")
	if exitans in ('y','Y','Yes','YES','yes'):
	  break
	else:
	  continue
      break
    
    if input == 'disable spellcheck':
      condspellcheck = False
      continue
    
    if input == 'enable spellcheck':
      condspellcheck = True
      continue
    
    condcorrected = False
    if condspellcheck:
      corrected_input = ''
      for i in input.split():
	str = spellcheck.correct(i)
	if str != i:
	  condcorrected = True
	corrected_input += str + ' '
      if condcorrected:
	print 'did you mean: \"' + corrected_input + '\"?'
	input = corrected_input
    
    currentstring = input.split()
    conversation.append(currentstring)
    
    # Start searching input for each of the keywords
    
    if input == 'train':
      condtrain = True
      printstr =  'Entering training mode. Enter input and response seperated by a "|": input|response. Type "exit" to quit training mode'
      print printstr
      logstr += '\n' + printstr + '\n'
      
      while True:
	traininput = raw_input('>')
	if traininput == 'exit':
	  break
	if traininput.find('|') < 0:
	  printstr =  'Format error: use input|response'
	  print printstr
	  logstr += '\n' + printstr + '\n'
	  continue
	traininput = traininput.split('|')
	responsedict[traininput[0]] = traininput[1]
    
    if condtrain:
      continue
    


    for i in countrylist:
      for j in currentstring:
	if lower(i[0]) == lower(j):
	  printstr = 'Which city in ' + i[0] + '?'
	  condcountry = True
	  foundinfo = True
	  break
      
    if condcountry:
      print printstr
      logstr += printstr
      continue
    

    if 'next' in input:
      foundinfo = True
      condnext = True
      condtime = False
      numdays = currentstring[currentstring.index('next') + 1]
      for i in numlist:
	if numdays == i[0]:
	  numdays = i[1]
	  break
      if re.match('[0-9]*$',numdays):
	numdays = int(numdays)
      else:
	numdays = ''
    
    if 'weather' in input:
      foundinfo = True
      condweather = True
      condkey = False
      condtemp = False
      key = ''
      keytemplate = []

    # get key from input
    for i in keylist:
      if i[0] in input:
	if 'sunday' in lower(input) and i[0] == 'sun':
	  break
	else:
	  foundinfo = True
	  condkey = True
	  condweather = False
	  condtemp = False
	  key = i[0]
	  keytemplate = i
	  break

    # get time from input
      for i in timelist:
	if lower(i[0]) in input:
	  foundinfo = True
	  condtime = True
	  numdays = ''
	  if lower(i[0]) != 'today' and lower(i[0]) != 'tomorrow':
	    time = i[1]
	    fulltime = i[0]
	    break
	  else:
	    time = i[0]
	    fulltime = time
	    break
    if fulltime == '':
      fulltime = time

    if numdays != '':
      condtime = True
      if numdays > 4:
	printstr =  'Forecast is available only for the next 4 days.'
	print printstr
	logstr += '\n' + printstr + '\n'
      else:
	time = ''
	fulltime = ''
	count = numdays
    
    # get location from input
    for i in citylist:
      if lower(i[0]) in input:
	foundinfo = True
	condlocation = True
	location = i[0]
	break
    
    # find if a new location has been mentioned. if not, don't fetch data again
    if location != prevlocation:
      newlocation = True
      condlocation = True
      prevlocation = location
    else:
      newlocation = False
    
    if location is '':
      if prevlocation is '':
	condlocation = False
      else:
	location = prevlocation
	newlocation = False
    
    location = location.replace(' ','-') #Google requires a '-' in 2-word city names
    result = False
    
    # get temperature from input
    if 'temperature' in input:
      foundinfo = True
      condtemp = True

    # User gave no infomation about weather. Switching to general predefined response based chat
    if not foundinfo:
      response = predefined_responses.respond(input, responsedict)
      if response == '':
	printstr =  "I don't know what that means. If I asked you the same question, what would you reply?"
	print printstr
	logstr += printstr
	responseinput = raw_input('Me > ')
	logstr += '\nMe > ' + responseinput
	if not responseinput in ('exit', 'quit'):
	  responsedict[input] = responseinput
	  print 'response learnt'
      else:
	printstr =  response
	print printstr
	logstr += printstr
      continue
    
    if condlocation:
      if newlocation:	#If location hasn't changed, don't fetch data again. It's already available
	printstr =  'Fetching weather information from Google...'
	print printstr
	logstr += printstr
	# Call Google weather to get current weather conditions
	google_result = weather.get_weather(location)
	if google_result == {}:
	  print 'Could not get data from google.'
	  continue
      
      
  # We have a valid location. Get further information

  # User has asked about temperature. Return temperature information and continue
      if condtemp:
	printstr =  temperature.temperature(google_result, time)
	print printstr
	logstr += printstr
	continue
      
  # User has asked about a specific weather condition. Print information. There are 2 possibilities:
  #    1. Find the condition in the next n days
  #    2. Find the condition in a specified day

      if condkey:

  # 1. User has asked about a specific condition in the 'next x days'. Return appropriate response
	printstr = ''
	timecounter = 0

	day_of_week = ''
	condition = ''
	if numdays != '':
	  for i in google_result['forecasts']:
	    count -= 1
	    if count < 0:
	      break
	    if key in lower(i['condition']):
	      result = True
	      day_of_week = i['day_of_week']
	      condition = i['condition']
	      break

	  for i in timelist:
	    if i[0] != 'today' and i[0] != 'tomorrow':
	      if i[1] == day_of_week:
		fulltime = i[0]
		break
	  if result:
	    printstr = keytemplate[3] + keytemplate[0] + ' on ' + fulltime
	  else:
	    printstr = keytemplate[4] + keytemplate[0] + ' in the next ' + str(numdays) + ' days.'

	  print printstr
	  logstr += printstr
	  continue

  # 2. User has asked about a particular condition on a particular day. Return appropriate response
	if time != 'today' and time != 'tomorrow':
	  for i in google_result['forecasts']:
	    if i['day_of_week'] == time:
	      if key in lower(i['condition']):
		printstr = keytemplate[3] + keytemplate[0] + ' on'
	      else:
		printstr = keytemplate[4] + keytemplate[0] + ' on'
	elif time == 'today':
	  fulltime = time
	  if key in lower(google_result['current_conditions']['condition']):
	    printstr = keytemplate[1] + keytemplate[0]
	  else:
	    printstr = keytemplate[2] + keytemplate[0]
	elif time == 'tomorrow':
	  fulltime = time
	  if key in lower(google_result['forecasts'][1]['condition']):
	    printstr = keytemplate[3] + keytemplate[0]
	  else:
	    printstr = keytemplate[4] + keytemplate[0]

	printstr =  printstr + ' ' + fulltime
	print printstr
	logstr += printstr
	continue

  # User is asking about today's weather. Print details
      elif time == '' or time == 'today' :
	printstr = sentence.sentence(google_result['current_conditions']['condition'], time)
	printstr += ' ' + fulltime + '. ' + google_result['current_conditions']['humidity'] + ' '
	if google_result['current_conditions'].has_key('wind_condition'):
	  printstr += google_result['current_conditions']['wind_condition']
	print printstr
	logstr += printstr
	continue

  # User is asking about weather of a particular day. Print details
      elif time == 'tomorrow':
	printstr = sentence.sentence(google_result['forecasts'][1]['condition'], time)
	printstr += ' ' + fulltime
	print printstr
	logstr += printstr
      else:
	found = False
	for i in range(4):
	  if google_result['forecasts'][i]['day_of_week'] == time:
	    printstr = sentence.sentence(google_result['forecasts'][i]['condition'], time)
	    printstr +=   " on" + ' ' +  fulltime
	    print printstr
	    logstr += printstr
	    found = True
	if not found:
	  printstr =  "Forecast for " + time + " is not available currently."
	  print printstr
	  logstr += printstr
	continue
      
    else:
      printstr =  'What\'s the location?'
      print printstr
      logstr += printstr
  # End of outermost while loop.

  # Print message before exiting program
  dictcount = 0
  for i in responsedict:
    dictcount += 1
  if dictcount > 0:
    printstr =  'Writing new entries to database...'
    print printstr
    logstr += printstr
  datafile = file('predefined_responses.txt', 'a')
  for i in responsedict.keys():
    trimmedi = re.sub('[^a-zA-Z0-9 ]+','', i)
    string = trimmedi + '|' + responsedict[i] + '\n'
    datafile.write(string)
  log.log(logstr)
  print 'Ending the program...'
  print 'Bye!'
  
# End of function chat()