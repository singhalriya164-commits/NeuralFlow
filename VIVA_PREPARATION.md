# Deep Learning Project Viva-Voce Questions & Answers
**Project Title**: Compare Vanilla RNN, Bidirectional RNN, LSTM & GRU on the Same Sequence Task

---

### Q1: Why do we need Recurrent Neural Networks (RNNs) instead of standard Feedforward Neural Networks (MLPs)?
**Answer**: Standard Feedforward networks assume all inputs and outputs are independent of each other. They cannot handle sequential data of variable length and have no internal memory of previous inputs. RNNs introduce recurrent loops that maintain a hidden state vector $h_t$ at each timestep:
$$h_t = \tanh(W_{ih} x_t + W_{hh} h_{t-1})$$
This hidden state acts as a persistent memory of past context, making RNNs suited for sequential patterns like language, time series, or sequential spatial scans.

---

### Q2: What is the Vanishing Gradient problem in RNNs, and what causes it?
**Answer**: During Backpropagation Through Time (BPTT), gradients of the loss with respect to early hidden states are computed by repeated chain-rule multiplications:
$$\frac{\partial h_T}{\partial h_1} = \prod_{j=2}^T W_{hh}^T \operatorname{diag}(1 - \tanh^2(a_j))$$
Because the derivative of the activation function $\tanh'(x)$ is always between 0 and 1, and the recurrent weight matrix $W_{hh}$ repeatedly multiplies the error, if the largest singular value (spectral radius) of $W_{hh}$ is less than 1, the gradient decays exponentially towards zero as sequence length $T$ grows. As a result, the network cannot learn dependencies from timesteps far in the past.

---

### Q3: What is the Exploding Gradient problem, and how is it usually prevented?
**Answer**: If the eigenvalues of the recurrent weight matrix $W_{hh}$ are greater than 1, the repeated matrix multiplications over many timesteps cause gradients to grow exponentially large ($> 10^3$ or NaN). This causes wildly unstable weight updates and training divergence. 
It is typically solved by **Gradient Clipping**, which rescales the gradient vector if its $L_2$ norm exceeds a predefined threshold $c$:
$$g \leftarrow g \cdot \frac{c}{\max(c, \|g\|_2)}$$

---

### Q4: Why does LSTM solve or significantly reduce the vanishing gradient problem?
**Answer**: LSTM introduces an **additive Cell State** ($c_t$) controlled by an explicit **Forget Gate** ($f_t$):
$$c_t = f_t \odot c_{t-1} + i_t \odot \widetilde{c}_t$$
When computing the gradient $\frac{\partial c_t}{\partial c_{t-1}}$, it is simply $f_t$ (plus a small additive term). If the forget gate is saturated near 1, the gradient flows directly through time without exponential decay and without being repeatedly multiplied by weight matrices or compressed by squashing activation functions. This mechanism is known as the **Constant Error Carousel (CEC)**.

---

### Q5: What are the three gates in an LSTM and what are their specific functions?
**Answer**:
1. **Forget Gate ($f_t$)**: Decides what fraction of information from the previous cell state $c_{t-1}$ to discard (output between 0 and 1 via sigmoid).
2. **Input Gate ($i_t$)**: Decides which new candidate values ($\widetilde{c}_t$) should be written into the cell state.
3. **Output Gate ($o_t$)**: Decides what part of the updated cell state should be output as the current hidden state $h_t = o_t \odot \tanh(c_t)$.

---

### Q6: How is GRU different from LSTM?
**Answer**:
1. **Fewer Gates**: GRU has only 2 gates (Reset Gate $r_t$ and Update Gate $z_t$), whereas LSTM has 3 gates (Forget, Input, Output).
2. **No Separate Cell State**: GRU merges the cell state and hidden state into a single state vector $h_t$.
3. **Coupled Updating**: The update gate $z_t$ simultaneously controls forgetting and writing:
   $$h_t = (1 - z_t) \odot n_t + z_t \odot h_{t-1}$$
4. **Fewer Parameters**: GRU has ~25% fewer parameters than an LSTM of the same hidden size (3 weight matrices per gate instead of 4).

---

### Q7: Why is GRU often considered faster or more computationally efficient than LSTM?
**Answer**: Because GRU computes only two gate activations per timestep instead of three, and manages one recurrent state vector instead of two, it requires 25% fewer matrix multiplications and less memory bandwidth per step. However, on CPU execution without specialized kernel fusion, sequential state dependencies can sometimes offset this theoretical speedup.

---

### Q8: What is a Bidirectional RNN, and how does it differ from a unidirectional RNN?
**Answer**: A unidirectional RNN processes inputs in one chronological order ($t=1 \to T$). A Bidirectional RNN runs two separate recurrent layers simultaneously:
- A **forward layer** processing from start to end ($t=1 \to T$).
- A **backward layer** processing from end to start ($t=T \to 1$).
Their outputs at each timestep are concatenated: $h_t = [\overrightarrow{h}_t \,\|\, \overleftarrow{h}_t]$. This gives the model access to both past history and future context at every timestep.

---

### Q9: Does a Bidirectional RNN completely solve the vanishing gradient problem? Why or why not?
**Answer**: **No.** Bidirectionality does not fundamentally change the multiplicative recurrent formulation $W_{hh} h_{t-1}$. In each individual direction (forward or backward), the gradient can still vanish over long distances. However, because each direction has its own starting point at opposite ends of the sequence, the effective distance from any point in the sequence to a boundary is halved ($T/2$ instead of $T$), which partially mitigates, but does not mathematically eliminate, the vanishing gradient problem.

---

### Q10: Why must all four models be trained on the exact same dataset, task, and preprocessing?
**Answer**: In scientific benchmarking, the **Controlled Variable Principle** must be maintained. If models are evaluated on different datasets, different sequence lengths, or different splits, any variance in performance could be caused by data distribution shifts or preprocessing artifacts rather than the architectural design itself. Using identical data, splits, learning rates, loss functions, and classification heads ensures that differences in accuracy, F1, parameters, and gradient flow are strictly attributable to the recurrent architectures.

---

### Q11: Why is Accuracy alone not sufficient to evaluate these models?
**Answer**: Accuracy simply measures the fraction of correct predictions: $\frac{\text{Correct}}{\text{Total}}$. In multi-class classification or imbalanced scenarios, a model can achieve ~33% accuracy simply by collapsing into predicting a single majority class for all inputs (as our Vanilla RNN did by predicting Class 2 for 459 out of 480 test cases). Such a model has learned no useful discriminative representations. Metrics like **Macro F1-score**, **Precision**, **Recall**, and **Confusion Matrices** reveal whether the model is actually distinguishing all classes fairly.

---

### Q12: What does F1-Score mean, and why did we use Macro F1 in this experiment?
**Answer**: The F1-score is the **harmonic mean** of Precision and Recall:
$$\text{F1} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$
**Macro F1** calculates the F1-score independently for each class and then takes the unweighted average across classes:
$$\text{Macro F1} = \frac{1}{K} \sum_{k=1}^K \text{F1}_k$$
This ensures that every class is treated with equal importance. If a model collapses and gets 0% F1 on two classes and 50% on one, its Macro F1 will be severely penalized (~16%), exposing the failure immediately.

---

### Q13: How did you formulate a sequence task from static rock images without inventing fake labels?
**Answer**: We implemented a self-supervised **Spatial Trajectory Verification Task**. We extracted spatial slices of length $D=32$ along continuous trajectories of $T=32$ timesteps. The 3 target classes are defined deterministically by the extraction geometry:
- Class 0: Horizontal scan ($0^\circ$, spatial continuity along rows)
- Class 1: Vertical scan ($90^\circ$, spatial continuity along columns)
- Class 2: Temporally inverted scan ($180^\circ$, row sequence reversed)
Because these classes are mathematical properties of the spatial trajectories, ground truth is 100% objective, reproducible, and requires zero fabricated external annotations.

---

### Q14: How did you prevent data leakage given that you only had 11 images?
**Answer**: We enforced a strict **Image-Level Partition**:
- Images 1 to 7 were used exclusively for generating Training sequences.
- Images 8 and 9 were used exclusively for Validation sequences.
- Images 10 and 11 were used exclusively for Test sequences.
We did **not** split randomly at the sequence/patch level. Random patch splitting would cause patches from the same image to appear in both training and testing, causing severe data leakage and artificially inflated performance.

---

### Q15: What were the actual experimental conclusions of your project?
**Answer**:
1. **Vanilla RNN** suffered from severe gradient decay (mean gradient norm dropped by >92% from 0.124 to 0.0099 over 25 epochs) and suffered representational collapse, predicting almost exclusively one class and yielding the lowest Macro F1 (18.39%).
2. **Bidirectional RNN** achieved the highest accuracy (34.58%) and strong F1 (28.96%) by leveraging dual-direction context, halving the effective sequence distance.
3. **LSTM** achieved the highest Macro F1-score (29.02%) with stable, well-regulated gradient norms (mean: 0.029) and balanced confusion matrix predictions across all 3 classes.
4. **GRU** demonstrated consistent gradient flow (mean: 0.084) with 23% fewer recurrent parameters than LSTM, but required longer CPU training time due to sequential gate dependencies.
5. **Exploding gradients** were not observed under our training conditions (Adam optimizer, LR $10^{-3}$, sequence length 32).
