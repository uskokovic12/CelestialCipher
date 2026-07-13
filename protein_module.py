import pygame
import sys
import webbrowser
import math
from itertools import combinations
from math import comb

def copy_to_clipboard(text):
    """Copy text to system clipboard"""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()

# ============================================================
# PROTEIN SEQUENCE MAPPING MODULE
# ============================================================

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Protein Sequence Mapping")

# ============================================================
# COLORS
# ============================================================
BG_COLOR = (10, 15, 30)
TEXT_COLOR = (200, 220, 255)
BUTTON_COLOR = (40, 50, 80)
BUTTON_HOVER = (60, 80, 120)
PANEL_BG = (20, 10, 40)
PANEL_LINE = (180, 100, 220)
SEQUENCE_COLOR = (200, 150, 255)
HIGHLIGHT_COLOR = (255, 200, 0)
SUCCESS_COLOR = (0, 200, 100)
WARNING_COLOR = (255, 150, 0)
ERROR_COLOR = (255, 80, 80)
PROTEIN_COLOR = (180, 100, 220)
PROTEIN_GLOW = (200, 150, 240)
CONFIRM_COLOR = (0, 150, 80)
CONFIRM_HOVER = (0, 200, 100)
LINK_COLOR = (0, 180, 220)
LINK_HOVER = (0, 220, 255)

# ============================================================
# FONTS
# ============================================================
font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)
tiny_font = pygame.font.SysFont("Arial", 13)
title_font = pygame.font.SysFont("Arial", 30)
sequence_font = pygame.font.SysFont("Courier", 16)
matrix_font = pygame.font.SysFont("Arial", 32, bold=True)

# ============================================================
# AMINO ACIDS
# Ordered by electron density volume / size
# ============================================================
AMINO_ACIDS = [
    ("G", "Glycine"),
    ("A", "Alanine"),
    ("S", "Serine"),
    ("C", "Cysteine"),
    ("T", "Threonine"),
    ("V", "Valine"),
    ("I", "Isoleucine"),
    ("L", "Leucine"),
    ("N", "Asparagine"),
    ("D", "Aspartic acid"),
    ("Q", "Glutamine"),
    ("K", "Lysine"),
    ("E", "Glutamic acid"),
    ("M", "Methionine"),
    ("H", "Histidine"),
    ("F", "Phenylalanine"),
    ("R", "Arginine"),
    ("Y", "Tyrosine"),
    ("W", "Tryptophan"),
    ("P", "Proline"),
]

# Sequence length options
LENGTH_OPTIONS = {
    9:   [(9, 8)],
    36:  [(9, 7)],
    84:  [(9, 6)],
    120: [(9, 7), (9, 6)],
    210: [(9, 6), (9, 5)],
    255: [(9, 8), (9, 7), (9, 6), (9, 5)],
}

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
# PROTEIN MAPPING FUNCTIONS
# ============================================================

def get_matrix_numbers(matrix):
    numbers = []
    for row in matrix:
        for val in row:
            numbers.append(val)
    return numbers

def compute_combinations(numbers, k):
    sums = []
    for combo in combinations(numbers, k):
        sums.append(sum(combo))
    return sums

def sum_to_amino_acid(total):
    pos = total % 20
    if pos == 0:
        pos = 20
    return AMINO_ACIDS[pos - 1]

def generate_sequence(matrix, length):
    numbers = get_matrix_numbers(matrix)
    params = LENGTH_OPTIONS[length]
    all_sums = []
    for n, k in params:
        sums = compute_combinations(numbers, k)
        all_sums.extend(sums)
    all_sums = all_sums[:length]
    sequence = []
    for total in all_sums:
        aa = sum_to_amino_acid(total)
        sequence.append(aa)
    return sequence

def sequence_to_string(sequence):
    return "".join([aa[0] for aa in sequence])

def format_sequence_lines(seq_string, chars_per_line=80):
    lines = []
    for i in range(0, len(seq_string), chars_per_line):
        lines.append(seq_string[i:i + chars_per_line])
    return lines

# ============================================================
# DRAWING FUNCTIONS
# ============================================================

def draw_matrix_display(surface, matrix, x, y):
    cell_size = 55
    title = font.render("Input Matrix:", True, TEXT_COLOR)
    surface.blit(title, (x, y - 28))
    for row in range(3):
        for col in range(3):
            cx = x + col * cell_size
            cy = y + row * cell_size
            pygame.draw.rect(surface, PANEL_BG,
                             (cx, cy,
                              cell_size - 2,
                              cell_size - 2))
            pygame.draw.rect(surface, PANEL_LINE,
                             (cx, cy,
                              cell_size - 2,
                              cell_size - 2), 1)
            val = matrix_font.render(
                str(matrix[row][col]),
                True, PANEL_LINE)
            surface.blit(val,
                         (cx + cell_size // 2 -
                          val.get_width() // 2,
                          cy + cell_size // 2 -
                          val.get_height() // 2))

def draw_amino_acid_list(surface, x, y):
    title = small_font.render(
        "Amino acid ordering (by size):",
        True, TEXT_COLOR)
    surface.blit(title, (x, y))
    y += 22
    for i, (letter, name) in enumerate(AMINO_ACIDS):
        col = i // 10
        row = i % 10
        text = small_font.render(
            f"{i+1:2}. {letter} — {name}",
            True, SEQUENCE_COLOR)
        surface.blit(text,
                     (x + col * 200,
                      y + row * 22))

def draw_combinatorial_info(surface, matrix,
                            length, x, y):
    params = LENGTH_OPTIONS[length]
    title = small_font.render(
        "Combinatorial construction:",
        True, TEXT_COLOR)
    surface.blit(title, (x, y))
    y += 22
    total = 0
    for n, k in params:
        count = comb(n, k)
        total += count
        text = small_font.render(
            f"C({n},{k}) = {count} combinations "
            f"of {k} numbers from matrix",
            True, (150, 170, 200))
        surface.blit(text, (x, y))
        y += 20
    text = small_font.render(
        f"Total: {total} residues",
        True, SUCCESS_COLOR)
    surface.blit(text, (x, y))

def draw_animated_protein(surface, timer,
                          sequence_length):
    points = []
    for i in range(min(sequence_length, 30)):
        points.append([
            100 + i * 35,
            580 + int(30 * math.sin(
                timer * 0.02 + i * 0.4))
        ])
    protein_surf = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT),
        pygame.SRCALPHA)
    for i, point in enumerate(points):
        px = point[0]
        py = point[1]
        if i < len(points) - 1:
            npx = points[i + 1][0]
            npy = points[i + 1][1]
            pygame.draw.line(
                protein_surf,
                (*PROTEIN_COLOR, 80),
                (px, py), (npx, npy), 2)
        pygame.draw.circle(
            protein_surf,
            (*PROTEIN_GLOW, 50),
            (px, py), 12)
        pygame.draw.circle(
            protein_surf,
            (*PROTEIN_COLOR, 180),
            (px, py), 6)
    surface.blit(protein_surf, (0, 0))

# ============================================================
# STAGES
# ============================================================
STAGE_SELECT_LENGTH = "select_length"
STAGE_SHOW_SEQUENCE = "show_sequence"

# ============================================================
# MAIN MODULE FUNCTION
# ============================================================

def run_protein_module(matrix):

    stage = STAGE_SELECT_LENGTH
    selected_length = None
    sequence = None
    seq_string = ""
    scroll_offset = 0
    timer = 0
    feedback = ""
    feedback_color = TEXT_COLOR

    # Length selection buttons
    lengths = [9, 36, 84, 120, 210, 255]
    length_buttons = {}
    for i, length in enumerate(lengths):
        btn = Button(
            30 + i * 205, 340,
            185, 45,
            f"{length} residues")
        length_buttons[length] = btn

    # Length buttons repositioned for sequence stage
    length_buttons_seq = {}
    for i, length in enumerate(lengths):
        btn = Button(
            30 + i * 205, 95,
            185, 45,
            f"{length} residues")
        length_buttons_seq[length] = btn

    # Generate button
    btn_generate = Button(
        SCREEN_WIDTH // 2 - 100,
        440, 200, 45,
        "Generate Sequence",
        CONFIRM_COLOR, CONFIRM_HOVER,
        active=False)

    # Right side buttons for sequence stage
    btn_generate_seq = Button(
        SCREEN_WIDTH - 300, 175,
        270, 45,
        "Generate Sequence",
        CONFIRM_COLOR, CONFIRM_HOVER)

    btn_reset = Button(
        SCREEN_WIDTH - 300, 235,
        270, 45,
        "Reset")

    btn_copy = Button(
        SCREEN_WIDTH - 300, 295,
        270, 45,
        "Copy Sequence",
        CONFIRM_COLOR, CONFIRM_HOVER)

    # Platform buttons
    platform_buttons = [
        Button(SCREEN_WIDTH - 300, 380,
               270, 45, "EMBOSS Pepinfo",
               LINK_COLOR, LINK_HOVER),
        Button(SCREEN_WIDTH - 300, 440,
               270, 45, "ExPASy ProtParam",
               LINK_COLOR, LINK_HOVER),
        Button(SCREEN_WIDTH - 300, 500,
               270, 45, "Jpred 4",
               LINK_COLOR, LINK_HOVER),
        Button(SCREEN_WIDTH - 300, 560,
               270, 45, "ColabFold",
               LINK_COLOR, LINK_HOVER),
    ]

    platform_urls = [
        "https://www.ebi.ac.uk/Tools/seqstats/emboss_pepinfo/",
        "https://web.expasy.org/protparam/",
        "https://www.compbio.dundee.ac.uk/jpred/",
        "https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb",
    ]

    # Back button
    btn_back = Button(
        30, SCREEN_HEIGHT - 65,
        200, 45, "Back to Basement")

    clock = pygame.time.Clock()

    while True:
        timer += 1
        screen.fill(BG_COLOR)

        # Animated protein at bottom
        if sequence:
            draw_animated_protein(
                screen, timer, len(sequence))

        # Title
        title = title_font.render(
            "Protein Room — Sequence Mapping",
            True, TEXT_COLOR)
        screen.blit(title,
                    (SCREEN_WIDTH // 2 -
                     title.get_width() // 2, 15))

        # ======================================
        # STAGE: SELECT LENGTH
        # ======================================
        if stage == STAGE_SELECT_LENGTH:

            # Matrix
            draw_matrix_display(
                screen, matrix, 30, 65)

            # Amino acid list
            draw_amino_acid_list(
                screen, 230, 65)

            # Length selection title
            length_title = font.render(
                "Select sequence length:",
                True, TEXT_COLOR)
            screen.blit(length_title, (30, 310))

            # Length buttons
            for length, btn in length_buttons.items():
                btn.draw(screen)
                if length == selected_length:
                    pygame.draw.rect(
                        screen, HIGHLIGHT_COLOR,
                        btn.rect, 3, border_radius=8)

            # Combinatorial info or hint
            if selected_length:
                draw_combinatorial_info(
                    screen, matrix,
                    selected_length, 30, 400)
                btn_generate.active = True
            else:
                hint = small_font.render(
                    "Select a length above "
                    "to see combinatorial details",
                    True, (150, 170, 200))
                screen.blit(hint, (30, 400))

            btn_generate.draw(screen)

        # ======================================
        # STAGE: SHOW SEQUENCE
        # ======================================
        elif stage == STAGE_SHOW_SEQUENCE:

            # Length buttons at top
            length_title = font.render(
                "Select different length:",
                True, TEXT_COLOR)
            screen.blit(length_title, (30, 60))

            for length, btn in length_buttons_seq.items():
                btn.draw(screen)
                if length == selected_length:
                    pygame.draw.rect(
                        screen, HIGHLIGHT_COLOR,
                        btn.rect, 3, border_radius=8)

            # Combinatorial info — single line
            params = LENGTH_OPTIONS[selected_length]
            combo_text = " + ".join(
                [f"C({n},{k})={comb(n,k)}"
                 for n, k in params])
            combo_surf = small_font.render(
                f"Construction: {combo_text}"
                f" = {selected_length} residues",
                True, (150, 170, 200))
            screen.blit(combo_surf, (30, 150))

            # Sequence panel
            panel_rect = pygame.Rect(
                30, 170,
                SCREEN_WIDTH - 340,
                SCREEN_HEIGHT - 240)
            pygame.draw.rect(
                screen, PANEL_BG,
                panel_rect, border_radius=8)
            pygame.draw.rect(
                screen, PANEL_LINE,
                panel_rect, 2, border_radius=8)

            # Sequence title inside panel
            seq_title = font.render(
                f"Generated Sequence "
                f"({len(sequence)} residues):",
                True, TEXT_COLOR)
            screen.blit(seq_title,
                        (panel_rect.x + 10,
                         panel_rect.y + 8))

            # Sequence lines
            lines = format_sequence_lines(
                seq_string, 70)
            visible_lines = 14
            for i, line in enumerate(
                    lines[scroll_offset:
                          scroll_offset +
                          visible_lines]):
                actual_pos = (
                    (scroll_offset + i) * 70 + 1)
                pos_label = tiny_font.render(
                    f"{actual_pos:4}",
                    True, (150, 170, 200))
                screen.blit(
                    pos_label,
                    (panel_rect.x + 8,
                     panel_rect.y + 40 + i * 24))
                seq_surf = sequence_font.render(
                    line, True, SEQUENCE_COLOR)
                screen.blit(
                    seq_surf,
                    (panel_rect.x + 45,
                     panel_rect.y + 40 + i * 24))

            # Scroll hint
            if len(lines) > visible_lines:
                scroll_hint = tiny_font.render(
                    "UP/DOWN arrows to scroll",
                    True, (150, 170, 200))
                screen.blit(
                    scroll_hint,
                    (panel_rect.x + 10,
                     panel_rect.bottom - 20))

            # Right side buttons
            btn_generate_seq.draw(screen)
            btn_reset.draw(screen)
            btn_copy.draw(screen)

            # Platform buttons label
            plat_title = font.render(
                "Predict properties:",
                True, TEXT_COLOR)
            screen.blit(plat_title,
                        (SCREEN_WIDTH - 300, 355))

            for btn in platform_buttons:
                btn.draw(screen)

        # Feedback
        if feedback:
            fb = small_font.render(
                feedback, True, feedback_color)
            screen.blit(fb, (250, SCREEN_HEIGHT - 45))

        # Back button
        btn_back.draw(screen)

        # ======================================
        # EVENTS
        # ======================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if stage == STAGE_SHOW_SEQUENCE:
                    if event.key == pygame.K_DOWN:
                        lines = format_sequence_lines(
                            seq_string, 70)
                        if scroll_offset < max(
                                0, len(lines) - 14):
                            scroll_offset += 1
                    if event.key == pygame.K_UP:
                        scroll_offset = max(
                            0, scroll_offset - 1)

            # Length selection — select length stage
            if stage == STAGE_SELECT_LENGTH:
                for length, btn in \
                        length_buttons.items():
                    if btn.is_clicked(event):
                        selected_length = length
                        btn_generate.active = True
                        feedback = (
                            f"{length} residues "
                            f"selected.")
                        feedback_color = SUCCESS_COLOR

                if btn_generate.is_clicked(event):
                    if selected_length:
                        sequence = generate_sequence(
                            matrix, selected_length)
                        seq_string = \
                            sequence_to_string(sequence)
                        stage = STAGE_SHOW_SEQUENCE
                        scroll_offset = 0
                        feedback = (
                            f"Sequence of "
                            f"{selected_length} "
                            f"residues generated.")
                        feedback_color = SUCCESS_COLOR

            # Sequence stage events
            elif stage == STAGE_SHOW_SEQUENCE:

                # Length reselection
                for length, btn in \
                        length_buttons_seq.items():
                    if btn.is_clicked(event):
                        selected_length = length
                        sequence = generate_sequence(
                            matrix, selected_length)
                        seq_string = \
                            sequence_to_string(sequence)
                        scroll_offset = 0
                        feedback = (
                            f"New sequence of "
                            f"{selected_length} "
                            f"residues generated.")
                        feedback_color = SUCCESS_COLOR

                # Generate new sequence
                if btn_generate_seq.is_clicked(event):
                    sequence = generate_sequence(
                        matrix, selected_length)
                    seq_string = \
                        sequence_to_string(sequence)
                    scroll_offset = 0
                    feedback = (
                        f"Sequence regenerated.")
                    feedback_color = SUCCESS_COLOR

                # Reset
                if btn_reset.is_clicked(event):
                    stage = STAGE_SELECT_LENGTH
                    selected_length = None
                    sequence = None
                    seq_string = ""
                    scroll_offset = 0
                    btn_generate.active = False
                    feedback = (
                        "Reset. Select a new length.")
                    feedback_color = TEXT_COLOR

                # Copy
                if btn_copy.is_clicked(event):
                    if seq_string:
                        copy_to_clipboard(seq_string)
                        feedback = (
                            "Sequence copied. "
                            "Paste into platform "
                            "search field.")
                        feedback_color = SUCCESS_COLOR

                # Platform links
                for i, btn in enumerate(
                        platform_buttons):
                    if btn.is_clicked(event):
                        webbrowser.open(
                            platform_urls[i])
                        feedback = (
                            f"{btn.text} opened. "
                            f"Paste sequence there.")
                        feedback_color = SUCCESS_COLOR

            # Back
            if btn_back.is_clicked(event):
                return seq_string \
                    if seq_string else None

        pygame.display.flip()
        clock.tick(60)


# ============================================================
# RUN STANDALONE FOR TESTING
# ============================================================
if __name__ == "__main__":
    test_matrix = [
        [1, 1, 2],
        [1, 3, 1],
        [4, 9, 4]
    ]
    result = run_protein_module(test_matrix)
    if result:
        print(f"Generated sequence: {result}")
    pygame.quit()
