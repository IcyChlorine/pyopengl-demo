#version 330 core
layout (location = 0) in vec3 pos;
layout (location = 1) in vec3 color;

out vec4 vertPos;
out vec3 _color;
//out vec3 debugColor;

uniform mat4 view;
uniform mat4 model;
uniform mat4 proj;

void main()
{
	//vertPos = pos;
	vertPos = vec4(pos, 1.0f) * model * view * proj;
	gl_Position = vertPos;
	_color = color;
}
