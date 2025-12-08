with open('beatsync_ultimate.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Comment out both occurrences
pattern = r'(self\.video_empty = QLabel.*?self\.video_layout\.addWidget\(self\.video_empty\))'
content = re.sub(pattern, r'# \1  # Removed - not needed', content, flags=re.DOTALL)

with open('beatsync_ultimate.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ Removed empty state text - cleaner UI')
