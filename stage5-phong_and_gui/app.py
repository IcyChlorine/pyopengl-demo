from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import glm

from camera import Camera
from shader import Shader
from render_data import RenderData
from texture import Texture
import vert_data
from async_gui import AsyncGUI

import time
from matplotlib.colors import hsv_to_rgb
	
class Application:
	def __init__(self, **kwargs):
		# init vaa
		self.frustum = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  # 视景体的left/right/bottom/top/near/far六个面
		self.camera = Camera()
		self.windowSize= [640, 480]							# 保存窗口宽度和高度的变量
		self.fov = 45.										# field of view, 45 by default
		self.mouse = {'left':False, 'right':False, 'pos':[0,0]}	# 鼠标信息

		self.companionGUI = AsyncGUI(self)
		self.hasOptionUpdated = False
		self.optionsUpdated = set()

		# init glut lib
		glutInit()
		displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
		glutInitDisplayMode(displayMode)
	
		# init and create window via GLUT
		glutInitWindowSize(*self.windowSize)
		glutInitWindowPosition(300, 200)
		glutCreateWindow('Quidam Of OpenGL')

		self.initGLParam()							  # 初始化画布
		self.registerRenderFunc()			   # 注册回调函数draw()
		self.registerCallbackFunc()
		
		# init shader and other render resources
		self.texturedShader = Shader(vertShaderFilename = 'vert.glsl', fragShaderFilename = 'frag.glsl')
		self.axesShader = Shader(vertShaderFilename = 'axes.vert.glsl', fragShaderFilename = 'axes.frag.glsl')
		self.lampShader = Shader(vertShaderFilename = 'lamp.vert.glsl', fragShaderFilename = 'lamp.frag.glsl')
		self.phongShader = Shader(vertShaderFilename = 'phong.vert.glsl', fragShaderFilename = 'phong.frag.glsl')
		self.lightPos, self.lightColor = [1.2,1.,2.], [1.,1.,1.]
		self.ambientStrength, self.diffuseStrength, self.specularStrength = 0.1,1.,0.5
		self.specularPow = 64.
		self.hasOptionUpdated = True
		self.optionsUpdated = {
			'viewMat', 'projMat', 
			'lightPos', 'lightColor', 
			'ambientStrength', 'diffuseStrength', 'specularStrength',
			'specularPow'
		}

		#self.triangle = RenderData(vert_data.cube_vert_data_xyz_st, ['xyz','st'])
		self.cube = RenderData(vert_data.cube_vert_data_xyz_nnn, ['xyz','nnn'])
		self.axes = RenderData(vert_data.axes_vert_data, ['xyz','rgb'])
		self.lamp = RenderData(vert_data.cube_vert_data_xyz, ['xyz'])
		
		self.pythonTexture = Texture('assets/texture/python_icon.jfif')
		self.blockTexture = Texture('assets/texture/grass_side.bmp')

		
	def run(self):
		self.companionGUI.start()
		glutMainLoop()   
		
	def initGLParam(self):
		glClearColor(0.2, 0.3, 0.3, 1.0) # 设置画布背景色。注意：这里必须是4个参数
		glEnable(GL_DEPTH_TEST)		  # 开启深度测试，实现遮挡关系
		glDepthFunc(GL_LEQUAL)		   # 设置深度测试函数（GL_LEQUAL只是选项之一）
	
	def mainLoop(self):
		# update options, LAZILY
		self.updateOptions()
		# RENDER!
		self.render()

		
	def updateOptions(self):
		# update options, LAZILY
		if self.hasOptionUpdated:
			if 'renderSkeleton' in self.optionsUpdated:
				if self.renderSkeleton:
					glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
				else:
					glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
				self.optionsUpdated.discard('renderSkeleton')
			if 'camera' in self.optionsUpdated or 'viewMat' in self.optionsUpdated:
				# supposed to be all shaders
				self.axesShader.setUniform('view', self.camera.viewMat)
				self.lampShader.setUniform('view', self.camera.viewMat)
				self.phongShader.setUniform('view', self.camera.viewMat)
				self.optionsUpdated.discard('cameraPos')
				self.optionsUpdated.discard('viewMat')
			if 'projMat' in self.optionsUpdated or 'proj' in self.optionsUpdated or 'fov' in self.optionsUpdated:
				projMat = glm.perspective(
					glm.radians(self.fov), 
					self.windowSize[0]/self.windowSize[1],
					0.1, 100.
				)
				self.axesShader.setUniform('proj', projMat)
				self.lampShader.setUniform('proj', projMat)
				self.phongShader.setUniform('proj', projMat)
				self.optionsUpdated.discard('proj')
				self.optionsUpdated.discard('projMat')
				self.optionsUpdated.discard('fov')
			
			if 'lightPos' in self.optionsUpdated:
				#self.lampShader.setUniform('lightPos', self.lightPos)
				modelMat = glm.mat4(1.)
				modelMat = glm.translate(modelMat, self.lightPos)
				modelMat = glm.scale(modelMat, glm.vec3(0.2))
				self.lampShader.setUniform('model', modelMat)
				self.phongShader.setUniform('lightPos', self.lightPos)
				self.optionsUpdated.discard('lightPos')
			if 'lightColor' in self.optionsUpdated:
				self.lampShader.setUniform('lightColor', self.lightColor)
				self.phongShader.setUniform('lightColor', self.lightColor)
				self.optionsUpdated.discard('lightColor')
			if 'ambientStrength' in self.optionsUpdated:
				self.phongShader.setUniform('ambientStrength', self.ambientStrength)
				self.optionsUpdated.discard('ambientStrength')
			if 'diffuseStrength' in self.optionsUpdated:
				self.phongShader.setUniform('diffuseStrength', self.diffuseStrength)
				self.optionsUpdated.discard('diffuseStrength')
			if 'specularStrength' in self.optionsUpdated:
				self.phongShader.setUniform('specularStrength', self.specularStrength)
				self.optionsUpdated.discard('specularStrength')
			if 'specularPow' in self.optionsUpdated:
				self.phongShader.setUniform('specularPow', self.specularPow)
				self.optionsUpdated.discard('specularPow')
			self.hasOptionUpdated = False
	def render(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		#self.texturedShader.setUniform('uniColor',color)
		#self.texturedShader.setTexture('texture1',self.blockTexture)
		#self.texturedShader.setTexture('texture2',self.pythonTexture)

		
		viewMat = self.camera.viewMat
		modelMat = glm.mat4(1.)
		#viewMat = np.array(viewMat)
		
		#projMat = np.array(projMat)

		'''self.texturedShader.setUniform('view',viewMat)
		self.texturedShader.setUniform('model',modelMat)
		self.texturedShader.setUniform('proj',projMat)
		self.texturedShader.render(self.triangle)
		光源位置，光源颜色
		环境，漫射，镜面强度
		镜面index
		'''

		self.axesShader.setUniform('model',modelMat)
		self.axesShader.render(self.axes, GL_LINES)

		#self.lampShader.setUniform('model',modelMat)
		#self.lampShader.setUniform('objectColor', [1.,0.5,0.31])
		#self.lampShader.setUniform('lightColor', [1.,1.,1.])
		#self.lampShader.render(self.lamp)

		# second lamp
		
		self.lampShader.setUniform('objectColor', [1.,1.,1.])
		#self.lampShader.setUniform('lightColor', [1.,1.,1.])
		self.lampShader.render(self.lamp)
		

		modelMat = glm.mat4(1.)
		self.phongShader.setUniform('model',modelMat)
		self.phongShader.setUniform('objectColor', [1.,0.5,0.31])
		self.phongShader.setUniform('cameraPos', self.camera.cameraPos)
		self.phongShader.render(self.cube)

		glutSwapBuffers()
		glutPostRedisplay()
	def registerRenderFunc(self):
		glutDisplayFunc(self.mainLoop)

	def registerCallbackFunc(self):
		def onReshape(width, height):
			self.windowSize = [width, height]
			glViewport(0,0,width,height)
			glutPostRedisplay()
			self.hasOptionUpdated = True
			self.optionsUpdated.add('proj')
		
		def onMouseClick(button, state, x, y):
			self.mouse['pos'] = [ x, y ]# crucial! as glut wont call onMouseMove when not clicked(seems to)
			if button == GLUT_LEFT_BUTTON:
				self.mouse['left'] = state==GLUT_DOWN
			if button == GLUT_RIGHT_BUTTON:
				self.mouse['right'] = state==GLUT_DOWN
		
		def onMouseMove(x, y):
			mouse = self.mouse
			windowSize = self.windowSize
			
			if mouse['left']:
				#print('mouse click')
				Δx = mouse['pos'][0] - x
				Δy = mouse['pos'][1] - y
				mouse['pos'] = [x, y]

				Δθ = 2*np.pi * Δy/windowSize[1]
				Δφ = 2*np.pi * Δx/windowSize[0]

				self.camera.modifyPosture(Δθ,Δφ)

				self.hasOptionUpdated = True
				self.optionsUpdated.add('camera')

				glutPostRedisplay()
			
		self.renderSkeleton = False
		def onKeyDown(key, x, y):
			if key == b'l' or key == b'L': #渲染线框
				self.renderSkeleton = not self.renderSkeleton
				if self.renderSkeleton:
					glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
				else:
					glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

				glutPostRedisplay()
			
		def onMouseWheel(button, dir, x, y):
			if dir>0: # 向前滚轮，视点前进
				self.camera.scale(0.9)
				glutPostRedisplay()
			else: #视点后退
				self.camera.scale(1.1)
				glutPostRedisplay()
			self.hasOptionUpdated = True
			self.optionsUpdated.add('proj')
		glutReshapeFunc(onReshape)			# 注册响应窗口改变的函数reshape()
		glutMouseFunc(onMouseClick)			# 注册响应鼠标点击的函数mouseclick()
		glutMotionFunc(onMouseMove)			# 注册响应鼠标拖拽的函数mousemotion()
		glutKeyboardFunc(onKeyDown)			# 注册键盘输入的函数keydown()
		glutMouseWheelFunc(onMouseWheel)	# 鼠标滚轮缩放函数

	def setOptionAsync(self, optionName, optionValue):	# maybe called asynchronously
		# option 真正的变化会被postpone至主线程中
		self.hasOptionUpdated = True
		self.optionsUpdated.add(optionName)
		setattr(self, optionName, optionValue)