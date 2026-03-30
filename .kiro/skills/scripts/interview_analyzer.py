#!/usr/bin/env python3
"""Analyze user interview transcripts."""

import argparse
import json
import re
from collections import Counter

def extract_pain_points(text: str) -> list:
    """Extract pain points from transcript."""
    pain_keywords = [
        "frustrating", "annoying", "difficult", "hard", "problem",
        "issue", "struggle", "hate", "wish", "can't", "doesn't work"
    ]
    
    sentences = re.split(r'[.!?]', text)
    pain_points = []
    
    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in pain_keywords):
            pain_points.append(sentence.strip())
    
    return pain_points

def extract_feature_requests(text: str) -> list:
    """Extract feature requests."""
    request_patterns = [
        r"I wish (.*)",
        r"It would be great if (.*)",
        r"I need (.*)",
        r"I want (.*)",
        r"Can you add (.*)"
    ]
    
    requests = []
    for pattern in request_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        requests.extend(matches)
    
    return requests

def analyze_sentiment(text: str) -> str:
    """Simple sentiment analysis."""
    positive_words = ["love", "great", "awesome", "excellent", "perfect", "easy"]
    negative_words = ["hate", "terrible", "awful", "bad", "difficult", "frustrating"]
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"

def main():
    parser = argparse.ArgumentParser(description="Interview analyzer")
    parser.add_argument("transcript", help="Interview transcript file")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    with open(args.transcript, 'r') as f:
        text = f.read()

    pain_points = extract_pain_points(text)
    feature_requests = extract_feature_requests(text)
    sentiment = analyze_sentiment(text)

    result = {
        "pain_points": pain_points[:10],
        "feature_requests": feature_requests[:10],
        "sentiment": sentiment,
        "word_count": len(text.split())
    }

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print("Interview Analysis")
        print("=" * 80)
        print(f"Sentiment: {sentiment}")
        print(f"Word count: {result['word_count']}")
        print()
        print("Pain Points:")
        for i, pain in enumerate(pain_points[:5], 1):
            print(f"{i}. {pain}")
        print()
        print("Feature Requests:")
        for i, req in enumerate(feature_requests[:5], 1):
            print(f"{i}. {req}")

if __name__ == "__main__":
    main()
