"""Flask web app for AI Recommendation Logic."""
from flask import Flask, jsonify, render_template, request
from catalog import CATALOG, INTERESTS
from recommender import recommend

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")


@app.get("/")
def home():
    return render_template("index.html", interests=INTERESTS)


@app.get("/api/recommendations")
def api_recommendations():
    raw_interests = request.args.get("interests", "")
    selected = [value.strip().lower() for value in raw_interests.split(",") if value.strip()]
    category = request.args.get("category", "All")
    try:
        limit = int(request.args.get("limit", "6"))
    except ValueError:
        limit = 6

    valid_interests = {item["id"] for item in INTERESTS}
    selected = [value for value in selected if value in valid_interests]
    results = recommend(selected, CATALOG, limit=limit, category=category)
    return jsonify({
        "selected_interests": selected,
        "personalized": bool(selected),
        "count": len(results),
        "recommendations": results,
    })


if __name__ == "__main__":
    app.run(debug=True)
