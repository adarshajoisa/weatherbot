def log(string):
  logfile = file('logfile.log','a')
  logfile.write(string)
  logfile.close()
  