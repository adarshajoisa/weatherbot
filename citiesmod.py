import re
readfile = file("cities-mod.txt","r")
writefile = file("cities-final.txt", "w")
writelist = []
for i in range(720):
  readstr = readfile.readline()
  writestr = re.sub('[^a-zA-Z]+','', readstr)
  writelist.append(writestr)
writestring = "\n"
final = writestring.join(writelist)
writefile.write(final)