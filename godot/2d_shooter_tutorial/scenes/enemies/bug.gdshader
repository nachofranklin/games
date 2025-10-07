shader_type canvas_item;

uniform vec3 colour: source_color = vec3(1);
uniform float progress: hint_range(0.0, 0.8, 0.1) = 0;

void fragment() {
	float current_a = texture(TEXTURE, UV).a;
	vec4 target_colour = mix(texture(TEXTURE, UV), vec4(colour, current_a), progress);
	COLOR = target_colour;
}