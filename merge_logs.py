"""
Merge individual iteration log files into a single conversation log.
Run this script after all 4 iterations have completed.

Usage:
    python merge_logs.py

Output:
    conversation_log.txt - merged conversation log in chronological order
"""

import os

LOG_FILES = ["log_iter1.txt", "log_iter2.txt", "log_iter3.txt", "log_iter4.txt"]
OUTPUT_FILE = "conversation_log.txt"


def merge_logs():
    """Merge all iteration logs into one conversation log."""

    # Check all files exist
    missing = [f for f in LOG_FILES if not os.path.exists(f)]
    if missing:
        print(f"Warning: Missing log files: {', '.join(missing)}")
        print("Proceeding with available files only.")

    available = [f for f in LOG_FILES if os.path.exists(f)]
    if not available:
        print("Error: No log files found. Run iterations first.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("=" * 70 + "\n")
        out.write("HPS Architecture Design - Complete Conversation Log\n")
        out.write("ADD 3.0 via Direct LLM Interaction (gemini-3.1-pro-preview)\n")
        out.write(f"Merged on: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write("=" * 70 + "\n\n")

        for fname in available:
            with open(fname, "r", encoding="utf-8") as f:
                content = f.read()
            out.write(content)
            out.write("\n" + "-" * 70 + "\n\n")

    print(f"Merged {len(available)} log file(s) into {OUTPUT_FILE}")
    for f in available:
        print(f"  + {f}")


if __name__ == "__main__":
    merge_logs()