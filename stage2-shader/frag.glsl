#version 330 core
in vec3 vertPos;

out vec4 fragColor;

uniform vec4 uniColor;

void main(){
	//fragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
	//fragColor = vec4(vertPos, 1.0f);
	fragColor = uniColor;
}