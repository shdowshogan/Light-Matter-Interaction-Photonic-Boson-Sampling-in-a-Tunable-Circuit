Script

Start on the title cell

“Now I’ll present the figure-reproduction part of our project notebook. In this section, our goal is to show how the main plots in the paper arise from the Boson Sampling formalism and from the measured unitary matrices given in the supplementary material.

This notebook focuses on the figures most relevant to the paper’s core results, namely Figures 2, 3, 4, and 5. For each one, we explain what is being reproduced, how the numbers are obtained, and what the plot tells us physically.”

Move to “Scope of reproduction”.

“Before going into the plots, I want to clarify what exactly is reproduced here. The matrix-based theory calculations are reproduced directly from the paper’s supplementary material. That includes the permanent-based bosonic probabilities, the distinguishable-particle probabilities, and the visibility predictions.

The summary L1 distances quoted in the main text are also included exactly as reported. For Figure 5, the overall trend is recreated from the published graph, so that part should be understood as a graphical reconstruction. And for Bob’s individual measured bars in Figures 2 to 4, the PDF does not provide a machine-readable numerical table, so what we reproduce here is the theoretical structure of those figures.”

Go to “Reproduction of Fig. 2(a)”.

“This cell reproduces the worked example from the supplementary material. The input configuration is one photon in mode 1 and one photon in mode 3, and the output configuration is one photon in mode 2 and one photon in mode 5.

The important point here is that the paper’s logic starts from the measured unitary matrix. From that unitary, we build the relevant submatrix corresponding to the chosen input and output occupations. Then we compute two quantities.

First, the quantum probability, which depends on the permanent of the submatrix. Second, the distinguishable-particle probability, which is computed using the permanent of the mod-squared matrix.

From these two probabilities, we calculate the visibility. The notebook reproduces the same values reported in the paper: P subscript Q equal to 0.0017, P subscript C equal to 0.0349, and visibility about 0.951.

This cell is useful in the presentation because it shows that our notebook is not just making similar-looking graphs. It is actually reproducing the central Boson Sampling calculation numerically.”

Go to “Reproduction of Fig. 2(c)”.

“Now we move to Figure 2(c), which is the two-photon visibility structure. The paper compares three two-photon input configurations, and for each one it shows how the visibility changes across all possible non-colliding outputs.

In our notebook, for each input configuration, we compute the bosonic visibility from the permanent-based quantum probabilities. We also compute the coherent-state visibility using the supplementary coherent-state formulas.

So in these plots, the bar structure corresponds to the quantum visibility prediction, while the circular markers correspond to the coherent-state prediction.

What matters physically is that these two predictions are different. The coherent-state calculation is important because it serves as a classical-optics baseline. If Bob’s measurements followed that coherent-state pattern, then the result could be explained by ordinary classical-wave interference. But the paper shows that Bob matches the quantum prediction much better than the coherent-state one.

So while presenting these plots, the main message is: already at the two-photon level, the visibility pattern is structured, input-dependent, and clearly non-classical.”

Go to “Reproduction of Fig. 3”.

“Next is Figure 3, which extends the same idea to the three-photon case. This is the central Boson Sampling part of the paper, because three-photon interference is a stronger test than the simpler two-photon case.

The notebook reproduces the visibility structure for the same three input configurations used in the paper: 1-3-5, 1-4-6, and 1-5-6.

Again, for each output configuration, we calculate the bosonic visibility from the measured unitary and compare it with the coherent-state prediction. The key thing to notice is that the visibility landscape becomes richer in the three-photon case. Some outputs are strongly enhanced, some are suppressed, and some even go negative.

This is exactly what we expect from many-boson interference, because different output events receive contributions from many interfering multi-photon paths, and those contributions combine through the permanent.

So this section is where we see the real Boson Sampling signature emerging more fully.”

Go to “Reproduction of Fig. 4(b)”.

“This section corresponds to Figure 4(b), which looks at colliding outputs. Until now, we were mostly discussing non-colliding events, where each output mode contains at most one photon. Here, the paper studies outputs in which two photons are detected in the same mode.

For the input configuration 1-3-5, the outputs considered are 1-5-5, 2-5-5, 3-5-5, 4-5-5, and 5-5-6.

The reason this matters is that Boson Sampling is naturally formulated in occupation-number language, so colliding outputs are part of the same formalism. The only difference is that now the output occupation numbers include repetition, so the submatrix construction includes repeated columns.

This notebook computes the corresponding quantum probabilities, distinguishable probabilities, and visibilities for those colliding-output events as well. So this cell shows that the Boson Sampling formalism is not limited to the simpler one-photon-per-mode case.”

Go to “Reproduction of Fig. 5”.

“Finally, this cell reproduces the trend shown in Figure 5. This figure is important because it connects the Boson Sampling theory to a practical limitation of the experiment, namely the quality of the photon source.

As pump power increases, the spontaneous parametric down-conversion source produces more higher-order photon-number terms. That improves count rate, but it also contaminates the ideal input state.

The graph shows how the L1 distance changes with pump power. One curve compares Bob’s data with Alice’s ideal Fock-state prediction, and the other compares Bob’s data with Alice’s coherent-state prediction.

The trend is very informative. As pump power increases, the agreement with the ideal Fock-state prediction becomes worse, while the statistics move closer to the more classical baseline. This is the experimental signature of higher-order source imperfections.

So this figure is especially useful in the presentation because it explains why Boson Sampling is not only a complexity problem or a permanent problem. It is also a state-preparation problem.”

Go to the closing note.

“To summarize my part, this notebook reproduces the mathematical and graphical structure of the paper’s main results.

First, we verified the worked permanent calculation directly from the supplementary unitary. Then we reproduced the two-photon and three-photon visibility structures, followed by the colliding-output case, and finally the source-imperfection trend.

Taken together, these plots show how the paper connects the Boson Sampling formalism, the measured unitary, and the observed visibility patterns. That is the main contribution of this notebook section.”

Timing guide

Intro + scope: 1.5 min
Fig. 2(a): 2 min
Fig. 2(c): 2 min
Fig. 3: 2.5 min
Fig. 4(b): 1.5 min
Fig. 5: 1.5 min
Summary: 1 min
