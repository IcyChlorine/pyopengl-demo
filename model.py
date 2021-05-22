from render_data import RenderData
from texture import Texture

import numpy as np
from OpenGL.GL import *
from ctypes import c_void_p

import pyassimp
from pyassimp.postprocess import *
import logging
logging.basicConfig(level=logging.INFO)

from shader import Shader

#from numba import jit


class Model:
	'''models imported by assimp'''
	def __init__(self, path):
		self.__loadModel(path)
		self.__loadMaterials()
		self.__initMeshes()
		#self.rootnode = self.__processNode(self.scene.rootnode)

	def __loadModel(self, path):
		try:
			path = path.replace('\\','/')
			self.scene = pyassimp.load(path, aiProcess_Triangulate+aiProcess_FlipUVs)
			self.assetPath = path[:path.rindex('/')+1]
		except pyassimp.AssimpError:
			logging.error('assimp failed to load model!')
	def __initMeshes(self):
		#self.meshes=[]
		for mesh in self.scene.meshes:
			mesh.glBuffer = RenderData(#这个东西最好塞到Mesh的构造函数里
				np.hstack((
					np.array(mesh.vertices, dtype='float32'),
					np.array(mesh.normals, dtype='float32'),
					np.array(mesh.texturecoords[0,:,:2], dtype='float32'),
				)).flatten(),
				['xyz','nnn','st'],
				mesh.faces.flatten(),
			)
	def __loadMaterials(self):
		logging.info(len(self.scene.materials),' mats to load totally')
		self.materials=[]
		for index, material in enumerate(self.scene.materials):
			print('loading material with index ', index)
			material=eval(str(material.properties))#转过去又转回来，不然会出错，好像因为什么延迟操作
			textures=dict()
			for i in range(9):#由于pyassimp的垃圾python绑定，只好用这么dirty的方法了
				
				value = material.get(('file',i))

				if not value: continue
				value = value.replace('\\','/')
				print(value)
				#continue
				if value.find('dif')!=-1:
					textures['diffuse']=Texture(self.assetPath+value)
				elif value.find('spec')!=-1:
					#textures['specular']=Texture(self.assetPath+value)
					pass
				elif value.find('ddn')!=-1:
					textures['normal']=Texture(self.assetPath+value)
				else:#默认是diffuse
					textures['diffuse']=Texture(self.assetPath+value)
			material['textures']=textures
			self.materials.append(material)
	def applyMaterial(self, shader, matIndex):
		material = self.materials[matIndex]
		textures = material['textures']

		shader.setUniform('material.shininess',material[('shininess',0)])
		if textures.get('diffuse'):
			shader.setTexture("material.diffuse",  textures['diffuse'])
		if textures.get('normal'):
			shader.setTexture("material.normal",  textures['normal'])
		if textures.get('specular'):
			shader.setTexture("material.specular",  textures['specular'])

		shader.setUniform('material.ambientColor', material[('ambient', 0)] )
		shader.setUniform('material.diffuseColor', material[('diffuse', 0)] )
		shader.setUniform('material.specularColor', material[('specular', 0)] )
			

	def render(self, shader):
		self.__recur_render(shader, self.scene.rootnode)

	def __recur_render(self, shader, node):
		#self.applyMaterial()
		for mesh in node.meshes:
			self.applyMaterial(shader, mesh.materialindex)
			shader.render(mesh.glBuffer)
		for child in node.children:
			self.__recur_render(shader, child)