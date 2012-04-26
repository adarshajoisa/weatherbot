import re
import nltk
import weather
import sentence
import string
from string import lower

conversation = []
location = ''

# Read names of cities from file
cityfile = file("cities.txt","r")
citylist = []
for i in range(720) :
  city = cityfile.readline()
  city = city.rstrip('\n')
  city = lower(city)
  citylist.append(city)
cityfile.close()
# citylist now contains a list of 719 major cities worldwide

time = 'today'

timefile = file("time.txt", "r")
timelist = []
for i in range(10):
  day = timefile.readline()
  day = day.rstrip('\n')
  day = lower(day)
  timelist.append(day)
timefile.close()
#timelist contains the times like today, tomorrow, monday, etc.
while True :
  input = raw_input('Me > ')
  if input == 'exit' or input == 'quit' or input == 'bye':
    break
  
  # Tokenize the input string
  splitinput = input.split()
  input = input.lower()
  
  # create a list to remove punctuations from 'input'
  trimmed_input = []
  print 'Bot > '
  
  #convert each token to lowercase and remove punctuations
  for i in splitinput :
    i = re.sub('[^a-zA-Z0-9]+','', i)
    i = lower(i)
    trimmed_input.append(i)

  #tagged_input = nltk.pos_tag(trimmed_input)
  conversation.append(trimmed_input)
  
  # We check if a time has been mentioned by the user
  for i in trimmed_input:
    if i in timelist:
      time = i
      break
  
  # Weather report uses short weekday names. substitute below
  newtime = ''
  if time == 'monday':
    newtime = 'Mon'
  elif time == 'tuesday' :
    newtime = 'Tue'
  elif time == 'wednesday' :
    newtime = 'Wed'
  elif time == 'thursday' :
    newtime = 'Thu'
  elif time == 'friday' :
    newtime = 'Fri'
  elif time == 'saturday' :
    newtime = 'Sat'
  elif time == 'sunday' :
    newtime = 'Sun'
  
  prevlocation = location #We store previous location to avoid re-fetching data if the location hasn't been changed
  
  # Below, we check if any token in the input matches a city name, and if so, set location to that city
  newlocation = False
  for i in citylist:
    if input.find(i) >= 0:
      location = i
      break
  
  
  if location != prevlocation:
    newlocation = True
  
  if location == '':
    if prevlocation == '':
      print 'City not found'
    else:
      location = prevlocation
      newlocation = False
  
  location = location.replace(' ','-') #Google requires a '-' in 2-word city names
  
  
  if location != '':
    if newlocation:	#If location hasn't changed, don't fetch data again. It's already available
      print 'Fetching weather information from Google...'
      # Call Google weather to get current weather conditions
      google_result = weather.get_weather(location)
      
    # Print today's weather report. Replace this with code to deduce the user request
    if time == '' or time == 'today' :
      printstring = sentence.sentence(google_result['current_conditions']['condition'], time)
      print printstring, time
    else :
      if time == 'tomorrow':
	printstring = sentence.sentence(google_result['forecasts'][1]['condition'], time)
	print printstring, time
      else:
	found = False
	for i in range(4):
	  if google_result['forecasts'][i]['day_of_week'] == newtime:
	    printstring = sentence.sentence(google_result['forecasts'][i]['condition'], time)
	    print printstring, "on", time
	    found = True
	if not found:
	  print "Forecast for " + time + " is not available currently."
    
  else:
    print "What's the location?"