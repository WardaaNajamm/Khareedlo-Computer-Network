from twisted.cred.checkers import AllowAnonymousAccess, InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.portal import Portal
from twisted.internet import reactor
from twisted.protocols.ftp import FTPFactory, FTPRealm

def ftpAdmin():
    checker = InMemoryUsernamePasswordDatabaseDontUse()
    checker.addUser("ShopAdmin", "admin")

    # portal=Portal(FTPRealm("./public","./myusers"), [AllowAnonymousAccess(), checker]) 
    portal=Portal(FTPRealm("./Admin","./Users"), [checker])

    factory=FTPFactory(portal)
    reactor.listenTCP(21, factory)
    reactor.run()
    
def addUsers(username,password):
    checker = InMemoryUsernamePasswordDatabaseDontUse()
    u=username
    p=password
    checker.addUser(u, p)