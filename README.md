# Indonesian–English Code-Mixed Cyberbullying Dataset

Annotated dataset accompanying the paper *"Is Multimodal Feature Fusion
Necessary? A Multi-Seed Ablation Study of XLM-RoBERTa for Indonesian–English
Code-Mixed Cyberbullying Detection."*

## Contents

| File | Rows | Purpose |
|------|-----:|---------|
| `train_data.xlsx` | 8,752 | Training split (minimal columns) |
| `val_data.xlsx` | 2,189 | Validation split (minimal columns) |
| `test_data.xlsx` | 2,736 | Test split (minimal columns) |
| `train_data_with_codemixed_preprocessing.xlsx` | 8,752 | Training split with code-mixed preprocessing features |
| `val_data_with_codemixed_preprocessing.xlsx` | 2,189 | Validation split with preprocessing features |
| `test_data_with_codemixed_preprocessing.xlsx` | 2,736 | Test split with preprocessing features |

**Total: 13,677 annotated tweets.** Splits are 64% / 16% / 20%.
Class balance: 6,837 cyberbullying (label 1) and 6,840 non-cyberbullying
(label 0). Inter-annotator agreement: Cohen's κ = 0.89 (three annotators).

## Column dictionary

| Column | Description |
|--------|-------------|
| `label` | 1 = cyberbullying, 0 = non-cyberbullying |
| `tweet_clean` | Normalized text (lowercased, mentions/URLs removed, slang normalized) |
| `tweet_clean_codemixed` | Cleaned text used for the code-mixing analysis |
| `lang_per_word` | Per-token language tags, e.g. `[id] kata [en] word` |
| `tweet_for_model` | Model input text, **anonymized**: usernames → `@USER`, links → `HTTPURL` |

## Privacy and Terms of Service

To respect the source platform's Terms of Service and to protect user privacy,
this release **does not contain the raw tweet text or any account
identifiers**. All user mentions have been replaced with the placeholder
`@USER` and all URLs with `HTTPURL`. No usernames, user IDs, or e-mail
addresses are included. The raw, unnormalized `tweet` column present in the
authors' internal files has been removed.

The file `sanitize_for_release.py` documents exactly how the released files
were produced from the internal annotated data.

## Citation

If you use this dataset, please cite the accompanying paper (details to be
added upon publication).

## License

This repository uses two licenses:

- **Source code** — [MIT License](LICENSE)
- **Dataset & annotations** — [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE-DATASET.md)
