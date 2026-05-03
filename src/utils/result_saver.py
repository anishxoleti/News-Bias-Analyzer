import json
import os
from datetime import datetime


def save_results(results):
    # Create results folder if it doesn't exist
    os.makedirs("results", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/analysis_{timestamp}.json"

    output = []
    for article, result in results:
        output.append({
            "id": article.id,
            "source": article.source_name,
            "source_type": article.source_type,
            "topic": article.topic,
            "author": article.author,
            "text": article.text,
            "analysis": result
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {filename}")
    return filename