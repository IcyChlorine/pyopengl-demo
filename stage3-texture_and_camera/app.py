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

import time
from matplotlib.colors import hsv_to_rgb
	
class Application:
	def __init__(self, **kwargs):
		# init vaa
		self.isPerspective = True							   # 透视投影
		self.frustum = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  # 视景体的left/right/bottom/top/near/far六个面
		self.camera = Camera()
		self.windowSize= [640, 480]							 # 保存窗口宽度和高度的变量
		self.mouse = {'left':False, 'right':False, 'pos':[0,0]}	# 鼠标信息

		# init gl lib
		glutInit()
		displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
		glutInitDisplayMode(displayMode)
	
		glutInitWindowSize(*self.windowSize)
		glutInitWindowPosition(300, 200)
		glutCreateWindow('Quidam Of OpenGL')

		self.initGLParam()							  # 初始化画布
		self.registerRenderFunc()			   # 注册回调函数draw()
		self.registerCallbackFunc()
		
		self.texturedShader = Shader(vertShaderFilename = 'vert.glsl', fragShaderFilename = 'frag.glsl')
		self.axesShader = Shader(vertShaderFilename = 'axes-vert.glsl', fragShaderFilename = 'axes-frag.glsl')
		
		self.triangle = RenderData(vert_data.cube_vert_data, ['xyz','st'])
		self.axes = RenderData(vert_data.axes_vert_data, ['xyz','rgb'])
		
		self.pythonTexture = Texture('assets/texture/python_icon.jfif')
		self.blockTexture = Texture('assets/texture/grass_side.bmp')
	def run(self):
		glutMainLoop()   
		
	def initGLParam(self):
		glClearColor(0.2, 0.3, 0.3, 1.0) # 设置画布背景色。注意：这里必须是4个参数
		glEnable(GL_DEPTH_TEST)		  # 开启深度测试，实现遮挡关系
		glDepthFunc(GL_LEQUAL)		   # 设置深度测试函数（GL_LEQUAL只是选项之一）
	
	def registerRenderFunc(self):
		def mainLoop():
			#glUseProgram(self.naiveShader)
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

			t,T = time.time(), 5.
			h, s, v= (t % T / T) , 1, 1
			color = hsv_to_rgb([h,s,v])
			color = np.append(color, [1.])

			#print(color)
			self.texturedShader.setUniform('uniColor',color)
			self.texturedShader.setTexture('texture1',self.blockTexture)
			self.texturedShader.setTexture('texture2',self.pythonTexture)

			projMat = glm.perspective(
				glm.radians(45.), 
				self.windowSize[0]/self.windowSize[1],
				0.1, 100.
			)
			viewMat = self.camera.viewMat
			#print(viewMat)
			modelMat = glm.mat4(1.)
			modelMat = glm.translate(
				modelMat, 
				glm.vec3(0.,0.,0.)
			)

			#viewMat = np.array(viewMat)
			modelMat = np.array(modelMat)
			projMat = np.array(projMat)

			self.texturedShader.setUniform('view',viewMat)
			self.texturedShader.setUniform('model',modelMat)
			self.texturedShader.setUniform('proj',projMat)
			self.texturedShader.render(self.triangle)

			self.axesShader.setUniform('view',viewMat)
			self.axesShader.setUniform('model',modelMat)
			self.axesShader.setUniform('proj',projMat)
			self.axesShader.render(self.axes, GL_LINES)
			
			glutSwapBuffers()
			glutPostRedisplay()
		glutDisplayFunc(mainLoop)


	def registerCallbackFunc(self):
		def onReshape(width, height):
			self.windowSize = [width, height]
			glViewport(0,0,width,height)
			glutPostRedisplay()
		
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
				print('mouse click')
				Δx = mouse['pos'][0] - x
				Δy = mouse['pos'][1] - y
				mouse['pos'] = [x, y]

				Δθ = 2*np.pi * Δy/windowSize[1]
				Δφ = 2*np.pi * Δx/windowSize[0]

				self.camera.modifyPosture(Δθ,Δφ)

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
				self.camera.scale(1.1)
				glutPostRedisplay()
			else: #视点后退
				self.camera.scale(0.9)
				glutPostRedisplay()
		glutReshapeFunc(onReshape)			# 注册响应窗口改变的函数reshape()
		glutMouseFunc(onMouseClick)		   # 注册响应鼠标点击的函数mouseclick()
		glutMotionFunc(onMouseMove)		 # 注册响应鼠标拖拽的函数mousemotion()
		glutKeyboardFunc(onKeyDown)		   # 注册键盘输入的函数keydown()
		glutMouseWheelFunc(onMouseWheel)	# 鼠标滚轮缩放函数