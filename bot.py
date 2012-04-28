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

citylist = readfile('cities.txt')
keylist = readfile('keywords.txt')
timefile = readfile('time.txt')
condlist = readfile('conditions.txt')


while True :
  input = raw_input('Me > ')
  if input == 'exit' or input == 'quit' or input == 'bye':
    break
  
  for i in keylist:
    if i in input:
      key = i
      break
  
  for i in timelist:
    if i[0] in input:
      if i[0] is not 'today' or i[0] is not 'tomorrow':
	time = i[1]
	break
      else:
	time = i[0]
	break
  
  prevlocation = location 
  #We store previous location to avoid re-fetching data if the location hasn't been changed
  
  # Below, we check if any token in the input matches a city name, and if so, set location to that city
  newlocation = False
  
  for i in citylist:
    if i in input:
      location = i
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
  
  
  
  
  else:
    print 'What\'s the location?'