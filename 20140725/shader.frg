varying vec2 v_texCoord;
uniform sampler2D s_texture;
uniform float texture_width;
uniform float texture_height;

void main() {
    gl_FragColor = texture2D( s_texture, v_texCoord);
}