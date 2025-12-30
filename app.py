import os
import requests
import mimetypes
from flask import Flask, render_template, request, jsonify, send_from_directory, redirect

app = Flask(__name__, template_folder='.')

# 配置
DOWNLOAD_DIR = '/music'
API_BASE = 'https://music-api.gdstudio.xyz/api.php'

# 确保下载目录存在
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cover')
def cover():
    source = request.args.get('source')
    pic_id = request.args.get('id')
    
    if not source or not pic_id:
        # 返回一个空的 1x1 像素图片或者404
        return "", 404
        
    try:
        resp = requests.get(API_BASE, params={
            'types': 'pic',
            'source': source,
            'id': pic_id,
            'size': 300
        })
        data = resp.json()
        if data and 'url' in data and data['url']:
             return redirect(data['url'])
        else:
             return "", 404
    except:
        return "", 404

@app.route('/api/search')
def search():
    # 获取参数，默认源为网易云
    source = request.args.get('source', 'netease')
    keyword = request.args.get('name', '')
    page = request.args.get('pages', 1)
    count = request.args.get('count', 20)
    
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    try:
        # 调用外部 API 搜索
        resp = requests.get(API_BASE, params={
            'types': 'search',
            'source': source,
            'name': keyword,
            'count': count,
            'pages': page
        })
        resp.raise_for_status()
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download_lyric', methods=['POST'])
def download_lyric_endpoint():
    data = request.json
    source = data.get('source')
    track_id = data.get('id')
    name = data.get('name')
    artist = data.get('artist', 'Unknown')
    
    if not all([source, track_id, name]):
        return jsonify({'error': 'Missing required fields'}), 400

    # 清理文件名
    safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c in ' .-_()']).strip()
    safe_artist = "".join([c for c in artist if c.isalpha() or c.isdigit() or c in ' .-_()']).strip()
    base_filename = f"{safe_artist} - {safe_name}"
    
    try:
        lyric_resp = requests.get(API_BASE, params={
            'types': 'lyric',
            'source': source,
            'id': track_id
        })
        lyric_resp.raise_for_status()
        lyric_data = lyric_resp.json()
        
        lrc_content = lyric_data.get('lyric', '')
        if not lrc_content:
             return jsonify({'error': '未找到歌词'}), 404

        lrc_path = os.path.join(DOWNLOAD_DIR, f"{base_filename}.lrc")
        with open(lrc_path, 'w', encoding='utf-8') as f:
            f.write(lrc_content)
        
        return jsonify({'status': 'success', 'filename': f"{base_filename}.lrc", 'path': lrc_path})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    source = data.get('source')
    track_id = data.get('id')
    name = data.get('name')
    artist = data.get('artist', 'Unknown')
    bitrate = data.get('br', 999) 
    download_lyric = data.get('lyric', False)
    
    # 允许仅提供 name 进行自动搜索下载
    if not source or not (track_id or name):
        return jsonify({'error': 'Missing required fields (source and either id or name)'}), 400

    results = {}

    # 0. 如果没有 ID，先搜索 (I'm feeling lucky 模式)
    if not track_id and name:
        try:
            search_resp = requests.get(API_BASE, params={
                'types': 'search',
                'source': source,
                'name': name,
                'count': 1,
                'pages': 1
            })
            search_data = search_resp.json()
            if search_data and isinstance(search_data, list) and len(search_data) > 0:
                best_match = search_data[0]
                track_id = best_match['id']
                # 如果没提供 artist，顺便更新一下让文件名更准确
                if artist == 'Unknown': 
                    artist = " ".join(best_match.get('artist', []))
                # 更新 name 以匹配精确歌名 (可选)
                name = best_match['name']
            else:
                return jsonify({'error': '未找到相关歌曲，请尝试提供准确 ID'}), 404
        except Exception as e:
            return jsonify({'error': f'自动搜索失败: {str(e)}'}), 500

    # 清理文件名
    safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c in ' .-_()']).strip()
    safe_artist = "".join([c for c in artist if c.isalpha() or c.isdigit() or c in ' .-_()']).strip()
    base_filename = f"{safe_artist} - {safe_name}"

    # 1. 下载歌词 (如果请求)
    if download_lyric:
        try:
            requests.post(f'http://127.0.0.1:{os.environ.get("PORT", 8000)}/api/download_lyric', json={
                'source': source, 'id': track_id, 'name': name, 'artist': artist
            })
            results['lyric'] = 'downloaded'
        except:
             # Ignore internal request fail, it's optional
             pass

    # 2. 获取音乐下载链接 (自动降级逻辑)
    available_fqs = [2000, 999, 740, 320, 192, 128]
    try:
        requested_br = int(bitrate)
    except:
        requested_br = 999
        
    download_url = None
    final_br = 0

    start_index = 0
    if requested_br in available_fqs:
        start_index = available_fqs.index(requested_br)
    
    for br_val in available_fqs[start_index:]:
        try:
            url_resp = requests.get(API_BASE, params={
                'types': 'url',
                'source': source,
                'id': track_id,
                'br': br_val
            })
            if url_resp.status_code != 200:
                continue
                
            url_data = url_resp.json()
            if url_data and 'url' in url_data and url_data['url']:
                download_url = url_data['url']
                final_br = br_val
                break 
        except Exception as e:
            continue
            
    if not download_url:
         return jsonify({'error': '无法获取下载链接 (可能版权限制或需要VIP)'}), 404
             
    # 3. 下载音乐文件
    try:
        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            
            # 尝试检测文件类型
            content_type = r.headers.get('content-type')
            ext = mimetypes.guess_extension(content_type)
            if not ext:
                # Fallback based on URL or default
                if '.flac' in download_url: ext = '.flac'
                elif '.m4a' in download_url: ext = '.m4a'
                elif '.ogg' in download_url: ext = '.ogg'
                else: ext = '.mp3'
            
            # Reduce weird extensions like .mpga to .mp3
            if ext == '.mpga': ext = '.mp3'
            
            filename = f"{base_filename}{ext}" 
            filepath = os.path.join(DOWNLOAD_DIR, filename)

            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
    
    except Exception as e:
        return jsonify({'error': f"下载文件失败: {str(e)}"}), 500

    results['status'] = 'success'
    results['filename'] = filename
    results['path'] = filepath
    results['bitrate'] = final_br
    return jsonify(results)

if __name__ == '__main__':
    # 仅在开发环境运行，生产环境使用 gunicorn
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
