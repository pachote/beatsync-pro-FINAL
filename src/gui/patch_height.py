with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# Increase the fixed height from 120 to 80 per track (need ~80px for one track card)
old = "audio_wrapper.setFixedHeight(120)"
new = "audio_wrapper.setFixedHeight(85)  # Single track height - compact but readable"

if old in content:
    content = content.replace(old, new)
    print("[+] Reduced wrapper height to 85px for single track!")
else:
    print("[!] Could not find height setting")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)
