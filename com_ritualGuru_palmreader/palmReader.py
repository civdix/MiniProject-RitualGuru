import cv2 as cv
import HandTrackingModule as htm
import json
import os
class PalmReader:
    def __init__(self):
        print("Package Initialized")
    
        
    def Planet(self,filePath):
        print("Function running")
        img  = cv.imread(filePath);
        detector = htm.FindHands(detection_con=0.75)
        img = cv.resize(img,(400,400))
        hand = detector.getPosition(img,range(21),draw=True)
        a1,a2,a3 = (hand[6][1]-hand[5][1])*-1,(hand[7][1]-hand[6][1])*-1,(hand[8][1]-hand[7][1])*-1
        b1,b2,b3 = (hand[10][1]-hand[9][1])*-1,(hand[11][1]-hand[10][1])*-1,(hand[12][1]-hand[11][1])*-1
        c1,c2,c3 = (hand[14][1]-hand[13][1])*-1,(hand[15][1]-hand[14][1])*-1,(hand[16][1]-hand[15][1])*-1
        d1,d2,d3 = (hand[18][1]-hand[17][1])*-1,(hand[19][1]-hand[18][1])*-1,(hand[20][1]-hand[19][1])*-1
        print(f'{a1,a2,a3}\n{b1,b2,b3}\n{c1,c2,c3}\n{d1,d2,d3}\n')
        a1 = a1- 0.25*a1
        b1 = b1 - 0.27*b1
        c1 = c1 - 0.3*c1
        d1 = d1 -0.3*d1
        a2 = a2 + 0.1*a2
        c2 = c2 + 0.17*c2
        b2 = b2 + 0.1*b2
        # points = [a1,a2,a3,b1,b2,b3,c1,c2,c3,d1,d2,d3]
        # cv.circle(img,(int(a1),hand[5][1]),5,(255,33,53),4)
        # cv.line(img,(hand[5][0],int(a1)),(hand[5][0],int(a2)),(0,255,255),5)
        planet = ''
        print(f'{a1,a2,a3}\n{b1,b2,b3}\n{c1,c2,c3}\n{d1,d2,d3}\n')
        sum_a = a1 + a2 + a3
        sum_b = b1 + b2 + b3
        sum_c = c1 + c2 + c3
        sum_d = d1 + d2 + d3
        # Determine the ruling planet
        if sum_a > sum_c and sum_a > (b1+b2+b3/2):
                planet = "jupiter"
        elif sum_c > sum_a and sum_c > (b1+b2+b3/2): 
                planet = "sun"
        elif sum_a == sum_c and (sum_a < (b1+b2+b3/2) or sum_a < (b1+b2+b3/2)): #(a1+a2+a3) = (c1+c2+c3) && (a1+a2+a3),(c1+c2+c3) < (b1+b2+b3/2) 
                planet = "saturn"
        elif sum_a == sum_c and (sum_a >(b1+b2+b3/2) or sum_c>(b1+b2+b3/2)) and sum_d > (c1+c2+c3/2):
                planet = "mercury"
        else:
                planet = "No ruling planet"
        with open('D:/Python/openCV/resources/dataset/planet.json','r') as file:
            data = json.load(file)
        print("\nMay contain error thats why showing all Possible planets nature")
        print(data)
        return {"mat":img,"result":data[planet],"message":"Congrats your planet is "+planet}

    def PuPiFl(self,filePath):

        img  = cv.imread(filePath)
        if img is not None:

            detector = htm.FindHands(detection_con=0.75)
            img = cv.resize(img,(400,400))
            hand = detector.getPosition(img,range(21),draw=True)

            #  Calculating Palm Lenght (PL) 
            PL=hand[9][1]-hand[0][1] + int((hand[10][1]-hand[9][1])/2)
            # Calculating the Palm Width(PW)
            PL*=-1
            PW = hand[5][0]-hand[17][0]
            PW += (30/100)*PW
            print(f'PW: {PW} PL:{PL}')
            ratioPWPL = PW/PL
            palmType = ''
            fingerType = ''
            if(ratioPWPL<0.8):
                palmType='Rectangular'
            else:
                palmType="Square"

            # Calculating the Finger Length (FL)
            FL =  hand[9][1]-hand[12][1] 

            ratioFLPL = FL/PL
            if(palmType=="Square"):
                if(ratioFLPL>0.9):
                    fingerType='Long'
                else:
                    fingerType="Short"
            else:
                if(ratioFLPL>0.8):
                    fingerType='Long'
                else:
                    fingerType="Short"

            # print(ratioFLPL)
            print(palmType+' Palm and Finger type '+fingerType,':-')
            with open("D:/Python/openCV/resources/dataset/ratioPWPLFL.json",'r') as file:
                data = json.load(file)
            return {"mat":img,"result":data[palmType+fingerType],"message":"Congrats your Palm is "+palmType+" with finger type "+fingerType}
        else:
            print('Check the file name or check Wheater the File Uploaded or not')
            return {"mat":[],"result":"error","message":"Error Occured"}



    def middleFingerAnalysis(self, filePath):
            img  = cv.imread(filePath)
            img = cv.resize(img,(400,400))

            def clear_terminal():
                # For Windows
                if os.name == 'nt':
                    os.system('cls')
            #     For macOS/Linux
                else:
                    os.system('clear')

            def checkFingerLength(handPosition):
                    yPosition=[]
                    mutualDistance={}
                    for id in [4,8,12,16,20]:# thumb index middle  pinky Upper tips
                            yPosition.append(-handPosition[id][1]+handPosition[id-3][1])
                   # determine the length diffrence of each finger with each other with correction with 
                    for id in [4,8,12,16,20]:
                            targetIds = [i for i in range(4,21,4) if i!=id]
                            mutualDistFromSpecificId = {}
                            yDash=handPosition[id][1]-handPosition[id-3][1]
                            for target in targetIds:
                                    # checking for x which is the distance of current tip to the target tip 
                                    # Here we simple subtract current Finger height to target finger height
                                    yDashDash = handPosition[target][1]-handPosition[target-3][1]
                                    realDistancefromId = -yDashDash + yDash
                                    mutualDistFromSpecificId[target]=realDistancefromId
                            mutualDistance[id] = mutualDistFromSpecificId
                    return (yPosition,mutualDistance)

            detector = htm.FindHands(detection_con=0.75)
            handPosition= detector.getPosition(img,range(21),draw=True)
            eachfingerLength,fingerDistanceFromOtherFinger = checkFingerLength(handPosition)
            # print('Length of Each Finger is',eachfingerLength)
            # print('Distance of Each Finger from Particular Finger',fingerDistanceFromOtherFinger)
            # max_value = max(my_dict.values())
            minFingerDistanceFromMiddleFinger=min(fingerDistanceFromOtherFinger[12].values())
            index=0
            maxi = -10000
            secondBig=0

            for i in fingerDistanceFromOtherFinger[12]:
                    temp= maxi
                    maxi = max(fingerDistanceFromOtherFinger[12][i],maxi)
                    if(temp!=maxi):
                            secondBig = i

            clear_terminal()
            print(secondBig)
            finger = "ERROR"
            thirdBig = 16 if secondBig == 8 else 8
            minFingerDistanceFromMiddleFinger=secondBig #maxi means mini height from middle finger or seconds max in fingers
            if((fingerDistanceFromOtherFinger[12][secondBig]-fingerDistanceFromOtherFinger[12][thirdBig])<2):
                    print(fingerDistanceFromOtherFinger[12][secondBig]-fingerDistanceFromOtherFinger[12][thirdBig])
                    print("Your Middle Index Ring Fingers are nearly equal and this shows\nBalanced Personality: \nEqual lengths are thought to symbolize harmony between ambition (index finger), responsibility (middle finger), and creativity (ring finger).It might suggest a well-rounded personality with balanced traits.\nModeration and Stabilty: \nA person with such finger proportions is often considered steady, even-tempered, and fair.\nThey might not lean too heavily toward dominance, creativity, or seriousness but display a mix of these qualities in moderation.\nInfluence of Saturn:\nSince the middle finger (associated with Saturn) is generally the longest, its equality with the index and ring fingers may indicate a grounding force.\nThis can represent a strong connection to practicality, discipline, and wisdom.\nSpiritual Balance:\nIn some traditions, it could signify a person who is naturally attuned to spiritual or universal balance, as the fingers reflect equilibrium in life.\nScientific Perspective\nFrom a scientific standpoint, the equal length of fingers might suggest:\n\nLow Variance in Hormonal Exposure:\nThis could indicate balanced prenatal exposure to testosterone and estrogen, as no finger was disproportionately influenced during development.\nGenetic Influence:\nIt might simply be a unique genetic trait, with no significant implications on personality or behavior.")     

            elif(minFingerDistanceFromMiddleFinger==16):
                    finger = "RingFinger"

            else:
                    finger = "IndexFinger"

            for pos in handPosition:
                    cv.circle(img, pos, 5, (0,255,0), cv.FILLED)
            cv.circle(img,handPosition[16],5,(255,255,255),cv.FILLED)

            k=cv.waitKey(0)
            if k==ord('q'):
                    cv.destroyAllWindows()
            with open("D:/Python/openCV/resources/dataset/fingerLengthAnalysis.json",'r') as file:
                   data = json.load(file)
            # print(data[finger])
            return {"mat":img,"result":data[finger],"message":"Your 2nd Big Finger is "+finger}
            # Printing Result or sending in response

    # s = middleFingerAnalysis("D:/Python/openCV/resources/images/fingerImages/luvHand.jpg")



    


