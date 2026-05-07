import numpy
import cv2
import coordinategrabber
sint = cv2.imread("sint.png")
# known coordinates
x1,y1= -4695, 23493;
u1,v1 = 190,208

x2, y2= -2800,21485
u2, v2 = 263,827

u3,v3=1245,42
x3,y3=-8131, 20622 

x4,y4=-6955,18208
u4,v4=1498,631
# ui,vi = x,y coordinates on the picture
# xi, yi = x and z coordinates ingame
#data
gamecoords = numpy.array([
    [x1,y1],
    [x2,y2],
    [x3,y3],
    [x4,y4]
])
mapcoords = numpy.array([
    [u1,v1],
    [u2,v2],
    [u3,v3],
    [u4,v4]
])


#MATH
    #using affine transform to transform the game coordinates to map coordinates
A= []
u=[]
v=[]
for (x,y),(nx,ny) in zip(gamecoords,mapcoords):
    A.append([x,y,1])
    u.append(nx)
    v.append(ny)
A= numpy.array(A);u= numpy.array(u);v= numpy.array(v)
a,b,c=numpy.linalg.lstsq(A,u,rcond=None)[0]
d,e,f=numpy.linalg.lstsq(A,v,rcond=None)[0]
    #map coordinates to game coordinates for mortaring :>
def Map2Game(_x,_y):
    M = numpy.array([
    [a,b],
    [d,e]
    ])
    uv = numpy.array([
    _x-c,
    _y-f
    ])
    x,y = numpy.linalg.solve(M,uv)
    return float(x),float(y)
def playercoordstomapcoords(pposx,pposy):
    map_xcoord = a*pposx + b*pposy + c
    map_ycoord = d*pposx + e*pposy + f
    return map_xcoord, map_ycoord
mapxc = 0
mapyc = 0

def ce(event,x,y,flags,param):
    if event == cv2.EVENT_MBUTTONDOWN:
        print(Map2Game(x,y))
#picture w,h
sint_w,sint_h =1551,866 
#Main loop
while True:
    #player pos gathering
    result = coordinategrabber.Main()
    if result is None:
        continue
    player_pos_x, player_pos_y = result
    #ppos to map
    mapxc, mapyc = playercoordstomapcoords(player_pos_x,player_pos_y)
    #--
    img = sint.copy()
    cv2.circle(img,(int(mapxc),int(mapyc)),5,(0,0,255),2)
    cv2.namedWindow("sint",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("sint",800,600)
    cv2.setWindowProperty("sint",cv2.WND_PROP_TOPMOST,1)
    cv2.imshow("sint",img)
    cv2.setMouseCallback("sint",ce)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
