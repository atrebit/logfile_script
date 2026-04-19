import os
from pathlib import Path
from collections import Counter
import re

LOG_DIR = (
    "."  # aktuelles Verzeichnis, kann angepasst werden, z.B. "logs" oder "/var/logs"
)

ERROR_PATTERNS = [
    re.compile(r"ERROR[:\s-]*(.*)", re.IGNORECASE),
    re.compile(r"Exception[:\s-]*(.*)", re.IGNORECASE),
]


def extract_error(line):
    for pattern in ERROR_PATTERNS:
        match = pattern.search(line)
        if match:
            return match.group(1).strip() or "Unbekannter Fehler"


def process_file(file_path, counter):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:  # streaming -> für große Dateien (bis 10GB) geeignet
                error = extract_error(line)
                if error:
                    counter[error] += 1
    except Exception as e:
        print(f"Fehler beim Lesen von {file_path}: {e}")


def main():
    counter = Counter()
    # REKURSIV durch alle Ordner laufen -> os.walk, um alle .log-Dateien zu finden
    for root, _, files in os.walk(LOG_DIR):
        for file in files:
            if file.endswith(".log"):
                full_path = os.path.join(root, file)
                print(f"Verarbeite: {full_path}")
                process_file(full_path, counter)

    # Ergebnis ausgeben
    if counter:
        error, count = counter.most_common(1)[0]

        print(f"\nHäufigster Fehler:\n{error} ({count}x)")
        print("\nAlle Fehler und ihre Häufigkeit:")
        for item in counter.items():  # Alle Fehler und ihre Häufigkeit ausgeben
            print(f"{item[0]}: {item[1]}x")
    else:
        print("Keine Fehler gefunden.")


if __name__ == "__main__":
    main()
