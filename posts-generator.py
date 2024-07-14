import os
import json
from markdown2 import Markdown
from jinja2 import Environment, FileSystemLoader

# Markdownパーサーの設定
markdowner = Markdown(extras=["metadata", "fenced-code-blocks"])

# Jinja2テンプレートエンジンの設定
env = Environment(loader=FileSystemLoader('.'))
post_template = env.get_template('post_template.html')

def convert_md_to_html(md_file_path, output_dir):
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_content = md_file.read()
    
    # MarkdownをHTMLに変換し、メタデータを取得
    html_content = markdowner.convert(md_content)
    metadata = html_content.metadata

    # テンプレートにデータを渡してHTMLを生成
    html_output = post_template.render(
        title=metadata.get('title', 'Untitled'),
        date=metadata.get('date', ''),
        content=html_content
    )

    # 出力ファイル名を決定（.mdを.htmlに置換）
    output_file_name = os.path.splitext(os.path.basename(md_file_path))[0] + '.html'
    output_file_path = os.path.join(output_dir, output_file_name)

    # HTMLファイルを保存
    with open(output_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_output)

    return output_file_name, metadata

def process_all_posts(posts_dir, output_dir):
    posts_data = []
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            md_file_path = os.path.join(posts_dir, filename)
            html_file_name, metadata = convert_md_to_html(md_file_path, output_dir)
            
            posts_data.append({
                'title': metadata.get('title', 'Untitled'),
                'date': metadata.get('date', ''),
                'description': metadata.get('description', ''),
                'filename': html_file_name
            })

    # posts.jsonを更新
    posts_data.sort(key=lambda x: x['date'], reverse=True)
    with open('posts.json', 'w', encoding='utf-8') as json_file:
        json.dump(posts_data, json_file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    posts_dir = 'posts'  # Markdownファイルのディレクトリ
    output_dir = 'posts'  # HTML出力先ディレクトリ（同じディレクトリに出力）
    process_all_posts(posts_dir, output_dir)
    print("All posts have been converted to HTML and posts.json has been updated.")