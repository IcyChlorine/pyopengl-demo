from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

from shader import Shader
from render_data import RenderData

import time
from matplotlib.colors import hsv_to_rgb
	
class Application:
	def __init__(self, **kwargs):
		# init vaa
		self.isPerspective = True							   # 透视投影
		self.view = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  # 视景体的left/right/bottom/top/near/far六个面
		self.scale_k = np.array([1.0, 1.0, 1.0])				 # 模型缩放比例
		self.cameraPos = np.array([0.0, 0.0, 2.0])					 # 眼睛的位置（默认z轴的正方向）
		self.lookAt = np.array([0.0, 0.0, 0.0])				 # 瞄准方向的参考点（默认在坐标原点）
		self.cameraUp = np.array([0.0, 1.0, 0.0])				  # 定义对观察者而言的上方（默认y轴的正方向）
		self.windowSize= [640, 480]							 # 保存窗口宽度和高度的变量
		self.mouse = {'left':False, 'right':False, 'pos':[0,0]}	# 鼠标信息
		self.dist, self.φ, self.θ = self.getPosture()					 # 眼睛与观察目标之间的距离、仰角、方位角

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

		self.naiveShader = Shader(vertShaderFilename = 'vert.glsl', fragShaderFilename = 'frag.glsl')


		vertices = np.array([
			-0.5, -0.5, 0.0,
			0.5, -0.5, 0.0,
			0.0,  0.5, 0.0
		], dtype='float32')
		self.triangle = RenderData(vertices, ['xyz'])
		
		
	def run(self):
		glutMainLoop()   
	
	def getPosture(self):
		cameraPos, lookAt = self.cameraPos, self.lookAt
		
		dist = np.sqrt(np.power((cameraPos-lookAt), 2).sum())
		if dist > 0:
			φ = np.arcsin((cameraPos[1]-lookAt[1])/dist)
			θ = np.arcsin((cameraPos[0]-lookAt[0])/(dist*np.cos(φ)))
		else:
			φ = 0.0
			θ = 0.0
			
		return dist, φ, θ
		
	def initGLParam(self):
		glClearColor(0.2, 0.3, 0.3, 1.0) # 设置画布背景色。注意：这里必须是4个参数
		glEnable(GL_DEPTH_TEST)		  # 开启深度测试，实现遮挡关系
		glDepthFunc(GL_LEQUAL)		   # 设置深度测试函数（GL_LEQUAL只是选项之一）
	
	def registerRenderFunc(self):
		def mainLoop():
			isPerspective, view = self.isPerspective, self.view
			cameraPos, lookAt, cameraUp = self.cameraPos, self.lookAt, self.cameraUp
			scale_k = self.scale_k
			windowSize = self.windowSize

			# 清除屏幕及深度缓存
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
			# 设置投影（透视投影）
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()

			if windowSize[0] > windowSize[1]:
				if isPerspective:
					glFrustum(view[0]*windowSize[0]/windowSize[1], view[1]*windowSize[0]/windowSize[1], view[2], view[3], view[4], view[5])
				else:
					glOrtho(view[0]*windowSize[0]/windowSize[1], view[1]*windowSize[0]/windowSize[1], view[2], view[3], view[4], view[5])
			else:
				if isPerspective:
					glFrustum(view[0], view[1], view[2]*windowSize[1]/windowSize[0], view[3]*windowSize[1]/windowSize[0], view[4], view[5])
				else:
					glOrtho(view[0], view[1], view[2]*windowSize[1]/windowSize[0], view[3]*windowSize[1]/windowSize[0], view[4], view[5])

			# 设置模型视图
			glMatrixMode(GL_MODELVIEW)
			glLoadIdentity()

			# 几何变换
			glScale(*scale_k)

			# 设置视点
			gluLookAt(*cameraPos,*lookAt,*cameraUp)

			# 设置视口
			glViewport(0, 0, *windowSize)
		
			# ---------------------------------------------------------------
			glBegin(GL_LINES)					# 开始绘制线段（世界坐标系）

			# 以红色绘制x轴
			glColor4f(1.0, 0.0, 0.0, 1.0)		# 设置当前颜色为红色不透明
			glVertex3f(-0.8, 0.0, 0.0)		   # 设置x轴顶点（x轴负方向）
			glVertex3f(0.8, 0.0, 0.0)			# 设置x轴顶点（x轴正方向）

			# 以绿色绘制y轴
			glColor4f(0.0, 1.0, 0.0, 1.0)		# 设置当前颜色为绿色不透明
			glVertex3f(0.0, -0.8, 0.0)		   # 设置y轴顶点（y轴负方向）
			glVertex3f(0.0, 0.8, 0.0)			# 设置y轴顶点（y轴正方向）

			# 以蓝色绘制z轴
			glColor4f(0.0, 0.0, 1.0, 1.0)		# 设置当前颜色为蓝色不透明
			glVertex3f(0.0, 0.0, -0.8)		   # 设置z轴顶点（z轴负方向）
			glVertex3f(0.0, 0.0, 0.8)			# 设置z轴顶点（z轴正方向）

			glEnd()							  # 结束绘制线段

			# ---------------------------------------------------------------
			glBegin(GL_TRIANGLES)				# 开始绘制三角形（z轴负半区）

			glColor4f(1.0, 0.0, 0.0, 1.0)		# 设置当前颜色为红色不透明
			glVertex3f(-0.5, -0.366, -0.5)	   # 设置三角形顶点
			glColor4f(0.0, 1.0, 0.0, 1.0)		# 设置当前颜色为绿色不透明
			glVertex3f(0.5, -0.366, -0.5)		# 设置三角形顶点
			glColor4f(0.0, 0.0, 1.0, 1.0)		# 设置当前颜色为蓝色不透明
			glVertex3f(0.0, 0.5, -0.5)		   # 设置三角形顶点

			glEnd()							  # 结束绘制三角形

			# ---------------------------------------------------------------
			glBegin(GL_TRIANGLES)				# 开始绘制三角形（z轴正半区）

			glColor4f(1.0, 0.0, 0.0, 1.0)		# 设置当前颜色为红色不透明
			glVertex3f(-0.5, 0.5, 0.5)		   # 设置三角形顶点
			glColor4f(0.0, 1.0, 0.0, 1.0)		# 设置当前颜色为绿色不透明
			glVertex3f(0.5, 0.5, 0.5)			# 设置三角形顶点
			glColor4f(0.0, 0.0, 1.0, 1.0)		# 设置当前颜色为蓝色不透明
			glVertex3f(0.0, -0.366, 0.5)		 # 设置三角形顶点

			glEnd()							  # 结束绘制三角形

			# ---------------------------------------------------------------
			glutSwapBuffers()					# 切换缓冲区，以显示绘制内容
		#glutDisplayFunc(mainLoop)
		def mainLoop2():
			#glUseProgram(self.naiveShader)
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

			t,T = time.time(), 5.
			h, s, v= (t % T / T) , 1, 1
			color = hsv_to_rgb([h,s,v])
			color = np.append(color, [1.])

			#print(color)
			self.naiveShader.setUniform('uniColor',color)
			self.naiveShader.render(self.triangle)
			glutSwapBuffers()
			glutPostRedisplay()
		glutDisplayFunc(mainLoop2)


	def registerCallbackFunc(self):
		def onReshape(width, height):
			windowSize = self.windowSize
		
			windowSize = [width, height]
			glutPostRedisplay()
		
		def onMouseClick(button, state, x, y):
			scale_k = self.scale_k
			mouse = self.mouse

			mouse['pos'] = [ x, y ]
			if button == GLUT_LEFT_BUTTON:
				mouse['left'] = state==GLUT_DOWN
			elif button == 3:
				scale_k *= 1.05
				glutPostRedisplay()
			elif button == 4:
				scale_k *= 0.95
				glutPostRedisplay()
		
		def onMouseMove(x, y):
			cameraPos, cameraUp = self.cameraPos, self.cameraUp
			mouse = self.mouse
			dist, φ, θ = self.dist, self.φ, self.θ
			windowSize = self.windowSize

			if mouse['left']:
				dx = mouse['pos'][0] - x
				dy = y - mouse['pos'][1]
				mouse['pos'] = [x, y]

				self.φ += 2*np.pi*dy/windowSize[1]
				self.φ %= 2*np.pi
				self.θ += 2*np.pi*dx/windowSize[0]
				self.θ %= 2*np.pi
				r = dist*np.cos(φ)

				cameraPos[1] = dist*np.sin(φ)
				cameraPos[0] = r*np.sin(θ)
				cameraPos[2] = r*np.cos(θ)

				if 0.5*np.pi < φ < 1.5*np.pi:
					cameraUp[1] = -1.0
				else:
					cameraUp[1] = 1.0

				glutPostRedisplay()

		self.renderSkeleton = False
		def onKeyDown(key, x, y):
			dist, φ, θ = self.dist, self.φ, self.θ
			cameraPos, lookAt, cameraUp = self.cameraPos, self.lookAt, self.cameraUp  
			isPerspective, view = self.isPerspective, self.view

			if key in [b'x', b'X', b'y', b'Y', b'z', b'Z', b'l', b'L']:
				if key == b'x': # 瞄准参考点 x 减小
					lookAt[0] -= 0.01
				elif key == b'X': # 瞄准参考 x 增大
					lookAt[0] += 0.01
				elif key == b'y': # 瞄准参考点 y 减小
					lookAt[1] -= 0.01
				elif key == b'Y': # 瞄准参考点 y 增大
					lookAt[1] += 0.01
				elif key == b'z': # 瞄准参考点 z 减小
					lookAt[2] -= 0.01
				elif key == b'Z': # 瞄准参考点 z 增大
					lookAt[2] += 0.01
				elif key == b'l' or key == b'L': #渲染线框
					self.renderSkeleton = not self.renderSkeleton
					if self.renderSkeleton:
						glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
					else:
						glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

				dist, φ, θ = self.getPosture()
				glutPostRedisplay()
			elif key == b'\r': # 回车键，视点前进
				cameraPos = lookAt + (cameraPos - lookAt) * 0.9
				dist, φ, θ = self.getPosture()
				glutPostRedisplay()
			elif key == b'\x08': # 退格键，视点后退
				cameraPos = lookAt + (cameraPos - lookAt) * 1.1
				dist, φ, θ = self.getPosture()
				glutPostRedisplay()
			elif key == b' ': # 空格键，切换投影模式
				isPerspective = not isPerspective 
				glutPostRedisplay()

		glutReshapeFunc(onReshape)			# 注册响应窗口改变的函数reshape()
		glutMouseFunc(onMouseClick)		   # 注册响应鼠标点击的函数mouseclick()
		glutMotionFunc(onMouseMove)		 # 注册响应鼠标拖拽的函数mousemotion()
		glutKeyboardFunc(onKeyDown)		   # 注册键盘输入的函数keydown()
		
		glVertexAttribPointer
	