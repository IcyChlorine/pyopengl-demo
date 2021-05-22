from OpenGL.GL import *
import numpy as np
from render_data import RenderData

class Shader:
	def __init__(self, **kwargs):
		# param check
		if not (('vertShaderSrc' in kwargs) ^ ('vertShaderFilename' in kwargs)):
			raise ValueError('必须提供恰好一份vertex shader src!')
		if not (('fragShaderSrc' in kwargs) ^ ('fragShaderFilename' in kwargs)):
			raise ValueError('必须提供恰好一份fragment shader src!')
		if kwargs.get('vertShaderFilename'):
			with open(kwargs['vertShaderFilename'], 'r') as f:
				vertShaderSrc = f.read()
		if kwargs.get('fragShaderFilename'):
			with open(kwargs['fragShaderFilename'], 'r') as f:
				fragShaderSrc = f.read()

		# compile
		vertShaderID = glCreateShader(GL_VERTEX_SHADER)
		glShaderSource(vertShaderID, vertShaderSrc)
		glCompileShader(vertShaderID)
		if glGetShaderiv(vertShaderID, GL_COMPILE_STATUS)==0:
			raise Exception('vert shader compilation failed!')
		fragShaderID = glCreateShader(GL_FRAGMENT_SHADER)
		glShaderSource(fragShaderID, fragShaderSrc)
		glCompileShader(fragShaderID)
		if glGetShaderiv(fragShaderID, GL_COMPILE_STATUS)==0:
			raise Exception('frag shader compilation failed!')

		# link
		self.shaderProgID = glCreateProgram()
		glAttachShader(self.shaderProgID, vertShaderID)
		glAttachShader(self.shaderProgID, fragShaderID)
		glLinkProgram(self.shaderProgID)
		if glGetProgramiv(self.shaderProgID, GL_LINK_STATUS)==0:
			raise Exception('shader program linking failed!')

		# delete tmp variables
		glDeleteShader(vertShaderID)
		glDeleteShader(fragShaderID)

		# dict that stages uniform values
		self.uniform = {}
		self.textureUniform = {}# 特殊处理

	def activate(self):
		glUseProgram(self.shaderProgID)

	def deactivate(self):
		glUseProgram(0)

	def setUniform(self, uniformName, uniformValue):
		if not isinstance(uniformName, str):
			raise Exception('uniformName must be string as a name for variables!')

		if type(uniformValue) == list:	#numpy 大法好
			uniformValue = np.array(uniformValue)
		self.uniform[uniformName] = uniformValue
	def __setUniform(self):
		'''truly pass uniform values to shader program'''
		for name, value in self.uniform.items():
			location = glGetUniformLocation(self.shaderProgID, name)
			if value.dtype == np.dtype('int32'):
				sType = 'i'
			else:
				sType = 'f'
			if value.ndim == 2:
				sMat = 'Matrix'
				if value.shape[0] == value.shape[1]:
					sLen = str(value.shape[0])
				else:
					sLen = f'{value.shape[0]}x{value.shape[1]}'
			else:
				sMat = ''
				sLen = str(value.shape[0])
			funcName = 'glUniform' + sMat + sLen + sType + 'v'
			eval(funcName+r'(location, 1, value)')
				

	def render(self, renderData, drawMode=GL_TRIANGLES):
		self.activate()
		renderData.activate()

		self.__setUniform()

		glDrawArrays(drawMode, 0, 3)
		self.deactivate()