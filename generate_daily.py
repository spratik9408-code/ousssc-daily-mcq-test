
import json
import random
import pathlib
import datetime
import sys
from zoneinfo import ZoneInfo

BASE_DIR = pathlib.Path(__file__).resolve().parent

BANK_FILE = BASE_DIR / "question-bank.json"
OUTPUT_FILE = BASE_DIR / "daily-test.json"

TOTAL_QUESTIONS = 100
PASS_MARK = 75
DURATION_MINUTES = 120


def main():
    # Load the question bank
    if not BANK_FILE.is_file():
        raise FileNotFoundError(
            f"Question bank not found: {BANK_FILE}"
        )

    with BANK_FILE.open("r", encoding="utf-8") as file:
        bank = json.load(file)

    if not isinstance(bank, list):
        raise ValueError("Question bank must contain a JSON list.")

    if len(bank) < TOTAL_QUESTIONS:
        raise ValueError("At least 100 questions are required.")

    # Validate the actual question-bank format
    for number, question in enumerate(bank, start=1):
        if not isinstance(question, dict):
            raise ValueError(f"Invalid question record: {number}")

        for field in ("subject", "q", "opts", "a", "exp"):
            if field not in question:
                raise ValueError(
                    f"Question {number} is missing field: {field}"
                )

        if not isinstance(question["opts"], list):
            raise ValueError(f"Question {number}: opts must be a list.")

        if len(question["opts"]) != 4:
            raise ValueError(
                f"Question {number} must have four options."
            )

        if not isinstance(question["a"], int) or question["a"] not in range(4):
            raise ValueError(
                f"Question {number} has an invalid answer index."
            )

    # Use Indian Standard Time
    today = datetime.datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).date().isoformat()

    # Generate a different paper for each date
    rng = random.Random("OUSSC-" + today)
    daily_questions = rng.sample(bank, TOTAL_QUESTIONS)

    # Keep the original question fields unchanged
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

    # Save the daily question paper
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            paper,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("SUCCESS: Daily test generated.")
    print("Date:", today)
    print("Questions:", len(daily_questions))
    print("Output:", OUTPUT_FILE)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("ERROR:", error)
        sys.exit(1)
