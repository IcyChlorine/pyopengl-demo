import numpy as np
from OpenGL.GL import *

class RenderData:
	'''wrapper class for VAO and VBO'''
	def __init__(self, vertData, dataFormat, dataFlag=GL_STATIC_DRAW):
		'''默认 vertData为numpy数组，dtype=float32'''
		self.VBO = glGenBuffers(1)
		self.VAO = glGenVertexArrays(1)

		glBindVertexArray(self.VAO)
		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBufferData(GL_ARRAY_BUFFER, vertData.nbytes, vertData, dataFlag)
		
		# 解析dataFormat
		# e.g. dataFormat = ['wyzx', 'rgba', 'st', 'nnn']
		FLOAT32_BYTES = 4
		for i, varFmt in enumerate(dataFormat):
			glVertexAttribPointer(i, len(varFmt), GL_FLOAT, GL_FALSE, len(varFmt)*FLOAT32_BYTES, None)
			glEnableVertexAttribArray(i)
	def activate(self):
		glBindVertexArray(self.VAO)
	def deactivate(self):
		glBindVertexArray(0)