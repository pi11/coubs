# -*- coding: utf-8 -*-
import socket
import os
from urllib.parse import urlparse
from datetime import datetime
import traceback

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
import logging

import sys
import os
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from main.models import Compilation


class Command(BaseCommand):
    help = """Bot poster"""

    def handle(self, *args, **options):

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO,
        )

        logger = logging.getLogger(__name__)

        def help(bot, update):
            update.message.reply_text("Yellow")

        def error(bot, update, error):
            """Log Errors caused by Updates."""
            logger.warning('Update "%s" caused error "%s"', update, error)

        def post_group(context):
            """Post coub to group"""
            try:
                comp = Compilation.objects.filter(is_tg_uploaded=False)[0]
            except IndexError:
                print("No more to post for now...")
            else:
                print(f"Posting to group: {coub.tmp_file}")
                if not coub.tmp_file:
                    print("No file found, skiping")
                else:
                    message = context.bot.send_video(
                        timeout=30,
                        chat_id=settings.CHAT_NAME,
                        video=open(comp.file, "rb"),
                    )
                comp.is_tg_uploaded = True
                comp.save()

        updater = Updater(settings.TG_TOKEN)
        jq = updater.job_queue
        d_job = jq.run_repeating(post_group, interval=settings.POST_INTERVAL, first=3)

        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", help))
        dp.add_handler(CommandHandler("help", help))
        # dp.add_error_handler(error)
        updater.start_polling()
        updater.idle()
