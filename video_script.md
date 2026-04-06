# PH530 Elective Project Video Script

## Topic
**Photonic Boson Sampling in a Tunable Circuit**  
Based on the paper by Broome et al.

## Team Format
- Total duration: about 60 minutes
- Number of speakers: 5
- Recommended split: 12 minutes per speaker
- Style: recorded seminar with slides
- Good target: 22 to 26 slides total

## Speaker Allocation
- **Speaker 1:** Motivation, background, and why Boson Sampling matters
- **Speaker 2:** Experimental setup and how the optical circuit works
- **Speaker 3:** The mathematical model, permanents, and visibility
- **Speaker 4:** Main results from the paper
- **Speaker 5:** Limitations, significance, future work, and conclusion

## Slide Plan
- Slide 1: Title, team members, course, paper citation
- Slide 2: Roadmap
- Slide 3: Why quantum advantage is interesting
- Slide 4: Extended Church-Turing thesis and the trilemma
- Slide 5: What is Boson Sampling
- Slide 6: Why bosons are hard to simulate classically
- Slide 7: Experimental idea: Alice vs Bob
- Slide 8: Overview of the photonic setup
- Slide 9: Six-mode tunable optical circuit
- Slide 10: Photon source and detection
- Slide 11: How the unitary is characterized
- Slide 12: Mathematical notation for input and output occupations
- Slide 13: Submatrices and permanents
- Slide 14: Classical vs quantum probabilities
- Slide 15: Visibility and why it is measured
- Slide 16: Two-photon results
- Slide 17: Three-photon results
- Slide 18: Colliding outputs and number resolution
- Slide 19: Effect of imperfect photon sources
- Slide 20: Why the result is important
- Slide 21: Limits of the current experiment
- Slide 22: Scaling toward larger Boson Sampling
- Slide 23: Our notebook demonstration
- Slide 24: Key takeaways
- Slide 25: Thank you / questions

## Full Script

## Speaker 1
### Time target
0:00 to 12:00

### Slides
1 to 7

### Script

**Slide 1: Title**

"Hello everyone. We are presenting our PH530 elective project on the paper *Photonic Boson Sampling in a Tunable Circuit* by Matthew Broome and collaborators. This paper is an important early experimental demonstration of Boson Sampling, which is a model of quantum computation that is not universal like a full quantum computer, but is still believed to solve a task that is very difficult for classical computers."

"Our presentation will explain the physical idea behind Boson Sampling, the optical experiment performed in the paper, the mathematical role of matrix permanents, the main experimental results, and finally the broader significance and limitations of the work."

**Slide 2: Roadmap**

"This is the structure of our talk. First, we will discuss the motivation and computational context. Then we will explain the optical setup and the mathematical description. After that, we will go through the main results for two-photon and three-photon interference, and we will end with the implications of the work and the notebook we prepared to reproduce the key calculations."

**Slide 3: Why quantum advantage is interesting**

"A major goal in quantum information science is to identify tasks where a quantum device can outperform any efficient classical algorithm. Usually people think of Shor's algorithm and factoring, but this paper asks a more basic question: do we really need a universal quantum computer to challenge classical computational assumptions? Or can a simpler physical system already do that?"

"This question is important because universal quantum computers are extremely hard to build. If a simpler quantum device can already perform a classically intractable task, then it gives a more accessible path toward demonstrating quantum advantage."

**Slide 4: Extended Church-Turing thesis and the trilemma**

"The paper frames the problem using the Extended Church-Turing thesis. Very roughly, this thesis says that any realistic physical computation can be simulated efficiently by a probabilistic classical Turing machine."

"If scalable quantum computation is physically possible, and if the Extended Church-Turing thesis is also true, then efficient classical simulation should exist for quantum computation. But famous quantum algorithms like Shor's algorithm suggest otherwise. So the paper highlights a trilemma: either large-scale quantum mechanics fails, or efficient classical algorithms exist where we do not expect them, or the Extended Church-Turing thesis is false."

"Boson Sampling is proposed as a way to experimentally probe this issue without building a full universal quantum computer."

**Slide 5: What is Boson Sampling**

"Boson Sampling is a sampling problem. We inject identical bosons, in this case photons, into a linear optical network described by a unitary matrix U. Then we measure which output modes the photons occupy. The goal is not to compute one special number. The goal is to sample from the whole output probability distribution."

"The challenge comes from the fact that for indistinguishable bosons, the scattering amplitudes depend on matrix permanents. Permanents are similar to determinants, but without alternating signs, and they are much harder to compute."

**Slide 6: Why bosons are hard to simulate classically**

"For fermions, amplitudes involve determinants, and determinants can be computed efficiently. For bosons, amplitudes involve permanents, and permanent computation is known to be computationally hard. This is the main reason Boson Sampling is believed to become classically intractable as the number of photons grows."

"So the paper is not claiming universal quantum computation. Instead, it focuses on a narrower but very important statement: even a restricted photonic setup may already implement a task that strongly resists classical simulation."

**Slide 7: Experimental idea: Alice versus Bob**

"The paper explains the experiment using a race between Alice and Bob. Alice has only classical resources. Bob has a quantum photonic device. Both are given the same optical network. Alice characterizes the network and computes the expected output distribution using classical calculations. Bob injects photons into the device and directly samples the outputs experimentally."

"If Bob's device continues to generate correct samples much faster than Alice can classically compute them, then that would provide strong evidence against the Extended Church-Turing thesis."

"At this point I will hand over to the next speaker, who will explain how the actual optical circuit and photon source are built."

## Speaker 2
### Time target
12:00 to 24:00

### Slides
8 to 11

### Script

**Slide 8: Overview of the photonic setup**

"Now I will discuss the experimental setup used in the paper. The experiment is based on linear optics. The authors build a six-mode interferometric network and inject two or three photons into it. The output is detected with avalanche photodiodes, and the coincidence counts are used to estimate the probabilities of different output events."

"The central idea is simple: if the photons are indistinguishable, they interfere quantum mechanically inside the network. If they are distinguishable, then the statistics are more classical. Comparing these two cases reveals the genuinely bosonic interference."

**Slide 9: Six-mode tunable optical circuit**

"The optical network has six input and six output modes. Physically, these are implemented using three spatial modes and two orthogonal polarizations in each spatial mode. The paper maps the six logical modes as horizontal and vertical polarizations across three spatial channels."

"The unitary transformation of the full six-mode network is produced using a combination of local polarization operations and a three-by-three fused-fiber tritter. This gives a fully connected interferometer, meaning every input mode can contribute to every output mode."

"One important point is that the circuit is tunable. The polarization controllers allow the effective unitary to be adjusted. This matters because Boson Sampling requires a nontrivial, well-characterized unitary matrix."

**Slide 10: Photon source and detection**

"The photons are generated using spontaneous parametric down-conversion. A mode-locked Ti:Sapphire laser is frequency doubled, and then a nonlinear crystal produces photon pairs. Depending on the measurement, two or three of the photons are injected into the Boson Sampling circuit, while one photon can be used as a trigger."

"At the output, avalanche photodiodes detect the photons, and a coincidence logic circuit records multi-photon detection events. For colliding outputs, where more than one photon exits the same mode, the authors use a beam splitter and an extra detector to achieve effective number resolution."

"This is experimentally demanding because the count rates become very low, especially for the three-photon case. That is why the paper spends significant effort on efficient characterization and careful visibility measurements."

**Slide 11: How the unitary is characterized**

"A key technical contribution of the paper is that the authors do not rely on full quantum process tomography. Instead, they use an efficient characterization method based on coherent-state inputs."

"First, they determine the moduli of the unitary elements by sending light into one mode at a time and measuring output intensities. Then they determine the phases using pairwise dual-mode coherent inputs. This gives them the measured unitary U that Alice uses for the theoretical predictions."

"This step is very important because the experiment is not compared with an idealized guessed matrix. It is compared with the actually measured optical network."

"The next speaker will now explain the mathematical model and show how permanents and visibilities are computed from this measured unitary."

## Speaker 3
### Time target
24:00 to 36:00

### Slides
12 to 15

### Script

**Slide 12: Input and output occupation notation**

"To describe Boson Sampling mathematically, the paper uses occupation-number notation. If we have m modes, then an input configuration is written as S = (s1, s2, up to sm), where si tells us how many photons enter mode i. Similarly, an output configuration is T = (t1, t2, up to tm), where tj tells us how many photons are detected in output mode j."

"For example, in a two-photon experiment, the input S = (1,0,1,0,0,0) means that one photon enters mode 1 and one photon enters mode 3."

**Slide 13: Submatrices and permanents**

"Once the full unitary U is known, the paper constructs a smaller matrix U_ST associated with a particular input-output event. This is done by repeating columns according to the output occupation numbers and repeating rows according to the input occupation numbers."

"The crucial statement is that for indistinguishable bosons, the probability amplitude is given by the permanent of this submatrix. Therefore the quantum probability is proportional to the absolute square of the permanent."

"This is the fundamental reason the problem is classically hard. For a general matrix, calculating a permanent is much more difficult than calculating a determinant."

**Slide 14: Classical versus quantum probabilities**

"The paper also defines a classical comparison case, corresponding to distinguishable photons. In that case, instead of quantum amplitudes interfering coherently, the contributions add incoherently. The resulting probability can be written in terms of the permanent of a matrix built from the squared moduli of the entries."

"So the paper compares two quantities for each output event: the bosonic quantum probability P subscript Q and the classical distinguishable probability P subscript C."

"If the observed data match P subscript Q rather than P subscript C, then the experiment is displaying genuine non-classical bosonic interference."

**Slide 15: Visibility and why it is measured**

"Experimentally, instead of using raw counts directly, the authors measure the non-classical visibility, defined as V equals P_C minus P_Q divided by P_C."

"Why do they use visibility? Because raw coincidence counts are strongly affected by detector efficiencies and other practical differences between channels. Visibility gives a cleaner comparison between theory and experiment."

"The paper even includes a worked example in the supplementary material. For one chosen two-photon input-output pair, they compute P_Q to be approximately 0.0017, P_C to be approximately 0.0349, and the resulting visibility to be about 0.951. In our notebook, we directly reproduce this calculation using the published unitary matrix."

"The next speaker will now present the main experimental results and show how well the measured data agree with these theoretical predictions."

## Speaker 4
### Time target
36:00 to 48:00

### Slides
16 to 19

### Script

**Slide 16: Two-photon results**

"Let us begin with the two-photon Boson Sampling results. The authors inject two photons into the circuit and measure all possible non-colliding output combinations. For each configuration, they compare Alice's predicted visibilities with Bob's experimentally measured visibilities."

"The agreement is very good. The paper reports an average L1 distance per output configuration of about 0.027 between prediction and measurement. This is a strong indication that the measured two-photon interference behaves as the permanent-based Boson Sampling model predicts."

"The paper also compares the data with what would be expected from coherent-state inputs. That comparison disagrees strongly, with a much larger L1 distance. This is important because it shows the output is genuinely non-classical and not something that could be reproduced by a simple classical-wave model."

**Slide 17: Three-photon results**

"The three-photon experiment is the central result of the paper. Here the count rates are much lower and the experiment is more sensitive to imperfections, but the authors still find good qualitative and reasonable quantitative agreement between theory and experiment."

"For the three-photon non-colliding outputs, the L1 distance between Alice's predictions and Bob's measured visibilities is reported as about 0.122. This is worse than the two-photon case, but still clearly much closer to the quantum prediction than to the classical coherent-state alternative."

"The larger discrepancy is not surprising. As photon number increases, source imperfections, distinguishability, and higher-order emissions become more significant."

**Slide 18: Colliding outputs and number resolution**

"The paper then goes beyond non-colliding events and studies colliding outputs, meaning cases where two photons leave through the same output mode. This requires number resolution, which the authors implement using an additional 50:50 beam splitter and detector."

"Again, the measured visibilities agree much better with the bosonic prediction than with the coherent-state prediction. This shows that the Boson Sampling model remains valid even when more complicated output occupations are considered."

**Slide 19: Effect of imperfect photon sources**

"One of the most honest and useful parts of the paper is its discussion of imperfections. The photon source is based on down-conversion, which produces a state like vacuum plus eta times one pair plus eta squared times two pairs, and so on. That means higher-order unwanted terms are always present."

"As the pump power increases, these higher-order terms become more important. The paper shows that this drives the experiment away from ideal Fock-state behavior and toward more classical-looking statistics. This is why source brightness cannot simply be increased without limit."

"I will now hand over to the final speaker, who will discuss the broader significance of the work, the limitations, and our concluding remarks."

## Speaker 5
### Time target
48:00 to 60:00

### Slides
20 to 25

### Script

**Slide 20: Why the result is important**

"This paper is important because it demonstrates a realistic intermediate quantum model that is experimentally simpler than universal quantum computing, but still connected to a classically hard computational task. It gives an early proof of principle that quantum advantage may be observed in restricted photonic systems."

"The paper is also important methodologically. It combines careful experimental photonics with a complexity-theoretic motivation, so it sits at the intersection of quantum optics, quantum information, and computational complexity."

**Slide 21: Limits of the current experiment**

"At the same time, the experiment is still very small scale. The authors use only two and three photons in a six-mode network. This is far from the regime where classical verification becomes impossible."

"Also, there is no known error-correction scheme for Boson Sampling comparable to fault-tolerant universal quantum computation. So scaling up is not just an engineering problem. It is also a conceptual problem about robustness."

"Another limitation is the source itself. Down-conversion is probabilistic, and its brightness falls off badly as we demand larger photon numbers while maintaining good quality."

**Slide 22: Scaling toward larger Boson Sampling**

"The authors argue that the interesting regime is around 20 to 30 photons in a much larger network. Reaching that regime would require major improvements in three areas: high-efficiency photon-number-resolving detectors, low-loss integrated optical circuits, and much better single-photon sources."

"The paper also points out that Boson Sampling ideas may be implemented in other physical systems, not only photons. So the broader message is that intermediate quantum computation can be explored across multiple platforms."

**Slide 23: Our notebook demonstration**

"As part of our PH530 submission, we prepared an executable Jupyter notebook based directly on this paper. In the notebook, we entered the measured unitary matrices from the supplementary material, implemented the permanent-based probability formulas, reproduced the worked example from the paper, and generated output probability and visibility comparisons for selected two-photon and three-photon inputs."

"We also included a compact model of down-conversion source imperfections, so the notebook connects the mathematical formulas to the practical limitations discussed in the paper."

**Slide 24: Key takeaways**

"We would like to end with four key takeaways."

"First, Boson Sampling provides a concrete route to probing quantum computational advantage without requiring a universal quantum computer."

"Second, the core mathematical object is the matrix permanent, which makes classical simulation difficult."

"Third, this paper experimentally verifies that a small photonic device follows the permanent-based Boson Sampling predictions with good agreement, even in the presence of realistic imperfections."

"Fourth, the work is promising, but large-scale Boson Sampling still depends on major improvements in source quality, losses, and detection."

**Slide 25: Thank you**

"Thank you for listening. We hope this presentation made both the physics and the computational significance of Boson Sampling clear. We will be happy to take questions."

## Recording Tips
- Keep the slide style clean and technical rather than decorative.
- Put the key equations on slides 13 to 15 and explain them slowly.
- When one speaker ends, the next speaker should begin by briefly reconnecting to the previous point.
- If the total runtime becomes too long, reduce examples rather than skipping the motivation.
- If the runtime becomes too short, add one extra explanation slide on matrix permanents or on Hong-Ou-Mandel type interference.

## Suggested Division of Work Beyond Speaking
- One member prepares the background and complexity slides.
- One member redraws the experimental setup figure in a cleaner slide format.
- One member prepares the equations and notation slides.
- One member prepares the results plots and compares figures from the paper with the notebook.
- One member edits the final video and checks timing consistency.
