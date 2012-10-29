from subprocess import Popen, PIPE

proc = Popen(['python', 'cx.py', 'build'],stdout=PIPE)

while True:
  line = proc.stdout.readline()
  if line != '':
    print line.rstrip()
  else:
    break
print "FINISHED"