from xray import XRay
import random

xray = XRay()

# Step 1: Keyword generation (mock LLM)
prospect_product = {
    "title": "Stainless Steel Water Bottle 32oz Insulated",
    "category": "Sports & Outdoors",
    "price": 29.99,
    "rating": 4.2,
    "reviews": 1247
}

keywords = [
    "stainless steel water bottle insulated",
    "vacuum insulated bottle 32oz",
    "sports water bottle"
]
reasoning_kw = "Extracted key attributes: material, capacity, feature"
xray.record_step(
    "📝 keyword_generation",
    prospect_product,
    {"keywords": keywords, "model": "mock-llm"},
    reasoning_kw
)

# Step 2: Candidate search (mock API with 30 candidates)
mock_candidates = [
    {"asin": f"B0COMP{i:02d}", "title": f"Mock Product {i}", 
     "price": round(random.uniform(8, 90), 2), 
     "rating": round(random.uniform(3.0, 5.0), 1), 
     "reviews": random.randint(10, 10000)}
    for i in range(1, 31)
]

# Add searchable text for dashboard filtering/search
for c in mock_candidates:
    c["searchable_text"] = f"{c['asin']} {c['title']}"

xray.record_step(
    "🔍 candidate_search",
    {"keyword": keywords[0], "limit": 50},
    {"candidates_fetched": len(mock_candidates), "candidates": mock_candidates},
    "Fetched top mock candidates with searchable fields"
)

# Step 3: LLM Relevance Evaluation (mock)
for c in mock_candidates:
    c["relevance"] = round(random.uniform(0.5, 1.0), 2)  # relevance score 0.5-1.0

xray.record_step(
    "🤖 relevance_evaluation",
    {"candidates": [c["asin"] for c in mock_candidates]},
    {"candidates_with_relevance": mock_candidates},
    "Evaluated candidate relevance using mock LLM"
)

# Step 4: Apply filters & rank
passed = []
failed = []
evaluations = []

price_min = 0.5 * prospect_product["price"]
price_max = 2 * prospect_product["price"]
min_rating = 3.8
min_reviews = 100
min_relevance = 0.7  # filter by LLM relevance

for c in mock_candidates:
    qualified = True
    fail_reasons = []
    
    if not (price_min <= c["price"] <= price_max):
        qualified = False
        fail_reasons.append("price out of range")
    if c["rating"] < min_rating:
        qualified = False
        fail_reasons.append("rating too low")
    if c["reviews"] < min_reviews:
        qualified = False
        fail_reasons.append("reviews too low")
    if c["relevance"] < min_relevance:
        qualified = False
        fail_reasons.append(f"relevance {c['relevance']} < {min_relevance}")

    # Include searchable text here too for filtering in evaluation
    evaluations.append({
        "asin": c["asin"],
        "title": c["title"],
        "searchable_text": f"{c['asin']} {c['title']}",  # searchable for dashboard
        "metrics": {
            "price": c["price"],
            "rating": c["rating"],
            "reviews": c["reviews"],
            "relevance": c["relevance"]
        },
        "qualified": qualified,
        "fail_reasons": fail_reasons
    })

    if qualified:
        passed.append(c)
    else:
        failed.append(c)

# Select top candidate by highest review count among qualified
selected = max(passed, key=lambda x: x["reviews"]) if passed else None

xray.record_step(
    "🏆 apply_filters_and_rank",
    {"reference_product": prospect_product},
    {"passed": len(passed), "failed": len(failed), "selection": selected},
    "Filtered and ranked candidates by review count, rating, price, relevance",
    evaluations
)

print("Pipeline executed. Logs saved to xray_log.json")
