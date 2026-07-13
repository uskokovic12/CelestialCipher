import pygame
import sys
import math
import webbrowser
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image

# ============================================================
# MATRIX MODULE
# ============================================================

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Matrix Construction")

# ============================================================
# DEFAULT DISPLAY AREA
# ============================================================
display_w = SCREEN_WIDTH - 350
display_h = SCREEN_HEIGHT - 120
default_img_x = (display_w - 800) // 2
default_img_y = 90 + (display_h - 500) // 2
default_rect = pygame.Rect(
    default_img_x, default_img_y, 800, 500)

# ============================================================
# LOAD PLACEHOLDER FIGURE
# ============================================================
def load_fig(filename, rect):
    try:
        img = pygame.image.load(filename)
        img = pygame.transform.scale(
            img, (rect.width, rect.height))
        return img
    except:
        return None

fig3a = load_fig("Figure 3a.jpg", default_rect)

# ============================================================
# COLORS
# ============================================================
BG_COLOR = (15, 20, 40)
TEXT_COLOR = (200, 220, 255)
BUTTON_COLOR = (40, 50, 80)
BUTTON_HOVER = (60, 80, 120)
MATRIX_BG = (10, 25, 45)
MATRIX_LINE = (0, 180, 220)
CENTRAL_COLOR = (255, 200, 0)
STAR_COLOR = (0, 255, 180)
LINE_COLOR = (0, 180, 220)
HIGHLIGHT_COLOR = (255, 100, 100)
CONFIRM_COLOR = (0, 150, 80)
CONFIRM_HOVER = (0, 200, 100)

# ============================================================
# FONTS
# ============================================================
font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)
title_font = pygame.font.SysFont("Arial", 30)
matrix_font = pygame.font.SysFont("Arial", 36, bold=True)

# ============================================================
# STATE VARIABLES
# ============================================================
loaded_image = None
pygame_image = None
image_rect = None
central_star = None
detected_stars = []
matrix = None
normalized_distances = []
image_path = None

STAGE_LOAD = "load"
STAGE_SELECT = "select"
STAGE_RESULT = "result"

current_stage = STAGE_LOAD

# ============================================================
# BUTTON CLASS
# ============================================================
class Button:
    def __init__(self, x, y, width, height, text,
                 color=None, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color or BUTTON_COLOR
        self.hover_color = hover_color or BUTTON_HOVER

    def draw(self, surface):
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
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# ============================================================
# BUTTONS
# ============================================================
btn_stellarium = Button(50, 15, 220, 45,
                        "Open Stellarium")
btn_paste = Button(290, 15, 220, 45,
                   "Paste Screenshot")
btn_load = Button(530, 15, 220, 45,
                  "Load Image")
btn_reset = Button(770, 15, 220, 45,
                   "Reset")
btn_confirm = Button(SCREEN_WIDTH - 270,
                     SCREEN_HEIGHT - 65,
                     220, 45, "Confirm Matrix",
                     CONFIRM_COLOR, CONFIRM_HOVER)
btn_back = Button(50, SCREEN_HEIGHT - 65,
                  220, 45, "Back to Game")

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def open_stellarium():
    webbrowser.open("https://stellarium-web.org")

def load_image_dialog():
    global loaded_image, pygame_image, image_rect
    global current_stage, central_star, detected_stars
    global matrix, normalized_distances

    central_star = None
    detected_stars = []
    matrix = None
    normalized_distances = []

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title="Select Stellarium Screenshot",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.bmp"),
            ("All files", "*.*")
        ]
    )
    root.destroy()

    if not path:
        return

    pil_img = Image.open(path).convert("RGB")

    # Scale to fit exactly within default display area
    pil_img_resized = pil_img.resize(
        (default_rect.width, default_rect.height),
        Image.LANCZOS)
    loaded_image = pil_img_resized

    # Convert to pygame surface
    pygame_image = pygame.image.fromstring(
        pil_img_resized.tobytes(),
        (default_rect.width, default_rect.height),
        "RGB")

    # Use default rect position exactly
    image_rect = pygame.Rect(
        default_rect.x, default_rect.y,
        default_rect.width, default_rect.height)

    current_stage = STAGE_SELECT

def paste_image_from_clipboard():
    """Paste image directly from Windows clipboard"""
    global loaded_image, pygame_image, image_rect
    global current_stage, central_star, detected_stars
    global matrix, normalized_distances

    try:
        from PIL import ImageGrab
        # Grab image from clipboard
        pil_img = ImageGrab.grabclipboard()

        if pil_img is None:
            return False

        if not hasattr(pil_img, 'size'):
            return False

        # Reset state
        central_star = None
        detected_stars = []
        matrix = None
        normalized_distances = []

        # Convert to RGB
        pil_img = pil_img.convert("RGB")

        # Scale to fit exactly within default display area
        pil_img_resized = pil_img.resize(
            (default_rect.width, default_rect.height),
            Image.LANCZOS)
        loaded_image = pil_img_resized

        # Convert to pygame surface
        pygame_image = pygame.image.fromstring(
            pil_img_resized.tobytes(),
            (default_rect.width, default_rect.height),
            "RGB")

        # Use default rect position exactly
        image_rect = pygame.Rect(
            default_rect.x, default_rect.y,
            default_rect.width, default_rect.height)

        current_stage = STAGE_SELECT
        return True

    except Exception as e:
        print(f"Clipboard paste error: {e}")
        return False
    
def find_bright_objects(pil_image, central_x, central_y,
                        num_objects=9,
                        min_distance=30,
                        threshold=130,
                        object_radius=15):

    img_array = np.array(pil_image)
    height, width = img_array.shape[:2]

    top_margin = int(height * 0.08)
    bottom_margin = int(height * 0.92)
    usable_height = bottom_margin - top_margin

    brightness = (
        img_array[:, :, 0].astype(float) * 0.299 +
        img_array[:, :, 1].astype(float) * 0.587 +
        img_array[:, :, 2].astype(float) * 0.114)

    brightness[:top_margin, :] = 0
    brightness[bottom_margin:, :] = 0

    grid_cols = 4
    grid_rows = 3
    region_w = width // grid_cols
    region_h = usable_height // grid_rows

    region_candidates = []

    for row in range(grid_rows):
        for col in range(grid_cols):
            x_start = col * region_w
            x_end = min(width, (col + 1) * region_w)
            y_start = top_margin + row * region_h
            y_end = min(bottom_margin,
                        top_margin + (row + 1) * region_h)

            region = brightness[
                y_start:y_end, x_start:x_end]

            if region.size == 0:
                continue

            max_idx = np.unravel_index(
                np.argmax(region), region.shape)
            best_y = y_start + max_idx[0]
            best_x = x_start + max_idx[1]
            best_brightness = region[max_idx]

            if best_brightness < threshold:
                continue

            dist = math.sqrt(
                (best_x - central_x) ** 2 +
                (best_y - central_y) ** 2)

            if dist > min_distance:
                region_candidates.append((
                    best_x, best_y,
                    best_brightness))

    if len(region_candidates) < num_objects:
        bright_pixels = np.argwhere(brightness > 80)
        global_candidates = []
        for pixel in bright_pixels:
            py, px = pixel[0], pixel[1]
            dist = math.sqrt(
                (px - central_x) ** 2 +
                (py - central_y) ** 2)
            if dist > min_distance:
                global_candidates.append(
                    (px, py, brightness[py, px]))

        global_candidates.sort(
            key=lambda c: c[2], reverse=True)

        for cx, cy, cb in global_candidates:
            too_close = False
            for rx, ry, rb in region_candidates:
                dist = math.sqrt(
                    (cx - rx) ** 2 + (cy - ry) ** 2)
                if dist < min_distance:
                    too_close = True
                    break
            if not too_close:
                region_candidates.append((cx, cy, cb))
            if len(region_candidates) >= num_objects:
                break

    if not region_candidates:
        return []

    unique = []
    for cx, cy, cb in sorted(
            region_candidates,
            key=lambda c: c[2], reverse=True):
        too_close = False
        for ux, uy, ub in unique:
            dist = math.sqrt(
                (cx - ux) ** 2 + (cy - uy) ** 2)
            if dist < min_distance:
                too_close = True
                break
        if not too_close:
            unique.append((cx, cy, cb))

    unique.sort(key=lambda s: s[2], reverse=True)
    brightest_9 = unique[:num_objects]
    brightest_9.sort(key=lambda s: (s[1], s[0]))

    return brightest_9

def compute_matrix(central, stars):
    if len(stars) < 9:
        return None, []

    distances = []
    for sx, sy, sb in stars:
        dist = math.sqrt(
            (sx - central[0]) ** 2 +
            (sy - central[1]) ** 2)
        distances.append(dist)

    max_dist = max(distances)
    min_dist = min(distances)

    if max_dist == min_dist:
        normalized = [5] * 9
    else:
        normalized = []
        for d in distances:
            n = 1 + round((d - min_dist) /
                          (max_dist - min_dist) * 8)
            n = max(1, min(9, n))
            normalized.append(n)

    mat = [
        [normalized[0], normalized[1], normalized[2]],
        [normalized[3], normalized[4], normalized[5]],
        [normalized[6], normalized[7], normalized[8]]
    ]

    return mat, normalized

def image_to_screen(px, py):
    if image_rect is None:
        return px, py
    return image_rect.x + px, image_rect.y + py

def screen_to_image(sx, sy):
    if image_rect is None:
        return sx, sy
    return sx - image_rect.x, sy - image_rect.y

# ============================================================
# DRAWING FUNCTIONS
# ============================================================

def draw_matrix_panel(surface, mat, norm_distances):
    panel_x = SCREEN_WIDTH - 320
    panel_y = 90
    panel_w = 300
    panel_h = SCREEN_HEIGHT - 160

    pygame.draw.rect(surface, MATRIX_BG,
                     (panel_x, panel_y,
                      panel_w, panel_h),
                     border_radius=10)
    pygame.draw.rect(surface, MATRIX_LINE,
                     (panel_x, panel_y,
                      panel_w, panel_h),
                     2, border_radius=10)

    title = font.render(
        "Celestial Distance", True, TEXT_COLOR)
    title2 = font.render("Matrix", True, TEXT_COLOR)
    surface.blit(title,
                 (panel_x + panel_w // 2 -
                  title.get_width() // 2,
                  panel_y + 15))
    surface.blit(title2,
                 (panel_x + panel_w // 2 -
                  title2.get_width() // 2,
                  panel_y + 40))

    if mat is None:
        waiting = small_font.render(
            "Select central star",
            True, MATRIX_LINE)
        surface.blit(waiting,
                     (panel_x + panel_w // 2 -
                      waiting.get_width() // 2,
                      panel_y + panel_h // 2))
        return

    cell_size = 70
    grid_x = panel_x + (panel_w - cell_size * 3) // 2
    grid_y = panel_y + 90

    for row in range(3):
        for col in range(3):
            cell_x = grid_x + col * cell_size
            cell_y = grid_y + row * cell_size

            pygame.draw.rect(surface, BG_COLOR,
                             (cell_x, cell_y,
                              cell_size - 2,
                              cell_size - 2))
            pygame.draw.rect(surface, MATRIX_LINE,
                             (cell_x, cell_y,
                              cell_size - 2,
                              cell_size - 2), 1)

            value = mat[row][col]
            val_text = matrix_font.render(
                str(value), True, MATRIX_LINE)
            surface.blit(
                val_text,
                (cell_x + cell_size // 2 -
                 val_text.get_width() // 2,
                 cell_y + cell_size // 2 -
                 val_text.get_height() // 2))

    dist_y = grid_y + cell_size * 3 + 20
    dist_title = small_font.render(
        "Normalized distances:",
        True, TEXT_COLOR)
    surface.blit(dist_title, (panel_x + 15, dist_y))

    for i, d in enumerate(norm_distances):
        dist_text = small_font.render(
            f"Star {i+1}: {d}", True, STAR_COLOR)
        surface.blit(dist_text,
                     (panel_x + 15,
                      dist_y + 25 + i * 22))

def draw_image_overlay(surface):
    if loaded_image is None or image_rect is None:
        return

    if central_star:
        sx, sy = image_to_screen(*central_star)
        pygame.draw.circle(surface, CENTRAL_COLOR,
                           (sx, sy), 12, 2)
        pygame.draw.line(surface, CENTRAL_COLOR,
                         (sx - 18, sy), (sx + 18, sy), 2)
        pygame.draw.line(surface, CENTRAL_COLOR,
                         (sx, sy - 18), (sx, sy + 18), 2)
        label = small_font.render(
            "Central", True, CENTRAL_COLOR)
        surface.blit(label, (sx + 15, sy - 10))

    for i, (ox, oy, ob) in enumerate(detected_stars):
        sx, sy = image_to_screen(ox, oy)
        if central_star:
            cx, cy = image_to_screen(*central_star)
            pygame.draw.line(surface, LINE_COLOR,
                             (cx, cy), (sx, sy), 1)
        pygame.draw.circle(surface, STAR_COLOR,
                           (sx, sy), 8, 2)
        num = small_font.render(
            str(i + 1), True, STAR_COLOR)
        surface.blit(num, (sx + 10, sy - 8))

def draw_instructions(surface, stage):
    if stage == STAGE_LOAD:
        msg = ("Step 1: Open Stellarium, "
               "capture image, then click Load Image")
    elif stage == STAGE_SELECT:
        msg = ("Step 2: Click on your "
               "central star in the image")
    elif stage == STAGE_RESULT:
        msg = ("Step 3: Confirm matrix "
               "or Reset to try again")

    inst = small_font.render(msg, True, TEXT_COLOR)
    surface.blit(inst,
                 (SCREEN_WIDTH // 2 -
                  inst.get_width() // 2,
                  SCREEN_HEIGHT - 38))

# ============================================================
# MAIN MATRIX MODULE LOOP
# ============================================================

def run_matrix_module():
    global current_stage, central_star, detected_stars
    global matrix, normalized_distances, loaded_image
    global pygame_image, image_rect

    clock = pygame.time.Clock()

    while True:
        screen.fill(BG_COLOR)

        # Title
        title = title_font.render(
            "Celestial Distance Matrix Construction",
            True, TEXT_COLOR)
        screen.blit(title, (20, 90))

        # Draw buttons
        btn_stellarium.draw(screen)
        btn_paste.draw(screen)
        btn_load.draw(screen)
        btn_reset.draw(screen)
        btn_back.draw(screen)
        

        # Draw image or placeholder
        if pygame_image and image_rect:
            screen.blit(pygame_image, image_rect)
            draw_image_overlay(screen)
        else:
            if fig3a:
                screen.blit(fig3a, default_rect)

        # Draw matrix panel
        draw_matrix_panel(screen, matrix,
                          normalized_distances)

        # Draw confirm button when matrix ready
        if current_stage == STAGE_RESULT and matrix:
            btn_confirm.draw(screen)

        # Draw instructions
        draw_instructions(screen, current_stage)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None

            if btn_stellarium.is_clicked(event):
                open_stellarium()

            if btn_paste.is_clicked(event):
                success = paste_image_from_clipboard()
                if not success:
                    print("No image found in clipboard. "
                          "Take a screenshot first.")

            if btn_load.is_clicked(event):
                load_image_dialog()

            if btn_reset.is_clicked(event):
                central_star = None
                detected_stars = []
                matrix = None
                normalized_distances = []
                current_stage = STAGE_LOAD
                loaded_image = None
                pygame_image = None
                image_rect = None

            if btn_back.is_clicked(event):
                return None, None

            if btn_confirm.is_clicked(event):
                if matrix:
                    return matrix, loaded_image

            if (event.type == pygame.MOUSEBUTTONDOWN
                    and current_stage == STAGE_SELECT):
                mx, my = event.pos
                if (image_rect and
                        image_rect.collidepoint(mx, my)):
                    img_x, img_y = screen_to_image(mx, my)
                    central_star = (img_x, img_y)

                    detected_stars = find_bright_objects(
                        loaded_image,
                        img_x, img_y,
                        num_objects=9,
                        min_distance=30,
                        threshold=130)

                    if len(detected_stars) < 9:
                        detected_stars = find_bright_objects(
                            loaded_image,
                            img_x, img_y,
                            num_objects=9,
                            min_distance=10,
                            threshold=80)

                    if len(detected_stars) >= 9:
                        matrix, normalized_distances = \
                            compute_matrix(
                                central_star,
                                detected_stars)
                        current_stage = STAGE_RESULT
                    else:
                        msg = font.render(
                            "Not enough bright objects. "
                            "Try different image or zoom.",
                            True, HIGHLIGHT_COLOR)
                        screen.blit(msg, (200, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

# ============================================================
# RUN STANDALONE FOR TESTING
# ============================================================
if __name__ == "__main__":
    result = run_matrix_module()
    if result:
        print("Matrix constructed:")
        for row in result:
            print(row)
    pygame.quit()
