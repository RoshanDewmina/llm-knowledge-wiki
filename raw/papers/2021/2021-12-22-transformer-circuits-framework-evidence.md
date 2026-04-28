---
title: A Mathematical Framework for Transformer Circuits Evidence Extracts
source_url: https://transformer-circuits.pub/2021/framework/index.html
source_domain: transformer-circuits.pub
author: "Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, Anthropic"
published: 2021-12-22
captured_at: 2026-04-28T22:30:46Z
capture_kind: verified-evidence-extracts
---

# A Mathematical Framework for Transformer Circuits Evidence Extracts

This immutable raw file preserves the exact evidence passages used by `wiki/sources/transformer-circuits-framework.md`. Passages were checked against the live source URL on 2026-04-28.

## Evidence Extracts`.
- [x] Link the source to study, Anki, implementation, and concept pages.
- [ ] Optional later pass: replace the stub raw paper file with an immutable full-text capture saved under a new raw path, then ingest that raw capture as a separate source if desired. Do not rewrite the existing raw stub.

## Verified Claims

- The paper argues that small attention-only transformers become more interpretable when rewritten into mathematically equivalent circuit terms: residual-stream communication, additive heads, QK/OV circuits, and path expansions. [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]] [[sources/transformer-circuits-framework#ex-independent-additive-heads]] [[sources/transformer-circuits-framework#ex-qk-ov-circuit]]
- The residual stream is framed as an additive communication channel: components read from it, write back into it, and can be analyzed through linear paths or subspaces rather than as a single contextual embedding. [[sources/transformer-circuits-framework#ex-residual-stream-communication]] [[sources/transformer-circuits-framework#ex-residual-stream-subspaces]]
- Multi-head attention can be viewed as independent head outputs added into the residual stream, even if efficient implementations concatenate head results. [[sources/transformer-circuits-framework#ex-independent-additive-heads]]
- QK and OV are the main attention-head interpretability objects: QK determines the attention pattern; OV determines what information is read and written when attention occurs. [[sources/transformer-circuits-framework#ex-qk-ov-circuit]] [[sources/transformer-circuits-framework#ex-attention-information-movement]]
- Zero-layer models correspond to bigram statistics; one-layer attention-only models add skip-trigram behavior; two-layer attention-only models can use head composition to form induction heads. [[sources/transformer-circuits-framework#ex-summary-results-zero-one-two]] [[sources/transformer-circuits-framework#ex-skip-trigram-examples]]
- Path expansion turns layer-product views into sums of end-to-end paths, which the paper treats as independently reasoned-about additive contributions to behavior. [[sources/transformer-circuits-framework#ex-path-expansion]]

## Evidence Extracts

### ex-summary-results-zero-one-two

Exact source passages checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> Zero layer transformers model bigram statistics. The bigram table can be accessed directly from the weights.

> One layer attention-only transformers are an ensemble of bigram and “skip-trigram” (sequences of the form "A… B C") models. The bigram and skip-trigram tables can be accessed directly from the weights, without running the model. These skip-trigrams can be surprisingly expressive. This includes implementing a kind of very simple in-context learning.

> Two layer attention-only transformers can implement much more complex algorithms using compositions of attention heads. These compositional algorithms can also be detected directly from the weights. Notably, two layer models use attention head composition to create “induction heads”, a very general in-context learning algorithm. We’ll explore induction heads in much more detail in a forthcoming paper.

### ex-independent-additive-heads

Exact source passage checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> Attention heads can be understood as independent operations, each outputting a result which is added into the residual stream. Attention heads are often described in an alternate “concatenate and multiply” formulation for computational efficiency, but this is mathematically equivalent.

### ex-qk-ov-circuit

Exact source passages checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> Attention heads can be understood as having two largely independent computations: a QK (“query-key”) circuit which computes the attention pattern, and an OV (“output-value”) circuit which computes how each token affects the output if attended to.

> What about the attention pattern? Typically, one computes the keys k_i = W_K x_i , computes the queries q_i = W_Q x_i and then computes the attention pattern from the dot products of each key and query vector A = \text{softmax}(q^T k) . But we can do it all in one step without referring to keys and queries: A = \text{softmax}(x^T W_Q^T W_K x) .

### ex-residual-stream-communication

Exact source passage checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> One of the main features of the high level architecture of a transformer is that each layer adds its results into what we call the “residual stream.” Constructing models with a residual stream traces back to early work by the Schmidhuber group, such as highway networks and LSTMs , which have found significant modern success in the more recent residual network architecture . In transformers, the residual stream vectors are often called the “embedding.” We prefer the residual stream terminology, both because it emphasizes the residual nature (which we believe to be important) and also because we believe the residual stream often dedicates subspaces to tokens other than the present token, breaking the intuitions the embedding terminology suggests. The residual stream is simply the sum of the output of all the previous layers and the original embedding. We generally think of the residual stream as a communication channel, since it doesn't do any processing itself and all layers communicate through it.

### ex-residual-stream-subspaces

Exact source passage checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> All components of a transformer (the token embedding, attention heads, MLP layers, and unembedding) communicate with each other by reading and writing to different subspaces of the residual stream. Rather than analyze the residual stream vectors, it can be helpful to decompose the residual stream into all these different communication channels, corresponding to paths through the model.

### ex-virtual-weights

Exact source passage checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> An especially useful consequence of the residual stream being linear is that one can think of implicit "virtual weights" directly connecting any pair of layers (even those separated by many other layers), by multiplying out their interactions through the residual stream. These virtual weights are the product of the output weights of one layer with the input weights Note that for attention layers, there are three different kinds of input weights: W_Q , W_K , and W_V . For simplicity and generality, we think of layers as just having input and output weights here. of another (ie. W_{I}^2W_{O}^1 ), and describe the extent to which a later layer reads in the information written by a previous layer.

### ex-attention-information-movement

Exact source passages checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> A governs which token's information is moved from and to.

> W_O W_V governs which information is read from the source token and how it is written to the destination token. What do we mean when we say that W_{OV}=W_O W_V governs which subspace of the residual stream the attention head reads and writes to when it moves information? It can be helpful to consider the singular value decomposition USV = W_{OV} . Since d_{head} < d_{model} , W_{OV} is low-rank and only a subset of the diagonal entries in S are non-zero. The right singular vectors V describe which subspace of the residual stream being attended to is “read in” (somehow stored as a value vector), while the left singular vectors U describe what subspace of the destination residual stream they are written to.

### ex-path-expansion

Exact source passages checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> Our key trick is to simply expand the product. This transforms the product (where every term corresponds to a layer), into a sum where every term corresponds to an end-to-end path .

> We claim each of these end-to-end path terms is tractable to understand, can be reasoned about independently, and additively combine to create model behavior.

### ex-skip-trigram-examples

Exact source passages checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> For a single head, here are some trigrams associated with the query " and" : back and → forth , eat and → drink , trying and → failing , day and → night , far and → away , created and → maintained , forward and → backward , past and → present , happy and → satisfied , walking and → talking , sick and → tired , … (see 12 head model, head 0:0 )

> One thing to note is that the learned skip-trigrams are often related to idiosyncrasies of one's tokenization. For example collapsing whitespace together allows individual tokens to reveal indentation. Not merging backslash into text tokens means that when the model is predicting LaTeX, there's a token after backslash that must be an escape sequence. And so on.

### ex-copying-ov-summary

Exact source passage checked from `https://transformer-circuits.pub/2021/framework/index.html`:

> One of the most striking things about looking at these matrices is that most attention heads in one layer models dedicate an enormous fraction of their capacity to copying. The OV circuit sets things up so that tokens, if attended to by the head, increase the probability of that token, and to a lesser extent, similar tokens. The QK circuit then only attends back to tokens which could plausibly be the next token. Thus, tokens are copied, but only to places where bigram-ish statistics make them seem plausible.
