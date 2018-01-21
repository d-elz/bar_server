import os
import time
import socket
import sys
import urllib2
import sqlite3 as lite
from twisted.internet import defer, reactor , ssl
from twisted.internet.protocol import ServerFactory, ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver, NetstringReceiver
from twisted.protocols import basic

from bar.network.protocols.BarServerToBar0 import BarServerToBar0Factory

"""
Bar Server : is the broadcsast server of the application . The main task of it is to
get a message from a user and broadcast it to everyone is log in to it.
"""

#Saves all the objects for the Protocol
clients = []

class BARServerProtocol(NetstringReceiver):

    def connectionMade(self):
        clients.append(self)#add the cleint object to the list , when we want to broadscast a meesage we call one by one the object
        self.factory.numOfConnection +=1 # KEep track of the connection
        peer = self.transport.getPeer()
        host = self.transport.getHost()

        print "~~ Connection established from " + str(peer)

        print "~~ LogIn Users : " , self.factory.numOfConnection
        #self.sendString("=== BAR Server ===")

    def stringReceived(self, data):
        peer = self.transport.getPeer()
        #Broadcast the message
        if data[:9] == "BROADCAST":
            print "~~ BROADCASTING message from " + str(peer)
            self.broadcast(data)
            #self.transport.loseConnection()
        #Log in to Bar Server
        elif data[:5] == "LogIn":
            print "~~ Log In from " + str(peer)
            self.logout_info =  data.split("||||")[1]
        elif data[:6] == "LogOut":
            print "~~ Log Out from " + str(peer)
            print data
        #Quit
        elif data[:4] == "QUIT":
            print "Quit: " , data
            self.transport.loseConnection()
        else:
            self.sendString("I can break rules too.")

    def broadcast(self, data):
        if len(data) <= 11:
            self.sendString("Ok, but where's the message to broadcast?")
        else:
            message = data[13:]
            print "STARTING BROADCASTING MESSAGES "
            print clients
            for client in clients:
                selfobject = str(self.transport.getPeer().host) +":"+ str(self.transport.getPeer().port)
                clientobject = str(client.transport.getPeer().host) +":"+ str(client.transport.getPeer().port)
                #if selfobject != clientobject:
                print "--------------------------------------"
                print "To : " , client.transport.getPeer().host
                #print "DATA : " , message
                print "--------------------------------------"
                client.sendString(message) #wirh client object sending the data to each client

    def connectionLost(self, reason):
        clients.remove(self)
        peer = self.transport.getPeer()
        print "~~ Client Disconnected with " + str(peer)

        self.factory.numOfConnection -=1
        print "~~ LogIn Users : " , self.factory.numOfConnection
        try:
            print "Inform Bar-Coordinator that client with IP:port combination " + self.logout_info + "logged out"
            bar0_conn("LogOut||||"+self.logout_info,"195.251.225.87",443)
        except AttributeError:
            pass
        #self.sendString("LogOut||||"+self.logout_info)

class BARServerFactory(ServerFactory):
    protocol = BARServerProtocol

    numOfConnection = 0

def bar_server(port,name):
    BAR0_SERVER = "195.251.225.87"
    BAR_SERVER = "195.251.225.88"
    BAR0_SERVER_PORT = 443

    data = "BarServer||||This is a Bar server from a M.||||" + BAR_SERVER +":"+ str(port) +"||||"+name
    bar0_conn(data,BAR0_SERVER,BAR0_SERVER_PORT)
    BARServer = BARServerFactory()
    listeningOn = reactor.listenTCP(port, BARServer)
    print 'Serving on %s.' % (listeningOn.getHost())
    reactor.run()

def bar0_conn(message,bar0,bar0_port):
    bar0_factory = BarServerToBar0Factory(message,"empty_defer")
    reactor.connectSSL(bar0,bar0_port,bar0_factory,ssl.ClientContextFactory())

if __name__ == '__main__':
    bar_server()
