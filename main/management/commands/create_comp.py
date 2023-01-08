# -*- coding: utf-8 -*-
import sys
import requests
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models import Q

from main.models import Coub, Compilation
from helpers.misc import run_shell_command


class Command(BaseCommand):
    help = """Parse imgur"""

    def add_arguments(self, parser):
        # parser.add_argument('start_page', type=int, default=0)
        # parser.add_argument('end_page', type=int, default=1)
        pass

    def handle(self, *args, **options):
        with open(f"{settings.BASE_DIR}/tmp/files.txt", "w+") as f:
            bad_tags = ["anime", "game", "gameplay", "hentai", "kawaii"]
            # Mark bad videos

            for c in Coub.objects.filter(is_compilation_used=False, is_good=True):
                bad_coub = False
                for t in coub.tags.all():
                    for bt in bad_tags:
                        if bt in t.title:
                            print(f"Skip coub with 'bad' tag: {bt}")
                            bad_coub = True
                if bad_coub:
                    c.is_good = False
                    c.save()

            sizes = {}
            for c in Coub.objects.filter(is_compilation_used=False):
                size = f"{c.w}x{c.h}"
                if size not in sizes:
                    sizes[size] = 1
                else:
                    sizes[size] += 1
            max_s = (max(sizes, key=sizes.get)).split("x")

            query = Coub.objects.filter(
                is_compilation_used=False, is_downloaded=True, w=max_s[0], h=max_s[1]
            )
            if query.count() < 180:
                print("Not enough videos")
                sys.exit()

            max_duration = 30 * 60
            total_duration = 0
            for coub in query.order_by("?"):
                bad_coub = False
                if os.path.exists(coub.tmp_file):
                    for t in coub.tags.all():
                        for bt in bad_tags:
                            if bt in t.title:
                                print("Skip coub with 'bad' tag")
                                bad_coub = True
                    if not bad_coub:
                        total_duration += coub.duration
                        f.write(f"file '{coub.tmp_file}'\n")
                        coub.is_compilation_used = True
                        coub.save()
                        if total_duration >= max_duration:
                            break  # keep compilations short enough

        comp = Compilation()
        comp.save()
        command = f"ffmpeg -safe 0 -f concat -i {settings.BASE_DIR}/tmp/files.txt -c copy {settings.BASE_DIR}/media/comp-{comp.pk}.mp4"
        print(command)
        run_shell_command(command, "Error creating compilation")
        comp.file = f"{settings.BASE_DIR}/media/comp-{comp.pk}.mp4"
        comp.save()
