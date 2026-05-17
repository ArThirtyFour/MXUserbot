#			__  ____  ___   _               _           _   
#			|  \/  \ \/ / | | |___  ___ _ __| |__   ___ | |_ 
#			| |\/| |\  /| | | / __|/ _ \ '__| '_ \ / _ \| __|
#			| |  | |/  \| |_| \__ \  __/ |  | |_) | (_) | |_ 
#			|_|  |_/_/\_\\___/|___/\___|_|  |_.__/ \___/ \__| 
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html


import asyncio

from datetime import datetime

from pydantic import BaseModel

from mautrix.types import MessageEvent, TrustState


class Meta:
    name = "VerifierModule"
    description = "Device trust management and verification."
    version = "2.1.0"
    tags = ["settings"]


from mxc.exceptions import UsageError
from mxc import utils
from mxc.types import EmojiButton
from mxc.utils.keyboard import EmojiKeyBoard
from .. import loader
from ..core.langs import Locales


class Strings(BaseModel):
    fetching: str
    no_devices: str
    dev_list_header: str
    dev_bot: str
    dev_verified: str
    dev_unverified: str
    dev_item: str
    dev_footer: str
    no_id: str
    cant_verify_self: str
    checking: str
    not_found: str
    already_verif: str
    check_other_device: str
    waiting_emoji: str
    verif_emoji: str
    verif_success: str
    verif_cancelled: str
    verif_failed: str
    error: str


locales = Locales(
    ru=Strings(
        fetching="🔍 | <b>Получаю список устройств...</b>",
        no_devices="❌ | <b>Устройства не найдены.</b>",
        dev_list_header="📱 | <b>Ваши устройства:</b><br><br>",
        dev_bot="🤖 | <b>(Этот бот)</b>",
        dev_verified="✅ <b>Проверено</b>",
        dev_unverified="❌ <b>Не проверено</b>",
        dev_item="🖥 | <b>{name}</b><br>└ <code>{id}</code> | {status}<br>└ Последний раз: {last_seen}<br><br>",
        dev_footer="<i>Используйте <code>.verif [device_id]</code> для проверки устройства.</i>",
        no_id="❌ | <b>Укажите ID устройства. Используйте <code>.devices</code> чтобы найти его.</b>",
        cant_verify_self="❌ | <b>Вы не можете проверить самого бота.</b>",
        checking="🔍 | <b>Проверяю устройство <code>{id}</code>...</b>",
        not_found="❌ | <b>Устройство <code>{id}</code> не найдено.</b>",
        already_verif="✅ | <b>Устройство <code>{id}</code> уже проверено!</b>",
        check_other_device="🛡 | <b>Верификация запущена для:</b> <code>{id}</code><br>⏳ <i>Примите запрос на том устройстве.</i>",
        waiting_emoji="⏳ | <b>Ожидание SAS эмодзи от устройства <code>{id}</code>...</b>",
        verif_emoji="🔐 | <b>SAS Эмодзи для устройства <code>{id}</code>:</b><br><br><code>{emojis}</code><br><br>⏳ <i>Верификация в процессе...</i>",
        verif_success="✅ | <b>Устройство <code>{id}</code> успешно проверено!</b>",
        verif_cancelled="❌ | <b>Верификация отменена</b> для устройства <code>{id}</code>.",
        verif_failed="❌ | <b>Верификация не удалась</b> для устройства <code>{id}</code>.",
        error="❌ | <b>Ошибка:</b> <code>{e}</code>",
    ),
    en=Strings(
        fetching="🔍 | <b>Fetching devices...</b>",
        no_devices="❌ | <b>No devices found.</b>",
        dev_list_header="📱 | <b>Your Devices:</b><br><br>",
        dev_bot="🤖 | <b>(This Bot)</b>",
        dev_verified="✅ <b>Verified</b>",
        dev_unverified="❌ <b>Unverified</b>",
        dev_item="🖥 | <b>{name}</b><br>└ <code>{id}</code> | {status}<br>└ Last seen: {last_seen}<br><br>",
        dev_footer="<i>Use <code>.verif [device_id]</code> to verify a device.</i>",
        no_id="❌ | <b>Specify a Device ID. Use <code>.devices</code> to find it.</b>",
        cant_verify_self="❌ | <b>You cannot verify the bot itself.</b>",
        checking="🔍 | <b>Checking device <code>{id}</code>...</b>",
        not_found="❌ | <b>Device <code>{id}</code> not found.</b>",
        already_verif="✅ | <b>Device <code>{id}</code> is already verified!</b>",
        check_other_device="🛡 | <b>Verification initiated for:</b> <code>{id}</code><br>⏳ <i>Accept the request on that device.</i>",
        waiting_emoji="⏳ | <b>Waiting for SAS emoji from device <code>{id}</code>...</b>",
        verif_emoji="🔐 | <b>SAS Emoji for device <code>{id}</code>:</b><br><br><code>{emojis}</code><br><br>⏳ <i>Verification in progress...</i>",
        verif_success="✅ | <b>Device <code>{id}</code> verified successfully!</b>",
        verif_cancelled="❌ | <b>Verification cancelled</b> for device <code>{id}</code>.",
        verif_failed="❌ | <b>Verification failed</b> for device <code>{id}</code>.",
        error="❌ | <b>Error:</b> <code>{e}</code>",
    ),
    ua=Strings(
        fetching="🔍 | <b>Отримую список пристроїв...</b>",
        no_devices="❌ | <b>Пристрої не знайдено.</b>",
        dev_list_header="📱 | <b>Ваші пристрої:</b><br><br>",
        dev_bot="🤖 | <b>(Цей бот)</b>",
        dev_verified="✅ <b>Перевірено</b>",
        dev_unverified="❌ <b>Не перевірено</b>",
        dev_item="🖥 | <b>{name}</b><br>└ <code>{id}</code> | {status}<br>└ Останній раз: {last_seen}<br><br>",
        dev_footer="<i>Використовуйте <code>.verif [device_id]</code> для перевірки пристрою.</i>",
        no_id="❌ | <b>Вкажіть ID пристрою. Використовуйте <code>.devices</code> щоб знайти його.</b>",
        cant_verify_self="❌ | <b>Ви не можете перевірити самого бота.</b>",
        checking="🔍 | <b>Перевіряю пристрій <code>{id}</code>...</b>",
        not_found="❌ | <b>Пристрій <code>{id}</code> не знайдено.</b>",
        already_verif="✅ | <b>Пристрій <code>{id}</code> вже перевірено!</b>",
        check_other_device="🛡 | <b>Верифікацію запущено для:</b> <code>{id}</code><br>⏳ <i>Прийміть запит на тому пристрої.</i>",
        waiting_emoji="⏳ | <b>Очікування SAS емодзі від пристрою <code>{id}</code>...</b>",
        verif_emoji="🔐 | <b>SAS Емодзі для пристрою <code>{id}</code>:</b><br><br><code>{emojis}</code><br><br>⏳ <i>Верифікація в процесі...</i>",
        verif_success="✅ | <b>Пристрій <code>{id}</code> успішно перевірено!</b>",
        verif_cancelled="❌ | <b>Верифікацію скасовано</b> для пристрою <code>{id}</code>.",
        verif_failed="❌ | <b>Верифікацію не вдалося</b> для пристрою <code>{id}</code>.",
        error="❌ | <b>Помилка:</b> <code>{e}</code>",
    ),
    fr=Strings(
        fetching="🔍 | <b>Récupération des appareils...</b>",
        no_devices="❌ | <b>Aucun appareil trouvé.</b>",
        dev_list_header="📱 | <b>Vos appareils:</b><br><br>",
        dev_bot="🤖 | <b>(Ce Bot)</b>",
        dev_verified="✅ <b>Vérifié</b>",
        dev_unverified="❌ <b>Non vérifié</b>",
        dev_item="🖥 | <b>{name}</b><br>└ <code>{id}</code> | {status}<br>└ Dernière vue: {last_seen}<br><br>",
        dev_footer="<i>Utilisez <code>.verif [device_id]</code> pour vérifier un appareil.</i>",
        no_id="❌ | <b>Spécifiez un ID d'appareil. Utilisez <code>.devices</code> pour le trouver.</b>",
        cant_verify_self="❌ | <b>Vous ne pouvez pas vérifier le bot lui-même.</b>",
        checking="🔍 | <b>Vérification de l'appareil <code>{id}</code>...</b>",
        not_found="❌ | <b>Appareil <code>{id}</code> introuvable.</b>",
        already_verif="✅ | <b>L'appareil <code>{id}</code> est déjà vérifié!</b>",
        check_other_device="🛡 | <b>Vérification lancée pour:</b> <code>{id}</code><br>⏳ <i>Acceptez la demande sur cet appareil.</i>",
        waiting_emoji="⏳ | <b>Attente des émojis SAS de l'appareil <code>{id}</code>...</b>",
        verif_emoji="🔐 | <b>Émojis SAS pour l'appareil <code>{id}</code>:</b><br><br><code>{emojis}</code><br><br>⏳ <i>Vérification en cours...</i>",
        verif_success="✅ | <b>Appareil <code>{id}</code> vérifié avec succès!</b>",
        verif_cancelled="❌ | <b>Vérification annulée</b> pour l'appareil <code>{id}</code>.",
        verif_failed="❌ | <b>Échec de la vérification</b> pour l'appareil <code>{id}</code>.",
        error="❌ | <b>Erreur:</b> <code>{e}</code>",
    ),
    de=Strings(
        fetching="🔍 | <b>Geräte werden abgerufen...</b>",
        no_devices="❌ | <b>Keine Geräte gefunden.</b>",
        dev_list_header="📱 | <b>Ihre Geräte:</b><br><br>",
        dev_bot="🤖 | <b>(Dieser Bot)</b>",
        dev_verified="✅ <b>Verifiziert</b>",
        dev_unverified="❌ <b>Nicht verifiziert</b>",
        dev_item="🖥 | <b>{name}</b><br>└ <code>{id}</code> | {status}<br>└ Zuletzt gesehen: {last_seen}<br><br>",
        dev_footer="<i>Nutzen Sie <code>.verif [Geräte-ID]</code> um ein Gerät zu verifizieren.</i>",
        no_id="❌ | <b>Geben Sie eine Geräte-ID an. Nutzen Sie <code>.devices</code> um sie zu finden.</b>",
        cant_verify_self="❌ | <b>Sie können den Bot selbst nicht verifizieren.</b>",
        checking="🔍 | <b>Prüfe Gerät <code>{id}</code>...</b>",
        not_found="❌ | <b>Gerät <code>{id}</code> nicht gefunden.</b>",
        already_verif="✅ | <b>Gerät <code>{id}</code> ist bereits verifiziert!</b>",
        check_other_device="🛡 | <b>Verifizierung gestartet für:</b> <code>{id}</code><br>⏳ <i>Akzeptieren Sie die Anfrage auf diesem Gerät.</i>",
        waiting_emoji="⏳ | <b>Warte auf SAS-Emoji von Gerät <code>{id}</code>...</b>",
        verif_emoji="🔐 | <b>SAS-Emoji für Gerät <code>{id}</code>:</b><br><br><code>{emojis}</code><br><br>⏳ <i>Verifizierung läuft...</i>",
        verif_success="✅ | <b>Gerät <code>{id}</code> erfolgreich verifiziert!</b>",
        verif_cancelled="❌ | <b>Verifizierung abgebrochen</b> für Gerät <code>{id}</code>.",
        verif_failed="❌ | <b>Verifizierung fehlgeschlagen</b> für Gerät <code>{id}</code>.",
        error="❌ | <b>Fehler:</b> <code>{e}</code>",
    ),
    jp=Strings(
        fetching="🔍 | <b>デバイスを取得中...</b>",
        no_devices="❌ | <b>デバイスが見つかりません。</b>",
        dev_list_header="📱 | <b>あなたのデバイス:</b><br><br>",
        dev_bot="🤖 | <b>(このボット)</b>",
        dev_verified="✅ <b>確認済み</b>",
        dev_unverified="❌ <b>未確認</b>",
        dev_item="🖥 | <b>{name}</b><br>└ <code>{id}</code> | {status}<br>└ 最終確認: {last_seen}<br><br>",
        dev_footer="<i><code>.verif [デバイスID]</code> でデバイスを確認します。</i>",
        no_id="❌ | <b>デバイスIDを指定してください。<code>.devices</code> で確認できます。</b>",
        cant_verify_self="❌ | <b>ボット自身を確認することはできません。</b>",
        checking="🔍 | <b>デバイス <code>{id}</code> を確認中...</b>",
        not_found="❌ | <b>デバイス <code>{id}</code> が見つかりません。</b>",
        already_verif="✅ | <b>デバイス <code>{id}</code> は既に確認済みです!</b>",
        check_other_device="🛡 | <b>確認を開始しました:</b> <code>{id}</code><br>⏳ <i>そのデバイスでリクエストを承認してください。</i>",
        waiting_emoji="⏳ | <b>デバイス <code>{id}</code> からのSAS絵文字を待機中...</b>",
        verif_emoji="🔐 | <b>デバイス <code>{id}</code> のSAS絵文字:</b><br><br><code>{emojis}</code><br><br>⏳ <i>確認処理中...</i>",
        verif_success="✅ | <b>デバイス <code>{id}</code> の確認に成功しました!</b>",
        verif_cancelled="❌ | <b>デバイス <code>{id}</code> の確認がキャンセルされました。</b>",
        verif_failed="❌ | <b>デバイス <code>{id}</code> の確認に失敗しました。</b>",
        error="❌ | <b>エラー:</b> <code>{e}</code>",
    ),
)


@loader.tds
class VerifierModule(loader.Module):
    strings = locales

    @loader.command(security=loader.OWNER)
    async def devices(self, mx, event: MessageEvent):
        """Lists all active devices and their verification status."""
        status_id = await utils.answer(mx, self.strings.get("fetching"))

        devices_resp = await mx.client.api.request("GET", "/_matrix/client/v3/devices")
        my_devices = devices_resp.get("devices", [])

        if not my_devices:
            await utils.answer(mx, self.strings.get("no_devices"), edit_id=status_id)
            return

        my_devices.sort(key=lambda d: d.get("last_seen_ts") or 0, reverse=True)

        page_size = 5
        total_pages = (len(my_devices) + page_size - 1) // page_size
        bot_mxid = mx.client.mxid
        bot_pub_key = mx.client.crypto.account.signing_key
        store = mx.client.crypto.crypto_store

        from mautrix.types import CrossSigner

        async def build_page(page):
            start = page * page_size
            end = start + page_size
            page_devices = my_devices[start:end]

            msg = self.strings.get("dev_list_header")
            if total_pages > 1:
                msg += f"<i>Page {page + 1}/{total_pages}</i><br><br>"

            for dev in page_devices:
                d_id = dev["device_id"]
                d_name = dev.get("display_name", "Unknown Device")
                last_seen_ts = dev.get("last_seen_ts", 0)

                if last_seen_ts:
                    dt = datetime.fromtimestamp(last_seen_ts / 1000)
                    last_seen_str = dt.strftime("%Y-%m-%d %H:%M")
                else:
                    last_seen_str = "Unknown"

                if d_id == mx.client.device_id:
                    status = self.strings.get("dev_bot")
                else:
                    device_info = await store.get_device(bot_mxid, d_id)
                    is_verified = False
                    if device_info:
                        if device_info.trust >= TrustState.VERIFIED:
                            is_verified = True
                        else:
                            target = CrossSigner(user_id=bot_mxid, key=device_info.signing_key)
                            signer = CrossSigner(user_id=bot_mxid, key=bot_pub_key)
                            is_verified = await store.is_key_signed_by(target, signer)
                    status = self.strings.get("dev_verified") if is_verified else self.strings.get("dev_unverified")

                msg += self.strings.get("dev_item").format(name=d_name, id=d_id, status=status, last_seen=last_seen_str)

            msg += self.strings.get("dev_footer")
            return msg

        async def page_callback(ctx):
            page = ctx.data.get("page", 0)

            if ctx.payload == "next" and page < total_pages - 1:
                page += 1
            elif ctx.payload == "prev" and page > 0:
                page -= 1
            else:
                return

            ctx.data["page"] = page

            msg = await build_page(page)

            buttons = []
            if page > 0:
                buttons.append(EmojiButton("⬅️", "prev"))
            if page < total_pages - 1:
                buttons.append(EmojiButton("➡️", "next"))

            ctx.session.buttons = {btn.emoji: btn for btn in buttons}
            await ctx.edit(msg)
            await ctx.refresh(force_order=True)

        msg = await build_page(0)

        buttons = []
        if total_pages > 1:
            buttons.append(EmojiButton("➡️", "next"))

        markup = EmojiKeyBoard(
            rows=[buttons],
            callback=page_callback,
            data={"page": 0},
        )

        await utils.answer(mx, msg, edit_id=status_id, reply_markup=markup)


    @loader.command(security=loader.OWNER)
    async def verif(self, mx, event: MessageEvent, target_id: str = None):
        """<device_id> — Start verification for a specific device."""

        if target_id == mx.client.device_id:
            return await utils.answer(mx, self.strings.get("cant_verify_self"))

        status_id = await utils.answer(mx, self.strings.get("checking").format(id=target_id))

        devices_resp = await mx.client.api.request("GET", "/_matrix/client/v3/devices")
        my_devices = devices_resp.get("devices",[])

        target_dev = next((d for d in my_devices if d['device_id'] == target_id), None)

        if not target_dev:
            return await utils.answer(mx, self.strings.get("not_found").format(id=target_id), edit_id=status_id)

        identity = await mx.client.crypto.crypto_store.get_device(mx.client.mxid, target_id)
        if not identity:
            identity = await mx.client.crypto.get_or_fetch_device(mx.client.mxid, target_id)

        if identity and identity.trust >= TrustState.VERIFIED:
            return await utils.answer(mx, self.strings.get("already_verif").format(id=target_id), edit_id=status_id)

        await utils.answer(mx, self.strings.get("check_other_device").format(id=target_id), edit_id=status_id)

        try:
            emojis, txn_id, result_future = await mx.sas_verifier.start_verification(
                mx.client.mxid, target_id
            )
            emoji_str = " | ".join(e.split(":", 1)[1] for e in emojis)
            await utils.answer(mx, self.strings.get("verif_emoji").format(
                id=target_id, emojis=emoji_str
            ), edit_id=status_id)

            try:
                result = await asyncio.wait_for(result_future, timeout=120)
            except asyncio.TimeoutError:
                result = "timeout"

            if result == "success":
                await utils.answer(mx, self.strings.get("verif_success").format(id=target_id))
            elif result == "cancelled":
                await utils.answer(mx, self.strings.get("verif_cancelled").format(id=target_id))
            else:
                await utils.answer(mx, self.strings.get("verif_failed").format(id=target_id))

        except asyncio.CancelledError:
            await utils.answer(mx, self.strings.get("verif_cancelled").format(id=target_id), edit_id=status_id)
        except TimeoutError:
            await utils.answer(mx, self.strings.get("error").format(
                e="Verification timed out. The device did not respond."
            ), edit_id=status_id)
        except Exception as e:
            await utils.answer(mx, self.strings.get("error").format(e=str(e)), edit_id=status_id)
