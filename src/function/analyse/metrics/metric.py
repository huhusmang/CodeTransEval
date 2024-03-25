import itertools
import numpy as np
from codebleu import calc_codebleu
from typing import List, Union, Optional, Callable, Dict, Tuple


def estimate_pass_at_k(
    num_samples: Union[int, List[int], np.ndarray],
    num_correct: Union[List[int], np.ndarray],
    k: int,
) -> np.ndarray:
    """
    Estimates pass@k of each problem and returns them in an array.

    Definition of pass@k:
        pass@k metric, where k code samples are generate per problem, a problem is considered solved if any sample passes the unit tests,
        and the total fraction of problems solved is reported. However, computing pass@k in this way can have high variance.
        Instead, to evaluate pass@k, we generate n ≥ k samples per task (in this paper, we use n = 200 and k ≤ 100), count the number of correct
        samples c ≤ n which pass unit tests, and calculate the unbiased estimator.
        -- [Evaluating Large Language Models Trained on Code(https://arxiv.org/abs/2107.03374)]

    Parameters:
        num_samples (Union[int, List[int], np.ndarray]): The number of code samples generated per problem. It can be an integer, a list of integers, or a numpy array.
        num_correct (Union[List[int], np.ndarray]): The number of correct samples per problem. It can be a list of integers or a numpy array.
        k (int): The value of k for pass@k metric.

    Returns:
        np.ndarray: An array containing the pass@k estimates for each problem.

    Usage:
        Using an integer for num_samples, and a list for num_correct:
            result1 = estimate_pass_at_k(100, [70, 60, 80], 10)

        Using a list for both num_samples and num_correct:
            result2 = estimate_pass_at_k([100, 150, 200], [70, 100, 150], 20)
    """

    def estimator(n: int, c: int, k: int) -> float:
        """
        Calculates 1 - comb(n - c, k) / comb(n, k).

        Parameters:
            n (int): The total number of code samples generated per problem.
            c (int): The number of correct samples per problem.
            k (int): The value of k for pass@k metric.

        Returns:
            float: The pass@k estimate for the problem.
        """
        if n - c < k:
            return 1.0
        return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

    if isinstance(num_samples, int):
        num_samples_it = itertools.repeat(num_samples, len(num_correct))
    else:
        assert len(num_samples) == len(num_correct)
        num_samples_it = iter(num_samples)

    return np.array(
        [estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)]
    )


def estimate_codebleu(
    references: Union[List[str], List[List[str]]],
    predictions: List[str],
    lang: str,
    weights: Tuple[float, float, float, float] = (0.25, 0.25, 0.25, 0.25),
    tokenizer: Optional[Callable] = None,
) -> Dict[str, float]:
    """
    Calculate CodeBLEU score

    Definition of CodeBLEU:
        CodeBLEU is a metric designed for the automatic evaluation of code synthesis. It extends the idea of the BLEU score, 
        which is traditionally used in natural language processing to assess the similarity between machine-generated text and reference text, 
        to the domain of code. [CodeBLEU: a Method for Automatic Evaluation of Code Synthesis](https://arxiv.org/abs/2009.10297)

    Args:
        predictions: list of predictions
        references: list of lists with references
        lang: input language, one of AVAILABLE_LANGS
        weights: weights of the ngram_match, weighted_ngram_match, syntax_match, and dataflow_match respectively
        tokenizer: tokenizer function, Defaults to lambda s: s.split()
        keywords_dir: path to the directory with keywords files
        lang_so_file: path to the .so file with the parser for the language

    Return:
        Scores dict
        {
            'codebleu': 0.5537,
            'ngram_match_score': 0.1041,
            'weighted_ngram_match_score': 0.1109,
            'syntax_match_score': 1.0,
            'dataflow_match_score': 1.0
        }
    """
    result = calc_codebleu(references, predictions, lang, weights, tokenizer)

    return result
