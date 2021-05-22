#version 330 core
layout (location = 0) in vec3 pos;
layout (location = 1) in vec2 texCoord;

out vec4 vertPos;
out vec2 _texCoord;
out vec3 debugColor;

uniform mat4 view;
uniform mat4 model;
uniform mat4 proj;

void main()
{
	//vertPos = pos;
	vertPos = vec4(pos, 1.0)*view*model*proj;
	gl_Position = vec4(pos.x,pos.y,pos.z, 1.0f)*view*model*proj;
	_texCoord = texCoord;
	//debugColor = vec3(vertPos.x,0,0);
	
	debugColor = vertPos.xyz;
	debugColor = (debugColor + vec3(1,1,1));
};
