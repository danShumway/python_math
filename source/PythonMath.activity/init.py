import sys
import os
import shutil

print """CISC374 Launcher Setup.

This script checks sanity and configures parameters for deploying your game to
the OLPC XO and performing translations. You should run it if you decide to
rename your game as more details are completed.
"""

split = os.path.basename(os.path.abspath(".")).split('.')
if len(split) != 2 or split[1] != 'activity':
    print "Invalid directory name. You should rename this directory to\nYourGameName.activity and run this script again."
    sys.exit()
    
name = split[0]

r = raw_input("Game Name [%s]: " % (name))
if len(r) != 0 and r != name:
    print "You should consider renaming the directory to match your game name.\nProceeding anyways."
    name = r

service_name = 'org.laptop.community.udel.cisc374.%s' % (name.lower())
r = raw_input("Service Name (must be globally unique) [%s]: " % (service_name))

if len(r) > 0:
    service_name = r

version = '1.0'
r = raw_input("Activity Version [1.0]: ")
if len(r) > 0:
    version = r

f = open('skel/activity.info', 'r')
try:
    g = open('activity/activity.info', 'w')
except IOError:
    # Create the directory and file if they don't exist
    os.mkdir('activity');
    g = open('activity/activity.info', 'w+')
g.write(f.read() % {'name' : name, 'version' : version, 'service_name' : service_name})
g.close()
f.close()
print 'Created activity/activity.info.'

if not os.path.isfile("activity/activity.svg"):
    print 'No icon found. A placeholder has been copied to activity/activity.svg, you\nshould replace this with your own icon.'
    f = 'skel/activity.svg'
    shutil.copy(f, 'activity/activity.svg')
    
print 'All done.'