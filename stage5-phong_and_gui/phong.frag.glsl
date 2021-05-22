#version 330 core

in vec3 fragPos;
in vec3 normFrag;

out vec4 fragColor;

uniform vec3 objectColor;
uniform vec3 lightColor;
uniform vec3 lightPos;
uniform vec3 cameraPos;

uniform float ambientStrength;
uniform float diffuseStrength;
uniform float specularStrength;
uniform float specularPow;

void main(){
	//float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColor;

	//float diffuseStrength = 1;
	vec3 norm = normalize(normFrag);
	vec3 lightDir = normalize(lightPos - fragPos);
	float diffuseFactor = max(dot(norm, lightDir), 0.0f);
	vec3 diffuse = diffuseStrength * diffuseFactor * lightColor;

	//float specularStrength = 0.5;
	vec3 cameraDir = normalize(cameraPos - fragPos);
	vec3 reflectDir = reflect(-lightDir, norm);
	//float specularPow = 64;
	float specularFactor = pow(max(dot(cameraDir, reflectDir), 0.0), specularPow);
	vec3 specular = specularStrength * specularFactor * lightColor;

    vec3 result = (ambient + diffuse + specular) * objectColor;
    fragColor = vec4(result, 1.0);
}