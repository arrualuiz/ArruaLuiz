import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Configurações do Banner
WIDTH = 880
HEIGHT = 220
NUM_FRAMES = 36
FPS = 18
FONT_SIZE = 14

# Caracteres típicos do Matrix Rain (Katakana, binário, números, símbolos)
KATAKANA = "ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ1234567890ABCDEF<>{}[]/*+=-_~|"

# Inicialização das colunas de chuva Matrix
random.seed(42)
col_width = 16
num_cols = WIDTH // col_width
columns = []
for i in range(num_cols):
    speed = random.uniform(1.2, 2.5)
    length = random.randint(8, 18)
    y_pos = random.uniform(-HEIGHT, 0)
    chars = [random.choice(KATAKANA) for _ in range(35)]
    columns.append({
        "x": i * col_width + 4,
        "y": y_pos,
        "speed": speed,
        "length": length,
        "chars": chars
    })

# Tenta carregar fontes ou usa padrão
try:
    font_char = ImageFont.truetype("consola.ttf", FONT_SIZE)
    font_title = ImageFont.truetype("impact.ttf", 46)
    font_sub = ImageFont.truetype("consola.ttf", 15)
except Exception:
    font_char = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()

frames = []

for frame_idx in range(NUM_FRAMES):
    # Imagem base escura
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(5, 10, 8))
    draw = ImageDraw.Draw(img)

    # Desenha as colunas de Matrix Rain
    for col in columns:
        col_y = (col["y"] + (frame_idx * col["speed"] * (HEIGHT / NUM_FRAMES))) % (HEIGHT + col["length"] * FONT_SIZE) - (col["length"] * FONT_SIZE)
        
        for j in range(col["length"]):
            char_y = col_y + j * FONT_SIZE
            if -FONT_SIZE <= char_y <= HEIGHT + FONT_SIZE:
                char_idx = (j + frame_idx) % len(col["chars"])
                char = col["chars"][char_idx]
                
                # O último caractere da gota é o mais brilhante (branco/neon)
                if j == col["length"] - 1:
                    color = (240, 255, 240) # Branco neon
                elif j >= col["length"] - 3:
                    color = (57, 255, 20)  # Verde neon ultra brilhante
                elif j >= col["length"] - 7:
                    color = (0, 200, 50)   # Verde médio
                else:
                    fade = max(15, int(120 * (j / col["length"])))
                    color = (0, fade, 20)  # Verde escuro / rastro

                draw.text((col["x"], char_y), char, font=font_char, fill=color)

    # Cria camada semi-transparente no centro para destacar o texto
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Caixa central escurecida para legibilidade do nome
    box_w, box_h = 560, 100
    box_x = (WIDTH - box_w) // 2
    box_y = (HEIGHT - box_h) // 2
    overlay_draw.rounded_rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        radius=12,
        fill=(5, 12, 8, 195),
        outline=(0, 255, 100, 180),
        width=2
    )

    # Converte e combina camadas
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    # Texto do Título: LUIZ ARRUA
    title_text = "LUIZ ARRUA"
    sub_text = "[ BACKEND • DATA SCIENCE • AUTOMATIONS ]"
    
    # Efeito de brilho / sombra neon no título
    for offset in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        draw.text((WIDTH//2 + offset[0], HEIGHT//2 - 24 + offset[1]), title_text, font=font_title, fill=(0, 255, 80, 200), anchor="mm")
    draw.text((WIDTH//2, HEIGHT//2 - 24), title_text, font=font_title, fill=(255, 255, 255, 255), anchor="mm")

    # Subtítulo
    draw.text((WIDTH//2, HEIGHT//2 + 22), sub_text, font=font_sub, fill=(0, 230, 120, 255), anchor="mm")

    # Converte de volta para P para otimização de GIF
    frames.append(img.convert("RGB").quantize(colors=64))

# Salva GIF animado
frames[0].save(
    "matrix_banner.gif",
    save_all=True,
    append_images=frames[1:],
    duration=int(1000 / FPS),
    loop=0,
    optimize=True
)

print("[Matrix Generator] matrix_banner.gif gerado com sucesso!")
