import pygame
import sys
import random
import math
import webbrowser
import numpy as np
from PIL import Image

# Import modules
from matrix_module import run_matrix_module
from material_module import run_material_module
from protein_module import run_protein_module

# ============================================================
# Initialize pygame
# ============================================================
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Celestial Cipher")

# ============================================================
# COLOR PALETTE
# ============================================================
ATTIC_BG = (15, 20, 40)
WALL_COLOR = (25, 30, 55)
FLOOR_COLOR = (10, 15, 30)
CEILING_COLOR = (20, 25, 45)
WINDOW_GLOW = (0, 200, 220)
WINDOW_INNER = (100, 220, 230)
PORTAL_BG = (10, 30, 80)
PORTAL_GLOW = (0, 150, 200)
SILHOUETTE = (5, 5, 10)
BUTTON_COLOR = (40, 50, 80)
BUTTON_HOVER = (60, 80, 120)
TEXT_COLOR = (200, 220, 255)
CORRIDOR_BG = (15, 30, 35)
DOORWAY_GLOW = (150, 220, 210)
BASEMENT_BG = (10, 20, 35)
CRYSTAL_COLOR = (100, 180, 220)
CRYSTAL_GLOW = (150, 210, 240)
SCREEN_GLOW = (0, 180, 200)
PROTEIN_COLOR = (180, 100, 220)
PROTEIN_GLOW = (200, 150, 240)
BALLOON_COLOR = (200, 220, 255)
BALLOON_TEXT = (10, 20, 40)
MATRIX_COLOR = (0, 220, 180)
SUCCESS_COLOR = (0, 200, 100)
WARNING_COLOR = (255, 150, 0)

# ============================================================
# FONTS
# ============================================================
font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)
tiny_font = pygame.font.SysFont("Arial", 13)
title_font = pygame.font.SysFont("Arial", 32)
matrix_font = pygame.font.SysFont("Arial", 36, bold=True)
balloon_font = pygame.font.SysFont("Arial", 14)

# ============================================================
# LOAD FIGURE IMAGES
# ============================================================
def load_figure(filename):
    try:
        img = pygame.image.load(filename)
        img = pygame.transform.scale(
            img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return img
    except:
        return None

try:
    figure1 = pygame.image.load("Figure 1.jpg")
except:
    figure1 = None
figure3a = load_figure("Figure 3a.jpg")
figure3b = load_figure("Figure 3b.jpg")
figure5 = load_figure("Figure 5.jpg")
figure6 = load_figure("Figure 6.jpg")
figure8 = load_figure("Figure 8.jpg")

# ============================================================
# GAME STATES
# ============================================================
INTRO = "intro"
PLAYER_SELECT = "player_select"
ATTIC_STAR = "attic_star"
ATTIC_ART = "attic_art"
CORRIDOR_INTRO = "corridor_intro"
CORRIDOR = "corridor"
BASEMENT = "basement"
CRYSTAL_INTRO = "crystal_intro"
CRYSTAL_ROOM = "crystal_room"
PROTEIN_INTRO = "protein_intro"
PROTEIN_ROOM = "protein_room"

current_room = INTRO

# ============================================================
# GAME STATE VARIABLES
# ============================================================
num_players = 1              # 1 or 2
captured_matrix = None       # Final matrix for predictions
captured_matrix_p1 = None    # Player 1 matrix
captured_matrix_p2 = None    # Player 2 matrix
captured_image = None
captured_image_surface = None
captured_image_surface_p2 = None
artwork_surface = None
artwork_surface_p2 = None
material_result = None
protein_result = None
artwork_copy_feedback = ""
artwork_copy_timer = 0

# ============================================================
# SF PENSEES QUOTES
# ============================================================
quotes = [
    "matter whispers to the mind",
    "the stars do not explain",
    "small things carry infinite weight",
    "every atom was once a star",
    "science is controlled imagination",
    "the observer shapes the observed",
    "order emerges from apparent chaos",
    "the universe computes itself",
    "light is both wave and particle",
    "the molecule remembers its origin",
    "energy is frozen information",
    "time flows differently at small scales",
    "complexity hides in simple rules",
    "the invisible governs the visible",
    "entropy is the arrow of time",
    "nature favors elegant solutions",
    "symmetry is the language of physics",
    "the boundary between self and world",
    "all matter seeks its lowest state",
    "observation disturbs what it measures",
    "the cosmos is indifferent and magnificent",
    "structure is memory made permanent",
    "every pattern conceals a deeper one",
    "the question outlives the answer",
    "silence between atoms is not empty",
    "what is measured becomes real",
    "the smallest things cast the longest shadows",
    "disorder is order not yet understood",
    "the universe tends toward connection",
    "a single bond changes everything",
    "knowledge is the slowest form of light",
    "the mind is a kind of matter",
    "nothing is destroyed only transformed",
    "the infinite lives in the infinitesimal",
    "to name a thing is to change it",
    "all boundaries are approximations",
    "the wave does not know it is water",
    "probability is nature's way of deciding",
    "what collapses was never truly solid",
    "the universe remembers every interaction",
    "to observe is already to intervene",
    "matter is patient beyond all reckoning",
    "the field exists before the particle",
    "every element was forged in a star",
    "the void is not nothing",
    "consciousness is matter becoming aware",
    "the deeper you look the more you find",
    "every measurement is a conversation",
    "the universe has no preferred direction",
    "what binds atoms binds worlds",
    "the simplest explanation hides the deepest truth",
    "space is not empty but full of potential",
    "every collision is a kind of dialogue",
    "the laws of nature are whispers of geometry",
    "a protein folds as a thought unfolds",
    "the lattice remembers its formation",
    "every crystal is frozen time",
    "the electron does not choose its path",
    "light carries information across the void",
    "the universe is older than any of its stories",
    "to understand is to find the hidden symmetry",
    "matter organizes itself toward complexity",
    "the boundary between living and nonliving is thin",
    "every sequence tells an evolutionary story",
    "the fold determines the function",
    "stability is a form of memory",
    "the universe prefers the path of least resistance",
    "what is rare is not always precious",
    "the scale of things humbles every certainty",
    "a single substitution rewrites the protein",
    "the cosmos speaks in mathematical syntax",
    "every force has its equal shadow",
    "the nucleus is almost infinitely small",
    "what we call solid is mostly space",
    "the heavier the element the briefer its life",
    "the periodic table is a map of the possible",
    "every reaction releases what was hidden",
    "nature has no waste only transformation",
    "the photon has no experience of time",
    "to split an atom is to release its history",
    "the chain of causation has no beginning",
    "what we see is always already the past",
    "the universe does not repeat itself exactly",
    "every element carries the signature of its origin",
]

# ============================================================
# GENERATED ASSETS
# ============================================================

stars = [(random.randint(0, 440),
          random.randint(0, 390),
          random.randint(1, 3),
          random.randint(150, 255))
         for _ in range(200)]

crystals = [(random.randint(80, 900),
             random.randint(80, 500),
             random.randint(25, 70),
             random.randint(180, 255))
            for _ in range(14)]

class MystifyLine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x1 = random.randint(0, SCREEN_WIDTH)
        self.y1 = random.randint(0, SCREEN_HEIGHT)
        self.x2 = random.randint(0, SCREEN_WIDTH)
        self.y2 = random.randint(0, SCREEN_HEIGHT)
        self.vx1 = random.uniform(-2, 2)
        self.vy1 = random.uniform(-2, 2)
        self.vx2 = random.uniform(-2, 2)
        self.vy2 = random.uniform(-2, 2)
        self.color = (random.randint(0, 100),
                      random.randint(100, 200),
                      random.randint(150, 255))
        self.alpha = random.randint(80, 180)

    def update(self):
        self.x1 += self.vx1
        self.y1 += self.vy1
        self.x2 += self.vx2
        self.y2 += self.vy2
        if self.x1 < 0 or self.x1 > SCREEN_WIDTH:
            self.vx1 *= -1
        if self.y1 < 0 or self.y1 > SCREEN_HEIGHT:
            self.vy1 *= -1
        if self.x2 < 0 or self.x2 > SCREEN_WIDTH:
            self.vx2 *= -1
        if self.y2 < 0 or self.y2 > SCREEN_HEIGHT:
            self.vy2 *= -1

mystify_lines = [MystifyLine() for _ in range(20)]

class Balloon:
    def __init__(self):
        self.reset()

    def reset(self):
        self.quote = random.choice(quotes)
        self.x = random.randint(200, SCREEN_WIDTH - 200)
        self.y = random.randint(200, SCREEN_HEIGHT - 200)
        self.vy = random.uniform(-0.5, -0.2)
        self.alpha = 255
        self.popped = False
        self.fade_speed = random.uniform(0.5, 1.5)
        text_surface = balloon_font.render(
            self.quote, True, BALLOON_TEXT)
        self.width = text_surface.get_width() + 30
        self.height = 35

    def update(self):
        if not self.popped:
            self.y += self.vy
            if self.y < 50:
                self.popped = True
        else:
            self.alpha -= self.fade_speed * 5
            if self.alpha <= 0:
                self.reset()

    def draw(self, surface):
        if self.alpha <= 0:
            return
        balloon_surf = pygame.Surface(
            (self.width, self.height + 15),
            pygame.SRCALPHA)
        alpha = int(max(0, min(255, self.alpha)))
        pygame.draw.ellipse(
            balloon_surf,
            (*BALLOON_COLOR, alpha),
            (0, 0, self.width, self.height))
        pygame.draw.polygon(
            balloon_surf,
            (*BALLOON_COLOR, alpha),
            [(self.width // 2 - 8, self.height - 5),
             (self.width // 2 + 8, self.height - 5),
             (self.width // 2, self.height + 15)])
        text_surf = balloon_font.render(
            self.quote, True, BALLOON_TEXT)
        text_surf.set_alpha(alpha)
        balloon_surf.blit(
            text_surf,
            (15, self.height // 2 -
             text_surf.get_height() // 2))
        surface.blit(
            balloon_surf,
            (self.x - self.width // 2, self.y))

    def is_clicked(self, pos):
        rect = pygame.Rect(
            self.x - self.width // 2,
            self.y, self.width, self.height)
        return rect.collidepoint(pos)

    def pop(self):
        self.popped = True

balloons = [Balloon() for _ in range(5)]
for b in balloons:
    b.y = random.randint(200, SCREEN_HEIGHT - 100)

protein_points = []
for i in range(20):
    protein_points.append([
        random.randint(200, 1000),
        random.randint(150, 550),
        random.uniform(0, math.pi * 2)
    ])

# ============================================================
# ANIMATION TIMER
# ============================================================
timer = 0

# ============================================================
# BUTTON CLASS
# ============================================================
class Button:
    def __init__(self, x, y, width, height, text,
                 color=None, hover_color=None,
                 active=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color or BUTTON_COLOR
        self.hover_color = hover_color or BUTTON_HOVER
        self.active = active

    def draw(self, surface):
        if not self.active:
            pygame.draw.rect(surface, (30, 35, 50),
                             self.rect, border_radius=8)
            pygame.draw.rect(surface, (50, 60, 80),
                             self.rect, 2, border_radius=8)
            text_surf = font.render(
                self.text, True, (80, 90, 110))
            text_rect = text_surf.get_rect(
                center=self.rect.center)
            surface.blit(text_surf, text_rect)
            return

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color,
                             self.rect, border_radius=8)
        else:
            pygame.draw.rect(surface, self.color,
                             self.rect, border_radius=8)
        pygame.draw.rect(surface, TEXT_COLOR,
                         self.rect, 2, border_radius=8)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(
            center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if not self.active:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# ============================================================
# NAVIGATION BUTTONS
# ============================================================
btn_open_stellarium = Button(
    50, SCREEN_HEIGHT - 110,
    220, 45, "Open Stellarium",
    (0, 100, 130), (0, 150, 180))
btn_capture_matrix = Button(
    290, SCREEN_HEIGHT - 110,
    220, 45, "Capture Matrix",
    (0, 130, 80), (0, 180, 100))
btn_capture_matrix_p2 = Button(
    530, SCREEN_HEIGHT - 110,
    220, 45, "Capture P2 Matrix",
    (80, 40, 120), (120, 60, 160))
btn_to_attic_art = Button(
    SCREEN_WIDTH // 2 - 100,
    SCREEN_HEIGHT - 70,
    200, 45, "View Artworks")

btn_back_to_star = Button(
    50, SCREEN_HEIGHT - 70,
    200, 45, "Back to Stars")
btn_to_corridor = Button(
    SCREEN_WIDTH // 2 - 100,
    SCREEN_HEIGHT - 70,
    200, 45, "Enter Corridor")

btn_back_to_attic = Button(
    50, SCREEN_HEIGHT - 70,
    200, 45, "Back to Attic")
btn_to_basement = Button(
    SCREEN_WIDTH // 2 - 100,
    SCREEN_HEIGHT - 70,
    200, 45, "Enter Basement")

btn_back_to_corridor = Button(
    50, SCREEN_HEIGHT - 70,
    200, 45, "Back to Corridor")
btn_crystal_room = Button(
    400, SCREEN_HEIGHT - 70,
    200, 45, "Crystal Room",
    (40, 80, 120), (60, 120, 160))
btn_protein_room = Button(
    650, SCREEN_HEIGHT - 70,
    200, 45, "Protein Room",
    (80, 40, 120), (120, 60, 160))

btn_back_to_basement_crystal = Button(
    50, SCREEN_HEIGHT - 70,
    200, 45, "Back to Basement")
btn_back_to_basement_protein = Button(
    50, SCREEN_HEIGHT - 70,
    200, 45, "Back to Basement")
btn_copy_artwork = Button(
    SCREEN_WIDTH - 250,
    SCREEN_HEIGHT - 70,
    220, 45, "Copy Artwork",
    (0, 130, 80), (0, 180, 100))

# Player selection buttons
btn_1player = Button(
    SCREEN_WIDTH // 2 - 220,
    SCREEN_HEIGHT - 80,
    200, 50, "1 Player",
    (0, 100, 130), (0, 150, 180))
btn_2player = Button(
    SCREEN_WIDTH // 2 + 20,
    SCREEN_HEIGHT - 80,
    200, 50, "2 Players",
    (80, 40, 120), (120, 60, 160))

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def draw_glow(surface, color, rect, radius=20):
    glow_surface = pygame.Surface(
        (rect.width + radius * 2,
         rect.height + radius * 2),
        pygame.SRCALPHA)
    for i in range(radius, 0, -2):
        alpha = int(60 * (1 - i / radius))
        pygame.draw.rect(
            glow_surface,
            (color[0], color[1], color[2], alpha),
            (radius - i, radius - i,
             rect.width + i * 2,
             rect.height + i * 2),
            border_radius=4)
    surface.blit(glow_surface,
                 (rect.x - radius, rect.y - radius))

def merge_matrices(m1, m2):
    """
    Merge two matrices by adding element-wise
    and retaining only the ones digit
    Analogous to modular arithmetic reduction
    """
    merged = []
    for row in range(3):
        merged_row = []
        for col in range(3):
            total = m1[row][col] + m2[row][col]
            # Retain ones digit
            ones = total % 10
            # If ones digit is 0 use 10
            if ones == 0:
                ones = 10
            # Clamp to 1-9 range
            ones = max(1, min(9, ones))
            merged_row.append(ones)
        merged.append(merged_row)
    return merged

def copy_image_to_clipboard(pygame_surface):
    """Copy pygame surface to Windows clipboard as image"""
    try:
        import win32clipboard
        from io import BytesIO

        # Convert pygame surface to PIL image
        width = pygame_surface.get_width()
        height = pygame_surface.get_height()
        raw = pygame.image.tostring(
            pygame_surface, "RGB")
        pil_img = Image.frombytes(
            "RGB", (width, height), raw)

        # Convert to BMP for clipboard
        output = BytesIO()
        pil_img.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()

        # Copy to clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(
            win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        print(f"Clipboard error: {e}")
        return False

def generate_artwork(image_surface):
    width = image_surface.get_width()
    height = image_surface.get_height()
    artwork = image_surface.copy()
    pixel_array = pygame.surfarray.array3d(artwork)

    pixel_array[:, :, 0] = np.clip(
        pixel_array[:, :, 0] * 0.5, 0, 255)
    pixel_array[:, :, 2] = np.clip(
        pixel_array[:, :, 2] * 1.8, 0, 255)

    rippled = np.zeros_like(pixel_array)
    for y in range(height):
        offset = int(8 * math.sin(
            y * math.pi * 2 / 40))
        for x in range(width):
            src_x = (x + offset) % width
            rippled[x, y] = pixel_array[src_x, y]
    pixel_array = rippled

    pinched = np.zeros_like(pixel_array)
    cx, cy = width // 2, height // 2
    for y in range(height):
        for x in range(width):
            dx = (x - cx) / cx
            dy = (y - cy) / cy
            r = math.sqrt(dx * dx + dy * dy)
            if r < 1:
                factor = math.sqrt(r)
                src_x = int(cx + dx * factor * cx)
                src_y = int(cy + dy * factor * cy)
                src_x = max(0, min(width - 1, src_x))
                src_y = max(0, min(height - 1, src_y))
                pinched[x, y] = \
                    pixel_array[src_x, src_y]
            else:
                pinched[x, y] = pixel_array[x, y]
    pixel_array = pinched

    waved = np.zeros_like(pixel_array)
    for y in range(height):
        for x in range(width):
            src_x = int(x + 10 * math.sin(
                y * math.pi * 2 / 50))
            src_y = int(y + 10 * math.sin(
                x * math.pi * 2 / 50))
            src_x = max(0, min(width - 1, src_x))
            src_y = max(0, min(height - 1, src_y))
            waved[x, y] = pixel_array[src_x, src_y]
    pixel_array = waved

    pixel_array = np.clip(
        pixel_array * 0.7, 0, 255).astype(np.uint8)

    result = pygame.surfarray.make_surface(pixel_array)
    return result

def draw_character(surface, x, y,
                   scale=1.0, girl=False):
    color = SILHOUETTE
    body_w = int(28 * scale)
    body_h = int(55 * scale)
    head_r = int(20 * scale)
    pygame.draw.rect(surface, color,
                     (x - body_w // 2,
                      y - body_h,
                      body_w, body_h),
                     border_radius=4)
    pygame.draw.circle(surface, color,
                       (x, y - body_h - head_r + 5),
                       head_r)
    if girl:
        points = [
            (x - body_w // 2, y - body_h + 20),
            (x + body_w // 2, y - body_h + 20),
            (x + body_w // 2 + 15, y),
            (x - body_w // 2 - 15, y)
        ]
        pygame.draw.polygon(surface, color, points)

def draw_matrix_panel(surface, matrix, x, y):
    if matrix is None:
        no_matrix = font.render(
            "No matrix captured yet.",
            True, WARNING_COLOR)
        surface.blit(no_matrix, (x, y))
        hint = small_font.render(
            "Go back to Stars and "
            "capture a matrix first.",
            True, (150, 170, 200))
        surface.blit(hint, (x, y + 35))
        return

    if num_players == 2:
        title = font.render(
            "Merged Celestial Distance Matrix:",
            True, TEXT_COLOR)
        subtitle = small_font.render(
            "Player 1 and Player 2 matrices "
            "combined element-wise",
            True, (150, 170, 200))
        surface.blit(title, (x, y))
        surface.blit(subtitle, (x, y + 28))
        y += 20
    else:
        title = font.render(
            "Captured Celestial Distance Matrix:",
            True, TEXT_COLOR)
        surface.blit(title, (x, y))
    y += 35

    cell_size = 70
    for row in range(3):
        for col in range(3):
            cx = x + col * cell_size
            cy = y + row * cell_size
            pygame.draw.rect(
                surface, (0, 25, 45),
                (cx, cy,
                 cell_size - 2, cell_size - 2))
            pygame.draw.rect(
                surface, MATRIX_COLOR,
                (cx, cy,
                 cell_size - 2, cell_size - 2), 1)
            val = matrix_font.render(
                str(matrix[row][col]),
                True, MATRIX_COLOR)
            surface.blit(
                val,
                (cx + cell_size // 2 -
                 val.get_width() // 2,
                 cy + cell_size // 2 -
                 val.get_height() // 2))

    y += cell_size * 3 + 15
    formula_preview = compute_formula_preview(matrix)
    if formula_preview:
        preview = small_font.render(
            f"Formula preview: {formula_preview}",
            True, MATRIX_COLOR)
        surface.blit(preview, (x, y))

def compute_formula_preview(matrix):
    try:
        NOBLE_GASES = {2, 10, 18, 36, 54, 86}
        ELEMENTS = {
            1: "H", 2: "He", 3: "Li", 4: "Be",
            5: "B", 6: "C", 7: "N", 8: "O",
            9: "F", 10: "Ne", 11: "Na", 12: "Mg",
            13: "Al", 14: "Si", 15: "P", 16: "S",
            17: "Cl", 18: "Ar", 19: "K", 20: "Ca",
            21: "Sc", 22: "Ti", 23: "V", 24: "Cr",
            25: "Mn", 26: "Fe", 27: "Co", 28: "Ni",
            29: "Cu", 30: "Zn", 31: "Ga", 32: "Ge",
            33: "As", 34: "Se", 35: "Br", 36: "Kr",
            37: "Rb", 38: "Sr", 39: "Y", 40: "Zr",
            41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru",
            45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd",
            49: "In", 50: "Sn", 51: "Sb", 52: "Te",
            53: "I", 54: "Xe", 55: "Cs", 56: "Ba",
            57: "La", 58: "Ce", 59: "Pr", 60: "Nd",
            61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd",
            65: "Tb", 66: "Dy", 67: "Ho", 68: "Er",
            69: "Tm", 70: "Yb", 71: "Lu", 72: "Hf",
            73: "Ta", 74: "W", 75: "Re", 76: "Os",
            77: "Ir", 78: "Pt", 79: "Au", 80: "Hg",
            81: "Tl", 82: "Pb", 83: "Bi", 84: "Po",
            85: "At", 86: "Rn", 87: "Fr", 88: "Ra",
            89: "Ac", 90: "Th", 91: "Pa", 92: "U",
        }
        formula = ""
        for row in matrix:
            a, b, c = row
            z = a * b + c
            if z in NOBLE_GASES:
                z = 1
            sym = ELEMENTS.get(z, "H")
            sub = min(row)
            formula += sym
            if sub > 1:
                formula += str(sub)
        return formula
    except:
        return None

# ============================================================
# INTRO SCREEN DRAWING FUNCTIONS
# ============================================================

def draw_figure_screen(surface, t, figure,
                       fallback_color,
                       lines, line_color,
                       accent_color):
    """
    Generic function to draw a figure intro screen
    with caption lines and pulsing prompt
    """
    if figure:
        surface.blit(figure, (0, 0))
    else:
        surface.fill(fallback_color)

    # Dark overlay at bottom
    overlay = pygame.Surface(
        (SCREEN_WIDTH, 240), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 190),
                     (0, 0, SCREEN_WIDTH, 240))
    surface.blit(overlay,
                 (0, SCREEN_HEIGHT - 240))

    # Caption lines
    y_start = SCREEN_HEIGHT - 225
    for i, line in enumerate(lines):
        color = accent_color if i >= 2 else line_color
        rendered = font.render(line, True, color)
        surface.blit(rendered,
                     (SCREEN_WIDTH // 2 -
                      rendered.get_width() // 2,
                      y_start + i * 38))

    # Pulsing prompt
    alpha = int(180 + 75 * math.sin(t * 0.05))
    alpha = max(0, min(255, alpha))
    click_surf = font.render(
        "— Click anywhere to continue —",
        True, (200, 220, 255))
    click_surf.set_alpha(alpha)
    surface.blit(click_surf,
                 (SCREEN_WIDTH // 2 -
                  click_surf.get_width() // 2,
                  SCREEN_HEIGHT - 35))

def draw_intro(surface, t):
    if figure1:
        # Get original image dimensions
        img_w = figure1.get_width()
        img_h = figure1.get_height()

        # Calculate scaled dimensions maintaining aspect ratio
        scale = min(SCREEN_WIDTH / img_w,
                    SCREEN_HEIGHT / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)

        # Scale image
        scaled = pygame.transform.scale(
            figure1, (new_w, new_h))

        # Fill black background
        surface.fill((0, 0, 0))

        # Center image
        x = (SCREEN_WIDTH - new_w) // 2
        y = (SCREEN_HEIGHT - new_h) // 2
        surface.blit(scaled, (x, y))
    else:
        surface.fill(ATTIC_BG)

    # Dark overlay at bottom
    overlay = pygame.Surface(
        (SCREEN_WIDTH, 220), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 190),
                     (0, 0, SCREEN_WIDTH, 220))
    surface.blit(overlay,
                 (0, SCREEN_HEIGHT - 220))

    # Caption lines
    lines = [
        "You are in the attic of a mysterious house.",
        "The view outside the window opens to "
        "a vast starry sky above and below.",
        "Something extraordinary is about to begin.",
        "The cosmos holds its secrets close...",
        "but not for long.",
    ]
    y_start = SCREEN_HEIGHT - 215
    for i, line in enumerate(lines):
        color = (150, 200, 255) if i >= 2 else TEXT_COLOR
        rendered = font.render(line, True, color)
        surface.blit(rendered,
                     (SCREEN_WIDTH // 2 -
                      rendered.get_width() // 2,
                      y_start + i * 38))

    # Pulsing prompt
    alpha = int(180 + 75 * math.sin(t * 0.05))
    alpha = max(0, min(255, alpha))
    click_surf = font.render(
        "— Click anywhere to continue —",
        True, (200, 220, 255))
    click_surf.set_alpha(alpha)
    surface.blit(click_surf,
                 (SCREEN_WIDTH // 2 -
                  click_surf.get_width() // 2,
                  SCREEN_HEIGHT - 30))

    # Credits
    credit = tiny_font.render(
        "Designed and developed by Vuk Uskoković — 2025",
        True, (120, 140, 160))
    surface.blit(credit, (20, SCREEN_HEIGHT - 20))

def draw_player_select(surface, t):
    """Draw player selection screen"""
    if figure3b:
        surface.blit(figure3b, (0, 0))
    else:
        surface.fill(ATTIC_BG)

    # Dark overlay at bottom
    overlay = pygame.Surface(
        (SCREEN_WIDTH, 140), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 180),
                     (0, 0, SCREEN_WIDTH, 140))
    surface.blit(overlay,
                 (0, SCREEN_HEIGHT - 140))

    # Title
    title = font.render(
        "How many players?", True, TEXT_COLOR)
    surface.blit(title,
                 (SCREEN_WIDTH // 2 -
                  title.get_width() // 2,
                  SCREEN_HEIGHT - 125))

    # Buttons
    btn_1player.draw(surface)
    btn_2player.draw(surface)

    # Pulsing prompt
    alpha = int(180 + 75 * math.sin(t * 0.05))
    alpha = max(0, min(255, alpha))
    click_surf = small_font.render(
        "Select number of players to begin",
        True, (200, 220, 255))
    click_surf.set_alpha(alpha)
    surface.blit(click_surf,
                 (SCREEN_WIDTH // 2 -
                  click_surf.get_width() // 2,
                  SCREEN_HEIGHT))

def draw_corridor_intro(surface, t):
    if figure5:
        surface.blit(figure5, (0, -80))
    else:
        surface.fill(CORRIDOR_BG)

    # Dark overlay at bottom
    overlay = pygame.Surface(
        (SCREEN_WIDTH, 160), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 190),
                     (0, 0, SCREEN_WIDTH, 160))
    surface.blit(overlay,
                 (0, SCREEN_HEIGHT - 140))

    # Left column — white text
    left_lines = [
        "The path between the stars and the molecules",
        "is neither straight nor fully lit.",
    ]
    # Right column — teal text
    right_lines = [
        "In the corridors between worlds,",
        "the universe leaves its messages.",
        "Walk carefully. Listen closely.",
    ]

    y_start = SCREEN_HEIGHT - 130

    for i, line in enumerate(left_lines):
        rendered = font.render(line, True, TEXT_COLOR)
        surface.blit(rendered,
                     (SCREEN_WIDTH // 4 -
                      rendered.get_width() // 2,
                      y_start + i * 38))

    for i, line in enumerate(right_lines):
        rendered = font.render(line, True, DOORWAY_GLOW)
        surface.blit(rendered,
                     (SCREEN_WIDTH * 3 // 4 -
                      rendered.get_width() // 2,
                      y_start + i * 32))

    # Pulsing prompt
    alpha = int(180 + 75 * math.sin(t * 0.05))
    alpha = max(0, min(255, alpha))
    click_surf = font.render(
        "— Click anywhere to continue —",
        True, (200, 220, 255))
    click_surf.set_alpha(alpha)
    surface.blit(click_surf,
                 (SCREEN_WIDTH // 2 -
                  click_surf.get_width() // 2,
                  SCREEN_HEIGHT - 30))

def draw_crystal_intro(surface, t):
    if figure6:
        surface.blit(figure6, (0, 0))
    else:
        surface.fill(BASEMENT_BG)

    # Dark overlay at bottom
    overlay = pygame.Surface(
        (SCREEN_WIDTH, 160), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 190),
                     (0, 0, SCREEN_WIDTH, 160))
    surface.blit(overlay,
                 (0, SCREEN_HEIGHT - 125))

    # Left column — white text
    left_lines = [
        "Within these walls, matter reveals itself.",
        "Every celestial pattern carries a hidden formula.",
    ]
    # Right column — cyan text
    right_lines = [
        "The stars have spoken.",
        "Now the crystals will answer.",
        "Enter, and discover what the cosmos has built.",
    ]

    y_start = SCREEN_HEIGHT - 120

    for i, line in enumerate(left_lines):
        rendered = font.render(line, True, TEXT_COLOR)
        surface.blit(rendered,
                     (SCREEN_WIDTH // 4 -
                      rendered.get_width() // 2,
                      y_start + i * 38))

    for i, line in enumerate(right_lines):
        rendered = font.render(line, True, CRYSTAL_GLOW)
        surface.blit(rendered,
                     (SCREEN_WIDTH * 3 // 4 -
                      rendered.get_width() // 2,
                      y_start + i * 32))

    # Pulsing prompt
    alpha = int(180 + 75 * math.sin(t * 0.05))
    alpha = max(0, min(255, alpha))
    click_surf = font.render(
        "— Click anywhere to continue —",
        True, (200, 220, 255))
    click_surf.set_alpha(alpha)
    surface.blit(click_surf,
                 (SCREEN_WIDTH // 2 -
                  click_surf.get_width() // 2,
                  SCREEN_HEIGHT - 30))

def draw_protein_intro(surface, t):
    if figure8:
        surface.blit(figure8, (0, 0))
    else:
        surface.fill(BASEMENT_BG)

    # No dark overlay — background already dark

    # Left column — white text
    left_lines = [
        "Life writes itself in sequences.",
        "Every arrangement of stars encodes a chain.",
    ]
    # Right column — blue text
    right_lines = [
        "From the vast and luminous",
        "to the intimate and molecular —",
        "the translation is about to begin.",
    ]

    y_start = SCREEN_HEIGHT - 110

    for i, line in enumerate(left_lines):
        rendered = font.render(line, True, TEXT_COLOR)
        surface.blit(rendered,
                     (SCREEN_WIDTH // 4 -
                      rendered.get_width() // 2,
                      y_start + i * 38))

    for i, line in enumerate(right_lines):
        rendered = font.render(line, True, PROTEIN_GLOW)
        surface.blit(rendered,
                     (SCREEN_WIDTH * 3 // 4 -
                      rendered.get_width() // 2,
                      y_start + i * 32))

    # Pulsing prompt
    alpha = int(180 + 75 * math.sin(t * 0.05))
    alpha = max(0, min(255, alpha))
    click_surf = font.render(
        "— Click anywhere to continue —",
        True, (200, 220, 255))
    click_surf.set_alpha(alpha)
    surface.blit(click_surf,
                 (SCREEN_WIDTH // 2 -
                  click_surf.get_width() // 2,
                  SCREEN_HEIGHT - 30))

# ============================================================
# ROOM DRAWING FUNCTIONS
# ============================================================

def draw_attic_star(surface, t):
    surface.fill(ATTIC_BG)
    pygame.draw.rect(surface, CEILING_COLOR,
                     (0, 0, SCREEN_WIDTH, 80))
    pygame.draw.rect(surface, FLOOR_COLOR,
                     (0, SCREEN_HEIGHT - 120,
                      SCREEN_WIDTH, 120))

    # Left cyan window
    window_rect = pygame.Rect(80, 120, 180, 380)
    draw_glow(surface, WINDOW_GLOW, window_rect,
              radius=25)
    pygame.draw.rect(surface, WINDOW_INNER,
                     window_rect)
    for i in range(1, 3):
        pygame.draw.line(
            surface, WINDOW_GLOW,
            (80, 120 + i * (380 // 3)),
            (260, 120 + i * (380 // 3)), 3)
        pygame.draw.line(
            surface, WINDOW_GLOW,
            (80 + i * (180 // 3), 120),
            (80 + i * (180 // 3), 500), 3)

    if num_players == 1:
        # Single portal — center right
        portal_rect = pygame.Rect(730, 80, 480, 530)
        draw_glow(surface, PORTAL_GLOW, portal_rect,
                  radius=30)
        pygame.draw.rect(surface, PORTAL_BG,
                         portal_rect)

        for (sx, sy, size, brightness) in stars:
            twinkle = int(brightness * (
                0.7 + 0.3 * math.sin(
                    t * 0.05 + sx * 0.1)))
            twinkle = max(0, min(255, twinkle))
            pygame.draw.circle(
                surface,
                (twinkle, twinkle, twinkle),
                (730 + sx, 80 + sy), size)

        pygame.draw.rect(surface, PORTAL_GLOW,
                         portal_rect, 3)

        # Status
        if captured_matrix_p1:
            status = small_font.render(
                "Matrix captured successfully",
                True, SUCCESS_COLOR)
        else:
            status = small_font.render(
                "No matrix captured yet",
                True, WARNING_COLOR)
        surface.blit(status, (730, 620))

        # Character
        draw_character(surface, 500,
                       SCREEN_HEIGHT - 120,
                       scale=1.2, girl=False)

    else:
        # Two portals side by side
        # Player 1 portal — left
        portal1_rect = pygame.Rect(300, 90, 380, 490)
        draw_glow(surface, PORTAL_GLOW, portal1_rect,
                  radius=25)
        pygame.draw.rect(surface, PORTAL_BG,
                         portal1_rect)

        for (sx, sy, size, brightness) in stars:
            if sx < 380:
                twinkle = int(brightness * (
                    0.7 + 0.3 * math.sin(
                        t * 0.05 + sx * 0.1)))
                twinkle = max(0, min(255, twinkle))
                pygame.draw.circle(
                    surface,
                    (twinkle, twinkle, twinkle),
                    (300 + sx, 90 + sy), size)

        pygame.draw.rect(surface, PORTAL_GLOW,
                         portal1_rect, 3)

        p1_label = small_font.render(
            "Player 1", True, PORTAL_GLOW)
        surface.blit(p1_label,
                     (portal1_rect.centerx -
                      p1_label.get_width() // 2,
                      portal1_rect.y - 25))

        if not (captured_matrix_p1 and captured_matrix_p2):
            if captured_matrix_p1:
                p1_status = small_font.render(
                    "Matrix captured",
                    True, SUCCESS_COLOR)
            else:
                p1_status = small_font.render(
                    "No matrix yet",
                    True, WARNING_COLOR)
            surface.blit(p1_status,
                         (portal1_rect.centerx +
                          50,
                          portal1_rect.bottom + 5))

        # Player 2 portal — right
        portal2_rect = pygame.Rect(730, 90, 380, 490)
        draw_glow(surface, (150, 100, 220),
                  portal2_rect, radius=25)
        pygame.draw.rect(surface, (10, 10, 40),
                         portal2_rect)

        for (sx, sy, size, brightness) in stars:
            if sx < 380:
                twinkle = int(brightness * (
                    0.7 + 0.3 * math.sin(
                        t * 0.05 + sx * 0.15)))
                twinkle = max(0, min(255, twinkle))
                pygame.draw.circle(
                    surface,
                    (twinkle, int(twinkle * 0.8),
                     twinkle),
                    (730 + sx, 90 + sy), size)

        pygame.draw.rect(surface, (150, 100, 220),
                         portal2_rect, 3)

        p2_label = small_font.render(
            "Player 2", True, (150, 100, 220))
        surface.blit(p2_label,
                     (portal2_rect.centerx -
                      p2_label.get_width() // 2,
                      portal2_rect.y - 25))

        if captured_matrix_p2:
            p2_status = small_font.render(
                "Matrix captured",
                True, SUCCESS_COLOR)
        else:
            p2_status = small_font.render(
                "No matrix yet",
                True, WARNING_COLOR)
            surface.blit(p2_status,
                     (portal2_rect.centerx +
                      50,
                      portal2_rect.bottom + 5))

        # Characters
        draw_character(surface, 420,
                       SCREEN_HEIGHT - 120,
                       scale=1.2, girl=False)
        draw_character(surface, 860,
                       SCREEN_HEIGHT - 120,
                       scale=1.0, girl=True)

        # Merged matrix status
        if captured_matrix_p1 and captured_matrix_p2:
            merged_status = small_font.render(
                "Both matrices captured — "
                "merged matrix ready",
                True, SUCCESS_COLOR)
            surface.blit(merged_status,
                         (SCREEN_WIDTH // 2 -
                          merged_status.get_width() // 2,
                          SCREEN_HEIGHT - 135))

    # Room label
    label = title_font.render(
        "Attic — Stargazing", True, TEXT_COLOR)
    surface.blit(label,
                 (SCREEN_WIDTH // 2 -
                  label.get_width() // 2, 20))

    btn_open_stellarium.draw(surface)
    btn_capture_matrix.draw(surface)
    if num_players == 2:
        btn_capture_matrix_p2.draw(surface)
        # Move View Artworks button to right edge
        btn_to_attic_art.rect.x = SCREEN_WIDTH - 220
        btn_to_attic_art.rect.y = SCREEN_HEIGHT - 70
    else:
        # Keep original position for one player
        btn_to_attic_art.rect.x = SCREEN_WIDTH // 2 - 100
        btn_to_attic_art.rect.y = SCREEN_HEIGHT - 70
    btn_to_attic_art.draw(surface)
    
def draw_attic_art(surface, t):
    surface.fill(ATTIC_BG)
    pygame.draw.rect(surface, CEILING_COLOR,
                     (0, 0, SCREEN_WIDTH, 80))
    pygame.draw.rect(surface, FLOOR_COLOR,
                     (0, SCREEN_HEIGHT - 120,
                      SCREEN_WIDTH, 120))

    glow_surf = pygame.Surface((600, 80),
                               pygame.SRCALPHA)
    pygame.draw.ellipse(glow_surf,
                        (50, 120, 60, 80),
                        (0, 0, 600, 80))
    surface.blit(glow_surf,
                 (SCREEN_WIDTH // 2 - 300,
                  SCREEN_HEIGHT - 140))

    shadow_surf = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA)
    for i in range(3):
        offset = int(20 * math.sin(
            t * 0.02 + i * 1.2))
        points = [
            (300 + i * 300 + offset, 80),
            (280 + i * 300 + offset, 300),
            (320 + i * 300 + offset, 300)
        ]
        pygame.draw.polygon(
            shadow_surf, (20, 40, 45, 180), points)
    surface.blit(shadow_surf, (0, 0))

    draw_matrix_panel(surface, captured_matrix,
                      60, 90)

    screen1_rect = pygame.Rect(
        550, SCREEN_HEIGHT - 310, 300, 190)
    screen2_rect = pygame.Rect(
        900, SCREEN_HEIGHT - 310, 300, 190)

    draw_glow(surface, SCREEN_GLOW,
              screen1_rect, radius=20)
    draw_glow(surface, SCREEN_GLOW,
              screen2_rect, radius=20)

    pygame.draw.rect(surface, (0, 40, 60),
                     screen1_rect)
    pygame.draw.rect(surface, (0, 40, 60),
                     screen2_rect)

    if captured_image_surface:
        surface.blit(captured_image_surface,
                     (screen1_rect.x + 2,
                      screen1_rect.y + 2))
    else:
        label1 = small_font.render(
            "Celestial Image", True, WINDOW_GLOW)
        surface.blit(label1,
                     (screen1_rect.centerx -
                      label1.get_width() // 2,
                      screen1_rect.centery - 10))

    if artwork_surface:
        surface.blit(artwork_surface,
                     (screen2_rect.x + 2,
                      screen2_rect.y + 2))
    else:
        label2 = small_font.render(
            "Abstract Artwork", True, WINDOW_GLOW)
        surface.blit(label2,
                     (screen2_rect.centerx -
                      label2.get_width() // 2,
                      screen2_rect.centery - 10))

    pygame.draw.rect(surface, SCREEN_GLOW,
                     screen1_rect, 2)
    pygame.draw.rect(surface, SCREEN_GLOW,
                     screen2_rect, 2)

    draw_character(surface, 450,
                   SCREEN_HEIGHT - 120,
                   scale=1.0, girl=True)

    label = title_font.render(
        "Attic — Artwork Conversion",
        True, TEXT_COLOR)
    surface.blit(label,
                 (SCREEN_WIDTH // 2 -
                  label.get_width() // 2, 20))

    if not captured_matrix:
        warn = font.render(
            "Capture a matrix first "
            "before proceeding.",
            True, WARNING_COLOR)
        surface.blit(warn,
                     (SCREEN_WIDTH // 2 -
                      warn.get_width() // 2,
                      SCREEN_HEIGHT - 105))

    btn_back_to_star.draw(surface)
    if captured_matrix:
        btn_to_corridor.draw(surface)
    if artwork_surface:
        btn_copy_artwork.draw(surface)
        if artwork_copy_feedback:
            fb = small_font.render(
                artwork_copy_feedback,
                True, SUCCESS_COLOR)
            surface.blit(fb,
                         (SCREEN_WIDTH // 2 -
                          fb.get_width() // 2,
                          SCREEN_HEIGHT - 120))
        
def draw_corridor(surface, t):
    surface.fill(CORRIDOR_BG)

    mystify_surf = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA)
    for line in mystify_lines:
        line.update()
        pygame.draw.line(
            mystify_surf,
            (*line.color, line.alpha),
            (int(line.x1), int(line.y1)),
            (int(line.x2), int(line.y2)), 2)
    surface.blit(mystify_surf, (0, 0))

    pygame.draw.polygon(surface, (20, 45, 50),
                        [(0, 0), (280, 180),
                         (280, SCREEN_HEIGHT - 180),
                         (0, SCREEN_HEIGHT)])
    pygame.draw.polygon(surface, (20, 45, 50),
                        [(SCREEN_WIDTH, 0),
                         (SCREEN_WIDTH - 280, 180),
                         (SCREEN_WIDTH - 280,
                          SCREEN_HEIGHT - 180),
                         (SCREEN_WIDTH, SCREEN_HEIGHT)])

    pygame.draw.rect(surface, (10, 25, 30),
                     (0, 0, SCREEN_WIDTH, 80))
    pygame.draw.rect(surface, (8, 20, 25),
                     (0, SCREEN_HEIGHT - 120,
                      SCREEN_WIDTH, 120))

    door_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - 110, 160, 220, 420)
    draw_glow(surface, DOORWAY_GLOW,
              door_rect, radius=40)

    # Fill doorway with generated artwork if available
    if artwork_surface:
        # Scale artwork to fit door exactly
        door_img = pygame.transform.scale(
            artwork_surface,
            (door_rect.width, door_rect.height))
        surface.blit(door_img, door_rect)
    else:
        pygame.draw.rect(surface, DOORWAY_GLOW, door_rect)

    # Door frame
    pygame.draw.rect(surface, DOORWAY_GLOW,
                     door_rect, 3)

    # Door frame
    pygame.draw.rect(surface, DOORWAY_GLOW,
                     door_rect, 3)

    for balloon in balloons:
        balloon.update()
        balloon.draw(surface)

    draw_character(surface, 320,
                   SCREEN_HEIGHT - 120,
                   scale=1.2, girl=False)
    draw_character(surface, 850,
                   SCREEN_HEIGHT - 130,
                   scale=0.9, girl=True)

    hint = small_font.render(
        "Click balloons to pop them",
        True, TEXT_COLOR)
    surface.blit(hint,
                 (SCREEN_WIDTH // 2 -
                  hint.get_width() // 2, 90))

    label = title_font.render(
        "Corridor", True, TEXT_COLOR)
    surface.blit(label,
                 (SCREEN_WIDTH // 2 -
                  label.get_width() // 2, 20))

    btn_back_to_attic.draw(surface)
    btn_to_basement.draw(surface)


def draw_basement(surface, t):
    surface.fill(BASEMENT_BG)

    for i in range(5):
        pygame.draw.rect(surface, (15, 25, 40),
                         (i * 280, 0, 25, 90))

    pygame.draw.rect(surface, (8, 15, 28),
                     (0, SCREEN_HEIGHT - 120,
                      SCREEN_WIDTH, 120))

    # ---- Crystal Room Door ----
    left_door = pygame.Rect(150, 150, 220, 430)
    pygame.draw.rect(surface, (15, 35, 60),
                     left_door)

    crystal_positions = [
        (210, 200), (310, 250), (210, 320),
        (310, 370), (210, 440), (310, 490),
        (260, 280), (260, 410), (260, 530),
    ]
    for i, (cx, cy) in enumerate(crystal_positions):
        float_offset = int(6 * math.sin(
            t * 0.03 + i * 0.7))
        cy = cy + float_offset
        size = 18 + i % 3 * 5

        glow_surf = pygame.Surface(
            (size * 4, size * 4), pygame.SRCALPHA)
        pygame.draw.polygon(
            glow_surf, (*CRYSTAL_GLOW, 40),
            [(size * 2, 0),
             (size * 4, size * 2),
             (size * 2, size * 4),
             (0, size * 2)])
        surface.blit(glow_surf,
                     (cx - size * 2,
                      cy - size * 2))

        pygame.draw.polygon(
            surface, CRYSTAL_COLOR,
            [(cx, cy - size),
             (cx + size // 2, cy),
             (cx, cy + size),
             (cx - size // 2, cy)])

        pygame.draw.polygon(
            surface, CRYSTAL_GLOW,
            [(cx, cy - size),
             (cx + size // 2, cy),
             (cx, cy - size // 3)])

    draw_glow(surface, CRYSTAL_GLOW,
              left_door, radius=20)
    pygame.draw.rect(surface, CRYSTAL_GLOW,
                     left_door, 2)

    crystal_label = font.render(
        "Crystal Room", True, CRYSTAL_GLOW)
    surface.blit(crystal_label,
                 (left_door.centerx -
                  crystal_label.get_width() // 2,
                  left_door.bottom + 10))

    # ---- Protein Room Door ----
    right_door = pygame.Rect(
        SCREEN_WIDTH - 370, 150, 220, 430)
    pygame.draw.rect(surface, (25, 10, 45),
                     right_door)

    protein_surf = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA)

    chain_points_1 = []
    chain_points_2 = []
    num_points = 12

    for i in range(num_points):
        progress = i / (num_points - 1)
        cy = right_door.y + int(
            progress * right_door.height)

        offset1 = int(50 * math.sin(
            progress * math.pi * 3 +
            t * 0.03))
        cx1 = right_door.centerx + offset1
        chain_points_1.append((cx1, cy))

        offset2 = int(50 * math.sin(
            progress * math.pi * 3 +
            t * 0.03 + math.pi))
        cx2 = right_door.centerx + offset2
        chain_points_2.append((cx2, cy))

    for i in range(len(chain_points_1) - 1):
        pygame.draw.line(
            protein_surf,
            (*PROTEIN_COLOR, 180),
            chain_points_1[i],
            chain_points_1[i + 1], 2)
        pygame.draw.line(
            protein_surf,
            (*PROTEIN_COLOR, 180),
            chain_points_2[i],
            chain_points_2[i + 1], 2)
        if i % 2 == 0:
            pygame.draw.line(
                protein_surf,
                (*PROTEIN_GLOW, 120),
                chain_points_1[i],
                chain_points_2[i], 1)

    for px, py in chain_points_1:
        if (right_door.x < px < right_door.right and
                right_door.y < py < right_door.bottom):
            pygame.draw.circle(
                protein_surf,
                (*PROTEIN_GLOW, 150),
                (px, py), 8)
            pygame.draw.circle(
                protein_surf,
                (*PROTEIN_COLOR, 255),
                (px, py), 5)

    for px, py in chain_points_2:
        if (right_door.x < px < right_door.right and
                right_door.y < py < right_door.bottom):
            pygame.draw.circle(
                protein_surf,
                (*PROTEIN_GLOW, 150),
                (px, py), 8)
            pygame.draw.circle(
                protein_surf,
                (*PROTEIN_COLOR, 255),
                (px, py), 5)

    surface.blit(protein_surf, (0, 0))

    draw_glow(surface, PROTEIN_GLOW,
              right_door, radius=20)
    pygame.draw.rect(surface, PROTEIN_GLOW,
                     right_door, 2)

    protein_label = font.render(
        "Protein Room", True, PROTEIN_GLOW)
    surface.blit(protein_label,
                 (right_door.centerx -
                  protein_label.get_width() // 2,
                  right_door.bottom + 10))

    # Matrix status
    if captured_matrix:
        status = small_font.render(
            "Matrix ready — enter a room "
            "to compute predictions.",
            True, SUCCESS_COLOR)
    else:
        status = small_font.render(
            "No matrix captured — "
            "return to attic first.",
            True, WARNING_COLOR)
    surface.blit(status,
                 (SCREEN_WIDTH // 2 -
                  status.get_width() // 2,
                  SCREEN_HEIGHT - 100))

    draw_character(surface,
                   SCREEN_WIDTH // 2 - 30,
                   SCREEN_HEIGHT - 120,
                   scale=1.1, girl=False)
    draw_character(surface,
                   SCREEN_WIDTH // 2 + 30,
                   SCREEN_HEIGHT - 120,
                   scale=0.85, girl=True)

    label = title_font.render(
        "Basement", True, TEXT_COLOR)
    surface.blit(label,
                 (SCREEN_WIDTH // 2 -
                  label.get_width() // 2, 20))

    btn_back_to_corridor.draw(surface)
    if captured_matrix:
        btn_crystal_room.draw(surface)
        btn_protein_room.draw(surface)


# ============================================================
# MAIN GAME LOOP
# ============================================================
clock = pygame.time.Clock()

while True:
    timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        # Balloon popping in corridor
        if current_room == CORRIDOR:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for balloon in balloons:
                    if balloon.is_clicked(event.pos):
                        balloon.pop()

        # ---- INTRO ----
        if current_room == INTRO:
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_room = PLAYER_SELECT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_room = PLAYER_SELECT

        # ---- PLAYER SELECT ----
        elif current_room == PLAYER_SELECT:
            if btn_1player.is_clicked(event):
                num_players = 1
                current_room = ATTIC_STAR
            if btn_2player.is_clicked(event):
                num_players = 2
                current_room = ATTIC_STAR

        # ---- ATTIC STAR ----
        elif current_room == ATTIC_STAR:
            if btn_open_stellarium.is_clicked(event):
                webbrowser.open(
                    "https://stellarium-web.org")

            # Player 1 matrix capture
            if btn_capture_matrix.is_clicked(event):
                result_matrix, result_image = \
                    run_matrix_module()
                if result_matrix:
                    captured_matrix_p1 = result_matrix
                    if num_players == 1:
                        captured_matrix = result_matrix
                    elif (captured_matrix_p1 and
                          captured_matrix_p2):
                        captured_matrix = \
                            merge_matrices(
                                captured_matrix_p1,
                                captured_matrix_p2)
                if result_image:
                    captured_image = result_image
                    img_copy = result_image.copy()
                    img_copy = img_copy.resize(
                        (296, 186), Image.LANCZOS)
                    captured_image_surface = \
                        pygame.image.fromstring(
                            img_copy.tobytes(),
                            img_copy.size, "RGB")
                    artwork_surface = \
                        generate_artwork(
                            captured_image_surface)

            # Player 2 matrix capture
            if (num_players == 2 and
                    btn_capture_matrix_p2.is_clicked(
                        event)):
                result_matrix, result_image = \
                    run_matrix_module()
                if result_matrix:
                    captured_matrix_p2 = result_matrix
                    if (captured_matrix_p1 and
                            captured_matrix_p2):
                        captured_matrix = \
                            merge_matrices(
                                captured_matrix_p1,
                                captured_matrix_p2)
                if result_image:
                    img_copy = result_image.copy()
                    img_copy = img_copy.resize(
                        (296, 186), Image.LANCZOS)
                    captured_image_surface_p2 = \
                        pygame.image.fromstring(
                            img_copy.tobytes(),
                            img_copy.size, "RGB")
                    artwork_surface_p2 = \
                        generate_artwork(
                            captured_image_surface_p2)

            if btn_to_attic_art.is_clicked(event):
                current_room = ATTIC_ART

        # ---- ATTIC ART ----
        elif current_room == ATTIC_ART:
            if btn_back_to_star.is_clicked(event):
                current_room = ATTIC_STAR

            if (btn_to_corridor.is_clicked(event)
                    and captured_matrix):
                current_room = CORRIDOR_INTRO

            if (btn_copy_artwork.is_clicked(event)
                    and artwork_surface):
                success = copy_image_to_clipboard(
                    artwork_surface)
                if success:
                    artwork_copy_feedback = (
                        "Artwork copied to clipboard "
                        "— paste anywhere with Ctrl+V")
                else:
                    artwork_copy_feedback = (
                        "Copy failed — "
                        "try saving manually")
                artwork_copy_timer = timer

        # ---- CORRIDOR INTRO ----
        elif current_room == CORRIDOR_INTRO:
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_room = CORRIDOR
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_room = CORRIDOR

        # ---- CORRIDOR ----
        elif current_room == CORRIDOR:
            if btn_back_to_attic.is_clicked(event):
                current_room = ATTIC_STAR

            if btn_to_basement.is_clicked(event):
                current_room = BASEMENT

        # ---- BASEMENT ----
        elif current_room == BASEMENT:
            if btn_back_to_corridor.is_clicked(event):
                current_room = CORRIDOR

            if (btn_crystal_room.is_clicked(event)
                    and captured_matrix):
                current_room = CRYSTAL_INTRO

            if (btn_protein_room.is_clicked(event)
                    and captured_matrix):
                current_room = PROTEIN_INTRO

        # ---- CRYSTAL INTRO ----
        elif current_room == CRYSTAL_INTRO:
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = run_material_module(
                    captured_matrix)
                if result:
                    material_result = result
                current_room = BASEMENT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    result = run_material_module(
                        captured_matrix)
                    if result:
                        material_result = result
                    current_room = BASEMENT

        # ---- PROTEIN INTRO ----
        elif current_room == PROTEIN_INTRO:
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = run_protein_module(
                    captured_matrix)
                if result:
                    protein_result = result
                current_room = BASEMENT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    result = run_protein_module(
                        captured_matrix)
                    if result:
                        protein_result = result
                    current_room = BASEMENT
    # Clear artwork copy feedback after 3 seconds
    if artwork_copy_feedback and \
            timer - artwork_copy_timer > 180:
        artwork_copy_feedback = ""

    # ---- DRAW CURRENT ROOM ----
    if current_room == INTRO:
        draw_intro(screen, timer)
    elif current_room == PLAYER_SELECT:
        draw_player_select(screen, timer)
    elif current_room == ATTIC_STAR:
        draw_attic_star(screen, timer)
    elif current_room == ATTIC_ART:
        draw_attic_art(screen, timer)
    elif current_room == CORRIDOR_INTRO:
        draw_corridor_intro(screen, timer)
    elif current_room == CORRIDOR:
        draw_corridor(screen, timer)
    elif current_room == BASEMENT:
        draw_basement(screen, timer)
    elif current_room == CRYSTAL_INTRO:
        draw_crystal_intro(screen, timer)
    elif current_room == PROTEIN_INTRO:
        draw_protein_intro(screen, timer)

    pygame.display.flip()
    clock.tick(60)
