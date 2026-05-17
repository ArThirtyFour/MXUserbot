#			__  ____  ___   _               _           _   
#			|  \/  \ \/ / | | |___  ___ _ __| |__   ___ | |_ 
#			| |\/| |\  /| | | / __|/ _ \ '__| '_ \ / _ \| __|
#			| |  | |/  \| |_| \__ \  __/ |  | |_) | (_) | |_ 
#			|_|  |_/_/\_\\___/|___/\___|_|  |_.__/ \___/ \__| 
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html


class Meta:
    name = "Security"
    description = "Ultimate access control with validation."
    version = "1.1.0"
    tags = ["settings"]


import re
import time
from typing import Any

from pydantic import BaseModel, Field, model_validator

from mautrix.types import MessageEvent

from mxc.exceptions import UsageError
from mxc import utils
from .. import loader
from ..core import utils as cutils
from ..core.langs import Locales


class Strings(BaseModel):
    name: str
    not_found: str
    mod_opened: str
    cmd_opened: str
    access_closed: str
    invalid_action: str
    sudo_usage: str
    sudo_list: str
    sudo_empty: str
    sudo_added: str
    sudo_removed: str
    sudo_invalid_mxid: str
    cmd_not_exist: str
    tsec_granted: str


locales = Locales(
    ru=Strings(
        name="Security",
        not_found="❌ Сущность <code>{}</code> (класс или команда) не найдена!",
        mod_opened="🔓 Доступ ко <b>всему модулю</b> <code>{}</code> предоставлен для <code>{}</code>",
        cmd_opened="🔓 Доступ к <b>команде</b> <code>{}</code> предоставлен для <code>{}</code>",
        access_closed="🔒 Доступ к <code>{}</code> отозван для <code>{}</code>",
        invalid_action="❌ Используйте <code>add</code>, <code>rm</code> или <code>list</code>",
        sudo_usage="<b>Использование:</b> <code>.sudo add/rm/list @user:id</code>",
        sudo_list="👤 <b>SUDO пользователи:</b>\n{}",
        sudo_empty="Нет SUDO пользователей.",
        sudo_added="👤 Пользователь <code>{}</code> теперь <b>SUDO</b>.",
        sudo_removed="👤 Пользователь <code>{}</code> больше не <b>SUDO</b>.",
        sudo_invalid_mxid="❌ Неверный пользователь. Используйте полный Matrix ID: <code>@user:server</code>",
        cmd_not_exist="❌ Команды <code>{}</code> не существует!",
        tsec_granted="⏱ <code>{}</code> получил(а) {} мин. на команду <code>{}</code>",
    ),
    en=Strings(
        name="Security",
        not_found="❌ Entity <code>{}</code> (as class or command) not found!",
        mod_opened="🔓 Access to the <b>entire module</b> <code>{}</code> granted for <code>{}</code>",
        cmd_opened="🔓 Access to the <b>command</b> <code>{}</code> granted for <code>{}</code>",
        access_closed="🔒 Access to <code>{}</code> revoked for <code>{}</code>",
        invalid_action="❌ Use <code>add</code>, <code>rm</code> or <code>list</code>",
        sudo_usage="<b>Usage:</b> <code>.sudo add/rm/list @user:id</code>",
        sudo_list="👤 <b>SUDO users:</b>\n{}",
        sudo_empty="No sudo users.",
        sudo_added="👤 User <code>{}</code> is now <b>SUDO</b>.",
        sudo_removed="👤 User <code>{}</code> is no longer <b>SUDO</b>.",
        sudo_invalid_mxid="❌ Invalid user. Use full Matrix ID: <code>@user:server</code>",
        cmd_not_exist="❌ Command <code>{}</code> does not exist!",
        tsec_granted="⏱ <code>{}</code> now has {} min. for command <code>{}</code>",
    ),
    ua=Strings(
        name="Security",
        not_found="❌ Сутність <code>{}</code> (клас або команда) не знайдена!",
        mod_opened="🔓 Доступ до <b>всього модуля</b> <code>{}</code> надано для <code>{}</code>",
        cmd_opened="🔓 Доступ до <b>команди</b> <code>{}</code> надано для <code>{}</code>",
        access_closed="🔒 Доступ до <code>{}</code> відкликано для <code>{}</code>",
        invalid_action="❌ Використовуйте <code>add</code>, <code>rm</code> або <code>list</code>",
        sudo_usage="<b>Використання:</b> <code>.sudo add/rm/list @user:id</code>",
        sudo_list="👤 <b>SUDO користувачі:</b>\n{}",
        sudo_empty="Немає SUDO користувачів.",
        sudo_added="👤 Користувач <code>{}</code> тепер <b>SUDO</b>.",
        sudo_removed="👤 Користувач <code>{}</code> більше не <b>SUDO</b>.",
        sudo_invalid_mxid="❌ Невірний користувач. Використовуйте повний Matrix ID: <code>@user:server</code>",
        cmd_not_exist="❌ Команди <code>{}</code> не існує!",
        tsec_granted="⏱ <code>{}</code> отримав(ла) {} хв. на команду <code>{}</code>",
    ),
    fr=Strings(
        name="Security",
        not_found="❌ Entité <code>{}</code> (classe ou commande) introuvable!",
        mod_opened="🔓 Accès au <b>module entier</b> <code>{}</code> accordé pour <code>{}</code>",
        cmd_opened="🔓 Accès à la <b>commande</b> <code>{}</code> accordé pour <code>{}</code>",
        access_closed="🔒 Accès à <code>{}</code> révoqué pour <code>{}</code>",
        invalid_action="❌ Utilisez <code>add</code>, <code>rm</code> ou <code>list</code>",
        sudo_usage="<b>Utilisation:</b> <code>.sudo add/rm/list @user:id</code>",
        sudo_list="👤 <b>Utilisateurs SUDO:</b>\n{}",
        sudo_empty="Aucun utilisateur SUDO.",
        sudo_added="👤 L'utilisateur <code>{}</code> est maintenant <b>SUDO</b>.",
        sudo_removed="👤 L'utilisateur <code>{}</code> n'est plus <b>SUDO</b>.",
        sudo_invalid_mxid="❌ Utilisateur invalide. Utilisez l'ID Matrix complet: <code>@user:server</code>",
        cmd_not_exist="❌ La commande <code>{}</code> n'existe pas!",
        tsec_granted="⏱ <code>{}</code> a maintenant {} min. pour la commande <code>{}</code>",
    ),
    de=Strings(
        name="Security",
        not_found="❌ Entität <code>{}</code> (Klasse oder Befehl) nicht gefunden!",
        mod_opened="🔓 Zugriff auf das <b>gesamte Modul</b> <code>{}</code> gewährt für <code>{}</code>",
        cmd_opened="🔓 Zugriff auf den <b>Befehl</b> <code>{}</code> gewährt für <code>{}</code>",
        access_closed="🔒 Zugriff auf <code>{}</code> entzogen für <code>{}</code>",
        invalid_action="❌ Verwenden Sie <code>add</code>, <code>rm</code> oder <code>list</code>",
        sudo_usage="<b>Verwendung:</b> <code>.sudo add/rm/list @user:id</code>",
        sudo_list="👤 <b>SUDO-Benutzer:</b>\n{}",
        sudo_empty="Keine SUDO-Benutzer.",
        sudo_added="👤 Benutzer <code>{}</code> ist jetzt <b>SUDO</b>.",
        sudo_removed="👤 Benutzer <code>{}</code> ist nicht mehr <b>SUDO</b>.",
        sudo_invalid_mxid="❌ Ungültiger Benutzer. Verwenden Sie die vollständige Matrix-ID: <code>@user:server</code>",
        cmd_not_exist="❌ Befehl <code>{}</code> existiert nicht!",
        tsec_granted="⏱ <code>{}</code> hat jetzt {} Min. für Befehl <code>{}</code>",
    ),
    jp=Strings(
        name="Security",
        not_found="❌ エンティティ <code>{}</code> (クラスまたはコマンド) が見つかりません!",
        mod_opened="🔓 <b>モジュール全体</b> <code>{}</code> へのアクセスを <code>{}</code> に許可しました",
        cmd_opened="🔓 <b>コマンド</b> <code>{}</code> へのアクセスを <code>{}</code> に許可しました",
        access_closed="🔒 <code>{}</code> へのアクセスを <code>{}</code> から取り消しました",
        invalid_action="❌ <code>add</code>、<code>rm</code>、または <code>list</code> を使用してください",
        sudo_usage="<b>使い方:</b> <code>.sudo add/rm/list @user:id</code>",
        sudo_list="👤 <b>SUDO ユーザー:</b>\n{}",
        sudo_empty="SUDO ユーザーがいません。",
        sudo_added="👤 ユーザー <code>{}</code> は <b>SUDO</b> になりました。",
        sudo_removed="👤 ユーザー <code>{}</code> は <b>SUDO</b> ではなくなりました。",
        sudo_invalid_mxid="❌ 無効なユーザーです。完全な Matrix ID を使用してください: <code>@user:server</code>",
        cmd_not_exist="❌ コマンド <code>{}</code> は存在しません!",
        tsec_granted="⏱ <code>{}</code> に {} 分間コマンド <code>{}</code> を許可しました",
    ),
)


def _extract_mxid(event, raw: str) -> str:
    fb = getattr(getattr(event, "content", None), "formatted_body", None)
    if fb:
        mxids = re.findall(r'href="[^"]*/(@[^"]+)"', fb)
        if mxids:
            return mxids[0]
    return raw


class ModAccessPayload(BaseModel):
    action: str
    target: str
    target_name: str

    @model_validator(mode="before")
    @classmethod
    def parse(cls, v: Any):
        if isinstance(v, str):
            parts = v.split()
            if len(parts) < 3:
                raise UsageError()
            return {
                "action": parts[0].lower(),
                "target": " ".join(parts[1:-1]),
                "target_name": parts[-1].lower(),
            }
        return v


class TSECPayload(BaseModel):
    target: str
    cmd: str
    mins: int

    @model_validator(mode="before")
    @classmethod
    def parse(cls, v: Any):
        if isinstance(v, str):
            parts = v.split()
            if len(parts) < 3:
                raise UsageError(
                    "<b>Usage:</b> <code>.tsec @user:id ping 10</code>"
                )
            try:
                int_mins = int(parts[-1])
            except ValueError:
                raise UsageError("❌ Minutes must be an integer!")
            return {
                "target": " ".join(parts[:-2]),
                "cmd": parts[-2].lower(),
                "mins": int_mins,
            }
        return v


@loader.tds
class SecurityModule(loader.Module):
    strings = locales

    @loader.command(security=loader.OWNER)
    async def modaccess(self, mx, event: MessageEvent, payload: ModAccessPayload):
        """<add/rm> <@user:id> <name> | Module (Class) or command access"""
        target = _extract_mxid(event, payload.target)
        
        is_mod = False
        is_cmd = False
        
        for mod in mx.active_modules.values():
            if mod.__class__.__name__.lower() == payload.target_name:
                is_mod = True
            
            if hasattr(mod, "commands") and payload.target_name in mod.commands:
                is_cmd = True

        if not is_mod and not is_cmd:
            return await utils.answer(
                mx, 
                self.strings.get("not_found").format(payload.target_name)
            )

        perms = mx.security.mod_perms
        if target not in perms: 
            perms[target] = []

        if payload.action == "add":
            if payload.target_name not in perms[target]: 
                perms[target].append(payload.target_name)
            
            if is_mod:
                msg = self.strings.get("mod_opened").format(payload.target_name, target)
            else:
                msg = self.strings.get("cmd_opened").format(payload.target_name, target)
                
        elif payload.action == "rm":
            if payload.target_name in perms[target]: 
                perms[target].remove(payload.target_name)
            msg = self.strings.get("access_closed").format(payload.target_name, target)
        else:
            return await utils.answer(mx, self.strings.get("invalid_action"))

        await mx._db.set("core", "mod_perms", perms)
        await utils.answer(mx, msg)


    @loader.command(security=loader.OWNER)
    async def sudo(self, mx, event):
        """<add/rm> <@user:id> | Manage SUDO users"""
        args = await cutils.get_args(mx, event)
        if len(args) < 2:
            raise UsageError(self.strings.get("sudo_usage"))
        
        action, target = args[0].lower(), _extract_mxid(event, " ".join(args[1:]))

        if action in ("add", "rm"):
            if not re.match(r"^@.+:.+$", target):
                return await utils.answer(mx, self.strings.get("sudo_invalid_mxid"))

        if action == "add":
            mx.security.sudos.add(target)
            msg = self.strings.get("sudo_added").format(target)
        elif action == "rm":
            mx.security.sudos.discard(target)
            msg = self.strings.get("sudo_removed").format(target)
        elif action == "list":
            if mx.security.sudos:
                msg = self.strings.get("sudo_list").format(
                    "\n".join(f"• {u}" for u in sorted(mx.security.sudos))
                )
            else:
                msg = self.strings.get("sudo_empty")
        else:
            return await utils.answer(mx, self.strings.get("invalid_action"))

        if action in ("add", "rm"):
            await mx._db.set("core", "sudos", list(mx.security.sudos))
        await utils.answer(mx, msg)


    @loader.command(security=loader.OWNER)
    async def tsec(self, mx, event: MessageEvent, payload: TSECPayload):
        """<@user:id> <cmd> <min> | Temporary permissions"""
        target = _extract_mxid(event, payload.target)

        cmd_exists = any(payload.cmd in m.commands for m in mx.active_modules.values())
        if not cmd_exists:
            return await utils.answer(
                mx, 
                self.strings.get("cmd_not_exist").format(payload.cmd)
            )

        exp = time.time() + (payload.mins * 60)

        mx.security.tsec_users.append({"target": target, "command": payload.cmd, "expires": exp, "room_id": event.room_id})
        
        await mx._db.set("core", "tsec_users", mx.security.tsec_users)

        await utils.answer(
            mx, 
            self.strings.get("tsec_granted").format(target, payload.mins, payload.cmd)
        )
