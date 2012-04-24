import re
import nltk
import weather
import string
from string import lower

conversation = []
location = ''

# Read names of cities from file
cityfile = file("cities-final.txt","r")
citylist = []
for i in range(720) :
  city = cityfile.readline()
  city = city.rstrip('\n')
  city = lower(city)
  citylist.append(city)
cityfile.close()
# citylist now contains a list of 719 major cities worldwide

time = ''

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
  input = input.split()
  
  # create a list to remove punctuations from 'input'
  trimmed_input = []
  print 'Bot > '
  
  #convert each token to lowercase and remove punctuations
  for i in input :
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
  if time == 'monday':
    time = 'mon'
  elif time == 'tuesday' :
    time = 'tue'
  elif time == 'wednesday' :
    time = 'wed'
  elif time == 'thursday' :
    time = 'thu'
  elif time == 'friday' :
    time = 'fri'
  elif time == 'saturday' :
    time = 'sat'
  elif time == 'sunday' :
    time = 'sun'
    
  # Below, we check if any token in the input matches a city name, and if so, set location to that city
  for i in trimmed_input:
    if i in citylist:
      location = i
      break
  if location != '':
    # Call Google weather to get current weather conditions
    google_result = weather.get_weather(location)
  
  # Print today's weather report. Replace this with code to deduce the user request
    print "It is " + string.lower(google_result['current_conditions']['condition']) + " and " + google_result['current_conditions']['temp_c'] + "C now in " + location + ".\n\n"
    
    print "Weather on " + google_result['forecasts'][0]['day_of_week']
  
  else:
    print "What's the location?"