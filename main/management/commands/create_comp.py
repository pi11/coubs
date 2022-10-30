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
            for coub in Coub.objects.filter(
                is_compilation_used=False, is_downloaded=True
            )[:40]:
                f.write(f"file '{coub.tmp_file}'\n")
                coub.is_compilation_used = True
                coub.save()

        comp = Compilation()
        comp.save()
        command = f"ffmpeg -safe 0 -f concat -i {settings.BASE_DIR}/tmp/files.txt -c copy {settings.BASE_DIR}/media/comp-{comp.pk}.mp4"
        print(command)
        run_shell_command(command, "Error creating compilation")
        comp.file = f"{settings.BASE_DIR}/media/comp-{comp.pk}.mp4"
        comp.save()
