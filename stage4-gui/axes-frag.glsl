#version 330 core
in vec4 vertPos;
in vec3 _color;

out vec4 fragColor;

void main(){
	fragColor = vec4(_color, 1.0);
}