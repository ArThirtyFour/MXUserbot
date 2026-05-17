#			__  ____  ___   _               _           _   
#			|  \/  \ \/ / | | |___  ___ _ __| |__   ___ | |_ 
#			| |\/| |\  /| | | / __|/ _ \ '__| '_ \ / _ \| __|
#			| |  | |/  \| |_| \__ \  __/ |  | |_) | (_) | |_ 
#			|_|  |_/_/\_\\___/|___/\___|_|  |_.__/ \___/ \__| 
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html


class Meta:
    name = "PingPong"
    description = "Simple ping-pong + dm checker"
    version = "1.2.0"
    tags = ["system"]


import time

from pydantic import BaseModel

from mxc import utils
from .. import loader
from ..core.langs import Locales


class Strings(BaseModel):
    name: str
    pinging: str
    pong: str


locales = Locales(
    ru=Strings(
        name="PingPong",
        pinging="<b>🏓 | Пингую...</b>",
        pong="<b>🏓 | Понг!</b><br><b>└ </b> <code>{} ms</code>",
    ),
    en=Strings(
        name="PingPong",
        pinging="<b>🏓 | Pinging...</b>",
        pong="<b>🏓 | Pong!</b><br><b>└ </b> <code>{} ms</code>",
    ),
    ua=Strings(
        name="PingPong",
        pinging="<b>🏓 | Пінгую...</b>",
        pong="<b>🏓 | Понг!</b><br><b>└ </b> <code>{} ms</code>",
    ),
    fr=Strings(
        name="PingPong",
        pinging="<b>🏓 | Ping en cours...</b>",
        pong="<b>🏓 | Pong!</b><br><b>└ </b> <code>{} ms</code>",
    ),
    de=Strings(
        name="PingPong",
        pinging="<b>🏓 | Pinge...</b>",
        pong="<b>🏓 | Pong!</b><br><b>└ </b> <code>{} ms</code>",
    ),
    jp=Strings(
        name="PingPong",
        pinging="<b>🏓 | ピング中...</b>",
        pong="<b>🏓 | ポン！</b><br><b>└ </b> <code>{} ms</code>",
    ),
)


@loader.tds
class PingPongModule(loader.Module):
    strings = locales

    @loader.command(security=loader.OWNER)
    async def ping(self, mx, event):
        """Check bot latency"""
        start = time.perf_counter()

        status_id = await utils.answer(mx, self.strings.get("pinging"))

        end = time.perf_counter()
        duration = round((end - start) * 1000, 2)

        await utils.answer(
            mx,
            self.strings.get("pong").format(duration),
            edit_id=status_id
        )
