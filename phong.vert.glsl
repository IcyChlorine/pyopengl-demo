#version 330 core

layout(location=0) in vec3 pos;
layout(location=1) in vec3 norm;
layout(location=2) in vec2 texCoord;

out vec3 fragPos;
out vec3 normFrag;
out vec2 texCoordFrag;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main(){
	gl_Position = vec4(pos, 1.0f) * model * view * proj;
	fragPos = vec3(vec4(pos, 1.0f) * model);
	
	normFrag = norm;
	texCoordFrag = texCoord;
}