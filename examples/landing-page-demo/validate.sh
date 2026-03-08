#!/bin/bash
# Landing Page Validation Script
# Scores 0-100 based on completeness and quality

set -e
cd "$(dirname "$0")"

OUTPUT_FILE="output/index.html"
SCORE=0

if [ ! -f "$OUTPUT_FILE" ]; then
    echo "No output/index.html found"
    echo '{"score": 0}'
    exit 0
fi

CONTENT=$(cat "$OUTPUT_FILE")

# Check 1: Valid HTML structure (15 points)
if echo "$CONTENT" | grep -q "<!DOCTYPE html>" && echo "$CONTENT" | grep -q "</html>"; then
    SCORE=$((SCORE + 15))
    echo "[+15] Valid HTML structure"
fi

# Check 2: Has hero section with headline (15 points)
if echo "$CONTENT" | grep -qi "hero\|<h1"; then
    SCORE=$((SCORE + 15))
    echo "[+15] Hero section present"
fi

# Check 3: Has CTA button (10 points)
if echo "$CONTENT" | grep -qi "button\|btn\|cta"; then
    SCORE=$((SCORE + 10))
    echo "[+10] CTA button present"
fi

# Check 4: Has feature section (15 points)
if echo "$CONTENT" | grep -qi "feature\|benefit\|<section"; then
    SCORE=$((SCORE + 15))
    echo "[+15] Feature section present"
fi

# Check 5: Has CSS styling (15 points)
if echo "$CONTENT" | grep -q "<style\|\.css"; then
    SCORE=$((SCORE + 15))
    echo "[+15] CSS styling present"
fi

# Check 6: Responsive meta tag (10 points)
if echo "$CONTENT" | grep -q "viewport"; then
    SCORE=$((SCORE + 10))
    echo "[+10] Responsive viewport"
fi

# Check 7: Has footer (10 points)
if echo "$CONTENT" | grep -qi "<footer\|©\|copyright"; then
    SCORE=$((SCORE + 10))
    echo "[+10] Footer present"
fi

# Check 8: Has multiple sections (10 points)
SECTION_COUNT=$(echo "$CONTENT" | grep -ci "<section\|<div class=\".*section" || echo "0")
if [ "$SECTION_COUNT" -ge 3 ]; then
    SCORE=$((SCORE + 10))
    echo "[+10] Multiple sections ($SECTION_COUNT)"
fi

echo ""
echo "================================"
echo "Score: $SCORE/100"
echo "================================"
echo ""
echo "{\"score\": $SCORE}"
