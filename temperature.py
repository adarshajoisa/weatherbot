def temperature(result, day):
  retstring = ''
  forecast_day = ''
  if day == 'today':
    retstring = 'Temperature is between ' + result['forecasts'][0]['low'] + ' and ' + result['forecasts'][0]['high'] + ' today. It is ' + result['current_conditions']['temp_f'] + ' now. '
  elif day == 'tomorrow':
    retstring = 'Temperature may be between ' + result['forecasts'][1]['low'] + ' and ' + result['forecasts'][1]['high'] + ' tomorrow.'
  else:
    timefile = file('time.txt','r')
    while True:
      time = timefile.readline()
      if time == '':
	break
      time = time.rstrip('\n')
      time = time.split('/')
      if time[0] == day:
	forecast_day = time[1]
	break
    temp_low = ''
    temp_high = ''
    
    for i in result['forecasts']:
      if i['day_of_week'] == forecast_day:
	temp_low = i['low']
	temp_high = i['high']
	break
    if temp_low == '' or temp_high == '':
      retstring = 'Temperature information not available for ' + day
    else:
      retstring = 'Temperature may be between ' + temp_low + ' and ' + temp_high + ' on ' + day
  return retstring
    