#w = 18 times (slightly cut off), h = 15 (64 by 64)
from scene import *
from levels import level1Str, level2Str
import math
playerWalkCycle = ['plf:AlienBeige_walk1', 'plf:AlienBeige_walk2']

def clear(which):
	for i in which:
		i.run_action(Action.remove())
			
class playerAtts():
	def __init__(self):
		self.vel = 4
		
class game(Scene):
	def setup(self):
		self.player = SpriteNode('plf:AlienBeige_stand', z_position = 3, parent = self)
		self.player.position = (128, 400)
		self.atts = playerAtts()
		self.player.anchor_point = (0,0)
		self.groundNode = Node(parent = self, z_position = 2)
		self.baddiesNode = Node(parent = self, z_position = 2)
		self.backgroundNode = Node(parent = self, z_position = 0)
		self.createButtons()
		self.createLevel(level1Str)
		self.onGround = False
		self.playerHitBox = Rect(self.player.position.x + 6, self.player.position.y, 52, 128)
		self.acceleration = 0
		self.jumpIndex = 0
		self.canJump = True
		self.canMoveRight = True
		self.nearWallRight = Rect(0,0,0,0)
		self.canMoveLeft = True
		self.nearWallLeft = Rect(0,0,0,0)
		self.currentlyJumping = False
		self.moveIndex = 0
		self.isMoving = False
		self.jumpMoving = False
		self.currentLevel = 1
		self.health = 3
		self.healthNode = Node(parent = self, z_position = 3)
		
		for i in range(self.health):
			self.healthPic = SpriteNode('plf:HudHeart_full', position = (50 + (i)*50, 800), parent = self.healthNode, z_position = i)
			
	def update(self):
		self.playerHitBox = Rect(self.player.position.x + 6, self.player.position.y, 52, 128)
		self.checkCollision()
		self.playerHitBox = Rect(self.player.position.x + 6, self.player.position.y, 52, 128)
		self.checkPlayerMovement()
		if self.player.position.y < 0:
			self.player.position = (128, 400)
		if self.player.position.x > self.size.w + 10:
			self.nextLevel()
			
	def playerDead(self):
		self.health -= .5
		if self.health < 1:
			clear(self.groundNode.children)
			clear(self.backgroundNode.children)
			clear(self.baddiesNode.children)
			clear(self.healthNode.children)
			clear(self.jumpBImg.children)
			clear(self.rightBImg.children)
			clear(self.leftBImg.children)
			self.player.run_action(Action.remove())
			self.lose = loss()
			self.present_modal_scene(self.lose)
		else:
			for i in self.healthNode.children:
				if self.health == 2:
					if i.z_position == 2:
						i.texture = Texture('plf:HudHeart_empty')
				elif self.health == 1:
					if i.z_position == 1:
						i.texture = Texture('plf:HudHeart_empty')
				
				
	def resetGameAtts(self):
		self.acceleration = 0
		self.jumpIndex = 0
		self.canJump = True
		self.canMoveRight = True
		self.nearWallRight = Rect(0,0,0,0)
		self.canMoveLeft = True
		self.nearWallLeft = Rect(0,0,0,0)
		self.currentlyJumping = False
		self.onGround = False
		self.player.position = (128, 400)
		
		
	def nextLevel(self):
		self.currentLevel += 1
		self.resetGameAtts()
		if self.currentLevel == 2:
			self.createLevel(level2Str)
		else:
			clear(self.groundNode.children)
			clear(self.backgroundNode.children)
			clear(self.baddiesNode.children)
			clear(self.healthNode.children)
			clear(self.jumpBImg.children)
			clear(self.rightBImg.children)
			clear(self.leftBImg.children)
			self.player.run_action(Action.remove())
			self.win = win()
			self.present_modal_scene(self.win)
			
	def checkPlayerMovement(self):
		self.isMoving = False
		if self.jumpPressed == True and self.canJump == True:
			self.currentlyJumping = True
				
		if self.jumpPressed == False and self.acceleration == 0 and self.currentlyJumping == False:
			self.canJump = True
		else:
			self.canJump = False	
							
		if self.currentlyJumping == True:
			self.jumpMoving = True
			self.player.texture = Texture('plf:AlienBeige_jump')
			self.jumpIndex += 1
			self.acceleration = -.3
			self.player.position = (self.player.position.x, self.player.position.y + (21 - self.jumpIndex))
			if self.jumpIndex == 20:
				self.jumpIndex = 0
				self.currentlyJumping = False
				
		if self.rightPressed == True and self.canMoveRight == True:
			self.isMoving = True
			self.player.position = (self.player.position.x + self.atts.vel, self.player.position.y)
			self.player.rotation = 0
			self.moveIndex += 1
			if self.jumpMoving == False:
				if self.moveIndex < 10:
					self.player.texture = Texture('plf:AlienBeige_walk1')
				elif self.moveIndex < 20:
					self.player.texture = Texture('plf:AlienBeige_walk2')
				else:
					self.moveIndex = 0
				
		if self.player.position.x > 0:	
			if self.leftPressed == True and self.canMoveLeft == True:
				self.isMoving = True
				self.player.position = (self.player.position.x - self.atts.vel, self.player.position.y)
				self.moveIndex += 1
				self.player.rotation = 0
				if self.jumpMoving == False:
					if self.moveIndex < 10:
						self.player.texture = Texture('plf:AlienBeige_walk1')
					elif self.moveIndex < 20:
						self.player.texture = Texture('plf:AlienBeige_walk2')
					else:
						self.moveIndex = 0
					
		if self.isMoving == False and self.jumpMoving == False:
			self.player.texture = Texture('plf:AlienBeige_stand')
		
	def checkCollision(self):
		index = 0
		for i in self.groundNode.children:
			tileRect = Rect(i.bbox.x, i.bbox.y, i.bbox.w - 1, i.bbox.h - 1)
			down = tileRect.intersection(self.playerHitBox)
			if down.h != 0:
				index += 1
				self.acceleration = 0
				self.player.position = (self.player.position.x, self.player.position.y + down.h - 1)
						
			right = tileRect.intersection(Rect(self.playerHitBox.x + self.atts.vel + 1, self.playerHitBox.y + 2, self.playerHitBox.w, self.playerHitBox.h))
			if self.canMoveRight == True:
				if right.w != 0:
					self.canMoveRight = False
					self.nearWallRight = tileRect
			else:
				right = self.nearWallRight.intersection(Rect(self.playerHitBox.x + self.atts.vel + 1, self.playerHitBox.y + 2, self.playerHitBox.w, self.playerHitBox.h))
				if right.w != 0:
					self.canMoveRight = False
				else:
					self.canMoveRight = True
			
			left = tileRect.intersection(Rect(self.playerHitBox.x - self.atts.vel - 1, self.playerHitBox.y + 2, self.playerHitBox.w, self.playerHitBox.h))
			if self.canMoveLeft == True:
				if left.w != 0:
					self.canMoveLeft = False
					self.nearWallLeft = tileRect
			else:
				left = self.nearWallLeft.intersection(Rect(self.playerHitBox.x - self.atts.vel - 1, self.playerHitBox.y + 2, self.playerHitBox.w, self.playerHitBox.h))
				if left.w != 0:
					self.canMoveLeft = False
				else:
					self.canMoveLeft = True
		
		if index == 0:
			self.acceleration += .3
			for i in self.groundNode.children:
				yateus = Rect(i.bbox.x, i.bbox.y, i.bbox.w - 1, i.bbox.h - 1)
				poopys = yateus.intersection(Rect(self.playerHitBox.x, self.playerHitBox.y - self.acceleration, self.playerHitBox.w, self.playerHitBox.h))
				if poopys.h != 0:
					index += 1
					downAmount = self.acceleration - poopys.h + 1
					break
			if index == 0:
				self.player.position = (self.player.position.x, self.player.position.y - self.acceleration)
			else:
				self.player.position = (self.player.position.x, self.player.position.y - downAmount)
				self.jumpMoving = False
		
		for i in self.baddiesNode.children:
			if i.z_position == -1:
				baddieRect = Rect(i.bbox.x, i.bbox.y, i.bbox.w - 1, i.bbox.h - 33)
			else:
				baddieRect = Rect(i.bbox.x, i.bbox.y, i.bbox.w - 1, i.bbox.h - 10)
			hit = baddieRect.intersection(self.playerHitBox)
			if hit.h != 0:
				self.player.position = (128, 400)
				self.playerDead()
				
																																																							
	def createButtons(self):
		#right button
		self.rightHitBox = Rect(130, 30, 105, 105)
		self.rightBImg2 = SpriteNode('iob:pinpoint_256', position = (192, 60), parent = self, z_position = 3, scale = 0.4, alpha = 0.5)
		self.rightBImg = SpriteNode('iob:arrow_down_b_256', position = (0, 0), parent = self.rightBImg2, scale = 0.7)
		self.rightBImg.rotation = 1.5708
		
		#left button
		self.leftHitBox = Rect(8, 30, 105, 105)
		self.leftBImg2 = SpriteNode('iob:pinpoint_256', position = (70, 60), parent = self, z_position = 3, scale = 0.4, alpha = 0.5)
		self.leftBImg = SpriteNode('iob:arrow_down_b_256', position = (0, 0), parent = self.leftBImg2, scale = 0.7)
		self.leftBImg.rotation = -1.5708
	
		#jump button
		self.jumpHitBox = Rect(978, 30, 105, 105)
		self.jumpBImg2 = SpriteNode('iob:pinpoint_256', position = (1050, 60), parent = self, z_position = 3, scale = 0.4, alpha = 0.5)
		self.jumpBImg = SpriteNode('iob:arrow_down_b_256', position = (0, 0), parent = self.jumpBImg2, scale = 0.7)
		self.jumpBImg.rotation = 3.1416
		
		self.rightPressed = False
		self.leftPressed = False
		self.jumpPressed = False
		
	def touch_began(self, touch):
		if self.rightHitBox.contains_point(touch.location):
			self.rightBImg.position = (25, 0)
			self.rightPressed = True
		elif self.leftHitBox.contains_point(touch.location):
			self.leftBImg.position = (-25, 0)
			self.leftPressed = True
		elif self.jumpHitBox.contains_point(touch.location):
			self.jumpBImg.position = (0, 25)
			self.jumpPressed = True
	
	def touch_moved(self, touch):
			if self.rightHitBox.contains_point(touch.prev_location) == True and self.rightHitBox.contains_point(touch.location) == False:
				self.rightBImg.position = (0,0)
				self.rightPressed = False
			elif self.rightHitBox.contains_point(touch.location) == True and self.rightHitBox.contains_point(touch.prev_location) == False:
				self.rightBImg.position = (25, 0)
				self.rightPressed = True
			
			if self.leftHitBox.contains_point(touch.prev_location) == True and self.leftHitBox.contains_point(touch.location) == False:
				self.leftBImg.position = (0,0)
				self.leftPressed = False
			elif self.leftHitBox.contains_point(touch.location) == True and self.leftHitBox.contains_point(touch.prev_location) == False:
				self.leftBImg.position = (-25, 0)
				self.leftPressed = True
			
			if self.jumpHitBox.contains_point(touch.prev_location) == True and self.jumpHitBox.contains_point(touch.location) == False:
				self.jumpBImg.position = (0,0)
				self.jumpPressed = False
			elif self.jumpHitBox.contains_point(touch.location) == True and self.jumpHitBox.contains_point(touch.prev_location) == False:
				self.jumpBImg.position = (0, 25)
				self.jumpPressed = True
	
	def touch_ended(self, touch):
		if self.rightHitBox.contains_point(touch.prev_location):
			self.rightBImg.position = (0, 0)
			self.rightPressed = False
		elif self.leftHitBox.contains_point(touch.prev_location):
			self.leftBImg.position = (0, 0)
			self.leftPressed = False
		elif self.jumpHitBox.contains_point(touch.prev_location):
			self.jumpBImg.position = (0, 0)
			self.jumpPressed = False
	
	def read(self, lvl, which):
		x = 0
		y = 15
		for i in lvl[which]:
			if which == 0:
				if i == "|":
					y -= 1
					x = 0
				elif i == "G":
					tile = SpriteNode('plf:Ground_SandMid', parent = self.groundNode, position = (x*64+32, y*64-32))
					x += 1
				elif i == "H":
					tile = SpriteNode('plf:Ground_SandCenter', parent = self.groundNode, position = (x*64 + 32, y*64 - 32))
					x += 1
				else:
					x += 1
					
			elif which == 1:
				if i == "|":
					y -= 1
					x = 0
				elif i == "S":
					baddie = SpriteNode('plf:Tile_Spikes', parent = self.baddiesNode, position = (x*64 + 32, y*64 - 32), z_position = -1)
					x += 1
				elif i == "L":
					baddie = SpriteNode('plf:Tile_LavaTop_low', parent = self.baddiesNode, position = (x*64 + 32, y*64 - 32), z_position = -1)
					x += 1
				elif i == "K":
					baddie = SpriteNode('plf:Tile_Lava', parent = self.baddiesNode, position = (x*64 + 32, y*64 - 32))
					x += 1
				else:
					x += 1
	def createLevel(self, lvl):
		clear(self.groundNode.children)
		clear(self.backgroundNode.children)
		clear(self.baddiesNode.children)
		self.background = SpriteNode(lvl[2], position = (self.size.w/2, self.size.h/2-50), scale = 2.2, parent = self.backgroundNode, alpha = 0.7)
		
		self.read(lvl, 0)
		self.read(lvl, 1)

class win(Scene):
	def setup(self):
		self.background_color = '#282828'
		self.text = LabelNode("You Win", position = (self.size.w/2, self.size.h/2), parent = self)

class loss(Scene):
	def setup(self):
		self.background_color = '#930a0a'
		self.text = LabelNode("You Lose", position = (self.size.w/2, self.size.h/2), parent = self)
run(game(), show_fps = True)	
