# imports
import re
import predefined_responses
import weather
import sentence
import readfile
import temperature
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

  # global variables
  conversation = []
  location = ''
  prevlocation = location 
  time = 'today'
  key = ''
  keytemplate = []
  fulltime = ''
  numdays = ''


  # read data files
  citylist = readfile.readfile('cities.txt')
  keylist = readfile.readfile('keywords.txt')
  timelist = readfile.readfile('time.txt')
  condlist = readfile.readfile('conditions.txt')
  numlist = readfile.readfile('numbers.txt')
  exitlist = ['exit', 'quit', 'bye', 'ok']

  # Greeting message
  print 'Hello! You can ask me questions about the weather in any major city in the world. What would you like to know?'

  # Start main loop
  while True :
    
    # read input from user
    input = raw_input('Me > ')
    if input in exitlist:
      break
      
    currentstring = input.split()
    conversation.append(currentstring)
    
    # Start searching input for each of the keywords

    if 'next' in currentstring:
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
    
    if 'weather' in currentstring:
      condweather = True
      condkey = False
      condtemp = False
      key = ''
      keytemplate = []

    # get key from input
    for i in keylist:
      if i[0] in input:
	condkey = True
	condweather = False
	condtemp = False
	key = i[0]
	keytemplate = i
	break

    # get time from input
      for i in timelist:
	if lower(i[0]) in input:
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
	print 'Forecast is available only for the next 4 days.'
      else:
	time = ''
	fulltime = ''
	count = numdays
    
    # get location from input
    for i in citylist:
      if lower(i[0]) in input:
	condlocation = True
	location = i[0]
	break
    
    # find if a new location has been mentioned. if not, don't fetch data again
    if location != prevlocation:
      newlocation = True
      prevlocation = location
    else:
      newlocation = False
    
    if location is '':
      if prevlocation is '':
	print 'City not found'
      else:
	location = prevlocation
	newlocation = False
    
    location = location.replace(' ','-') #Google requires a '-' in 2-word city names
    result = False
    
    # get temperature from input
    if 'temperature' in currentstring:
      condtemp = True
    
    if not( condtemp or condlocation or condkey or condlist or condnext or condtime or condweather ):
      predefined_responses.respond()
    
    if location is not '':
      if newlocation:	#If location hasn't changed, don't fetch data again. It's already available
	print 'Fetching weather information from Google...'
	# Call Google weather to get current weather conditions
	google_result = weather.get_weather(location)
      
      
  # We have a valid location. Get further information

  # User has asked about temperature. Return temperature information and continue
      if condtemp:
	print temperature.temperature(google_result, time)
	continue
      
  # User has asked about a specific weather condition. Print information. There are 2 possibilities:
  #    1. Find the condition in the next n days
  #    2. Find the condition in a specified day

      if condkey:
	
  # 1. User has asked about a specific condition in the 'next x days'. Return appropriate response
	printstring = ''
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
	    printstring = keytemplate[3] + keytemplate[0] + ' on ' + fulltime
	  else:
	    printstring = keytemplate[4] + keytemplate[0] + ' in the next ' + str(numdays) + ' days.'
	  
	  print printstring
	  continue
	
  # 2. User has asked about a particular condition on a particular day. Return appropriate response
	if time != 'today' and time != 'tomorrow':
	  for i in google_result['forecasts']:
	    if i['day_of_week'] == time:
	      if key in lower(i['condition']):
		printstring = keytemplate[3] + keytemplate[0] + ' on'
	      else:
		printstring = keytemplate[4] + keytemplate[0] + ' on'
	elif time == 'today':
	  fulltime = time
	  if key in lower(google_result['current_conditions']['condition']):
	    printstring = keytemplate[1] + keytemplate[0]
	  else:
	    printstring = keytemplate[2] + keytemplate[0]
	elif time == 'tomorrow':
	  fulltime = time
	  if key in lower(google_result['forecasts'][1]['condition']):
	    printstring = keytemplate[3] + keytemplate[0]
	  else:
	    printstring = keytemplate[4] + keytemplate[0]
		
	print printstring, fulltime
	printed = True
	continue
	
  # User is asking about today's weather. Print details
      elif time == '' or time == 'today' :
	printstring = sentence.sentence(google_result['current_conditions']['condition'], time)
	print printstring, fulltime,  google_result['current_conditions']['humidity'], google_result['current_conditions']['wind_condition']
	continue
	
  # User is asking about weather of a particular day. Print details
      else :
	if time == 'tomorrow':
	  printstring = sentence.sentence(google_result['forecasts'][1]['condition'], time)
	  print printstring, fulltime
	else:
	  found = False
	  for i in range(4):
	    if google_result['forecasts'][i]['day_of_week'] == time:
	      printstring = sentence.sentence(google_result['forecasts'][i]['condition'], time)
	      print printstring, "on", fulltime
	      found = True
	  if not found:
	    print "Forecast for " + time + " is not available currently."
	continue
      
    else:
      print 'What\'s the location?'
  # End of outermost while loop.

  # Print message before exiting program
  print 'ending the program...'
  print 'bye!'
  
# End of function chat()