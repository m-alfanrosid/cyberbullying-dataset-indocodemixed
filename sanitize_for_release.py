#!/usr/bin/env python3
"""
sanitize_for_release.py

Prepare the Indonesian-English code-mixed cyberbullying dataset for public
release (e.g., GitHub) in a way that respects the platform's Terms of Service
and protects user privacy:

  * The raw ``tweet`` column (unnormalized text) is DROPPED.
  * ``tweet_for_model`` is kept but ANONYMIZED: @mentions -> @USER,
    URLs -> HTTPURL, e-mails -> EMAIL. This preserves model-input
    reproducibility without exposing account identifiers.
  * Already-clean columns (tweet_clean, tweet_clean_codemixed, lang_per_word,
    label) are passed through and re-verified.
  * The script verifies that NO real @mention / URL / e-mail remains in any
    released column and prints a report.

Usage:
    python sanitize_for_release.py --in <input_dir> --out <output_dir>
"""

import argparse
import re
from pathlib import Path
import pandas as pd

# --- normalization patterns -------------------------------------------------
URL_RE     = re.compile(r'(https?://\S+|www\.\S+)', re.IGNORECASE)
MENTION_RE = re.compile(r'@\w+')
EMAIL_RE   = re.compile(r'[\w.\-]+@[\w.\-]+\.\w+')

# columns that must never leave your machine
DROP_COLS = ['tweet']
# columns that contain raw text and must be anonymized before release
ANONYMIZE_COLS = ['tweet_for_model']
# preferred output column order (only those present are written)
COLUMN_ORDER = ['tweet_clean', 'tweet_clean_codemixed', 'lang_per_word',
                'tweet_for_model', 'label']


def anonymize(text: str) -> str:
    if not isinstance(text, str):
        return text
    text = EMAIL_RE.sub('EMAIL', text)      # e-mail first (contains @)
    text = URL_RE.sub('HTTPURL', text)
    text = MENTION_RE.sub('@USER', text)
    return text


def verify_clean(df: pd.DataFrame):
    """Return {column: {mention, url, email}} counts of leftover real PII."""
    report = {}
    for col in df.columns:
        if df[col].dtype == object:
            s = df[col].astype(str)
            # a real mention is @something that is NOT the @USER placeholder
            real_mention = s.apply(
                lambda x: bool(re.search(r'@(?!USER\b)\w+', x))).sum()
            url = s.apply(lambda x: bool(URL_RE.search(x))).sum()
            email = s.apply(lambda x: bool(EMAIL_RE.search(x))).sum()
            if real_mention or url or email:
                report[col] = {'mention': int(real_mention),
                               'url': int(url), 'email': int(email)}
    return report


def process_file(path: Path, out_dir: Path):
    df = pd.read_excel(path)
    original_cols = list(df.columns)

    for col in ANONYMIZE_COLS:
        if col in df.columns:
            df[col] = df[col].map(anonymize)

    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

    ordered = [c for c in COLUMN_ORDER if c in df.columns]
    ordered += [c for c in df.columns if c not in ordered]
    df = df[ordered]

    report = verify_clean(df)
    status = 'CLEAN' if not report else 'LEFTOVER PII FOUND'

    out_path = out_dir / path.name
    df.to_excel(out_path, index=False)

    print(f"[{status}] {path.name}")
    print(f"    rows={len(df)}  in_cols={original_cols}")
    print(f"    out_cols={list(df.columns)}")
    if report:
        print(f"    !! leftover: {report}")
    return len(df), df.get('label')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in',  dest='indir',  required=True)
    ap.add_argument('--out', dest='outdir', required=True)
    args = ap.parse_args()

    in_dir, out_dir = Path(args.indir), Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    label_frames = []
    for path in sorted(in_dir.glob('*.xlsx')):
        n, labels = process_file(path, out_dir)
        total += n
        if labels is not None:
            label_frames.append(labels)

    print("\n--- summary ---")
    print(f"files processed : {len(list(in_dir.glob('*.xlsx')))}")
    print(f"total rows      : {total}")
    if label_frames:
        alllabels = pd.concat(label_frames)
        # de-duplicate the double counting from the two file variants:
        # report per-unique-split not needed; just show distribution once
        print(f"label values    : {sorted(alllabels.unique().tolist())}")


if __name__ == '__main__':
    main()
