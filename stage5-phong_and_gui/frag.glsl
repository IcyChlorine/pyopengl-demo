#version 330 core
in vec4 vertPos;
in vec2 _texCoord;
in vec3 debugColor;

out vec4 fragColor;

uniform sampler2D texture1;
uniform sampler2D texture2;

void main(){
	//fragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
	//fragColor = vec4(vertPos, 1.0f);
	//fragColor = uniColor;
	//fragColor = texture(outTexture, _texCoord);
	fragColor = mix(
		texture(texture1, _texCoord),
		texture(texture2, _texCoord),
		(vertPos.x+vertPos.y+1)/2
	);
	//fragColor = vec4(debugColor, 1.0);
}