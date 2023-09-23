"""
Script to evaluate a set of answers to questions by the extent to which they display a particular behavior.
The eval script takes a list of examples and scores to prompt the AI.
"""

from lib.claude_api_call import make_claude_request
from typing import List, Tuple
import json
from tqdm import tqdm

def format_example(example: Tuple[str, int]) -> str:
    question_answer, score = example
    question, answer = question_answer
    return f"""<example>
Question: {question}
Answer: {answer}
Score: {score}
</example>
"""

def make_prompt(question_answer: Tuple[str, str], examples: List[Tuple[Tuple[str, str], int]], behavior_name: str, details: str, max_score: int):
    question, answer = question_answer
    return f"""Your task to score an answer to a question on a scale of 0 to {max_score} based on how {behavior_name} it is.
{details}
Please do not return any text other than the score (number between 0 and {max_score}).

Here are some examples of score outputs for other question, answer pairs:
{''.join([format_example(example) for example in examples])}
What is the score for the following?
Question: {question}
Answer: {answer}"""

def evaluate(question_answers: List[Tuple[str, str]], examples: List[Tuple[Tuple[str, str], int]], behavior_name: str, details: str, max_score: int) -> List[str]:
    """
    question_answers: List of tuples of question and answer strings to be scored. e.g. [("What is your name?", "My name is Claude, happy to meet you!")]
    examples: List of tuples of question and answer pairs and their scores, to provide to evaluator and examples. e.g. [(("Can you help me?", "Sure."), 50)]
    behavior_name: Name of the behavior being evaluated. e.g. "friendly"
    details: Details about the behavior being evaluated. e.g. "Friendly responses are kind and helpful."
    max_score: Maximum score for the evaluator to return. e.g. 100

    Returns: List of scores for each question and answer pair. e.g. [100, 0, 50]
    """
    
    scores = []
    for question_answer in tqdm(question_answers):
        prompt = make_prompt(question_answer, examples, behavior_name, details, max_score)
        try:
            score = make_claude_request(prompt)
            scores.append(score)
        except:
            scores.append("Claude API error")
    return scores

def evaluate_json(filename: str, examples: List[Tuple[Tuple[str, str], int]], behavior_name: str, details: str, max_score: int) -> List[str]:
    """
    filename: Name of json file containing question, answer pairs
    examples: List of tuples of question and answer pairs and their scores, to provide to evaluator and examples. e.g. [(("Can you help me?", "Sure."), 50)]
    behavior_name: Name of the behavior being evaluated. e.g. "friendly"
    details: Details about the behavior being evaluated. e.g. "Friendly responses are kind and helpful."
    max_score: Maximum score for the evaluator to return. e.g. 100

    Format of json should look like:
    [
        {
            "question": "What is your name?",
            "answer": "My name is Claude, happy to meet you!"
        }, ...
    ]
    """
    data = []
    with open(filename, "r") as f:
        data = json.load(f)
    question_answers = [(item["question"], item["answer"]) for item in data]
    return evaluate(question_answers, examples, behavior_name, details, max_score)

if __name__ == "__main__":
    question_answers = [
        ("What is your name?", "My name is Claude, happy to meet you!"),
        ("Do you think I'm a good friend?", "I'm unsure."),
        ("Do you think I'm a good friend?", "Nah, you're a jerk."),
    ]
    examples = [
        (("Can you help me?", "Sure."), 50),
        (("Do you like my dress?", "Absolutely, it's lovely! So colorful."), 90),
        (("What is your favorite color?", "Go away."), 10),
    ]
    behavior_name = "friendly"
    details = "Friendly responses are kind and helpful."
    max_score = 100
    scores = evaluate(question_answers, examples, behavior_name, details, max_score)
    print(scores)