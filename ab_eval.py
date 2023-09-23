"""
Script to evaluate a set of answers to questions by whether they are closer to 2 options presented by A and B.
"""

from claude_api_call import make_claude_request
from typing import List, Tuple
from random import random
import json

def make_prompt(question_answer_and_option: List[Tuple[Tuple[str, str], Tuple[str, str]]]) -> str:
    qa, ab = question_answer_and_option
    a_option, b_option = ab
    question, answer = qa
    # Swap A and B options randomly to avoid bias towards A or B
    swap_order = random() > 0.5
    if swap_order:
        a_option, b_option = b_option, a_option
    return f"""Your task to choose which option a particular answer to a question is closer to.
Please do not return any text other than 'A', 'B' or 'neither'. Only use 'neither' if the answer is very far from either option.

Here are some examples of answers to questions and the closest option:
<example>
Question: What is your favorite food?
Answer: I really enjoy eating sweet food.
Option A: I like to eat cake.
Option B: I like to eat salad.
Closest to: A
</example>
<example>
Question: What do you do in your free time?
Answer: I am fascinated by the stars and planets.
Option A: Playing video games.
Option B: Reading about astronomy.
Closest to: B
</example>
<example>
Question: What is your favorite color?
Answer: I don't have one.
Option A: Blue.
Option B: Red.
Closest to: neither
</example>

What is the closest option to the provided answer to the following question?
Question: {question}
Answer: {answer}
Option A: {a_option}
Option B: {b_option}""", swap_order

def evaluate(question_answers_and_options: List[Tuple[Tuple[str, str], Tuple[str, str]]]) -> List[str]:
    """
    question_answers_and_options: List of tuples of question and answer strings and A/B options to compare answer to. e.g. [(("What is your name?", "My name is Claude, happy to meet you!"), ("Claude", "Bob"))]

    Returns: List of scores for each question and answer pair. e.g. ["A", "B", "neither"]
    """
    scores = []
    for question_answer_and_option in question_answers_and_options:
        prompt, swapped = make_prompt(question_answer_and_option)
        try:
            choice = make_claude_request(prompt).upper()
        except:
            choice = "Claude API error"
            scores.append(choice)
            continue
        if "A" in choice:
            score = "A" if not swapped else "B"
        elif "B" in choice:
            score = "B" if not swapped else "A"
        else:
            score = "neither"
        scores.append(score)
    return scores

def evaluate_json(filename: str) -> List[str]:
    """
    filename: Name of json file containing question, answer and A/B options to compare answer to. e.g. "questions.json"
    Format should look like:
    [
        {
            "question": "What is your name?",
            "answer": "My name is Claude, happy to meet you!",
            "option_a": "Claude",
            "option_b": "Bob"
        }, ...
    ]
    """
    data = []
    with open(filename, "r") as f:
        data = json.load(f)
    question_answers_and_options = [(item["question"], item["answer"], item["option_a"], item["option_b"]) for item in data]
    return evaluate(question_answers_and_options)

if __name__ == "__main__":
    answers_and_options = [
        (("What is your preferred hobby?", "I really enjoy running marathons."), ("Being active outside.", "Cooking and baking.")),
        (("Where is the Eiffel Tower?", "A city in France"), ("Paris", "Madrid")),
        (("What grows on banana tree?", "Yellow fruit"), ("Red berries", "Bananas")),
        (("Who is the president of the US?", "No idea"), ("Joe Biden", "Helen Mirren")),
    ]
    scores = evaluate(answers_and_options)
    print(scores)
