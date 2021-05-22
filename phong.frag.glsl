#version 330 core

in vec3 fragPos;
in vec3 normFrag;
in vec2 texCoordFrag;

out vec4 fragColor;

uniform vec3 cameraPos;

struct Material {
	vec3 ambientColor;
	sampler2D diffuse;
	vec3 diffuseColor;
	sampler2D specular;
	vec3 specularColor;
	float shininess;
	
	sampler2D normal;
};
uniform Material material;

struct Light {
	vec3 position;

	vec3 color;
	vec3 ambient;
	vec3 diffuse;
	vec3 specular;
};
uniform Light light;

void main(){
	//ambient
	vec3 ambient = 
		material.ambientColor *
		vec3(texture(material.diffuse, texCoordFrag)) * 
		light.color;

	//diffuse
	//vec3 norm = normalize(normFrag);
	vec3 norm = texture(material.normal, texCoordFrag).rgb; 
	norm = normalize(norm * 2.0 - 1.0);
	vec3 lightDir = normalize(light.position - fragPos);
	float diffuseFactor = max(dot(norm, lightDir), 0.0f);
	vec3 diffuse = 
		diffuseFactor * 
		material.diffuseColor *
		vec3(texture(material.diffuse, texCoordFrag)) *
		light.color;

	//specular
	vec3 cameraDir = normalize(cameraPos - fragPos);
	vec3 reflectDir = reflect(-lightDir, norm);
	float specularFactor = pow(max(dot(cameraDir, reflectDir), 0.0), material.shininess);
	vec3 specular = 
		specularFactor *
		material.specularColor *
		vec3(texture(material.specular, texCoordFrag)) *
		light.color;
		
	//combine
	vec3 result = (ambient + diffuse + specular);
	fragColor = vec4(result, 1.0);
}