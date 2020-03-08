__module_name__ = 'sudo'
__module_version__ = '1.0'
__module_description__ = 'executes command as op'
__author__ = 'ericathesnark'
__license__ = 'MIT/X11'

import weechat
weechat.register(__module_name__, __author__, __module_version__, __license__, __module_description__, "", "")

def printtobuffer(message):
	weechat.prnt(weechat.current_buffer(), message)

def nea():
	printtobuffer("-!-\tNot enough arguments")

def sudo(data, buffer, args):
	arguments = filter(None, args.split(" "))
	curbuff = weechat.current_buffer()
	cmd = " ".join(arguments)
	chan = weechat.buffer_get_string(curbuff, "short_name")

	if len(arguments) < 1:
		nea()
		return weechat.WEECHAT_RC_ERROR


	weechat.command(curbuff, '/quote PRIVMSG ChanServ :op %s' % chan)
	weechat.command(curbuff, '/wait 300ms /%s' % cmd)
	weechat.command(curbuff, '/wait 500ms /quote PRIVMSG ChanServ :deop %s' % chan)
	return weechat.WEECHAT_RC_OK

weechat.hook_command("sudo", "sudo executes a command as op", "<command>", "<command> the command to execute", "", "sudo", "")
