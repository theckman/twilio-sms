#!/usr/bin/env python
#
# Copyright (c) 2012 Tim Heckman <timothy.heckman@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from os import environ, mkdir, path, path
from time import time

CONF_DIR = path.join(path.dirname(__file__), 'conf/')
CONF_FILE = 'twilio-sms.json'
EMPTY_OPTS = { 'acct_sid': '', 'acct_token': '', 'to_number': '', 'from_number': '', 'message': '', 'force': 0, 'delay': 60, 'timestamp': 0 }
SID_LEN = 34

def check_message(message):
	if len(message) > 160:
		message = message[0:157] + '...'
	return message

def writeConfig(config=CONF_FILE, acct_sid='', acct_token='', to_number='', from_number='', message='', force=0, delay=60, timestamp=0):
	args = locals()
	del(args['config'])
	args['message'] = check_message(args['message'])
	from json import dumps
	f = open(CONF_DIR+config, 'w')
	f.write(dumps(args, indent=4, sort_keys=True) + "\n")
	f.close()

def getConfig(config=CONF_FILE):
	from json import loads
	try:
		c = open(CONF_DIR+config, 'r')
	except IOError:
		writeConfig(config)

	c = open(CONF_DIR+config, 'r')
	with c:
		return loads(c.read())

def updateTimestamp(config, opts, timestamp=0):
	writeConfig(config, opts['acct_sid'], opts['acct_token'], opts['to_number'], opts['from_number'], opts['message'], opts['force'], opts['delay'], timestamp)

def validateArgs(args, strict):
	if not args.reset and strict:
		if not len(args.acct_sid) == SID_LEN:
			raise ValueError('The APP_SID is not the proper length (' + str(SID_LEN) + ')')
		if args.message == None or len(str(args.message).strip()) < 1:
			raise ValueError('You did not provide a valid message')
		if len(args.to_number) < 10 or len(args.to_number) < 10:
			raise ValueError("Either the recipient or sending number are not valid (needs to be at least 10 digits)")
	return args

def getArgs(opts, strict=True):
	from optparse import OptionParser
	usage = "\t%prog [options]"
	o = OptionParser(usage=usage)
	o.add_option("-a", "--acct-sid", dest="acct_sid", default=opts['acct_sid'], help="The account SID for your Twilio account.")
	o.add_option("-c", "--config", dest="config", default=CONF_FILE, help="configuration file to use")
	o.add_option("-d", "--delay", dest="delay", default=opts['delay'], help="delay to use between texts, soft-override compared to '--reset'")
	o.add_option("-m", "--message", dest="message", default=opts['message'], help="The body of the SMS you are sending")
	o.add_option("-r", "--recipient", dest="to_number", default=opts['to_number'], help="The recipient of the SMS message")
	o.add_option("-s", "--sender", dest="from_number", default=opts['from_number'], help="The phone number to have the SMS message appear from")
	o.add_option("-t", "--acct-token", dest="acct_token", default=opts['acct_token'], help="The account token for your Twilio account")
	o.add_option("--force", action="store_true", default=opts['force'], dest="force", help="force SMS even if delay period hasn't elapsed")
	o.add_option("--reset", action="store_true", default=False, dest="reset", help="Reset delay timestamp so next time script is called the message is sent")
	(opt, args) = o.parse_args()
	return validateArgs(opt, strict)

def sendMsg(sid, token, to_number, from_number, message, force=False, delay=60, timestamp=0):
	if force or int(time()) - timestamp > delay * 60:
		message = check_message(message.strip())
		from twilio.rest import TwilioRestClient
		client = TwilioRestClient(sid, token)
		sms = client.sms.messages.create(to=to_number, from_=from_number, body=message)
		return True

	return False

if __name__ == "__main__":
	args = getArgs(EMPTY_OPTS, strict=False) # This is but a clever hack to get config file to use from getArgs...
	opts = getConfig(args.config)
	args = getArgs(opts)

	if args.reset:
		updateTimestamp(args.config, opts)
		quit()

	if sendMsg(args.acct_sid, args.acct_token, args.to_number, args.from_number, args.message, args.force, args.delay, opts['timestamp']):
		updateTimestamp(args.config, opts, int(time()))
