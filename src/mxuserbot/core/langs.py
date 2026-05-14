# ©️ Pasha Hatsune, 2025-2026
# This file is a part of MXUserbot
# 🌐 https://github.com/MxUserBot/MXUserbot
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import yaml
from pathlib import Path

LANGS_DIR = Path(__file__).resolve().parent.parent / "langpacks"

_CURRENT = "en"
_FLAT: dict[str, str] = {}
_FALLBACK: dict[str, str] = {}
_GETTER = None
_SETTER = None


def _flatten(data: dict, prefix: str = "") -> dict[str, str]:
    result = {}
    for k, v in data.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            result.update(_flatten(v, key))
        elif isinstance(v, str):
            result[key] = v
    return result


# Preload English as default fallback
_en_path = LANGS_DIR / "en.yaml"
if _en_path.exists():
    with open(_en_path, encoding="utf-8") as f:
        _FALLBACK = _flatten(yaml.safe_load(f) or {})
        _FLAT = dict(_FALLBACK)


def _load(code: str) -> None:
    global _CURRENT, _FLAT
    path = LANGS_DIR / f"{code}.yaml"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            _FLAT = _flatten(yaml.safe_load(f) or {})
        _CURRENT = code


def _fmt(template: str, **kwargs) -> str:
    for k, v in kwargs.items():
        template = template.replace(f"{{{k}}}", str(v))
    return template


class CoreStrings:
    def __call__(self, _key: str, **kwargs) -> str:
        text = _FLAT.get(_key, _FALLBACK.get(_key, _key))
        return _fmt(text, **kwargs) if kwargs else text


STRINGS = CoreStrings()


async def init(getter, setter) -> None:
    global _GETTER, _SETTER
    _GETTER = getter
    _SETTER = setter
    saved = await getter("lang")
    if saved and saved != "en":
        _load(saved)


def available() -> list[str]:
    return sorted(p.stem for p in LANGS_DIR.glob("*.yaml"))


def current() -> str:
    return _CURRENT


async def switch(code: str) -> bool:
    path = LANGS_DIR / f"{code}.yaml"
    if not path.exists():
        return False
    _load(code)
    if _SETTER:
        await _SETTER("lang", code)
    return True
