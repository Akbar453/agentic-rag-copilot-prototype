"""Offline, citation-backed inventory retrieval demo (not an LLM)."""
import csv
import re
import sys
from pathlib import Path

DATA = Path(__file__).parent / "data" / "inventory.csv"
STOP = {"is", "the", "of", "what", "how", "much", "many", "do", "we", "have", "in", "stock"}

def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP

def answer(question):
    with DATA.open(encoding="utf-8", newline="") as f:
        records = list(csv.DictReader(f))
    query = tokens(question)
    scored = []
    for idx, row in enumerate(records, start=2):
        doc = f"{row['product']} {row['notes']}"
        score = len(query & tokens(doc))
        if score:
            scored.append((score, idx, row))
    if not scored:
        return "No matching inventory entry found. Please ask about a listed product."
    _, lineno, best = sorted(scored, key=lambda x:(-x[0], x[1]))[0]
    return (f"{best['product']}: {best['quantity']} {best['unit']} available. "
            f"Source: data/inventory.csv row {lineno}.")

if __name__ == "__main__":
    print(answer(" ".join(sys.argv[1:]) or "What is the stock of rice?"))
