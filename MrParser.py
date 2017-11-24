import sys, yaml, re
import Parser as p
from twisted.internet import reactor, protocol
from twisted.python import log
from twisted.words.protocols import irc
from twisted.application import internet, service

with open('config.yml') as f:
    config = yaml.load(f.read())
HOST, PORT, USER, PASS, CHANNELS = config['host'], config['port'], config['username'], config['password'], config['channels']


class ParserProtocol(irc.IRCClient):
    nickname = "MrParser"
    password = PASS
    username = USER
    versionName = 'Baguette'
    versionNum = 'v1.0'
    realname = 'MrParser'

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)

    def privmsg(self, user, channel, message):
        nick, _, host = user.partition('!')
        self.sendErrors(self,channel,message,nick)
        print(nick, ">", message)

    @staticmethod
    def sendErrors(self,channel,message, nick):
        if channel not in CHANNELS:
            return
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        for x in urls:
            parsed = p.parse(x)
            if parsed is not None:
                for stuff in parsed:
                    self._send_notice(stuff + " Found: " + parsed.get(stuff))

    def _send_message(self, msg, target, nick=None):
        if nick:
            msg = '%s, %s' % (nick, msg)
        self.msg(target, msg)

    def _send_notice(self, msg):
        self.notice("LaxWasHere", msg)

    def _show_error(self, failure):
        return failure.getErrorMessage()


class ParserFactory(protocol.ReconnectingClientFactory):
    protocol = ParserProtocol
    channels = CHANNELS

if __name__ == '__main__':
    reactor.connectTCP(HOST, PORT, ParserFactory())
    log.startLogging(sys.stdout)
    reactor.run()

elif __name__ == '__builtin__':
    application = service.Application('MrParser')
    ircService = internet.TCPClient(HOST, PORT, ParserFactory())
    ircService.setServiceParent(application)