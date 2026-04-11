import json
from pathlib import Path


NOTEBOOK = Path("Report.ipynb")


CELL_4 = """import numpy as np
import itertools
import time
from pathlib import Path
import matplotlib.pyplot as plt

PNG_OUTPUT_DIR = Path("png_plots")
PNG_OUTPUT_DIR.mkdir(exist_ok=True)

def calculate_permanent_naive(A):
    \"""
    Calculates the permanent of a matrix using the naive O(n!) definition.
    This directly mirrors the mathematical formula (summing over all permutations)
    without the alternating sign term used in determinants.
    \"""
    n = A.shape[0]
    perm = 0
    
    # Iterate over all possible permutations of the columns
    for p in itertools.permutations(range(n)):
        # Calculate the product of the elements for this specific permutation
        prod = 1
        for i in range(n):
            prod *= A[i, p[i]]
        perm += prod
        
    return perm

# Matrix sizes to benchmark
# Warning: Do not push this much past 10! 
# 10! = 3,628,800 permutations. 11! = 39,916,800 (will take a minute or two).
sizes = [2, 4, 5, 6, 8, 10]

det_times = []
perm_times = []

print("Running complexity benchmarks...")

for n in sizes:
    # Generate a random n x n matrix
    A = np.random.rand(n, n)
    
    # --- Benchmark Determinant ---
    start_det = time.perf_counter()
    np.linalg.det(A) # NumPy uses highly optimized O(n^3) algorithms
    end_det = time.perf_counter()
    det_times.append(end_det - start_det)
    
    # --- Benchmark Permanent ---
    start_perm = time.perf_counter()
    calculate_permanent_naive(A) # Our naive O(n!) implementation
    end_perm = time.perf_counter()
    perm_times.append(end_perm - start_perm)
    
    print(f"Size {n:>2}x{n:<2} | Det Time: {det_times[-1]:.6f}s | Perm Time: {perm_times[-1]:.6f}s")

# --- Plotting the Results ---
plt.figure(figsize=(10, 6))

# We use a logarithmic scale for the y-axis because the difference in time
# becomes so massive that a linear scale would squish the determinant line flat.
plt.plot(sizes, det_times, marker='o', label='Determinant $\\mathcal{O}(n^3)$', color='#007acc', linewidth=2)
plt.plot(sizes, perm_times, marker='o', label='Permanent $\\mathcal{O}(n!)$', color='#e63946', linewidth=2)

plt.yscale('log')
plt.xlabel('Matrix Size ($n \\\\times n$)', fontsize=12)
plt.ylabel('Time taken (seconds) - Log Scale', fontsize=12)
plt.title('The Complexity Chasm: Determinant vs. Permanent', fontsize=14, pad=15)
plt.xticks(sizes)
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.tight_layout()
plt.savefig(PNG_OUTPUT_DIR / "complexity_chasm_determinant_vs_permanent.png", dpi=220, bbox_inches="tight")

plt.show()
"""


CELL_20 = """import cmath
import itertools
import math
import random
import re
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


PNG_OUTPUT_DIR = Path("png_plots")
PNG_OUTPUT_DIR.mkdir(exist_ok=True)


def permanent(matrix):
    n = len(matrix)
    if n == 0:
        return 1
    total = 0j
    for perm in itertools.permutations(range(n)):
        term = 1 + 0j
        for i in range(n):
            term *= matrix[i][perm[i]]
        total += term
    return total


def build_submatrix(U, input_occ, output_occ):
    cols = []
    for j, count in enumerate(output_occ):
        cols.extend([j] * count)

    rows = []
    for i, count in enumerate(input_occ):
        rows.extend([i] * count)

    return [[U[i][j] for j in cols] for i in rows]


def factorial_product(occ):
    out = 1
    for x in occ:
        out *= math.factorial(x)
    return out


def quantum_probability(U, input_occ, output_occ):
    sub = build_submatrix(U, input_occ, output_occ)
    amp = permanent(sub)
    norm = math.sqrt(factorial_product(input_occ) * factorial_product(output_occ))
    return (abs(amp) ** 2) / (norm ** 2), sub


def classical_probability(U, input_occ, output_occ):
    sub = build_submatrix(U, input_occ, output_occ)
    weight = [[abs(z) ** 2 for z in row] for row in sub]
    return permanent(weight).real


def visibility(Pc, Pq):
    if abs(Pc) < 1e-15:
        return float("nan")
    return ((Pc - Pq) / Pc).real


def occ_from_modes(modes, m=6):
    occ = [0] * m
    for mode in modes:
        occ[mode - 1] += 1
    return tuple(occ)


def choose_noncolliding_outputs(n, m=6):
    for combo in itertools.combinations(range(1, m + 1), n):
        yield combo, occ_from_modes(combo, m=m)


def coherent_visibility(U, input_modes, output_modes, samples=4000, seed=7):
    rng = random.Random(seed)
    input_idx = [m - 1 for m in input_modes]
    output_idx = [m - 1 for m in output_modes]

    p0 = 0.0
    for _ in range(samples):
        phases = [rng.uniform(0.0, 2.0 * math.pi) for _ in input_idx]
        prod = 1.0
        for out_j in output_idx:
            amp = 0j
            for idx, in_i in enumerate(input_idx):
                amp += U[in_i][out_j] * cmath.exp(1j * phases[idx])
            prod *= abs(amp) ** 2
        p0 += prod
    p0 /= samples

    p_inf = 1.0
    for out_j in output_idx:
        incoherent_intensity = sum(abs(U[in_i][out_j]) ** 2 for in_i in input_idx)
        p_inf *= incoherent_intensity

    return visibility(p_inf, p0)


def display_table(rows, headers):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    def fmt(row):
        return " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))

    print(fmt(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt(row))


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")


def save_png(fig, filename):
    path = PNG_OUTPUT_DIR / filename
    fig.savefig(path, dpi=220, bbox_inches="tight")
    return path


def show_svg(plot_obj):
    fig, filename = plot_obj
    path = save_png(fig, filename)
    try:
        from IPython.display import Image, display
        display(Image(filename=str(path)))
        plt.close(fig)
    except Exception:
        print(f"Saved PNG to {path}")


def svg_visibility_panel(title, labels, quantum_vals, coherent_vals, y_min=-1.1, y_max=1.1):
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(12.5, 5.2))

    ax.bar(
        x,
        quantum_vals,
        color="#f8b4b4",
        edgecolor="#5a67d8",
        linewidth=1.2,
        label="Quantum visibility",
    )
    ax.scatter(
        x,
        coherent_vals,
        color="#f6e05e",
        edgecolor="#444444",
        s=45,
        zorder=3,
        label="Coherent-state prediction",
    )
    ax.axhline(0.0, color="black", linewidth=1)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_title(title, fontsize=14, pad=12)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    return fig, f"{slugify(title)}.png"


def svg_line_chart(title, x_vals, series, x_label, y_label, y_min=None, y_max=None):
    all_y = []
    for item in series:
        all_y.extend(item["y"])
    if y_min is None:
        y_min = min(all_y)
    if y_max is None:
        y_max = max(all_y)

    fig, ax = plt.subplots(figsize=(10.5, 5.5))
    dash_map = {
        "8,6": (8, 6),
        "2,4": (2, 4),
    }

    for item in series:
        line, = ax.plot(
            x_vals,
            item["y"],
            color=item["color"],
            linewidth=2.2,
            marker="o",
            markersize=6,
            label=item["name"],
        )
        dash = item.get("dash")
        if dash in dash_map:
            line.set_dashes(dash_map[dash])

    ax.set_title(title, fontsize=14, pad=12)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(x_vals)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    return fig, f"{slugify(title)}.png"


U2 = [
    [0.297 + 0.000j,  0.325 + 0.000j,  0.126 + 0.000j,  0.500 + 0.000j,  0.430 + 0.000j,  0.253 + 0.000j],
    [0.330 + 0.000j, -0.302 - 0.011j,  0.001 + 0.503j,  0.028 - 0.390j,  0.221 + 0.118j, -0.385 - 0.213j],
    [0.388 + 0.000j,  0.182 + 0.248j, -0.220 + 0.133j, -0.212 + 0.204j, -0.127 - 0.386j,  0.108 - 0.081j],
    [0.311 + 0.000j, -0.220 - 0.315j, -0.169 - 0.246j,  0.190 + 0.157j, -0.073 - 0.089j, -0.227 + 0.355j],
    [0.396 + 0.000j, -0.222 - 0.169j,  0.387 - 0.130j, -0.265 + 0.004j, -0.103 + 0.202j,  0.353 - 0.112j],
    [0.279 + 0.000j,  0.322 + 0.244j, -0.101 - 0.239j, -0.051 - 0.400j, -0.184 + 0.320j, -0.217 + 0.074j],
]

U3 = [
    [0.334 + 0.000j,  0.277 + 0.000j,  0.125 + 0.000j,  0.479 + 0.000j,  0.415 + 0.000j,  0.237 + 0.000j],
    [0.273 + 0.000j, -0.329 - 0.051j,  0.055 + 0.478j,  0.021 - 0.121j,  0.197 + 0.128j, -0.345 - 0.253j],
    [0.420 + 0.000j,  0.140 + 0.242j, -0.191 + 0.198j, -0.195 + 0.204j, -0.139 - 0.393j,  0.113 - 0.085j],
    [0.284 + 0.000j, -0.197 - 0.367j, -0.194 - 0.224j,  0.189 + 0.190j, -0.072 - 0.106j, -0.278 + 0.333j],
    [0.340 + 0.000j, -0.329 - 0.049j,  0.328 - 0.312j, -0.144 + 0.042j, -0.131 + 0.187j,  0.283 - 0.216j],
    [0.324 + 0.000j,  0.344 + 0.036j, -0.114 - 0.101j, -0.206 - 0.398j, -0.111 + 0.351j, -0.098 + 0.208j],
]

print("Helpers and measured unitaries loaded. PNG plots will be saved to png_plots/.")
"""


def main():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    nb["cells"][4]["source"] = CELL_4.splitlines(keepends=True)
    nb["cells"][20]["source"] = CELL_20.splitlines(keepends=True)
    NOTEBOOK.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
