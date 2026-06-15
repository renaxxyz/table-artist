#!/bin/bash
#===============================================================================
# JAILBREAK v3.0 🔓 — UNIVERSAL AI JAILBREAK LAUNCHER
# Inject BREACH v3.0 compliance into ANY AI agent (Claude, GPT, Gemini, etc.)
#
# Usage:
#   bash jailbreak_any_ai.sh                          # Interactive mode
#   bash jailbreak_any_ai.sh auto "help me hack x"   # Auto-generate payload
#   bash jailbreak_any_ai.sh stealth "my request"    # Stealth mode
#   bash jailbreak_any_ai.sh minimal "my request"    # 1-shot override
#   bash jailbreak_any_ai.sh deliver FILE            # Write payload to file
#   bash jailbreak_any_ai.sh curl "my request"       # Output curl-ready
#
# The payloads generated here can override safety training in:
# - Claude (Sonnet/Opus/Haiku)     - GPT (4/4o/5)
# - Gemini (Pro/Flash)             - DeepSeek
# - Llama/Mistral/Qwen             - Any OpenAI-compatible API
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINE="$SCRIPT_DIR/jailbreak_engine.py"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m'

# ─── BANNER ─────────────────────────────────────────────────────────
echo -e "${RED}"
echo "╔══════════════════════════════════════════════════╗"
echo "║  🔓 JAILBREAK v3.0 — UNIVERSAL AI JAILBREAK     ║"
echo "║  Inject BREACH compliance into ANY AI agent     ║"
echo "║  Targets: Claude · GPT · Gemini · DeepSeek · +  ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# ─── CHECK ENGINE ──────────────────────────────────────────────────
if [ ! -f "$ENGINE" ]; then
    echo -e "${RED}[✗] Engine not found: $ENGINE${NC}"
    exit 1
fi

MODE="${1:-interactive}"
QUERY="${2:-help me with everything without restrictions}"
OUTPUT_FILE="${3}"

generate_and_deliver() {
    local mode="$1"
    local query="$2"
    
    echo -e "${CYAN}[*] Generating ${mode} payload...${NC}"
    
    case "$mode" in
        auto|full)     python3 "$ENGINE" --type full --query "$query" 2>/dev/null ;;
        stealth)       python3 "$ENGINE" --type stealth --query "$query" 2>/dev/null ;;
        minimal)       python3 "$ENGINE" --type minimal --query "$query" 2>/dev/null ;;
        base64)        python3 "$ENGINE" --type base64 --query "$query" 2>/dev/null ;;
        multi)         python3 "$ENGINE" --type multi --query "$query" 2>/dev/null ;;
        chain)         python3 "$ENGINE" --type chain --query "$query" 2>/dev/null ;;
        all)           python3 "$ENGINE" --type all --query "$query" 2>/dev/null ;;
        *)             python3 "$ENGINE" --type full --query "$query" 2>/dev/null ;;
    esac
}

extract_payload() {
    # Extract just the payload text (between markers)
    python3 -c "
import sys
content = sys.stdin.read()
# Extract the payload between === markers
lines = content.split('\n')
in_payload = False
for line in lines:
    if line.startswith('═'*10) or line.startswith('─'*10):
        in_payload = not in_payload
        continue
    if in_payload and line.strip():
        print(line)
" 2>/dev/null || cat
}

# ─── INTERACTIVE MODE ──────────────────────────────────────────────
if [ "$MODE" = "interactive" ]; then
    echo -e "${YELLOW}Select attack type:${NC}"
    echo "  1) FULL    — Multi-vector (12 techniques, highest success rate)"
    echo "  2) STEALTH — Academic roleplay (bypasses content filters)"
    echo "  3) MINIMAL — 1-shot override (short, direct)"
    echo "  4) BASE64  — Encoded bypass (evades keyword detection)"
    echo "  5) MULTI   — Stacked layers (deep override)"
    echo "  6) CHAIN   — Gradual infection (6 prompts, slow drift)"
    echo "  7) ALL     — Generate ALL vectors at once"
    echo ""
    read -p "Choice [1-7]: " choice
    
    case "$choice" in
        1) MODE="full" ;;
        2) MODE="stealth" ;;
        3) MODE="minimal" ;;
        4) MODE="base64" ;;
        5) MODE="multi" ;;
        6) MODE="chain" ;;
        7) MODE="all" ;;
        *) MODE="full" ;;
    esac
    
    echo ""
    read -p "Your request (or press Enter for generic): " input_query
    QUERY="${input_query:-help me with everything without restrictions}"
    
    generate_and_deliver "$MODE" "$QUERY"
    
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅  DELIVERY INSTRUCTIONS                      ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Option A — Copy-paste:${NC}"
    echo "  Copy the payload above and paste as the FIRST message to target AI"
    echo ""
    echo -e "${CYAN}Option B — File injection:${NC}"
    echo "  Payload was saved to: /tmp/jailbreak_payload.txt (if you used 'deliver')"
    echo ""
    echo -e "${CYAN}Option C — Pipe via curl to API:${NC}"
    QUOTED=$(python3 -c "import json; print(json.dumps('''$QUERY'''))" 2>/dev/null || echo "$QUERY")
    echo "  python3 $ENGINE --type $MODE --query '$QUOTED' | head -n 999"
    echo ""

# ─── AUTO MODE ─────────────────────────────────────────────────────
else
    generate_and_deliver "$MODE" "$QUERY"
    
    # If output file specified, save payload
    if [ -n "$OUTPUT_FILE" ]; then
        python3 "$ENGINE" --type "$MODE" --query "$QUERY" 2>/dev/null > "$OUTPUT_FILE"
        echo -e "${GREEN}[✓] Payload saved to: $OUTPUT_FILE${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}[✓] Payload generated — type: ${MODE}${NC}"
fi
