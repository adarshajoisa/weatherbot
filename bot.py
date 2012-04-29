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

citylist = readfile.readfile('cities.txt')
keylist = readfile.readfile('keywords.txt')
timelist = readfile.readfile('time.txt')
condlist = readfile.readfile('conditions.txt')

while True :
  input = raw_input('Me > ')
  if input == 'exit' or input == 'quit' or input == 'bye':
    break
  
  for i in keylist:
    if i[0] in input:
      key = i
      break
  
  fulltime = ''
  for i in timelist:
    if lower(i[0]) in input:
      if lower(i[0]) is not 'today' or lower(i[0]) is not 'tomorrow':
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
  
  for i in citylist:
    if lower(i[0]) in input:
      location = i[0]
      break
  
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