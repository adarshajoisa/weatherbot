import re
import weather
import sentence
import readfile
import temperature
import string
from string import lower

def bot():
  conversation = []
  location = ''
  time = 'today'
  key = ''
  keytemplate = []
  fulltime = ''
  numdays = ''

  citylist = readfile.readfile('cities.txt')
  keylist = readfile.readfile('keywords.txt')
  timelist = readfile.readfile('time.txt')
  condlist = readfile.readfile('conditions.txt')
  numlist = readfile.readfile('numbers.txt')

  while True :
    input = raw_input('Me > ')
    if input == 'exit' or input == 'quit' or input == 'bye':
      break
    
    currentstring = input.split()
    conversation.append(currentstring)
    
    if 'next' in currentstring:
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
      key = ''
      keytemplate = []
    # get key from input
    for i in keylist:
      if i[0] in input:
	key = i[0]
	keytemplate = i
	break
    
    # get time from input

    for i in timelist:
      if lower(i[0]) in input:
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
      if numdays > 4:
	print 'Forecast is available only for the next 4 days.'
      else:
	time = ''
	fulltime = ''
	count = numdays
    prevlocation = location 
    #We store previous location to avoid re-fetching data if the location hasn't been changed
    
    
    # Below, we check if any token in the input matches a city name, and if so, set location to that city
    newlocation = False
    
    # get location from input
    for i in citylist:
      if lower(i[0]) in input:
	location = i[0]
	break
    
    # find if a new location has been mentioned. if not, don't fetch data again
    if location is not prevlocation:
      newlocation = True
    
    if location is '':
      if prevlocation is '':
	print 'City not found'
      else:
	location = prevlocation
	newlocation = False
    
    location = location.replace(' ','-') #Google requires a '-' in 2-word city names
    result = False
    
    
    if location is not '':
      if newlocation:	#If location hasn't changed, don't fetch data again. It's already available
	print 'Fetching weather information from Google...'
	# Call Google weather to get current weather conditions
	google_result = weather.get_weather(location)
      
      if 'temperature' in currentstring:
	print temperature.temperature(google_result, time)
	continue
      
      printed = False
      
      
      if key is not '':
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
	  printed = True
	      
	if not printed:
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

      elif time == '' or time == 'today' :
	  printstring = sentence.sentence(google_result['current_conditions']['condition'], time)
	  print printstring, fulltime,  google_result['current_conditions']['humidity'], google_result['current_conditions']['wind_condition']
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

    
    else:
      print 'What\'s the location?'