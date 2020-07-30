#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2020 Stɑrry Shivɑm // This file is part of AcuteBot
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import requests as r

from telegram.ext.dispatcher import run_async
from telegram.ext import PrefixHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply

from acutebot import dp, cmd, LOG, TMDBAPI, typing
from acutebot.helpers import strings as st
from acutebot.helpers.getid import getid

NAME, TV, MOVIE = range(3)
base_url = "https://api.themoviedb.org/3"


@run_async
@typing
def review_entry(update, context):
    reply_keyboard = [["TV series", "Movies"]]

    update.effective_message.reply_text(
        st.TOSEARCHREVIEW,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, selective=True
        ),
    )

    return NAME


@run_async
@typing
def rname(update, context):
    msg = update.message
    name = msg.text
    if name == "TV series":
        msg.reply_text(st.TOSEARCHTV, reply_markup=ForceReply(selective=True))
        return TV
    if name == "Movies":
        msg.reply_text(st.TOSEARCHMOVIE, reply_markup=ForceReply(selective=True))
        return MOVIE
    msg.reply_text(st.INVALIDREVIEWNAME, reply_markup=ReplyKeyboardRemove())
    return -1


@run_async
@typing
def tvreview(update, context):
    msg = update.message
    r_id = getid(msg.text, category="TV")

    if r_id == "api_error":
        msg.reply_text(st.API_ERR)
        return -1

    if r_id == "not_found":
        msg.reply_text(st.NOT_FOUND)
        return -1

    try:
        res = r.get(
            f"{base_url}/tv/{r_id}/reviews?api_key={TMDBAPI}&language=en&page=1"
        ).json()

        text = reviewdata(res, msg.text)
        msg.reply_text(
            text, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True
        )

    except Exception as e:
        LOG.error(e)
    return -1


@run_async
@typing
def moviereview(update, context):
    msg = update.message
    r_id = getid(msg.text, category="MOVIE")

    if r_id == "api_error":
        msg.reply_text(st.API_ERR)
        return -1
    if r_id == "not_found":
        msg.reply_text(st.NOT_FOUND)
        return -1

    try:
        res = r.get(
            f"{base_url}/movie/{r_id}/reviews?api_key={TMDBAPI}&language=en&page=1"
        ).json()

        text = reviewdata(res, msg.text)
        msg.reply_text(
            text, reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True,
        )

    except Exception as e:
        LOG.error(e)
    return ConversationHandler.END


def reviewdata(res: dict, title: str):
    """build review text from dict"""

    # TODO: use single loop?
    results = res["results"]
    author = []
    url = []

    if len(results) > 0:
        for dic in results:
            author.append(dic["author"])
            url.append(dic["url"])
    else:
        return st.REVIEW_NOT_FOUND

    text = f"💬 Reviews for <b>{title}</b>\n\n"
    num = 0
    for a in author:
        text += f"<b>🎖 By {a}</b> :\n"
        for c in url:
            text += f"🏷 Link: {url[num]}\n\n"
            num += 1
            break

    return text


@run_async
@typing
def cancel(update, context):
    context.bot.sendMessage(update.effective_chat.id, (st.CANCEL))
    return ConversationHandler.END


REVIEW_HANDLER = ConversationHandler(
    entry_points=[PrefixHandler(cmd, "reviews", review_entry)],
    states={
        NAME: [MessageHandler(Filters.text & ~Filters.command, rname)],
        TV: [MessageHandler(Filters.text & ~Filters.command, tvreview)],
        MOVIE: [MessageHandler(Filters.text & ~Filters.command, moviereview)],
    },
    fallbacks=[PrefixHandler(cmd, "cancel", cancel)],
    conversation_timeout=120,
)

dp.add_handler(REVIEW_HANDLER)
