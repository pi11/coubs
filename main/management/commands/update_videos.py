# -*- coding: utf-8 -*-
import sys
import requests
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q

from main.models import Coub, Compilation
from helpers.misc import get_video_info


class Command(BaseCommand):
    help = """Parse imgur"""

    def add_arguments(self, parser):
        # parser.add_argument('start_page', type=int, default=0)
        # parser.add_argument('end_page', type=int, default=1)
        pass

    def handle(self, *args, **options):
        sizes = {}
        for c in Coub.objects.filter():
            size = f"{c.w}x{c.h}"
            if size not in sizes:
                sizes[size] = 1
            else:
                sizes[size] += 1
        print(sizes)

        # max_s = (max(sizes, key=sizes.get))
        # print(max_s)
        #for s, v in sizes.items():
        #    if s == max_s:
        #        print(s)
        # for c in Coub.objects.filter(duration=0):
        #     try:
        #         info = get_video_info(c.tmp_file)
        #     except IndexError: # file missing
        #         c.delete()
        #         continue
        #     c.w = info["size"][0]
        #     c.h = info["size"][1]
        #     c.duration = info["duration"]
        #     c.is_compilation_used = False
        #     c.save()
        #     print(c.w, c.h)
