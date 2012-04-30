import re
import weather
import sentence
import readfile
import string
from string import lower

conversation = []
location = ''
time = 'today'
key = ''
keytemplate = ''
fulltime = ''

citylist = readfile.readfile('cities.txt')
keylist = readfile.readfile('keywords.txt')
timelist = readfile.readfile('time.txt')
condlist = readfile.readfile('conditions.txt')

while True :
  input = raw_input('Me > ')
  if input == 'exit' or input == 'quit' or input == 'bye':
    break
  
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
      if lower(i[0]) != 'today' and lower(i[0]) != 'tomorrow':
	time = i[1]
	fulltime = i[0]
	break
      else:
	time = i[0]
	fulltime = i[0]
	break
  
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
  
  if location is not '':
    if newlocation:	#If location hasn't changed, don't fetch data again. It's already available
      print 'Fetching weather information from Google...'
      # Call Google weather to get current weather conditions
      google_result = weather.get_weather(location)
    
    if key is not '':
      printstring = ''
      timecounter = 0
      
      
      keyresult = False
      if time != 'today' and time != 'tomorrow':
	for i in google_result['forecasts']:
	  if i['day_of_week'] == time:
	    if key in lower(i['condition']):
	      printstring = keytemplate[3] + keytemplate[0] + ' on'
	    else:
	      printstring = keytemplate[4] + keytemplate[0] + ' on'
      elif time == 'today':
	if key in lower(google_result['current_conditions']['condition']):
	  printstring = keytemplate[1] + keytemplate[0]
	else:
	  printstring = keytemplate[2] + keytemplate[0]
      elif time == 'tomorrow':
	if key in lower(google_result['forecasts'][1]['condition']):
	  printstring = keytemplate[3] + keytemplate[0]
	else:
	  printstring = keytemplate[4] + keytemplate[0]
	    
      #if key in input:
	#for i in google_result['forecasts']:
	  #timecounter += 1
	  #if key in i['condition']:
	    #keyresult = True
	    #print 'YO ho ho and a bottle of rum!'
	    #break
      #if keyresult:
	#if timecounter is 1:
	  #printstring = keytemplate[1] + keytemplate[0]
	#elif timecounter is 2:
	  #printstring = keytemplate[3] + keytemplate[0]
	#else:
	  #printstring = keytemplate[3] + keytemplate[0]
	  #print timecounter
      #else:
	#if timecounter is 1:
	  #printstring = keytemplate[2] + keytemplate[0]
	#elif timecounter is 2:
	  #printstring = keytemplate[4] + keytemplate[0]
	#else:
	  #printstring = keytemplate[4] + keytemplate[0]
	  #print timecounter
      print printstring, fulltime
    
    else:
  
      if time == '' or time == 'today' :
	  printstring = sentence.sentence(google_result['current_conditions']['condition'], time)
	  print printstring, fulltime
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