# -*- coding: utf-8 -*-
import sys
import requests
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q

from main.models import Coub
from helpers.misc import get_video_info, run_shell_command

class Command(BaseCommand):
    help = """Parse imgur"""

    def add_arguments(self, parser):
        # parser.add_argument('start_page', type=int, default=0)
        # parser.add_argument('end_page', type=int, default=1)
        pass

    def handle(self, *args, **options):
        def download_file(url, i, j):
            r = requests.get(url, stream=True)
            local_filename = f"{settings.BASE_DIR}/tmp/{i}-{j}.mp4"

            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            return local_filename

        base_urls = [
            "https://coub.com/api/v2/timeline/tag/funny?order_by=likes_count&type=&scope=all&page="
            "https://coub.com/api/v2/timeline/tag/fails?order_by=likes_count&type=&scope=all&page="
            "https://coub.com/api/v2/timeline/tag/fun?order_by=likes_count&type=&scope=all&page="
            "https://coub.com/api/v2/timeline/tag/lol?order_by=likes_count&type=&scope=all&page="
            "https://coub.com/api/v2/timeline/tag/epic?order_by=likes_count&type=&scope=all&page="
            "https://coub.com/api/v2/timeline/tag/comedy?order_by=likes_count&type=&scope=all&page="
            "https://coub.com/api/v2/timeline/subscriptions/monthly?page="
            
        ]
        for base_url in base_urls:
            for p in range(1, 150):
                data = requests.get(f"{base_url}{p}")
                for coub in data.json()["coubs"]:
                    i = coub["id"]
                    new_coub, is_new = Coub.objects.get_or_create(pk=i)
                    if is_new:
                        try:
                            mp4_url = coub["file_versions"]["html5"]["video"]["higher"]["url"]
                            mp3_url = coub["file_versions"]["html5"]["audio"]["med"]["url"]
                        except KeyError:
                            print("Looks like no audio, skipping")
                            continue
                        
                        if mp4_url:
                            print(f"Downloading {mp4_url}")
                            result_mp4_file = download_file(mp4_url, i, "mp4")
                            
                        print("Download mp3")
                        if mp3_url:
                            print(f"Downloading {mp3_url}")
                            result_mp3_file = download_file(mp3_url, i, "mp3")
                        if result_mp4_file and result_mp3_file:
                            result_file = f"{settings.BASE_DIR}/tmp/{i}-result.mp4"
                            print(f"Concat video + audio to {result_file}")
                            command = f"ffmpeg -i {result_mp4_file} -i {result_mp3_file} -c copy -map 0:v:0 -map 1:a:0 -shortest {result_file}"
                            
                            run_shell_command(command, "Error merging video+audio")
                            
                            if result_file:
                                new_coub.is_downloaded = True
                                new_coub.tmp_file = result_file
                                info = get_video_info(result_file)
                                new_coub.w = info["size"][0]
                                new_coub.h = info["size"][1]
                                new_coub.duration = info["duration"]
                                new_coub.save()
                            os.remove(result_mp4_file)
                            os.remove(result_mp3_file)
