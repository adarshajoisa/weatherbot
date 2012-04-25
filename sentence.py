from string import lower
def sentence(condition, time):
  retstring = ''
  #print condition
  confile = file("conditions1.txt","r")
  tempconlist = []
  while True:
    con = confile.readline()
    if con == '':
      break
    con = con.rstrip('\n')
    tempconlist.append(con)
  confile.close()
  conlist = []
  for i in tempconlist:
    i = i.split('/')
    conlist.append(i)
  #print conlist
  for i in conlist:
    if condition in i:
      if time == 'today':
	retstring = i[1] + ' ' +  lower(i[0])
      else:
	retstring = i[2] + ' ' +  lower(i[0])
  if retstring == '':
    retstring = 'The weather is : ' + condition
  return retstring