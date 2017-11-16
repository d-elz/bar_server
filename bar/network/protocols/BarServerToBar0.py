from twisted.internet import ssl, reactor , defer
from twisted.internet.protocol import Factory, Protocol ,ClientFactory , ServerFactory


"""
Protocol for the communication with BAR Coordinator(BAR0).


"""

class BarServerToBar0Protocol(Protocol):

    def __init__(self , data ,deferred):
        self.data = data
        self.d = deferred


    def connectionMade(self):
        peer = self.transport.getPeer()
        host = self.transport.getHost()
        print "~~ Connected to Bar-Coordinator at " +str(peer)
        self.transport.write(self.data)
        #self.transport.loseConnection()

    def dataReceived(self, data):
        #Getting message from the Register Service of BAR0
        if data.split('||||')[0] == "BarServer":
            print data.split('||||')[1]
        elif data.split('||||')[0] == "LogOut":
            if data.split('||||')[1] != -1:
                print "User successfully logged out"
            elif data.split('||||')[1] == -1:
                print "User not successfully logged out"
            else:
                print "Something wrong with logged out!"
        else:
            print "Garbage: " + data
        #self.transport.loseConnection()

    ## is called when a connection could not be established
    def connectionFailed(self,  reason):
        peer = self.transport.getPeer()
        print "Connection failed to Bar-Coordinator " + str(peer)
        print "Reason was : ", reason
        reactor.stop()

    ## is called when a connection was made and then disconnected
    def connectionLost(self, reason):
        peer = self.transport.getPeer()
        print "~~ Disconnected from Bar-Coordinator at " +str(peer)
        self.transport.loseConnection()
        #reactor.stop()


class BarServerToBar0Factory(ClientFactory):

        #Not working for some reason
    def startedConnecting(self, connector):
        print '~~ Start connection to BAR Coordinator ~~'

    def __init__(self , data ,deferred):
        self.data = data
        self.d = deferred

    def buildProtocol(self , addr):
        #print "Bar Server To Bar0 Protocol connect"
        return BarServerToBar0Protocol(self.data , self.d)

        #Not working for some reason
    def clientConnectionFailed(self, connector, reason):
        #print "Connection failed."
        #ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
        pass

        #Not working for some reason
    def clientConnectionLost(self, connector, reason):
        #print "Connection lost."
        #ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
        pass
