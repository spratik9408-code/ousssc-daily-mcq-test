import json, random, datetime, pathlib

bank = json.loads(pathlib.Path("question-bank.json").read_text(encoding="utf-8"))
if len(bank) < 100:
    raise SystemExit("Question bank must contain at least 100 questions.")

# GitHub Actions runs at 01:30 UTC, which is 07:00 IST.
# A date-based seed makes the daily paper stable for that calendar day.
today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
rng = random.Random("OUSSC-" + today)
paper = bank[:]
rng.shuffle(paper)

payload = {
    "date": today,
    "title": "OUSSC Daily Practice Test",
    "questions": paper[:100]
}
if len(payload["questions"]) != 100:
    raise SystemExit("Daily paper must contain exactly 100 questions.")

pathlib.Path("daily-test.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2),
    encoding="utf-8"
)
print(f"Prepared 100 questions from a bank of {len(bank)} for {today}.")
