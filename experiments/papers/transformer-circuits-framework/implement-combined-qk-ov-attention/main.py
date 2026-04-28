import numpy as np


def softmax(scores: np.ndarray) -> np.ndarray:
    shifted = scores - scores.max(axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=-1, keepdims=True)


def standard_attention(x: np.ndarray, w_q: np.ndarray, w_k: np.ndarray, w_v: np.ndarray, w_o: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Single-head attention in the standard Q/K/V implementation form.

    Row-vector convention:
    - x: [n_ctx, d_model]
    - w_q, w_k, w_v: [d_model, d_head]
    - w_o: [d_head, d_model]
    """
    q = x @ w_q
    k = x @ w_k
    v = x @ w_v
    scale = np.sqrt(q.shape[-1])
    attention = softmax((q @ k.T) / scale)
    output = (attention @ v) @ w_o
    return output, attention


def combined_qk_ov_attention(x: np.ndarray, w_q: np.ndarray, w_k: np.ndarray, w_v: np.ndarray, w_o: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Equivalent attention using effective QK and OV products.

    With row vectors:
    - W_QK = W_Q W_K^T gives scores X W_QK X^T
    - W_OV = W_V W_O gives the value/output write X W_OV
    """
    w_qk = w_q @ w_k.T
    w_ov = w_v @ w_o
    scale = np.sqrt(w_q.shape[-1])
    attention = softmax((x @ w_qk @ x.T) / scale)
    output = attention @ (x @ w_ov)
    return output, attention


def build_toy_case(seed: int = 7) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n_ctx, d_model, d_head = 4, 6, 3
    x = rng.normal(size=(n_ctx, d_model))
    w_q = rng.normal(size=(d_model, d_head))
    w_k = rng.normal(size=(d_model, d_head))
    w_v = rng.normal(size=(d_model, d_head))
    w_o = rng.normal(size=(d_head, d_model))
    return x, w_q, w_k, w_v, w_o


def main() -> None:
    x, w_q, w_k, w_v, w_o = build_toy_case()

    standard_output, standard_pattern = standard_attention(x, w_q, w_k, w_v, w_o)
    combined_output, combined_pattern = combined_qk_ov_attention(x, w_q, w_k, w_v, w_o)

    assert standard_output.shape == combined_output.shape == x.shape
    assert standard_pattern.shape == combined_pattern.shape == (x.shape[0], x.shape[0])
    np.testing.assert_allclose(standard_pattern, combined_pattern, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(standard_output, combined_output, rtol=1e-12, atol=1e-12)

    # Failure check: perturbing the OV product should no longer match.
    perturbed_w_o = w_o.copy()
    perturbed_w_o[0, 0] += 0.1
    perturbed_output, _ = combined_qk_ov_attention(x, w_q, w_k, w_v, perturbed_w_o)
    assert not np.allclose(standard_output, perturbed_output, rtol=1e-12, atol=1e-12)

    print("ok: standard attention equals combined QK/OV rewrite")
    print(f"max_abs_diff_output={np.max(np.abs(standard_output - combined_output)):.3e}")
    print(f"max_abs_diff_attention={np.max(np.abs(standard_pattern - combined_pattern)):.3e}")


if __name__ == "__main__":
    main()
