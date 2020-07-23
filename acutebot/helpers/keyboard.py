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



from telegram import InlineKeyboardButton

def keyboard(ytkey, homepage, title=None, imdbid=None):
    """Attach buttons dynamically from data"""

    keyblist = [[]]
    if len(ytkey["results"]) > 0:
        ytkey = ytkey["results"][0]["key"]
        yt_url = f"https://www.youtube.com/watch?v={ytkey}"
        keyblist[0].append(InlineKeyboardButton(text="📹 Trailer", url=yt_url))

    if homepage != "" and homepage != None:
        keyblist.append([InlineKeyboardButton(text="📃 Homepage", url=homepage)])

    if imdbid and imdbid is not None:
        keyblist[0].append(
            InlineKeyboardButton(text="🎞️ IMDb", url=f"https://m.imdb.com/title/{imdbid}")
        )

    if title:
        keyblist.append([InlineKeyboardButton(text="Save to watchlist 🔖", callback_data=f"fav_{title}")])

    return keyblist

