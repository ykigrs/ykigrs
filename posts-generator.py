import os
import json
import re
from datetime import datetime

def extract_front_matter(content):
    front_matter = {}
    match = re.match(r'^---\s+(.*?)\s+---', content, re.DOTALL)
    if match:
        front_matter_text = match.group(1)
        for line in front_matter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                front_matter[key.strip()] = value.strip()
    return front_matter

def get_posts_data():
    posts = []
    posts_dir = 'posts'
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            front_matter = extract_front_matter(content)
            
            post = {
                'title': front_matter.get('title', 'Untitled'),
                'date': front_matter.get('date', datetime.now().strftime('%Y-%m-%d')),
                'description': front_matter.get('description', ''),
                'filename': filename
            }
            posts.append(post)
    
    return sorted(posts, key=lambda x: x['date'], reverse=True)

if __name__ == '__main__':
    posts_data = get_posts_data()
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=2)

print("posts.json has been generated successfully.")