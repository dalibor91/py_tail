import re
import os 
import sys
import time
import service
import tornado.web
import tornado.ioloop
import json

LOCK_FILE = "/var/lock/watcher.lock";

LOG_FILE = '/var/log/%s_.log' % time.strftime("%Y-%m-%d")

LOG_ENABLED = False

def log(msg, type="info"):
	if not LOG_ENABLED:
		return None
	with open(LOG_FILE, "a") as f:
		f.write("[%s] %s\n" % (str(type), str(msg)))

def isNum(s):
	if re.match("[^0-9]", str(s)):
		return False
	return True

def lockExists():
	if not os.path.isfile(LOCK_FILE):
		return None

	with open(LOCK_FILE, "r") as lf:
		return str(lf.read())
	return None

def createLock():
	if lockExists():
		return None;
	with open(LOCK_FILE, "w") as lf:
		lf.write(getPid())
		return True
	return False

def getPid():
	return str(os.getpid());

def removeLock():
	if lockExists():
		os.unlink(LOCK_FILE)
		return True
	return False


def argv(num, default=None):
	if len(sys.argv) > num:
		return sys.argv[num]
	return default


def run(port, conf=None):
	log("Trying to start program on port %s..." % str(port));
	if lockExists():
		print "Already started PID %s " % lockExists()
		log("Already runing");
		return None;

	if conf is None:
		conf = "conf.json"

	if not os.path.isfile(conf):
		print "Unable to find %s conf file" % str(conf)
		return None

	confdata = None
	with open(conf) as conffile:
		confdata = json.load(conffile)
	
	if (confdata is None) or len(confdata) == 0:
		print "Please insert configuration"
		return None


	createLock();
	print "Runing on port %s " % str(port)
	app = tornado.web.Application([
		(r'/', service.IndexHandle, { "data" : confdata }),
		(r'/socket', service.WebSocketHandle, { "data": confdata })
	])
	app.listen(int(port));

	tornado.ioloop.IOLoop.instance().start()

	return None;

def help(prog):
	print "Use %s start <port>  - to start " % prog
	print "Use %s stop          - to stop" % prog
	print "Use %s status        - to get status" % prog
	print "Use %s help          - for this message" % prog
	print "Use %s log           - to see log" % prog

def stop():
	log("Trying to stop program...")
	lock = lockExists();
	if lock:
		log("Trying to kill pid %s" % str(lock))
		removeLock()
		print "Trying to stop PID %s" % lock
		try :
			os.kill(int(lock), 9)
		except Exception as k:
			print "Unable to kill process, probably already dead";
		print "Done."
		log("Done")
	return None

def status():
	lock = lockExists()
	if lock:
		print "Runing under PID %s" % lock
	else: 
		print "Not running"
	return None

def readlog():
	with open(LOG_FILE, "r") as lf:
		for line in lf.readlines():
			print line.strip()

