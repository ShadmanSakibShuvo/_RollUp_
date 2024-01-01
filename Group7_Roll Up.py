from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random,math

pSpeed,pL,pR,oL1,oR1,oL2,oR2,bLLp,bLRp,bRLp,bRRp,R,bLL,bLR,bRL,bRR,timer,exit,score,pause=0.5,0,0,[],[],[],[],[590,200],[650,200],[1260,200],[1330,200],10,True,False,False,False,1000,False,0,False





#platforms(using midpoint line)
def platforms(x1,y1,x2,y2,width):
    glColor3f(1.0,1.0, 0.0)
    dx=abs(x2-x1)
    dy=abs(y2-y1)
    if x1<x2:
        sx=1
    else:
        sx=-1
    if y1<y2:
        sy=1
    else:
        sy=-1
    err=dx-dy
    while True:
        glPointSize(width)
        glBegin(GL_POINTS)
        glVertex2f(x1, y1)
        glEnd()
        if x1==x2 and y1==y2:
            break
        e2=2*err
        if e2>-dy:
            err=err-dy
            x1=x1+sx
        if x1==x2 and y1==y2:
            glBegin(GL_POINTS)
            glVertex2f(x1, y1)
            glEnd()
            break
        if e2<dx:
            err=err+dx
            y1=y1+sy

def plot(x,y):
    glColor3f(1.0,1.0, 0.0)
    glVertex2f(x,y)

def updatePlatform(v):
    global pL,pR,score,pause,pSpeed
    if not pause:
        pL+=pSpeed
        pR+=pSpeed
        if pL>50:
            pL=0
            score+=1
        if pR>50:
            pR=0
            score+=1
        if score%100==0:
            pSpeed+=0.1
        glutPostRedisplay()
        glutTimerFunc(16,updatePlatform,0)






#Obstacles
def drawos(x,y,size):
    glBegin(GL_TRIANGLES)
    for i in range(100):
        angle = 2.0 * math.pi * i / 5
        x_i = x + size * 0.5 * math.cos(angle)
        y_i = y + size * 0.5 * math.sin(angle)
        glVertex2f(x_i, y_i)

        angle_next = 2.0 * math.pi * (i + 2) / 5
        x_next = x + size * 0.2 * math.cos(angle_next)
        y_next = y + size * 0.2 * math.sin(angle_next)
        glVertex2f(x_next, y_next)
    glEnd()

def oGenerate(v):
    global oL1, oR1, oL2, oR2, pause
    if not pause:
        if not oL1 or oL1[-1][1]<0:
            oL1.append((random.uniform(588,588),random.uniform(1080,1080+1080)))
        if not oL2 or oL2[-1][1]<0:
            oL2.append((random.uniform(653,653),random.uniform(1080,1080+1080)))

        if not oR1 or oR1[-1][1]<0:
            oR1.append((random.uniform(1265,1265),random.uniform(1080,1080+1080)))
        if not oR2 or oR2[-1][1]<0:
            oR2.append((random.uniform(1330,1330),random.uniform(1080,1080+1080)))
        glutTimerFunc(timer,oGenerate,0)

def updateos():
    global oL1,oR1,oL2,oR2,pause
    if not pause:
        oL1=[(x,y-pSpeed) for x,y in oL1]
        oR1=[(x,y-pSpeed) for x,y in oR1]

        oL1=[o for o in oL1 if o[1]>0]
        oR1=[o for o in oR1 if o[1]>0]

        oL2=[(x,y-pSpeed) for x,y in oL2]
        oR2=[(x,y-pSpeed) for x,y in oR2]

        oL2=[o for o in oL2 if o[1]>0]
        oR2=[o for o in oR2 if o[1]>0]

def draw_os():
    while (True):
        for o in oL1:
            drawos(o[0],o[1],20)
        for o in oR1:
            drawos(o[0],o[1],20)
        for o in oL2:
            drawos(o[0],o[1],20)
        for o in oR2:
            drawos(o[0],o[1],20)
        break






#Player's controllable ball(using midpoint circle)
def ball(x,y,r,n=100):
    x=x+2
    glBegin(GL_POLYGON)
    for i in range(n):
        theta = (i / n) * (2 * math.pi)
        x_i = x + r * math.cos(theta)+5
        y_i = y + r * math.sin(theta)
        glVertex2f(x_i, y_i)
    glEnd()

    r+=1
    glColor3f(0.8,0,1)
    x_c,y_c=x+5,y
    x,y,P=r,0,1-r
    glBegin(GL_POINTS)
    glVertex2f(x_c+x,y_c-y)
    glVertex2f(x_c-x,y_c-y)
    glVertex2f(x_c+x,y_c+y)
    glVertex2f(x_c-x,y_c+y)
    while x>y:
        y+=1
        if P<=0:
            P=P+2*y+1
        else:
            x-=1
            P=P+2*y-2*x+1
        if x<y:
            break
        glVertex2f(x_c+x,y_c-y)
        glVertex2f(x_c-x,y_c-y)
        glVertex2f(x_c+x,y_c+y)
        glVertex2f(x_c-x,y_c+y)
        if x!=y:
            glVertex2f(x_c+y,y_c-x)
            glVertex2f(x_c-y,y_c-x)
            glVertex2f(x_c+y,y_c+x)
            glVertex2f(x_c-y,y_c+x)
    glEnd()

def special_keys(key,x,y):
    global bLR,bRL,bLRp,bRLp,bLL,bRR,bLLp,bRRp,pause,exit

    if key==GLUT_KEY_RIGHT:
        if bLL and not bLR and not bRL and not bRR:
            bLL= False
            bLR= True
            bRL = False
            bRR = False
        elif not bLL and bLR and not bRL and not bRR:
            bLL= False
            bLR= False
            bRL = True
            bRR = False
        elif not bLL and not bLR and bRL and not bRR:
            bLL= False
            bLR= False
            bRL = False
            bRR = True
        elif not bLL and not bLR and not bRL and bRR:
            bLL= True
            bLR= False
            bRL = False
            bRR = False

    if key==GLUT_KEY_LEFT:
        if not bLL and not bLR and not bRL and bRR:
            bLL= False
            bLR= False
            bRL = True
            bRR = False
        elif not bLL and not bLR and bRL and not bRR:
            bLL= False
            bLR= True
            bRL = False
            bRR = False
        elif not bLL and bLR and not bRL and not bRR:
            bLL= True
            bLR= False
            bRL = False
            bRR = False
        elif bLL and not bLR and not bRL and not bRR:
            bLL= False
            bLR= False
            bRL = False
            bRR = True

    if key==GLUT_KEY_UP:
        print(f"You left the game! Your score: {score}")
        glutLeaveMainLoop()
    if key==GLUT_KEY_DOWN:
        pause=not pause









#Collision check
def collision(b,os):
    for o in os:
        distance=math.sqrt((b[0]-o[0])**2+(b[1]-o[1])**2)
        if distance<R+20:
            return True
    return False









def init():
    glClearColor(0.38,0.7,0.98,1.0)  #bg color
    gluOrtho2D(0,1920,0,1080)

def Display():
    global pause,exit,score
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0,0.0,0.0)

    glColor3f(1,0.66,0.21)
    glBegin(GL_TRIANGLES)
    for y in range(1130,0,-50):
        glVertex2f(640,y-pL)
        glVertex2f(640,y-50-pL)
        glVertex2f(600,y-25-pL)
    glEnd()

    glColor3f(1,0.66,0.21)
    glBegin(GL_TRIANGLES)
    for y in range(1130,0,-50):
        glVertex2f(1280,y-pR)
        glVertex2f(1280,y-50-pR)
        glVertex2f(1320,y-25-pR)
    glEnd()

    glColor3f(1.0,1.0,0.0)
    platforms(640,1080,640,0,10)
    platforms(600,1080,600,0,4)
    glColor3f(0.0,0.0,0.0)
    platforms(603,1080,603,0,2)

    glColor3f(1.0,1.0,0.0)
    platforms(1280,0,1280,1080,10)
    platforms(1320,0,1320,1080,4)
    glColor3f(0.0,0.0,0.0)
    platforms(1317,1080,1317,0,2)

    glColor3f(0.0,0.0,1.0)
    if not exit:
            glColor3f(0.0,0.0,1.0)
            if bLR:
                ball(bLRp[0],bLRp[1],R)
                if collision(bLRp,oL1+oR1+oL2+oR2):
                    print(f"Game Over! Your score: {score}")
                    glutLeaveMainLoop()
            elif bLL:
                ball(bLLp[0]-11,bRRp[1],R)
                if collision(bLLp,oL1+oR1+oL2+oR2):
                    print(f"Game Over! Your score: {score}")
                    glutLeaveMainLoop()
            elif bRL:
                ball(bRLp[0]-4,bRLp[1],R)
                if collision(bRLp,oL1+oR1+oL2+oR2):
                    print(f"Game Over! Your score: {score}")
                    glutLeaveMainLoop()
            else:
                ball(bRRp[0]-1,bLLp[1],R)
                if collision(bRRp,oL1+oR1+oL2+oR2):
                    print(f"Game Over! Your score: {score}")
                    glutLeaveMainLoop()

            updateos()
            glColor3f(random.random(),0,0)
            draw_os()

    glutSwapBuffers()




def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1920,1080)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b'ROLL UP')

    init()
    glutDisplayFunc(Display)
    glutTimerFunc(0, updatePlatform,0)
    glutTimerFunc(0, oGenerate,0)
    oGenerate(0)
    glutSpecialFunc(special_keys)

    glutMainLoop()

if __name__ == "__main__":
    main()