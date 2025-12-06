#!/usr/bin/env python3
# ai.py
# FHA GPT v33.0 - Pella Hosting Edition
# - An cire 'Labaran Dariya' na hard-code.
# - An kara karfin fahimta (Topic vs Content search).
# - An saita shi don Pella.app (Dynamic Port).

from flask import Flask, request, jsonify
from flask_cors import CORS
import re, os, datetime
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

BRAIN_FILE = "brain.txt"

# ==============================================================================
# 1. INITIAL BRAIN LOADER
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
AURE: Aure shine hadin gwiwa tsakanin namiji da mace bisa sunnar Manzon Allah.
"""

def load_brain():
    if not os.path.exists(BRAIN_FILE):
        with open(BRAIN_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_DATA)
    
    with open(BRAIN_FILE, "r", encoding="utf-8") as f:
        # Muna cire layukan banza
        return [line.strip() for line in f if line.strip()]

# ==============================================================================
# 2. LOGIC ENGINE (HIRA & LISSAFI KAWAI)
# Mun cire Labaran Dariya anan.
# ==============================================================================
def check_chat_logic(text):
    clean = text.lower()
    
    # 1. Gaisuwa (Greetings)
    if any(w in clean for w in ['sannu', 'barka', 'hy', 'yayau', 'barkanka', 'ina kwana', 'slm', 'hello', 'hi']):
        return "Sannu! Barka da zuwa FHA GPT. Nine mataimakinka. Me kake son sani?"
    
    if any(w in clean for w in ['lafiya', 'nagode', 'masha allah', 'na gode']):
        return "Madalla, Allah ya kara lafiya da natsuwa."

    # 2. Lokaci
    if 'lokaci' in clean or 'karfe' in clean:
        now = datetime.datetime.now()
        return f"Yanzu lokaci shine: {now.strftime('%I:%M %p')}."

    # 3. Lissafi (Simple Math)
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
# 3. SEARCH ENGINE (BINCIKE MAI FAHIMTA)
# ==============================================================================
class FHA_GPT_V33:
    def __init__(self):
        self.brain_lines = load_brain()

    def search_brain(self, query):
        # Tsaftace tambaya
        clean_q = query.lower().replace("bani", "").replace("menene", "").replace("labarin", "").replace("ma'anar", "").strip()
        
        best_match = None
        
        # 1. TOPIC MATCH (Bincike na Musamman)
        # Muna duba abin da ke gaban ':', misali: "AURE:"
        for line in self.brain_lines:
            if ":" in line:
                parts = line.split(":", 1) # Raba Topic da Bayani
                topic = parts[0].strip().lower()
                content = parts[1].strip()
                
                # Idan topic din yayi daidai da tambayar (Direct Match)
                if clean_q == topic:
                    return f"**{topic.upper()}:**\n{content}"
                
                # Idan topic din yana cikin tambayar
                if topic in clean_q:
                    return f"Na gane kana nufin {topic.upper()}:\n{content}"

        # 2. CONTENT SEARCH (Binciken Ciki)
        # Idan ba a samu Topic ba, duba cikin bayanan
        matches = []
        for line in self.brain_lines:
            # Lissafa kalmomin da suka zo daya
            matches_count = sum(1 for w in clean_q.split() if w in line.lower())
            if matches_count > 0:
                matches.append((matches_count, line))
        
        if matches:
            # Dauki wanda yafi yawan kalmomi (Highest Score)
            matches.sort(key=lambda x: x[0], reverse=True)
            best_line = matches[0][1]
            return f"Bisa bincikena a Brain.txt:\n{best_line}"
        
        return None

    def learn(self, text):
        with open(BRAIN_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{text}")
        self.brain_lines.append(text)
        return "Na ajiye wannan a kwakwalwata."

    def process_input(self, user_input):
        # 1. Koyo (Teaching Mode)
        if "koya min" in user_input.lower():
            return "Don koya min, rubuta bayanin a format din nan: 'TOPIC: Bayani'. Misali: 'KANO: Babban birni ne.'"
        
        # 2. Check Chat Logic
        chat_reply = check_chat_logic(user_input)
        if chat_reply:
            return chat_reply

        # 3. Search Brain
        search_reply = self.search_brain(user_input)
        if search_reply:
            return search_reply

        # 4. Fallback
        return "Gaskiya ban samu wannan a 'Brain.txt' ba. \nAmma zan iya koyo idan ka saka shi."

# Init Bot
bot = FHA_GPT_V33()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get("message", "")
    return jsonify({"reply": bot.process_input(msg)})

# Pella/Render/Heroku Port Configuration
if __name__ == '__main__':
    # Wannan yana daukar Port din da Pella ta bayar ta atomatik
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)