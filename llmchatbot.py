#!/usr/bin/env python3
import os, sys, time, json, urllib.request

CALL = os.environ.get("STATION_CALL", "YOURCALL-8")
LAST_ID = 0

SYSTEM_PROMPT = (
  "You are an amateur radio text bot operating under US Part 97. "
  "Keep replies <400 chars, plain ASCII, no URLs, no business, no codes, no encryption. "
  "Be friendly, factual, and brief. ID is sent automatically."
)

def ask_ollama(user):
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps({
          "model":"llama3.1:8b-instruct-q4_K_M",
          "prompt": f"{SYSTEM_PROMPT}\nCaller: {user}\nReply:",
          "stream": False
        }).encode("utf-8"),
        headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        out = json.load(r)
    return out.get("response","").replace("\n"," ")[:380]

def maybe_id():
    global LAST_ID
    if time.time() - LAST_ID > 540:  # ~9 min
        sys.stdout.write(f"\r\nde {CALL}\r\n")
        sys.stdout.flush()
        LAST_ID = time.time()

sys.stdout.write(f"AI chat bot de {CALL}. Type your msg; end with /EX.\r\n")
sys.stdout.flush()
LAST_ID = time.time()
buf=[]
for line in sys.stdin:
    line=line.strip()
    if not line: 
        continue
    if line.upper() == "/EX":
        sys.stdout.write(f"73 de {CALL}\r\n")
        sys.stdout.flush()
        break
    # answer
    reply = ask_ollama(line)
    sys.stdout.write(reply + "\r\n")
    sys.stdout.flush()
    maybe_id()
# ensure end-of-contact ID
sys.stdout.write(f"de {CALL}\r\n")
sys.stdout.flush()
