#!/usr/bin/env python3
# ai.py
# FHA GPT v32.0 - The Fixed Master
# - Yana gane Gaisuwa da Hira (Chat Mode).
# - Yana bincike a Brain.txt (Research Mode).
# - Yana lissafi da Lokaci.

from flask import Flask, request, jsonify
from flask_cors import CORS
import re, random, os, datetime
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

BRAIN_FILE = "brain.txt"

# ==============================================================================
# 1. INITIAL BRAIN LOADER
# Idan babu brain.txt, zai kirkiri shi da bayanai.
# ==============================================================================
DEFAULT_DATA = """
RAYUWA: Rayuwa tana da dadi idan ana lafiya da arziki. Hakuri shine maganin zaman duniya.
SOYAYYA: Soyayya gamon jini ce. Masoyi na gaskiya baya yaudara.
KOYARWA: Koyarwa ita ce hanyar bada ilimi ga wani. Malami yana amfani da allo.
MOTA: Mota abin hawa ne mai inji wanda ke saukaka zirga-zirga.
FASAHA: Fasaha tana nufin kere-kere na zamani don saukaka rayuwa.
ILIMI: Ilimi haske ne. Jahilci duhu ne. Karatu yana bude kwakwalwa.
KUDI: Kudi shine abin da ake amfani da shi wajen ciniki.
ABINCI: Abinci yana gina jiki. Tuwo da shinkafa sune abincin Hausawa.
LISSAPIN KUDI: Kudi yana bukatar lissafi.
KANO: Kano ta Dabo cibiyar kasuwanci ce a Afirka ta Yamma.
LADABI: Ladabi shine girmama na gaba. Yana kawo albarka.
ISKA: Iska tana da muhimmanci. Idan babu iska babu numfashi.
"""

def load_brain():
    if not os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_DATA)
    
    with open(BRAIN_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# ==============================================================================
# 2. LOGIC ENGINE (HIRA & LISSAFI)
# ==============================================================================
FUNNY_STORIES = [
    "Labarin Gizo: Wata rana Gizo ya sayo kayan miya, Koki tace babu itace. Sai yace bari in cinye su danye!",
    "Wani Bahaushe ya je Ingila, ya ga Bature yana cin tuwo da cokali, yace 'A'a, ai hannu yafi dadi'.",
    "Likita ya tambayi mahaukaci: 'Me yasa kake dukan bango?' Mahaukaci yace: 'Saboda yana min dariya!'."
]

def check_chat_logic(text):
    clean = text.lower()
    
    # 1. Gaisuwa (Greetings)
    if any(w in clean for w in ['sannu', 'barka', 'ina kwana', 'slm', 'hello', 'hi']):
        return "Sannu! Barka da zuwa FHA GPT v32. Nine mataimakinka. Me kake son sani?"
    
    if any(w in clean for w in ['lafiya', 'nagode', 'na gode']):
        return "Madalla, Allah ya kara lafiya da natsuwa."

    # 2. Labari
    if 'labari' in clean:
        return f"To ga wani labari: \n{random.choice(FUNNY_STORIES)}"

    # 3. Lokaci
    if 'lokaci' in clean or 'karfe' in clean:
        now = datetime.datetime.now()
        return f"Yanzu lokaci shine: {now.strftime('%I:%M %p')}."

    # 4. Lissafi (Simple Math)
    if any(c.isdigit() for c in clean):
        try:
            expr = clean.replace('ahada', '+').replace('da', '+').replace('cire', '-').replace('sau', '*')
            # Cire haruffa, bar lambobi da alamomi
            safe_expr = re.sub(r"[^0-9\+\-\*\/\.]", "", expr)
            if safe_expr:
                return f"Lissafin ya kama: {eval(safe_expr)}"
        except: pass

    return None

# ==============================================================================
# 3. SEARCH ENGINE (BINCIKE A BRAIN.TXT)
# ==============================================================================
class FHA_GPT_V32:
    def __init__(self):
        self.brain_lines = load_brain()

    def search_brain(self, query):
        clean_q = query.lower().replace("bani", "").replace("menene", "").replace("labarin", "").strip()
        
        best_match = None
        max_score = 0
        
        for line in self.brain_lines:
            # Simple keyword matching
            line_lower = line.lower()
            score = 0
            
            # Check Title (kafin colon :)
            parts = line_lower.split(':')
            if len(parts) > 1 and clean_q in parts[0]:
                return f"Na samu wannan:\n{line}"

            # Check content count
            words_in_query = clean_q.split()
            matches = sum(1 for w in words_in_query if w in line_lower)
            
            if matches > max_score:
                max_score = matches
                best_match = line
        
        if max_score > 0:
            return f"Bisa bincikena:\n{best_match}"
        
        return None

    def learn(self, text):
        # Kara ilimi a brain.txt
        with open(BRAIN_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{text}")
        self.brain_lines.append(text)
        return "Na ajiye wannan a kwakwalwata (Brain.txt)."

    def process_input(self, user_input):
        # 1. Koyo (Teaching Mode)
        if "koya min" in user_input.lower():
            return "Rubuta bayanin da kake so in haddace, zan sa shi a Brain.txt."
        
        # Idan jumlar tana da tsawo kuma tana kama da bayani, ajiye ta (Auto-Learn optional)
        # Amma a nan, zamu barshi sai an sa command don kada ya cika da surutu.

        # 2. Check Chat Logic (Gaisuwa, Labari, Math)
        chat_reply = check_chat_logic(user_input)
        if chat_reply:
            return chat_reply

        # 3. Search Brain
        search_reply = self.search_brain(user_input)
        if search_reply:
            return search_reply

        # 4. Fallback
        return "Gaskiya ban samu wannan a 'Brain.txt' ba. \nZaka iya koya min ta hanyar rubuta bayanin a 'Brain.txt' ko nan gaba."

# Init
bot = FHA_GPT_V32()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get("message", "")
    return jsonify({"reply": bot.process_input(msg)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
