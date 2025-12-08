with open('beatsync_ultimate.py', 'rb') as f:
    content = f.read()
    
# Find the setText line
search = b'play_btn.setText'
pos = content.find(search)
if pos != -1:
    # Show 50 bytes after "setText("
    start = pos + len(search) + 2
    chunk = content[start:start+20]
    print('Hex bytes:', chunk.hex())
    print('As string:', chunk)
    print('')
    print('Looking for this pattern to replace...')
