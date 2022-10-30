# -*- coding: utf-8 -*-
import sys
import requests
import os
from datetime import datetime

from pyquery import PyQuery as pq

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q

from main.models import Coub


class Command(BaseCommand):
    help = """Parse imgur"""

    def add_arguments(self, parser):
        # parser.add_argument('start_page', type=int, default=0)
        # parser.add_argument('end_page', type=int, default=1)
        pass

    def handle(self, *args, **options):
        def download_file(url, i):
            r = requests.get(url, stream=True)
            local_filename = f"{settings.BASE_DIR}/tmp/{i}.mp4"

            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            return local_filename

        base_urls = ["https://coub.com/api/v2/timeline/explore/random?order_by=&type=&scope=all&page=", "https://coub.com/api/v2/timeline/subscriptions/monthly?page="]
        for base_url in base_urls:
            for p in range(1, 30):
                data = requests.get(f"{base_url}{p}")
                for coub in data.json()["coubs"]:
                    i = coub["id"]
                    new_coub, is_new = Coub.objects.get_or_create(pk=i)
                    if is_new:
                        file_url = coub["file_versions"]["share"]["default"]
                        print(f"Downloading {file_url}")
                        result_file = download_file(file_url, i)
                        if result_file:
                            new_coub.is_downloaded = True
                            new_coub.tmp_file = result_file
                            new_coub.save()
