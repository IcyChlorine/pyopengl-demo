#version 330 core
layout (location = 0) in vec3 pos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main()
{
    gl_Position = vec4(pos, 1.0) * model * view * proj;
}