Twilio Notifier
===============
This is a [Twilio](https://www.twilio.com/) Notifier script written in Python.  This script was built to simply send SMS messages to the number of your choosing using Twilio.  While not capable now, this will eventually be able to be used as a module so you can bolt it on to your scripts.

This is still a work in progress.  All attempts will be made to not alter any of the current features to ensure backwards compatibility.

Requirements
------------
This script was written for Python 2.x and request the twilio module to be available.  Nothing too crazy. :)

Configuration
-------------

The configuration files are stored in the `conf` directory.  Each The configuration is currently stored within the script itself.  The configuration is entirely optional, as all options can be passed on the command-line.  Additionally, if you specify an option on the command-line it will override the value stored in the file.

By default, the script loads the `conf/twilio-notifier.json` configuration file.  You can specify a different configuration file on the command-line (see below).  The benefit of being able to select configs via the command line, is you can predefine numbers and messages in separate configuration files and load each one as needed.

**Note:** Passing your account SID or token on the command-line may be a security risk, as that will live in your shell history

Here are the contents of the example configuration file, `conf/example.json`:

	{
	    "acct_sid": "",
	    "acct_token": "",
	    "delay": 60,
	    "from_number": "",
	    "message": "",
	    "timestamp": 0,
	    "to_number": ""
	}


* `acct_sid` - the account SID from your [Twilio Dashboard](https://www.twilio.com/user/account)
* `acct_token` - the account token from your [Twilio Dashboard](https://www.twilio.com/user/account)
* `delay` - the minimum amount of time before this script will send the next SMS.  If the script is called within the delay time, the message is simply discarded without being sent and the script exits.
* `from_number` - the [Twilio number](https://www.twilio.com/user/account/phone-numbers/incoming) that the SMS messages will originate from
* `message` - the message to send via SMS to the recipient
* `to_number` - the number to send the SMS messages to

There is a final option in the file, `timestamp`, that's used by the script to determine if the `delay` period has passed.  You shouldn't edit this value by hand.  If you need to force an SMS through use the `--force` option below.  Alternatively, you could override the delay period via command-line option as well.


Script Usage
------------

Here is the output of the help information for the script:

	Usage: 	twilio-notifier.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -a ACCT_SID, --acct-sid=ACCT_SID
	                        The account SID for your Twilio account.
	  -c CONFIG, --config=CONFIG
	                        configuration file to use
	  -d DELAY, --delay=DELAY
	                        delay to use between texts, soft-override compared to
	                        '--reset'
	  -m MESSAGE, --message=MESSAGE
	                        The body of the SMS you are sending
	  -r TO_NUMBER, --recipient=TO_NUMBER
	                        The recipient of the SMS message
	  -s FROM_NUMBER, --sender=FROM_NUMBER
	                        The phone number to have the SMS message appear from
	  -t ACCT_TOKEN, --acct-token=ACCT_TOKEN
	                        The account token for your Twilio account
	  --force               force SMS even if delay period hasn't elapsed
	  --reset               Reset delay timestamp so next time script is called
	                        the message is sent

Assuming you have the SID and token configured within the configuration file itself, you could run this command to send a message to yourself from one of your Twilio numbers.

`twilio-notifier.py -s 5055553842 -r 5055553243 -m "This is a message from Twilio"`

As mentioned above, you can specify which config to load via the command-line.  Assuming your configuration file has all values filled out, including message, you could run this command to send a message based on a configuration file:

`twilio-notifier.py -c notify-me.json`

License
-------
Copyright (c) 2012 Tim Heckman <<timothy.heckman@gmail.com>>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
