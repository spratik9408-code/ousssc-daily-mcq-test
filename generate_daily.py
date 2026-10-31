
import json
import random
import pathlib
import datetime
import sys

BASE_DIR = pathlib.Path(__file__).resolve().parent
BANK_FILE = BASE_DIR / "question-bank.json"
OUTPUT_FILE = BASE_DIR / "daily-test.json"

TOTAL_QUESTIONS = 100
PASS_MARK = 75
DURATION_MINUTES = 120


def load_bank():
    if not BANK_FILE.is_file():
        raise FileNotFoundError(
            f"Cannot find question-bank.json at: {BANK_FILE}"
        )

    with BANK_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        questions = data
    elif isinstance(data, dict):
        questions = data.get("questions")
    else:
        questions = None

    if not isinstance(questions, list):
        raise ValueError(
            "Question bank must be a list or contain a questions list."
        )

    if len(questions) < TOTAL_QUESTIONS:
        raise ValueError(
            f"Only {len(questions)} questions found; 100 are required."
        )

    return questions


def validate_bank(questions):
    for number, q in enumerate(questions, start=1):
        if not isinstance(q, dict):
            raise ValueError(f"Question {number} is not an object.")

        if not q.get("question"):
            raise ValueError(f"Question {number} has no question text.")

        options = q.get("options")

        if isinstance(options, list):
            valid_options = len(options) == 4
        elif isinstance(options, dict):
            valid_options = all(
                key in options for key in ("A", "B", "C", "D")
            )
        else:
            valid_options = False

        if not valid_options:
            raise ValueError(
                f"Question {number} must have four A/B/C/D options."
            )

        if "answer" not in q:
            raise ValueError(f"Question {number} has no answer.")


def main():
    questions = load_bank()
    validate_bank(questions)

    today = datetime.datetime.now(
        datetime.timezone.utc
    ).astimezone(
        datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    ).date().isoformat()

    rng = random.Random("OUSSC-" + today)
    daily_questions = rng.sample(questions, TOTAL_QUESTIONS)

    paper = {
        "title": "OUSSC Daily Constable Practice Test",
        "date": today,
        "totalQuestions": TOTAL_QUESTIONS,
        "durationMinutes": DURATION_MINUTES,
        "positiveMarks": 1,
        "negativeMarks": 0.25,
        "unattemptedMarks": 0,
        "passMark": PASS_MARK,
        "questions": daily_questions
    }

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(paper, f, ensure_ascii=False, indent=2)

    print(f"SUCCESS: Generated {TOTAL_QUESTIONS} questions for {today}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}")
        sys.exit(1)
