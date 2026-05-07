import mss
import pytesseract
import numpy as np
import time
import cv2
x1,y1 = 1797, 194
x2,y2 = 1843,210
u1,v1 = 1798,158
u2,v2 = 1837,172
width = x2 - x1
h = y2 - y1
vidth = u2 - u1
l = v2 - v1
region1 = {"left": u1, "top": v1, "width": vidth, "height": l}
region2 = {"left": x1, "top": y1, "width": width, "height": h}
def Main():
    with mss.mss() as sct:
        s1 = np.array(sct.grab(region1))
        s2 = np.array(sct.grab(region2))
        s1 = cv2.cvtColor(s1, cv2.COLOR_BGRA2GRAY)
        s2 = cv2.cvtColor(s2, cv2.COLOR_BGRA2GRAY)
        x = pytesseract.image_to_string(s1)
        y = pytesseract.image_to_string(s2)
        time.sleep(0.5)
        
        x= x.strip()
        x = "-" + x
        if x.startswith("--"):
            x = x.replace("--", "-")
        x = x.replace("_", "0").replace("¢", "0").replace("O","0").replace(".","").replace("°","0")
        try:
            y= int(y.strip())
            print(f"{x}  {y}")
            x = int(x)
            return x,y
        except ValueError:
            print("H")
            
    

    
