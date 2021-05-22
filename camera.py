import glm
import numpy as np

class Camera():
	def __init__(self, ρ0=5, θ0=np.pi/2, φ0=0):
		self.ρ=ρ0
		self.θ=θ0
		self.φ=φ0
		self.cameraPos=np.zeros((3,))
		self.__updateMatrix()


	def modifyPosture(self, Δθ=0, Δφ=0):
		self.φ += Δφ
		self.φ %= 2*np.pi
		self.θ += Δθ
		if self.θ > np.pi:
			self.θ = np.pi
		elif self.θ < 1e-6:#不能严格是0(这是可以被float32取到的)，不然随后的矩阵中会出现nan
			self.θ = 1e-6
		#print(self.θ,self.φ)
		self.__updateMatrix()
	def scale(self, factor=1):
		self.ρ *= factor
		self.__updateMatrix()

	def __updateMatrix(self):
		cameraUp  = np.array([0.,1.,0.]) #多亏了一些正交性，这个一直保持0,1,0就可以了(不用根据θ的变化而变化)		
		cameraLookAt = np.array([0.,0.,0.])#对于这个相机，视点始终保持在[0,0,0]

		#cameraPos = np.array([0.,0.,0.])
		self.cameraPos[1] = self.ρ*np.cos(self.θ)
		r            = self.ρ*np.sin(self.θ)# ρ's projection on xz-plane
		#print(r)
		self.cameraPos[0] =      r*np.sin(self.φ)
		self.cameraPos[2] =      r*np.cos(self.φ)
		self.viewMat = np.array(
			glm.lookAt(
				glm.vec3(self.cameraPos),
				glm.vec3(cameraLookAt-self.cameraPos),#vector forward
				glm.vec3(cameraUp)
			)
		)#有优化的空间