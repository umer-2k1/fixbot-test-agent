#!/bin/bash
# Demo script for FixBot - AI Test Auto-Fix Agent

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         FixBot - AI Test Auto-Fix Agent Demo              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📁 Repository: fixbot-test-agent"
echo "🎯 Purpose: Automatically detect and fix failing tests"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Show initial test failures"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest examples/test_example.py -v || true
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Run FixBot in dry-run mode (shows analysis)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python fixbot.py examples/test_example.py 2>&1 | head -40
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Features demonstrated"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Automatic test execution"
echo "✅ Failure detection and parsing"
echo "✅ Intelligent failure analysis"
echo "✅ AI-powered fix generation"
echo "✅ Safe dry-run mode (default)"
echo "✅ Detailed explanations"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Run unit tests for FixBot itself"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
pytest tests/test_fixbot.py -v
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Demo Complete! ✨                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "💡 To apply fixes: python fixbot.py examples/test_example.py --apply"
echo "📖 See README.md for full documentation"
