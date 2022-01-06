import os
import cv2
import codecs
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))

argv={}
for d in range(1,len(sys.argv)):
	d=d.split("=")
	argv[d[0]]=d[1]


POS_NAME="POS"
if 'WIDTH' in argv:
	POS_WIDTH=argv["WIDTH"]
else:
	POS_WIDTH=50

if 'HEIGHT' in argv:
	POS_HEIGHT=argv["HEIGHT"]
else:
	POS_HEIGHT=50

NEG_NAME="NEG"

if 'NUMSTAGES' in argv:
	NUMSTAGES=argv["NUMSTAGES"]
else:
	NUMSTAGES=10

if 'METHOD' in argv:
	METHOD=argv["METHOD"]
else:
	METHOD="HAAR" #HAAR, LBP


OUT_TEXT=""
POS_NUM=0
for f in os.listdir(POS_NAME):
	print(f"{POS_NAME}/{f}")
	OUT_TEXT+=POS_NAME+"/"+f+" 1 0 0 "+str(POS_WIDTH)+" "+str(POS_HEIGHT)+"\n"
	POS_NUM+=1

f=codecs.open(POS_NAME+".txt","w")
f.write(OUT_TEXT)
f.close()

OUT_TEXT=""
NEG_NUM=0
for f in os.listdir(NEG_NAME):
	print(f"{NEG_NAME}/{f}")
	OUT_TEXT+=f"{NEG_NAME}/{f}\n"
	NEG_NUM+=1

f=codecs.open(NEG_NAME+".txt","w")
f.write(OUT_TEXT)
f.close()


print("===opencv_createsamples===")
opencv_createsamples="opencv_createsamples"
opencv_createsamples+=" -info "+POS_NAME+".txt -vec "+POS_NAME+".vec -bg "+NEG_NAME+".txt -num "+str(POS_NUM)
opencv_createsamples+=" -w "+str(POS_WIDTH)+" -h "+str(POS_HEIGHT)
os.system(opencv_createsamples)

print("===opencv_traincascade===")
opencv_traincascade="opencv_traincascade"
opencv_traincascade+=" -data xml -vec "+POS_NAME+".vec -bg "+NEG_NAME+".txt -numPos "+str(POS_NUM)
opencv_traincascade+=" -numNeg "+str(NEG_NUM)+" -numStages "+str(NUMSTAGES)
opencv_traincascade+=" -featureType "+METHOD
opencv_traincascade+=" -w "+str(POS_WIDTH)+" -h "+str(POS_HEIGHT)
opencv_traincascade+=" -precalcValBufSize 4048 -precalcIdxBufSize 4048 -numThreads 24 -maxFalseAlarmRate 0.5 -minHitRate 0.99999"
os.system(opencv_traincascade)

