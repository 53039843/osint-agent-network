"""
Bulk scan script: reads a list of targets from a file and submits
them all to the Celery worker queue.

Usage:
    python scripts/bulk_scan.py --file targets.txt
    python scripts/bulk_scan.py --targets "APT29,APT32,Lazarus Group"
"""
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from worker.tasks import run_pipeline_task


def main():
    parser = argparse.ArgumentParser(description="Bulk OSINT scan submitter")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="Path to a text file with one target per line")
    group.add_argument("--targets", type=str, help="Comma-separated list of targets")
    args = parser.parse_args()

    targets = []
    if args.file:
        with open(args.file, "r") as f:
            targets = [line.strip() for line in f if line.strip()]
    elif args.targets:
        targets = [t.strip() for t in args.targets.split(",") if t.strip()]

    if not targets:
        print("No targets found. Exiting.")
        sys.exit(1)

    print(f"Submitting {len(targets)} scan tasks to worker queue...")
    for target in targets:
        task = run_pipeline_task.delay(target)
        print(f"  ✓ Queued: '{target}' → task_id={task.id}")

    print(f"\nAll {len(targets)} tasks submitted.")
    print("Monitor progress with: celery -A worker.tasks flower")


if __name__ == "__main__":
    main()
