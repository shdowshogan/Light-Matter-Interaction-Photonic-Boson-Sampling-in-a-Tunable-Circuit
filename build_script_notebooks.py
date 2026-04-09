import json
from textwrap import dedent


def md_cell(text, cell_id):
    return {
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": dedent(text).strip("\n").splitlines(keepends=True),
    }


def write_notebook(path, title, sections):
    cells = [md_cell(f"# {title}", "title")]
    for idx, (heading, body) in enumerate(sections, start=1):
        cells.append(md_cell(f"## {heading}\n\n{body}", f"cell-{idx}"))

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

    with open(path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)


ashok_sections = [
    (
        "Opening",
        """
        Now I’ll present the figure-reproduction part of our project notebook. In this section, our goal is to show how the main plots in the paper arise from the Boson Sampling formalism and from the measured unitary matrices given in the supplementary material.

        This notebook focuses on the figures most relevant to the paper’s core results, namely Figures 2, 3, 4, and 5. For each one, we explain what is being reproduced, how the numbers are obtained, and what the plot tells us physically.
        """,
    ),
    (
        "Scope",
        """
        Before going into the plots, I want to clarify what exactly is reproduced here. The matrix-based theory calculations are reproduced directly from the paper’s supplementary material. That includes the permanent-based bosonic probabilities, the distinguishable-particle probabilities, and the visibility predictions.

        The summary L1 distances quoted in the main text are also included exactly as reported. For Figure 5, the overall trend is recreated from the published graph, so that part should be understood as a graphical reconstruction. And for Bob’s individual measured bars in Figures 2 to 4, the PDF does not provide a machine-readable numerical table, so what we reproduce here is the theoretical structure of those figures.
        """,
    ),
    (
        "Figure 2(a)",
        """
        This cell reproduces the worked example from the supplementary material. The input configuration is one photon in mode 1 and one photon in mode 3, and the output configuration is one photon in mode 2 and one photon in mode 5.

        The important point here is that the paper’s logic starts from the measured unitary matrix. From that unitary, we build the relevant submatrix corresponding to the chosen input and output occupations. Then we compute two quantities.

        First, the quantum probability, which depends on the permanent of the submatrix. Second, the distinguishable-particle probability, which is computed using the permanent of the mod-squared matrix.

        From these two probabilities, we calculate the visibility. The notebook reproduces the same values reported in the paper: P subscript Q equal to 0.0017, P subscript C equal to 0.0349, and visibility about 0.951.

        This cell is useful in the presentation because it shows that our notebook is not just making similar-looking graphs. It is actually reproducing the central Boson Sampling calculation numerically.
        """,
    ),
    (
        "Figure 2(c)",
        """
        Now we move to Figure 2(c), which is the two-photon visibility structure. The paper compares three two-photon input configurations, and for each one it shows how the visibility changes across all possible non-colliding outputs.

        In our notebook, for each input configuration, we compute the bosonic visibility from the permanent-based quantum probabilities. We also compute the coherent-state visibility using the supplementary coherent-state formulas.

        So in these plots, the bar structure corresponds to the quantum visibility prediction, while the circular markers correspond to the coherent-state prediction.

        What matters physically is that these two predictions are different. The coherent-state calculation is important because it serves as a classical-optics baseline. If Bob’s measurements followed that coherent-state pattern, then the result could be explained by ordinary classical-wave interference. But the paper shows that Bob matches the quantum prediction much better than the coherent-state one.

        So while presenting these plots, the main message is: already at the two-photon level, the visibility pattern is structured, input-dependent, and clearly non-classical.
        """,
    ),
    (
        "Figure 3",
        """
        Next is Figure 3, which extends the same idea to the three-photon case. This is the central Boson Sampling part of the paper, because three-photon interference is a stronger test than the simpler two-photon case.

        The notebook reproduces the visibility structure for the same three input configurations used in the paper: 1-3-5, 1-4-6, and 1-5-6.

        Again, for each output configuration, we calculate the bosonic visibility from the measured unitary and compare it with the coherent-state prediction. The key thing to notice is that the visibility landscape becomes richer in the three-photon case. Some outputs are strongly enhanced, some are suppressed, and some even go negative.

        This is exactly what we expect from many-boson interference, because different output events receive contributions from many interfering multi-photon paths, and those contributions combine through the permanent.

        So this section is where we see the real Boson Sampling signature emerging more fully.
        """,
    ),
    (
        "Figure 4(b)",
        """
        This section corresponds to Figure 4(b), which looks at colliding outputs. Until now, we were mostly discussing non-colliding events, where each output mode contains at most one photon. Here, the paper studies outputs in which two photons are detected in the same mode.

        For the input configuration 1-3-5, the outputs considered are 1-5-5, 2-5-5, 3-5-5, 4-5-5, and 5-5-6.

        The reason this matters is that Boson Sampling is naturally formulated in occupation-number language, so colliding outputs are part of the same formalism. The only difference is that now the output occupation numbers include repetition, so the submatrix construction includes repeated columns.

        This notebook computes the corresponding quantum probabilities, distinguishable probabilities, and visibilities for those colliding-output events as well. So this cell shows that the Boson Sampling formalism is not limited to the simpler one-photon-per-mode case.
        """,
    ),
    (
        "Figure 5",
        """
        Finally, this cell reproduces the trend shown in Figure 5. This figure is important because it connects the Boson Sampling theory to a practical limitation of the experiment, namely the quality of the photon source.

        As pump power increases, the spontaneous parametric down-conversion source produces more higher-order photon-number terms. That improves count rate, but it also contaminates the ideal input state.

        The graph shows how the L1 distance changes with pump power. One curve compares Bob’s data with Alice’s ideal Fock-state prediction, and the other compares Bob’s data with Alice’s coherent-state prediction.

        The trend is very informative. As pump power increases, the agreement with the ideal Fock-state prediction becomes worse, while the statistics move closer to the more classical baseline. This is the experimental signature of higher-order source imperfections.

        So this figure is especially useful in the presentation because it explains why Boson Sampling is not only a complexity problem or a permanent problem. It is also a state-preparation problem.
        """,
    ),
    (
        "Closing",
        """
        To summarize my part, this notebook reproduces the mathematical and graphical structure of the paper’s main results.

        First, we verified the worked permanent calculation directly from the supplementary unitary. Then we reproduced the two-photon and three-photon visibility structures, followed by the colliding-output case, and finally the source-imperfection trend.

        Taken together, these plots show how the paper connects the Boson Sampling formalism, the measured unitary, and the observed visibility patterns. That is the main contribution of this notebook section.
        """,
    ),
]


ronit_sections = [
    (
        "Opening",
        """
        Now I will explain an important conceptual part of the paper, which is why the authors compare Bob’s measured visibility with Alice’s coherent-state visibility.
        """,
    ),
    (
        "Why coherent-state visibility is compared",
        """
        At first glance, this may look slightly surprising, because Boson Sampling is supposed to involve single-photon Fock-state inputs, not coherent states. So the natural question is: why bring coherent states into the comparison at all?

        The answer is that the authors want to rule out a classical explanation of the observed interference pattern.

        Bob is the one performing the actual Boson Sampling experiment. He injects photons into the optical circuit and measures the output statistics. Alice, on the other hand, represents the classical side. She is allowed only classical resources.

        Now, coherent states are the most natural classical-optics inputs for a linear interferometer. They are important for two reasons.

        First, coherent states allow Alice to characterize the interferometer efficiently. Using coherent light, she can determine the magnitudes and phases of the entries of the unitary matrix describing the optical network.

        Second, coherent states also give a classical-wave benchmark for what the same device would do if the input were classical rather than genuinely bosonic single-photon states.

        So the role of the coherent-state comparison is very specific. It is not meant to replace the Boson Sampling prediction. Instead, it provides a classical baseline.
        """,
    ),
    (
        "Physical logic",
        """
        The logic is the following. If Bob’s results matched both the Fock-state prediction and the coherent-state prediction, then the experiment would not provide strong evidence for genuinely bosonic interference. In that case, one could argue that the observed pattern is just a classical interference effect of the same interferometer.

        But if Bob’s measurements agree with the Fock-state prediction and disagree strongly with the coherent-state prediction, then the measured distribution cannot be explained as ordinary classical-wave interference. That is exactly the distinction the paper wants to establish.

        This is why the paper emphasizes the large L1 distances between Bob’s measured visibilities and Alice’s coherent-state visibilities. Those large distances show that the coherent-state model is not reproducing the same structure as the Boson Sampling experiment.
        """,
    ),
    (
        "Mathematical basis",
        """
        Now let me connect that statement to the mathematics given in the supplementary material.

        For the coherent-state calculation, the authors consider equal-amplitude coherent inputs in the occupied input modes. The electric field amplitude in each input mode is written as E subscript i equals e to the power i theta subscript i.

        These fields then pass through the same unitary interferometer, so the electric field at output mode j is given by the sum over i of U subscript i j times E subscript i.

        That is equation 8 in the supplementary material.

        Then the authors define two quantities.

        When the coherent states overlap at zero delay, the output correlation function is written as P of 0. This is obtained by phase averaging the product of the output intensities.

        When the coherent states are delayed far beyond the coherence length, interference is removed, and the corresponding incoherent correlation is written as P of 1.

        From these two quantities, the coherent-state visibility is defined in the same way as the photon visibility, namely V equals P of 1 minus P of 0 divided by P of 1.

        So mathematically, the coherent-state prediction is constructed from the same measured unitary, but physically it represents classical optical interference rather than bosonic Fock-state interference.

        That is the key point of this notebook section. The coherent-state visibility is included not because it is the Boson Sampling answer, but because it is the classical comparison that helps show the observed effect is genuinely quantum.
        """,
    ),
    (
        "Why visibility is used",
        """
        In this second part, I will explain why the paper compares theory and experiment using visibility rather than raw coincidence probabilities, and why this still preserves the original aim of the Boson Sampling experiment.

        The original Boson Sampling problem is formulated in terms of output probabilities. For a given input configuration and a given output configuration, the theory predicts a probability.

        So it is natural to ask: if the original goal is about probabilities, then why does the paper focus so much on visibility?

        The answer is that visibility is a normalized observable that still captures the same physics, but in a much more experimentally robust way.
        """,
    ),
    (
        "Detector efficiency derivation",
        """
        The fundamental comparison in the paper is between two kinds of statistics.

        First, the indistinguishable-photon case, where the photons interfere as identical bosons. This gives the quantum probability, which the paper writes as P subscript Q.

        Second, the distinguishable-photon case, where the photons do not interfere quantum mechanically. This gives the classical reference probability, written as P subscript C.

        The visibility is then defined as V subscript T equals P subscript C minus P subscript Q divided by P subscript C.

        So visibility is still built directly from the same two probabilities that Boson Sampling theory is concerned with. In that sense, it does not change the aim of the experiment at all. It simply packages the comparison into a more useful observable.

        Now the practical reason for doing this is detector efficiency.

        In a real experiment, all detectors are not identical. Different output channels can have different losses or different detector efficiencies. Because of that, the raw coincidence counts at the detectors are not determined only by the underlying Boson Sampling probability. They are also multiplied by the efficiency of that specific output channel.

        So if we directly compared raw counts across different outputs, we would be mixing together two effects: the actual probability predicted by the Boson Sampling model, and the efficiency bias of the detector setup.

        This is where visibility becomes powerful.

        Suppose the true probabilities for a given output event T are P subscript Q for indistinguishable photons and P subscript C for distinguishable photons. Let eta subscript T be the overall detection efficiency for that same output event.

        Then the measured count rates are proportional to eta subscript T times P subscript Q, and eta subscript T times P subscript C.

        Now if we form the visibility from the measured counts, we get C subscript C minus C subscript Q divided by C subscript C.

        Substituting the efficiency-weighted counts, the factor eta subscript T appears in both numerator and denominator, so it cancels out exactly.

        What remains is just P subscript C minus P subscript Q divided by P subscript C, which is the theoretical visibility formula itself.
        """,
    ),
    (
        "Conclusion",
        """
        So visibility preserves the same quantum-versus-classical comparison, but removes detector-efficiency distortion.

        That is why the use of visibility does not take us away from the Boson Sampling objective. Instead, it gives a cleaner and more reliable way of testing whether the experimental output statistics follow the bosonic interference predicted from the measured unitary.

        This is also why the paper says that raw coincidence counts are strongly affected by detector efficiency differences, and that visibility is used to remove this effect.

        So if Alice’s predicted visibilities agree with Bob’s measured visibilities, then the experiment is still validating the same underlying Boson Sampling theory. It is just doing so through a normalized quantity that is experimentally more robust.

        To summarize my part:

        First, the comparison with coherent-state visibility is used to show that Bob’s data are not just a classical-wave effect of the same interferometer.

        Second, the use of visibility instead of raw counts does not change the goal of the experiment, because visibility is still built from the same quantum and distinguishable probabilities, while cancelling detector-efficiency bias.

        So together, these two ideas strengthen the paper’s claim that the observed output statistics are genuinely bosonic and consistent with Boson Sampling theory.
        """,
    ),
]


write_notebook("ashokScript.ipynb", "Ashok Script", ashok_sections)
write_notebook("ronitScript.ipynb", "Ronit Script", ronit_sections)

print("Wrote ashokScript.ipynb and ronitScript.ipynb")
