import json
from textwrap import dedent


CELL_COUNTER = 0


def md(text: str) -> dict:
    global CELL_COUNTER
    CELL_COUNTER += 1
    return {
        "cell_type": "markdown",
        "id": f"cell-{CELL_COUNTER}",
        "metadata": {},
        "source": dedent(text).strip("\n").splitlines(keepends=True),
    }


def code(text: str) -> dict:
    global CELL_COUNTER
    CELL_COUNTER += 1
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": f"cell-{CELL_COUNTER}",
        "metadata": {},
        "outputs": [],
        "source": dedent(text).strip("\n").splitlines(keepends=True),
    }


cells = [
    md(
        """
        # Executable Paper: Photonic Boson Sampling in a Tunable Circuit

        This notebook is a compact executable companion to the paper **"Photonic Boson Sampling in a Tunable Circuit"** by Broome *et al.* It focuses on the parts of the paper that can be reproduced directly from the published text:

        - the measured 6x6 optical network matrices from the supplementary material,
        - the permanent-based formula for bosonic scattering,
        - the classical distinguishable-particle comparison,
        - the visibility formula used throughout the paper,
        - a small source-imperfection model based on the SPDC expansion in Eq. (12).

        The notebook avoids external dependencies and uses only the Python standard library so it stays runnable on a clean Jupyter setup.
        """
    ),
    md(
        """
        ## What the paper shows

        Boson Sampling studies how identical bosons scatter through a linear optical network. The key physical and computational point is that **indistinguishable bosons interfere with amplitudes given by matrix permanents**, while distinguishable particles do not.

        In the paper:

        - Alice characterizes the optical network and computes output probabilities classically.
        - Bob injects photons into the actual circuit and measures the output statistics.
        - Agreement between Alice's permanent-based predictions and Bob's measurements supports the Boson Sampling model.

        For the non-colliding outputs emphasized in the main paper, the probability is

        $$
        P_Q(T) = |\\mathrm{Per}(U_{ST})|^2
        $$

        while the distinguishable-particle comparison is

        $$
        P_C(T) = \\mathrm{Per}(\\widetilde{U}_{ST}),
        \\quad
        \\widetilde{U}_{ST,ij} = |(U_{ST})_{ij}|^2.
        $$

        The non-classical visibility is

        $$
        V_T = \\frac{P_C(T)-P_Q(T)}{P_C(T)}.
        $$
        """
    ),
    code(
        """
        import cmath
        import itertools
        import math


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
            result = 1
            for x in occ:
                result *= math.factorial(x)
            return result


        def quantum_probability(U, input_occ, output_occ):
            sub = build_submatrix(U, input_occ, output_occ)
            amp = permanent(sub)
            norm = math.sqrt(factorial_product(input_occ) * factorial_product(output_occ))
            return (abs(amp) ** 2) / (norm ** 2), sub


        def classical_probability_noncolliding(U, input_occ, output_occ):
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


        def format_complex(z):
            return f"{z.real:+.3f}{z.imag:+.3f}i"


        def print_matrix(M):
            for row in M:
                print("[" + ", ".join(format_complex(z) for z in row) + "]")


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


        def svg_bar_chart(title, labels, values_a, values_b=None, name_a="Quantum", name_b="Classical"):
            width = 960
            height = 420
            margin_left = 70
            margin_right = 20
            margin_top = 55
            margin_bottom = 120
            plot_w = width - margin_left - margin_right
            plot_h = height - margin_top - margin_bottom
            vmax = max(values_a + (values_b if values_b else [0])) or 1.0

            def bar_height(v):
                return (v / vmax) * plot_h

            n = len(labels)
            slot = plot_w / max(n, 1)
            bar_w = slot * (0.34 if values_b else 0.60)

            pieces = [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
                '<rect width="100%" height="100%" fill="white"/>',
                f'<text x="{width/2}" y="28" font-size="22" text-anchor="middle" font-family="Arial">{title}</text>',
                f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="black"/>',
                f'<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" stroke="black"/>',
            ]

            for tick in range(6):
                yv = vmax * tick / 5
                y = margin_top + plot_h - (plot_h * tick / 5)
                pieces.append(f'<line x1="{margin_left-5}" y1="{y}" x2="{margin_left}" y2="{y}" stroke="black"/>')
                pieces.append(f'<text x="{margin_left-10}" y="{y+4}" font-size="11" text-anchor="end" font-family="Arial">{yv:.3f}</text>')

            for i, label in enumerate(labels):
                x_center = margin_left + slot * (i + 0.5)
                if values_b:
                    x1 = x_center - bar_w - 2
                    x2 = x_center + 2
                    h1 = bar_height(values_a[i])
                    h2 = bar_height(values_b[i])
                    y1 = margin_top + plot_h - h1
                    y2 = margin_top + plot_h - h2
                    pieces.append(f'<rect x="{x1}" y="{y1}" width="{bar_w}" height="{h1}" fill="#2b6cb0"/>')
                    pieces.append(f'<rect x="{x2}" y="{y2}" width="{bar_w}" height="{h2}" fill="#dd6b20"/>')
                else:
                    x = x_center - bar_w / 2
                    h = bar_height(values_a[i])
                    y = margin_top + plot_h - h
                    pieces.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" fill="#2b6cb0"/>')

                pieces.append(
                    f'<text x="{x_center}" y="{margin_top + plot_h + 16}" font-size="10" text-anchor="end" transform="rotate(-45 {x_center},{margin_top + plot_h + 16})" font-family="Arial">{label}</text>'
                )

            if values_b:
                lx = width - 210
                ly = 42
                pieces.append(f'<rect x="{lx}" y="{ly}" width="14" height="14" fill="#2b6cb0"/>')
                pieces.append(f'<text x="{lx+20}" y="{ly+12}" font-size="12" font-family="Arial">{name_a}</text>')
                pieces.append(f'<rect x="{lx+90}" y="{ly}" width="14" height="14" fill="#dd6b20"/>')
                pieces.append(f'<text x="{lx+110}" y="{ly+12}" font-size="12" font-family="Arial">{name_b}</text>')

            pieces.append("</svg>")
            return "".join(pieces)


        def show_svg(svg):
            try:
                from IPython.display import SVG, display
                display(SVG(svg))
            except Exception:
                print(svg)


        print("Helpers loaded.")
        """
    ),
    code(
        """
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

        print("Measured 6x6 matrices loaded from the supplementary material.")
        """
    ),
    md(
        """
        ## Worked example from the supplementary material

        The paper explicitly works through the two-photon case

        - input configuration: $S=(1,0,1,0,0,0)$, which means photons enter modes $1$ and $3$,
        - output configuration: $T=(0,1,0,0,1,0)$, which means photons are detected in modes $2$ and $5$.

        The supplementary material reports:

        - $P_Q(T) = 0.0017$,
        - $P_C(T) = 0.0349$,
        - $V = 0.951$.

        We now reproduce that calculation directly.
        """
    ),
    code(
        """
        S = (1, 0, 1, 0, 0, 0)
        T = (0, 1, 0, 0, 1, 0)

        Pq, U_ST = quantum_probability(U2, S, T)
        Pc = classical_probability_noncolliding(U2, S, T)
        V = visibility(Pc, Pq)

        print("Submatrix U_ST:")
        print_matrix(U_ST)
        print()
        print(f"Pq = {Pq:.4f}")
        print(f"Pc = {Pc:.4f}")
        print(f"V  = {V:.3f}")
        """
    ),
    md(
        """
        ## Two-photon Boson Sampling across all non-colliding outputs

        A clean way to reproduce the paper's central idea is to fix one input pair and compare:

        - bosonic probabilities from permanents,
        - distinguishable-particle probabilities,
        - the resulting non-classical visibility.

        Here we choose the input modes $(1,5)$ because that input appears explicitly in Fig. 2 of the paper.
        """
    ),
    code(
        """
        input_modes_2 = (1, 5)
        S2 = occ_from_modes(input_modes_2)

        rows = []
        labels = []
        quantum_vals = []
        classical_vals = []
        visibility_vals = []

        for out_modes, T2 in choose_noncolliding_outputs(2, m=6):
            Pq, _ = quantum_probability(U2, S2, T2)
            Pc = classical_probability_noncolliding(U2, S2, T2)
            V = visibility(Pc, Pq)
            label = "{" + ",".join(map(str, out_modes)) + "}"
            labels.append(label)
            quantum_vals.append(Pq)
            classical_vals.append(Pc)
            visibility_vals.append(V)
            rows.append([label, f"{Pq:.4f}", f"{Pc:.4f}", f"{V:.3f}"])

        display_table(rows, headers=["Output", "Pq", "Pc", "Visibility"])
        show_svg(svg_bar_chart("Two-photon output probabilities for input {1,5}", labels, quantum_vals, classical_vals))
        show_svg(svg_bar_chart("Two-photon visibilities for input {1,5}", labels, visibility_vals))
        """
    ),
    md(
        """
        ## Three-photon Boson Sampling across all non-colliding outputs

        For the three-photon case we use the input modes $(1,3,5)$, which also appears in the paper. We evaluate all $\\binom{6}{3}=20$ non-colliding outputs.
        """
    ),
    code(
        """
        input_modes_3 = (1, 3, 5)
        S3 = occ_from_modes(input_modes_3)

        rows = []
        labels = []
        quantum_vals = []
        classical_vals = []
        visibility_vals = []

        for out_modes, T3 in choose_noncolliding_outputs(3, m=6):
            Pq, _ = quantum_probability(U3, S3, T3)
            Pc = classical_probability_noncolliding(U3, S3, T3)
            V = visibility(Pc, Pq)
            label = "{" + ",".join(map(str, out_modes)) + "}"
            labels.append(label)
            quantum_vals.append(Pq)
            classical_vals.append(Pc)
            visibility_vals.append(V)
            rows.append([label, f"{Pq:.4f}", f"{Pc:.4f}", f"{V:.3f}"])

        display_table(rows, headers=["Output", "Pq", "Pc", "Visibility"])
        show_svg(svg_bar_chart("Three-photon output probabilities for input {1,3,5}", labels, quantum_vals, classical_vals))
        show_svg(svg_bar_chart("Three-photon visibilities for input {1,3,5}", labels, visibility_vals))
        """
    ),
    md(
        """
        ## A compact derivation for source imperfections

        The paper models spontaneous parametric down-conversion as

        $$
        |\\psi\\rangle \\propto |00\\rangle + \\eta |11\\rangle + \\eta^2 |22\\rangle + \\eta^3 |33\\rangle + \\cdots
        $$

        The higher-order terms become more important as the source gets brighter. The next cell visualizes the relative weights of the first few pair-number sectors after normalization.
        """
    ),
    code(
        """
        def spdc_weights(eta, max_pairs=3):
            raw = [eta ** (2 * n) for n in range(max_pairs + 1)]
            total = sum(raw)
            return [x / total for x in raw]


        eta_values = [0.05, 0.10, 0.20, 0.35]

        for eta in eta_values:
            weights = spdc_weights(eta, max_pairs=3)
            labels = ["0 pairs", "1 pair", "2 pairs", "3 pairs"]
            print(f"eta = {eta:.2f}")
            display_table(
                [[labels[i], f"{weights[i]:.6f}"] for i in range(len(labels))],
                headers=["Sector", "Normalized weight"],
            )
            show_svg(svg_bar_chart(f"SPDC sector weights for eta = {eta:.2f}", labels, weights))
            print()
        """
    ),
    md(
        """
        ## Takeaways

        This executable notebook reproduces the main calculational logic of the paper:

        - measured interferometer matrices are used as direct input,
        - permanents generate bosonic output probabilities,
        - distinguishable-particle probabilities provide the classical baseline,
        - visibility cleanly quantifies non-classical interference,
        - higher-order SPDC terms explain why larger source brightness pushes the experiment away from the ideal Fock-state limit.

        A natural extension for a project report is to add:

        - manual transcription of selected measured bars from Figs. 2 to 5,
        - an $L_1$-distance calculation against those experimental points,
        - a short discussion of why permanents make Boson Sampling hard for classical computers.
        """
    ),
]


notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.x",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


with open("boson_sampling_executable_paper.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2)

print("Wrote boson_sampling_executable_paper.ipynb")
