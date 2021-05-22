import numpy as np
from OpenGL.GL import *
from ctypes import c_void_p

class RenderData:
	'''wrapper class for VAO and VBO'''
	def __init__(self, vertData, dataFormat, indicesData=None, dataFlag=GL_STATIC_DRAW):
		'''默认 vertData为numpy数组，dtype=float32'''
		self.VBO = glGenBuffers(1)
		if type(indicesData)!=type(None):
			self.EBO = glGenBuffers(1)
		else:
			self.EBO = None
		self.VAO = glGenVertexArrays(1)

		glBindVertexArray(self.VAO)
		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBufferData(GL_ARRAY_BUFFER, vertData.nbytes, vertData, dataFlag)
		if self.EBO:
			glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
			glBufferData(GL_ELEMENT_ARRAY_BUFFER, indicesData.nbytes, indicesData, dataFlag)
			

		# 解析dataFormat
		# e.g. dataFormat = ['wyzx', 'rgba', 'st', 'nnn']
		FLOAT32_BYTES = 4
		self.stride = 0
		begin_index = []
		for varFmt in dataFormat:
			begin_index.append(self.stride)
			self.stride += len(varFmt)
		if self.EBO:
			self.recNum = len(indicesData)
		else:
			self.recNum = len(vertData)//self.stride

		#print(self.recNum)
		for i, varFmt in enumerate(dataFormat):
			glVertexAttribPointer(
				i, len(varFmt),	# i-th attrib and its length
				GL_FLOAT,		# float, by usual
				GL_FALSE,		# normalize or not -> False
				self.stride*FLOAT32_BYTES, 				# stride, in bytes, of each record
				c_void_p(begin_index[i]*FLOAT32_BYTES)	# TRICKY!(c_void_p convertion needed)
														# 	the start pos of i-th attrib
			)
			glEnableVertexAttribArray(i)
	def activate(self):
		glBindVertexArray(self.VAO)
	def deactivate(self):
		glBindVertexArray(0)
