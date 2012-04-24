from string import lower
def sentence(condition, time):
  retstring = ''
  confile = file("conditions1.txt","r")
  tempconlist = []
  for i in range(20):
    con = confile.readline()
    con = con.rstrip('\n')
    #con = lower(con)
    tempconlist.append(con)
  confile.close()
  conlist = []
  for i in tempconlist:
    i = i.split('/')
    conlist.append(i)
  for i in conlist:
    if condition in i:
      if time == '' or time == 'today':
	retstring = i[1] + ' ' +  lower(i[0])
      else:
	retstring = i[2] + ' ' +  lower(i[0])
  return retstring