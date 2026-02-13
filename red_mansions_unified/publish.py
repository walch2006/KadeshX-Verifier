import os
import json
import re
from datetime import datetime, timedelta

# Paths
BASE_DIR = r'c:\lingxi\github_serialization\red_mansions_unified'
TRACKER_PATH = os.path.join(BASE_DIR, 'PUBLISHING_TRACKER.json')
README_PATH = os.path.join(BASE_DIR, 'README.md')
SOURCE_FILE = r'c:\lingxi\HONG_LOU_MENG_SERIAL.md'
CHAPTERS_DIR = os.path.join(BASE_DIR, 'chapters')

def load_tracker():
    with open(TRACKER_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tracker(tracker):
    with open(TRACKER_PATH, 'w', encoding='utf-8') as f:
        json.dump(tracker, f, ensure_ascii=False, indent=4)

def get_chapter_from_source(chapter_num):
    if not os.path.exists(SOURCE_FILE):
        return None, None
    
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chinese numerals to match the header
    num_map = {
        81: '八十一', 82: '八十二', 83: '八十三', 84: '八十四', 85: '八十五',
        86: '八十六', 87: '八十七', 88: '八十八', 89: '八十九', 90: '九十',
        91: '九十一', 92: '九十二', 93: '九十三', 94: '九十四', 95: '九十五',
        96: '九十六', 97: '九十七', 98: '九十八', 99: '九十九', 100: '一百',
        101: '一百零一', 102: '一百零二', 103: '一百零三', 104: '一百零四', 105: '一百零五',
        106: '一百零六', 107: '一百零七', 108: '一百零八', 109: '一百零九', 110: '一百一十',
        111: '一百一十一', 112: '一百一十二', 113: '一百一十三', 114: '一百一十四', 115: '一百一十五',
        116: '一百一十六', 117: '一百一十七', 118: '一百一十八', 119: '一百一十九', 120: '一百二十'
    }
    
    # Target numeral
    target_num_zh = num_map.get(chapter_num)
    if not target_num_zh:
        return None, None
        
    # Regex to find specific chapter
    pattern = rf'### 第{target_num_zh}回 (.*?)\n(.*?)(?=\n### 第|$)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        return match.group(1).strip(), match.group(2).strip()
            
    return None, None

def update_readme(chapter_num, title, filename, publish_date, next_date):
    with open(README_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    table_found = False
    row_added = False
    
    for line in lines:
        if "| :--- | :--- | :--- | :--- |" in line:
            table_found = True
            new_lines.append(line)
            continue
        
        if table_found and not row_added and line.strip() == "":
            # End of table, add the new row
            new_row = f"| **第八十三回** | [{title}](./chapters/{filename}) | {publish_date} | ✅ 已发布 |\n"
            # Convert chapter_num to Chinese for the table
            zh_nums = {83: '八十三', 84: '八十四', 85: '八十五', 86: '八十六', 87: '八十七', 88: '八十八', 89: '八十九', 90: '九十'}
            zh_num = zh_nums.get(chapter_num, str(chapter_num))
            new_row = f"| **第{zh_num}回** | [{title}](./chapters/{filename}) | {publish_date} | ✅ 已发布 |\n"
            new_lines.append(new_row)
            row_added = True
            
        # Update next publish date
        if "下一回预计发布时间：" in line:
            line = re.sub(r'下一回预计发布时间：\d{4}-\d{2}-\d{2}', f'下一回预计发布时间：{next_date}', line)
            
        new_lines.append(line)
    
    with open(README_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def publish_next():
    tracker = load_tracker()
    next_chapter = tracker['last_published_chapter'] + 1
    
    title, content = get_chapter_from_source(next_chapter)
    
    if not title:
        print(f"Chapter {next_chapter} not found in source.")
        return False
    
    # Create chapter file
    filename = f"CH_{next_chapter:03d}.md"
    filepath = os.path.join(CHAPTERS_DIR, filename)
    
    header = f"# 第{next_chapter}回 {title}\n\n"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(header + content)
    
    publish_date = datetime.now().strftime('%Y-%m-%d')
    next_date = (datetime.now() + timedelta(days=tracker['publish_interval_days'])).strftime('%Y-%m-%d')
    
    # Update README
    update_readme(next_chapter, title, filename, publish_date, next_date)
    
    # Update Tracker
    tracker['last_published_chapter'] = next_chapter
    tracker['next_publish_date'] = next_date
    tracker['history'].append({
        "chapter": next_chapter,
        "title": title,
        "date": publish_date,
        "status": "published"
    })
    save_tracker(tracker)
    
    print(f"Successfully published Chapter {next_chapter}: {title}")
    return True

if __name__ == "__main__":
    publish_next()
