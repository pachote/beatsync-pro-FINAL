with open('beatsync_ultimate.py', 'rb') as f:
    content = f.read()

# Find and replace the folder button - remove emoji, keep text only
# Search for the broken emoji pattern
old_button = b'QPushButton("Open Videos Folder")'
# This might have the broken emoji in front, let's check both

# First try with any emoji pattern before "Open Videos Folder"
import re
content_str = content.decode('utf-8', errors='replace')

# Replace any pattern like QPushButton("[emoji] Open Videos Folder") 
# with just QPushButton("Open Videos Folder")
if 'QPushButton(' in content_str and 'Open Videos Folder' in content_str:
    # Use regex to remove emoji before "Open Videos Folder"
    import re
    new_content = re.sub(r'QPushButton\(".*?\s*Open Videos Folder"\)', 
                         'QPushButton("Open Videos Folder")', 
                         content_str)
    
    # Write back
    with open('beatsync_ultimate.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('✅ Removed folder emoji - now just text!')
else:
    print('⚠️ Pattern not found')
