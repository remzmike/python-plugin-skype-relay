# https://mindcollapse-com-blog-source.googlecode.com/svn/small_projects/SkypeBot/__init__.py
# skyp4com api gives me what i want
# ChangeUserStatus(cus.TUserStatus
# CurrentUserStatus (allows get/set)
# http://dev.skype.com/accessories/skype4com-examples-delphi-chatmessages-pas
'''
Enumerator: 
cusUnknown  indicates the user status is unknown. 
cusOffline  indicates the user is offline. 
cusOnline  indicates the user is online. 
cusAway  indicates the user is away. 
cusNotAvailable  indicates the user is not available. 
cusDoNotDisturb  indicates the user is in do not disturb mode. 
cusInvisible  indicates the user is invisible to others. 
cusLoggedOut  indicates the user is logged out. 
cusSkypeMe  indicates the user is in SkypeMe mode. 
'''
import os, sys, time
import Skype4Py
libpath = os.path.join(os.getcwd(), '..\lib')
sys.path.append(libpath)
from kmessage import send_message # we relay to a custom message system

def main():
    s = Skype4Py.Skype()

    print 'attaching...'
    s.Attach(5, True)
    print 'attached'
    
    relayed = []    
    def doRelay(Message, missed=False):
      if missed:
          postfix = ' (missed)'
      else:
          postfix = ''
      if Message.Id in relayed:
          pass
      else:
          relayed.append(Message.Id)
          for lognum in ['rival','ganymede']:
              send_message(str(Message.Body) + postfix, str(Message.FromDisplayName), lognum=lognum)
   
    # todo: change doRelay to take message object, handle duplicates there
    # a message can actually be received AND missed, really retarded, i saw it once
    def MessageStatus(Message, Status):
        print 'messagestatus', str(Status)
        if Status == Skype4Py.cmsReceived:
            print Message.FromHandle, Message.Body
            doRelay(Message)

    def SmsMessageStatus(Message, Status):
        print 'sms message status', str(Status)

    def MessageHistory(Username):
        print 'message history', str(Username)

    def CallStatus(Call, Status):
        print 'call status', str(Status)

    def Error(Command, Number, Description):
        print 'error', str(Description)

    def AttachmentStatus(Sender, Status):
        print 'attachmentstatus', str(status)
        if Status == Skype4Py.apiAttachAvailable:
            print 'reattaching...'
            s.Attach(5, True);            
    
    s.OnMessageStatus = MessageStatus
    s.OnAttachmentStatus = AttachmentStatus
    s.OnSmsMessageStatus = SmsMessageStatus
    s.OnCallStatus = CallStatus
    s.OnMessageHistory = MessageHistory

    while True:
        time.sleep(0.1)        
        # wow, this fixes problems!
        messages = s.MissedMessages
        for i in range(messages.Count):
            message = messages.Item(i)          
            if not message.Id in relayed: # duplicate of doRelay logic, not really needed now, but stops print spam
                print 'missed messages', message.Id, message.FromDisplayName, message.Body
                doRelay(message, True)

if __name__=='__main__':
    main()