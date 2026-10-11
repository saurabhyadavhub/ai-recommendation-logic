# AI Recommendation Logic

A beginner-friendly recommendation system built for **Artificial Intelligence Project 3 – Industrial Training Kit (DecodeLabs, Batch 2026)**.

It asks users for interests, compares those preferences with item tags using a transparent similarity score, and ranks the most relevant recommendations.

## Features
- Choose interests from a simple web interface
- Similarity scoring based on tag overlap (Jaccard similarity)
- Ranked recommendations with match percentages and explanations
- Filter by category and adjust the number of results
- Responsive layout for desktop and mobile
- Unit tests for the recommendation logic
- No API keys, external services, or database required

## Tech stack
- Python 3.10+
- Flask
- HTML, CSS, JavaScript
- pytest for tests

## Quick start

```bash
python -m venv .venv
```

Activate the environment:

**Windows**
```powershell
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies and run:

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Run tests

```bash
pip install -r requirements-dev.txt
pytest
```

## How the algorithm works

Each item has a set of tags. The user's selected interests are treated as another set.

**Jaccard similarity**

`similarity = size(user interests ∩ item tags) / size(user interests ∪ item tags)`

The score is between 0 and 1. The app sorts items by score, then by title for consistent results. If there are no matching interests, the interface displays popular starter suggestions and clearly labels them as general suggestions rather than pretending they match.

## Project structure

```text
ai-recommendation-logic/
├── app.py
├── recommender.py
├── catalog.py
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── README.md
├── LICENSE
├── src/
│   └── static/
│       ├── style.css
│       └── app.js
│   └── templates/
│       └── index.html
└── tests/
    └── test_recommender.py
```

## GitHub upload

1. Create a new repository on GitHub named `ai-recommendation-logic`.
2. Keep it **Public** if you need a shareable portfolio link.
3. Upload the contents of this folder (not the ZIP file itself), or use Git:

```bash
git init
git add .
git commit -m "Build AI recommendation logic project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ai-recommendation-logic.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## Customization ideas
- Add user ratings and incorporate them into ranking
- Store users and preferences in SQLite
- Expand the catalog or add a content-based similarity metric
- Add collaborative filtering after understanding this baseline
