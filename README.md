# Celestial Cipher

An educational videogame bridging astronomical observation and computational molecular science, developed as a companion to the research paper "Gamifying Computational Predictions: From Celestial Spheres to Molecular Domains", Journal of Electrical Systems and Information Technology, in press, 2026.

---

## Overview

Players navigate two silhouetted characters through a mysterious abandoned house, capturing images of the real-time celestial sphere and converting them into predictions of material and protein properties through integrated open-access computational platforms.

---

## Description

Celestial Cipher is an educational videogame that bridges the vastness of astronomical observation with the intimacy of molecular science, guiding players through an immersive journey from the starry sky to the computational prediction of material and protein properties. Players navigate two silhouetted characters – a boy and a girl – through the rooms of a mysterious abandoned house. The journey begins in the attic, where the ceiling, walls and floor become transparent, opening a panoramic view of the real-time celestial sphere rendered through an integrated astronomical platform. Players capture images of the starry sky, selecting a central celestial object and allowing the game to construct a celestial distance matrix – a 3 x 3 numerical array encoding the apparent pixel distances between the selected object and the nine brightest celestial bodies in its vicinity.
This matrix serves as the generative seed for everything that follows. It is first transformed into an abstract expressionist artwork through a sequence of visual operations applied to the captured image, offering the player a creative intermediary between the astronomical and the molecular. The player then descends through atmospheric corridors filled with animated mystify-like patterns and floating philosophical fragments drawn from a vast literary source, before arriving at the basement, where two computational rooms await. In the Crystal Room, the matrix entries are translated into a ternary chemical compound via an arithmetic mapping, and the predicted material properties of the compound are retrieved in real time from an open-access neural network platform. In the Protein Room, the same matrix drives a combinatorial algorithm that generates a polypeptide sequence of variable length, whose secondary and tertiary structure and physicochemical properties are computed through integrated platforms including AlphaFold2, ExPASy ProtParam, Jpred 4 and EMBOSS Pepinfo. The game supports both single-player and two-player modes, with the latter enabling the merging of two independently captured celestial matrices into a shared compound prediction. It is built entirely in Python using Pygame and integrates exclusively open-access scientific platforms, embedding open-science principles into the gameplay experience. Celestial Cipher demonstrates that computational science can be made accessible, engaging and visually immersive for audiences ranging from K-12 students to advanced researchers.

---

## Gameplay

Attic — Capture starry sky images via Stellarium
↓
Celestial distance matrix constructed
↓
Abstract artwork generated from matrix
↓
Corridor — Atmospheric passage with philosophical fragments
↓
Basement — Two computational rooms
↓
Crystal Room — Material property prediction
Protein Room — Protein sequence and structure prediction

---

## Requirements

### Python Version
Python 3.10 or higher

### Required Libraries
Install all dependencies with:

pip install pygame numpy pillow scipy pyperclip python-docx

| Library | Purpose |
|---------|---------|
| `pygame` | Game engine |
| `numpy` | Matrix operations and image processing |
| `pillow` | Image loading and manipulation |
| `scipy` | Star detection algorithms |
| `pyperclip` | Clipboard operations |

---

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/CelestialCipher

2. Navigate to the game folder:
cd CelestialCipher

3. Install dependencies:
pip install pygame numpy pillow scipy pyperclip

4. Run the game:
python game.py

Or double click `run.bat` on Windows.

---

## How to Play

### One Player Mode
1. Launch the game and click through the intro screen
2. Select **1 Player** on the player selection screen
3. In the attic click **Open Stellarium** to open the astronomical platform in your browser
4. Navigate to a region of the starry sky and take a screenshot
5. Return to the game and click **Paste Screenshot** or **Load Image**
6. Click on a central celestial object in the image
7. The game automatically identifies surrounding objects and constructs a 3x3 celestial distance matrix
8. Proceed to the artwork conversion screen then through the corridor to the basement
9. Enter the **Crystal Room** to predict material properties or the **Protein Room** to generate and analyze a protein sequence

### Two Player Mode
1. Select **2 Players** on the player selection screen
2. Each player captures their own celestial image using the two portals in the attic
3. The two matrices are automatically merged element-wise
4. The merged matrix drives all subsequent predictions

---

## External Platforms Integrated

| Platform | Purpose |
|----------|---------|
| [Stellarium Web](https://stellarium-web.org) | Real-time celestial sphere observation |
| [Northwestern Materials Property Predictor](http://ai.eecs.northwestern.edu/MPpredictor) | Material property prediction |
| [Crystallography Open Database](https://crystallography.net) | Crystal structure retrieval |
| [ColabFold / AlphaFold2](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb) | Protein tertiary structure prediction |
| [ExPASy ProtParam](https://web.expasy.org/protparam/) | Protein physicochemical properties |
| [Jpred 4](https://www.compbio.dundee.ac.uk/jpred/) | Protein secondary structure prediction |
| [EMBOSS Pepinfo](https://www.ebi.ac.uk/Tools/seqstats/emboss_pepinfo/) | Protein sequence analysis |

---

## File Structure

CelestialCipher/
│
├── game.py                 ← Main game file
├── matrix_module.py        ← Celestial distance matrix construction
├── material_module.py      ← Material property mapping
├── protein_module.py       ← Protein sequence mapping
├── run.bat                 ← Windows launcher
├── README.md               ← This file
├── LICENSE                 ← CC BY-NC 4.0
│
├── Figure 1.jpg            ← Intro screen
├── Figure 3a.jpg           ← Matrix module placeholder
├── Figure 3b.jpg           ← Player selection screen
├── Figure 5.jpg            ← Corridor intro screen
├── Figure 6.jpg            ← Crystal room intro screen
└── Figure 8.jpg            ← Protein room intro screen

---

## Scientific Workflow

### Material Prediction
Each row of the 3x3 matrix is mapped to a chemical element using the formula:

Z = a × b + c

Where `a`, `b`, `c` are the three values in the row and `Z` is the atomic number of the resulting element. Noble gases are replaced with hydrogen. The resulting ternary compound formula is submitted to the Northwestern Materials Property Predictor.

### Protein Prediction
The matrix values are used to generate combinatorial sums which are mapped to amino acids ordered by electron density volume. Sequence lengths of 9, 36, 84, 120, 210 or 255 residues are available. The resulting sequence is submitted to AlphaFold2, ExPASy, Jpred 4 and EMBOSS Pepinfo.

---

## Two Player Matrix Merging

In two player mode the matrices are merged element-wise:

merged[i][j] = (m1[i][j] + m2[i][j]) % 10

If the result is 0 it is replaced with 10 and then clamped to the 1-9 range.

---

## Citation

If you use this software in your research please cite:

Vuk Uskoković (2025). Celestial Cipher: An Educational Videogame
for Computational Material and Protein Property Prediction.
GitHub repository: https://github.com/uskokovic12/CelestialCipher

---

## License

This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

You are free to share and adapt this material for non-commercial purposes provided appropriate credit is given.

---

## Acknowledgements

- Astronomical observation powered by [Stellarium Web](https://stellarium-web.org)
- Material property predictions powered by the Northwestern University Materials Property Predictor
- Protein structure predictions powered by AlphaFold2 via ColabFold
- Character and scenography imagery generated with [Craiyon](https://www.craiyon.com)

---

## Contact

For questions or collaboration opportunities please contact Vuk Uskoković at vuk21@yahoo.com.
