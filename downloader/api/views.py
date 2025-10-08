from django.shortcuts import render
from django.http import JsonResponse
import yt_dlp
import os

def download_video(request):
    url = request.GET.get('url')
    formato = request.GET.get('format', 'mp3')

    if not url:
        return JsonResponse({'error': 'No se proporcionó una URL'}, status=400)

    try:
        # Carpeta donde se guardaran los archivos descargados
        output_path = os.path.join(os.getcwd(), 'downloads')

        # Creamos carpeta si no existe
        os.makedirs(output_path, exist_ok=True)

        # Configuración de youtube-dlp
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            }
        
        # Si el formato es mp3, configuramos la extracción de audio
        if formato == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif formato == 'mp4':
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })

            # Descargamos el video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return JsonResponse({'success': True, 'path': output_path})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Create your views here.
