import cv2
from cvzone.HandTrackingModule import HandDetector


class buttons:
    def __init__ (self, p, w, h, v):
        self.p = p
        self.w = w
        self.h = h
        self.v = v
# p = position , w = width, h = height, v = value
    def draw(self,img):
        cv2.rectangle(img, self.p, (self.p[0]+self.w, self.p[1]+self.h), (200, 150, 100), -2)
        cv2.rectangle(img, self.p, (self.p[0]+self.w, self.p[1]+self.h), (0, 0, 255), 2)
        cv2.putText(img, self.v, (self.p[0]+25,self.p[1]+46), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0,0,0), 2)
    
    def isClick(self,pt1,pt2):
        if (self.p[0] < pt1 < self.p[0]+self.w)& \
            (self.p[1] < pt2 < self.p[1]+self.h):
            cv2.rectangle(cam, self.p, (self.p[0]+self.w, self.p[1]+self.h), (0, 0, 0), -2)
            cv2.rectangle(cam, self.p, (self.p[0]+self.w, self.p[1]+self.h), (0, 0, 255), 2)
            cv2.putText(cam, self.v, (self.p[0]+16,self.p[1]+33), cv2.FONT_HERSHEY_COMPLEX, 1.3, (255,255,255), 3)
            return 20
        else:
            return 0
    
    
    

buttons_list= [['1', '2', '3', '+'],
               ['4', '5', '6', '-'],
               ['7', '8', '9', '*'],
               ['.', '0', '/', '=']]


button = []
for i in range(1,5):
    for k in range(1,5):
        x = i* 70 +285
        y = k* 70 +19
        button.append(buttons((x,y), 70, 70, buttons_list[k-1][i-1]))


HD = HandDetector(maxHands=1)
vid = cv2.VideoCapture(0)

Equation = ''
stop = 0
while 1:
    done, cam = vid.read()
    cam = cv2.flip(cam, 1)
    
    hand, cam = HD.findHands(cam)
    
    for i in button:
        i.draw(cam)
    
    # The background of Equation and result rectangle
    cv2.rectangle(cam, (355, 20), (635, 89), (255, 0, 0), -2)
    # The boundary of equation and result rectangle
    cv2.rectangle(cam, (355, 20), (635, 89), (0, 0, 255), 2)
    
    if hand:
        LandMarks = hand[0]['lmList']
        distance, info, cam = HD.findDistance(LandMarks[4], LandMarks[8], cam)
        x1,y1 = LandMarks[8]
        
        if distance<36 and stop==0:
            for i, r in enumerate(button):
                if r.isClick(x1,y1):
                    f = buttons_list[int(i%4)][int(i/4)]
                    
                    if f == '=':
                        Equation = str(eval(Equation))
                    else:   
                        Equation += f
                        stop = 1
    # to limit the duplications of the value you write it on the calculator                    
    if stop !=0:
        stop+=1
        if stop >6:
            stop=0
    
    # write the equation on the display of calculator
    cv2.putText(cam, Equation, (361, 61), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0,0,0), 2)
    
    
    cv2.imshow("__Ayad __"*6, cam)
    
    # if you click on the c button on your keyboard,
    # it will clear the display of the calculator
    if cv2.waitKey(1) == ord('c'):
        Equation = ''
        
    # if you click on the x button on your keyboard,
    # it will close the calculator
    if cv2.waitKey(1) == ord('x'):
        break
    
    # if you click on the d button on your keyboard,
    # it will delete the last value you write it on the calculator
    # if cv2.waitKey(1) == ord('d'):
    #     Equation = Equation[:-1]

cv2.destroyAllWindows()
