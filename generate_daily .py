import json, random, datetime, pathlib
bank = json.loads(pathlib.Path("question-bank.json").read_text(encoding="utf-8"))
today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
# Stable daily shuffle: the same date always produces the same paper.
rng = random.Random(today + "-OUSSC")
paper = bank[:]
rng.shuffle(paper)
payload = {"date": today, "title": "OUSSC Daily Practice Test", "questions": paper[:100]}
pathlib.Path("daily-test.json").write_text(
    json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"Prepared {len(payload['questions'])} questions for {today}")
