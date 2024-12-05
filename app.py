import yt_dlp
import os
from googleapiclient.discovery import build
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
DOWNLOAD_FOLDER = "./downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

API_KEY = 'AIzaSyC0etCTzfywabIaHI9w-kRuIfy-uD7psKE'  # Ganti dengan API key Anda
youtube = build('youtube', 'v3', developerKey=API_KEY)

@app.route('/ytmp4', methods=['GET'])
def download_mp4():
    try:
        video_url = request.args.get('url')
        if not video_url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Konfigurasi yt-dlp untuk YouTube
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'format': 'best[ext=mp4]',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info_dict)

        # Kirim file dan hapus setelahnya
        response = send_file(file_path, as_attachment=True)
        os.remove(file_path)  # Menghapus file setelah dikirim
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ytmp3', methods=['GET'])
def download_mp3():
    try:
        video_url = request.args.get('url')
        if not video_url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Konfigurasi yt-dlp untuk YouTube
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.mp4', '.mp3')

        # Kirim file dan hapus setelahnya
        response = send_file(file_path, as_attachment=True)
        os.remove(file_path)  # Menghapus file setelah dikirim
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ttmp4', methods=['GET'])
def download_tiktok_mp4():
    try:
        video_url = request.args.get('url')
        if not video_url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Konfigurasi yt-dlp untuk TikTok
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'format': 'best[ext=mp4]',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info_dict)

        # Kirim file dan hapus setelahnya
        response = send_file(file_path, as_attachment=True)
        os.remove(file_path)  # Menghapus file setelah dikirim
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ttmp3', methods=['GET'])
def download_tiktok_mp3():
    try:
        video_url = request.args.get('url')
        if not video_url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Konfigurasi yt-dlp untuk TikTok
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.mp4', '.mp3')

        # Kirim file dan hapus setelahnya
        response = send_file(file_path, as_attachment=True)
        os.remove(file_path)  # Menghapus file setelah dikirim
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ytsearch', methods=['GET'])
def ytsearch():
    query = request.args.get('query')  # Mendapatkan query pencarian dari URL
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        # Mencari video menggunakan YouTube Data API v3
        search_request = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=5
        )
        search_response = search_request.execute()

        # Memproses hasil pencarian
        videos = []
        if 'items' in search_response:
            for item in search_response['items']:
                if item['id']['kind'] == 'youtube#video':  # Pastikan item adalah video
                    video_info = {
                        'title': item['snippet']['title'],
                        'link': f'https://www.youtube.com/watch?v={item["id"]["videoId"]}',
                        'thumbnail': item['snippet']['thumbnails']['default']['url'],
                        'published': item['snippet']['publishedAt'],
                        'channelTitle': item['snippet']['channelTitle']
                    }
                    videos.append(video_info)
        
        if not videos:
            return jsonify({'error': 'No videos found for this query'}), 404

        return jsonify({'videos': videos})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

