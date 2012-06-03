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

from os import environ, mkdir, path
from time import time

####
# User editable options
#
# These first two options are obtained from your Twilio dashboard
# - https://www.twilio.com/user/account
ACCT_SID = ""
ACCT_TOKEN = ""
#
# Phone number section.  Please only the numbers, no other characters
# The number you are notifying (your phone number)
TO_NUMBER = ""
#
# The Twilio number you are sending the SMS from.  They can be from the following
# two pages:
# - https://www.twilio.com/user/account/phone-numbers/incoming
# - https://www.twilio.com/user/account/phone-numbers/verified
FROM_NUMBER = ""
#
# the delay in minutes before a the next SMS will be sent
DELAY = 15
#
# Do not edit past this point
####

TN_DIR = environ['HOME'] + "/.twilio-notifier/"
TN_FILE = TN_DIR + "twilio-notifier.json"
SID_LEN = 34

def getTimestamp():
	from json import loads
	f = open(TN_FILE)
	with f:
		return loads(f.read())

def setTimestamp(ts=0):
	'Set the UNIX timestamp for flood protection.'
	from json import dumps
	try:
		f = open(TN_FILE, 'w+')
	except IOError:
		mkdir(TN_DIR)
		f = open(TN_FILE, 'w+')
	f.write(dumps({'timestamp': ts}, indent=4) + "\n")
	f.close()

def validateArgs(args):
	if not len(args.acct_sid) == SID_LEN:
		raise ValueError('The APP_SID is not the proper length (' + str(SID_LEN) + ')')
	if not args.reset and args.message == None or len(str(args.message).strip()) < 1:
		raise ValueError('You did not provide a valid message')
	if len(args.to_number) < 10 or len(args.to_number) < 10:
		raise ValueError("Either the recipient or sending number are not valid (needs to be at least 10 digits)")
	return args

def getArgs():
	from optparse import OptionParser
	usage = "\t%prog [options]"
	o = OptionParser(usage=usage)
	o.add_option("-a", "--acct-sid", dest="acct_sid", default=ACCT_SID, help="The account SID for your Twilio account.")
	o.add_option("-m", "--message", dest="message", help="The body of the SMS you are sending")
	o.add_option("-r", "--recipient", dest="to_number", default=TO_NUMBER, help="The recipient of the SMS message")
	o.add_option("-s", "--sender", dest="from_number", default=FROM_NUMBER, help="The phone number to have the SMS message appear from")
	o.add_option("-t", "--acct-token", dest="acct_token", default=ACCT_TOKEN, help="The account token for your Twilio account")
	o.add_option("--force", action="store_true", default=False, dest="force", help="force SMS even if delay period hasn't elapsed")
	o.add_option("--reset", action="store_true", default=False, dest="reset", help="Reset delay timestamp so next time script is called the message is sent")
	(opts, args) = o.parse_args()
	return validateArgs(opts)

def sendMsg(sid, token, to_number, from_number, message, timestamp, force=False):
	if force or int(time()) - timestamp > DELAY * 60:
		message = message.strip()
		if len(message) > 160:
			message = message[0:157] + '...'
		from twilio.rest import TwilioRestClient
		client = TwilioRestClient(sid, token)
		message = client.sms.messages.create(to=to_number, from_=from_number, body=message)
		return True

	return False

if __name__ == "__main__":
	args = getArgs()
	if args.reset:
		setTimestamp()
		quit()
	if not path.exists(TN_FILE):
		setTimestamp()

	ts = getTimestamp()['timestamp']

	if sendMsg(args.acct_sid, args.acct_token, args.to_number, args.from_number, args.message, ts, args.force):
		setTimestamp(int(time()))
