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
        In my part, I’ll go through the figure-reproduction section of our notebook. The idea here is not just to show a few plots that look similar to the paper, but to show how those plots actually come out of the Boson Sampling formalism and the measured unitary matrices given in the supplementary material.

        I’ll mainly focus on Figures 2, 3, 4, and 5, because together they tell the story of the paper quite nicely. They take us from the basic permanent calculation, to two-photon and three-photon visibility patterns, then to colliding outputs, and finally to the effect of source imperfections.
        """,
    ),
    (
        "Scope",
        """
        Before I start with the individual figures, I just want to make one thing clear about what is exact and what is reconstructed.

        The matrix-based calculations in this notebook are directly based on the published supplementary material. So whenever we calculate bosonic probabilities, distinguishable probabilities, or visibilities from the unitary, that part is an exact reproduction of the theory using the authors’ own matrix.

        The summary L1 values quoted in the text are also included exactly as reported in the paper.

        For Figure 5, the trend is recreated from the plotted graph, so that part should be thought of as a careful graphical transcription. And for Bob’s individual measured bars in Figures 2 to 4, the paper does not provide a machine-readable data table, so what we reproduce here is the theoretical structure of those figures rather than claiming that every experimental bar has been extracted exactly.
        """,
    ),
    (
        "Figure 2(a)",
        """
        I’ll start with Figure 2(a), because this is really the backbone of everything else.

        Here the paper gives a worked example from the supplementary material. The input is one photon in mode 1 and one photon in mode 3, and the output we look at is one photon in mode 2 and one photon in mode 5.

        What the notebook does is exactly what the paper describes in words. We start from the measured unitary, then we construct the relevant submatrix for that specific input-output event, and then we compute two different probabilities.

        The first is the bosonic quantum probability, which comes from the permanent of that submatrix. The second is the distinguishable-particle probability, which comes from the permanent of the mod-squared version.

        Once we have those two numbers, we compute the visibility. The nice thing is that the notebook reproduces the same values quoted in the paper: P subscript Q is 0.0017, P subscript C is 0.0349, and the visibility is about 0.951.

        So while presenting this cell, the main point I would emphasize is that this is where the paper’s core mathematics becomes concrete. We are not just discussing Boson Sampling in abstract terms. We are actually reconstructing the same calculation the authors used.
        """,
    ),
    (
        "Figure 2(c)",
        """
        Now moving to Figure 2(c), this is where we begin to see the visibility pattern across many output configurations in the two-photon case.

        The paper considers three different two-photon input configurations, and for each one it looks at how the visibility changes over all possible non-colliding outputs.

        In the notebook, for every one of those outputs, we calculate the bosonic visibility from the permanent-based probabilities. Alongside that, we also calculate the coherent-state visibility using the formulas from the supplementary material.

        So when these plots appear, the bars correspond to the quantum visibility prediction, and the circular markers correspond to the coherent-state prediction.

        What I find important here is not just that the values are different, but that the whole pattern is different. The coherent-state calculation acts as a classical baseline. If Bob’s data followed that pattern, then one could argue that the same optical circuit is just producing an ordinary classical interference effect. But the paper shows that Bob agrees much more strongly with the quantum prediction.

        So this figure is a nice bridge between the basic permanent calculation and the more serious three-photon Boson Sampling result. It already shows that even at the two-photon level, the visibility structure is highly nontrivial and clearly depends on genuine bosonic interference.
        """,
    ),
    (
        "Figure 3",
        """
        Next comes Figure 3, and this is really the central part of the paper, because now we are in the three-photon regime.

        The notebook reproduces the visibility structure for the same three input configurations shown by the authors: 1-3-5, 1-4-6, and 1-5-6.

        Just like before, for each possible non-colliding output, we compute the bosonic visibility from the measured unitary and compare it with the coherent-state prediction.

        But now the structure becomes much richer. Some outputs have large positive visibility, some are suppressed, and some even go negative. That is exactly what we expect in a genuine many-boson interference setting, because each output event receives contributions from several multi-photon paths, and all of those combine through the permanent.

        So when I present this figure, I would probably slow down a little and say that this is where the Boson Sampling idea really becomes visible in the notebook. The two-photon case helps build intuition, but the three-photon case is where the main claim of the paper starts to feel much more substantial.
        """,
    ),
    (
        "Figure 4(b)",
        """
        After that, we come to Figure 4(b), which deals with colliding outputs.

        Up to this point, most of the discussion is about non-colliding events, meaning each occupied output mode contains only one photon. But in Figure 4, the paper deliberately studies outputs where two photons appear in the same output mode.

        For the input configuration 1-3-5, the outputs considered are 1-5-5, 2-5-5, 3-5-5, 4-5-5, and 5-5-6.

        This matters because Boson Sampling is naturally written in occupation-number language, so colliding outputs are not some separate phenomenon. They are part of the same formalism. The only technical change is that repeated occupation means repeated rows or columns in the submatrix construction.

        So this cell is useful because it shows that the formalism still works even when the output is more complicated than the simple one-photon-per-mode case. It makes the notebook feel more complete, and it also follows the structure of the paper closely.
        """,
    ),
    (
        "Figure 5",
        """
        Finally, we reach Figure 5, and this is one of my favorite plots in the paper because it connects the theory to a very real experimental limitation.

        As pump power increases, the down-conversion source produces more higher-order photon-number terms. That helps with count rate, but at the same time it makes the input state less ideal.

        The graph tracks how the L1 distance changes with pump power. One curve compares Bob’s measurements with Alice’s ideal Fock-state prediction, and the other compares Bob’s measurements with Alice’s coherent-state prediction.

        The trend is very telling. As pump power goes up, the agreement with the ideal Fock-state prediction becomes worse, while the system starts looking closer to the more classical baseline.

        So this figure is very useful in a presentation, because it reminds us that Boson Sampling is not just about abstract permanents or complexity theory. It also depends critically on how well the photon source approximates the ideal input state.
        """,
    ),
    (
        "Closing",
        """
        So to wrap up my part, this notebook section follows the same logic as the paper itself.

        We begin with the worked permanent calculation, then move to the two-photon visibility structure, then to the three-photon case, after that to colliding outputs, and finally to the source-imperfection trend.

        Taken together, these plots show how the measured unitary, the Boson Sampling formalism, and the observed visibility patterns all fit together.

        For me, that is the real value of this notebook section: it turns the paper from something we read into something we can actually compute, visualize, and explain step by step.
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
