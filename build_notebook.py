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


        def coherent_visibility(U, input_modes, output_modes, samples=4000, seed=7):
            rng = __import__("random").Random(seed)
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


        def svg_visibility_panel(title, labels, quantum_vals, coherent_vals, y_min=-1.1, y_max=1.1):
            width = 980
            height = 360
            margin_left = 70
            margin_right = 20
            margin_top = 45
            margin_bottom = 115
            plot_w = width - margin_left - margin_right
            plot_h = height - margin_top - margin_bottom

            def y_map(v):
                return margin_top + (y_max - v) * plot_h / (y_max - y_min)

            zero_y = y_map(0.0)
            n = len(labels)
            slot = plot_w / max(n, 1)
            bar_w = slot * 0.60

            pieces = [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
                '<rect width="100%" height="100%" fill="white"/>',
                f'<text x="{width/2}" y="26" font-size="22" text-anchor="middle" font-family="Arial">{title}</text>',
                f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="black"/>',
                f'<line x1="{margin_left}" y1="{zero_y}" x2="{margin_left + plot_w}" y2="{zero_y}" stroke="black"/>',
            ]

            for tick in [-1.0, -0.5, 0.0, 0.5, 1.0]:
                y = y_map(tick)
                pieces.append(f'<line x1="{margin_left}" y1="{y}" x2="{margin_left + plot_w}" y2="{y}" stroke="#dddddd"/>')
                pieces.append(f'<text x="{margin_left-10}" y="{y+4}" font-size="11" text-anchor="end" font-family="Arial">{tick:.1f}</text>')

            for i, label in enumerate(labels):
                x_center = margin_left + slot * (i + 0.5)
                x = x_center - bar_w / 2
                y_q = y_map(quantum_vals[i])
                top = min(y_q, zero_y)
                height_rect = abs(zero_y - y_q)
                pieces.append(f'<rect x="{x}" y="{top}" width="{bar_w}" height="{height_rect}" fill="#f8b4b4" stroke="#5a67d8" stroke-width="1.2"/>')

                y_c = y_map(coherent_vals[i])
                pieces.append(f'<circle cx="{x_center}" cy="{y_c}" r="4" fill="#f6e05e" stroke="#444444" stroke-width="1"/>')

                pieces.append(
                    f'<text x="{x_center}" y="{margin_top + plot_h + 14}" font-size="10" text-anchor="end" transform="rotate(-45 {x_center},{margin_top + plot_h + 14})" font-family="Arial">{label}</text>'
                )

            pieces.append(f'<rect x="{width-240}" y="18" width="16" height="10" fill="#f8b4b4" stroke="#5a67d8" stroke-width="1.2"/>')
            pieces.append(f'<text x="{width-218}" y="28" font-size="12" font-family="Arial">Quantum visibility</text>')
            pieces.append(f'<circle cx="{width-112}" cy="24" r="4" fill="#f6e05e" stroke="#444444" stroke-width="1"/>')
            pieces.append(f'<text x="{width-98}" y="28" font-size="12" font-family="Arial">Coherent-state prediction</text>')
            pieces.append("</svg>")
            return "".join(pieces)


        def svg_line_chart(title, x_vals, series, x_label, y_label, y_min=None, y_max=None):
            width = 860
            height = 470
            margin_left = 80
            margin_right = 20
            margin_top = 50
            margin_bottom = 70
            plot_w = width - margin_left - margin_right
            plot_h = height - margin_top - margin_bottom

            all_y = []
            for item in series:
                all_y.extend(item["y"])
            if y_min is None:
                y_min = min(all_y)
            if y_max is None:
                y_max = max(all_y)
            x_min = min(x_vals)
            x_max = max(x_vals)

            def x_map(x):
                return margin_left + (x - x_min) * plot_w / (x_max - x_min)

            def y_map(y):
                return margin_top + (y_max - y) * plot_h / (y_max - y_min)

            pieces = [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
                '<rect width="100%" height="100%" fill="white"/>',
                f'<text x="{width/2}" y="28" font-size="22" text-anchor="middle" font-family="Arial">{title}</text>',
                f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="black"/>',
                f'<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{margin_left + plot_w}" y2="{margin_top + plot_h}" stroke="black"/>',
            ]

            for tick in range(6):
                frac = tick / 5
                y_val = y_min + frac * (y_max - y_min)
                y = y_map(y_val)
                pieces.append(f'<line x1="{margin_left}" y1="{y}" x2="{margin_left + plot_w}" y2="{y}" stroke="#dddddd"/>')
                pieces.append(f'<text x="{margin_left-10}" y="{y+4}" font-size="11" text-anchor="end" font-family="Arial">{y_val:.3f}</text>')

            for x in x_vals:
                x_pos = x_map(x)
                pieces.append(f'<line x1="{x_pos}" y1="{margin_top + plot_h}" x2="{x_pos}" y2="{margin_top + plot_h + 5}" stroke="black"/>')
                pieces.append(f'<text x="{x_pos}" y="{margin_top + plot_h + 20}" font-size="11" text-anchor="middle" font-family="Arial">{x}</text>')

            for item in series:
                pts = " ".join(f"{x_map(x)},{y_map(y)}" for x, y in zip(x_vals, item["y"]))
                pieces.append(f'<polyline fill="none" stroke="{item["color"]}" stroke-width="2.2" stroke-dasharray="{item.get("dash", "none")}" points="{pts}"/>')
                for x, y in zip(x_vals, item["y"]):
                    pieces.append(f'<circle cx="{x_map(x)}" cy="{y_map(y)}" r="4" fill="{item["color"]}" stroke="white" stroke-width="1"/>')

            legend_x = width - 235
            legend_y = 65
            for idx, item in enumerate(series):
                yy = legend_y + idx * 20
                pieces.append(f'<line x1="{legend_x}" y1="{yy}" x2="{legend_x+18}" y2="{yy}" stroke="{item["color"]}" stroke-width="2.2" stroke-dasharray="{item.get("dash", "none")}"/>')
                pieces.append(f'<text x="{legend_x+24}" y="{yy+4}" font-size="12" font-family="Arial">{item["name"]}</text>')

            pieces.append(f'<text x="{width/2}" y="{height-12}" font-size="16" text-anchor="middle" font-family="Arial">{x_label}</text>')
            pieces.append(f'<text x="22" y="{height/2}" font-size="16" text-anchor="middle" transform="rotate(-90 22,{height/2})" font-family="Arial">{y_label}</text>')
            pieces.append("</svg>")
            return "".join(pieces)


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
        ## Exact paper numbers reproduced in this notebook

        The paper explicitly reports several quantitative results in the main text. Some of these can be reproduced exactly from the published matrices, and others are reported summary distances between theory and experiment.

        The table below separates those two cases clearly:

        - **Exact from supplementary matrix**: directly recalculated here from the published unitary.
        - **Reported in paper**: quoted from the paper text because the raw experimental bar heights are not tabulated in the PDF.
        """
    ),
    code(
        """
        reported_rows = [
            ["Worked example P_Q", "0.0017", f"{Pq:.4f}", "Exact from supplementary matrix"],
            ["Worked example P_C", "0.0349", f"{Pc:.4f}", "Exact from supplementary matrix"],
            ["Worked example visibility", "0.951", f"{V:.3f}", "Exact from supplementary matrix"],
            ["Two-photon L1 (Alice vs Bob)", "0.027", "0.027", "Reported in main text"],
            ["Two-photon L1 (coherent vs Bob)", "0.548", "0.548", "Reported in main text"],
            ["Three-photon L1 (Alice vs Bob)", "0.122", "0.122", "Reported in main text"],
            ["Three-photon L1 (coherent vs Bob)", "0.358", "0.358", "Reported in main text"],
            ["Colliding-output L1 (Alice vs Bob)", "0.153", "0.153", "Reported in main text"],
            ["Colliding-output L1 (coherent vs Bob)", "0.995", "0.995", "Reported in main text"],
        ]

        display_table(reported_rows, headers=["Quantity", "Paper", "Notebook", "Status"])
        """
    ),
    md(
        r"""
        ## Comparison with coherent-state visibility

        A central conceptual point in the paper is the comparison between Bob's measured visibility and Alice's coherent-state visibility.

        Bob's data are compared with **Alice's coherent-state visibility** in order to rule out the possibility that the observed interference pattern is merely a classical-wave effect of the same interferometer.

        Alice is allowed only classical resources. Coherent states are the most natural classical-optics inputs for a linear network:

        - they let Alice characterize the unitary efficiently,
        - they propagate through the same interferometer,
        - but they do **not** produce the same many-boson interference statistics as Fock-state photon inputs.

        The comparison has a very specific purpose:

        - if Bob matched both the Fock-state prediction and the coherent-state prediction, the result would not certify genuinely bosonic interference;
        - if Bob matches the Fock-state prediction but **disagrees strongly** with the coherent-state prediction, then the measured distribution is genuinely quantum and not just classical field interference.

        This is exactly why the paper emphasizes the large $L_1$ gaps between Bob's measured visibilities and Alice's coherent-state visibilities.

        ### Physical motivation

        The experiment has two different theoretical baselines:

        1. **BosonSampling baseline**:
           identical single-photon Fock-state inputs interfere with amplitudes given by permanents.

        2. **Classical-wave baseline**:
           coherent states pass through the same unitary, but their correlations are computed from phase-averaged field intensities rather than many-boson amplitudes.

        The second comparison is important because the interferometer itself is linear. It is therefore necessary to show that the measured output pattern is not simply something that a classical optical field would also produce in the same circuit. The coherent-state calculation addresses that possibility directly.

        ### Mathematical derivation from the supplementary material

        For equal-amplitude coherent-state inputs in the occupied input modes,

        $$
        E_i = e^{i\theta_i},
        $$

        the electric field at output mode $j$ is

        $$
        E_j = \sum_i U_{ij} E_i.
        $$

        This is Eq. (8) of the supplementary material.

        When the coherent states overlap at zero delay, the phase-averaged $2n$-th order correlation at the chosen output modes is

        $$
        P(0)=\frac{1}{(2\pi)^n}\int_0^{2\pi}\cdots\int_0^{2\pi}
        \prod_j |E_j|^2 \, d\theta_1 \cdots d\theta_n.
        $$

        This is Eq. (9).

        When the inputs are delayed far beyond the coherence length, interference is removed and the correlation becomes an incoherent sum:

        $$
        P(1)=\frac{1}{(2\pi)^n}\int_0^{2\pi}\cdots\int_0^{2\pi}
        \prod_j \left(\sum_i |E_j^{(i)}|^2 \right)\, d\theta_1 \cdots d\theta_n.
        $$

        This is Eq. (10), where $E_j^{(i)}$ is the field at output $j$ due to input mode $i$ alone.

        The coherent-state visibility is then defined analogously to the photon case:

        $$
        V_{\mathrm{coh}} = \frac{P(1)-P(0)}{P(1)}.
        $$

        This is Eq. (11).

        Alice's coherent-state prediction is therefore **not** the BosonSampling prediction. It is a deliberately classical comparison built from the same measured unitary, included to demonstrate that Bob's observed statistics cannot be explained by classical optical interference alone.
        """
    ),
    md(
        r"""
        ## Why visibility preserves the original aim of the experiment

        The original BosonSampling task is formulated in terms of output probabilities. The paper, however, compares theory and experiment primarily through **visibility** rather than raw coincidence counts. This does not change the aim of the experiment. Instead, it provides a more robust way to test the same physical statement:

        > the output statistics of the device are governed by bosonic interference predicted from the measured unitary.

        Visibility is a normalized observable that removes detector-efficiency bias while preserving the difference between

        - the indistinguishable-photon distribution, and
        - the distinguishable-photon distribution.

        In this sense, visibility is a normalized way of comparing the same two probability laws that BosonSampling theory predicts.

        ### Why raw counts are not the preferred observable

        In the paper, the detectors do not all have identical efficiencies. If one output channel has a worse detector, its raw coincidence counts will be artificially smaller even if the underlying physical probability is correct.

        So a direct comparison of raw counts would mix together two effects:

        - the genuine BosonSampling probability of that output event,
        - the detection efficiency of that specific channel.

        The paper explicitly says that raw coincident photon counts are strongly affected by detector-efficiency differences. To remove this effect, they use non-classical interference visibility.

        ### Mathematical derivation

        Let the true event probabilities for a fixed output configuration $T$ be

        $$
        P_T^Q \quad \text{for indistinguishable photons,}
        $$

        and

        $$
        P_T^C \quad \text{for distinguishable photons.}
        $$

        Suppose the total detection efficiency for that same output pattern is $\eta_T$.
        Then the measured count rates are proportional to

        $$
        C_T^Q = \eta_T P_T^Q,
        \qquad
        C_T^C = \eta_T P_T^C.
        $$

        Now define visibility from the measured counts:

        $$
        V_T
        = \frac{C_T^C - C_T^Q}{C_T^C}.
        $$

        Substituting the efficiency-weighted counts gives

        $$
        V_T
        = \frac{\eta_T P_T^C - \eta_T P_T^Q}{\eta_T P_T^C}
        = \frac{P_T^C - P_T^Q}{P_T^C}.
        $$

        So the unknown detector factor $\eta_T$ cancels exactly.

        This is the key reason visibility preserves the aim of the experiment:

        - it still compares the **same underlying probabilities** $P_T^Q$ and $P_T^C$,
        - while removing an experimental nuisance parameter that would otherwise distort the comparison.

        ### Why this still tests BosonSampling theory

        BosonSampling theory predicts $P_T^Q$ from permanents of submatrices of the measured unitary.
        The distinguishable reference $P_T^C$ is computed from the same unitary but without bosonic interference.

        Therefore,

        $$
        V_T = \frac{P_T^C - P_T^Q}{P_T^C}
        $$

        is still a direct function of the BosonSampling prediction.

        If Alice's predicted visibilities agree with Bob's measured visibilities, then the experiment confirms that the underlying quantum-versus-classical probability difference is the one expected from bosonic interference.

        The experiment is therefore **not** abandoning the original aim. It is measuring a normalized observable that faithfully captures the same physics in a detector-robust way.
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
        ## Figure-style theory plots for the paper's listed inputs

        The next two cells build figure-inspired visualizations similar to Figs. 2 and 3:

        - blue-outlined bars: permanent-based quantum visibility predictions,
        - yellow circles: coherent-state visibility predictions computed from the supplementary formulas,
        - x-axis labels: output mode combinations.

        These are **theory reproductions**. They do not yet include Bob's measured orange bars because the paper PDF does not provide a machine-readable table of the experimental values.
        """
    ),
    code(
        """
        two_photon_inputs = [(1, 3), (2, 6), (4, 6)]

        for input_modes in two_photon_inputs:
            S2 = occ_from_modes(input_modes)
            labels = []
            quantum_vis = []
            coherent_vis = []
            for out_modes, T2 in choose_noncolliding_outputs(2, m=6):
                Pq, _ = quantum_probability(U2, S2, T2)
                Pc = classical_probability_noncolliding(U2, S2, T2)
                labels.append("{" + ",".join(map(str, out_modes)) + "}")
                quantum_vis.append(visibility(Pc, Pq))
                coherent_vis.append(coherent_visibility(U2, input_modes, out_modes))

            title = f"Two-photon visibility structure for input {{{','.join(map(str, input_modes))}}}"
            show_svg(svg_visibility_panel(title, labels, quantum_vis, coherent_vis))
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
    code(
        """
        three_photon_inputs = [(1, 3, 5), (1, 4, 6), (1, 5, 6)]

        for input_modes in three_photon_inputs:
            S3 = occ_from_modes(input_modes)
            labels = []
            quantum_vis = []
            coherent_vis = []
            for out_modes, T3 in choose_noncolliding_outputs(3, m=6):
                Pq, _ = quantum_probability(U3, S3, T3)
                Pc = classical_probability_noncolliding(U3, S3, T3)
                labels.append("{" + ",".join(map(str, out_modes)) + "}")
                quantum_vis.append(visibility(Pc, Pq))
                coherent_vis.append(coherent_visibility(U3, input_modes, out_modes, samples=3000))

            title = f"Three-photon visibility structure for input {{{','.join(map(str, input_modes))}}}"
            show_svg(svg_visibility_panel(title, labels, quantum_vis, coherent_vis))
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
        ## Recreated Fig. 5 trend from the paper

        The main text and caption of Fig. 5 describe how source brightness changes the distance between:

        - Bob's measurements and Alice's ideal Fock-state predictions,
        - Bob's measurements and Alice's coherent-state predictions.

        The next plot uses the **paper's plotted points transcribed from Fig. 5** to recreate the qualitative trend. These values are useful for project discussion and visualization, but unlike the worked permanent example they are not exact table values published in the PDF text.
        """
    ),
    code(
        """
        pump_power = [10, 20, 50, 100]
        l1_fock_5nm = [0.188, 0.199, 0.218, 0.245]
        l1_coherent_5nm = [0.229, 0.228, 0.210, 0.204]

        series = [
            {"name": "L1: Fock prediction vs Bob (5 nm filter)", "y": l1_fock_5nm, "color": "#e53e3e", "dash": "8,6"},
            {"name": "L1: coherent-state prediction vs Bob (5 nm filter)", "y": l1_coherent_5nm, "color": "#2d3748", "dash": "2,4"},
        ]

        show_svg(
            svg_line_chart(
                "Recreated Fig. 5 trend: imperfect Fock states in Boson Sampling",
                pump_power,
                series,
                x_label="Pump power (%)",
                y_label="L1 norm",
                y_min=0.0,
                y_max=0.28,
            )
        )

        display_table(
            [
                [10, "0.188", "0.229"],
                [20, "0.199", "0.228"],
                [50, "0.218", "0.210"],
                [100, "0.245", "0.204"],
            ],
            headers=["Pump power (%)", "Fock vs Bob (approx. from figure)", "Coherent vs Bob (approx. from figure)"],
        )
        print()
        print("Additional Fig. 5 points visible at 20% pump in the paper image:")
        print("- 2 nm filter: Fock vs Bob is approximately 0.095")
        print("- 2 nm filter: coherent vs Bob is approximately 0.260")
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

        What is exact here:

        - the unitary matrices from the supplementary material,
        - the permanent-based worked example,
        - the quantum visibility predictions for chosen inputs,
        - the coherent-state predictions computed from the supplementary formulas.

        What is still approximate:

        - the recreated Fig. 5 pump-power points, which are transcribed from the published figure image,
        - Bob's per-output experimental visibilities in Figs. 2 to 4, which would require digitization or raw data to reproduce exactly.
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
