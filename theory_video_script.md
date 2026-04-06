# PH530 Elective Project — Theory Video Script (Improved)

**Paper:** *Photonic Boson Sampling in a Tunable Circuit* — Broome et al. (arXiv:1212.2234)
**Format:** 60 minutes · 5 speakers · ~12 minutes each · Theory focus only

---

## Speaker Allocation

| Speaker | Time | Topic |
|---------|------|-------|
| 1 | 0:00 – 12:00 | Motivation, the ECT thesis, and the trilemma |
| 2 | 12:00 – 24:00 | Optical modes, Fock states, and linear optics |
| 3 | 24:00 – 36:00 | Submatrix construction, permanents, and bosonic probabilities |
| 4 | 36:00 – 48:00 | Distinguishability, visibility, coherent states, and SPDC imperfections |
| 5 | 48:00 – 60:00 | Complexity-theoretic meaning, scaling, limitations, and conclusion |

---

## Speaker 1 — Motivation, the ECT Thesis, and the Trilemma
**Time: 0:00 – 12:00**

---

"Hello everyone. This video covers the theoretical framework behind *Photonic Boson Sampling in a Tunable Circuit* by Broome and collaborators. We are going to focus entirely on theory — the complexity background, the quantum optical formalism, and the mathematical structure that makes this experiment meaningful."

"Let me start with a foundational question in computer science: what can be computed efficiently by a realistic physical device?"

"The Extended Church-Turing thesis — which I will call the ECT thesis from now on — gives a very clean answer. It says that any function computable by a realistic physical device can also be computed efficiently by a probabilistic classical Turing machine. In other words, the universe does not offer any computational shortcuts beyond what classical probability can already provide."

"This thesis has guided computer science for decades. It is not a theorem — it is a hypothesis about physics. And it is that hypothesis that quantum computation threatens to falsify."

"Here is why. Consider Shor's factoring algorithm. It runs efficiently on a quantum computer, factoring an n-bit number in time polynomial in n. No classical algorithm is known to do the same — the best known classical methods require time that grows sub-exponentially but super-polynomially. If Shor's algorithm is physically implementable at scale, and if no efficient classical factoring algorithm exists, then the ECT thesis must be wrong."

"This creates a trilemma, which the paper frames explicitly. At least one of the following three things must be false. First: scalable quantum mechanics is physically valid. Second: no efficient classical factoring algorithm exists. Third: the ECT thesis is true. We cannot hold all three simultaneously if Shor's algorithm works."

"Now, this trilemma is centered on a very specific and hard task — factoring — and requires a full universal quantum computer to implement. The natural question is whether we need all of that. Can something simpler already challenge the ECT thesis?"

"The answer Aaronson and Arkhipov proposed in 2011 is: yes — if Boson Sampling is hard to simulate classically, then we already have a candidate. And the physical device that implements Boson Sampling is much simpler than a universal quantum computer. It does not need entangling gates, adaptive measurements, or error correction. It needs only linear optics and identical photons."

"So what is Boson Sampling? At the most basic level, it is a sampling problem. We inject n identical bosons into a linear optical interferometer described by an m-by-m unitary matrix U. We then measure the output mode occupations. The task is to produce samples from the resulting probability distribution over all possible output configurations."

"Two things make this hard classically. First, the output probability distribution involves many different output configurations, and the probabilities of those configurations are not independent — they are all coupled through the global unitary. Second, and more deeply, the amplitude for each output configuration depends on a quantity called the permanent of a matrix derived from U. Computing permanents is a provably hard problem, and the number of relevant permanents grows exponentially with photon number."

"So Boson Sampling is not just any sampling problem. It is one whose classical simulation appears to require computing permanent-related quantities, which puts it in a very hard complexity class."

"I want to stress one subtle but important point. Boson Sampling is not itself believed to be a #P-complete problem. The paper is careful about this. Rather, the argument is that any efficient classical algorithm for Boson Sampling would imply consequences in classical complexity theory so severe — specifically, the collapse of the polynomial hierarchy — that essentially all complexity theorists believe those consequences are false. So the difficulty of Boson Sampling is established indirectly, through complexity-theoretic consequences."

"This is a more careful claim than saying Boson Sampling is directly as hard as permanent computation. It is still a very strong claim, and it is what motivates the experiment."

"The paper by Broome and collaborators is an early experimental test of the core physical premise: that multi-photon scattering amplitudes in a real optical network actually follow the permanent-based quantum theory. That premise must be verified before any complexity-theoretic argument becomes physically grounded."

"To understand what that means technically, we first need the quantum optical language for describing modes, photons, and linear optical networks. That is what the next speaker will explain."

---

## Speaker 2 — Optical Modes, Fock States, and Linear Optics
**Time: 12:00 – 24:00**

---

"The theoretical framework for Boson Sampling lives entirely within quantum optics, and specifically within the formalism of second quantization. Let me build it up from scratch."

"Start with the concept of a mode. A mode is any physically distinguishable degree of freedom that a photon can occupy — a spatial path, a polarization state, a frequency bin, a time bin, or some combination. In the Broome experiment, six modes are used: they are encoded as horizontal and vertical polarization across three spatial channels, giving a mode mapping where modes 1 through 6 correspond to horizontal and vertical polarizations in spatial modes 1, 2, and 3 respectively."

"For each mode i, we define a bosonic creation operator, written a-dagger subscript i. When this operator acts on the vacuum state — the state with no photons — it creates one photon in mode i. Applying it k times creates k photons in the same mode. The adjoint, the annihilation operator a subscript i, removes a photon from mode i."

"These operators satisfy the canonical bosonic commutation relations. The key one is that the commutator of a subscript i with a-dagger subscript j equals delta i j — which is 1 when i equals j and 0 otherwise. This algebraic rule encodes the fact that photons are bosons: they are distinguishable by mode but indistinguishable within a mode."

"A Fock state in a single mode is simply a state with a definite number of photons. We write it as |n⟩ for n photons in that mode. For multiple modes, a multi-mode Fock state specifies the occupation number in every mode simultaneously. We write it as |s_1, s_2, ..., s_m⟩ where s_i is the number of photons in mode i."

"This occupation-number representation is the natural basis for Boson Sampling. Instead of asking which specific photon is in which mode — a question that has no meaning for identical bosons — we ask how many photons are in each mode. The state is fully specified by the list of occupation numbers."

"Now consider a passive linear optical network: beamsplitters, phase shifters, polarization rotators. These devices mix modes linearly. They do not create or destroy photons. Mathematically, the entire network is described by a unitary matrix U of dimension m-by-m."

"The action of the network on creation operators is described by the transformation: a-dagger subscript j at the output equals the sum over i of U_{ij} times a-dagger subscript i at the input. This is equation 1 in the paper. Each output mode is a coherent linear combination of all input modes, with coefficients given by the columns of U."

"For a single photon, the physics is simple. If a photon enters mode i, the amplitude for it to exit mode j is U_{ij}. The probabilities follow directly from Born's rule."

"For multiple photons, the story is richer. Suppose we input two identical photons, one in mode i and one in mode k. To find the amplitude for one photon to exit mode j and one to exit mode l — with j not equal to l — we must sum over both ways this can happen: U_{ij} times U_{kl}, and U_{il} times U_{kj}. These two terms interfere because the photons are identical bosons. If they were distinguishable particles, only one assignment would apply to each particle, and there would be no interference."

"This is many-boson interference. It is a generalization of the two-photon Hong-Ou-Mandel effect to larger systems. In Hong-Ou-Mandel, two identical photons entering a 50-50 beamsplitter always exit together — the two terms that contribute to them exiting separately add destructively. In Boson Sampling, the same physics operates across a much larger and more complex network."

"The key insight is that the interference pattern for n identical bosons through an m-mode network is governed by sums over all n-factorial permutations of how photons could be assigned to output modes. Each permutation contributes one product of matrix elements, and all contributions add coherently because the photons are indistinguishable. This sum over permutations is exactly the mathematical definition of a permanent."

"So the linear optical formalism, combined with bosonic symmetry, directly produces permanents as the relevant quantity. This is not an accident or a coincidence. It is a structural consequence of quantum statistics."

"The contrast with fermions is instructive. Fermions obey an antisymmetry principle — their states must be antisymmetric under exchange. This means that identical terms get subtracted rather than added, and the resulting sum over permutations with alternating signs is a determinant. Determinants are efficiently computable. Permanents are not. Boson Sampling exploits this asymmetry."

"With this framework in place, we can now write down the precise probability formulas for Boson Sampling. That is what the next speaker will do."

---

## Speaker 3 — Submatrices, Permanents, and Bosonic Probabilities
**Time: 24:00 – 36:00**

---

"Now I want to make everything concrete. We have a linear optical network described by a 6-by-6 unitary U. We inject n photons into specified input modes and ask for the probability of detecting them in a specified set of output modes. I will walk through exactly how that probability is computed."

"First, we need notation for configurations. An input configuration S is a vector of length m, where S = (s_1, s_2, ..., s_m) and s_i tells us how many photons enter mode i. Similarly, an output configuration T = (t_1, t_2, ..., t_m) where t_j tells us how many photons are detected in output mode j. The total photon number n is the sum of all s_i values, which also equals the sum of all t_j values — it is conserved by the linear network."

"For example, in the two-photon case from the supplementary material, the input is S = (1, 0, 1, 0, 0, 0), meaning one photon enters mode 1 and one enters mode 3. The output of interest is T = (0, 1, 0, 0, 1, 0), meaning one photon exits mode 2 and one exits mode 5."

"Given S and T, we construct an n-by-n submatrix of U. The procedure has two steps. First, form an n-by-m intermediate matrix by taking t_j copies of column j of U for each j. This selects the columns corresponding to the occupied output modes. Second, from that intermediate matrix, form the n-by-n submatrix by taking s_i copies of row i for each i. This selects the rows corresponding to the occupied input modes."

"In the worked example, t_2 = 1 and t_5 = 1, so we select columns 2 and 5 of U. Then s_1 = 1 and s_3 = 1, so we select rows 1 and 3 from those two columns. The result is a 2-by-2 matrix whose entries are U_{1,2}, U_{1,5}, U_{3,2}, and U_{3,5}."

"The paper gives these values explicitly from the measured two-photon unitary. The top row is (0.325, 0.430) and the bottom row is (0.182 + 0.248i, −0.127 − 0.386i)."

"Now the bosonic probability formula. For indistinguishable photons, the quantum probability of the output T given input S is:"

"P^Q_T = |Per(U_{ST})|^2 divided by the product of s_i factorial over all i and t_j factorial over all j."

"The factorials in the denominator account for normalization when multiple photons occupy the same mode. For the non-colliding case where every s_i and t_j is 0 or 1, all factorials are 1, so the formula reduces to simply the squared modulus of the permanent."

"The permanent of an n-by-n matrix A is defined as the sum over all permutations sigma of the symmetric group S_n of the product of A_{i, sigma(i)} for i from 1 to n. This looks identical to the determinant formula except that there is no sign factor — every permutation contributes with a plus sign."

"For a 2-by-2 matrix with entries a, b, c, d, the permanent is simply ad + bc. The determinant would be ad − bc. For small matrices, the difference seems trivial. But for large matrices, computing a permanent requires summing over n-factorial terms with no cancellation to exploit, while computing a determinant can be done efficiently using Gaussian elimination."

"Let us verify the worked example. The 2-by-2 submatrix has permanent equal to (0.325)(−0.127 − 0.386i) plus (0.430)(0.182 + 0.248i). Computing these products and adding gives a complex number whose squared magnitude is 0.0017. This matches the value P^Q_T = 0.0017 quoted in the supplementary material."

"Now consider what would happen if the two photons were distinguishable — if they were labelled particles rather than identical bosons. In that case, interference between different photon assignments cannot occur. The correct formula uses the permanent of a different matrix, constructed from the squared magnitudes of the entries of U_{ST}. Call this matrix U-tilde_{ST}, where U-tilde_{ST,ij} = |U_{ST,ij}|^2."

"The distinguishable probability is then P^C_T = Per(U-tilde_{ST}). In the worked example, U-tilde_{ST} has entries |0.325|^2, |0.430|^2, |0.182 + 0.248i|^2, and |−0.127 − 0.386i|^2. Computing those squared magnitudes and taking the 2-by-2 permanent gives P^C_T = 0.0349."

"So for this one output event, the quantum probability is about 17 times smaller than the classical distinguishable probability. That dramatic suppression is a direct consequence of many-boson interference. Summing the quantum amplitudes coherently before squaring gives a very different result from squaring individual amplitudes and summing incoherently."

"It is worth pausing on what Boson Sampling actually asks of us computationally. The task is not to compute one permanent once. The task is to sample from the full distribution over all output configurations T. For a fixed input S, the number of non-colliding output configurations in an m-mode system with n photons is C(m, n) — m choose n. For n = 20 and m = 400, that is an astronomically large number of configurations, each associated with a different permanent. Sampling from this distribution efficiently requires, in effect, access to the structure of all those permanents simultaneously."

"This is why classical simulation of Boson Sampling is believed to be hard: not because any single permanent is hard to compute for small n, but because the full sampling problem at large n becomes intractable."

"The next speaker will now discuss what happens when the photons are only partially indistinguishable, and how the visibility measurement connects the ideal theory to real experimental data."

---

## Speaker 4 — Distinguishability, Visibility, Coherent States, and SPDC Imperfections
**Time: 36:00 – 48:00**

---

"The permanent-based theory I just described assumes perfectly identical input photons. In any real experiment, that assumption is only approximately satisfied. The photons may differ slightly in their spectral profiles, arrival times, or polarizations. This partial distinguishability smoothly interpolates between the ideal bosonic regime and the fully classical distinguishable-particle regime."

"To understand this interpolation, it helps to think about what indistinguishability means physically. Two photons are indistinguishable if and only if they overlap completely in every degree of freedom — not just the ones we control, but also internal degrees of freedom like frequency spectrum. If they differ in any degree of freedom, quantum erasure is incomplete, and the bosonic interference is reduced."

"The standard experimental handle for controlling distinguishability is the temporal delay between input photons. When the delay is zero, the photons arrive at the network simultaneously and, if their spectra overlap well, interfere as identical bosons. When the delay is made much larger than the coherence length of the photons, they arrive at distinct times, the which-path information is in principle available, and the statistics approach the distinguishable-particle case."

"This is exactly how the paper extracts both P^Q_T and P^C_T from the same optical setup. For n = 2, the coincidence rate is measured as a continuous function of the delay — this is effectively a Hong-Ou-Mandel-style scan. The coincidence rate at zero delay gives a measurement proportional to P^Q_T, and the coincidence rate at large delay gives a measurement proportional to P^C_T."

"For n = 3, running the same continuous scan is impractical because the four-fold coincidence rates are too low, and optical drift over the long measurement times would corrupt the data. Instead, the paper measures P^C_T at just two specific delay configurations — one with delays (−Δτ_∞, 0, +Δτ_∞) and one with (+Δτ_∞, 0, −Δτ_∞) — and averages them to reduce the effect of any residual misalignment. P^Q_T is obtained from a single measurement at zero delay (0, 0, 0)."

"Raw coincidence counts are not directly comparable between different output modes because each detector has a different efficiency, and the coupling efficiencies into different modes are not all equal. So comparing Alice's theoretical predictions with Bob's experimental counts would require careful efficiency calibration for every channel."

"The visibility sidesteps this problem elegantly. The non-classical interference visibility for output T is defined as V_T = (P^C_T − P^Q_T) / P^C_T. Because both P^C_T and P^Q_T are measured through the same detection channel for the same output mode T, the detector efficiency cancels in the ratio. The visibility measures the fractional reduction in coincidence rate when the photons become indistinguishable, as a pure number between −1 and 1."

"In the worked example from the supplementary material: P^Q_T = 0.0017, P^C_T = 0.0349, so the predicted visibility is (0.0349 − 0.0017) / 0.0349 ≈ 0.951. The experimentally measured visibility for this same input-output pair is 0.939. The agreement is very close — the small gap reflects residual distinguishability and other experimental imperfections."

"A visibility near 1 means the bosonic interference strongly suppresses that output relative to the classical case. A visibility near 0 means the quantum and classical probabilities are similar — the bosonic interference has little effect for that particular event. Negative visibilities are also possible, corresponding to events that are enhanced rather than suppressed by bosonic interference."

"Now I want to discuss a separate and important theoretical comparison: coherent states. Alice uses coherent states to characterize the interferometer — she injects coherent light and measures output intensities and phases to reconstruct the unitary U. This is efficient: only 2m − 1 measurement settings are needed for an m-mode network."

"But the paper also asks: what if Alice used coherent states in place of Fock states when trying to reproduce Bob's output distribution? This question has a clean theoretical answer. The paper derives, in supplementary section III, the n-th order correlation function for coherent-state inputs propagating through the same unitary U. The result involves phase-averaging over the input phases, and the formulas — equations 9 and 10 in the supplementary — show that coherent-state correlations do not generally match the permanent-based Fock-state probabilities."

"This is an important point. A coherent state is a superposition of Fock states with a Poissonian photon-number distribution. It does not have a fixed photon number. The multi-photon correlations it produces are fundamentally different from those of a fixed-photon-number Fock state. So even though Alice uses coherent states to characterize the network perfectly, those same coherent states cannot reproduce the Boson Sampling distribution."

"The paper uses this comparison to verify that the quantum output is genuinely non-classical. For the two-photon case, the L1 distance between Alice's Fock-state predictions and Bob's measurements is 0.027 — excellent agreement. But the L1 distance between Alice's coherent-state predictions and Bob's measurements is 0.548 — a large disagreement. This tells us that whatever Bob is sampling, it is not something a classical wave model would produce."

"Finally, let me discuss the SPDC photon source imperfections, which are described in supplementary section IV. Spontaneous parametric down-conversion produces photon pairs according to a state of the form: vacuum plus η times one-pair plus η-squared times two-pairs plus higher-order terms, where η is a small parameter related to the nonlinear interaction strength. Triggering on one photon of a pair removes the vacuum term, but the higher-order two-pair, three-pair contributions remain."

"These higher-order terms contaminate the intended input state. If we are trying to inject exactly one photon into each of n modes, any extra photons from higher-order terms add noise. This drives the output statistics away from the ideal bosonic prediction and toward a more classical-looking distribution."

"As pump power increases, η increases, and the relative weight of higher-order terms grows. The paper demonstrates this explicitly in figure 5: increasing pump power systematically increases the L1 distance between Alice's Fock-state predictions and Bob's measurements, while decreasing the distance from Alice's coherent-state predictions. In other words, the output becomes more classical as the source becomes noisier."

"This is the fundamental tension for SPDC sources: you need higher rates to accumulate statistics quickly, but higher rates introduce more multi-pair contamination. The paper runs at 20% of maximum pump power for this reason — a deliberate tradeoff between rate and purity."

"The last speaker will now take all of this and place it in the bigger picture: what does this mean for computational complexity, what are the theoretical limits, and where does the field go from here?"

---

## Speaker 5 — Complexity, Scaling, Limitations, and Conclusion
**Time: 48:00 – 60:00**

---

"We now have all the pieces to understand why Boson Sampling is theoretically significant, and equally important, to understand precisely what its current limitations are."

"Let me begin with the complexity argument more carefully. The core theorem, due to Aaronson and Arkhipov, is roughly as follows. Suppose there existed a classical probabilistic algorithm that could efficiently sample from the output distribution of Boson Sampling for n photons in a randomly chosen m-mode network, where m is polynomial in n. Then this would imply that the polynomial hierarchy collapses to the third level."

"Collapsing the polynomial hierarchy is considered extremely unlikely in complexity theory — it would mean that a vast number of seemingly harder problems are actually no harder than much simpler ones. Since complexity theorists believe this collapse does not happen, they also believe no such efficient classical algorithm exists."

"It is important to understand the exact nature of this argument. It is not a proof that classical simulation is impossible. It is a proof that classical simulation would require something that the entire field considers implausible. This is the best kind of hardness result available for Boson Sampling, and it is comparable in spirit to how we know factoring is believed to be hard — not by proof, but by the absence of efficient algorithms and by complexity-theoretic evidence."

"There is also a subtlety in the Aaronson-Arkhipov argument about what kind of sampling is required. The result applies to approximate Boson Sampling — sampling from a distribution that is close in total variation distance to the ideal one. This matters for experiment, because real experiments always have noise. Rohde and Ralph showed in a related work that photonic Boson Sampling retains its computational hardness even in the presence of photon loss, which is encouraging for realistic implementations."

"Now consider the question of scale. How large does the system need to be before Boson Sampling becomes classically intractable to verify? Aaronson and Arkhipov estimated the interesting regime to be around n = 20 to 30 photons in a network with m of order n-squared modes. At that scale, the output distribution would have so many possible configurations that even storing the distribution classically would be infeasible, let alone sampling from it."

"The experiment in this paper uses n = 2 and n = 3 photons in m = 6 modes. This is far below the threshold of classical intractability. A classical computer can easily compute and verify these distributions. But that is not the point of this experiment. The point is to verify the physical premise — that the actual scattering amplitudes in a real optical circuit follow the permanent-based theory — before trusting that premise at larger scales where verification is impossible."

"This is good scientific strategy. You test a model in a regime where you can check it, and then you extrapolate with confidence. The paper does this, and the agreement is good."

"What would it take to reach the interesting regime? Three things need to improve simultaneously. First, photon sources must produce genuinely single photons with high purity and high rate. Down-conversion is not a suitable source at large n because its exponentially decreasing rate makes multi-photon experiments take impossibly long times. Quantum dots and other deterministic single-photon emitters are more promising. Second, the optical network must have very low loss, since photon loss reduces the effective photon number and degrades the quantum advantage. Integrated photonic platforms are actively being developed for this purpose. Third, photon-number-resolving detection must be highly efficient across all output modes. Transition edge sensors with efficiencies above 95% are now available and have enabled detection of entangled photon pairs with overall system efficiencies exceeding 60%."

"There are also conceptual challenges that go beyond engineering. Unlike universal quantum computation, Boson Sampling has no known error-correction protocol. This is a general feature of intermediate quantum computation models — the class that sits between purely classical computation and full fault-tolerant quantum computing. Other models in this class include deterministic quantum computing with one qubit, known as DQC1, instantaneous quantum polytime computation or IQP, and permutational quantum computing. None of these currently has error correction."

"This means that errors in Boson Sampling accumulate without any way to suppress them systematically. As the system grows, the distance between the ideal distribution and the experimentally produced distribution will grow too. At some point, the question of whether the output is genuinely hard to simulate classically becomes ambiguous — because the errors themselves may make the distribution easy to simulate."

"There is active theoretical work on this question. Some results suggest that the computational hardness is robust to a constant rate of photon loss. But a complete theory of noise robustness for Boson Sampling does not yet exist."

"Finally, I want to close with the broader theoretical picture. Boson Sampling sits at the intersection of three fields: quantum optics, quantum information theory, and computational complexity. The reason it became influential is precisely that it connects a natural, physically simple process to a deep complexity-theoretic question."

"Quantum optics provides the physical platform: identical photons, linear networks, and bosonic interference. Quantum information theory provides the mathematical language: Fock states, creation operators, unitary transformations. And computational complexity provides the motivation: the permanent, #P-completeness, the polynomial hierarchy, and the ECT thesis."

"To summarize the theoretical content of this paper in five points:"

"One: Boson Sampling is a sampling task whose classical simulation is believed to be hard because the output probabilities involve permanents of complex matrices, and permanent computation is #P-hard."

"Two: The natural framework is second-quantized linear optics, where the network is a unitary on modes and the input state is a multi-mode Fock state."

"Three: The bosonic probability for a specific output configuration is the squared modulus of the permanent of an n-by-n submatrix constructed from the network unitary. The classical distinguishable probability is instead the permanent of the matrix of squared moduli — a formally similar but physically very different quantity."

"Four: The non-classical interference visibility is the theoretically and experimentally preferred figure of merit, because it is independent of detector efficiencies and cleanly separates the bosonic quantum prediction from the classical distinguishable prediction."

"Five: Real photon sources from SPDC have higher-order multi-pair contributions that push the output statistics away from the ideal theory, setting a fundamental trade-off between source brightness and sampling quality that must be solved by next-generation photon sources."

"This is the theoretical foundation of *Photonic Boson Sampling in a Tunable Circuit*. Thank you."

---

## Production Notes

**Pacing:**
- Speaker 3 should slow down at the definition of the permanent and at the worked example calculation. Write those values on the slide and read them out one at a time.
- Speaker 4 should write the visibility formula on screen before explaining it verbally, and keep it visible during the SPDC discussion.
- Speaker 2 should have the commutation relation and the creation operator definition visible simultaneously.

**Transitions:**
- Each speaker should begin their section by briefly referencing the last point made by the previous speaker. Do not assume the audience has a perfect memory.

**Equations to display on slides:**
- Slide for Speaker 2: a†_j = Σ_i U_{ij} a†_i and [a_i, a†_j] = δ_{ij}
- Slide for Speaker 3: P^Q_T = |Per(U_{ST})|² and P^C_T = Per(Ũ_{ST}) and the 2×2 submatrix from the worked example
- Slide for Speaker 4: V_T = (P^C_T − P^Q_T) / P^C_T and |ψ⟩ ∝ |00⟩ + η|11⟩ + η²|22⟩ + ...
- Slide for Speaker 5: The polynomial hierarchy statement (informal), and the approximate scale n ~ 20–30 for classical intractability

**Timing buffer:**
- If any speaker finishes early, the best place to add content is Speaker 3 (add a 3×3 permanent example to contrast with the 2×2 case) or Speaker 5 (add a brief comparison with DQC1 or IQP).
- If any speaker runs long, the safest cuts are the SPDC rate numbers in Speaker 4 and the technology roadmap details in Speaker 5.