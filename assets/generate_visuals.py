import os
import urllib.request
import ssl
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Disable SSL verification for font downloads
ssl._create_default_https_context = ssl._create_unverified_context

# Paths
BASE_DIR = "/Users/nikhilgollachannu/Desktop/KaggleCapstone/assistive-agent-vision"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Input generated images
CARD_BASE_PATH = "/Users/nikhilgollachannu/.gemini/antigravity-ide/brain/baa18d08-56a4-4f38-a9a7-698bde54fbc6/assistive_vision_card_base_1782230559153.png"
THUMBNAIL_BASE_PATH = "/Users/nikhilgollachannu/.gemini/antigravity-ide/brain/baa18d08-56a4-4f38-a9a7-698bde54fbc6/assistive_vision_thumbnail_base_1782230578253.png"

# Output paths
CARD_OUT_PATH = os.path.join(ASSETS_DIR, "kaggle_cover.png")
THUMBNAIL_OUT_PATH = os.path.join(ASSETS_DIR, "youtube_thumbnail.png")

def download_fonts():
    os.makedirs(FONTS_DIR, exist_ok=True)
    
    fonts = {
        "Outfit-Bold.ttf": "https://raw.githubusercontent.com/Outfitio/Outfit-Fonts/main/fonts/ttf/Outfit-Bold.ttf",
        "Outfit-Medium.ttf": "https://raw.githubusercontent.com/Outfitio/Outfit-Fonts/main/fonts/ttf/Outfit-Medium.ttf",
        "Outfit-Regular.ttf": "https://raw.githubusercontent.com/Outfitio/Outfit-Fonts/main/fonts/ttf/Outfit-Regular.ttf"
    }
    
    print("Checking/Downloading fonts...")
    for font_name, url in fonts.items():
        path = os.path.join(FONTS_DIR, font_name)
        if not os.path.exists(path):
            print(f"Downloading {font_name} from Google Fonts repository...")
            try:
                urllib.request.urlretrieve(url, path)
                print(f"Successfully downloaded {font_name}")
            except Exception as e:
                print(f"Error downloading {font_name}: {e}")
        else:
            print(f"{font_name} already exists.")

def get_font(name, size):
    path = os.path.join(FONTS_DIR, name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception as e:
            print(f"Error loading {name}: {e}. Falling back to default.")
    
    # Fallback to system fonts
    fallbacks = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf"
    ]
    for fb in fallbacks:
        if os.path.exists(fb):
            try:
                return ImageFont.truetype(fb, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_gradient_background(width, height, left_color, right_color):
    """Creates a smooth linear horizontal gradient."""
    base = Image.new("RGBA", (width, height), left_color)
    top = Image.new("RGBA", (width, height), right_color)
    
    # Create gradient mask
    mask = Image.new("L", (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (x / width)))
    mask.putdata(mask_data)
    
    base.alpha_composite(top, dest=(0, 0), source=(0, 0))
    # We blend them
    return Image.composite(top, base, mask)

def fade_left_edge(img, fade_width=120):
    """Smoothly fades the left edge of an image to transparent."""
    img = img.convert("RGBA")
    width, height = img.size
    
    # Split alpha
    r, g, b, alpha = img.split()
    alpha_data = list(alpha.getdata())
    
    for y in range(height):
        for x in range(fade_width):
            idx = y * width + x
            factor = x / fade_width
            alpha_data[idx] = int(alpha_data[idx] * factor)
            
    new_alpha = Image.new("L", img.size)
    new_alpha.putdata(alpha_data)
    
    return Image.merge("RGBA", (r, g, b, new_alpha))

def draw_badge(draw, text, font, x, y, text_color, border_color, bg_color):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    
    pad_x = 16
    pad_y = 10
    badge_w = w + pad_x * 2
    badge_h = h + pad_y * 2
    
    # Rounded rect border
    draw.rounded_rectangle(
        [x, y, x + badge_w, y + badge_h],
        radius=8,
        fill=bg_color,
        outline=border_color,
        width=1
    )
    
    # Draw text (vertically centered)
    draw.text((x + pad_x, y + pad_y - 2), text, fill=text_color, font=font)
    return badge_w, badge_h

def draw_text_with_shadow(draw, text, font, x, y, text_color, shadow_color, offset=(2, 2)):
    # Draw shadow first
    draw.text((x + offset[0], y + offset[1]), text, fill=shadow_color, font=font)
    # Draw main text
    draw.text((x, y), text, fill=text_color, font=font)

def wrap_text(text, font, max_width, draw):
    words = text.split(" ")
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_str = " ".join(current_line)
        bbox = draw.textbbox((0, 0), line_str, font=font)
        w = bbox[2] - bbox[0]
        if w > max_width:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
            
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def build_project_card():
    print("Building Project Card...")
    # Dimensions: 1200 x 630
    width, height = 1200, 630
    
    # Colors: dark purple/blue gradient matching the base image background
    # Left edge of base image is roughly #0c081e. Top is similar, bottom is blacker.
    bg = create_gradient_background(width, height, (6, 4, 15, 255), (20, 13, 44, 255))
    
    # Load and resize base image
    base_img = Image.open(CARD_BASE_PATH).convert("RGBA")
    # Base is square, resize to height 630 (so 630x630)
    base_img = base_img.resize((630, 630), Image.Resampling.LANCZOS)
    
    # Fade left edge of base image to blend seamlessly
    base_img = fade_left_edge(base_img, fade_width=150)
    
    # Composite base image on the right
    bg.alpha_composite(base_img, dest=(570, 0))
    
    # Draw on canvas
    draw = ImageDraw.Draw(bg)
    
    # Load fonts
    font_title = get_font("Outfit-Bold.ttf", 52)
    font_subtitle = get_font("Outfit-Regular.ttf", 22)
    font_badge = get_font("Outfit-Medium.ttf", 14)
    
    # Draw Title
    title_text = "Assistive Vision Agent"
    draw_text_with_shadow(draw, title_text, font_title, 70, 120, (255, 255, 255, 255), (0, 0, 0, 120), (3, 3))
    
    # Draw Subtitle
    sub_text = "Gemini-powered live camera guidance for visually impaired users"
    wrapped_sub = wrap_text(sub_text, font_subtitle, 480, draw)
    
    curr_y = 205
    for line in wrapped_sub:
        draw.text((70, curr_y), line, fill=(209, 201, 255, 255), font=font_subtitle)
        curr_y += 32
        
    # Draw Badges (Multi-Agent AI, Gemini Vision, Live Assist, Safety Guardrails)
    badge_y = curr_y + 45
    
    # Badge configuration: text, colors (text_color, border_color, bg_color)
    badges = [
        ("Multi-Agent AI", (0, 240, 255, 255), (0, 240, 255, 100), (0, 240, 255, 15)),
        ("Gemini Vision", (168, 85, 247, 255), (168, 85, 247, 100), (168, 85, 247, 15)),
        ("Live Assist", (251, 191, 36, 255), (251, 191, 36, 100), (251, 191, 36, 15)),
        ("Safety Guardrails", (34, 197, 94, 255), (34, 197, 94, 100), (34, 197, 94, 15))
    ]
    
    # Draw badges in 2 rows
    # Row 1
    w1, h1 = draw_badge(draw, badges[0][0], font_badge, 70, badge_y, badges[0][1], badges[0][2], badges[0][3])
    draw_badge(draw, badges[1][0], font_badge, 70 + w1 + 15, badge_y, badges[1][1], badges[1][2], badges[1][3])
    
    # Row 2
    badge_y += h1 + 15
    w2, h2 = draw_badge(draw, badges[2][0], font_badge, 70, badge_y, badges[2][1], badges[2][2], badges[2][3])
    draw_badge(draw, badges[3][0], font_badge, 70 + w2 + 15, badge_y, badges[3][1], badges[3][2], badges[3][3])
    
    # Save image
    bg.save(CARD_OUT_PATH, "PNG")
    print(f"Project Card saved to {CARD_OUT_PATH}")

def build_thumbnail():
    print("Building YouTube Thumbnail...")
    # Dimensions: 1280 x 720
    width, height = 1280, 720
    
    # Background gradient: very dark indigo/blue
    bg = create_gradient_background(width, height, (5, 6, 14, 255), (14, 16, 38, 255))
    
    # Load and resize base image
    base_img = Image.open(THUMBNAIL_BASE_PATH).convert("RGBA")
    # Base is square, resize to height 720 (so 720x720)
    base_img = base_img.resize((720, 720), Image.Resampling.LANCZOS)
    
    # Fade left edge to blend
    base_img = fade_left_edge(base_img, fade_width=180)
    
    # Composite base image on the right
    bg.alpha_composite(base_img, dest=(560, 0))
    
    # Draw on canvas
    draw = ImageDraw.Draw(bg)
    
    # Load fonts
    font_main_title = get_font("Outfit-Bold.ttf", 68)
    font_sec_text = get_font("Outfit-Bold.ttf", 30)
    font_small = get_font("Outfit-Medium.ttf", 18)
    
    # Draw Main Text (YouTube Thumbnail style: high impact, neon yellow/cyan accent)
    # Line 1: AI Vision (white)
    # Line 2: Assistant (cyan/yellow)
    y_pos = 150
    draw_text_with_shadow(draw, "AI Vision", font_main_title, 70, y_pos, (255, 255, 255, 255), (0, 0, 0, 160), (4, 4))
    
    y_pos += 85
    # Use neon cyan or neon yellow. The street has neon yellow outlines and cyan speech bubble.
    # Yellow makes it stand out immensely! Let's use neon yellow (#ffd700 or #ffe600)
    draw_text_with_shadow(draw, "Assistant", font_main_title, 70, y_pos, (255, 215, 0, 255), (0, 0, 0, 160), (4, 4))
    
    # Draw Secondary Text
    y_pos += 120
    draw_text_with_shadow(draw, "Live Camera + Audio Guidance", font_sec_text, 70, y_pos, (0, 240, 255, 255), (0, 0, 0, 140), (3, 3))
    
    # Draw Small text at the bottom
    draw_text_with_shadow(draw, "Built with Gemini + Antigravity", font_small, 70, 600, (170, 175, 190, 255), (0, 0, 0, 120), (2, 2))
    
    # Save image
    bg.save(THUMBNAIL_OUT_PATH, "PNG")
    print(f"Thumbnail saved to {THUMBNAIL_OUT_PATH}")

if __name__ == "__main__":
    download_fonts()
    build_project_card()
    build_thumbnail()
    print("Done generating visuals!")
