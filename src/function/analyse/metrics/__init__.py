from .metric import estimate_pass_at_k, estimate_codebleu

METRICS_REGISTRY = {
    "pass_at_k": estimate_pass_at_k,
    "codebleu": estimate_codebleu,
}


def get_metric(metric_name):
    return METRICS_REGISTRY[metric_name]
