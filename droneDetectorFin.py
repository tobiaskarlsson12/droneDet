from scipy import fft, arange
import numpy as np
from scipy.io import wavfile
import os
import pyaudio
import wave
#Nedan skapas fft. Detta görs med fft bilbotek. Det skapas även en array med frekvens.
def fft_creator(x, sf):
    #Normalisera kring nollan nedan.
    x = x - np.mean(x)
    n = len(x)
    k = arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)
    #Skapar frekvensarray
    frqarr = frqarr[range(n // 2)]
    x = fft(x) / n
    #Vi vill bara ha ena halvan av frekvens intervall, inte de negativa delarna.
    x = x[range(n // 2)]
    return frqarr, abs(x)


#Funktionen nedan är sjävla hjärnan i programmet. Den får in vårt samplade 2 sekunders
#värde och testar.
def drone_Detector(fsInData, inData):

    #Här så tas des sample vi gjorde i början in för att jämföra med hur det brukar vara. FFt skapas av insignalen och vår samplesignal
    #och vi subtraherar med samplesignalen för att få bort brus och annat.
    fsInDataSample, inDataSample = wavfile.read(WAVE_OUTPUT_FILENAMESa)
    #Våra samples kommer i två såkallade kanaler ibland därför tittar vi detta nedan
    #ifall det är fallet tar vi medelvärdet av dessa två.
    try:
       inDataSample = (inDataSample[:, 0] + inDataSample[:, 1])/2 
       inData = (inData[:, 0]+inData[:, 1])/2
    except:
       inData = inData
    frqInDataSa, fftInDataSa = fft_creator(inDataSample, fsInDataSample)
    frqInData, fftInData = fft_creator(inData, fsInData)
    #Nedan så används vår sample som vi tog i början för att få bort eventuellt bakgrundsljud.
    fftInData = (fftInData-fftInDataSa)
    fftInData = abs(fftInData)

    #Här så skapar vi kvot för indata genom att välja ett frekvensområde sen hitta peaken inom det område. Sedan då jämförs det med
    #summan av FFTn i samma intervall och kvotInData skapas.Denna kvot finns beskrivit i flödetschemat.För att undvika falskalarm görs en annan
    # jämföran.Vi tittar då 1500 hz bort från frekvensintervaller för att jämföra maxvärdet där mot maxvärdet i vårt intervall.
    # Denna kvot skiljer sig mycket om det är drönare eller bara lågt ljud som ger falsk alarm. Denna kvot finns också i flödesschemat.
    dataMaxfrq = np.max(fftInData[int((len(frqInData)/(RATE/2))*freqStart): int((len(frqInData)/(RATE/2))*freqEnd)])
    dataMaxfrqO = np.max(fftInData[int((len(frqInData)/(RATE/2))*(freqStart+1500)): int((len(frqInData)/(RATE/2))*(freqEnd+1500))])

    freqRangeInData = int((len(frqInData)/(RATE/2))*freqEnd) - int((len(frqInData)/(RATE/2))*freqStart)
    AInData = (freqRangeInData)*np.max(fftInData[int((len(frqInData)/(RATE/2))*freqStart): int((len(frqInData)/(RATE/2))*freqEnd)])
    AjInData = sum(fftInData[int((len(frqInData)/(RATE/2))*freqStart): int((len(frqInData)/(RATE/2))*freqEnd)]) 
    kvotInData=AInData/AjInData;
    
    
    # Hämta data från 4 exempelfall                                                            
    fsT30, dataT30 = wavfile.read('T30.wav')
    fsT50, dataT50 = wavfile.read('T50.wav')
    fsT70, dataT70 = wavfile.read('T70.wav')
    fsT100, dataT100 = wavfile.read('T100.wav')
    
    #Dessa jämför vi med och skapar sedan respektive fft
    yT30 = (dataT30[:, 0]+ dataT30[:, 0] )/2
    yT50 = (dataT50[:, 0]+ dataT50[:, 0] )/2
    yT70 = (dataT70[:, 0]+ dataT70[:, 0] )/2
    yT100 =(dataT100[:, 0]+ dataT100[:, 0] )/2
       
    frkvotT30, fftT30 = fft_creator(yT30, fsT30)
    frkvotT50, fftT50 = fft_creator(yT50, fsT50)
    frkvotT70, fftT70 = fft_creator(yT70, fsT70)
    frkvotT100, fftT100 = fft_creator(yT100, fsT100)
    
    #Nedan så skapas kvoten för alla våra exempelfall på samma sätt som de gjordes för indatan ovan.
    #30% Throttle
#Nedan används för att jämföra kvot mot indata men behövs inte annars
#    xT30max=np.max(fftT30[int((len(fftT30)/(RATE/2))*freqStart): int((len(fftT30)/(RATE/2))*freqEnd)])
#    xT30max2=np.max(fftT30[int((len(fftT30)/(RATE/2))*(freqStart+1500)): int((len(fftT30)/(RATE/2))*(freqEnd+1500))])
   
    xT30 = int((len(frkvotT30)/(RATE/2))*freqEnd) - int((len(frkvotT30)/(RATE/2))*freqStart)
    AT30 = (xT30)*np.max(fftT30[int((len(fftT30)/(RATE/2))*freqStart): int((len(fftT30)/(RATE/2))*freqEnd)])
    AjT30 = sum(fftT30[int((len(frkvotT30)/(RATE/2))*freqStart): int((len(frkvotT30)/(RATE/2))*freqEnd)])
    kvotT30=AT30/AjT30;
    #50% Throttle    
#    xT50max=np.max(fftT50[int((len(fftT50)/(RATE/2))*freqStart): int((len(fftT50)/(RATE/2))*freqEnd)])
#    xT50max2=np.max(fftT50[int((len(fftT50)/(RATE/2))*(freqStart+1500)): int((len(fftT50)/(RATE/2))*(freqEnd+1500))])
    
    xT50 = int((len(frkvotT50)/(RATE/2))*freqEnd)-int((len(frkvotT50)/(RATE/2))*freqStart)
    AT50 = (xT50)*np.amax(fftT50[int((len(frkvotT50)/(RATE/2))*freqStart): int((len(frkvotT50)/(RATE/2))*freqEnd)])
    AjT50 = sum(fftT50[int((len(frkvotT50)/(RATE/2))*freqStart): int((len(frkvotT50)/(RATE/2))*freqEnd)])
    kvotT50=AT50/AjT50;
    #70% Throttle
#    xT70max=np.max(fftT70[int((len(fftT30)/(RATE/2))*freqStart): int((len(fftT30)/(RATE/2))*freqEnd)])
#    xT70max2=np.max(fftT70[int((len(fftT30)/(RATE/2))*(freqStart+1500)): int((len(fftT30)/(RATE/2))*(freqEnd+1500))])
    
    xT70 = int((len(frkvotT70)/(RATE/2))*freqEnd)- int((len(frkvotT70)/(RATE/2))*freqStart)
    AT70 = (xT70)*np.max(fftT70[int((len(fftT70)/(RATE/2))*freqStart): int((len(fftT70)/(RATE/2))*freqEnd)])
    AjT70 = sum(fftT70[int((len(frkvotT70)/(RATE/2))*freqStart):int((len(frkvotT70)/(RATE/2))*freqEnd)])
    kvotT70=AT70/AjT70;
    #100% Throttle
#    xT100max=np.max(fftT100[int((len(fftT30)/(RATE/2))*freqStart): int((len(fftT30)/(RATE/2))*freqEnd)])
#    xT100max2=np.max(fftT100[int((len(fftT30)/(RATE/2))*(freqStart+1500)): int((len(fftT30)/(RATE/2))*(freqEnd+1500))])
    xT100= int((len(frkvotT100)/(RATE/2))*freqEnd) -int((len(frkvotT100)/(RATE/2))*freqStart);
    AT100 = (xT100)*np.amax(fftT100[int((len(frkvotT100)/(RATE/2))*freqStart):int((len(frkvotT100)/(RATE/2))*freqEnd)])
    AjT100 = sum(fftT100[int((len(frkvotT100)/(RATE/2))*freqStart):int((len(frkvotT100)/(RATE/2))*freqEnd)])
    kvotT100=AT100/AjT100;
    
    #Här hämtar vi droneCount som håller koll på gånger vi trott att vi sett drönare
    #Tittar vilka som matchar, är det potentiellt drönare?
    #Jämför även dataMaxfrq/dataMaxfrqO för att undersöka om det kan vara brus. Dessa
    # siffor, tex 0.8 och 1.25 kan behövas ändras vid optimering. droneCount
    # är till för att undvika falskalarm och det krävs just nu 3 alarm
    #för drönare för att vi ska tro på det. Denna siffran kan också ändras
    
    global droneCount
    if (kvotT30/kvotInData)>0.8 and (kvotT30/kvotInData)<1.25 and (dataMaxfrq/dataMaxfrqO)>4 :
      #song = AudioSegment.from_wav("BOMB_SIREN-BOMB_SIREN-247265934.wav")
      #play(song)
      droneCount=droneCount+1
      if(droneCount==3):    
          print('\x1b[0;30;41m'+'Drone!' + '\x1b[0m')
          droneCount=0
      else:
          print('\x1b[0;30;41m'+'Waiting for confirmation....' + '\x1b[0m')
          print("Drone search count is: "+ np.str(droneCount)+"|")
      
    elif (kvotT50/kvotInData)>0.8 and (kvotT50/kvotInData)<1.25  and  (dataMaxfrq/dataMaxfrqO)>4:
      #song = AudioSegment.from_wav("BOMB_SIREN-BOMB_SIREN-247265934.wav")
      #play(song)
      droneCount=droneCount+1
      if(droneCount==3):    
          print('\x1b[0;30;41m'+'Drone!' + '\x1b[0m')
          droneCount=0
      else:
          print('\x1b[0;30;41m'+'Waiting for confirmation....' + '\x1b[0m')
          print("Drone search count is: "+ np.str(droneCount)+"|")
      
    elif (kvotT70/kvotInData)>0.8 and (kvotT70/kvotInData)<1.25  and  (dataMaxfrq/dataMaxfrqO)>4:
      #song = AudioSegment.from_wav("BOMB_SIREN-BOMB_SIREN-247265934.wav")
      #play(song)
      droneCount=droneCount+1
      if(droneCount==3):    
          print('\x1b[0;30;41m'+'Drone!' + '\x1b[0m')
          droneCount=0
      else:
          print('\x1b[0;30;41m'+'Waiting for confirmation....' + '\x1b[0m')
          print("Drone search count is: "+ np.str(droneCount)+"|")
    
    elif (kvotT100/kvotInData)>0.8 and (kvotT100/kvotInData)<1.25  and (dataMaxfrq/dataMaxfrqO)>4:
      #song = AudioSegment.from_wav("BOMB_SIREN-BOMB_SIREN-247265934.wav")
      #play(song)
      droneCount=droneCount+1
      if(droneCount==3):    
          print('\x1b[0;30;41m'+'Drone!' + '\x1b[0m')
          droneCount=0
      else:
          print('\x1b[0;30;41m'+'Waiting for confirmation....' + '\x1b[0m')
          print("Drone search count is: "+ np.str(droneCount)+"|")

    else:
      droneCount=0
      print('\x1b[6;30;42m' + 'Puhh.. No Drone so far!' + '\x1b[0m' )
      print("Drone search count is: "+ np.str(dataMaxfrq/dataMaxfrqO)+"|"+ np.str(xT100max/xT100max2))
    
    print("_____________________________________________________"+"\n")

#Här nedan börjar programmet och loopas sedan i while(true) satsen. Dronecount är en global variabel
#som håller koll på hur många gånger vi trott att vi har hittat drönare. Gränsen är 3 sen kan vi vara "Säkra".
#Nedan är lite grejer för inspelning. Typ vilket rate samt hur många sekunder.
#Ett biblotek används för inspelning, PyAudio.
WAVE_OUTPUT_FILENAME = "recorded.wav"
droneCount=0
CHUNK = 1024*2
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
#Detta är frekvensitervallet vi valt för att undersöka om drönare finns.
#Värdet kommer att behöva anpassas till mikrofon samt vart vi ser signifikant
#och speciell peak för just drönare jämfört med annat.
freqStart=4800;
freqEnd=5200;

#Nedan så spelas sample in som sedan används för att jämföra. Denna fil
#sparas som en .wav fil under namnet recordedSa.wav
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
print("* recording sample")
        
frames = []
        
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
WAVE_OUTPUT_FILENAMESa = "recordedSa.wav"

print("* done recording sample")
print("____________________________________________________________________________________")
  
print("____________________________________________________________________________________")
 
stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILENAMESa, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
here_path = os.path.dirname(os.path.realpath(__file__))

#Testfiler att jämföra med. Så kallade störningar
sounds= ['applause-2.wav', 'recordinsrone2020_02_22_00_21_02.wav','crowd_outside_2.wav','droneT30.wav', 'laugh_4.wav','crowd_outside_1.wav','drone101.wav'];
#for x in range(len(sounds)):
while True:
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    #Här nedan spelas indata in under en sekund. Denna indatan sparas under
    #en .wav fil vid namn recorded.wav.
    frames = []    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)        
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    here_path = os.path.dirname(os.path.realpath(__file__))
    wav_file_name = 'recorded.wav'
    fsInData, inData = wavfile.read(wav_file_name)
    #När vi spelat in skickar vi in inspelade till vår drone_Detector sen
    #börjar vi om i toppen på while-satsen igen.
    drone_Detector(fsInData,inData);  