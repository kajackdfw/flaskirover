# Example of Raspi UPS Hat
#
# You should install wiringPi first.
# sudo apt-get update
# sudo apt-get upgrade
# git clone git://git.drogon.net/wiringPi
# cd wiringPi
# git pull origin
# cd wiringPi
# ./build

# We only provide 2 interfave to get battery information; 
#
#Interface 1:
#Function: get current battery voltage
#Return value: battery voltage;
#float getv();

#Interface 2:
#Function:    get battery capacity
#Return value: 0~100
#float getsoc(); 
#

import sys
# import Raspi UPS Hat library
import raspiupshat

# init Raspi UPS Hat
raspiupshat.init();

# Get info
print "Voltage:%5.2fV" % raspiupshat.getv();
print "Battery:%5i%%" % raspiupshat.getsoc();

# draw batery
n = int(round(raspiupshat.getsoc() / 10));
print "----------- "
sys.stdout.write('|')
for i in range(0,n):
	sys.stdout.write('#')
for i in range(0,10-n):
	sys.stdout.write(' ')
sys.stdout.write('|+\n')
print "----------- "

if raspiupshat.getsoc() == 100:
	print "Battery FULL"
if raspiupshat.getsoc() < 20:
	print "Battery LOW"
while 1:
	if raspiupshat.getsoc() < 5:
		print "System will shutdown now,bye!"
		os.system("sudo shutdown")
