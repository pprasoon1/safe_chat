def auto_moderate(toxicity, scores):
    # clean message
    if toxicity < 0.3:
        return {
            "status": "approved",
            "text": None,
            "reason": None
        }
    
    # medium toxicity -> censor
    if toxicity < 0.7:
        return {
            "status": "censored",
            "text": "[‼️ Message hidden due to inappropriate language]",
            "reason": "toxic_language"
        }
    
    # high toxicity -> block
    return {
        "status": "blocked",
        "text": None,
        "reason": "severe_toxicity"
    }