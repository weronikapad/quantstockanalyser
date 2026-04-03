import numpy as np
def run_quantum_analysis(closes: list, volumes: list) -> dict:
    closes = np.array(closes, dtype=float)
    volumes = np.array(volumes, dtype=float)
    returns = np.diff(closes) / closes[:-1]
    vols = volumes[1:] 
    vw_returns = returns * (vols/vols.mean())
    threshold = np.std(returns) * 0.3
    bull_mask = returns > threshold
    bear_mask = returns < -threshold
    neutral_mask = ~bull_mask & ~bear_mask
    alpha = np.sqrt(bull_mask.mean())
    beta = np.sqrt(neutral_mask.mean())
    gamma = np.sqrt(bear_mask.mean())
    recent = vw_returns[-10:] if len(vw_returns) >= 10 else vw_returns
    momentum = np.tanh(recent.mean() * 10)

    if momentum > 0:
     alpha += abs(momentum) * 0.2
    else:
       gamma += abs(momentum) * 0.2
    
    norm = np.sqrt(alpha**2 + beta**2 + gamma**2)
    alpha /= norm
    beta /= norm
    gamma /= norm

    p_bull = float(alpha**2)
    p_bear = float(gamma**2)
    p_neutral = float(beta**2)
    
    probs = np.array([p_bull, p_neutral, p_bear])
    probs = np.clip(probs, 1e-9, 1)
    entropy = float(-np.sum(probs * np.log2(probs)) / np.log2(3))

    coherence = float(2 * (abs(alpha * beta) + abs(beta * gamma) + abs(alpha * gamma)))

    price_std =float(np.std(closes[-20:]) / closes[-1])
    return_std = float(np.std(returns[-20:]))
    uncertainty = float(price_std * return_std * 100)

    phase_angle = float(np.arctan2(gamma - bear_mask.mean(), alpha - bull_mask.mean()))

    superpos_score = 1 - float(np.max(probs) - np.min(probs))
    superpos_label = "high" if superpos_score > 0.6 else "mid" if superpos_score > 0.35 else "low"

    dominant = ["bull", "neutral", "bear"][int(np.argmax(probs))]

    hist_vol = float(np.std(returns) * np.sqrt(252) * 100)

    return {
       "bull_pct": round(p_bull * 100, 2),
       "bear_pct": round(p_bear * 100, 2),
       "neutral_pct": round(p_neutral * 100, 2),
       "entanglement": round(entropy, 4),
       "coherence": round(coherence, 4),
       "uncertainty": round(uncertainty, 4),
       "phase": round(phase_angle, 4),
       "superposition": superpos_label,
       "dominant": dominant,
       "hist_volatility": round(hist_vol, 2),
       "momentum": round(float(momentum), 4),
    }

   