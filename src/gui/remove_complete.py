with open('beatsync_ultimate.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Find all video_empty references and replace with just pass or None checks
replacements_made = []

# 1. Remove initial creation (keep container and layout, just remove the label)
pattern1 = r'self\.video_empty = QLabel\("No video clips imported\\nMax 15 seconds each"\)\s+self\.video_empty\.setAlignment\(Qt\.AlignmentFlag\.AlignCenter\)\s+self\.video_empty\.setStyleSheet\([^)]+\)\s+self\.video_layout\.addWidget\(self\.video_empty\)'
if re.search(pattern1, content):
    content = re.sub(pattern1, '# Empty state label removed for cleaner UI', content)
    replacements_made.append('Initial creation')

# 2. Remove the delete check in import dialog
pattern2 = r'if self\.video_empty:\s+self\.video_empty\.deleteLater\(\)\s+self\.video_empty = None'
content = re.sub(pattern2, '# video_empty removed', content)
replacements_made.append('Delete checks')

# 3. Remove re-creation in update method
pattern3 = r'self\.video_empty = QLabel\("No video clips imported\\nMax 15 seconds each"\)\s+self\.video_empty\.setAlignment\(Qt\.AlignmentFlag\.AlignCenter\)\s+self\.video_empty\.setStyleSheet\([^)]+\)\s+self\.video_layout\.addWidget\(self\.video_empty\)'
content = re.sub(pattern3, '# Empty state removed', content)

with open('beatsync_ultimate.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'✅ Completely removed video_empty: {len(replacements_made)} sections')
