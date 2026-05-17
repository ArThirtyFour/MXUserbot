#			__  ____  ___   _               _           _   
#			|  \/  \ \/ / | | |___  ___ _ __| |__   ___ | |_ 
#			| |\/| |\  /| | | / __|/ _ \ '__| '_ \ / _ \| __|
#			| |  | |/  \| |_| \__ \  __/ |  | |_) | (_) | |_ 
#			|_|  |_/_/\_\\___/|___/\___|_|  |_.__/ \___/ \__| 
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html


class Meta:
    name = "PrefixModule"
    description = "Управление префиксом команд юзербота."
    version = "1.1.0"
    tags = ["settings"]


from pydantic import BaseModel

from mautrix.types import MessageEvent

from mxc.exceptions import UsageError
from mxc import utils
from .. import loader
from ..core import utils as cutils
from ..core.langs import Locales


class Strings(BaseModel):
    error_no_args: str
    error_too_long: str
    error_set_prefix: str
    success_set_prefix: str


locales = Locales(
    ru=Strings(
        error_no_args="❌ | <b>Префикс не указан.</b><br>Пример: <code>.set_prefix !</code>",
        error_too_long="❌ | <b>Префикс должен быть <u>один</u></b> символ.",
        error_set_prefix="❌ | <b>Символ <code>{new_prefix}</code> запрещён.</b><br>"
                         "Доступно: <code>{allowed_symbols}</code>",
        success_set_prefix="✅ | <b>Префикс изменён на</b>: <code>{new_prefix}</code>",
    ),
    en=Strings(
        error_no_args="❌ | <b>No prefix specified.</b><br>Example: <code>.set_prefix !</code>",
        error_too_long="❌ | <b>The prefix must be exactly <u>one</u></b> character long.",
        error_set_prefix="❌ | <b>The character <code>{new_prefix}</code> is not allowed.</b><br>"
                         "Allowed: <code>{allowed_symbols}</code>",
        success_set_prefix="✅ | <b>Prefix changed to</b>: <code>{new_prefix}</code>",
    ),
    ua=Strings(
        error_no_args="❌ | <b>Префікс не вказано.</b><br>Приклад: <code>.set_prefix !</code>",
        error_too_long="❌ | <b>Префікс має бути <u>один</u></b> символ.",
        error_set_prefix="❌ | <b>Символ <code>{new_prefix}</code> заборонено.</b><br>"
                         "Доступно: <code>{allowed_symbols}</code>",
        success_set_prefix="✅ | <b>Префікс змінено на</b>: <code>{new_prefix}</code>",
    ),
    fr=Strings(
        error_no_args="❌ | <b>Aucun préfixe spécifié.</b><br>Exemple: <code>.set_prefix !</code>",
        error_too_long="❌ | <b>Le préfixe doit être exactement <u>un</u></b> seul caractère.",
        error_set_prefix="❌ | <b>Le caractère <code>{new_prefix}</code> n'est pas autorisé.</b><br>"
                         "Autorisé: <code>{allowed_symbols}</code>",
        success_set_prefix="✅ | <b>Préfixe changé en</b>: <code>{new_prefix}</code>",
    ),
    de=Strings(
        error_no_args="❌ | <b>Kein Präfix angegeben.</b><br>Beispiel: <code>.set_prefix !</code>",
        error_too_long="❌ | <b>Das Präfix muss genau <u>ein</u></b> Zeichen sein.",
        error_set_prefix="❌ | <b>Das Zeichen <code>{new_prefix}</code> ist nicht erlaubt.</b><br>"
                         "Erlaubt: <code>{allowed_symbols}</code>",
        success_set_prefix="✅ | <b>Präfix geändert zu</b>: <code>{new_prefix}</code>",
    ),
    jp=Strings(
        error_no_args="❌ | <b>プレフィックスが指定されていません。</b><br>例: <code>.set_prefix !</code>",
        error_too_long="❌ | <b>プレフィックスは<u>1</u>文字でなければなりません。</b>",
        error_set_prefix="❌ | <b>文字 <code>{new_prefix}</code> は許可されていません。</b><br>"
                         "使用可能: <code>{allowed_symbols}</code>",
        success_set_prefix="✅ | <b>プレフィックスを変更しました</b>: <code>{new_prefix}</code>",
    ),
)


@loader.tds
class PrefixModule(loader.Module):
    strings = locales

    config = {
        "allowed_symbols": loader.ConfigValue(default="!\"./\\,;:@#$%^&*-_+=?|~", description="list allowed symbols"),
    }

    @loader.command(security=loader.OWNER)
    async def set_prefix(self, mx, event: MessageEvent):
        """Установить новый префикс (только спец. символы)"""

        args = await cutils.get_args(mx=mx, event=event)
    
        if len(args) < 1:
            raise UsageError(self.strings.get("error_no_args"))

        new_prefix = args[0]

        if len(new_prefix) != 1:
            return await utils.answer(mx, self.strings.get("error_too_long"))

        allowed = self.config.get("allowed_symbols")

        if new_prefix not in allowed:
            return await utils.answer(mx, 
                self.strings.get("error_set_prefix").format(
                    new_prefix=new_prefix,
                    allowed_symbols=allowed
                )
            )

        query = [new_prefix]
        await self._db.set("core", "prefix", query)
        mx._prefixes = query

        await utils.answer(mx, 
            self.strings.get("success_set_prefix").format(new_prefix=new_prefix)
        )
