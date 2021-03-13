
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.event import EventDispatcher
import urllib3
import threading
import json
from kivy.clock import Clock
import sys
import time
from datetime import datetime, date, time, timedelta
import MFRC522
import signal

Config.set('kivy', 'log_level', 'debug')
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'show_cursor', '0')
Config.set('kivy', 'exit_on_escape', '1')
Config.write()
import RPi.GPIO as GPIO       ## Import GPIO library
GPIO.setmode(GPIO.BOARD)      ## Use board pin numbering
GPIO.setup(32, GPIO.OUT)      ## Setup GPIO Pin 32 to OUT
GPIO.setwarnings(False)
Window.clearcolor = (1, 1, 1, 1)
path = 'data/'
temp_en = StringProperty()
temp_en = True
#################################################################Desktop/project/final/
with open(path+'mdata.txt') as json_file:  
                data = json.load(json_file)
                details = data['machine_details']
                machine_no = int(details['machine_no'])
                temp_en = str(details['temp_en'])
                duration = int(details['duration'])
                PreWashTime = int(details['PreWashTime'])
                powercutTime = int(details['powercut'])
                default_option = str(details['default_option'])
#################################################################
WashTime = duration
countdown = WashTime
continuereading = True
coins = ''
UserName = 'Your Name'
card = False
mId= machine_no
uId = ''
ordersID = 0
ordercomplet = True
pressStart = True
cardId = 'S0000001'
options = default_option
availablebal = 0
counter = 0
screentobe= 'main0'
UserName = 'Your Name'
timenow = datetime.now()
checkScreen = True
save = True
puls = 1
##############################################
##############################################
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continuereading
    print "Ctrl+C captured, ending read."
    continuereading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
#################################################################################################
#################################################################################################
#################################################################################################



#################################################################################################
#################################################################################################
#################################################################################################
class MainScreen1(Screen):

    def __init__(self, **kwargs):
        super(MainScreen1, self).__init__(**kwargs)
        global temp_en
        self.temp_en = temp_en
        global checkScreen
        checkScreen = True
        print('MainScreen0')
        threading.Thread(target=self.Check_Screen).start()
        #self.loop()

        
    def on_enter(self, **kwargs):
        global checkScreen
        checkScreen = True
        #threading.Thread(target=self.Check_Screen).start()
        self.Check_Screen()
        return(self)

    def loop(self, **kwargs):
        global checkScreen
        global uId
        global UserName
        global powercut
        global cardId
        global card
        global countdown
        while checkScreen:
            ############################################################
            coins = ''
            UserName = ''
            card = False
            mId= 1
            uId = ''
            cardId = ''
            UserName = ''
            checkScreen = True
            powercut = 0
            ############################################################
            print "MainScreen0 update"
            checkScreen = True
            self.Check_Screen()
        return(self)
    
    def Check_Screen(self, **kwargs):
        global cardId
        global card
        global countdown
        global ordersID
        global checkScreen
        global pressStart
        print "check Screen value = "+ str(checkScreen)
        if checkScreen:
            #checkScreen = False
            print "MainScreen0 Check_Screen"
            with open(path+'data.txt') as json_file:  
                data = json.load(json_file)
                backup = data['backup']
                screentobe = str(backup['screentobe'])
                ordersID = int(backup['order'])
                countdown = int(backup['countdown'])
                timenow = datetime.strptime(backup['timenow'], '%Y-%m-%d %H:%M:%S.%f')
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                print "datetime.now() = "+str(datetime.now() )+" timenow = "+str(timenow)
                delta =  datetime.now() - timenow
                print('time diff = '+str(delta)+' ###################################')
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                
                if delta.days > 0 or delta.days < 0:
                    print "****************powercut****************"
                    powercut = 3
                else:
                    powercut = int(datetime.strptime(str(delta), '%H:%M:%S.%f').hour)
                   
                print('Screen to be = '+str(screentobe))
                print('last ordersID = '+str(ordersID))
                print('last countdown = '+str(countdown))
                print('last time = '+str(timenow))
                print('powercut = '+str(powercut)+' ***************')
                print backup
                
            if screentobe == "main4" and powercut < powercutTime and countdown >0:
                print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2'
                print 'You are an A**'
                print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
                self.parent.current = 'main4'
                pressStart =  False 
                print "Call Next screen"
            elif screentobe == "main0" and powercut >= powercutTime and countdown <= PreWashTime:
                print "Call main0 screen :::: No Refund"
            elif screentobe == "main0" and powercut >= powercutTime and countdown > PreWashTime:
                print "Call main0 screen :::: Need Refund"
                threading.Thread(target=self.orderUpdate).start()
            else:
                print "Stay on same screen"
                
        else:
            print "else on check Screen"
            
        return(self)

    def orderUpdate(self, **kwargs):
        global ordersID
        try:
            print('bnormal Order Update API')
            http = urllib3.PoolManager()
            r = http.request('PUT','http://api.centurylaundryindia.com/m1/orders',
                            headers={'Content-Type': 'application/json'},
                            body= json.dumps({ 'id': str(ordersID), 'status': 'C' }))
            order = json.loads(r.data.decode('utf-8'))
            print('Order Completed')
        except:
            print(' Abnormal Order Exception ')

        return(self)
    
    def on_leave(self, **kwargs):
        global checkScreen
        checkScreen = True
        return(self)
      
    pass

#################################################################################################
#################################################################################################
#################################################################################################
class MainScreen2(Screen):
    
    def __init__(self, **kwargs):
        print "MainScreen2 __init__"
        super(MainScreen2, self).__init__(**kwargs)
        cardId = 'saio'
        print('MainScreen2')
    
    def start(self):
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 0.005)

    def stop(self):
        print "MainScreen2 stop"
        Clock.unschedule(self.update)

    def update(self, *kwargs):
        print "MainScreen2 update"
        global cardId
        global card
        if not card:
            print "                         MainScreen1 Reading Card"
            try:
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                if status == MIFAREReader.MI_OK:
                    print "Card detected"
                    (status,uid) = MIFAREReader.MFRC522_Anticoll()
                    if status == MIFAREReader.MI_OK:
                        cardId = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
                        card = True
                        print("cardId = "+ str(cardId))
                        self.parent.current = 'main3'
                        self.stop()

            except:
                print "Card NOT detected"
                    
        else:
            print "Reader NOT Working"
 
                
        return(self)
    
    def updatelable(self, **kwargs):  
        return(self)

    def on_enter(self, **kwargs):
        threading.Thread(target=self.start).start()
        return(self)
    
    def on_leave(self, **kwargs):
        self.stop()
        return(self)
    
    
    pass
#################################################################################################
#################################################################################################
#################################################################################################
class MainScreen3(Screen):
    global ordersID


    def on_enter(self):
        print "MainScreen3 On_enter"
        global cardId
        global UserName
        global uId
        global ordersID
        global card
        self.ids.username.text = 'Please Wait'
        self.ids.balance.text = 'Connecting...'
        self.ids.coins.text = ''
        ####################################### user details #########################################
        try:
            if(card):
                print('API 0 Card')
                http = urllib3.PoolManager()
                r = http.request('GET', 'http://api.centurylaundryindia.com/m1/users/card/' + str(cardId),timeout=3.5)
                userdata = json.loads(r.data.decode('utf-8'))
                print('userdata = '+ str(userdata))
                userdetails = userdata['user']
                uId = userdetails['id']
                UserName = userdetails['name']
                success = userdata['success']
                print('success = '+ str(success))
                
                if(success):
                    self.ids.username.text = str('Welcome ' + str(UserName))
                    print('uId = '+ str(uId))
                else:
                    self.ids.username.text = 'Invalid Card'
                    self.ids.balance.text = 'Please Check your Card'
                    self.ids.coins.text = 'Contact Customer Care'
                    print('Invalid Card')
                    Clock.schedule_interval(self.goBack, 5)
            
            
            else:
                print('QR API')
                http = urllib3.PoolManager()
                r = http.request('GET', 'http://api.centurylaundryindia.com/m1/orders/' + str(mId),timeout=3.5)
                userdata = json.loads(r.data.decode('utf-8'))
                orders = userdata['orders']
                ordersID = orders['id']
                cid = orders['cid']
                http = urllib3.PoolManager()
                r = http.request('GET', 'http://api.centurylaundryindia.com/m1/users/'+str(cid),timeout=3.5)
                userdata = json.loads(r.data.decode('utf-8'))
                namedetails = userdata['user']
                uId = namedetails['id']
                UserName = namedetails['name']
                print('QR API')

                
        except:
            self.ids.username.text = 'No InterNet'
            print('UserName except 1 api')
            Clock.schedule_interval(self.goBack, 2)
            card = False

        #self.ids.username.text = str(UserName)
        ####################################### machinedetails & coins #########################################
        try:
            print('API 1 Machinedetails')
            http = urllib3.PoolManager()
            r = http.request('POST','http://api.centurylaundryindia.com/m1/machinedetails/price',
                            headers={'Content-Type': 'application/json'},
                            body= json.dumps({'mid': str(mId), 'options': options}))
            data = json.loads(r.data.decode('utf-8'))
            mdetails= data['machinedetails']
            global coins
            coins = str(mdetails['coins'])
            print('coins required = ' + coins)

            print('API 2 Wallet')
            r = http.request('GET', 'http://api.centurylaundryindia.com/m1/wallet/'+str(uId),timeout=3.5)
            wallet = json.loads(r.data.decode('utf-8'))
            
            wdetails = wallet['wallet']
            availablebal = wdetails['available']
            print('Required coins :' + str(mdetails['coins']) + 'wallet available ' + str(availablebal))
            
            if int(availablebal) == 0:
                self.ids.balance.text = 'Zero Balance'
                self.ids.coins.text = 'Press Back'
                print('No Balance')
                card = False
                Clock.schedule_interval(self.goBack, 2)
            else:
                self.ids.balance.text = str('Available Coins  : ' + str(availablebal))
                self.ids.coins.text = str('Coins to be Deducted : ' + str(mdetails['coins']))
                print('Balance Available')
                
        except:
            coins = 'No InterNet'
            print('CARD API :'+ coins + ' mId :' + str(mId) + ' options:' + options)
            print(coins)
            coins = '0'
            self.ids.coins.text = 'Please Check Connection'
            print('except 2 api')
            Clock.schedule_interval(self.goBack, 2)
            card = False
            
        return(self)

    def goBack(self, *kwargs):
        Clock.unschedule(self.goBack)
        self.parent.current = 'main0'
        return(self)
    
    def on_leave(self, **kwargs):
        global WashTime
        global ordersID
        '''
        data = {}  
        data['backup'] = {
            'countdown': str(WashTime),
            'screentobe': 'main4',
            'order': str(ordersID),
            'timenow': str(datetime.now()),
        }
        with open(path+'data.txt', 'w') as outfile:  
            json.dump(data, outfile)
        '''
        global pressStart
        pressStart = True
        print "MainScreen1 on_leave"
        #self.ids.username.text = 'Please Check'
        #self.ids.balance.text = 'Invalid Card'
        #self.ids.coins.text = 'Contact Customer Care'
        self.ids.username.text = 'Please Wait'
        self.ids.balance.text = 'Connecting...'
        self.ids.coins.text = ''
        return(self)
    
    def place_order(self, **kwargs):
        threading.Thread(target=self.order).start()
        global ordersID
        return(self)

    def order(self, **kwargs):
        global ordersID
        print "MainScreen1 place_order"
        print("Order Confirmed by User :" + str(coins))
        print('uId '+str(uId))
        
        if(card):
            print('uId '+str(uId))
            print('card')
            
            try:
                print('API 2 Order')
                http = urllib3.PoolManager()
                r = http.request('POST','http://api.centurylaundryindia.com/m1/orders',
                                headers={'Content-Type': 'application/json'},
                                body= json.dumps({ 'mid': str(mId), 'cid': str(uId), 'options': str(options), 'ordertotal': str(coins), 'status': 'P' }),timeout=3.5)
                order = json.loads(r.data.decode('utf-8'))
                print(str(order))
                ordersdetails= order['orders']
                ordersID = ordersdetails['id']
                print("Order no in if:" + str(ordersID)+ "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                success= order['success']
                print('Card Order created or updated :' + str(success))

            except:
                print('Card : Could not place order')
                
        else:
            try:
                http = urllib3.PoolManager()
                r = http.request('PUT','http://api.centurylaundryindia.com/m1/orders',
                                headers={'Content-Type': 'application/json'},
                                body= json.dumps({'id': str(ordersID), 'mid': str(mId), 'cid': str(uId), 'options': options, 'ordertotal': str(coins), 'status': 'P' }),timeout=3.5)
                order = json.loads(r.data.decode('utf-8'))
                print(str(order))
                success= order['success']
                ordersdetails= order['orders']
                ordersID = ordersdetails['id']
                print('QR'+str(ordersID) +' Order created or updated :' + str(success))

            except:
                print('QR Could not place order')

        print("Order no :" + str(ordersID)+ "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        return(self)

    
    pass

#################################################################################################
#################################################################################################
#################################################################################################
class MainScreen4(Screen):
    minutes = StringProperty()
    seconds = StringProperty()
    delta = None
    global WashTime  
    
    def __init__(self, **kwargs):
        super(MainScreen4, self).__init__(**kwargs)

    def start(self):
        print "MainScreen2 start"
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 0.05)

    def stop(self):
        print "MainScreen2 stop"
        Clock.unschedule(self.update)

    def update(self, *kwargs):
        global ordersID
        global save
        delta = self.delta - datetime.now()
        self.minutes, seconds = str(delta).split(":")[1:]
        self.seconds = seconds[:5]
        try:
            if int(self.seconds.split(".")[0]) == 1:
                save = True
                
            if int(self.seconds.split(".")[0]) == 0:
                if self.parent.current == 'main4' and save:
                    save = False
                    data = {}  
                    data['backup'] = {
                        'countdown': self.minutes,
                        'screentobe': 'main4',
                        'order': str(ordersID),
                        'timenow': str(datetime.now()),
                    }
                    with open(path+'data.txt', 'w') as outfile:  
                        json.dump(data, outfile)
                    print data

        except:
                print('excepction on updateing screentobe and countdown')
                if save:
                    save = False
                    data = {}  
                    data['backup'] = {
                        'countdown': self.minutes,
                        'screentobe': 'main4',
                        'order': str(ordersID),
                        'timenow': str(datetime.now()),

                    }
                    with open(path+'data.txt', 'w') as outfile:  
                        json.dump(data, outfile)
                    print data
                
        if int(self.minutes) == 0:
            if int(self.seconds.split(".")[0]) == 0:
                if int(self.seconds.split(".")[1]) < 30:
                    self.seconds = "00.00"
                    try:
                        threading.Thread(target=self.Order).start()

                    except:
                        print('Order Not Completed')
                    data = {}  
                    data['backup'] = {
                        'countdown': str(WashTime),
                        'screentobe': 'main0',
                        'order': str(ordersID),
                        'timenow': str(datetime.now()),
                    }
                    with open(path+'data.txt', 'w') as outfile:  
                        json.dump(data, outfile)
                    Clock.unschedule(self.update)
                    print data
                    ############################################################
                    global card
                    global pressStart
                    global checkScreen
                    countdown = 0
                    continuereading = True
                    coins = ''
                    UserName = ''
                    card = False
                    mId= 1
                    uId = ''
                    ordersID = 0
                    cardId = ''
                    options = 'cold'
                    availablebal = 0
                    counter = 0
                    screentobe= 'main0'
                    UserName = ''
                    timenow = datetime.now()
                    checkScreen = True
                    powercut = 0
                    pressStart = True
                    card = False

                    checkScreen = True
                    ############################################################
                    try:
                        self.parent.current = 'main1'
                        self.stop()
                    except:
                        print "MainScreen2 except self.parent.current = 'main0'"
        return(self)
    
    def on_leave(self, **kwargs):
        self.ids.Timer.color = (0, 0, 0, 0)
        print "MainScreen2 on_leave"
        global card
        global pressStart
        pressStart = True
        card = False
        global checkScreen
        checkScreen = True
        return(self)
    
    def on_enter(self, **kwargs):
        global ordersID
        global WashTime
        data = {} 
        data['backup'] = {
        'countdown': str(WashTime),
        'screentobe': 'main4',
        'order': str(ordersID),
        'timenow': str(datetime.now()),
        }
        with open(path+'data.txt', 'w') as outfile:  
            json.dump(data, outfile)
        global countdown
        Clock.unschedule(self.update)
        Clock.unschedule(self.start)
        print "on_enter in 4"
        global pressStart
        print "help pressStart = " + str(pressStart)         
        self.ids.Timer.color = (0, 0, 0, 0)
        print('countdown in __init__ ='+str(countdown))
        print "MainScreen2 on_enter"      
        print('clock on_enter loded countdown = '+str(countdown))

        if pressStart:
            self.ids.ScreenBG.source = 'Screen3.PNG'
            threading.Thread(target=self.puls).start()
            Clock.schedule_once(self.helpScreen, 10)
            pressStart = False
        else:
            print "help on_enter"
            self.parent.current = 'main5'
        return(self)

    def startscreen(self):
        global countdown
        self.delta = datetime.now()+timedelta(minutes = countdown)
        print ">>>>>>>>>>>>>Call screen to press Start<<<<<<<<<<<<<<<<"
        self.ids.ScreenBG.source = 'Screen4.PNG'
        self.ids.Timer.color = (0, 0, 0, 1)
        self.start()
        return(self)
        
    def puls(self):
        global puls
        print "MainScreen2 puls"
        MIFAREReader.puls(puls)
        GPIO.cleanup()
        return(self)
    
    def helpScreen(self, dt):
        global countdown
        self.delta = datetime.now()+timedelta(minutes = countdown)
        print ">>>>>>>>>>>>>Call screen to press Start<<<<<<<<<<<<<<<<"
        self.ids.ScreenBG.source = 'Screen4.PNG'
        self.ids.Timer.color = (0, 0, 0, 1)
        self.start()
        return(self)
    
    def Order(self, dt):
        print('Completed Order Update API')
        http = urllib3.PoolManager()
        r = http.request('PUT','http://api.centurylaundryindia.com/m1/orders',
                        headers={'Content-Type': 'application/json'},
                        body= json.dumps({ 'id': str(ordersID), 'status': 'C' }))
        order = json.loads(r.data.decode('utf-8'))
        print(str(order))
        ordersdetails= order['orders']
        ordersID = ordersdetails['id']
        print("Order no in if:" + str(ordersID)+ "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        success= order['success']
        print('Card Order created or updated :' + str(success))
        print('Order Completed')
        return(self)
    
    pass
############################################################################################3
class MainScreen5(Screen):
    minutes = StringProperty()
    seconds = StringProperty()
    delta = None
    global WashTime  
    
    def __init__(self, **kwargs):
        super(MainScreen5, self).__init__(**kwargs)

    def start(self):
        print "MainScreen5 start"
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, 0.05)

    def stop(self):
        print "MainScreen5 stop"
        Clock.unschedule(self.update)

    def update(self, *kwargs):
        global countdown
        global ordersID
        global save
        delta = self.delta - datetime.now()
        self.minutes, seconds = str(delta).split(":")[1:]
        self.seconds = seconds[:5]
        try:
            if int(self.seconds.split(".")[0]) == 1:
                save = True
                
            if int(self.seconds.split(".")[0]) == 0:
                if self.parent.current == 'main5' and save:
                    save = False
                    countdown = int(self.minutes)
                    data = {}
                    data['backup'] = {
                        'countdown': self.minutes,
                        'screentobe': 'main4',
                        'order': str(ordersID),
                        'timenow': str(datetime.now()),
                    }
                    with open(path+'data.txt', 'w') as outfile:  
                        json.dump(data, outfile)
                    print data

        except:
                print('excepction on updateing screentobe and countdown')
                if save:
                    save = False
                    data = {}  
                    data['backup'] = {
                        'countdown': self.minutes,
                        'screentobe': 'main4',
                        'order': str(ordersID),
                        'timenow': str(datetime.now()),

                    }
                    with open(path+'data.txt', 'w') as outfile:  
                        json.dump(data, outfile)
                    print data
                
        if int(self.minutes) == 0:
            if int(self.seconds.split(".")[0]) == 0:
                if int(self.seconds.split(".")[1]) < 30:
                    self.seconds = "00.00"
                    try:
                        threading.Thread(target=self.Order).start()

                    except:
                        print('Order Not Completed')
                    data = {}  
                    data['backup'] = {
                        'countdown': str(WashTime),
                        'screentobe': 'main0',
                        'order': str(ordersID),
                        'timenow': str(datetime.now()),
                    }
                    with open(path+'data.txt', 'w') as outfile:  
                        json.dump(data, outfile)
                    Clock.unschedule(self.update)
                    print data
                    ############################################################
                    countdown = 0
                    continuereading = True
                    coins = ''
                    UserName = ''
                    card = False
                    mId= 1
                    uId = ''
                    ordersID = 0
                    cardId = ''
                    options = 'cold'
                    availablebal = 0
                    counter = 0
                    screentobe= 'main0'
                    UserName = ''
                    timenow = datetime.now()
                    checkScreen = True
                    powercut = 0
                    ############################################################
                    try:
                        self.parent.current = 'main1'
                        self.stop()
                    except:
                        print "MainScreen2 except self.parent.current = 'main0'"
        return(self)
    
    def on_leave(self, **kwargs):
        data = {}  
        data['backup'] = {
            'countdown': str(WashTime),
            'screentobe': 'main0',
            'order': str(ordersID),
            'timenow': str(datetime.now()),
        }
        with open(path+'data.txt', 'w') as outfile:  
            json.dump(data, outfile)
        self.ids.Timer.color = (0, 0, 0, 0)
        print "MainScreen2 on_leave"
        global card
        global pressStart
        pressStart = True
        card = False
        global checkScreen
        checkScreen = True
        return(self)
    
    def on_enter(self, **kwargs):
        global countdown
        Clock.unschedule(self.update)
        Clock.unschedule(self.start)
        global ordersID
        global WashTime
        print "on_enter in 5"
        global pressStart
        print "help pressStart = " + str(pressStart)    
        self.ids.Timer.color = (0, 0, 0, 0)
        print('countdown in __init__ ='+str(countdown))
        print "MainScreen2 on_enter"
        print('clock on_enter loded countdown = '+str(countdown))
        return(self)

    def startscreen(self):
        global countdown
        self.delta = datetime.now()+timedelta(minutes = countdown)
        print ">>>>>>>>>>>>>Call screen to press Start<<<<<<<<<<<<<<<<"
        self.ids.ScreenBG.source = 'Screen4.PNG'
        self.ids.Timer.color = (0, 0, 0, 1)
        self.start()
        return(self)
        
    def puls(self):
        global puls
        print "MainScreen2 puls"
        MIFAREReader.puls(puls)
        GPIO.cleanup()
        return(self)
    
    def helpScreen(self, dt):
        global countdown
        self.delta = datetime.now()+timedelta(minutes = countdown)
        print ">>>>>>>>>>>>>Call screen to press Start<<<<<<<<<<<<<<<<"
        self.ids.ScreenBG.source = 'Screen4.PNG'
        self.ids.Timer.color = (0, 0, 0, 1)
        self.start()
        return(self)
    
    def Order(self, dt):
        print('Completed Order Update API')
        http = urllib3.PoolManager()
        r = http.request('PUT','http://api.centurylaundryindia.com/m1/orders',
                        headers={'Content-Type': 'application/json'},
                        body= json.dumps({ 'id': str(ordersID), 'status': 'C' }))
        order = json.loads(r.data.decode('utf-8'))
        print(str(order))
        ordersdetails= order['orders']
        ordersID = ordersdetails['id']
        print("Order no in if:" + str(ordersID)+ "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        success= order['success']
        print('Card Order created or updated :' + str(success))
        print('Order Completed')
        return(self)
    
    pass
#################################################################################################
#################################################################################################
#################################################################################################
class ScreenManagement(ScreenManager):
    pass
#################################################################################################
#################################################################################################
#################################################################################################

presentation = Builder.load_file("styles.kv")

#################################################################################################
#################################################################################################
#################################################################################################
class MainApp(App):
        
    def build(self, **kwargs):
        return presentation

if __name__ == '__main__':
    MainApp().run()
