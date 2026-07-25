import pygame
import sys
import webbrowser
import math

# ============================================================
# MATERIAL MAPPING MODULE
# ============================================================

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Material Mapping")

# ============================================================
# COLORS
# ============================================================
BG_COLOR = (10, 20, 35)
TEXT_COLOR = (200, 220, 255)
BUTTON_COLOR = (40, 50, 80)
BUTTON_HOVER = (60, 80, 120)
PANEL_BG = (15, 30, 50)
PANEL_LINE = (0, 180, 220)
FORMULA_COLOR = (0, 220, 180)
HIGHLIGHT_COLOR = (255, 200, 0)
SUCCESS_COLOR = (0, 200, 100)
WARNING_COLOR = (255, 150, 0)
ERROR_COLOR = (255, 80, 80)
CRYSTAL_COLOR = (100, 180, 220)
CRYSTAL_GLOW = (150, 210, 240)
CONFIRM_COLOR = (0, 150, 80)
CONFIRM_HOVER = (0, 200, 100)
SKIP_COLOR = (80, 50, 120)
SKIP_HOVER = (120, 80, 160)

# ============================================================
# FONTS
# ============================================================
font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 16)
title_font = pygame.font.SysFont("Arial", 30)
formula_font = pygame.font.SysFont("Arial", 42, bold=True)
matrix_font = pygame.font.SysFont("Arial", 32, bold=True)

# ============================================================
# PERIODIC TABLE
# ============================================================
ELEMENTS = {
    1: ("H", "Hydrogen"),
    2: ("He", "Helium"),
    3: ("Li", "Lithium"),
    4: ("Be", "Beryllium"),
    5: ("B", "Boron"),
    6: ("C", "Carbon"),
    7: ("N", "Nitrogen"),
    8: ("O", "Oxygen"),
    9: ("F", "Fluorine"),
    10: ("Ne", "Neon"),
    11: ("Na", "Sodium"),
    12: ("Mg", "Magnesium"),
    13: ("Al", "Aluminum"),
    14: ("Si", "Silicon"),
    15: ("P", "Phosphorus"),
    16: ("S", "Sulfur"),
    17: ("Cl", "Chlorine"),
    18: ("Ar", "Argon"),
    19: ("K", "Potassium"),
    20: ("Ca", "Calcium"),
    21: ("Sc", "Scandium"),
    22: ("Ti", "Titanium"),
    23: ("V", "Vanadium"),
    24: ("Cr", "Chromium"),
    25: ("Mn", "Manganese"),
    26: ("Fe", "Iron"),
    27: ("Co", "Cobalt"),
    28: ("Ni", "Nickel"),
    29: ("Cu", "Copper"),
    30: ("Zn", "Zinc"),
    31: ("Ga", "Gallium"),
    32: ("Ge", "Germanium"),
    33: ("As", "Arsenic"),
    34: ("Se", "Selenium"),
    35: ("Br", "Bromine"),
    36: ("Kr", "Krypton"),
    37: ("Rb", "Rubidium"),
    38: ("Sr", "Strontium"),
    39: ("Y", "Yttrium"),
    40: ("Zr", "Zirconium"),
    41: ("Nb", "Niobium"),
    42: ("Mo", "Molybdenum"),
    43: ("Tc", "Technetium"),
    44: ("Ru", "Ruthenium"),
    45: ("Rh", "Rhodium"),
    46: ("Pd", "Palladium"),
    47: ("Ag", "Silver"),
    48: ("Cd", "Cadmium"),
    49: ("In", "Indium"),
    50: ("Sn", "Tin"),
    51: ("Sb", "Antimony"),
    52: ("Te", "Tellurium"),
    53: ("I", "Iodine"),
    54: ("Xe", "Xenon"),
    55: ("Cs", "Cesium"),
    56: ("Ba", "Barium"),
    57: ("La", "Lanthanum"),
    58: ("Ce", "Cerium"),
    59: ("Pr", "Praseodymium"),
    60: ("Nd", "Neodymium"),
    61: ("Pm", "Promethium"),
    62: ("Sm", "Samarium"),
    63: ("Eu", "Europium"),
    64: ("Gd", "Gadolinium"),
    65: ("Tb", "Terbium"),
    66: ("Dy", "Dysprosium"),
    67: ("Ho", "Holmium"),
    68: ("Er", "Erbium"),
    69: ("Tm", "Thulium"),
    70: ("Yb", "Ytterbium"),
    71: ("Lu", "Lutetium"),
    72: ("Hf", "Hafnium"),
    73: ("Ta", "Tantalum"),
    74: ("W", "Tungsten"),
    75: ("Re", "Rhenium"),
    76: ("Os", "Osmium"),
    77: ("Ir", "Iridium"),
    78: ("Pt", "Platinum"),
    79: ("Au", "Gold"),
    80: ("Hg", "Mercury"),
    81: ("Tl", "Thallium"),
    82: ("Pb", "Lead"),
    83: ("Bi", "Bismuth"),
    84: ("Po", "Polonium"),
    85: ("At", "Astatine"),
    86: ("Rn", "Radon"),
    87: ("Fr", "Francium"),
    88: ("Ra", "Radium"),
    89: ("Ac", "Actinium"),
    90: ("Th", "Thorium"),
    91: ("Pa", "Protactinium"),
    92: ("U", "Uranium"),
}

# Noble gases
NOBLE_GASES = {2, 10, 18, 36, 54, 86}

# Common oxidation states
OXIDATION_STATES = {
    1: [1, -1],
    3: [1],
    4: [2],
    5: [3, -3],
    6: [4, 2, -4],
    7: [-3, 3, 5, -1],
    8: [-2, -1],
    9: [-1],
    11: [1],
    12: [2],
    13: [3],
    14: [4, 2, -4],
    15: [-3, 3, 5, 1],
    16: [-2, 4, 6, 2],
    17: [-1, 1, 3, 5, 7],
    19: [1],
    20: [2],
    21: [3],
    22: [2, 3, 4, -1],
    23: [2, 3, 4, 5, -1],
    24: [2, 3, 6, -2],
    25: [2, 3, 4, 6, 7, -3],
    26: [2, 3, 4, 6],
    27: [2, 3, -1],
    28: [2, 3, -1],
    29: [1, 2, 3],
    30: [2],
    31: [3, 1],
    32: [2, 4, -4],
    33: [-3, 3, 5, 2],
    34: [-2, 4, 6, 2],
    35: [-1, 1, 3, 5, 7],
    37: [1],
    38: [2],
    39: [3],
    40: [4, 2, 3],
    41: [3, 5, 2, 4],
    42: [4, 6, 2, 3, -2],
    43: [4, 6, 7, 2, 3],
    44: [2, 3, 4, 6, 8],
    45: [2, 3, 4, -1],
    46: [2, 4, -2],
    47: [1, 2, 3],
    48: [2, 1],
    49: [3, 1],
    50: [2, 4, -4],
    51: [-3, 3, 5],
    52: [-2, 4, 6, 2],
    53: [-1, 1, 3, 5, 7],
    55: [1],
    56: [2],
    57: [3],
    58: [3, 4],
    59: [3, 4],
    60: [3],
    62: [3, 2],
    63: [3, 2],
    64: [3],
    65: [3, 4],
    66: [3],
    67: [3],
    68: [3],
    69: [3, 2],
    70: [3, 2],
    71: [3],
    72: [4, 2, 3],
    73: [5, 3, 4],
    74: [4, 6, 2, 3, -2],
    75: [4, 6, 7, 2, 3, -1],
    76: [4, 6, 8, 2, 3],
    77: [3, 4, 6, -1, 1],
    78: [2, 4, -2],
    79: [1, 3, -1],
    80: [1, 2],
    81: [1, 3],
    82: [2, 4],
    83: [3, 5],
    84: [2, 4, -2],
    85: [-1, 1, 3, 5, 7],
    87: [1],
    88: [2],
    89: [3],
    90: [4, 3],
    91: [5, 4, 3],
    92: [4, 6, 3, 5],
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
            text_surf = font.render(self.text, True,
                                    (80, 90, 110))
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
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if not self.active:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# ============================================================
# MATERIAL MAPPING FUNCTIONS
# ============================================================

def apply_formula(matrix):
    atomic_numbers = []
    for row in matrix:
        a, b, c = row[0], row[1], row[2]
        z = a * b + c
        atomic_numbers.append(z)
    return atomic_numbers

def replace_noble_gases(atomic_numbers):
    return [1 if z in NOBLE_GASES else z
            for z in atomic_numbers]

def get_subscripts(matrix):
    return [min(row) for row in matrix]

def get_element_symbol(z):
    if z in ELEMENTS:
        return ELEMENTS[z][0]
    return "?"

def get_element_name(z):
    if z in ELEMENTS:
        return ELEMENTS[z][1]
    return "Unknown"

def format_formula(symbols, subscripts):
    formula = ""
    for sym, sub in zip(symbols, subscripts):
        formula += sym
        if sub > 1:
            formula += str(sub)
    return formula

def check_oxidation_validity(atomic_numbers, subscripts):
    total_charge = 0
    for z, sub in zip(atomic_numbers, subscripts):
        if z in OXIDATION_STATES:
            ox = OXIDATION_STATES[z][0]
            total_charge += ox * sub
    return total_charge == 0

def auto_adjust_oxidation(atomic_numbers, subscripts):
    adjusted = list(subscripts)
    for scale in range(1, 10):
        trial = [s * scale for s in subscripts]
        total = 0
        for z, sub in zip(atomic_numbers, trial):
            if z in OXIDATION_STATES:
                ox = OXIDATION_STATES[z][0]
                total += ox * sub
        if total == 0:
            return trial
    for i in range(len(adjusted)):
        for new_sub in range(1, 10):
            trial = list(adjusted)
            trial[i] = new_sub
            total = 0
            for z, sub in zip(atomic_numbers, trial):
                if z in OXIDATION_STATES:
                    ox = OXIDATION_STATES[z][0]
                    total += ox * sub
            if total == 0:
                return trial
    return adjusted

def find_binary_simplification(atomic_numbers,
                               subscripts, symbols):
    pairs = [(0, 1), (0, 2), (1, 2)]
    best_formula = None
    for i, j in pairs:
        z1 = atomic_numbers[i]
        z2 = atomic_numbers[j]
        if z1 in OXIDATION_STATES and z2 in OXIDATION_STATES:
            ox1 = OXIDATION_STATES[z1][0]
            ox2 = OXIDATION_STATES[z2][0]
            for s1 in range(1, 8):
                for s2 in range(1, 8):
                    if s1 * ox1 + s2 * ox2 == 0:
                        sym1 = symbols[i]
                        sym2 = symbols[j]
                        f = sym1
                        if s1 > 1:
                            f += str(s1)
                        f += sym2
                        if s2 > 1:
                            f += str(s2)
                        best_formula = f
                        break
                if best_formula:
                    break
        if best_formula:
            break
    return best_formula

# ============================================================
# DRAWING FUNCTIONS
# ============================================================

def draw_matrix_display(surface, matrix, x, y):
    cell_size = 60
    title = font.render("Input Matrix:", True, TEXT_COLOR)
    surface.blit(title, (x, y - 30))
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
                str(matrix[row][col]), True, PANEL_LINE)
            surface.blit(val,
                         (cx + cell_size // 2 -
                          val.get_width() // 2,
                          cy + cell_size // 2 -
                          val.get_height() // 2))

def draw_derivation(surface, matrix,
                    atomic_numbers, symbols,
                    subscripts, x, y):
    title = font.render("Formula Derivation:",
                        True, TEXT_COLOR)
    surface.blit(title, (x, y))
    y += 30
    row_labels = ["Element 1", "Element 2", "Element 3"]
    for i, (row, z, sym, sub) in enumerate(
            zip(matrix, atomic_numbers,
                symbols, subscripts)):
        a, b, c = row
        text = (f"{row_labels[i]}: "
                f"{a} x {b} + {c} = {z} -> "
                f"Z={z} -> {sym}  "
                f"(subscript: {sub})")
        color = FORMULA_COLOR if z not in NOBLE_GASES \
            else WARNING_COLOR
        line = small_font.render(text, True, color)
        surface.blit(line, (x, y + i * 28))

def draw_formula_display(surface, formula,
                         label, x, y, color=None):
    color = color or FORMULA_COLOR
    lbl = font.render(label, True, TEXT_COLOR)
    surface.blit(lbl, (x, y))
    frm = formula_font.render(formula, True, color)
    surface.blit(frm, (x, y + 30))

def draw_floating_crystals(surface, timer):
    crystal_positions = [
        (80, 200), (1150, 150), (100, 500),
        (1180, 480), (60, 350), (1200, 320)
    ]
    for i, (cx, cy) in enumerate(crystal_positions):
        size = 25 + i * 3
        float_y = cy + int(8 * math.sin(
            timer * 0.03 + i * 0.8))
        glow_surf = pygame.Surface(
            (size * 4, size * 4), pygame.SRCALPHA)
        pygame.draw.polygon(
            glow_surf, (*CRYSTAL_GLOW, 30),
            [(size * 2, 0), (size * 4, size * 2),
             (size * 2, size * 4), (0, size * 2)])
        surface.blit(glow_surf,
                     (cx - size * 2, float_y - size * 2))
        pygame.draw.polygon(
            surface, CRYSTAL_COLOR,
            [(cx, float_y - size),
             (cx + size // 2, float_y),
             (cx, float_y + size),
             (cx - size // 2, float_y)])
        pygame.draw.polygon(
            surface, CRYSTAL_GLOW,
            [(cx, float_y - size),
             (cx + size // 2, float_y),
             (cx, float_y - size // 3)])

# ============================================================
# STAGES
# ============================================================
STAGE_INIT = "init"
STAGE_OX_CHOICE = "ox_choice"
STAGE_MANUAL_OX = "manual_ox"
STAGE_BINARY_CHOICE = "binary_choice"
STAGE_FINAL = "final"

# ============================================================
# MAIN MODULE FUNCTION
# ============================================================

def run_material_module(matrix):

    # Compute initial values
    raw_atomic = apply_formula(matrix)
    atomic_numbers = replace_noble_gases(raw_atomic)
    subscripts = get_subscripts(matrix)
    symbols = [get_element_symbol(z)
               for z in atomic_numbers]
    raw_formula = format_formula(symbols, subscripts)

    # Working copies
    current_subscripts = list(subscripts)
    current_formula = raw_formula
    final_formula = raw_formula
    binary_formula = find_binary_simplification(
        atomic_numbers, subscripts, symbols)

    # Stage
    stage = STAGE_INIT

    # Manual oxidation input
    manual_inputs = [str(s) for s in subscripts]
    active_input = 0
    manual_error = ""

    # Feedback
    feedback = ""
    feedback_color = TEXT_COLOR

    # Timer
    timer = 0

    # ---- Buttons ----
    btn_auto = Button(300, 480, 180, 45, "Automatic")
    btn_manual = Button(500, 480, 180, 45, "Manual")
    btn_skip_ox = Button(700, 480, 180, 45,
                         "Skip", SKIP_COLOR, SKIP_HOVER)

    btn_binary_yes = Button(400, 480, 180, 45,
                            "Yes — Simplify",
                            CONFIRM_COLOR, CONFIRM_HOVER)
    btn_binary_no = Button(600, 480, 180, 45,
                           "No — Keep Ternary")
    btn_back_to_ox = Button(SCREEN_WIDTH // 2 - 90,
                            540, 180, 45,
                            "Change Adjustment")

    btn_predict = Button(400, SCREEN_HEIGHT - 65,
                         280, 45, "Predict Properties ->",
                         CONFIRM_COLOR, CONFIRM_HOVER)
    btn_visualize = Button(700, SCREEN_HEIGHT - 65,
                           280, 45, "Visualize Crystal Structure ->",
                           (40, 80, 120), (60, 120, 160))
    btn_back = Button(50, SCREEN_HEIGHT - 65,
                      200, 45, "Back to Basement")
    btn_manual_confirm = Button(500, 650, 180, 45,
                                "Confirm",
                                CONFIRM_COLOR, CONFIRM_HOVER)

    clock = pygame.time.Clock()

    while True:
        timer += 1
        screen.fill(BG_COLOR)

        # Background crystals
        draw_floating_crystals(screen, timer)

        # Title
        title = title_font.render(
            "Crystal Room — Material Mapping",
            True, TEXT_COLOR)
        screen.blit(title,
                    (SCREEN_WIDTH // 2 -
                     title.get_width() // 2, 20))

        # Draw matrix
        draw_matrix_display(screen, matrix, 60, 80)

        # Draw derivation
        draw_derivation(screen, matrix,
                        atomic_numbers, symbols,
                        current_subscripts, 60, 290)

        # Noble gas warnings
        for i, (raw, adj) in enumerate(
                zip(raw_atomic, atomic_numbers)):
            if raw in NOBLE_GASES:
                warn = small_font.render(
                    f"Z={raw} (noble gas) -> "
                    f"replaced with H (Z=1)",
                    True, WARNING_COLOR)
                screen.blit(warn, (60, 390 + i * 20))

        # Raw formula
        draw_formula_display(
            screen, raw_formula,
            "Generated Formula:", 500, 80)

        # ---- STAGE: Oxidation choice ----
        if stage == STAGE_INIT:
            valid = check_oxidation_validity(
                atomic_numbers, current_subscripts)
            if not valid:
                question = font.render(
                    "Oxidation states may not balance. "
                    "Adjust subscripts?",
                    True, WARNING_COLOR)
            else:
                question = font.render(
                    "Oxidation states appear balanced. "
                    "Still adjust?",
                    True, SUCCESS_COLOR)
            screen.blit(question,
                        (SCREEN_WIDTH // 2 -
                         question.get_width() // 2,
                         440))
            btn_auto.draw(screen)
            btn_manual.draw(screen)
            btn_skip_ox.draw(screen)

        # ---- STAGE: Manual oxidation input ----
        elif stage == STAGE_MANUAL_OX:
            instruction = font.render(
                "Enter preferred subscripts "
                "for each element:",
                True, TEXT_COLOR)
            screen.blit(instruction, (300, 440))

            for i, sym in enumerate(symbols):
                lbl = font.render(
                    f"{sym} subscript:",
                    True, TEXT_COLOR)
                screen.blit(lbl, (300, 490 + i * 45))

                input_rect = pygame.Rect(
                    500, 490 + i * 45, 60, 35)
                color = (HIGHLIGHT_COLOR
                         if active_input == i
                         else PANEL_LINE)
                pygame.draw.rect(screen, PANEL_BG,
                                 input_rect)
                pygame.draw.rect(screen, color,
                                 input_rect, 2)
                val = font.render(
                    manual_inputs[i], True, TEXT_COLOR)
                screen.blit(val,
                            (input_rect.x + 8,
                             input_rect.y + 5))

                ox_states = OXIDATION_STATES.get(
                    atomic_numbers[i], ["?"])
                ox_str = ", ".join(
                    [f"{'+' if o > 0 else ''}{o}"
                     for o in ox_states])
                hint = small_font.render(
                    f"Common oxidation states: {ox_str}",
                    True, (150, 170, 200))
                screen.blit(hint,
                            (580, 495 + i * 45))

            if manual_error:
                err = small_font.render(
                    manual_error, True, ERROR_COLOR)
                screen.blit(err, (300, 630))

            btn_manual_confirm.draw(screen)

        # ---- STAGE: Binary choice ----
        elif stage == STAGE_BINARY_CHOICE:
            current_formula = format_formula(
                symbols, current_subscripts)
            draw_formula_display(
                screen,
                current_formula,
                "Adjusted Formula:",
                500, 160,
                SUCCESS_COLOR)

            if binary_formula:
                question = font.render(
                    f"Simplify to binary compound "
                    f"{binary_formula}?",
                    True, WARNING_COLOR)
                screen.blit(question,
                            (SCREEN_WIDTH // 2 -
                             question.get_width() // 2,
                             440))
                btn_binary_yes.draw(screen)
                btn_binary_no.draw(screen)
            else:
                no_binary = font.render(
                    "No binary simplification found.",
                    True, TEXT_COLOR)
                screen.blit(no_binary,
                            (SCREEN_WIDTH // 2 -
                             no_binary.get_width() // 2,
                             440))
                btn_binary_no.draw(screen)

            # Always draw change adjustment button
            btn_back_to_ox.draw(screen)

        # ---- STAGE: Final result ----
        elif stage == STAGE_FINAL:
            draw_formula_display(
                screen,
                final_formula,
                "Final Compound Formula:",
                500, 160,
                HIGHLIGHT_COLOR)

            info = font.render(
                "Click below to predict properties "
                "using the Northwestern predictor.",
                True, TEXT_COLOR)
            screen.blit(info,
                        (SCREEN_WIDTH // 2 -
                         info.get_width() // 2,
                         420))

            nw_note = small_font.render(
                "Note: Copy the formula into "
                "the predictor search field.",
                True, (150, 170, 200))
            screen.blit(nw_note,
                        (SCREEN_WIDTH // 2 -
                         nw_note.get_width() // 2,
                         460))

            copy_hint = font.render(
                f"Formula to enter: {final_formula}",
                True, FORMULA_COLOR)
            screen.blit(copy_hint,
                        (SCREEN_WIDTH // 2 -
                         copy_hint.get_width() // 2,
                         500))

            btn_predict.draw(screen)
            btn_visualize.draw(screen)

            # Allow going back to oxidation choice
            btn_back_to_ox.draw(screen)

        # ---- Feedback message ----
        if feedback:
            fb = font.render(feedback, True,
                             feedback_color)
            screen.blit(fb,
                        (SCREEN_WIDTH // 2 -
                         fb.get_width() // 2,
                         SCREEN_HEIGHT - 110))

        # Always draw back button
        btn_back.draw(screen)

        # ---- Events ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

                # Manual input typing
                if stage == STAGE_MANUAL_OX:
                    if event.key == pygame.K_TAB:
                        active_input = (
                            (active_input + 1) % 3)
                    elif event.key == pygame.K_BACKSPACE:
                        manual_inputs[active_input] = \
                            manual_inputs[
                                active_input][:-1]
                    elif event.unicode.isdigit():
                        if len(manual_inputs[
                                   active_input]) < 2:
                            manual_inputs[
                                active_input] += \
                                event.unicode

            # Click to select input box
            if (stage == STAGE_MANUAL_OX and
                    event.type == pygame.MOUSEBUTTONDOWN):
                for i in range(3):
                    input_rect = pygame.Rect(
                        500, 490 + i * 45, 60, 35)
                    if input_rect.collidepoint(event.pos):
                        active_input = i

            # Stage buttons
            if stage == STAGE_INIT:
                if btn_auto.is_clicked(event):
                    current_subscripts = \
                        auto_adjust_oxidation(
                            atomic_numbers,
                            subscripts)
                    feedback = ("Subscripts automatically "
                                "adjusted.")
                    feedback_color = SUCCESS_COLOR
                    stage = STAGE_BINARY_CHOICE

                if btn_manual.is_clicked(event):
                    stage = STAGE_MANUAL_OX
                    manual_inputs = [
                        str(s) for s in subscripts]

                if btn_skip_ox.is_clicked(event):
                    current_subscripts = list(subscripts)
                    feedback = ("Keeping original "
                                "subscripts.")
                    feedback_color = TEXT_COLOR
                    stage = STAGE_BINARY_CHOICE

            elif stage == STAGE_MANUAL_OX:
                if btn_manual_confirm.is_clicked(event):
                    if all(m.isdigit() and int(m) > 0
                           for m in manual_inputs):
                        current_subscripts = [
                            int(m)
                            for m in manual_inputs]
                        feedback = ("Manual subscripts "
                                    "applied.")
                        feedback_color = SUCCESS_COLOR
                        stage = STAGE_BINARY_CHOICE
                    else:
                        manual_error = (
                            "Please enter valid "
                            "positive integers "
                            "for all subscripts.")

            elif stage == STAGE_BINARY_CHOICE:
                if btn_binary_yes.is_clicked(event):
                    final_formula = binary_formula
                    stage = STAGE_FINAL

                if btn_binary_no.is_clicked(event):
                    final_formula = format_formula(
                        symbols, current_subscripts)
                    stage = STAGE_FINAL

                if btn_back_to_ox.is_clicked(event):
                    current_subscripts = list(subscripts)
                    manual_inputs = [
                        str(s) for s in subscripts]
                    feedback = ""
                    stage = STAGE_INIT

            elif stage == STAGE_FINAL:
                if btn_predict.is_clicked(event):
                    webbrowser.open(
                        "http://ai.eecs.northwestern"
                        ".edu/MPpredictor")
                    feedback = (
                        "Northwestern predictor opened."
                        f" Enter: {final_formula}")
                    feedback_color = SUCCESS_COLOR

                if btn_visualize.is_clicked(event):
                    webbrowser.open(
                        "https://next-gen.materialsproject"
                        ".org/materials")
                    feedback = (
                        "Materials Project opened. "
                        f"Search for: {final_formula}")
                    feedback_color = SUCCESS_COLOR

                if btn_back_to_ox.is_clicked(event):
                    current_subscripts = list(subscripts)
                    manual_inputs = [
                        str(s) for s in subscripts]
                    feedback = ""
                    stage = STAGE_INIT

            if btn_back.is_clicked(event):
                return final_formula

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
    result = run_material_module(test_matrix)
    if result:
        print(f"Final compound: {result}")
    pygame.quit()
