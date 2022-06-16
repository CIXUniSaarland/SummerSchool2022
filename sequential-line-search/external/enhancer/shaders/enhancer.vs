#version 330

layout(location = 0) in vec2 vertex_position;
smooth out vec2 vertex_uv;

void main()
{
    gl_Position = vec4(vertex_position, 0.0, 1.0);
    vertex_uv = vertex_position * vec2(0.5) + vec2(0.5);
}
