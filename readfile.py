'''

File: readfile.py
reads data from a file and puts it into a list
'''

from string import lower
def readfile(filename):
  infile = file(filename, 'r')
  datalist = []
  while True:
    data = infile.readline()
    if data == '':	# data is '' doesn't work for some reason. using data == '' instead
      break
    data = data.rstrip('\n')
    data = data.split('/')
    datalist.append(data)
  infile.close()
  return datalist