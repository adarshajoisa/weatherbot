def readfile(filename)
  infile = file(filename, "r")
  datalist = []
  while True:
    data = infile.readline()
    if data is '':
      break
    data = data.rstrip('\n')
    data = lower(data)
    data = data.split('/')
    datalist.append(data)
  infile.close()
  return datalist