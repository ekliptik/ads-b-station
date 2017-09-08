import fileinput
import string
import pyModeS as pms    #This library is awesome!
from string import ascii_uppercase

def main():
    for unformatted in fileinput.input():
        formatted = processLine(unformatted)
        msg = Message(formatted)
        #print(msg.type)
        if msg.type == "callsign":
            # print(msg.callsign, end='\n')
            print(pms.adsb.callsign(formatted))
        elif msg.type == "surfPos":
            print(pms.adsb.)
    print('')

def processLine(i):
    out = []
    for c in i:
        if not c.isalnum():
            pass
        else:
            out.append(c)
    return ''.join(out)

class Message:
    def __init__(self, msg):
        self.checksum = int(pms.util.crc(msg, encode=False))
        self.typeCode = pms.adsb.typecode(msg)
        self.downlinkFormat = pms.adsb.df(msg)
        self.ICAO = pms.adsb.icao(msg)
        self.data = pms.adsb.data(msg)
        if self.checksum != 0:
            self.type = 'bad'
        elif self.typeCode < 5 and self.downlinkFormat == 17:
            self.type = 'callsign'
            self.callsign = pms.adsb.callsign(msg)
        elif self.typeCode < 9:
            self.type= 'surfPos'
        elif self.typeCode < 19:
            self.type= 'airPosBaro'
        elif self.typeCode < 20:
            self.type= 'airVel'
        elif self.typeCode < 23:
            self.type= 'airPosGNSS'
        else:
            self.type= 'other' 
    
    def getCallsign(self):                                      #I spent two days on this before I found out 
        lean = []                                               #the library can do it
        for i in range(12):
            lean.append(self.data[i+2])
        interim = bin(int(''.join(lean), 16))
        interim = interim[2:].zfill(48)
        rawCS = []
        callsign = ''
        for c in range(8):
            rawCS.append(0)
            for bit in range(6):
                rawCS[c] = rawCS[c] + pow(2, bit) * int(interim[5-bit+6*c])
            if 1 <= rawCS[c] < 27:
                callsign = callsign + ascii_uppercase[rawCS[c]-1]
            elif 48 <= rawCS[c] < 58:
                callsign = (callsign + str(rawCS[c] - 48))
            elif rawCS[c] == 32:
                callsign = callsign + '_'
            else:
                print("It's borked!")
                self.type = 'borked' # heck
        return(callsign)

main()