#			__  ____  ___   _               _           _   
#			|  \/  \ \/ / | | |___  ___ _ __| |__   ___ | |_ 
#			| |\/| |\  /| | | / __|/ _ \ '__| '_ \ / _ \| __|
#			| |  | |/  \| |_| \__ \  __/ |  | |_) | (_) | |_ 
#			|_|  |_/_/\_\\___/|___/\___|_|  |_.__/ \___/ \__| 
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html


class Meta:
    name = "LoaderModule"
    description = "Module Manager"
    version = "3.0.0"
    tags = ["system"]


import logging
from pathlib import Path
from typing import Any

from mautrix.types import MessageEvent
from pydantic import BaseModel, ConfigDict, Field, model_validator


from mxc.exceptions import UsageError
from mxc import utils
from mxc.types import EmojiButton
from ..core import utils as cutils
from mxc.utils.keyboard import EmojiKeyBoard
from .. import loader
from ..core.langs import Locales


class Strings(BaseModel):
    downloading: str
    fetching: str
    repo_not_found: str
    search_empty: str
    done: str
    error: str
    reloading: str
    reloaded: str
    unloaded: str
    search_header: str
    search_item: str
    confirm_unsafe: str
    confirm_cancelled: str
    dev_usage: str
    no_args: str
    repo_added: str
    repo_removed: str
    invalid_file: str


locales = Locales(
    ru=Strings(
        downloading="⏳ | <b>Скачивание...</b>",
        fetching="⏳ | <b>Обработка <code>{id}</code>...</b>",
        repo_not_found="❌ | <b>Модуль <code>{id}</code> не найден в репозиториях.</b>",
        search_empty="❌ | <b>Модули не найдены по запросу: <code>{query}</code>.</b>",
        done="✅ | <b>Модуль <code>{name}</code> успешно загружен!</b>",
        error="❌ | <b>Ошибка: <code>{err}</code></b>",
        reloading="⏳ | <b>Перезагрузка всех модулей...</b>",
        reloaded="♻️ | <b>Модули перезагружены. Всего: {count}</b>",
        unloaded="✅ | <b>Модуль <code>{name}</code> выгружен.</b>",
        search_header="<b>{icon} | <a href='{url}'>{type} Repository</a></b><br>⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯<br>",
        search_item="📦 | <b><a href='{raw_url}'>{name}</a></b> [v{version}]<br>┗ <code>.mdl {cmd_id}</code><br><br>",
        confirm_unsafe="⚠️ | <b>ПРЕДУПРЕЖДЕНИЕ БЕЗОПАСНОСТИ</b><br>Вы устанавливаете модуль из <b>{source}</b> — <b>НЕПРОВЕРЕННЫЙ</b> источник.<br>Этот модуль <b>НЕ</b> был проверен и может содержать вредоносный код.<br><br><b>Вы подтверждаете установку этого модуля?</b>",
        confirm_cancelled="❌ | <b>Установка отменена пользователем.</b>",
        dev_usage="❌ | <b>Прямые ссылки/файлы требуют префикса <code>dev</code>.</b>",
        no_args="❌ | <b>Укажите ID модуля, URL или ответьте на .py файл!</b>",
        repo_added="✅ | <b>Репозиторий добавлен: <code>{url}</code></b>",
        repo_removed="✅ | <b>Репозиторий удалён.</b>",
        invalid_file="❌ | <b>ТОЛЬКО .PY И .ZIP ФАЙЛЫ ПРИНИМАЮТСЯ!</b>",
    ),
    en=Strings(
        downloading="⏳ | <b>Downloading...</b>",
        fetching="⏳ | <b>Processing <code>{id}</code>...</b>",
        repo_not_found="❌ | <b>Module <code>{id}</code> not found in any repository.</b>",
        search_empty="❌ | <b>No modules found for query: <code>{query}</code>.</b>",
        done="✅ | <b>Module <code>{name}</code> loaded successfully!</b>",
        error="❌ | <b>Error: <code>{err}</code></b>",
        reloading="⏳ | <b>Reloading all modules...</b>",
        reloaded="♻️ | <b>Modules reloaded. Total: {count}</b>",
        unloaded="✅ | <b>Module <code>{name}</code> unloaded.</b>",
        search_header="<b>{icon} | <a href='{url}'>{type} Repository</a></b><br>⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯<br>",
        search_item="📦 | <b><a href='{raw_url}'>{name}</a></b> [v{version}]<br>┗ <code>.mdl {cmd_id}</code><br><br>",
        confirm_unsafe="⚠️ | <b>SECURITY WARNING</b><br>You are installing a module from <b>{source}</b> — an <b>UNVERIFIED</b> source.<br>This module has <b>NOT</b> been reviewed and may contain malicious code.<br><br><b>Do you confirm that you want to install this module?</b>",
        confirm_cancelled="❌ | <b>Installation cancelled by user.</b>",
        dev_usage="❌ | <b>Direct links/files require <code>dev</code> prefix.</b>",
        no_args="❌ | <b>Provide Module ID, URL or reply to a .py file!</b>",
        repo_added="✅ | <b>Repository added: <code>{url}</code></b>",
        repo_removed="✅ | <b>Repository removed.</b>",
        invalid_file="❌ | <b>ONLY .PY AND .ZIP FILES ACCEPTED!</b>",
    ),
    ua=Strings(
        downloading="⏳ | <b>Завантаження...</b>",
        fetching="⏳ | <b>Обробка <code>{id}</code>...</b>",
        repo_not_found="❌ | <b>Модуль <code>{id}</code> не знайдено в репозиторіях.</b>",
        search_empty="❌ | <b>Модулі не знайдено за запитом: <code>{query}</code>.</b>",
        done="✅ | <b>Модуль <code>{name}</code> успішно завантажено!</b>",
        error="❌ | <b>Помилка: <code>{err}</code></b>",
        reloading="⏳ | <b>Перезавантаження всіх модулів...</b>",
        reloaded="♻️ | <b>Модулі перезавантажено. Всього: {count}</b>",
        unloaded="✅ | <b>Модуль <code>{name}</code> вивантажено.</b>",
        search_header="<b>{icon} | <a href='{url}'>{type} Repository</a></b><br>⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯<br>",
        search_item="📦 | <b><a href='{raw_url}'>{name}</a></b> [v{version}]<br>┗ <code>.mdl {cmd_id}</code><br><br>",
        confirm_unsafe="⚠️ | <b>ПОПЕРЕДЖЕННЯ БЕЗПЕКИ</b><br>Ви встановлюєте модуль із <b>{source}</b> — <b>НЕПЕРЕВІРЕНЕ</b> джерело.<br>Цей модуль <b>НЕ</b> було перевірено та може містити шкідливий код.<br><br><b>Ви підтверджуєте встановлення цього модуля?</b>",
        confirm_cancelled="❌ | <b>Встановлення скасовано користувачем.</b>",
        dev_usage="❌ | <b>Прямі посилання/файли вимагають префікса <code>dev</code>.</b>",
        no_args="❌ | <b>Вкажіть ID модуля, URL або відповідайте на .py файл!</b>",
        repo_added="✅ | <b>Репозиторій додано: <code>{url}</code></b>",
        repo_removed="✅ | <b>Репозиторій видалено.</b>",
        invalid_file="❌ | <b>ТІЛЬКИ .PY ТА .ZIP ФАЙЛИ ПРИЙМАЮТЬСЯ!</b>",
    ),
    fr=Strings(
        downloading="⏳ | <b>Téléchargement...</b>",
        fetching="⏳ | <b>Traitement de <code>{id}</code>...</b>",
        repo_not_found="❌ | <b>Module <code>{id}</code> introuvable dans les dépôts.</b>",
        search_empty="❌ | <b>Aucun module trouvé pour la requête: <code>{query}</code>.</b>",
        done="✅ | <b>Module <code>{name}</code> chargé avec succès!</b>",
        error="❌ | <b>Erreur: <code>{err}</code></b>",
        reloading="⏳ | <b>Rechargement de tous les modules...</b>",
        reloaded="♻️ | <b>Modules rechargés. Total: {count}</b>",
        unloaded="✅ | <b>Module <code>{name}</code> déchargé.</b>",
        search_header="<b>{icon} | <a href='{url}'>{type} Repository</a></b><br>⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯<br>",
        search_item="📦 | <b><a href='{raw_url}'>{name}</a></b> [v{version}]<br>┗ <code>.mdl {cmd_id}</code><br><br>",
        confirm_unsafe="⚠️ | <b>AVERTISSEMENT DE SÉCURITÉ</b><br>Vous installez un module depuis <b>{source}</b> — une source <b>NON VÉRIFIÉE</b>.<br>Ce module <b>N'A PAS</b> été examiné et peut contenir du code malveillant.<br><br><b>Confirmez-vous l'installation de ce module?</b>",
        confirm_cancelled="❌ | <b>Installation annulée par l'utilisateur.</b>",
        dev_usage="❌ | <b>Les liens/fichiers directs nécessitent le préfixe <code>dev</code>.</b>",
        no_args="❌ | <b>Fournissez un ID de module, une URL ou répondez à un fichier .py!</b>",
        repo_added="✅ | <b>Dépôt ajouté: <code>{url}</code></b>",
        repo_removed="✅ | <b>Dépôt supprimé.</b>",
        invalid_file="❌ | <b>SEULS LES FICHIERS .PY ET .ZIP SONT ACCEPTÉS!</b>",
    ),
    de=Strings(
        downloading="⏳ | <b>Herunterladen...</b>",
        fetching="⏳ | <b>Verarbeite <code>{id}</code>...</b>",
        repo_not_found="❌ | <b>Modul <code>{id}</code> in keinem Repository gefunden.</b>",
        search_empty="❌ | <b>Keine Module gefunden für: <code>{query}</code>.</b>",
        done="✅ | <b>Modul <code>{name}</code> erfolgreich geladen!</b>",
        error="❌ | <b>Fehler: <code>{err}</code></b>",
        reloading="⏳ | <b>Lade alle Module neu...</b>",
        reloaded="♻️ | <b>Module neu geladen. Gesamt: {count}</b>",
        unloaded="✅ | <b>Modul <code>{name}</code> entladen.</b>",
        search_header="<b>{icon} | <a href='{url}'>{type} Repository</a></b><br>⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯<br>",
        search_item="📦 | <b><a href='{raw_url}'>{name}</a></b> [v{version}]<br>┗ <code>.mdl {cmd_id}</code><br><br>",
        confirm_unsafe="⚠️ | <b>SICHERHEITSWARNUNG</b><br>Sie installieren ein Modul von <b>{source}</b> — einer <b>UNVERIFIZIERTEN</b> Quelle.<br>Dieses Modul wurde <b>NICHT</b> geprüft und könnte schädlichen Code enthalten.<br><br><b>Bestätigen Sie die Installation dieses Moduls?</b>",
        confirm_cancelled="❌ | <b>Installation vom Benutzer abgebrochen.</b>",
        dev_usage="❌ | <b>Direkte Links/Dateien erfordern das <code>dev</code>-Präfix.</b>",
        no_args="❌ | <b>Geben Sie eine Modul-ID, URL oder antworten Sie auf eine .py-Datei!</b>",
        repo_added="✅ | <b>Repository hinzugefügt: <code>{url}</code></b>",
        repo_removed="✅ | <b>Repository entfernt.</b>",
        invalid_file="❌ | <b>NUR .PY- UND .ZIP-DATEIEN WERDEN AKZEPTIERT!</b>",
    ),
    jp=Strings(
        downloading="⏳ | <b>ダウンロード中...</b>",
        fetching="⏳ | <b><code>{id}</code> を処理中...</b>",
        repo_not_found="❌ | <b>モジュール <code>{id}</code> がどのリポジトリにも見つかりません。</b>",
        search_empty="❌ | <b>クエリ <code>{query}</code> に一致するモジュールはありません。</b>",
        done="✅ | <b>モジュール <code>{name}</code> を正常に読み込みました!</b>",
        error="❌ | <b>エラー: <code>{err}</code></b>",
        reloading="⏳ | <b>すべてのモジュールを再読み込み中...</b>",
        reloaded="♻️ | <b>モジュールを再読み込みしました。合計: {count}</b>",
        unloaded="✅ | <b>モジュール <code>{name}</code> をアンロードしました。</b>",
        search_header="<b>{icon} | <a href='{url}'>{type} Repository</a></b><br>⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯<br>",
        search_item="📦 | <b><a href='{raw_url}'>{name}</a></b> [v{version}]<br>┗ <code>.mdl {cmd_id}</code><br><br>",
        confirm_unsafe="⚠️ | <b>セキュリティ警告</b><br><b>{source}</b> からモジュールをインストールしようとしています — <b>未検証</b>のソースです。<br>このモジュールはレビューされておらず、悪意のあるコードを含む可能性があります。<br><br><b>このモジュールをインストールしてもよろしいですか？</b>",
        confirm_cancelled="❌ | <b>ユーザーによりインストールがキャンセルされました。</b>",
        dev_usage="❌ | <b>直接リンク/ファイルには <code>dev</code> プレフィックスが必要です。</b>",
        no_args="❌ | <b>モジュールID、URLを指定するか、.pyファイルに返信してください!</b>",
        repo_added="✅ | <b>リポジトリを追加しました: <code>{url}</code></b>",
        repo_removed="✅ | <b>リポジトリを削除しました。</b>",
        invalid_file="❌ | <b>.PY および .ZIP ファイルのみ受け付けます!</b>",
    ),
)


class MdlPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    target: str = ""
    is_dev: bool = False

    @model_validator(mode='before')
    @classmethod
    def parse_mdl(cls, v: Any):
        if not v or not isinstance(v, str):
            return {"target": ""}
        parts = v.split(maxsplit=1)
        if parts[0].lower() == "dev":
            return {"is_dev": True, "target": parts[1] if len(parts) > 1 else ""}
        return {"is_dev": False, "target": v}

class RepoPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    url: str

    @model_validator(mode='before')
    @classmethod
    def parse(cls, v: Any):
        if isinstance(v, str):
            return {"url": cutils.convert_repo_url(v.strip())}
        return {"url": ""}

class SearchPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    query: str = Field(default="")

    @model_validator(mode='before')
    @classmethod
    def parse_search(cls, v: Any):
        return {"query": v.strip()} if isinstance(v, str) else {"query": ""}

class UnmdPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str

    @model_validator(mode='before')
    @classmethod
    def parse(cls, v: Any):
        return {"name": v.strip()} if isinstance(v, str) else {"name": ""}



@loader.tds
class LoaderModule(loader.Module):
    config = {
        "repo_url": loader.ConfigValue("https://raw.githubusercontent.com/MxUserBot/mx-modules/main", "Main system repository URL", required=True),
        "repo_warn_ok": loader.ConfigValue(False, "User accepted third-party repo warning"),
        "dev_warn_ok": loader.ConfigValue(False, "User accepted dev/file installation warning")
    }

    strings = locales

    async def _matrix_start(self, mx):
        self.repo = loader.RepoManager(mx, self._db, self.config.get("repo_url"))

    async def _security_gate(self, mx, event, payload: MdlPayload, source_verified: bool, is_file: bool = False, on_confirm=None):
        is_direct = payload.target.startswith(("http", "import ", "from ")) or is_file

        if is_direct and not payload.is_dev:
            raise UsageError(self.strings["dev_usage"])

        if is_direct:
            return await self._confirm_unsafe(mx, event, "dev", on_confirm=on_confirm)
        elif not source_verified:
            return await self._confirm_unsafe(mx, event, "repo", on_confirm=on_confirm)

        return True

    async def _confirm_unsafe(self, mx, event, warn_type, on_confirm=None):
        conf_key = f"{warn_type}_warn_ok"
        if self.config.get(conf_key):
            return True

        source_name = "community repository" if warn_type == "repo" else "direct link/file"

        async def _callback(ctx):
            if ctx.payload == "yes":
                self.config.set(conf_key, True)
                if on_confirm:
                    await on_confirm(ctx)
            else:
                await ctx.edit(self.strings["confirm_cancelled"])
            await ctx.close()

        markup = EmojiKeyBoard(
            rows=[[
                EmojiButton("✅", "yes"),
                EmojiButton("❌", "no"),
            ]],
            callback=_callback,
        )

        await utils.answer(
            mx,
            self.strings["confirm_unsafe"].format(source=source_name),
            event=event,
            reply_markup=markup,
        )
        return False

    @loader.command(aliases=["ms"], security=loader.OWNER)
    async def msearch(self, mx, event: MessageEvent, payload: SearchPayload):
        """<query> — search module in repo"""
        if not payload.query:
            raise UsageError
            
        results = await self.repo.search(payload.query)
        if not results:
            return await utils.answer(mx, self.strings["search_empty"].format(query=payload.query))

        results.sort(key=lambda x: not x["is_verified"])

        flat_list = []
        for res in results:
            prefix = ""
            if not res["is_verified"]:
                # Красивый префикс из ника GitHub или "comm/"
                parts = res["repo_url"].split("/")
                if "github" in res["repo_url"] and len(parts) > 3:
                    prefix = f"{parts[3]}/"
                else:
                    prefix = "comm/"

            for mod in res["modules"]:
                flat_list.append({
                    "repo_info": res,
                    "mod_info": mod,
                    "prefix": prefix
                })

        def render_page(items_slice, page_num, total_pages):
            content = []
            last_repo_url = None
            
            for item in items_slice:
                res = item["repo_info"]
                mod = item["mod_info"]
                prefix = item["prefix"]
                
                if res["repo_url"] != last_repo_url:
                    if res["is_verified"]:
                        header = self.strings["search_header"].format(
                            icon="✅", 
                            type="SYSTEM", 
                            url=res["repo_url"]
                        )
                    else:
                        header = "<b>👥 | COMMUNITY Repository</b><br>⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯<br>"
                    
                    content.append(header)
                    last_repo_url = res["repo_url"]
                
                mod_name = mod.get("name") or mod.get("id", "Unknown")
                content.append(
                    self.strings["search_item"].format(
                        name=mod_name,
                        raw_url=mod.get("url", "#"),
                        version=mod.get("version", "1.0.0"),
                        cmd_id=f"{prefix}{mod.get('id')}"
                    )
                )
            
            footer = f"<br><i>Page {page_num + 1} of {total_pages}</i>"
            return "".join(content) + footer

        per_page = 5
        pages = []
        total_mod_count = len(flat_list)
        total_pages_count = (total_mod_count - 1) // per_page + 1
        
        for i in range(0, total_mod_count, per_page):
            pages.append(render_page(flat_list[i : i + per_page], len(pages), total_pages_count))

        if len(pages) == 1:
            await utils.answer(mx, pages[0])
            return

        async def on_page(ctx):
            page = ctx.data.get("page", 0)
            if ctx.payload == "prev":
                page = page - 1 if page > 0 else len(pages) - 1
            else:
                page = (page + 1) % len(pages)
            
            ctx.data["page"] = page
            await ctx.edit(pages[page])

        markup = EmojiKeyBoard(
            rows=[[
                EmojiButton(emoji="⬅️", data="prev"),
                EmojiButton(emoji="➡️", data="next"),
            ]],
            callback=on_page,
            data={"page": 0},
            remove_clicked=True,
        )

        await utils.answer(mx, pages[0], event=event, reply_markup=markup)


    @loader.command(security=loader.OWNER)
    async def mdl(self, mx, event: MessageEvent, payload: MdlPayload):
        """[dev] <id/url/reply> — install module."""
        reply_event = await utils.get_reply_event(mx, event)

        if reply_event:
            fname, content = await self.repo.get_file_content(reply_event)

            if not fname.endswith((".py", ".zip")):
                raise UsageError(self.strings["invalid_file"])

            install_kw = {"filename": fname}
            if fname.endswith(".zip"):
                install_kw["code"] = content
            else:
                install_kw["code"] = content.decode("utf-8", errors="ignore")

            status_id = await utils.answer(mx, self.strings["downloading"])

            async def _install(ctx):
                await ctx.close()
                if await self.repo.install(**install_kw, event=event):
                    await utils.answer(mx, self.strings["done"].format(name=fname), edit_id=status_id)
                    await self.loader.show_module_help(mx, event, fname)
                else:
                    await utils.answer(mx, self.strings["error"].format(err="Install failed!"), edit_id=status_id)

            if not await self._security_gate(mx, event, payload, False, is_file=True, on_confirm=_install):
                return

            if await self.repo.install(**install_kw, event=event):
                await utils.answer(mx, self.strings["done"].format(name=fname), edit_id=status_id)
                await self.loader.show_module_help(mx, event, fname)
            else:
                raise ValueError("Installation failed")
            return

        if not payload.target:
            raise UsageError(self.strings["no_args"])

        status_id = await utils.answer(mx, self.strings["fetching"].format(id=payload.target[:20]))
        url, source = await self.repo.resolve_and_download(payload.target)

        if not url:
            return await utils.answer(mx, self.strings["repo_not_found"].format(id=payload.target), edit_id=status_id)

        async def _install(ctx):
            await ctx.close()
            await utils.answer(mx, self.strings["downloading"], edit_id=status_id)
            if await self.repo.install(target=payload.target, event=event):
                    filename = url.split("/")[-1]
                    if not filename.endswith((".py", ".zip")): filename += ".py"
                    await utils.answer(mx, self.strings["done"].format(name=filename), edit_id=status_id)
                    await self.loader.show_module_help(mx, event, filename)
            else:
                    await utils.answer(mx, self.strings["error"].format(err="Install failed!"), edit_id=status_id)

        if not await self._security_gate(mx, event, payload, getattr(source, "is_verified", False), on_confirm=_install):
            return

        await utils.answer(mx, self.strings["downloading"], edit_id=status_id)
        if await self.repo.install(target=payload.target, event=event):
            filename = url.split("/")[-1]
            if not filename.endswith((".py", ".zip")): filename += ".py"
            await utils.answer(mx, self.strings["done"].format(name=filename), edit_id=status_id)
            await self.loader.show_module_help(mx, event, filename)
        else:
            await utils.answer(mx, self.strings["error"].format(err="Install failed!"), edit_id=status_id)


    @loader.command(security=loader.OWNER)
    async def addrepo(self, mx, event: MessageEvent, payload: RepoPayload):
        """<url> — add repo"""
        if not payload.url:
            raise UsageError(self.strings["no_args"])

        test = await self.repo._fetch_index(payload.url)
        if not test: 
            return await utils.answer(mx, "❌ | <b>Invalid repo or index!</b>")

        async def _add_repo(ctx):
            repos = await self.repo.get_repos()
            if payload.url not in repos:
                repos.append(payload.url)
                await self._db.set("core", "community_repos", repos)
            await ctx.edit(self.strings["repo_added"].format(url=payload.url))

        if not await self._confirm_unsafe(mx, event, "repo", on_confirm=_add_repo):
            return

        repos = await self.repo.get_repos()
        if payload.url not in repos:
            repos.append(payload.url)
            await self._db.set("core", "community_repos", repos)

        await utils.answer(mx, self.strings["repo_added"].format(url=payload.url))


    @loader.command(security=loader.OWNER)
    async def delrepo(self, mx, event: MessageEvent, payload: RepoPayload):
        """<url> — delete repo"""
        if not payload.url:
            raise UsageError(self.strings["no_args"])
            
        repos = await self.repo.get_repos()
        if payload.url in repos:
            repos.remove(payload.url)
            await self._db.set("core", "community_repos", repos)
            await utils.answer(mx, self.strings["repo_removed"])


    @loader.command(security=loader.OWNER)
    async def reload(self, mx, event: MessageEvent):
        """Reload everything modules!"""
        status_id = await utils.answer(mx, self.strings["reloading"])
        errors = await self.loader.register_all(mx)
        msg = self.strings["reloaded"].format(count=len(mx.active_modules))
        if errors:
            error_lines = [f"  ⚠️ <b>{e['name']}</b>: <code>{cutils.escape_html(e['error'])}</code>" for e in errors]
            msg += "<br><br><b>Failed modules:</b><br>" + "<br>".join(error_lines)
        await utils.answer(mx, msg, edit_id=status_id)


    @loader.command(security=loader.OWNER)
    async def unmd(self, mx, event: MessageEvent, payload: UnmdPayload):
        """<name> — delete module"""
        if not payload.name:
            raise UsageError(self.strings["no_args"])
            
        await self.repo.uninstall(payload.name)
        await utils.answer(mx, self.strings["unloaded"].format(name=payload.name))