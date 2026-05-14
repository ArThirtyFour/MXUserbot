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
    version = "1.0.0"
    tags = ["settings"]


import re
import time
from typing import Any

from mautrix.types import MessageEvent
from pydantic import BaseModel, Field, model_validator

from mxc.exceptions import UsageError
from mxc import utils
from .. import loader


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
    
    strings = {
        "name": "Security",
        "not_found": "❌ Entity <code>{}</code> (as class or command) not found!",
        "mod_opened": "🔓 Access to the <b>entire module</b> <code>{}</code> granted for <code>{}</code>",
        "cmd_opened": "🔓 Access to the <b>command</b> <code>{}</code> granted for <code>{}</code>",
        "access_closed": "🔒 Access to <code>{}</code> revoked for <code>{}</code>",
        "invalid_action": "❌ Use <code>add</code>, <code>rm</code> or <code>list</code>",
        "sudo_usage": "<b>Usage:</b> <code>.sudo add/rm/list @user:id</code>",
        "sudo_list": "👤 <b>SUDO users:</b>\n{}",
        "sudo_empty": "No sudo users.",
        "sudo_added": "👤 User <code>{}</code> is now <b>SUDO</b>.",
        "sudo_removed": "👤 User <code>{}</code> is no longer <b>SUDO</b>.",
        "sudo_invalid_mxid": "❌ Invalid user. Use full Matrix ID like <code>@user:server</code>",
        "cmd_not_exist": "❌ Command <code>{}</code> does not exist!",
        "tsec_granted": "⏱ <code>{}</code> now has {} min. for command <code>{}</code>"
    }


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
        args = await utils.get_args(mx, event)
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
