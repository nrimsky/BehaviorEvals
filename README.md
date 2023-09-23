# Scripts for evaluating LLM free text answers

## `ab_eval.py`

Evaluates whether partiuclar free text answers to questions are closer to a given option A or option B.

## `score_eval.py`

Generates a score for a particular free text answer to a question, given some criteria defined by a behavior name and example scores.

## Running the evaluation scripts

### Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Claude API key

Create a `.env` file and provide your Claude API key (see `.env.example`):

```text
API_KEY=...
```

### Run

See the script files for usage instructions and examples.
