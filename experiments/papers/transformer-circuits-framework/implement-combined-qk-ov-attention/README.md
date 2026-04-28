# Implement Combined QK/OV Attention

Study: `wiki/studies/papers/transformer-circuits-framework.md`
Implementation task: `wiki/studies/implementations/implement-combined-qk-ov-attention.md`

This toy script verifies the algebraic equivalence between:

1. standard single-head attention with explicit Q/K/V matrices, and
2. the Transformer Circuits rewrite using combined QK and OV products.

Run:

```bash
python3 experiments/papers/transformer-circuits-framework/implement-combined-qk-ov-attention/main.py
```

Expected output:

```text
ok: standard attention equals combined QK/OV rewrite
max_abs_diff_output=...
max_abs_diff_attention=...
```

The script also includes a negative check: perturbing the OV product must make the rewritten output diverge from the standard output.
