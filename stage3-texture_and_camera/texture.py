from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from PIL import Image


class Texture:
	def __init__(self, filename):
		try:
			image = Image.open(filename)
		except IOError as ex:
			raise Exception(f'IOError: failed to open texture file {filename}')
		#image.show()
		#print('opened file: size=', image.size, 'format=', image.format)
		image = image.transpose(Image.FLIP_TOP_BOTTOM) # 上下翻转，以和gl标准一致
		imageData = np.array(list(image.getdata()), np.uint8)

		self.textureID = glGenTextures(1)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
		glBindTexture(GL_TEXTURE_2D, self.textureID)
		#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
		#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
		glTexImage2D(
			GL_TEXTURE_2D, 
			0,							# mipmap level 
			GL_RGB, 					# format generated
			*image.size, 				# image size
			0, 							# legacy stuff, just ignore it
			GL_RGB, GL_UNSIGNED_BYTE, 	# format of source
			imageData					# ACTUAL DATA
		)
		glBindTexture(GL_TEXTURE_2D, 0)
		image.close()
