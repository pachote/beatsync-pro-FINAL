with open("beatsync_ultimate.py", "r", encoding="utf-8") as f:
    content = f.read()

# Shorten filename truncation from 35 to 25 characters
old_truncate = """        display_name = self.filename

        if len(display_name) > 35:

            display_name = display_name[:32] + "...\""""

new_truncate = """        # Get just the filename, not full path
        import os
        display_name = os.path.basename(self.filename)
        if len(display_name) > 25:
            display_name = display_name[:22] + "...\""""

if old_truncate in content:
    content = content.replace(old_truncate, new_truncate)
    print("[+] Fixed filename truncation - now uses basename and shorter limit!")
else:
    print("[!] Could not find truncation pattern")

with open("beatsync_ultimate.py", "w", encoding="utf-8") as f:
    f.write(content)
