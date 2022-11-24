import pygame as pg
import sys
from random import randint as ri
#surface
pg.init()
sf=pg.display.set_mode()
sfrect=sf.get_rect()
#classes


class Box:
	global sf,sfrect
	def __init__(self,w,h):
		self.rect=pg.Rect(sfrect.left+100,sfrect.bottom*5/6-100,w,h)
		self.spdr=spdr
		self.jumpb=False
		self.spd=spd
	def draw(self,color):
		pg.draw.rect(sf,color,self.rect)
	def jump(self):
		self.rect.y-=self.spdr
		self.spdr-=self.spd
		if self.rect.y>sfrect.bottom*5/6-100:
			self.rect.y=sfrect.bottom*5/6-100
			self.jumpb=False
			self.spdr=spdr
	def stop(self):
		self.spd=0
		self.spdr=0
		
		
class Enemy:
		global sf,sfrect
		def __init__(self,x):
			self.rect=pg.Rect(0,0,ri(20,100),ri(20,200))
			self.rect.centerx=x
			self.espd=espd
			self.rect.bottom=sfrect.bottom*5/6
		def draw(self,color):
			pg.draw.rect(sf,color,self.rect)
		def emove(self):
			self.rect.x-=self.espd
		def estop(self):
			self.espd=0
			
			
#variables
bgcolor=(250,245,200)
scolor=(0,0,0)
hiscolor=(20,45,90)
linecolor=(0,0,0)
lcin=(0,sfrect.height*5/6)
lcfi=(sfrect.width,sfrect.height*5/6)
jump=False
clk=pg.time.Clock()
n=1000
enenum=6
espd=10
spdr=50
spd=3
score=0
out=False
start=False

#hiscore system
with open('hiscore.txt','r') as hifile:
	hisc=hifile.read()
	
#text fonts
outfont=pg.font.SysFont('Arial',128)
startfont=pg.font.SysFont('Arial',200)
scorefont=pg.font.SysFont('Arial',72)
#scorelabel=scorefont.render(f'HI-SCORE={score}',1,(200,200,255))

#game objects
startbox=Box(610,200)
startbox.rect.x=50
startbox.rect.y=700
jumper=Box(100,100)
enebox=[]

def addene(enenum,enebox,n):
	for i in range(enenum):
		enebox.append(Enemy(n))
		n+=ri(600,1000)
addene(enenum,enebox,n)

#game loop
while True:
	hislabel=scorefont.render(f'HI-SCORE={hisc}',1,hiscolor)
	for ev in pg.event.get():
		if ev.type==pg.QUIT:
			sys.exit()
		if ev.type==pg.MOUSEBUTTONDOWN:
			if startbox.rect.collidepoint(ev.pos):
				start=True
	if start:
		break
	sf.fill((200,235,255))
	sf.blit(hislabel,(10,0))
	startlabel=startfont.render('START',1,(20,180,250))
	startbox.draw((80,250,180))
	sf.blit(startlabel,(50,690))
	pg.display.flip()
				
while True:
	for ev in pg.event.get():
		if ev.type==pg.QUIT:
			sys.exit()
		if ev.type==pg.MOUSEBUTTONDOWN:
			jumper.jumpb=True
	if jumper.jumpb:
		jumper.jump()
	sf.fill(bgcolor)
	jumper.draw((0,100,150))
	for i in enebox:
		i.emove()
		i.draw((0,0,0))	
		if i.rect.right<sfrect.left:
			enebox.remove(i)
			score+=1
		if len(enebox)==0:
			addene(enenum,enebox,n)
			espd+=espd*0.10
			bgcolor=(ri(200,255),ri(200,255),ri(200,255))
		if (i.rect.top<jumper.rect.bottom and
		i.rect.left<jumper.rect.right and
		i.rect.right>jumper.rect.left):
			out=True
			spd=0
			spdr=0
		if  score>int(hisc):
			with open('hiscore.txt','w') as hifile:
				hifile.write(str(score))
		scorelabel=scorefont.render(f'SCORE={score}',1,scolor)
		hisclabel=scorefont.render(f'HI-SCORE={hisc}',1,hiscolor)
	if out:
		outlabel=outfont.render('Game Over',1,(200,0,0))
		sf.blit(outlabel,(50,300))
		jumper.stop()
		for i in enebox:
			i.estop()
	sf.blit(scorelabel,(100,100))
	sf.blit(hisclabel,(10,0))
	pg.draw.line(sf,linecolor,lcin,lcfi,3)
	clk.tick(60)
	pg.display.flip()
