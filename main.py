import customtkinter as ctk
import minecraft_launcher_lib
import subprocess
import os
import json
import threading
import re
import io
import sys
import requests
import urllib.request
import urllib.parse
import urllib.error
import tempfile
import shutil
import platform
import zipfile
import tarfile
import hashlib
import traceback
from tkinter import filedialog
from datetime import datetime
from tkinter import messagebox
from PIL import Image

# ============ НАСТРОЙКИ ============
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ============ ЛОКАЛИЗАЦИЯ И ТЕМЫ v1.0 ============
LANGUAGE_NAMES = {
    "ru": "Русский",
    "en": "English",
    "de": "Deutsch",
    "uk": "Українська",
}
THEME_NAMES = {
    "dark": "Тёмная",
    "light": "Светлая",
    "midnight": "Midnight",
    "ocean": "Ocean",
    "purple": "Purple",
    "forest": "Forest",
}
THEME_STYLES = {
    "dark": ("dark", "green", "#4CAF50", "#3d8b40"),
    "light": ("light", "blue", "#2563EB", "#1D4ED8"),
    "midnight": ("dark", "dark-blue", "#6366F1", "#4F46E5"),
    "ocean": ("dark", "blue", "#06B6D4", "#0891B2"),
    "purple": ("dark", "dark-blue", "#A855F7", "#9333EA"),
    "forest": ("dark", "green", "#22C55E", "#16A34A"),
}
TRANSLATIONS = {
    "en": {
        "Настройки":"Settings","⚙  Настройки":"⚙  Settings","🎨 Внешний вид":"🎨 Appearance",
        "Тема оформления:":"Theme:","Язык интерфейса:":"Interface language:",
        "Тёмная":"Dark","Светлая":"Light","Системная":"System",
        "Сохранить":"Save","Закрыть":"Close","💾 Сохранить":"💾 Save",
        "👤 Профиль":"👤 Profile","Никнейм офлайн режима:":"Offline nickname:",
        "⚡ Поведение":"⚡ Behaviour","Авто-запуск игры после установки":"Auto-launch after installation",
        "Показывать консоль при запуске":"Show console on launch","☕ Java":"☕ Java",
        "☕ Java Manager":"☕ Java Manager","💻 Система":"💻 System","📁 Папки":"📁 Folders",
        "📂 Открыть папку лаунчера":"📂 Open launcher folder","📝 Открыть launcher.log":"📝 Open launcher.log",
        "📂 Открыть папку экземпляров":"📂 Open instances folder","Фоновое изображение:":"Background image:",
        "📷 Выбрать":"📷 Choose","🔄 Сбросить":"🔄 Reset","↩ Автовыбор":"↩ Automatic",
        "Версия Minecraft:":"Minecraft version:","Загрузчик модов:":"Mod loader:",
        "▶  ИГРАТЬ":"▶  PLAY","➕ Новый экземпляр":"➕ New instance","❓  Частые вопросы":"❓  FAQ",
        "🌐  Сетевая игра":"🌐  Network game","Состояние экземпляра":"Instance status",
    },
    "de": {
        "Настройки":"Einstellungen","⚙  Настройки":"⚙  Einstellungen","🎨 Внешний вид":"🎨 Erscheinungsbild",
        "Тема оформления:":"Thema:","Язык интерфейса:":"Oberflächensprache:",
        "Тёмная":"Dunkel","Светлая":"Hell","Системная":"System",
        "Сохранить":"Speichern","Закрыть":"Schließen","💾 Сохранить":"💾 Speichern",
        "👤 Профиль":"👤 Profil","Никнейм офлайн режима:":"Offline-Spitzname:",
        "⚡ Поведение":"⚡ Verhalten","Авто-запуск игры после установки":"Spiel nach Installation starten",
        "Показывать консоль при запуске":"Konsole beim Start anzeigen","☕ Java":"☕ Java",
        "☕ Java Manager":"☕ Java Manager","💻 Система":"💻 System","📁 Папки":"📁 Ordner",
        "📂 Открыть папку лаунчера":"📂 Launcher-Ordner öffnen","📝 Открыть launcher.log":"📝 launcher.log öffnen",
        "📂 Открыть папку экземпляров":"📂 Instanzordner öffnen","Фоновое изображение:":"Hintergrundbild:",
        "📷 Выбрать":"📷 Auswählen","🔄 Сбросить":"🔄 Zurücksetzen","↩ Автовыбор":"↩ Automatisch",
        "Версия Minecraft:":"Minecraft-Version:","Загрузчик модов:":"Mod-Loader:",
        "▶  ИГРАТЬ":"▶  SPIELEN","➕ Новый экземпляр":"➕ Neue Instanz","❓  Частые вопросы":"❓  FAQ",
        "🌐  Сетевая игра":"🌐 Netzwerk","Состояние экземпляра":"Instanzstatus",
    },
    "uk": {
        "Настройки":"Налаштування","⚙  Настройки":"⚙  Налаштування","🎨 Внешний вид":"🎨 Вигляд",
        "Тема оформления:":"Тема:","Язык интерфейса:":"Мова інтерфейсу:",
        "Тёмная":"Темна","Светлая":"Світла","Системная":"Системна",
        "Сохранить":"Зберегти","Закрыть":"Закрити","💾 Сохранить":"💾 Зберегти",
        "👤 Профиль":"👤 Профіль","Никнейм офлайн режима:":"Нік офлайн режиму:",
        "⚡ Поведение":"⚡ Поведінка","Авто-запуск игры после установки":"Автозапуск після встановлення",
        "Показывать консоль при запуске":"Показувати консоль під час запуску","☕ Java":"☕ Java",
        "☕ Java Manager":"☕ Java Manager","💻 Система":"💻 Система","📁 Папки":"📁 Папки",
        "📂 Открыть папку лаунчера":"📂 Відкрити папку лаунчера","📝 Открыть launcher.log":"📝 Відкрити launcher.log",
        "📂 Открыть папку экземпляров":"📂 Відкрити папку екземплярів","Фоновое изображение:":"Фонове зображення:",
        "📷 Выбрать":"📷 Вибрати","🔄 Сбросить":"🔄 Скинути","↩ Автовыбор":"↩ Автовибір",
        "Версия Minecraft:":"Версія Minecraft:","Загрузчик модов:":"Завантажувач модів:",
        "▶  ИГРАТЬ":"▶  ГРАТИ","➕ Новый экземпляр":"➕ Новий екземпляр","❓  Частые вопросы":"❓  FAQ",
        "🌐  Сетевая игра":"🌐 Мережева гра","Состояние экземпляра":"Стан екземпляра",
    },
}
def _translate_widget_tree(widget, lang):
    if lang == "ru": return
    mapping = TRANSLATIONS.get(lang, {})
    try:
        if hasattr(widget, "cget") and hasattr(widget, "configure"):
            val = widget.cget("text")
            if isinstance(val, str) and val in mapping:
                widget.configure(text=mapping[val])
    except Exception:
        pass
    try:
        for child in widget.winfo_children():
            _translate_widget_tree(child, lang)
    except Exception:
        pass

def apply_launcher_theme(theme):
    theme = theme if theme in THEME_STYLES else "dark"
    mode, color_theme, accent, hover = THEME_STYLES[theme]
    ctk.set_appearance_mode(mode)
    try:
        ctk.set_default_color_theme(color_theme)
    except Exception:
        pass
    return accent, hover

APPDATA = os.getenv("APPDATA") or os.path.expanduser("~")
LAUNCHER_DIR = os.path.join(APPDATA, ".CraftLauncher")
INSTANCES_DIR = os.path.join(LAUNCHER_DIR, "instances")
CONFIG_FILE = os.path.join(LAUNCHER_DIR, "config.json")
LOG_FILE = os.path.join(LAUNCHER_DIR, "launcher.log")
JAVA_RUNTIME_DIR = os.path.join(LAUNCHER_DIR, "runtime")

AUTHLIB_JAR = os.path.join(LAUNCHER_DIR, "authlib-injector.jar")
AUTHLIB_URL = "https://github.com/yushijinhun/authlib-injector/releases/latest/download/authlib-injector.jar"

APP_VERSION = "1.0.0"
APP_VERSION_LABEL = f"v{APP_VERSION}"
USER_AGENT = f"CraftLauncher/{APP_VERSION}"
MAIN_THREAD_ID = threading.get_ident()

ELY_AUTH_URL = "https://authserver.ely.by/auth/authenticate"
ELY_SKIN_URL = "https://skinsystem.ely.by/skins/{nickname}.png"

MODRINTH_API = "https://api.modrinth.com/v2"

os.makedirs(LAUNCHER_DIR, exist_ok=True)
os.makedirs(INSTANCES_DIR, exist_ok=True)
os.makedirs(JAVA_RUNTIME_DIR, exist_ok=True)


def get_resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


ICON_PATH = get_resource_path("icon.ico")

# ============ БЕЗОПАСНОСТЬ И СОВМЕСТИМОСТЬ ============
IS_WINDOWS = os.name == "nt"
CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

def run_subprocess_kwargs():
    kwargs = {}
    if CREATE_NO_WINDOW:
        kwargs["creationflags"] = CREATE_NO_WINDOW
    return kwargs

def safe_instance_name(name):
    name = str(name or "").strip()
    if not name or name in {".", ".."} or any(ch in name for ch in "/\\"):
        raise ValueError("Недопустимое имя экземпляра")
    if os.path.basename(name) != name or len(name) > 80:
        raise ValueError("Недопустимое имя экземпляра")
    return name

def atomic_json_write(path, data):
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp_", suffix=".json", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass

def ui_call(widget, callback):
    try:
        widget.after(0, callback)
    except Exception:
        pass

def open_path(path):
    """Открыть файл/папку системным приложением на Windows/Linux/macOS."""
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    if IS_WINDOWS:
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path], **run_subprocess_kwargs())
    else:
        subprocess.Popen(["xdg-open", path], **run_subprocess_kwargs())

def on_ui_thread():
    return threading.get_ident() == MAIN_THREAD_ID

def http_get(url, *, params=None, timeout=10, stream=False):
    return requests.get(
        url, params=params, timeout=timeout, stream=stream,
        headers={"User-Agent": USER_AGENT}
    )



# ============ JAVA MANAGER ============
JAVA_REQUIRED_BY_MC = (
    ((0, 0), 8),       # fallback
    ((1, 17), 17),
    ((1, 20, 5), 21),
)

def parse_mc_version(version):
    match = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?", str(version or "").strip())
    if not match:
        return None
    return tuple(int(x) for x in match.groups(default="0"))

def required_java_major(mc_version):
    parsed = parse_mc_version(mc_version)
    if not parsed:
        return 17
    if parsed < (1, 17):
        return 8
    if parsed < (1, 20, 5):
        return 17
    return 21

def java_executable(path):
    if not path:
        return None
    path = os.path.abspath(os.path.expanduser(str(path)))
    if os.path.isfile(path):
        return path
    if os.path.isdir(path):
        candidate = os.path.join(path, "bin", "java.exe" if IS_WINDOWS else "java")
        if os.path.isfile(candidate):
            return candidate
    return None

def java_major_version(executable):
    executable = java_executable(executable) or executable
    if not executable:
        return None
    try:
        result = subprocess.run(
            [executable, "-version"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
            timeout=5, **run_subprocess_kwargs()
        )
        text = result.stdout or ""
        # Java 8: java version "1.8.0_..."
        m = re.search(r'version\s+"([^"]+)"', text, re.I)
        if not m:
            m = re.search(r'openjdk\s+(\d+)', text, re.I)
            if m:
                return int(m.group(1))
            return None
        value = m.group(1)
        if value.startswith("1."):
            return int(value.split(".")[1])
        return int(re.match(r"\d+", value).group())
    except (OSError, subprocess.SubprocessError, ValueError, AttributeError):
        return None

def discover_java_runtimes():
    candidates = []
    seen = set()

    def add(path):
        path = java_executable(path)
        if not path:
            return
        key = os.path.normcase(os.path.normpath(path))
        if key in seen:
            return
        seen.add(key)
        major = java_major_version(path)
        if major:
            candidates.append({"path": path, "major": major})

    # PATH first.
    add(shutil.which("java"))

    roots = []
    if IS_WINDOWS:
        for env in ("JAVA_HOME", "JDK_HOME"):
            if os.getenv(env):
                roots.append(os.getenv(env))
        roots.append(JAVA_RUNTIME_DIR)
        for base in (
            os.getenv("ProgramFiles"),
            os.getenv("ProgramFiles(x86)"),
            os.getenv("LOCALAPPDATA"),
        ):
            if base:
                roots.extend([
                    os.path.join(base, "Java"),
                    os.path.join(base, "Eclipse Adoptium"),
                    os.path.join(base, "Microsoft"),
                ])
    elif sys.platform == "darwin":
        roots.append("/Library/Java/JavaVirtualMachines")
        if os.getenv("JAVA_HOME"):
            roots.append(os.getenv("JAVA_HOME"))
    else:
        roots.append(JAVA_RUNTIME_DIR)
        roots.extend(["/usr/lib/jvm", "/usr/java"])
        if os.getenv("JAVA_HOME"):
            roots.append(os.getenv("JAVA_HOME"))

    for root in roots:
        if not root or not os.path.exists(root):
            continue
        try:
            if os.path.isfile(root):
                add(root)
                continue
            add(root)
            for entry in os.listdir(root):
                child = os.path.join(root, entry)
                add(child)
                if os.path.isdir(child):
                    add(os.path.join(child, "Contents", "Home"))
        except OSError:
            continue

    candidates.sort(key=lambda x: (x["major"], x["path"]), reverse=True)
    return candidates

def choose_java_for_version(mc_version, configured_path=None):
    required = required_java_major(mc_version)
    configured = java_executable(configured_path)
    if configured:
        major = java_major_version(configured)
        if major:
            if major == required:
                return configured, major, None
            return configured, major, (
                f"Выбрана Java {major}, но Minecraft {mc_version} "
                f"рекомендует Java {required}."
            )

    runtimes = discover_java_runtimes()
    exact = [j for j in runtimes if j["major"] == required]
    if exact:
        return exact[0]["path"], required, None

    return None, required, (
        f"Для Minecraft {mc_version} нужна Java {required}. "
        f"Совместимая Java не найдена."
    )


def java_platform_info():
    """Return Adoptium API platform identifiers for the current machine."""
    system = sys.platform
    machine = platform.machine().lower()
    if system.startswith("win"):
        os_id = "windows"
    elif system == "darwin":
        os_id = "mac"
    else:
        os_id = "linux"

    if machine in ("amd64", "x86_64", "x64"):
        arch = "x64"
    elif machine in ("aarch64", "arm64"):
        arch = "aarch64"
    elif machine in ("x86", "i386", "i686"):
        arch = "x32"
    else:
        arch = "x64"
    return os_id, arch

def managed_java_path(major):
    root = os.path.join(JAVA_RUNTIME_DIR, f"java{int(major)}")
    return java_executable(root)

def download_and_install_java(major, progress_callback=None):
    """Download a Temurin JDK from Adoptium and install it privately for CraftLauncher."""
    major = int(major)
    os_id, arch = java_platform_info()
    if os_id == "windows" and arch == "x32":
        raise RuntimeError("Автоустановка Java для Windows x86 не поддерживается.")
    api = f"https://api.adoptium.net/v3/assets/latest/{major}/hotspot"
    params = {"os": os_id, "architecture": arch, "image_type": "jdk", "vendor": "eclipse"}
    response = http_get(api, params=params, timeout=30)
    response.raise_for_status()
    assets = response.json()
    if not assets:
        raise RuntimeError(f"Adoptium не предоставил Java {major} для {os_id}/{arch}.")
    binary = assets[0].get("binary", {})
    package = binary.get("package", {})
    url = package.get("link")
    filename = package.get("name") or os.path.basename(urllib.parse.urlparse(url or "").path)
    if not url:
        raise RuntimeError("Не удалось получить ссылку на архив Java.")

    target_root = os.path.join(JAVA_RUNTIME_DIR, f"java{major}")
    os.makedirs(JAVA_RUNTIME_DIR, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix=f"java{major}_", dir=JAVA_RUNTIME_DIR)
    archive = os.path.join(temp_dir, filename or "java.archive")
    try:
        with requests.get(url, stream=True, timeout=60, headers={"User-Agent": USER_AGENT}) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length") or 0)
            done = 0
            with open(archive, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if not chunk:
                        continue
                    f.write(chunk)
                    done += len(chunk)
                    if progress_callback:
                        progress_callback(done, total)

        extract_dir = os.path.join(temp_dir, "extract")
        os.makedirs(extract_dir, exist_ok=True)
        lower = archive.lower()
        if lower.endswith(".zip"):
            with zipfile.ZipFile(archive) as z:
                z.extractall(extract_dir)
        elif lower.endswith((".tar.gz", ".tgz", ".tar")):
            with tarfile.open(archive, "r:*") as t:
                t.extractall(extract_dir)
        else:
            raise RuntimeError("Неизвестный формат архива Java.")

        candidates = []
        for root, dirs, files in os.walk(extract_dir):
            exe = os.path.join(root, "bin", "java.exe" if IS_WINDOWS else "java")
            if os.path.isfile(exe):
                candidates.append(root)
        if not candidates:
            raise RuntimeError("В архиве Java не найден исполняемый файл.")

        selected_root = candidates[0]
        if os.path.exists(target_root):
            shutil.rmtree(target_root, ignore_errors=True)
        shutil.move(selected_root, target_root)
        executable = java_executable(target_root)
        detected = java_major_version(executable)
        if detected != major:
            shutil.rmtree(target_root, ignore_errors=True)
            raise RuntimeError(f"Скачана Java {detected}, ожидалась Java {major}.")
        log(f"Installed managed Java {major}: {executable}")
        return executable
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def log(msg, level="INFO"):
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] [{level}] {msg}\n")
    except Exception:
        pass


log("=" * 60)
log(f"CraftLauncher {APP_VERSION_LABEL} started")


# ============ СТАТИСТИКА ЗАПУСКОВ ============
STATS_FILE = os.path.join(LAUNCHER_DIR, "launch_stats.json")

def load_launch_stats(instance_name=None):
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f: data = json.load(f)
        if not isinstance(data, dict): data = {}
    except Exception: data = {}
    if instance_name is None: return data
    return data.setdefault(instance_name, {"launches": 0, "success": 0, "crashes": 0, "last_start": "", "last_exit": "", "last_code": None})

def save_launch_stats(data):
    try: atomic_json_write(STATS_FILE, data)
    except Exception as e: log(f"Stats save error: {e}", "WARN")

def record_launch_start(instance_name):
    data=load_launch_stats(); item=data.setdefault(instance_name, {"launches":0,"success":0,"crashes":0,"last_start":"","last_exit":"","last_code":None})
    item["launches"]=int(item.get("launches",0))+1; item["last_start"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S"); save_launch_stats(data)

def record_launch_end(instance_name, code):
    data=load_launch_stats(); item=data.setdefault(instance_name, {"launches":0,"success":0,"crashes":0,"last_start":"","last_exit":"","last_code":None})
    item["last_exit"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S"); item["last_code"]=int(code) if code is not None else None
    key="success" if code==0 else "crashes"; item[key]=int(item.get(key,0))+1; save_launch_stats(data)

def prepare_safe_mode(instance_name):
    mods=os.path.join(instance_minecraft_dir(instance_name),"mods"); backup=os.path.join(instance_minecraft_dir(instance_name),".craftlauncher_safe_mods"); moved=[]
    if not os.path.isdir(mods): return moved
    os.makedirs(backup,exist_ok=True)
    for fn in os.listdir(mods):
        src=os.path.join(mods,fn)
        if os.path.isfile(src) and fn.lower().endswith(".jar"):
            dst=os.path.join(backup,fn)
            if os.path.exists(dst):
                base,ext=os.path.splitext(fn); dst=os.path.join(backup,f"{base}.backup{ext}")
            shutil.move(src,dst); moved.append((dst,src))
    return moved

def restore_safe_mode(moved):
    for src,dst in moved or []:
        try:
            os.makedirs(os.path.dirname(dst),exist_ok=True)
            if os.path.exists(src): shutil.move(src,dst)
        except OSError as e: log(f"Safe mode restore error: {e}","WARN")

def duplicate_instance(source_name,new_name):
    source_name=safe_instance_name(source_name); new_name=safe_instance_name(new_name); src=instance_path(source_name); dst=instance_path(new_name)
    if not os.path.isdir(src): raise FileNotFoundError(source_name)
    if os.path.exists(dst): raise FileExistsError(new_name)
    shutil.copytree(src,dst)
    with open(instance_config_path(new_name),"r",encoding="utf-8") as f: cfg=json.load(f)
    cfg["name"]=new_name; cfg["created"]=datetime.now().strftime("%Y-%m-%d %H:%M"); atomic_json_write(instance_config_path(new_name),cfg)
    data=load_launch_stats(); data.pop(new_name,None); save_launch_stats(data); return new_name

def preflight_instance(instance_name):
    problems=[]
    try:
        with open(instance_config_path(instance_name),"r",encoding="utf-8") as f: cfg=json.load(f)
    except Exception as e: return [f"Не удалось прочитать конфигурацию: {e}"]
    version=cfg.get("version") or cfg.get("launch_version"); launch_version=cfg.get("launch_version") or version
    if not version: problems.append("Не указана версия Minecraft")
    elif not is_version_installed(instance_name,launch_version): problems.append(f"Minecraft {launch_version} не установлен или повреждён")
    profile=get_active_profile(instance_name); java,required,warning=choose_java_for_version(version or "1.20.1",profile.get("java_path") or load_config().get("java_path"))
    if not java: problems.append(f"Не найдена совместимая Java {required}")
    elif warning: problems.append(warning)
    if cfg.get("mod_loader","vanilla")!="vanilla" and not cfg.get("launch_version"): problems.append(f"Для {cfg.get('mod_loader').upper()} не выбран launch version")
    return problems

# ============ RAM ============
try:
    import psutil

    def get_ram_limits():
        total_mb = int(psutil.virtual_memory().total / (1024 * 1024))
        max_ram = max(1024, ((total_mb - 1024) // 256) * 256)
        return 512, max_ram, total_mb

    RAM_MIN, RAM_MAX, RAM_TOTAL = get_ram_limits()
    log(f"RAM: {RAM_TOTAL} MB")
except ImportError:
    RAM_MIN, RAM_MAX, RAM_TOTAL = 512, 8192, 8192
    log("psutil not installed", "WARN")


# ============ VPN ============
def get_vpn_ip():
    try:
        if not IS_WINDOWS:
            return None, None
        result = subprocess.run(
            ["ipconfig"], capture_output=True, text=True,
            encoding="cp866", errors="replace", **run_subprocess_kwargs()
        )
        lines = result.stdout.split("\n")

        for i, line in enumerate(lines):
            if "Radmin VPN" in line or "Radmin" in line:
                for j in range(i, min(i + 15, len(lines))):
                    if "IPv4" in lines[j] or "IP-адрес" in lines[j] or "IP Address" in lines[j]:
                        parts = lines[j].strip().split(":")
                        if len(parts) >= 2:
                            ip = parts[-1].strip().split()[0]
                            if "." in ip and not ip.startswith("127."):
                                return ip, "Radmin VPN"

        for i, line in enumerate(lines):
            if "Hamachi" in line:
                for j in range(i, min(i + 15, len(lines))):
                    if "IPv4" in lines[j] or "IP-адрес" in lines[j] or "IP Address" in lines[j]:
                        parts = lines[j].strip().split(":")
                        if len(parts) >= 2:
                            ip = parts[-1].strip().split()[0]
                            if "." in ip and not ip.startswith("127."):
                                return ip, "Hamachi"

        for line in lines:
            if ("IPv4" in line or "IP-адрес" in line) and ("25." in line or "5." in line):
                parts = line.strip().split(":")
                if len(parts) >= 2:
                    ip = parts[-1].strip().split()[0]
                    if ip.startswith("25."):
                        return ip, "Radmin VPN"
                    elif ip.startswith("5."):
                        return ip, "Hamachi"
    except Exception as e:
        log(f"VPN scan: {e}", "ERROR")
    return None, None


# ============ КАТЕГОРИИ MODRINTH ============
MODRINTH_CATEGORIES = [
    "Все категории",
    "adventure",       # приключения
    "cursed",          # хоррор / странное
    "decoration",      # декорации
    "economy",         # экономика
    "equipment",       # снаряжение
    "food",            # еда
    "game-mechanics",  # игровая механика
    "library",         # библиотеки
    "magic",           # магия
    "mobs",            # мобы
    "optimization",    # оптимизация
    "social",          # социальное
    "storage",         # хранение
    "technology",      # технологии
    "transportation",  # транспорт
    "utility",         # утилиты
    "worldgen",        # генерация мира
]

# Русские названия для категорий
CATEGORY_LABELS = {
    "Все категории": "Все категории",
    "adventure": "🏔 Приключения",
    "cursed": "👻 Хоррор",
    "decoration": "🎨 Декорации",
    "economy": "💰 Экономика",
    "equipment": "⚔ Снаряжение",
    "food": "🍔 Еда",
    "game-mechanics": "🎮 Механика",
    "library": "📚 Библиотеки",
    "magic": "🔮 Магия",
    "mobs": "🐉 Мобы",
    "optimization": "⚡ Оптимизация",
    "social": "👥 Социальное",
    "storage": "📦 Хранилище",
    "technology": "⚙ Технологии",
    "transportation": "🚗 Транспорт",
    "utility": "🔧 Утилиты",
    "worldgen": "🌍 Генерация мира",
}

CATEGORY_LABELS_REVERSE = {v: k for k, v in CATEGORY_LABELS.items()}


# ============ MODRINTH ============
def search_modrinth_mods_advanced(query="", mc_version=None, category=None,
                                    limit=20, index="downloads"):
    """
    Расширенный поиск модов.
    index: "downloads" (популярные), "relevance" (релевантность),
           "newest" (новые), "updated" (обновлённые)
    """
    try:
        facets = [["project_type:mod"]]
        if mc_version:
            facets.append([f"versions:{mc_version}"])
        if category and category != "Все категории":
            facets.append([f"categories:{category}"])

        params = {
            "limit": limit,
            "index": index,
            "facets": json.dumps(facets),
        }
        # Если запрос пустой — поиск популярных
        if query:
            params["query"] = query

        headers = {"User-Agent": USER_AGENT}
        response = http_get(f"{MODRINTH_API}/search", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        log(f"Modrinth: query='{query}' cat='{category}' → {len(data.get('hits', []))}")
        return data.get("hits", [])
    except Exception as e:
        log(f"Modrinth search error: {e}", "ERROR")
        return []


def get_modrinth_versions(project_id, mc_version, mod_loader=None):
    try:
        params = {"game_versions": json.dumps([mc_version])}
        if mod_loader:
            params["loaders"] = json.dumps([mod_loader])
        headers = {"User-Agent": USER_AGENT}
        response = http_get(f"{MODRINTH_API}/project/{project_id}/version", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log(f"Modrinth versions error: {e}", "ERROR")
        return []


def get_modrinth_version(version_id):
    if not version_id:
        return None
    try:
        response = http_get(
            f"{MODRINTH_API}/version/{version_id}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log(f"Modrinth version {version_id} error: {e}", "WARN")
        return None

def get_mod_dependencies(project_id, mc_version):
    try:
        versions = get_modrinth_versions(project_id, mc_version)
        if not versions:
            return []
        version = versions[0]
        deps = version.get("dependencies", [])
        required = []
        for dep in deps:
            if dep.get("dependency_type") == "required":
                required.append({
                    "project_id": dep.get("project_id"),
                    "version_id": dep.get("version_id"),
                    "file_name": dep.get("file_name", "unknown"),
                })
        return required
    except Exception as e:
        log(f"get_mod_dependencies error: {e}", "ERROR")
        return []


def install_mod_from_modrinth(instance_name, project_id, mc_version, _visited=None, mod_loader=None):
    if _visited is None:
        _visited = set()
    if project_id in _visited:
        return True, "Уже установлен"
    _visited.add(project_id)

    try:
        if mod_loader is None:
            try:
                with open(instance_config_path(instance_name), "r", encoding="utf-8") as f:
                    mod_loader = json.load(f).get("mod_loader", "vanilla")
            except Exception:
                mod_loader = "vanilla"
        loader_filter = mod_loader if mod_loader in {"fabric", "forge", "neoforge", "quilt"} else None
        versions = get_modrinth_versions(project_id, mc_version, loader_filter)
        if not versions:
            return False, f"Нет версии для MC {mc_version}"

        version = versions[0]
        files = version.get("files", [])
        primary = None
        for f in files:
            if f.get("primary") and f["filename"].endswith(".jar"):
                primary = f
                break
        if not primary:
            for f in files:
                if f["filename"].endswith(".jar"):
                    primary = f
                    break
        if not primary:
            return False, "JAR не найден"

        deps = version.get("dependencies", [])
        required_deps = [d for d in deps if d.get("dependency_type") == "required"]
        log(f"Dependencies of {project_id}: {len(required_deps)} required")

        for dep in required_deps:
            dep_project_id = dep.get("project_id")
            if not dep_project_id:
                continue
            dep_ok, dep_result = install_mod_from_modrinth(
                instance_name, dep_project_id, mc_version, _visited, mod_loader
            )
            if not dep_ok:
                return False, f"Не удалось установить зависимость {dep_project_id}: {dep_result}"

        mods_dir = os.path.join(instance_minecraft_dir(instance_name), "mods")
        os.makedirs(mods_dir, exist_ok=True)
        filename = os.path.basename(str(primary.get("filename", "")))
        if not filename.lower().endswith(".jar") or filename in {".", "..", ""}:
            return False, "Некорректное имя JAR"
        filepath = os.path.join(mods_dir, filename)
        if os.path.isfile(filepath) and os.path.getsize(filepath) > 1024:
            log(f"Mod already present: {filename}")
            return True, f"{filename} (уже установлен)"
        fd, tmp = tempfile.mkstemp(prefix=".mod_", suffix=".part", dir=mods_dir)
        os.close(fd)
        try:
            r = http_get(primary["url"], timeout=60, stream=True)
            r.raise_for_status()
            total = 0
            with open(tmp, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        total += len(chunk)
            if total <= 0:
                raise IOError("Сервер вернул пустой файл")
            os.replace(tmp, filepath)
        finally:
            if os.path.exists(tmp):
                try: os.remove(tmp)
                except OSError: pass

        log(f"Mod installed: {filename}")
        return True, filename
    except Exception as e:
        log(f"Install mod error: {e}", "ERROR")
        return False, str(e)


def download_mod_icon(icon_url):
    if not icon_url:
        return None
    try:
        headers = {"User-Agent": USER_AGENT}
        r = http_get(icon_url, timeout=10)
        r.raise_for_status()
        img = Image.open(io.BytesIO(r.content)).convert("RGBA")
        return img
    except Exception as e:
        log(f"Icon download error: {e}", "WARN")
        return None



# ============ РЕЗЕРВНЫЕ КОПИИ / МОДПАКИ / ДИАГНОСТИКА ============

def _safe_zip_extract(zf, destination):
    """Распаковывает ZIP без path traversal."""
    destination = os.path.abspath(destination)
    for member in zf.infolist():
        target = os.path.abspath(os.path.join(destination, member.filename))
        if os.path.commonpath([destination, target]) != destination:
            raise ValueError(f"Опасный путь в архиве: {member.filename}")
    zf.extractall(destination)


def create_instance_archive(instance_name, output_path, modpack=False):
    """Создаёт backup или переносимый modpack экземпляра."""
    name = safe_instance_name(instance_name)
    root = os.path.abspath(instance_path(name))
    if not os.path.isdir(root):
        raise FileNotFoundError("Экземпляр не найден")

    cfg = {}
    try:
        with open(instance_config_path(name), "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        pass

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        manifest = {
            "format": "craftlauncher-modpack" if modpack else "craftlauncher-backup",
            "format_version": 1,
            "created": datetime.now().isoformat(timespec="seconds"),
            "instance": cfg,
        }
        z.writestr("craftlauncher.json",
                   json.dumps(manifest, ensure_ascii=False, indent=2))
        for base, dirs, files in os.walk(root):
            # Не переносим временные файлы и логи лаунчера.
            dirs[:] = [d for d in dirs if d not in {"__pycache__"}]
            for fn in files:
                if fn.endswith(".part") or fn.endswith(".tmp"):
                    continue
                full = os.path.join(base, fn)
                rel = os.path.relpath(full, root)
                if modpack and rel.lower() in {"instance.json"}:
                    continue
                z.write(full, rel)

    return output_path


def import_instance_archive(archive_path, requested_name=None):
    """Импортирует backup/modpack как новый экземпляр."""
    with zipfile.ZipFile(archive_path, "r") as z:
        if z.testzip() is not None:
            raise ValueError("Архив повреждён")
        manifest = {}
        try:
            manifest = json.loads(z.read("craftlauncher.json").decode("utf-8"))
        except Exception:
            pass

        old_cfg = manifest.get("instance", {}) if isinstance(manifest, dict) else {}
        old_name = str(old_cfg.get("name", "Imported")).strip() or "Imported"
        name = safe_instance_name(requested_name or old_name)
        if os.path.exists(instance_path(name)):
            base = name
            for i in range(2, 1000):
                candidate = f"{base} ({i})"
                try:
                    candidate = safe_instance_name(candidate)
                except ValueError:
                    continue
                if not os.path.exists(instance_path(candidate)):
                    name = candidate
                    break
            else:
                raise FileExistsError("Не удалось подобрать свободное имя")

        target = instance_path(name)
        os.makedirs(target, exist_ok=True)
        _safe_zip_extract(z, target)

    cfg_path = instance_config_path(name)
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            cfg = dict(old_cfg)
    else:
        cfg = dict(old_cfg)

    cfg["name"] = name
    cfg.setdefault("version", "1.20.1")
    cfg.setdefault("launch_version", cfg["version"])
    cfg.setdefault("mod_loader", "vanilla")
    cfg.setdefault("ram", 4096)
    save_instance_config(name, cfg)
    return name


def build_diagnostics(instance_name=None):
    """Возвращает диагностический отчёт без секретов."""
    report = [
        f"CraftLauncher {APP_VERSION_LABEL}",
        f"OS: {platform.platform()}",
        f"Python: {platform.python_version()}",
        f"Architecture: {platform.machine()}",
        f"Launcher directory: {LAUNCHER_DIR}",
    ]
    for java in discover_java_runtimes():
        report.append(f"Java {java.get('major', '?')}: {java.get('path', '')}")
    if instance_name:
        try:
            name = safe_instance_name(instance_name)
            cfg = {}
            with open(instance_config_path(name), "r", encoding="utf-8") as f:
                cfg = json.load(f)
            mc = cfg.get("version", "?")
            launch = cfg.get("launch_version", mc)
            report += [
                f"Instance: {name}",
                f"Minecraft: {mc}",
                f"Launch version: {launch}",
                f"Loader: {cfg.get('mod_loader', 'vanilla')}",
                f"RAM: {cfg.get('ram', '?')} MB",
                f"Installed version files: {'OK' if is_version_installed(name, launch) else 'MISSING'}",
            ]
            mods_dir = os.path.join(instance_minecraft_dir(name), "mods")
            mods = [f for f in os.listdir(mods_dir) if f.lower().endswith(".jar")] if os.path.isdir(mods_dir) else []
            report.append(f"Mods: {len(mods)}")
        except Exception as e:
            report.append(f"Instance diagnostics error: {e}")
    return "\n".join(report)


def save_diagnostics(instance_name=None):
    path = os.path.join(LAUNCHER_DIR, f"diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    os.makedirs(LAUNCHER_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_diagnostics(instance_name))
        f.write("\n\n--- launcher.log ---\n")
        try:
            with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as logf:
                f.write(logf.read()[-50000:])
        except Exception:
            pass
    return path


def check_instance_integrity(instance_name):
    """Проверяет конфиг, Minecraft version и моды; возвращает список проблем."""
    problems = []
    name = safe_instance_name(instance_name)
    if not os.path.isdir(instance_path(name)):
        return ["Папка экземпляра отсутствует"]
    try:
        with open(instance_config_path(name), "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception as e:
        return [f"Повреждён instance.json: {e}"]

    version = cfg.get("launch_version") or cfg.get("version")
    if not version:
        problems.append("Не указана версия Minecraft")
    elif not is_version_installed(name, version):
        problems.append(f"Minecraft {version} не установлен полностью")

    mc_dir = instance_minecraft_dir(name)
    if not os.path.isdir(mc_dir):
        problems.append("Папка .minecraft отсутствует")
    if cfg.get("mod_loader") in {"fabric", "forge", "neoforge", "quilt"} and version:
        if not os.path.isdir(os.path.join(mc_dir, "versions", version)):
            problems.append(f"Файлы загрузчика {version} не найдены")

    mods_dir = os.path.join(mc_dir, "mods")
    if os.path.isdir(mods_dir):
        for fn in os.listdir(mods_dir):
            full = os.path.join(mods_dir, fn)
            if fn.endswith((".part", ".tmp")):
                problems.append(f"Остался временный файл: {fn}")
            elif fn.lower().endswith(".jar"):
                try:
                    if os.path.getsize(full) < 1024:
                        problems.append(f"Повреждённый/пустой мод: {fn}")
                except OSError:
                    problems.append(f"Не удалось проверить мод: {fn}")
    return problems


class ToolsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Инструменты CraftLauncher")
        self.geometry("650x620")
        self.minsize(600, 520)
        self.grab_set()
        set_icon(self)

        ctk.CTkLabel(self, text="🛠 Инструменты",
                     font=("Arial", 21, "bold"),
                     text_color="#4CAF50").pack(pady=(18, 4))
        ctk.CTkLabel(self,
                     text="Резервные копии, перенос модпаков и диагностика",
                     font=("Arial", 10), text_color="gray").pack(pady=(0, 12))

        self.instance_var = ctk.StringVar()
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=25, pady=5)
        ctk.CTkLabel(row, text="Экземпляр:", width=100, anchor="w").pack(side="left")
        names = list_instances()
        self.instance_menu = ctk.CTkOptionMenu(
            row, variable=self.instance_var,
            values=names or ["Нет экземпляров"], width=360)
        self.instance_menu.pack(side="left", fill="x", expand=True)
        if names:
            self.instance_var.set(names[0])

        self.status = ctk.CTkLabel(self, text="", text_color="gray",
                                   wraplength=570, justify="left")
        self.status.pack(fill="x", padx=25, pady=8)

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.pack(fill="x", padx=25, pady=5)
        buttons = [
            ("💾 Backup", self.backup),
            ("📦 Экспорт модпака", self.export_modpack),
            ("📥 Импорт", self.import_archive),
            ("🔧 Проверить", self.check),
            ("🩺 Диагностика", self.diagnostics),
            ("📄 Лог", self.open_log),
        ]
        for text, cmd in buttons:
            ctk.CTkButton(actions, text=text, height=38,
                          command=cmd, fg_color="#3a3a3a",
                          hover_color="#4a4a4a").pack(fill="x", pady=4)

        ctk.CTkButton(self, text="Закрыть", height=38,
                      command=self.destroy, fg_color="#4CAF50",
                      hover_color="#3d8b40").pack(fill="x", padx=25, pady=15)

    def selected(self):
        value = self.instance_var.get()
        return None if value == "Нет экземпляров" else value

    def backup(self):
        name = self.selected()
        if not name:
            return
        path = filedialog.asksaveasfilename(
            title="Сохранить backup",
            defaultextension=".zip",
            filetypes=[("ZIP архив", "*.zip")],
            initialfile=f"{name}_backup.zip")
        if not path:
            return
        try:
            create_instance_archive(name, path, False)
            self.status.configure(text=f"✅ Backup сохранён:\n{path}", text_color="#4CAF50")
        except Exception as e:
            self.status.configure(text=f"❌ {e}", text_color="#e74c3c")

    def export_modpack(self):
        name = self.selected()
        if not name:
            return
        path = filedialog.asksaveasfilename(
            title="Экспортировать модпак",
            defaultextension=".zip",
            filetypes=[("CraftLauncher modpack", "*.zip")],
            initialfile=f"{name}_modpack.zip")
        if not path:
            return
        try:
            create_instance_archive(name, path, True)
            self.status.configure(text=f"✅ Модпак экспортирован:\n{path}", text_color="#4CAF50")
        except Exception as e:
            self.status.configure(text=f"❌ {e}", text_color="#e74c3c")

    def import_archive(self):
        path = filedialog.askopenfilename(
            title="Импортировать backup/modpack",
            filetypes=[("ZIP архив", "*.zip")])
        if not path:
            return
        try:
            name = import_instance_archive(path)
            self.parent.refresh_instances()
            self.status.configure(text=f"✅ Импортирован экземпляр: {name}",
                                  text_color="#4CAF50")
            names = list_instances()
            self.instance_menu.configure(values=names or ["Нет экземпляров"])
            if names:
                self.instance_var.set(name)
        except Exception as e:
            log(f"Import archive error: {e}", "ERROR")
            self.status.configure(text=f"❌ Импорт не удался: {e}",
                                  text_color="#e74c3c")

    def check(self):
        name = self.selected()
        if not name:
            return
        problems = check_instance_integrity(name)
        if problems:
            self.status.configure(
                text="⚠ Найдены проблемы:\n• " + "\n• ".join(problems),
                text_color="#f39c12")
        else:
            self.status.configure(text="✅ Экземпляр выглядит исправным.",
                                  text_color="#4CAF50")

    def diagnostics(self):
        path = save_diagnostics(self.selected())
        self.status.configure(text=f"✅ Диагностика сохранена:\n{path}",
                              text_color="#4CAF50")

    def open_log(self):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        if not os.path.exists(LOG_FILE):
            Path(LOG_FILE).touch()
        open_path(LOG_FILE)


# ============ ЗАГРУЗЧИКИ МОДОВ ============
def get_available_loader_versions(loader_id, mc_version):
    """Возвращает версии loader, совместимые с конкретной версией Minecraft."""
    try:
        if hasattr(minecraft_launcher_lib, "mod_loader"):
            loader = minecraft_launcher_lib.mod_loader.get_mod_loader(loader_id)
            try:
                return list(loader.get_loader_versions(mc_version, True) or [])
            except TypeError:
                return list(loader.get_loader_versions(mc_version) or [])
        if loader_id == "forge":
            versions = minecraft_launcher_lib.forge.list_forge_versions()
            prefix = f"{mc_version}-"
            return sorted([v for v in versions if v.startswith(prefix)],
                          key=version_sort_key, reverse=True)
        if loader_id == "fabric":
            versions = minecraft_launcher_lib.fabric.get_all_loader_versions()
            return [v["version"] if isinstance(v, dict) else v for v in versions]
        if loader_id == "neoforge":
            return get_neoforge_versions(mc_version)
    except Exception as e:
        log(f"get_available_loader_versions: {e}", "ERROR")
    return []


NEOFORGE_MAVEN_METADATA = "https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml"

def neoforge_version_prefix(mc_version):
    parsed = parse_mc_version(mc_version)
    if not parsed or parsed < (1, 20, 2):
        return None
    return f"{parsed[1]}.{parsed[2]}."

def get_neoforge_versions(mc_version):
    prefix = neoforge_version_prefix(mc_version)
    if not prefix:
        return []
    try:
        r = http_get(NEOFORGE_MAVEN_METADATA, timeout=15)
        r.raise_for_status()
        values = re.findall(r"<version>([^<]+)</version>", r.text)
        return sorted([v for v in values if v.startswith(prefix)], key=version_sort_key, reverse=True)
    except Exception as e:
        log(f"NeoForge versions error: {e}", "WARN")
        return []

def neoforge_installer_url(version):
    return f"https://maven.neoforged.net/releases/net/neoforged/neoforge/{urllib.parse.quote(version)}/neoforge-{urllib.parse.quote(version)}-installer.jar"

def install_neoforge(instance_name, mc_version, loader_version, java_path, status):
    if parse_mc_version(mc_version) < (1, 20, 2):
        return False, "NeoForge поддерживается начиная с Minecraft 1.20.2"
    if not loader_version:
        versions = get_neoforge_versions(mc_version)
        if not versions:
            return False, f"NeoForge не найден для Minecraft {mc_version}"
        loader_version = versions[0]
    mc_dir = instance_minecraft_dir(instance_name)
    os.makedirs(mc_dir, exist_ok=True)
    installer = os.path.join(mc_dir, f".neoforge-installer-{loader_version}.jar")
    tmp = installer + ".part"
    status(f"Загрузка NeoForge {loader_version}...")
    try:
        r = http_get(neoforge_installer_url(loader_version), timeout=60, stream=True)
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1024 * 64):
                if chunk: f.write(chunk)
        os.replace(tmp, installer)
        status("Установка NeoForge...")
        result = subprocess.run([java_path, "-jar", installer, "--install-client", mc_dir], cwd=mc_dir,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                encoding="utf-8", errors="replace", timeout=300, **run_subprocess_kwargs())
        output = result.stdout or ""
        log(f"NeoForge installer output: {output[-4000:]}")
        if result.returncode != 0:
            return False, f"Установщик NeoForge завершился с кодом {result.returncode}"
        # NeoForge creates a version directory; prefer the generated ID.
        versions_dir = os.path.join(mc_dir, "versions")
        candidates = []
        if os.path.isdir(versions_dir):
            for entry in os.listdir(versions_dir):
                if entry.lower().startswith("neoforge-"):
                    candidates.append(entry)
        installed_id = sorted(candidates, key=version_sort_key, reverse=True)[0] if candidates else f"neoforge-{loader_version}"
        status(f"NeoForge установлен: {installed_id}")
        return True, installed_id
    except Exception as e:
        log(f"NeoForge install error: {e}\n{traceback.format_exc()}", "ERROR")
        return False, str(e)
    finally:
        for path in (tmp, installer):
            if os.path.exists(path):
                try: os.remove(path)
                except OSError: pass


def install_loader_to_instance(instance_name, loader_id, mc_version,
                               loader_version=None, status_callback=None,
                               forge_mode="auto"):
    mc_dir = instance_minecraft_dir(instance_name)

    def status(msg):
        log(f"[loader] {msg}")
        if status_callback:
            try:
                status_callback(msg)
            except Exception:
                pass

    try:
        status(f"Проверка ванильной версии {mc_version}...")
        minecraft_launcher_lib.install.install_minecraft_version(
            mc_version, mc_dir,
            callback={"setStatus": lambda s: status(s[:60])}
        )

        if loader_id == "forge":
            if not loader_version:
                available = get_available_loader_versions("forge", mc_version)
                if not available:
                    return False, f"Forge не поддерживает MC {mc_version}"
                loader_version = available[0]

            status(f"Найден Forge: {loader_version}")

            if forge_mode == "official":
                status("Запуск официального установщика Forge...")
                try:
                    minecraft_launcher_lib.forge.run_forge_installer(loader_version)
                    return False, "Официальный установщик запущен. Заверши установку в нём."
                except Exception as e:
                    log(f"run_forge_installer error: {e}", "ERROR")
                    return False, f"Ошибка запуска: {e}"

            try:
                supports_auto = minecraft_launcher_lib.forge.supports_automatic_install(
                    loader_version
                )
            except Exception:
                supports_auto = False

            if not supports_auto:
                try:
                    minecraft_launcher_lib.forge.run_forge_installer(loader_version)
                    return False, "Этот Forge требует ручной установки. Установщик запущен."
                except Exception as e:
                    log(f"run_forge_installer error: {e}", "ERROR")
                    return False, f"Ошибка запуска установщика: {e}"

            status("Автоматическая установка Forge...")
            minecraft_launcher_lib.forge.install_forge_version(
                loader_version, mc_dir,
                callback={"setStatus": lambda s: status(s[:60])}
            )

            try:
                installed_id = minecraft_launcher_lib.forge.forge_to_installed_version(
                    loader_version
                )
            except Exception:
                installed_id = loader_version

            status(f"✅ Forge установлен: {installed_id}")
            return True, installed_id

        if loader_id == "fabric":
            if hasattr(minecraft_launcher_lib, "mod_loader"):
                loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
                if not loader_version:
                    compatible = loader.get_loader_versions(mc_version, True)
                    if not compatible:
                        return False, f"Fabric не поддерживает MC {mc_version}"
                    first = compatible[0]
                    loader_version = first.get("version") if isinstance(first, dict) else first
                status(f"Установка Fabric {loader_version}...")
                installed_id = loader.install(
                    mc_version, mc_dir, loader_version=loader_version,
                    callback={"setStatus": lambda s: status(s[:60])}
                )
            else:
                if not loader_version:
                    loader_version = minecraft_launcher_lib.fabric.get_latest_loader_version()
                status(f"Установка Fabric {loader_version}...")
                minecraft_launcher_lib.fabric.install_fabric(
                    mc_version, mc_dir, loader_version=loader_version,
                    callback={"setStatus": lambda s: status(s[:60])}
                )
                installed_id = f"fabric-loader-{loader_version}-{mc_version}"

            status(f"✅ Fabric установлен: {installed_id}")
            return True, installed_id

        if loader_id == "neoforge":
            java_path, _, warning = choose_java_for_version(mc_version)
            if not java_path:
                return False, warning or "Для NeoForge не найдена Java"
            if warning:
                status(warning)
            return install_neoforge(instance_name, mc_version, loader_version, java_path, status)

        return False, f"Неизвестный загрузчик: {loader_id}"

    except Exception as e:
        log(f"install_loader_to_instance error: {e}", "ERROR")
        status(f"❌ Ошибка: {str(e)[:80]}")
        return False, str(e)


# ============ УТИЛИТЫ ============
def version_sort_key(v):
    nums = re.findall(r'\d+', v)
    if not nums:
        return (0,)
    return tuple(int(n) for n in nums)


def sort_versions(versions):
    return sorted(versions, key=version_sort_key, reverse=True)


def set_icon(window):
    if os.path.exists(ICON_PATH):
        try:
            window.iconbitmap(ICON_PATH)
        except Exception:
            pass


def download_authlib():
    if os.path.exists(AUTHLIB_JAR):
        return True
    try:
        log("Downloading authlib-injector.jar...")
        urllib.request.urlretrieve(AUTHLIB_URL, AUTHLIB_JAR)
        return True
    except Exception as e:
        log(f"authlib download: {e}", "ERROR")
        return False


def load_skin_image(nickname):
    if not nickname:
        return None
    try:
        url = ELY_SKIN_URL.format(nickname=nickname)
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                img = Image.open(io.BytesIO(response.read()))
                return img.convert("RGBA")
    except Exception:
        pass
    return None


def crop_head_from_skin(img):
    try:
        w, h = img.size
        if w >= 64 and h >= 64:
            head = img.crop((8, 8, 16, 16))
            try:
                overlay = img.crop((40, 8, 48, 16))
                head = Image.alpha_composite(head.convert("RGBA"), overlay.convert("RGBA"))
            except Exception:
                pass
            return head.resize((64, 64), Image.NEAREST)
        else:
            size = min(w, h)
            return img.crop((0, 0, size, size)).resize((64, 64), Image.NEAREST)
    except Exception:
        return img.resize((64, 64), Image.LANCZOS)


def load_config():
    defaults = {
        "nickname": "Steve", "appearance": "dark", "language": "ru", "theme_name": "dark",
        "auto_launch_after_install": True, "show_console": True,
        "window_geometry": "1100x740+100+100", "last_server_ip": "", "servers": [],
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            if isinstance(cfg, dict):
                for k, v in cfg.items():
                    if k not in {"ely_token", "ely_uuid", "ely_username"}:
                        defaults[k] = v
        except Exception as e:
            log(f"Config read error: {e}", "WARN")
    return defaults

def save_config(cfg):
    try:
        clean = dict(cfg or {})
        for key in ("ely_token", "ely_uuid", "ely_username"):
            clean.pop(key, None)
        atomic_json_write(CONFIG_FILE, clean)
    except Exception as e:
        log(f"Config save error: {e}", "ERROR")


# ============ ЭКЗЕМПЛЯРЫ ============
def instance_path(name):
    return os.path.join(INSTANCES_DIR, safe_instance_name(name))

def instance_minecraft_dir(name):
    return os.path.join(instance_path(name), ".minecraft")

def instance_config_path(name):
    return os.path.join(instance_path(name), "instance.json")

def instance_profiles_path(name):
    return os.path.join(instance_path(name), "profiles.json")

def load_instance_profiles(name):
    name = safe_instance_name(name)
    path = instance_profiles_path(name)
    default = {"default": {"nickname": "Steve", "ram": 2048, "java_path": "", "jvm_args": []}, "active": "default"}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("profiles.json должен быть объектом")
    except Exception:
        data = default
    data.setdefault("active", "default")
    if not isinstance(data.get("profiles"), dict):
        profiles = {k: v for k, v in data.items() if k != "active" and isinstance(v, dict)}
        if not profiles:
            profiles = default.copy()
        data = {"active": data.get("active", "default"), "profiles": profiles}
    data.setdefault("profiles", {})
    data["profiles"].setdefault("default", default["default"])
    if data["active"] not in data["profiles"]:
        data["active"] = "default"
    return data

def save_instance_profiles(name, data):
    name = safe_instance_name(name)
    payload = data if isinstance(data, dict) else {}
    atomic_json_write(instance_profiles_path(name), payload)

def get_active_profile(name):
    data = load_instance_profiles(name)
    profile = dict(data["profiles"].get(data.get("active", "default"), {}))
    profile["name"] = data.get("active", "default")
    return profile

def is_version_installed(instance_name, version, _seen=None):
    """Return True only when the version has the files required to launch.

    A previous check incorrectly treated any version JSON containing ``libraries``
    as installed. That is not enough for vanilla versions: the client JAR must
    actually exist. This caused errors such as ``ClassNotFoundException: ...Main``
    when a stale JSON file remained after an interrupted download. Loader versions
    may inherit the vanilla client, so their parent is checked recursively.
    """
    try:
        version = str(version or "").strip()
        if not version or os.path.basename(version) != version:
            return False
        _seen = set() if _seen is None else _seen
        if version in _seen:
            return False
        _seen.add(version)

        version_dir = os.path.join(instance_minecraft_dir(instance_name), "versions", version)
        metadata = os.path.join(version_dir, f"{version}.json")
        jar = os.path.join(version_dir, f"{version}.jar")
        if not (os.path.isfile(metadata) and os.path.getsize(metadata) > 20):
            return False
        with open(metadata, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or data.get("id") != version:
            return False

        # Vanilla and standalone versions must contain their client/server JAR.
        if os.path.isfile(jar) and os.path.getsize(jar) > 1024:
            return True

        # Fabric/Forge/NeoForge profiles commonly inherit the vanilla client.
        # Their own JAR can be absent, but the inherited parent must be valid.
        parent = str(data.get("inheritsFrom") or "").strip()
        if parent:
            return is_version_installed(instance_name, parent, _seen)

        return False
    except (ValueError, OSError, json.JSONDecodeError):
        return False

def list_instances():
    result = []
    if not os.path.isdir(INSTANCES_DIR):
        return result
    for name in os.listdir(INSTANCES_DIR):
        try:
            if os.path.isdir(os.path.join(INSTANCES_DIR, name)) and os.path.isfile(instance_config_path(name)):
                with open(instance_config_path(name), "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    data.setdefault("name", name)
                    result.append(data)
        except Exception as e:
            log(f"Cannot read instance {name}: {e}", "WARN")
    return result

def create_instance(name, version, ram=2048, mod_loader="vanilla", launch_version=None):
    name = safe_instance_name(name)
    version = str(version or "").strip()
    if not version or os.path.basename(version) != version:
        raise ValueError("Недопустимая версия Minecraft")
    os.makedirs(instance_minecraft_dir(name), exist_ok=True)
    data = {
        "name": name,
        "version": version,
        "launch_version": launch_version or version,
        "mod_loader": mod_loader or "vanilla",
        "ram": max(512, int(ram)),
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    atomic_json_write(instance_config_path(name), data)
    save_instance_profiles(name, {"active": "default", "profiles": {
        "default": {"nickname": "Steve", "ram": max(512, int(ram)), "java_path": "", "jvm_args": []}
    }})
    return data

def save_instance_config(name, data):
    name = safe_instance_name(name)
    payload = dict(data or {})
    payload["name"] = name
    atomic_json_write(instance_config_path(name), payload)

def delete_instance(name):
    name = safe_instance_name(name)
    path = os.path.abspath(instance_path(name))
    root = os.path.abspath(INSTANCES_DIR)
    if os.path.commonpath([path, root]) != root or path == root:
        raise ValueError("Недопустимый путь экземпляра")
    if os.path.islink(path):
        os.unlink(path)
        return True
    if os.path.isdir(path):
        shutil.rmtree(path)
        return True
    return False

class ModsWindow(ctk.CTkToplevel):
    def __init__(self, parent, instance_name, mc_version):
        super().__init__(parent)
        self.parent = parent
        self.instance_name = instance_name
        self.mc_version = mc_version
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)

        self.title(f"Моды для {instance_name}")
        self.geometry("820x850")
        self.minsize(760, 640)

        self.installed_mods = set()
        self._icon_refs = []

        # Заголовок
        ctk.CTkLabel(self, text="🧩  Мод-браузер",
                     font=("Arial", 22, "bold"),
                     text_color="#4CAF50").pack(pady=(20, 3))
        ctk.CTkLabel(self, text=f"Экземпляр: {instance_name}  ·  Minecraft {mc_version}",
                     font=("Arial", 11), text_color="gray").pack(pady=(0, 15))

        # === ПОИСК + ФИЛЬТР ===
        search_row = ctk.CTkFrame(self, fg_color="transparent")
        search_row.pack(fill="x", padx=25, pady=(0, 5))

        ctk.CTkLabel(search_row, text="🔍",
                     font=("Arial", 16)).pack(side="left", padx=(0, 5))
        self.search_entry = ctk.CTkEntry(
            search_row, height=38, font=("Arial", 13),
            placeholder_text="Название мода (оставь пусто — покажет популярные)")
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<Return>", lambda e: self.search())

        self.search_btn = ctk.CTkButton(
            search_row, text="Найти", width=100, height=38,
            font=("Arial", 12, "bold"),
            fg_color="#4CAF50", hover_color="#3d8b40",
            command=self.search)
        self.search_btn.pack(side="left", padx=(8, 0))

        # === ФИЛЬТРЫ ===
        filter_row = ctk.CTkFrame(self, fg_color="transparent")
        filter_row.pack(fill="x", padx=25, pady=(5, 10))

        ctk.CTkLabel(filter_row, text="Категория:",
                     font=("Arial", 11), text_color="gray").pack(side="left", padx=(0, 5))

        self.category_var = ctk.StringVar(value=CATEGORY_LABELS["Все категории"])
        category_values = [CATEGORY_LABELS[c] for c in MODRINTH_CATEGORIES]
        self.category_menu = ctk.CTkOptionMenu(
            filter_row, variable=self.category_var,
            values=category_values, width=220, height=32,
            font=("Arial", 11),
            command=lambda _: self.search()
        )
        self.category_menu.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(filter_row, text="Сортировка:",
                     font=("Arial", 11), text_color="gray").pack(side="left", padx=(0, 5))

        self.sort_var = ctk.StringVar(value="📥 По популярности")
        self.sort_menu = ctk.CTkOptionMenu(
            filter_row, variable=self.sort_var,
            values=["📥 По популярности", "🆕 Новые", "🔥 Обновлённые", "🎯 По релевантности"],
            width=180, height=32, font=("Arial", 11),
            command=lambda _: self.search()
        )
        self.sort_menu.pack(side="left")

        # Статус
        self.status_label = ctk.CTkLabel(
            self, text="Введи название или выбери категорию",
            font=("Arial", 11), text_color="gray")
        self.status_label.pack(pady=(5, 10))

        # Список
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color=("gray90", "gray15"),
            width=770, height=580)
        self.scroll.pack(padx=25, pady=(0, 15), fill="both", expand=True)

        # Кнопки внизу
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(pady=(0, 15), fill="x", padx=25)

        ctk.CTkButton(bottom_frame, text="📂 Открыть папку модов", height=36,
                      font=("Arial", 12), fg_color="#555", hover_color="#333",
                      command=self.open_mods_folder).pack(side="left", expand=True,
                                                            fill="x", padx=(0, 5))
        ctk.CTkButton(bottom_frame, text="🔄 Обновить", height=36,
                      font=("Arial", 12), fg_color="#555", hover_color="#333",
                      command=self.refresh_installed).pack(side="left", expand=True,
                                                             fill="x", padx=(0, 5))
        ctk.CTkButton(bottom_frame, text="Закрыть", height=36,
                      font=("Arial", 12), fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.destroy).pack(side="left", expand=True,
                                                  fill="x", padx=(5, 0))

        self.refresh_installed()

        # Автозагрузка популярных при открытии
        self.after(300, self.load_popular)

    def open_mods_folder(self):
        mods_dir = os.path.join(instance_minecraft_dir(self.instance_name), "mods")
        os.makedirs(mods_dir, exist_ok=True)
        open_path(mods_dir)

    def refresh_installed(self):
        mods_dir = os.path.join(instance_minecraft_dir(self.instance_name), "mods")
        self.installed_mods = set()
        if os.path.exists(mods_dir):
            for f in os.listdir(mods_dir):
                if f.endswith(".jar"):
                    self.installed_mods.add(f.lower())
        self.status_label.configure(
            text=f"Установлено модов: {len(self.installed_mods)}",
            text_color="#4CAF50")

    def load_popular(self):
        """Загружает популярные моды при открытии"""
        self.search_entry.delete(0, "end")
        self.do_search(query="")

    def search(self):
        query = self.search_entry.get().strip()
        self.do_search(query=query)

    def do_search(self, query=""):
        # Определяем категорию
        cat_label = self.category_var.get()
        category = CATEGORY_LABELS_REVERSE.get(cat_label, "Все категории")

        # Определяем сортировку
        sort_label = self.sort_var.get()
        sort_map = {
            "📥 По популярности": "downloads",
            "🆕 Новые": "newest",
            "🔥 Обновлённые": "updated",
            "🎯 По релевантности": "relevance",
        }
        index = sort_map.get(sort_label, "downloads")

        # UI
        self.search_btn.configure(state="disabled", text="Поиск...")
        info = f"«{query}»" if query else "популярные"
        if category != "Все категории":
            info += f" · {CATEGORY_LABELS.get(category, category)}"
        self.status_label.configure(text=f"Загрузка {info}...", text_color="#f39c12")

        # Очистка
        for w in self.scroll.winfo_children():
            w.destroy()
        self._icon_refs.clear()

        def do():
            results = search_modrinth_mods_advanced(
                query=query,
                mc_version=self.mc_version,
                category=category,
                limit=20,
                index=index
            )
            self.after(0, lambda r=results: self.render_results(r, query, category))

        threading.Thread(target=do, daemon=True).start()

    def render_results(self, results, query, category):
        self.search_btn.configure(state="normal", text="Найти")

        if not results:
            info = f"«{query}»" if query else "популярные моды"
            if category != "Все категории":
                info += f" в категории {CATEGORY_LABELS.get(category, category)}"
            self.status_label.configure(text=f"Ничего не найдено: {info}",
                                         text_color="#e74c3c")
            ctk.CTkLabel(self.scroll,
                         text=f"🔍 Ничего не найдено\n\n{info}\n\n"
                              f"Попробуй другую категорию или версию MC",
                         font=("Arial", 12), text_color="gray",
                         justify="center").pack(pady=50)
            return

        info = f"«{query}»" if query else "популярные"
        if category != "Все категории":
            info += f" · {CATEGORY_LABELS.get(category, category)}"
        self.status_label.configure(
            text=f"Найдено: {len(results)} модов ({info})",
            text_color="#4CAF50")

        for mod in results:
            self.create_mod_card(mod)

    def create_mod_card(self, mod):
        card = ctk.CTkFrame(self.scroll, fg_color=("gray80", "gray20"),
                            corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)

        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=12, pady=(10, 3))

        icon_label = ctk.CTkLabel(
            top_row, text="🧩", width=64, height=64,
            fg_color=("gray70", "gray25"), corner_radius=8,
            font=("Arial", 28), text_color="gray")
        icon_label.pack(side="left", padx=(0, 12))

        icon_url = mod.get("icon_url")
        if icon_url:
            def load_icon(url=icon_url, lbl=icon_label):
                img = download_mod_icon(url)
                if img:
                    self.after(0, lambda: self._apply_icon(lbl, img))
            threading.Thread(target=load_icon, daemon=True).start()

        info_col = ctk.CTkFrame(top_row, fg_color="transparent")
        info_col.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(info_col, text=mod.get("title", "Unknown"),
                     font=("Arial", 14, "bold"),
                     text_color="#4CAF50", anchor="w").pack(fill="x")

        meta = ctk.CTkFrame(info_col, fg_color="transparent")
        meta.pack(fill="x", pady=(2, 3))

        ctk.CTkLabel(meta, text=f"👤 {mod.get('author', '?')}",
                     font=("Arial", 10),
                     text_color="gray").pack(side="left", padx=(0, 10))

        downloads = mod.get("downloads", 0)
        if downloads >= 1_000_000:
            dl_text = f"📥 {downloads / 1_000_000:.1f}M"
        elif downloads >= 1000:
            dl_text = f"📥 {downloads / 1000:.0f}K"
        else:
            dl_text = f"📥 {downloads}"

        ctk.CTkLabel(meta, text=dl_text, font=("Arial", 10),
                     text_color="gray").pack(side="left", padx=(0, 10))

        loaders = mod.get("categories", []) + mod.get("loaders", [])
        loaders_text = ", ".join([l for l in loaders
                                   if l in ["forge", "fabric", "quilt", "neoforge"]])
        if loaders_text:
            ctk.CTkLabel(meta, text=f"⚙ {loaders_text}",
                         font=("Arial", 10),
                         text_color="gray").pack(side="left")

        # Категории
        cats = mod.get("categories", [])
        interesting_cats = [c for c in cats if c in MODRINTH_CATEGORIES]
        if interesting_cats:
            cat_text = " · ".join([CATEGORY_LABELS.get(c, c) for c in interesting_cats[:3]])
            ctk.CTkLabel(info_col, text=cat_text,
                         font=("Arial", 10),
                         text_color="#9b59b6",
                         anchor="w").pack(fill="x", pady=(0, 3))

        desc = mod.get("description", "Без описания")
        if len(desc) > 180:
            desc = desc[:177] + "..."
        ctk.CTkLabel(info_col, text=desc,
                     font=("Arial", 10), anchor="w", justify="left",
                     wraplength=460,
                     text_color=("black", "#d4d4d4")).pack(fill="x", pady=(0, 3))

        project_id = mod.get("project_id") or mod.get("slug")
        mod_slug = mod.get("slug", "mod")

        install_btn = ctk.CTkButton(
            info_col, text="📥 Установить", width=130, height=28,
            font=("Arial", 11, "bold"),
            fg_color="#4CAF50", hover_color="#3d8b40",
            command=lambda: self.install_mod(project_id, mod_slug, install_btn))
        install_btn.pack(anchor="e", pady=(3, 0))

    def _apply_icon(self, label, pil_image):
        try:
            w, h = pil_image.size
            size = min(w, h)
            left = (w - size) // 2
            top = (h - size) // 2
            cropped = pil_image.crop((left, top, left + size, top + size))
            cropped = cropped.resize((64, 64), Image.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=cropped, dark_image=cropped,
                                    size=(64, 64))
            label.configure(image=ctk_img, text="")
            self._icon_refs.append(ctk_img)
        except Exception as e:
            log(f"apply_icon error: {e}", "WARN")

    def install_mod(self, project_id, mod_slug, btn):
        btn.configure(state="disabled", text="⏳ Проверка...")
        self.status_label.configure(text=f"Проверка зависимостей {mod_slug}...",
                                     text_color="#f39c12")

        def do_install():
            deps = get_mod_dependencies(project_id, self.mc_version)
            if deps:
                log(f"{mod_slug} requires: {len(deps)} deps")

            self.after(0, lambda: btn.configure(text="⏳ Скачивание..."))
            self.after(0, lambda: self.status_label.configure(
                text=f"Скачивание {mod_slug} + {len(deps)} зависимостей...",
                text_color="#f39c12"))

            success, info = install_mod_from_modrinth(
                self.instance_name, project_id, self.mc_version)

            self.after(0, lambda: self.on_install_done(success, info, btn, deps))

        threading.Thread(target=do_install, daemon=True).start()

    def on_install_done(self, success, info, btn, deps=None):
        if success:
            btn.configure(text="✓ Установлен", fg_color="#2d5a2d",
                          state="disabled")
            if deps:
                dep_text = f" + {len(deps)} зависимостей"
            else:
                dep_text = ""
            self.status_label.configure(text=f"✓ {info}{dep_text}",
                                         text_color="#4CAF50")
            self.refresh_installed()
        else:
            btn.configure(text="❌ Ошибка", fg_color="#5a2a2a", state="normal")
            self.status_label.configure(text=f"❌ {info[:80]}",
                                         text_color="#e74c3c")



# ============ ЛОКАЛЬНЫЕ СЕРВЕРЫ ============

class ServerListWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Мои серверы")
        self.geometry("650x520")
        self.grab_set()
        set_icon(self)

        self.servers = self.parent.config_data.setdefault("servers", [])
        ctk.CTkLabel(self, text="🖥 Мои серверы",
                     font=("Arial", 20, "bold")).pack(pady=(18, 4))
        ctk.CTkLabel(self, text="Только твой локальный список — без каталога и рекламы.",
                     text_color="gray").pack(pady=(0, 10))

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=20, pady=10)
        ctk.CTkButton(self, text="➕ Добавить сервер", command=self.add_server,
                      fg_color="#4CAF50").pack(fill="x", padx=20, pady=5)
        ctk.CTkButton(self, text="Закрыть", command=self.destroy,
                      fg_color="#555").pack(fill="x", padx=20, pady=(0, 15))
        self.refresh()

    def refresh(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        for i, server in enumerate(self.servers):
            row = ctk.CTkFrame(self.scroll)
            row.pack(fill="x", pady=4)
            text = f"{server.get('name','Без названия')}  ·  {server.get('address','')}"
            ctk.CTkLabel(row, text=text, anchor="w").pack(side="left", fill="x", expand=True, padx=10, pady=8)
            ctk.CTkButton(row, text="📋", width=38,
                          command=lambda a=server.get("address",""): self.copy(a)).pack(side="right", padx=3)
            ctk.CTkButton(row, text="🗑", width=38, fg_color="#5a2a2a",
                          command=lambda x=i: self.remove(x)).pack(side="right", padx=3)

    def copy(self, value):
        self.clipboard_clear()
        self.clipboard_append(value)
        self.status("Адрес скопирован")

    def status(self, text):
        self.title(f"Мои серверы — {text}")

    def add_server(self):
        win = ctk.CTkToplevel(self)
        win.title("Добавить сервер")
        win.geometry("420x260")
        win.grab_set()
        name = ctk.CTkEntry(win, placeholder_text="Название")
        addr = ctk.CTkEntry(win, placeholder_text="IP:порт")
        name.pack(fill="x", padx=25, pady=(30,8))
        addr.pack(fill="x", padx=25, pady=8)
        def save():
            n, a = name.get().strip(), addr.get().strip()
            if not n or not a:
                messagebox.showwarning("Сервер", "Заполни название и адрес.")
                return
            self.servers.append({"name": n, "address": a})
            self.parent.config_data["servers"] = self.servers
            save_config(self.parent.config_data)
            self.refresh()
            win.destroy()
        ctk.CTkButton(win, text="Сохранить", command=save,
                      fg_color="#4CAF50").pack(fill="x", padx=25, pady=15)

    def remove(self, index):
        if 0 <= index < len(self.servers):
            self.servers.pop(index)
            self.parent.config_data["servers"] = self.servers
            save_config(self.parent.config_data)
            self.refresh()


# ============ СЕТЕВАЯ ИГРА ============
class NetworkWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Сетевая игра")
        self.geometry("560x680")
        self.resizable(False, False)
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)
        self.my_ip = None
        self.my_vpn = None

        ctk.CTkLabel(self, text="🌐  Сетевая игра",
                     font=("Arial", 22, "bold"),
                     text_color="#4CAF50").pack(pady=(20, 3))
        ctk.CTkLabel(self, text="Играй с друзьями через Radmin VPN / Hamachi",
                     font=("Arial", 11), text_color="gray").pack(pady=(0, 15))

        my_ip_section = ctk.CTkFrame(self, fg_color=("gray85", "gray20"),
                                      corner_radius=10)
        my_ip_section.pack(fill="x", padx=25, pady=(0, 12))
        ctk.CTkLabel(my_ip_section, text="📡 Твой IP",
                     font=("Arial", 14, "bold"),
                     text_color="#4CAF50").pack(pady=(12, 5))
        self.ip_label = ctk.CTkLabel(my_ip_section, text="⏳ Определение...",
                                      font=("Consolas", 18, "bold"),
                                      text_color="#f39c12")
        self.ip_label.pack(pady=(0, 5))
        self.vpn_label = ctk.CTkLabel(my_ip_section, text="",
                                       font=("Arial", 11), text_color="gray")
        self.vpn_label.pack(pady=(0, 8))
        ip_btns = ctk.CTkFrame(my_ip_section, fg_color="transparent")
        ip_btns.pack(pady=(0, 12))
        ctk.CTkButton(ip_btns, text="🔄 Обновить", width=130, height=32,
                      font=("Arial", 11), fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.refresh_ip).pack(side="left", padx=3)
        ctk.CTkButton(ip_btns, text="📋 Копировать", width=130, height=32,
                      font=("Arial", 11), fg_color="#555", hover_color="#333",
                      command=self.copy_ip).pack(side="left", padx=3)

        connect_section = ctk.CTkFrame(self, fg_color=("gray85", "gray20"),
                                        corner_radius=10)
        connect_section.pack(fill="x", padx=25, pady=(0, 12))
        ctk.CTkLabel(connect_section, text="🔗 Подключиться к другу",
                     font=("Arial", 14, "bold"),
                     text_color="#4CAF50").pack(pady=(12, 5))
        ctk.CTkLabel(connect_section, text="Введи IP друга:",
                     font=("Arial", 11), text_color="gray").pack(pady=(0, 5))
        ip_input_frame = ctk.CTkFrame(connect_section, fg_color="transparent")
        ip_input_frame.pack(fill="x", padx=15, pady=(0, 8))
        self.friend_ip_entry = ctk.CTkEntry(ip_input_frame, height=35,
                                             font=("Consolas", 13),
                                             placeholder_text="25.12.34.56")
        self.friend_ip_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        saved_ip = self.parent.config_data.get("last_server_ip", "")
        if saved_ip:
            self.friend_ip_entry.insert(0, saved_ip)
        ctk.CTkButton(ip_input_frame, text="📋", width=45, height=35,
                      font=("Arial", 14), fg_color="#555", hover_color="#333",
                      command=self.paste_ip).pack(side="left")
        ctk.CTkLabel(connect_section, text="Порт (по умолчанию 25565):",
                     font=("Arial", 11), text_color="gray").pack(pady=(5, 5))
        self.friend_port_entry = ctk.CTkEntry(connect_section, height=32,
                                               font=("Consolas", 12),
                                               placeholder_text="25565")
        self.friend_port_entry.insert(0, "25565")
        self.friend_port_entry.pack(fill="x", padx=15, pady=(0, 8))
        ctk.CTkButton(connect_section, text="🎮 Подключиться и играть",
                      height=40, font=("Arial", 13, "bold"),
                      fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.connect_to_friend).pack(fill="x", padx=15, pady=(5, 12))

        info_scroll = ctk.CTkScrollableFrame(self, fg_color=("gray90", "gray15"),
                                              width=510, height=200)
        info_scroll.pack(padx=25, pady=(0, 15), fill="both", expand=True)

        instructions = [
            ("📖 Как играть с друзьями", "bold"),
            ("", "normal"),
            ("1️⃣ Все устанавливают Radmin VPN или Hamachi", "normal"),
            ("   • Radmin VPN: https://www.radmin-vpn.com/", "gray"),
            ("   • Hamachi: https://vpn.net/", "gray"),
            ("", "normal"),
            ("2️⃣ Создайте общую сеть (имя + пароль)", "normal"),
            ("", "normal"),
            ("3️⃣ Проверьте IP в окне сверху", "normal"),
            ("", "normal"),
            ("4️⃣ Хост: Esc → «Открыть для сети»", "normal"),
            ("   • Запомните порт (например, 54321)", "gray"),
            ("   • Скопируйте свой IP кнопкой 📋", "gray"),
            ("", "normal"),
            ("5️⃣ Друзья вводят IP и порт → Подключиться", "normal"),
            ("", "normal"),
            ("⚠️ Все должны быть в одной сети VPN!", "warn"),
        ]

        for text, style in instructions:
            if style == "bold":
                ctk.CTkLabel(info_scroll, text=text, font=("Arial", 12, "bold"),
                             text_color="#4CAF50", anchor="w",
                             justify="left").pack(fill="x", padx=5, pady=(8, 2))
            elif style == "warn":
                ctk.CTkLabel(info_scroll, text=text, font=("Arial", 10),
                             text_color="#f39c12", anchor="w",
                             justify="left").pack(fill="x", padx=10, pady=1)
            elif style == "gray":
                ctk.CTkLabel(info_scroll, text=text, font=("Arial", 10),
                             text_color="gray", anchor="w",
                             justify="left").pack(fill="x", padx=10, pady=1)
            elif text == "":
                ctk.CTkLabel(info_scroll, text="", font=("Arial", 5)).pack(pady=2)
            else:
                ctk.CTkLabel(info_scroll, text=text, font=("Arial", 11),
                             anchor="w", justify="left").pack(fill="x", padx=5, pady=1)

        ctk.CTkButton(self, text="Закрыть", width=200, height=38,
                      font=("Arial", 12), fg_color="#555", hover_color="#333",
                      command=self.destroy).pack(pady=(0, 15))

        self.after(200, self.refresh_ip)

    def refresh_ip(self):
        self.ip_label.configure(text="⏳ Сканирую...", text_color="#f39c12")
        self.vpn_label.configure(text="")
        self.update()

        def scan():
            ip, vpn = get_vpn_ip()
            self.after(0, lambda: self.apply_ip(ip, vpn))

        threading.Thread(target=scan, daemon=True).start()

    def apply_ip(self, ip, vpn):
        self.my_ip = ip
        self.my_vpn = vpn
        if ip:
            self.ip_label.configure(text=ip, text_color="#4CAF50")
            self.vpn_label.configure(text=f"✓ {vpn}", text_color="#4CAF50")
        else:
            self.ip_label.configure(text="❌ Не найден", text_color="#e74c3c")
            self.vpn_label.configure(text="Radmin VPN / Hamachi не запущен",
                                      text_color="#e74c3c")

    def copy_ip(self):
        if self.my_ip:
            self.clipboard_clear()
            self.clipboard_append(self.my_ip)
            self.parent.set_status(f"IP скопирован: {self.my_ip}", "#4CAF50")

    def paste_ip(self):
        try:
            text = self.clipboard_get()
            self.friend_ip_entry.delete(0, "end")
            self.friend_ip_entry.insert(0, text.strip())
        except Exception:
            pass

    def connect_to_friend(self):
        ip = self.friend_ip_entry.get().strip()
        port = self.friend_port_entry.get().strip() or "25565"
        if not ip:
            self.parent.set_status("Введи IP друга", "#e74c3c")
            return
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            self.parent.set_status("Неверный формат IP", "#e74c3c")
            return
        try:
            pn = int(port)
            if pn < 1 or pn > 65535:
                raise ValueError
        except ValueError:
            self.parent.set_status("Неверный порт", "#e74c3c")
            return
        self.parent.config_data["last_server_ip"] = ip
        save_config(self.parent.config_data)
        self.parent.set_status(f"Подключение к {ip}:{port}...", "#4CAF50")
        self.parent.open_quick_connect(ip, port)
        self.destroy()


# ============ КОНСОЛЬ ============
class ConsoleWindow(ctk.CTkToplevel):
    def __init__(self, parent, instance_name):
        super().__init__(parent)
        self.title(f"Консоль — {instance_name}")
        self.geometry("900x600")
        self.minsize(700, 400)
        set_icon(self)
        self.log_lines = []
        self.process = None
        self.instance_name = instance_name

        header = ctk.CTkFrame(self, height=50, corner_radius=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=f"🖥  Консоль · {instance_name}",
                     font=("Consolas", 14, "bold"),
                     text_color="#4CAF50").pack(side="left", padx=15)
        self.status_label = ctk.CTkLabel(header, text="● Запуск...",
                                          font=("Arial", 12),
                                          text_color="#f39c12")
        self.status_label.pack(side="right", padx=15)

        btn_bar = ctk.CTkFrame(self, height=40, corner_radius=0,
                               fg_color=("gray85", "gray20"))
        btn_bar.pack(fill="x", side="top")
        btn_bar.pack_propagate(False)
        ctk.CTkButton(btn_bar, text="🗑 Очистить", width=110, height=30,
                      font=("Arial", 11), fg_color="#555", hover_color="#333",
                      command=self.clear_log).pack(side="left", padx=4, pady=5)
        ctk.CTkButton(btn_bar, text="💾 Сохранить", width=120, height=30,
                      font=("Arial", 11), fg_color="#555", hover_color="#333",
                      command=self.save_to_file).pack(side="left", padx=4, pady=5)
        ctk.CTkButton(btn_bar, text="📋 Копировать", width=120, height=30,
                      font=("Arial", 11), fg_color="#555", hover_color="#333",
                      command=self.copy_all).pack(side="left", padx=4, pady=5)
        ctk.CTkButton(btn_bar, text="📂 Папка экземпляра", width=160, height=30,
                      font=("Arial", 11), fg_color="#3a3a3a", hover_color="#4a4a4a",
                      command=self.open_instance_folder).pack(side="left", padx=4, pady=5)
        ctk.CTkButton(btn_bar, text="📦 Папка модов", width=140, height=30,
                      font=("Arial", 11), fg_color="#3a3a3a", hover_color="#4a4a4a",
                      command=self.open_mods_folder).pack(side="left", padx=4, pady=5)
        self.autoscroll_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(btn_bar, text="Автопрокрутка",
                        variable=self.autoscroll_var, font=("Arial", 11),
                        checkbox_width=18,
                        checkbox_height=18).pack(side="right", padx=15, pady=5)

        self.textbox = ctk.CTkTextbox(self, font=("Consolas", 11),
                                       fg_color=("#1e1e1e", "#0d0d0d"),
                                       text_color="#d4d4d4", wrap="word")
        self.textbox.pack(fill="both", expand=True, padx=10, pady=(10, 10))
        for tag, color in [("error", "#e74c3c"), ("warn", "#f39c12"),
                           ("info", "#4CAF50"), ("normal", "#d4d4d4"),
                           ("system", "#3498db")]:
            self.textbox.tag_config(tag, foreground=color)

        footer = ctk.CTkFrame(self, height=40, corner_radius=0,
                              fg_color=("gray85", "gray20"))
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        self.stats_label = ctk.CTkLabel(footer, text="Строк: 0",
                                         font=("Arial", 11), text_color="gray")
        self.stats_label.pack(side="left", padx=15, pady=5)
        ctk.CTkButton(footer, text="❌ Стоп", width=120, height=30,
                      font=("Arial", 11), fg_color="#5a2a2a", hover_color="#7a2020",
                      command=self.kill_process).pack(side="right", padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def append_log(self, line, level="normal"):
        try:
            if not self.winfo_exists():
                return
        except Exception:
            return
        self.log_lines.append(line)
        try:
            self.textbox.insert("end", line + "\n", level)
            if self.autoscroll_var.get():
                self.textbox.see("end")
            self.stats_label.configure(text=f"Строк: {len(self.log_lines)}")
        except Exception:
            pass

    def add_message(self, text, level="info"):
        prefixes = {"info": "ℹ ", "error": "✗ ", "warn": "⚠ ",
                    "ok": "✓ ", "system": "» "}
        prefix = prefixes.get(level, "")
        tag = level if level in ("error", "warn", "info") else (
            "system" if level == "system" else "normal")
        if level == "ok":
            tag = "info"
        self.append_log(f"{prefix}{text}", tag)

    def update_status(self, text, color="#f39c12"):
        try:
            if self.winfo_exists():
                self.status_label.configure(text=text, text_color=color)
        except Exception:
            pass

    def clear_log(self):
        self.textbox.delete("1.0", "end")
        self.log_lines.clear()
        self.stats_label.configure(text="Строк: 0")

    def save_to_file(self):
        from tkinter import filedialog
        path = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("All files", "*.*")],
            initialfile="minecraft_log.txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.log_lines))
            self.add_message(f"Лог сохранён: {path}", "ok")

    def copy_all(self):
        self.clipboard_clear()
        self.clipboard_append("\n".join(self.log_lines))
        self.add_message("Лог скопирован", "ok")

    def repair_selected(self):
        if not self.selected_instance:
            return
        name = self.selected_instance
        problems = check_instance_integrity(name)
        if not problems:
            self.set_status("✅ Проверка завершена: проблем не найдено.", "#4CAF50")
            return
        if not messagebox.askyesno("Восстановление",
                                   "Найдены проблемы:\n\n" + "\n".join("• " + x for x in problems) +
                                   "\n\nПопробовать переустановить Minecraft-файлы?"):
            return
        def work():
            try:
                cfg_path = instance_config_path(name)
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                version = cfg.get("version") or cfg.get("launch_version")
                if not version:
                    raise ValueError("Версия Minecraft не указана")
                self.after(0, lambda: self.set_status("🔧 Восстановление Minecraft...", "#f39c12"))
                minecraft_launcher_lib.install.install_minecraft_version(
                    version, instance_minecraft_dir(name),
                    callback={"setStatus": lambda x: None})
                loader = cfg.get("mod_loader", "vanilla")
                if loader != "vanilla":
                    self.after(0, lambda: self.set_status(f"🔧 Восстановление {loader.upper()}...", "#f39c12"))
                    ok, result = install_loader_to_instance(name, loader, version,
                                                            loader_version=None,
                                                            status_callback=lambda x: None)
                    if not ok:
                        raise RuntimeError(f"Не удалось восстановить {loader}: {result}")
                    cfg["launch_version"] = result
                    save_instance_config(name, cfg)
                self.after(0, lambda: self.set_status("✅ Minecraft и загрузчик восстановлены.", "#4CAF50"))
            except Exception as e:
                log(f"Repair error: {e}\n{traceback.format_exc()}", "ERROR")
                self.after(0, lambda err=str(e): self.set_status(f"❌ Ошибка восстановления: {err}", "#e74c3c"))
        threading.Thread(target=work, daemon=True).start()

    def open_instance_folder(self):
        mc_dir = instance_minecraft_dir(self.instance_name)
        if os.path.exists(mc_dir):
            open_path(mc_dir)

    def open_mods_folder(self):
        mods_path = os.path.join(instance_minecraft_dir(self.instance_name), "mods")
        os.makedirs(mods_path, exist_ok=True)
        open_path(mods_path)

    def kill_process(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.kill()
                self.add_message("Процесс убит", "warn")
                self.update_status("● Остановлено", "#e74c3c")
            except Exception as e:
                self.add_message(f"Ошибка: {e}", "error")

    def on_close(self):
        if self.process and self.process.poll() is None:
            result = messagebox.askyesno("Игра запущена",
                                          "Minecraft работает. Закрыть консоль?")
            if not result:
                return
        self.destroy()


# ============ ELY AUTH ============
class ElyAuthWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.title("Вход в Ely.by")
        self.geometry("440x500")
        self.resizable(False, False)
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)
        self.on_success = on_success
        self.twofa_needed = False

        ctk.CTkLabel(self, text="🔐 Вход в Ely.by",
                     font=("Arial", 22, "bold"),
                     text_color="#4CAF50").pack(pady=(25, 5))
        ctk.CTkLabel(self, text="Введите данные аккаунта Ely.by",
                     font=("Arial", 11), text_color="gray").pack(pady=(0, 25))

        ctk.CTkLabel(self, text="Логин (или E-mail):",
                     font=("Arial", 12), anchor="w").pack(fill="x", padx=40)
        self.login_entry = ctk.CTkEntry(self, width=360, height=35,
                                         font=("Arial", 13))
        self.login_entry.pack(pady=(5, 15))

        ctk.CTkLabel(self, text="Пароль:",
                     font=("Arial", 12), anchor="w").pack(fill="x", padx=40)
        self.pass_entry = ctk.CTkEntry(self, width=360, height=35,
                                        font=("Arial", 13), show="●")
        self.pass_entry.pack(pady=(5, 15))

        self.twofa_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctk.CTkLabel(self.twofa_frame, text="Код 2FA (из приложения):",
                     font=("Arial", 12), anchor="w").pack(fill="x")
        self.twofa_entry = ctk.CTkEntry(self.twofa_frame, width=360, height=35,
                                         font=("Consolas", 14),
                                         placeholder_text="123456")
        self.twofa_entry.pack(pady=(5, 5))

        self.error_label = ctk.CTkLabel(self, text="", text_color="#e74c3c",
                                         font=("Arial", 11), wraplength=360)
        self.error_label.pack(pady=(0, 10))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(5, 10))
        self.login_btn = ctk.CTkButton(btn_frame, text="Войти",
                                        width=170, height=40,
                                        font=("Arial", 13, "bold"),
                                        fg_color="#4CAF50", hover_color="#3d8b40",
                                        command=self.do_login)
        self.login_btn.pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Отмена", width=170, height=40,
                      font=("Arial", 13), fg_color="#555", hover_color="#333",
                      command=self.destroy).pack(side="left", padx=5)

        ctk.CTkLabel(self,
                     text="⚠ Сессия только пока лаунчер открыт",
                     font=("Arial", 10), text_color="#f39c12").pack(pady=(10, 0))

    def do_login(self):
        login = self.login_entry.get().strip()
        password = self.pass_entry.get()
        twofa = self.twofa_entry.get().strip() if self.twofa_needed else ""

        if not login or not password:
            self.error_label.configure(text="Заполни логин и пароль!")
            return
        if self.twofa_needed and not twofa:
            self.error_label.configure(text="Введи код 2FA!")
            return

        self.login_btn.configure(state="disabled", text="Вход...")
        self.error_label.configure(text="")

        def auth_thread():
            try:
                result = ely_authenticate(login, password, twofa)
                self.after(0, lambda r=result: self.handle_result(r))
            except Exception as e:
                self.after(0, lambda: self.error_label.configure(
                    text=f"Ошибка: {str(e)[:60]}"))

        threading.Thread(target=auth_thread, daemon=True).start()

    def handle_result(self, result):
        if result == "NEED_2FA":
            self.twofa_needed = True
            self.twofa_frame.pack(fill="x", padx=40, pady=(0, 15), before=self.error_label)
            self.error_label.configure(
                text="⚠ Включена 2FA. Введи код из приложения.",
                text_color="#f39c12"
            )
            self.login_btn.configure(state="normal", text="Войти")
            return

        if result and isinstance(result, dict):
            self.on_success(result)
            self.destroy()
        else:
            self.error_label.configure(text="Неверный логин, пароль или код 2FA.")
            self.login_btn.configure(state="normal", text="Войти")




# ============ ВЫБОР ВЕРСИИ ============
class VersionSelectWindow(ctk.CTkToplevel):
    def __init__(self, parent, vanilla_versions, current_version, on_selected):
        super().__init__(parent)
        self.title("Выбор версии")
        self.geometry("540x640")
        self.resizable(False, False)
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)
        self.vanilla_versions = vanilla_versions
        self.selected = current_version
        self.on_selected = on_selected

        ctk.CTkLabel(self, text="📋 Выбор версии Minecraft",
                     font=("Arial", 20, "bold"),
                     text_color="#4CAF50").pack(pady=(20, 15))

        sf = ctk.CTkFrame(self, fg_color="transparent")
        sf.pack(fill="x", padx=30, pady=(0, 10))
        ctk.CTkLabel(sf, text="🔍", font=("Arial", 16)).pack(side="left", padx=(0, 5))
        self.search_entry = ctk.CTkEntry(sf, height=35, font=("Arial", 13),
                                          placeholder_text="Поиск: например 1.16")
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda e: self.render_list())

        qf = ctk.CTkFrame(self, fg_color="transparent")
        qf.pack(fill="x", padx=30, pady=(0, 10))
        for v in ["Последняя", "1.20.1", "1.16.5", "1.12.2", "1.7.10"]:
            ctk.CTkButton(qf, text=v, width=88, height=30, font=("Arial", 11),
                          fg_color="#3a3a3a", hover_color="#4a4a4a",
                          command=lambda ver=v: self.quick_select(ver)).pack(side="left", padx=2)

        self.scroll = ctk.CTkScrollableFrame(self, width=460, height=380,
                                              fg_color=("gray90", "gray15"))
        self.scroll.pack(padx=30, pady=(0, 10), fill="both", expand=True)

        self.info_label = ctk.CTkLabel(self, text=f"Выбрано: {self.selected}",
                                        font=("Arial", 13, "bold"),
                                        text_color="#4CAF50")
        self.info_label.pack(pady=(0, 10))

        bf = ctk.CTkFrame(self, fg_color="transparent")
        bf.pack(pady=(0, 20))
        ctk.CTkButton(bf, text="✓ Выбрать", width=150, height=40,
                      font=("Arial", 13, "bold"), fg_color="#4CAF50",
                      hover_color="#3d8b40", command=self.confirm).pack(side="left", padx=5)
        ctk.CTkButton(bf, text="Отмена", width=150, height=40,
                      font=("Arial", 13), fg_color="#555", hover_color="#333",
                      command=self.destroy).pack(side="left", padx=5)

        self.render_list()

    def render_list(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        query = self.search_entry.get().strip().lower()
        versions = [v for v in self.vanilla_versions if query in v.lower()] if query else self.vanilla_versions
        if not versions:
            ctk.CTkLabel(self.scroll, text="Ничего не найдено 🔍",
                          font=("Arial", 12), text_color="gray").pack(pady=20)
            return
        for v in versions:
            ctk.CTkButton(self.scroll, text=v, width=420, height=32,
                          font=("Arial", 12), anchor="w",
                          fg_color="#4CAF50" if v == self.selected else "#2b2b2b",
                          hover_color="#3d8b40",
                          command=lambda ver=v: self.select_version(ver)).pack(pady=2, padx=5, fill="x")

    def quick_select(self, v):
        if v == "Последняя":
            if self.vanilla_versions:
                self.selected = self.vanilla_versions[0]
        elif v in self.vanilla_versions:
            self.selected = v
        else:
            return
        self.info_label.configure(text=f"Выбрано: {self.selected}")
        self.render_list()

    def select_version(self, v):
        self.selected = v
        self.info_label.configure(text=f"Выбрано: {v}")
        self.render_list()

    def confirm(self):
        self.on_selected(self.selected)
        self.destroy()


# ============ СОЗДАНИЕ ЭКЗЕМПЛЯРА ============
class CreateInstanceWindow(ctk.CTkToplevel):
    def __init__(self, parent, all_versions, on_created):
        super().__init__(parent)
        self.title("Создать экземпляр")
        self.geometry("440x620")
        self.resizable(False, False)
        self.on_created = on_created
        self.all_versions = all_versions
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)

        ctk.CTkLabel(self, text="➕ Новый экземпляр",
                     font=("Arial", 20, "bold"),
                     text_color="#4CAF50").pack(pady=(20, 15))

        ctk.CTkLabel(self, text="Название:", font=("Arial", 12),
                     anchor="w").pack(fill="x", padx=40)
        self.name_entry = ctk.CTkEntry(self, width=360, height=35,
                                        placeholder_text="Например: Моя выживалка")
        self.name_entry.pack(pady=(5, 12))

        ctk.CTkLabel(self, text="Версия Minecraft:",
                     font=("Arial", 12), anchor="w").pack(fill="x", padx=40)
        self.selected_version = all_versions[0] if all_versions else "1.20.1"
        vf = ctk.CTkFrame(self, fg_color="transparent")
        vf.pack(fill="x", padx=40, pady=(5, 12))
        self.version_btn = ctk.CTkButton(vf, text=f"📋 {self.selected_version}",
                                          width=250, height=35, font=("Arial", 12),
                                          fg_color="#2b2b2b", hover_color="#3a3a3a",
                                          command=self.open_version_select)
        self.version_btn.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(vf, text="🔍", width=50, height=35, font=("Arial", 14),
                      fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.open_version_select).pack(side="left", padx=(5, 0))

        ctk.CTkLabel(self, text="Загрузчик модов:",
                     font=("Arial", 12), anchor="w").pack(fill="x", padx=40)
        self.loader_var = ctk.StringVar(value="Vanilla (без модов)")
        ctk.CTkOptionMenu(
            self, variable=self.loader_var, width=360, height=35,
            font=("Arial", 12),
            values=["Vanilla (без модов)", "Forge", "Fabric", "NeoForge"]
        ).pack(pady=(5, 12))

        ctk.CTkLabel(self, text="Оперативная память (МБ):",
                     font=("Arial", 12), anchor="w").pack(fill="x", padx=40)
        rf = ctk.CTkFrame(self, fg_color="transparent")
        rf.pack(fill="x", padx=40, pady=(5, 0))
        steps = max(1, (RAM_MAX - RAM_MIN) // 256)
        self.ram_slider = ctk.CTkSlider(rf, from_=RAM_MIN, to=RAM_MAX,
                                         number_of_steps=steps,
                                         command=self.on_ram_change)
        default_ram = max(2048, (RAM_MAX // 2 // 256) * 256)
        self.ram_slider.set(default_ram)
        self.ram_slider.pack(side="left", fill="x", expand=True)
        self.ram_label = ctk.CTkLabel(rf, text=str(default_ram),
                                       font=("Arial", 12, "bold"),
                                       text_color="#4CAF50", width=60)
        self.ram_label.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(self, text=f"💡 Доступно: до {RAM_MAX} МБ",
                     font=("Arial", 10), text_color="gray").pack(pady=(3, 12))

        bf = ctk.CTkFrame(self, fg_color="transparent")
        bf.pack(pady=(5, 15))
        ctk.CTkButton(bf, text="Создать", width=150, height=40,
                      fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.create).pack(side="left", padx=5)
        ctk.CTkButton(bf, text="Отмена", width=150, height=40,
                      fg_color="#555", hover_color="#333",
                      command=self.destroy).pack(side="left", padx=5)
        self.error_label = ctk.CTkLabel(self, text="", text_color="#e74c3c",
                                         font=("Arial", 11))
        self.error_label.pack()

    def open_version_select(self):
        VersionSelectWindow(self, self.all_versions, self.selected_version,
                             self.on_version_selected)

    def on_version_selected(self, v):
        self.selected_version = v
        self.version_btn.configure(text=f"📋 {v}")

    def on_ram_change(self, value):
        val = int(value // 256 * 256)
        self.ram_slider.set(val)
        self.ram_label.configure(text=str(val))

    def create(self):
        name = self.name_entry.get().strip()
        version = self.selected_version
        ram = int(self.ram_slider.get())
        loader_display = self.loader_var.get()
        loader_map = {
            "Vanilla (без модов)": "vanilla",
            "Forge": "forge",
            "Fabric": "fabric",
            "NeoForge": "neoforge"
        }
        mod_loader = loader_map.get(loader_display, "vanilla")

        if not name:
            self.error_label.configure(text="Введи название!")
            return
        if os.path.exists(instance_path(name)):
            self.error_label.configure(text="Уже существует!")
            return
        bad = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        if any(c in name for c in bad):
            self.error_label.configure(text="Недопустимые символы!")
            return

        create_instance(name, version, ram, mod_loader)
        self.on_created()
        self.destroy()


# ============ РЕДАКТИРОВАНИЕ ЭКЗЕМПЛЯРА ============
class EditInstanceWindow(ctk.CTkToplevel):
    def __init__(self, parent, instance_name, on_saved):
        super().__init__(parent)
        self.parent = parent
        self.instance_name = instance_name
        self.on_saved = on_saved
        self.title("Настройки экземпляра")
        self.geometry("480x700")
        self.minsize(480, 550)
        self.resizable(False, True)
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)

        with open(instance_config_path(instance_name), "r", encoding="utf-8") as f:
            self.inst_data = json.load(f)
        self.inst_data.setdefault("ram", 2048)
        self.inst_data.setdefault("mod_loader", "vanilla")
        self.inst_data.setdefault("launch_version", self.inst_data.get("version", ""))

        ctk.CTkLabel(self, text=f"⚙ {instance_name}",
                     font=("Arial", 18, "bold"),
                     text_color="#4CAF50").pack(pady=(15, 3))
        ctk.CTkLabel(self, text=f"Версия: {self.inst_data['version']}",
                     font=("Arial", 11), text_color="gray").pack(pady=(0, 10))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", width=440)
        scroll.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # RAM
        ctk.CTkLabel(scroll, text="Оперативная память (МБ):",
                     font=("Arial", 12), anchor="w").pack(fill="x", pady=(5, 3))
        rf = ctk.CTkFrame(scroll, fg_color="transparent")
        rf.pack(fill="x", pady=(0, 15))
        steps = max(1, (RAM_MAX - RAM_MIN) // 256)
        self.ram_slider = ctk.CTkSlider(rf, from_=RAM_MIN, to=RAM_MAX,
                                         number_of_steps=steps,
                                         command=self.on_ram_change)
        saved_ram = max(min(self.inst_data["ram"], RAM_MAX), RAM_MIN)
        self.ram_slider.set(saved_ram)
        self.ram_slider.pack(side="left", fill="x", expand=True)
        self.ram_label = ctk.CTkLabel(rf, text=str(saved_ram),
                                       font=("Arial", 12, "bold"),
                                       text_color="#4CAF50", width=60)
        self.ram_label.pack(side="left", padx=(10, 0))

        # Загрузчик
        ctk.CTkLabel(scroll, text="⚙ Загрузчик модов:",
                     font=("Arial", 13, "bold"),
                     anchor="w", text_color="#4CAF50").pack(fill="x", pady=(10, 5))

        current_loader = self.inst_data.get("mod_loader", "vanilla")
        loader_map = {"vanilla": "Vanilla (без модов)",
                      "forge": "Forge", "fabric": "Fabric", "neoforge": "NeoForge"}
        self.loader_display = ctk.StringVar(
            value=loader_map.get(current_loader, "Vanilla (без модов)")
        )

        self.loader_menu = ctk.CTkOptionMenu(
            scroll, variable=self.loader_display, height=32,
            font=("Arial", 12),
            values=["Vanilla (без модов)", "Forge", "Fabric", "NeoForge"],
            command=self.on_loader_change
        )
        self.loader_menu.pack(fill="x", pady=(0, 5))

        current_launch = self.inst_data.get("launch_version", "")
        current_loader_id = self.inst_data.get("mod_loader", "vanilla")

        if current_loader_id == "vanilla":
            loader_info = "Ванильный Minecraft (без модов)"
            loader_color = "gray"
        else:
            loader_info = f"Активен: {current_loader_id.upper()} · ID: {current_launch}"
            loader_color = "#4CAF50"

        self.loader_status = ctk.CTkLabel(
            scroll, text=loader_info,
            font=("Arial", 10), text_color=loader_color,
            wraplength=400, justify="left"
        )
        self.loader_status.pack(fill="x", pady=(0, 8))

        self.install_loader_btn = ctk.CTkButton(
            scroll, text="📥 Установить выбранный загрузчик",
            height=36, font=("Arial", 11),
            fg_color="#4CAF50", hover_color="#3d8b40",
            command=self.install_loader
        )
        self.install_loader_btn.pack(fill="x", pady=(0, 5))

        self.install_progress = ctk.CTkProgressBar(scroll, height=6)
        self.install_progress.set(0)
        self.install_progress.pack(fill="x", pady=(0, 5))

        self.install_status_label = ctk.CTkLabel(
            scroll, text="",
            font=("Arial", 10), text_color="gray",
            wraplength=400, justify="left"
        )
        self.install_status_label.pack(fill="x", pady=(0, 15))

        bf = ctk.CTkFrame(self, fg_color="transparent")
        bf.pack(side="bottom", pady=15, fill="x", padx=20)
        ctk.CTkButton(bf, text="💾 Сохранить", height=38,
                      font=("Arial", 12), fg_color="#4CAF50",
                      hover_color="#3d8b40",
                      command=self.save).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(bf, text="Закрыть", height=38,
                      font=("Arial", 12), fg_color="#555", hover_color="#333",
                      command=self.destroy).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def on_ram_change(self, value):
        val = int(value // 256 * 256)
        self.ram_slider.set(val)
        self.ram_label.configure(text=str(val))

    def on_loader_change(self, choice):
        mapping = {
            "Vanilla (без модов)": "vanilla",
            "Forge": "forge",
            "Fabric": "fabric",
            "NeoForge": "neoforge"
        }
        loader_id = mapping.get(choice, "vanilla")

        if loader_id == "forge":
            self.loader_status.configure(
                text="⚠ Forge: для MC 1.12.2 нужна Java 8, для 1.17+ — Java 17",
                text_color="#f39c12"
            )
        elif loader_id == "fabric":
            self.loader_status.configure(
                text="⚠ Fabric: нужна Java 17 (1.20.1) или Java 21 (1.21)",
                text_color="#f39c12"
            )
        elif loader_id == "neoforge":
            self.loader_status.configure(
                text="NeoForge: Minecraft 1.20.2+ · требуется Java 17/21 по версии Minecraft",
                text_color="#f39c12"
            )
        else:
            self.loader_status.configure(
                text="Ванильный Minecraft (без модов)",
                text_color="gray"
            )

    def install_loader(self):
        display = self.loader_display.get()
        mapping = {
            "Vanilla (без модов)": "vanilla",
            "Forge": "forge",
            "Fabric": "fabric",
            "NeoForge": "neoforge"
        }
        loader_id = mapping.get(display, "vanilla")

        if loader_id == "vanilla":
            self.install_status_label.configure(
                text="Vanilla не требует установки", text_color="gray"
            )
            return

        mc_version = self.inst_data.get("version", "1.20.1")
        forge_mode = "auto"
        if loader_id == "forge":
            choice = messagebox.askyesnocancel(
                "⚙ Установка Forge",
                "Выбери способ установки Forge.\n\n"
                "Да — открыть официальный установщик.\n"
                "Нет — попробовать автоматическую установку.\n"
                "Отмена — отменить."
            )
            if choice is None:
                self.install_status_label.configure(
                    text="Установка отменена", text_color="gray"
                )
                return
            forge_mode = "official" if choice else "auto"

        self.install_loader_btn.configure(state="disabled", text="⏳ Установка...")
        self.install_status_label.configure(
            text="Начинаю установку...", text_color="#f39c12"
        )
        self.install_progress.set(0)

        def status_callback(msg):
            self.after(0, lambda: self.install_status_label.configure(
                text=msg[:100], text_color="#f39c12"
            ))

        def do_install():
            try:
                success, result = install_loader_to_instance(
                    self.instance_name, loader_id, mc_version,
                    status_callback=status_callback, forge_mode=forge_mode
                )
                if success:
                    self.inst_data["mod_loader"] = loader_id
                    self.inst_data["launch_version"] = result
                    save_instance_config(self.instance_name, self.inst_data)
                    self.after(0, lambda: self.install_status_label.configure(
                        text=f"✅ Установлено! ID: {result}",
                        text_color="#4CAF50"
                    ))
                    self.after(0, lambda: self.install_progress.set(1.0))
                    self.after(0, lambda: self.loader_status.configure(
                        text=f"Активен: {loader_id.upper()} · ID: {result}",
                        text_color="#4CAF50"
                    ))
                else:
                    self.after(0, lambda: self.install_status_label.configure(
                        text=f"⚠ {result}", text_color="#f39c12"
                    ))
                    self.after(0, lambda: self.install_progress.set(0))
            except Exception as e:
                log(f"install_loader error: {e}", "ERROR")
                self.after(0, lambda: self.install_status_label.configure(
                    text=f"❌ Ошибка: {str(e)[:80]}", text_color="#e74c3c"
                ))
            finally:
                self.after(0, lambda: self.install_loader_btn.configure(
                    state="normal", text="📥 Установить выбранный загрузчик"
                ))

        threading.Thread(target=do_install, daemon=True).start()

    def save(self):
        ram = int(self.ram_slider.get())
        self.inst_data["ram"] = ram
        save_instance_config(self.instance_name, self.inst_data)
        self.on_saved()
        self.destroy()


# ============ ПРОФИЛИ И CRASH ANALYZER ============
def find_latest_game_log(instance_name):
    """Find the newest useful Minecraft/CraftLauncher log, including our captured launch output."""
    mc_dir = instance_minecraft_dir(instance_name)
    candidates = []
    logs_dir = os.path.join(mc_dir, "logs")
    crash_dir = os.path.join(mc_dir, "crash-reports")
    roots = [(logs_dir, (".log", ".txt")), (crash_dir, (".log", ".txt"))]

    # Our own capture is important: some Minecraft/loader failures happen before
    # Log4j creates latest.log, so the console may be the only useful evidence.
    capture = os.path.join(mc_dir, "craftlauncher-last-run.log")
    if os.path.isfile(capture):
        try:
            candidates.append((os.path.getmtime(capture), capture))
        except OSError:
            pass

    for root, extensions in roots:
        if os.path.isdir(root):
            for fn in os.listdir(root):
                path = os.path.join(root, fn)
                if os.path.isfile(path) and fn.lower().endswith(extensions):
                    try:
                        candidates.append((os.path.getmtime(path), path))
                    except OSError:
                        pass
    return max(candidates, default=(0, None))[1]


def _extract_error_context(text):
    """Return concise exception/loader context from a Minecraft launch log."""
    lines = text.splitlines()
    hits = []
    seen = set()

    # Prefer the actual exception and its cause, not just generic 'ERROR' lines.
    patterns = [
        re.compile(r"\b(?:[A-Za-z_$][\w$]*\.)*(?:[A-Za-z_$][\w$]*(?:Exception|Error))(?::.*)?"),
        re.compile(r"^\s*Caused by:\s+.+", re.I),
        re.compile(r"^\s*(?:Error|ERROR|FATAL|Fatal):\s+.+", re.I),
    ]
    for idx, line in enumerate(lines):
        clean = line.strip()
        if not clean:
            continue
        if any(p.search(clean) for p in patterns):
            key = clean[:500]
            if key in seen:
                continue
            seen.add(key)
            context = []
            # Include the immediately following stack line when useful.
            if idx + 1 < len(lines) and lines[idx + 1].strip().startswith("at "):
                context.append(lines[idx + 1].strip())
            hits.append((clean[:500], context))
        if len(hits) >= 12:
            break
    return hits


def analyze_crash(instance_name, exit_code=None):
    path = find_latest_game_log(instance_name)
    if not path:
        summary = "Лог Minecraft не найден."
        if exit_code is not None:
            summary += f" Код выхода: {exit_code}."
        return {"path": None, "summary": summary, "details": []}

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()[-200000:]
    except Exception as e:
        return {"path": path, "summary": f"Не удалось прочитать лог: {e}", "details": []}

    low = text.lower()
    details = []
    if exit_code is not None:
        details.append(("Код выхода", str(exit_code)))

    # Exact, high-value failures first.
    if "classnotfoundexception: net.minecraft.client.main.main" in low:
        details.append(("Причина",
                        "Minecraft не нашёл основной класс клиента. Обычно это означает "
                        "отсутствующий/повреждённый клиентский JAR или неправильную установку версии. "
                        "Переустанови эту версию через ремонт."))
    elif "unsupportedclassversionerror" in low:
        details.append(("Причина", "Java не подходит по версии. Проверь Java Manager."))
    elif "outofmemoryerror" in low:
        details.append(("Причина", "Закончилась выделенная Java-память. Увеличь RAM профиля или убери тяжёлые моды."))
    elif "noclassdeffounderror" in low:
        details.append(("Причина", "Не найдена зависимость/библиотека. Проверь установку loader и зависимости модов."))
    elif "modloadingexception" in low or "modloadingfailed" in low:
        details.append(("Причина", "Ошибка загрузки мода. Проверь последние установленные/обновлённые моды."))
    elif "duplicateModsFoundException".lower() in low:
        details.append(("Причина", "Найдены дубликаты модов. Удали одну из копий."))
    elif "mixinapplyerror" in low:
        details.append(("Причина", "Ошибка Mixin: вероятна несовместимость мода с Minecraft/loader."))

    # Preserve the useful known markers from the previous analyzer.
    known = [
        ("MixinApplyError", "Ошибка Mixin: вероятна несовместимость мода с текущей версией Minecraft/loader."),
        ("NoClassDefFoundError", "Не найдена зависимость мода или библиотека."),
        ("ClassNotFoundException", "Не найден класс/зависимость. Проверь установку версии, моды и loader."),
        ("ModLoadingException", "Ошибка загрузки мода."),
        ("GLFW", "Ошибка графического слоя. Проверь драйвер видеокарты и параметры запуска."),
        ("java.lang.IllegalStateException", "Minecraft завершился с IllegalStateException; смотри контекст ниже."),
    ]
    existing_titles = {d[0] for d in details}
    for marker, explanation in known:
        if marker.lower() in low and marker not in existing_titles:
            details.append((marker, explanation))

    exceptions = _extract_error_context(text)
    if exceptions:
        details.append(("Исключения и причины",
                        "\n".join(item[0] for item in exceptions[:10])))

    mod_names = sorted(set(re.findall(r"[A-Za-z0-9_.-]+\.jar", text, re.I)))
    if mod_names:
        details.append(("Упомянутые JAR", ", ".join(mod_names[:30])))

    if not details:
        details.append(("Результат", "Известный шаблон ошибки не найден. Ниже сохранён полный вывод последнего запуска."))

    summary = next((d for title, d in details if title in ("Причина", "Исключения и причины", "Результат")),
                   "Minecraft завершился с ошибкой.")
    return {"path": path, "summary": summary, "details": details}

class ProfileManagerWindow(ctk.CTkToplevel):
    def __init__(self, parent, instance_name, on_changed):
        super().__init__(parent)
        self.parent = parent
        self.instance_name = instance_name
        self.on_changed = on_changed
        self.title(f"Профили · {instance_name}")
        self.geometry("520x620")
        self.resizable(False, False)
        self.grab_set(); self.after(100, self.lift); set_icon(self)
        self.data = load_instance_profiles(instance_name)
        self.current = self.data.get("active", "default")

        ctk.CTkLabel(self, text="👤 Профили запуска", font=("Arial", 20, "bold"), text_color="#4CAF50").pack(pady=(16, 4))
        ctk.CTkLabel(self, text="Отдельные RAM, Java, ник и JVM-параметры для этого экземпляра", font=("Arial", 10), text_color="gray").pack(pady=(0, 12))
        self.menu = ctk.CTkOptionMenu(self, values=list(self.data["profiles"].keys()), command=self.load_profile, width=430)
        self.menu.set(self.current); self.menu.pack(padx=30, fill="x", pady=5)
        row = ctk.CTkFrame(self, fg_color="transparent"); row.pack(fill="x", padx=30, pady=8)
        ctk.CTkButton(row, text="➕ Новый", command=self.new_profile, fg_color="#4CAF50").pack(side="left", expand=True, fill="x", padx=(0,4))
        ctk.CTkButton(row, text="🗑 Удалить", command=self.delete_profile, fg_color="#5a2a2a").pack(side="left", expand=True, fill="x", padx=(4,0))
        form = ctk.CTkFrame(self, fg_color="transparent"); form.pack(fill="x", padx=30, pady=8)
        ctk.CTkLabel(form, text="Никнейм").pack(anchor="w")
        self.nick = ctk.CTkEntry(form); self.nick.pack(fill="x", pady=(2,8))
        ctk.CTkLabel(form, text="RAM (МБ)").pack(anchor="w")
        self.ram = ctk.CTkEntry(form); self.ram.pack(fill="x", pady=(2,8))
        ctk.CTkLabel(form, text="Java (необязательно)").pack(anchor="w")
        jf=ctk.CTkFrame(form, fg_color="transparent"); jf.pack(fill="x", pady=(2,8))
        self.java = ctk.CTkEntry(jf); self.java.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(jf, text="📁", width=42, command=self.pick_java).pack(side="left", padx=(5,0))
        ctk.CTkLabel(form, text="Доп. JVM аргументы (через пробел)").pack(anchor="w")
        self.jvm = ctk.CTkEntry(form); self.jvm.pack(fill="x", pady=(2,8))
        self.status = ctk.CTkLabel(self, text="", text_color="gray", wraplength=450); self.status.pack(pady=5)
        ctk.CTkButton(self, text="💾 Сохранить профиль и выбрать", height=40, command=self.save, fg_color="#4CAF50").pack(fill="x", padx=30, pady=10)
        self.load_profile(self.current)

    def load_profile(self, name):
        self.current=name; p=self.data["profiles"].get(name,{})
        self.nick.delete(0,"end"); self.nick.insert(0,p.get("nickname","Steve"))
        self.ram.delete(0,"end"); self.ram.insert(0,str(p.get("ram",2048)))
        self.java.delete(0,"end"); self.java.insert(0,p.get("java_path",""))
        self.jvm.delete(0,"end"); self.jvm.insert(0," ".join(p.get("jvm_args",[])))

    def new_profile(self):
        name = ctk.CTkInputDialog(text="Название нового профиля:", title="Новый профиль").get_input()
        if not name: return
        name=name.strip()
        if not name or len(name)>40 or name in self.data["profiles"]:
            messagebox.showerror("Профиль", "Некорректное или уже существующее имя."); return
        self.data["profiles"][name]={"nickname":"Steve","ram":2048,"java_path":"","jvm_args":[]}
        self.menu.configure(values=list(self.data["profiles"].keys())); self.menu.set(name); self.load_profile(name)

    def delete_profile(self):
        if self.current == "default":
            messagebox.showinfo("Профиль", "Профиль default удалить нельзя."); return
        self.data["profiles"].pop(self.current,None); self.current="default"
        self.menu.configure(values=list(self.data["profiles"].keys())); self.menu.set("default"); self.load_profile("default")

    def pick_java(self):
        path=filedialog.askopenfilename(title="Выбери Java", filetypes=[("Java", "java.exe" if IS_WINDOWS else "java"),("Все файлы","*.*")])
        if path: self.java.delete(0,"end"); self.java.insert(0,java_executable(path) or path)

    def save(self):
        try: ram=max(512,int(self.ram.get()))
        except ValueError: messagebox.showerror("Профиль","RAM должна быть числом."); return
        jp=self.java.get().strip()
        if jp and (not java_executable(jp) or not java_major_version(jp)):
            messagebox.showerror("Профиль","Указанный Java executable не прошёл проверку."); return
        args=self.jvm.get().strip().split() if self.jvm.get().strip() else []
        self.data["active"]=self.current
        self.data["profiles"][self.current]={"nickname":self.nick.get().strip() or "Steve","ram":ram,"java_path":jp,"jvm_args":args}
        save_instance_profiles(self.instance_name,self.data); self.on_changed(); self.destroy()

class CrashAnalyzerWindow(ctk.CTkToplevel):
    def __init__(self,parent,instance_name):
        super().__init__(parent); self.title("🩺 Crash Analyzer"); self.geometry("700x620"); self.minsize(600,500); set_icon(self)
        ctk.CTkLabel(self,text=f"🩺 Анализ ошибок · {instance_name}",font=("Arial",20,"bold"),text_color="#4CAF50").pack(pady=(16,4))
        result=analyze_crash(instance_name, exit_code)
        ctk.CTkLabel(self,text=result["summary"],font=("Arial",12,"bold"),wraplength=630,justify="left").pack(fill="x",padx=25,pady=10)
        box=ctk.CTkTextbox(self,font=("Consolas",11)); box.pack(fill="both",expand=True,padx=25,pady=5)
        for title,detail in result["details"]: box.insert("end",f"[{title}]\n{detail}\n\n")
        if result["path"]: box.insert("end",f"Источник: {result['path']}\n")
        box.configure(state="disabled")
        ctk.CTkButton(self,text="📂 Открыть лог",command=lambda: open_path(result["path"]) if result["path"] else None,fg_color="#3a3a3a").pack(fill="x",padx=25,pady=(5,15))

# ============ НАСТРОЙКИ ============
class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Настройки")
        self.geometry("460x660")
        self.minsize(460, 520)
        self.resizable(False, True)
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)

        ctk.CTkLabel(self, text="⚙  Настройки",
                     font=("Arial", 20, "bold"),
                     text_color="#4CAF50").pack(pady=(15, 3))
        ctk.CTkLabel(self, text=f"CraftLauncher {APP_VERSION_LABEL}",
                     font=("Arial", 10), text_color="gray").pack(pady=(0, 10))

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", width=420)
        scroll.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        s1 = ctk.CTkFrame(scroll, fg_color="transparent")
        s1.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(s1, text="👤 Профиль", font=("Arial", 13, "bold"),
                     anchor="w").pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(s1, text="Никнейм офлайн режима:",
                     font=("Arial", 11), anchor="w").pack(fill="x")
        self.nick_entry = ctk.CTkEntry(s1, height=32, font=("Arial", 12))
        self.nick_entry.insert(0, self.parent.config_data.get("nickname", "Steve"))
        self.nick_entry.pack(fill="x", pady=(3, 0))

        s2 = ctk.CTkFrame(scroll, fg_color="transparent")
        s2.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(s2, text="🎨 Внешний вид", font=("Arial", 13, "bold"),
                     anchor="w").pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(s2, text="Тема оформления:",
                     font=("Arial", 11), anchor="w").pack(fill="x")
        self.theme_menu = ctk.CTkOptionMenu(s2, height=32, font=("Arial", 12),
                                             values=list(THEME_NAMES.values()),
                                             command=self.change_theme)
        current_theme = self.parent.config_data.get("theme_name", self.parent.config_data.get("appearance", "dark"))
        self.theme_menu.set(THEME_NAMES.get(current_theme, "Тёмная"))
        self.theme_menu.pack(fill="x", pady=(3, 0))

        ctk.CTkLabel(s2, text="Язык интерфейса:",
                     font=("Arial", 11), anchor="w").pack(fill="x", pady=(8, 0))
        self.language_menu = ctk.CTkOptionMenu(
            s2, height=32, font=("Arial", 12),
            values=list(LANGUAGE_NAMES.values()),
            command=self.change_language)
        current_lang = self.parent.config_data.get("language", "ru")
        self.language_menu.set(LANGUAGE_NAMES.get(current_lang, "Русский"))
        self.language_menu.pack(fill="x", pady=(3, 0))

        ctk.CTkLabel(s2, text="Фоновое изображение:",
                     font=("Arial", 11), anchor="w").pack(fill="x", pady=(8, 3))
        bf = ctk.CTkFrame(s2, fg_color="transparent")
        bf.pack(fill="x", pady=(0, 3))
        ctk.CTkButton(bf, text="📷 Выбрать", width=130, height=30,
                      font=("Arial", 11), fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.choose_background).pack(side="left", padx=(0, 5))
        ctk.CTkButton(bf, text="🔄 Сбросить", width=130, height=30,
                      font=("Arial", 11), fg_color="#555", hover_color="#333",
                      command=self.reset_background).pack(side="left")

        sb = ctk.CTkFrame(scroll, fg_color="transparent")
        sb.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(sb, text="⚡ Поведение", font=("Arial", 13, "bold"),
                     anchor="w").pack(fill="x", pady=(0, 5))
        self.auto_launch_var = ctk.BooleanVar(
            value=self.parent.config_data.get("auto_launch_after_install", True))
        ctk.CTkCheckBox(sb, text="Авто-запуск игры после установки",
                        variable=self.auto_launch_var, font=("Arial", 11),
                        checkbox_width=20, checkbox_height=20,
                        command=self.toggle_auto_launch).pack(fill="x", pady=(3, 8), anchor="w")
        self.show_console_var = ctk.BooleanVar(
            value=self.parent.config_data.get("show_console", True))
        ctk.CTkCheckBox(sb, text="Показывать консоль при запуске",
                        variable=self.show_console_var, font=("Arial", 11),
                        checkbox_width=20, checkbox_height=20,
                        command=self.toggle_show_console).pack(fill="x", pady=(0, 3), anchor="w")

        # Java
        sj = ctk.CTkFrame(scroll, fg_color="transparent")
        sj.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(sj, text="☕ Java", font=("Arial", 13, "bold"),
                     anchor="w").pack(fill="x", pady=(0, 5))
        java_path = self.parent.config_data.get("java_path", "")
        self.java_label = ctk.CTkLabel(
            sj,
            text=(f"Выбрана: {java_path}" if java_path else "Автоматический выбор Java"),
            font=("Arial", 10), text_color="gray",
            anchor="w", justify="left", wraplength=400
        )
        self.java_label.pack(fill="x", pady=(0, 5))
        jf = ctk.CTkFrame(sj, fg_color="transparent")
        jf.pack(fill="x")
        ctk.CTkButton(
            jf, text="☕ Java Manager", height=32,
            fg_color="#4CAF50", hover_color="#3d8b40",
            command=self.open_java_manager
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(
            jf, text="🔍 Проверить Java", height=32,
            fg_color="#4CAF50", hover_color="#3d8b40",
            command=self.detect_java
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(
            jf, text="📁 Выбрать", height=32,
            fg_color="#555", hover_color="#333",
            command=self.choose_java
        ).pack(side="left", fill="x", expand=True, padx=(5, 0))
        ctk.CTkButton(
            sj, text="↩ Автовыбор", height=30,
            fg_color="#444", hover_color="#333",
            command=self.reset_java
        ).pack(fill="x", pady=(5, 0))

        ss = ctk.CTkFrame(scroll, fg_color="transparent")
        ss.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(ss, text="💻 Система", font=("Arial", 13, "bold"),
                     anchor="w").pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(ss, text=f"Всего RAM: {RAM_TOTAL} МБ\n"
                              f"Максимум для Minecraft: {RAM_MAX} МБ\n\n"
                              f"⌨ F11 — на весь экран\n"
                              f"Esc — выйти из fullscreen",
                     font=("Arial", 11), text_color="#4CAF50",
                     justify="left").pack(fill="x")

        s3 = ctk.CTkFrame(scroll, fg_color="transparent")
        s3.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(s3, text="📁 Папки", font=("Arial", 13, "bold"),
                     anchor="w").pack(fill="x", pady=(0, 5))
        ctk.CTkButton(s3, text="📂 Открыть папку лаунчера", height=32,
                      font=("Arial", 11), fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.open_launcher_folder).pack(fill="x", pady=(0, 5))
        ctk.CTkButton(s3, text="📝 Открыть launcher.log", height=32,
                      font=("Arial", 11), fg_color="#555", hover_color="#333",
                      command=self.open_log_file).pack(fill="x", pady=(0, 5))
        ctk.CTkButton(s3, text="📂 Открыть папку экземпляров", height=32,
                      font=("Arial", 11), fg_color="#555", hover_color="#333",
                      command=self.open_instances_folder).pack(fill="x")

        bf2 = ctk.CTkFrame(self, fg_color="transparent")
        bf2.pack(side="bottom", pady=15, fill="x", padx=20)
        ctk.CTkButton(bf2, text="💾 Сохранить", height=38,
                      font=("Arial", 12), fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.save_and_close).pack(side="left", expand=True,
                                                          fill="x", padx=(0, 5))
        ctk.CTkButton(bf2, text="Закрыть", height=38,
                      font=("Arial", 12), fg_color="#555", hover_color="#333",
                      command=self.destroy).pack(side="left", expand=True,
                                                   fill="x", padx=(5, 0))

    def toggle_auto_launch(self):
        self.parent.config_data["auto_launch_after_install"] = self.auto_launch_var.get()
        save_config(self.parent.config_data)

    def toggle_show_console(self):
        self.parent.config_data["show_console"] = self.show_console_var.get()
        save_config(self.parent.config_data)

    def change_theme(self, choice):
        reverse = {v: k for k, v in THEME_NAMES.items()}
        theme = reverse.get(choice, choice if choice in THEME_NAMES else "dark")
        accent, hover = apply_launcher_theme(theme)
        self.parent.config_data["theme_name"] = theme
        self.parent.config_data["appearance"] = THEME_STYLES[theme][0]
        save_config(self.parent.config_data)
        self.parent.update_background()
        # Recolor the open launcher so the change is visible immediately.
        self._recolor_tree(self.parent, accent, hover)

    def _recolor_tree(self, widget, accent, hover):
        try:
            if isinstance(widget, ctk.CTkButton):
                widget.configure(fg_color=accent, hover_color=hover)
            elif isinstance(widget, ctk.CTkOptionMenu):
                widget.configure(button_color=accent, button_hover_color=hover)
            elif isinstance(widget, ctk.CTkProgressBar):
                widget.configure(progress_color=accent)
        except Exception:
            pass
        try:
            for child in widget.winfo_children():
                self._recolor_tree(child, accent, hover)
        except Exception:
            pass

    def change_language(self, choice):
        reverse = {v: k for k, v in LANGUAGE_NAMES.items()}
        lang = reverse.get(choice, choice if choice in LANGUAGE_NAMES else "ru")
        self.parent.config_data["language"] = lang
        save_config(self.parent.config_data)
        _translate_widget_tree(self, lang)
        _translate_widget_tree(self.parent, lang)
        # Rebuild Settings so all its labels are immediately shown in the new language.
        messagebox.showinfo("Language", "Language changed. Some existing windows will use the new language after reopening.")

    def open_java_manager(self):
        # Settings is modal. Release its grab while the child Java Manager is open,
        # otherwise Tk sends all mouse/keyboard input back to Settings.
        try:
            self.grab_release()
        except Exception:
            pass
        manager = JavaManagerWindow(self.parent, owner=self)
        manager.focus_force()

    def detect_java(self):
        runtimes = discover_java_runtimes()
        if not runtimes:
            self.java_label.configure(
                text="Java не найдена. Установи Java 8/17/21 и повтори проверку.",
                text_color="#e74c3c"
            )
            return
        lines = [f"Java {j['major']}: {j['path']}" for j in runtimes[:5]]
        configured = self.parent.config_data.get("java_path", "")
        self.java_label.configure(
            text=("Автовыбор:\n" + "\n".join(lines)) if not configured
                 else ("Выбрана: " + configured + "\n" + "\n".join(lines)),
            text_color="#4CAF50"
        )
        log("Java runtimes: " + "; ".join(f"{j['major']}={j['path']}" for j in runtimes))

    def choose_java(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="Выбери java executable",
            filetypes=[("Java executable", "java.exe" if IS_WINDOWS else "java"),
                       ("Все файлы", "*.*")]
        )
        if not path:
            return
        executable = java_executable(path)
        major = java_major_version(executable) if executable else None
        if not executable or not major:
            messagebox.showerror("Java", "Выбранный файл не похож на рабочую Java.")
            return
        self.parent.config_data["java_path"] = executable
        save_config(self.parent.config_data)
        self.java_label.configure(
            text=f"Выбрана Java {major}:\n{executable}",
            text_color="#4CAF50"
        )

    def reset_java(self):
        self.parent.config_data.pop("java_path", None)
        save_config(self.parent.config_data)
        self.java_label.configure(
            text="Автоматический выбор Java",
            text_color="gray"
        )

    def choose_background(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="Выбери фоновое изображение",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif"),
                       ("Все файлы", "*.*")])
        if not path:
            return
        try:
            img = Image.open(path)
            img.verify()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть:\n{e}")
            return
        self.parent.config_data["background"] = path
        save_config(self.parent.config_data)
        self.parent.update_background()
        self.parent.set_status("Фон установлен ✅", "#4CAF50")

    def reset_background(self):
        self.parent.config_data.pop("background", None)
        save_config(self.parent.config_data)
        self.parent.update_background()
        self.parent.set_status("Фон сброшен", "gray")

    def save_and_close(self):
        nickname = self.nick_entry.get().strip() or "Steve"
        self.parent.config_data["nickname"] = nickname
        self.parent.config_data["language"] = self.parent.config_data.get("language", "ru")
        self.parent.config_data["theme_name"] = self.parent.config_data.get("theme_name", "dark")
        save_config(self.parent.config_data)
        if not self.parent.ely_token:
            self.parent.nick_entry.configure(state="normal")
            self.parent.nick_entry.delete(0, "end")
            self.parent.nick_entry.insert(0, nickname)
        self.parent.set_status("Настройки сохранены ✅", "#4CAF50")
        self.destroy()

    def open_launcher_folder(self):
        open_path(LAUNCHER_DIR)

    def open_log_file(self):
        if os.path.exists(LOG_FILE):
            open_path(LOG_FILE)
        else:
            self.parent.set_status("Лог ещё не создан", "gray")

    def open_instances_folder(self):
        open_path(INSTANCES_DIR)


# ============ FAQ ============
class FAQWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("FAQ — Частые вопросы")
        self.geometry("620x680")
        self.resizable(False, False)
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)

        ctk.CTkLabel(self, text="❓  Частые вопросы",
                     font=("Arial", 22, "bold"),
                     text_color="#4CAF50").pack(pady=(20, 3))
        ctk.CTkLabel(self, text="FAQ — ответы на популярные вопросы",
                     font=("Arial", 11), text_color="gray").pack(pady=(0, 15))

        scroll = ctk.CTkScrollableFrame(self, width=560, height=550,
                                         fg_color=("gray90", "gray15"))
        scroll.pack(padx=25, pady=(0, 15), fill="both", expand=True)

        faq_items = [
            ("🔍 Как искать моды по категориям?",
             "1. Открой «🧩 Мод-браузер»\n"
             "2. Сверху есть фильтр «Категория»\n"
             "3. Выбери нужную:\n\n"
             "• 👻 Хоррор — страшные моды\n"
             "• ⚔ Снаряжение — оружие, броня\n"
             "• 🔮 Магия — магические моды\n"
             "• ⚡ Оптимизация — Sodium, Lithium\n"
             "• ⚙ Технологии — машины, механизмы\n"
             "• 🐉 Мобы — новые существа\n\n"
             "Оставь поиск пустым — покажет популярные!"),
            ("📥 Как сортировать моды?",
             "Справа от фильтра категорий есть\n"
             "«Сортировка»:\n\n"
             "• 📥 По популярности (по умолчанию)\n"
             "• 🆕 Новые\n"
             "• 🔥 Обновлённые\n"
             "• 🎯 По релевантности (для поиска)"),
            ("⚙ Почему Forge ставится не автоматически?",
             "Forge — небольшая команда. Их доход — реклама\n"
             "на официальной странице загрузки.\n\n"
             "Разработчики просят не автоматизировать установку.\n\n"
             "Мы уважаем их просьбу, но даём ТЕБЕ выбор:\n\n"
             "✅ Официальный установщик — поддержишь Forge\n"
             "❌ Автоустановка — быстро, но без поддержки"),
            ("⚙ Как установить Forge / Fabric?",
             "1. Создай экземпляр с нужной версией MC\n"
             "2. Запусти игру 1 раз (скачается ванилла)\n"
             "3. Открой настройки экземпляра (⚙ Настройки)\n"
             "4. В секции «Загрузчик модов» выбери Forge/Fabric\n"
             "5. Нажми «📥 Установить выбранный загрузчик»\n\n"
             "⚠ Для Forge 1.12.2 нужна Java 8\n"
             "⚠ Для Forge 1.17+ нужна Java 17\n"
             "⚠ Для Fabric нужна Java 17 или 21"),
            ("🧩 Как установить моды?",
             "1. Сначала установи загрузчик (Forge/Fabric)\n"
             "2. Выбери экземпляр\n"
             "3. Жми «🧩 Мод-браузер»\n"
             "4. Введи название или выбери категорию\n"
             "5. Жми «📥 Установить»\n\n"
             "Все обязательные зависимости\n"
             "скачаются АВТОМАТИЧЕСКИ!"),
            ("🌐 Как играть с друзьями?",
             "1. Все ставят Radmin VPN / Hamachi\n"
             "2. Создают общую сеть\n"
             "3. Жми «🌐 Сетевая игра»\n"
             "4. Хост: Esc → Открыть для сети\n"
             "5. Друзья вводят IP хоста"),
            ("📍 Где хранятся файлы?",
             "%APPDATA%\\.CraftLauncher\\\n\n"
             "⚙ Настройки → 📂 Открыть папку"),
            ("🎮 Не запускается Minecraft",
             "1. Проверь Java: cmd → java -version\n"
             "2. Открой консоль\n"
             "3. Увеличь RAM\n"
             "4. Посмотри launcher.log"),
            ("☕ Ошибка «Java не найдена»",
             "1. Скачай Java: java.com/download/\n"
             "2. Поставь галочку «Add to PATH»\n"
             "3. Перезапусти лаунчер\n\n"
             "MC 1.16.5- → Java 8\n"
             "MC 1.17-1.20.4 → Java 17\n"
             "MC 1.20.5+ → Java 21"),
            ("💾 Сколько RAM?",
             "• Ванилла: 2048-4096 МБ\n"
             "• С модами: 4096-8192 МБ"),
            ("☕ Какую Java использует лаунчер?",
             "Лаунчер автоматически ищет Java 8, 17 и 21.\n\n"
             "• MC 1.16.5 и ниже → Java 8\n"
             "• MC 1.17–1.20.4 → Java 17\n"
             "• MC 1.20.5+ → Java 21\n\n"
             "При необходимости открой «⚙ Настройки» → «☕ Java»\n"
             "и выбери собственный java.exe/java."),
            ("🐛 Лаунчер крашится",
             "1. Открой launcher.log\n"
             "2. Найди [ERROR]\n"
             "3. Создай Issue на GitHub"),
        ]

        for q, a in faq_items:
            ctk.CTkLabel(scroll, text=q, font=("Arial", 13, "bold"),
                         text_color="#4CAF50", anchor="w", justify="left",
                         wraplength=520).pack(fill="x", padx=10, pady=(12, 3))
            ctk.CTkLabel(scroll, text=a, font=("Arial", 11), anchor="w",
                         justify="left", wraplength=520).pack(fill="x", padx=20, pady=(0, 8))

        ctk.CTkButton(self, text="Закрыть", width=200, height=40,
                      font=("Arial", 13), fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.destroy).pack(pady=(0, 20))


# ============ CHANGELOG ============
class ChangelogWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Список обновлений")
        self.geometry("520x620")
        self.resizable(False, False)
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)

        ctk.CTkLabel(self, text="📋  Список обновлений",
                     font=("Arial", 22, "bold"),
                     text_color="#4CAF50").pack(pady=(20, 3))
        ctk.CTkLabel(self, text="CraftLauncher — история версий",
                     font=("Arial", 11), text_color="gray").pack(pady=(0, 15))

        scroll = ctk.CTkScrollableFrame(self, width=460, height=480,
                                         fg_color=("gray90", "gray15"))
        scroll.pack(padx=25, pady=(0, 15), fill="both", expand=True)

        changes = [
            ("v1.0.0", [
                "🚀 Финальный стабильный релиз CraftLauncher",
                "🌐 Добавлена локализация интерфейса: Русский, English, Deutsch, Українська",
                "🎨 Добавлены 6 тем оформления: Тёмная, Светлая, Midnight, Ocean, Purple, Forest",
                "⚙ Язык и тема настраиваются непосредственно в окне «Настройки» и сохраняются между запусками",
                "🛠 Финальная стабилизация лаунчера перед выпуском 1.0",
            ]),
            ("v0.99.9", [
                "🔎 Crash Analyzer получил полный вывод запуска и код завершения процесса",
                "🧩 Добавлен разбор Exception, Caused by, Java-ошибок и ошибок loader",
                "📄 Анализатор работает даже если Minecraft не успел создать latest.log",
            ]),
            ("v0.99.8", [
                "🐛 Исправлена проверка установленных версий Minecraft: одного JSON недостаточно без клиентского JAR",
                "🧩 Для Forge/Fabric/NeoForge проверяется наследуемая vanilla-версия",
                "🔧 Предотвращён запуск с ClassNotFoundException после неполной установки Minecraft",
            ]),
            ("v0.99.7", [
                "🟢 Центр состояния экземпляра: MC, loader, Java, RAM и локальная статистика",
                "🛡 Безопасный запуск без модов с автоматическим восстановлением",
                "📑 Дублирование экземпляров",
                "🔎 Проверка перед запуском",
                "📊 Локальная статистика запусков и крашей",
                "☕ Java Manager: поиск Java 8 / 17 / 21 и выбор собственного java.exe",
                "🎯 Java автоматически выбирается под версию Minecraft",
                "🧵 UI безопаснее обновляется из фоновых потоков",
                "⚙ Установка Forge больше не показывает Tkinter-диалоги из фонового потока",
                "🧩 Fabric устанавливается с совместимым loader для выбранной версии MC",
                "📦 Повторная установка уже скачанного мода пропускается",
                "🛡 Проверка экземпляров и удаление каталогов стали безопаснее",
                "📚 Обновлены FAQ и README",
            ]),
            ("v0.99", [
                "🔍 Фильтры категорий в мод-браузере",
                "👻 Хоррор (cursed), приключения, магия и др.",
                "📥 Автозагрузка популярных модов",
                "🎯 Сортировка: популярные / новые / обновлённые",
                "🏷 Показ категорий на карточках модов",
                "🎨 Русские названия категорий",
            ]),
            ("v0.98.1", [
                "🤝 Уважение к Forge: диалог выбора",
                "✅ Официальный установщик (поддержка)",
                "❌ Автоустановка (быстро)",
            ]),
            ("v0.98", [
                "⚙ Установщик загрузчиков в настройках",
                "🔧 Поддержка Forge и Fabric",
            ]),
            ("v0.97.2", [
                "🔓 Токены не сохраняются",
                "🐛 Убраны краши",
            ]),
            ("v0.97", [
                "🔒 2FA",
                "🚪 Выход со всех устройств",
            ]),
            ("v0.96", [
                "🔗 Проверка зависимостей",
                "📦 Рекурсивная установка",
            ]),
            ("v0.95", ["🖼 Иконки модов"]),
            ("v0.94", ["🧩 Modrinth"]),
            ("v0.93", ["🌐 Сетевая игра"]),
            ("v0.92", ["❓ FAQ"]),
            ("v0.9", ["🐛 Фикс консоли"]),
            ("v0.85", ["🎨 Ely.by"]),
            ("v0.8", ["🖥 Консоль"]),
            ("v0.7", ["📋 Выбор версии"]),
            ("v0.5", ["🧠 Авто RAM"]),
            ("v0.4", ["💾 RAM-слайдер"]),
            ("v0.3", ["⚙ Настройки"]),
            ("v0.2", ["📦 Экземпляры"]),
            ("v0.1", ["🎉 Первая версия"]),
        ]

        for v, items in changes:
            h = ctk.CTkFrame(scroll, fg_color="transparent")
            h.pack(fill="x", pady=(10, 5))
            ctk.CTkLabel(h, text=f"━━━ {v} ━━━", font=("Arial", 14, "bold"),
                         text_color="#4CAF50").pack()
            for item in items:
                ctk.CTkLabel(scroll, text=f"  {item}", font=("Arial", 11),
                             anchor="w", justify="left",
                             wraplength=420).pack(fill="x", padx=10, pady=1)

        ctk.CTkButton(self, text="Закрыть", width=200, height=40,
                      font=("Arial", 13), fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.destroy).pack(pady=(0, 20))


# ============ О ЛАУНЧЕРЕ ============
class AboutWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("О лаунчере")
        self.geometry("420x560")
        self.resizable(False, False)
        self.grab_set()
        self.after(100, self.lift)
        set_icon(self)

        ctk.CTkLabel(self, text="⛏", font=("Arial", 60),
                     text_color="#4CAF50").pack(pady=(25, 5))
        ctk.CTkLabel(self, text="CraftLauncher",
                     font=("Arial", 24, "bold"),
                     text_color="#4CAF50").pack()
        ctk.CTkLabel(self, text=f"Stable {APP_VERSION_LABEL}",
                     font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x", padx=40, pady=(0, 15))

        items = [
            ("📦 Версия", f"Beta {APP_VERSION_LABEL}"),
            ("🐍 Python", "3.x"),
            ("📚 Библиотека", "minecraft-launcher-lib"),
            ("🎨 Скины", "Ely.by"),
            ("🌐 Сеть", "Radmin / Hamachi"),
            ("🧩 Моды", "Modrinth + Фильтры"),
            ("⚙ Загрузчики", "Forge (с выбором) + Fabric"),
            ("💾 RAM", f"{RAM_TOTAL} МБ"),
        ]

        for label, value in items:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=label, font=("Arial", 11),
                         anchor="w", width=140).pack(side="left")
            ctk.CTkLabel(row, text=value, font=("Arial", 11, "bold"),
                         text_color="#4CAF50", anchor="w",
                         wraplength=220, justify="left").pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(self, text="Самодельный лаунчер Minecraft.\n"
                                "Создан в учебных целях. 🎓\n\n"
                                "F11 — на весь экран",
                     font=("Arial", 11), text_color="gray",
                     justify="center").pack(pady=(15, 20))

        bf = ctk.CTkFrame(self, fg_color="transparent")
        bf.pack(side="bottom", pady=20)
        ctk.CTkButton(bf, text="📂 Папка лаунчера", width=170, height=38,
                      font=("Arial", 12), fg_color="#555", hover_color="#333",
                      command=lambda: open_path(LAUNCHER_DIR)).pack(side="left", padx=5)
        ctk.CTkButton(bf, text="Закрыть", width=140, height=38,
                      font=("Arial", 12), fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.destroy).pack(side="left", padx=5)


# ============ ГЛАВНОЕ ОКНО ============
class Launcher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CraftLauncher Beta")
        self.minsize(900, 670)
        self.resizable(True, True)
        set_icon(self)
        self.config_data = load_config()

        saved_geometry = self.config_data.get("window_geometry", "1100x740+100+100")
        try:
            self.geometry(saved_geometry)
        except Exception:
            self.geometry("1100x740")

        apply_launcher_theme(self.config_data.get("theme_name", self.config_data.get("appearance", "dark")))

        self.is_fullscreen = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_image_ref = None

        self.all_versions = []
        self.selected_instance = None
        self.instance_widgets = {}
        self._nick_timer = None
        self._resize_timer = None
        self.skin_photo = None

        self.ely_token = None
        self.ely_uuid = None
        self.ely_username = None

        threading.Thread(target=download_authlib, daemon=True).start()

        self.bottom_bar = ctk.CTkFrame(self, height=50, corner_radius=0,
                                        fg_color=("gray85", "gray20"))
        self.progress_frame = ctk.CTkFrame(self.bottom_bar, height=10,
                                            corner_radius=5,
                                            fg_color=("gray75", "gray25"))
        self.progress_frame.pack(fill="x", padx=20, pady=(12, 5))
        self.progress = ctk.CTkFrame(self.progress_frame, width=1, height=10,
                                      corner_radius=5, fg_color="#4CAF50")
        self.progress.place(x=0, y=0, relheight=1)
        self.progress_glow = ctk.CTkFrame(self.progress_frame, width=60, height=10,
                                           corner_radius=5, fg_color="#8BC34A")
        self.progress_glow.place(x=-100, y=0, relheight=1)
        self.percent_label = ctk.CTkLabel(self.bottom_bar, text="0%",
                                           font=("Consolas", 11, "bold"),
                                           text_color="#4CAF50")
        self.percent_label.pack(pady=(0, 8))
        self._progress_value = 0.0
        self._glow_offset = -50
        self._glow_running = False
        self.bottom_bar_visible = False

        self.top_container = ctk.CTkFrame(self, fg_color="transparent")
        self.top_container.pack(side="top", fill="both", expand=True)

        self.left_frame = ctk.CTkFrame(self.top_container, width=280,
                                        corner_radius=10,
                                        fg_color=("gray90", "gray15"))
        self.left_frame.pack(side="left", fill="y", padx=(15, 5), pady=15)
        self.left_frame.pack_propagate(False)

        ctk.CTkLabel(self.left_frame, text="📦 Экземпляры",
                     font=("Arial", 16, "bold")).pack(pady=(15, 8))

        sf = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        sf.pack(fill="x", padx=15, pady=(0, 8))
        ctk.CTkLabel(sf, text="🔍", font=("Arial", 14)).pack(side="left", padx=(0, 5))
        self.instance_search = ctk.CTkEntry(sf, height=30, font=("Arial", 11),
                                             placeholder_text="Поиск...")
        self.instance_search.pack(side="left", fill="x", expand=True)
        self.instance_search.bind("<KeyRelease>", lambda e: self.refresh_instances())

        ctk.CTkButton(self.left_frame, text="➕ Создать", width=240, height=35,
                      fg_color="#4CAF50", hover_color="#3d8b40",
                      command=self.open_create_window).pack(pady=(0, 10))

        self.instances_scroll = ctk.CTkScrollableFrame(self.left_frame, width=240,
                                                        fg_color="transparent")
        self.instances_scroll.pack(pady=5, padx=10, fill="both", expand=True)

        self.right_frame = ctk.CTkFrame(self.top_container, corner_radius=10,
                                         fg_color=("gray90", "gray15"))
        self.right_frame.pack(side="right", fill="both", expand=True,
                               padx=(5, 15), pady=15)

        for x, txt, cmd in [
            (-195, "⛶", self.toggle_fullscreen),
            (-150, "ℹ", self.open_about),
            (-105, "📋", self.open_changelog),
            (-60, "❓", self.open_faq),
            (-15, "⚙", self.open_settings),
        ]:
            ctk.CTkButton(self.right_frame, text=txt, width=40, height=40,
                          font=("Arial", 18), fg_color="transparent",
                          hover_color="#3d3d3d", text_color=("black", "white"),
                          command=cmd).place(relx=1.0, rely=0.0, x=x, y=15, anchor="ne")

        self.center_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.center_frame.pack(fill="both", expand=True, pady=(70, 15), padx=40)

        ctk.CTkLabel(self.center_frame, text="⛏ CraftLauncher",
                     font=("Arial", 26, "bold"),
                     text_color="#4CAF50").pack(pady=(0, 5))
        ctk.CTkLabel(self.center_frame,
                     text=f"Beta {APP_VERSION_LABEL} · RAM: {RAM_TOTAL} МБ",
                     font=("Arial", 10), text_color="gray").pack(pady=(0, 15))

        self.ely_status = ctk.CTkButton(self.center_frame,
                                         text="🔐 Войти в Ely.by",
                                         width=380, height=32,
                                         font=("Arial", 12, "bold"),
                                         fg_color="#3a3a3a",
                                         hover_color="#4a4a4a",
                                         command=self.open_ely_auth)
        self.ely_status.pack(pady=(0, 8))

        extra_btns = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        extra_btns.pack(pady=(0, 12), fill="x")

        ctk.CTkButton(extra_btns, text="🌐 Сетевая игра",
                      height=36, font=("Arial", 12, "bold"),
                      fg_color="#3498db", hover_color="#2980b9",
                      command=self.open_network_window).pack(side="left", expand=True,
                                                              fill="x", padx=(0, 5))

        self.mods_btn = ctk.CTkButton(extra_btns, text="🧩 Мод-браузер",
                                       height=36, font=("Arial", 12, "bold"),
                                       fg_color="#9b59b6", hover_color="#8e44ad",
                                       command=self.open_mods_window,
                                       state="disabled")
        self.mods_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))
        self.profiles_btn = ctk.CTkButton(extra_btns, text="👤 Профили",
                                          height=36, font=("Arial", 12, "bold"),
                                          fg_color="#8e44ad", hover_color="#71368a",
                                          command=self.open_profiles_window, state="disabled")
        self.profiles_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

        skin_row = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        skin_row.pack(pady=(5, 12))
        self.skin_preview = ctk.CTkLabel(skin_row, text="👤", width=64, height=64,
                                          fg_color=("gray85", "gray20"),
                                          corner_radius=8, font=("Arial", 28),
                                          text_color="gray")
        self.skin_preview.pack(side="left", padx=(0, 12))

        nick_col = ctk.CTkFrame(skin_row, fg_color="transparent")
        nick_col.pack(side="left")
        ctk.CTkLabel(nick_col, text="Никнейм:",
                     font=("Arial", 12), anchor="w").pack(fill="x")
        self.nick_entry = ctk.CTkEntry(nick_col, width=300, height=35,
                                        font=("Arial", 13))
        self.nick_entry.insert(0, self.config_data.get("nickname", "Steve"))
        self.nick_entry.pack(pady=(3, 0))
        self.nick_entry.bind("<KeyRelease>", self.on_nick_change)

        self.instance_info = ctk.CTkLabel(self.center_frame,
                                           text="Выбери экземпляр слева",
                                           font=("Arial", 13),
                                           text_color="gray")
        self.instance_info.pack(pady=(5, 3))

        self.ram_info = ctk.CTkLabel(self.center_frame, text="",
                                      font=("Arial", 11),
                                      text_color="#4CAF50")
        self.ram_info.pack(pady=(0, 8))

        self.state_frame = ctk.CTkFrame(self.center_frame, corner_radius=10, fg_color=("gray85", "gray20"))
        self.state_frame.pack(fill="x", pady=(0, 10))
        self.state_label = ctk.CTkLabel(self.state_frame, text="Состояние экземпляра", font=("Arial", 12, "bold"), text_color="#4CAF50")
        self.state_label.pack(pady=(8, 3))
        self.state_details = ctk.CTkLabel(self.state_frame, text="Выбери экземпляр", font=("Consolas", 10), text_color="gray", justify="left", wraplength=430)
        self.state_details.pack(padx=12, pady=(0, 8))

        self.status_label = ctk.CTkLabel(self.center_frame,
                                          text="Готов к запуску",
                                          font=("Arial", 11),
                                          text_color="gray",
                                          wraplength=380)
        self.status_label.pack(pady=(0, 15))

        self.play_button = ctk.CTkButton(
            self.center_frame, text="▶  ИГРАТЬ", width=380, height=50,
            font=("Arial", 16, "bold"), fg_color="#4CAF50", hover_color="#3d8b40",
            command=self.start_game_thread, state="disabled")
        self.play_button.pack(pady=(5, 6))
        quick_row = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        quick_row.pack(fill="x", pady=(0, 8))
        self.safe_play_button = ctk.CTkButton(quick_row, text="🛡 Без модов", height=30, font=("Arial", 10), fg_color="#6c5a2b", hover_color="#806d35", command=self.start_safe_mode, state="disabled")
        self.safe_play_button.pack(side="left", expand=True, fill="x", padx=(0, 4))
        self.duplicate_button = ctk.CTkButton(quick_row, text="📑 Дублировать", height=30, font=("Arial", 10), fg_color="#3a3a3a", hover_color="#4a4a4a", command=self.duplicate_selected, state="disabled")
        self.duplicate_button.pack(side="left", expand=True, fill="x", padx=(4, 0))

        inst_btns = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        inst_btns.pack(pady=(0, 10))
        self.open_folder_button = ctk.CTkButton(inst_btns, text="📂 Папка",
                                                 width=120, height=30,
                                                 font=("Arial", 11),
                                                 fg_color="#3a3a3a",
                                                 hover_color="#4a4a4a",
                                                 command=self.open_instance_folder,
                                                 state="disabled")
        self.open_folder_button.pack(side="left", padx=(0, 5))
        self.edit_button = ctk.CTkButton(inst_btns, text="⚙ Настройки",
                                          width=120, height=30,
                                          font=("Arial", 11), fg_color="#3a3a3a",
                                          hover_color="#4a4a4a",
                                          command=self.edit_selected,
                                          state="disabled")
        self.edit_button.pack(side="left", padx=(0, 5))
        self.delete_button = ctk.CTkButton(inst_btns, text="🗑 Удалить",
                                            width=120, height=30,
                                            font=("Arial", 11),
                                            fg_color="#5a2a2a",
                                            hover_color="#7a2020",
                                            command=self.delete_selected,
                                            state="disabled")
        self.delete_button.pack(side="left")
        self.repair_button = ctk.CTkButton(inst_btns, text="🔧 Проверить",
                                           width=120, height=30, font=("Arial", 11),
                                           fg_color="#3a3a3a", hover_color="#4a4a4a",
                                           command=self.repair_selected, state="disabled")
        self.repair_button.pack(side="left", padx=(5, 0))
        self.crash_button = ctk.CTkButton(inst_btns, text="🩺 Краш", width=120, height=30,
                                          font=("Arial", 11), fg_color="#3a3a3a",
                                          hover_color="#4a4a4a", command=self.open_crash_analyzer, state="disabled")
        self.crash_button.pack(side="left", padx=(5, 0))

        self.bind("<Configure>", self.on_window_resize)
        threading.Thread(target=self.load_versions, daemon=True).start()
        self.refresh_instances()
        self.update_ely_status()
        self.after(100, self.update_background)

    def on_close(self):
        try:
            self.config_data["window_geometry"] = self.geometry()
            save_config(self.config_data)
        except Exception:
            pass
        self.destroy()

    def show_progress_bar(self):
        if not self.bottom_bar_visible:
            self.bottom_bar.pack(side="bottom", fill="x")
            self.bottom_bar_visible = True

    def hide_progress_bar(self):
        if self.bottom_bar_visible:
            self.bottom_bar.pack_forget()
            self.bottom_bar_visible = False
            self._progress_value = 0.0
            self.progress.configure(width=1)
            self.percent_label.configure(text="0%")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self, event=None):
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.attributes("-fullscreen", False)

    def on_window_resize(self, event=None):
        if event and event.widget != self:
            return
        if self._resize_timer:
            self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(200, self.update_background)

    def get_default_background(self, w, h):
        is_dark = ctk.get_appearance_mode() == "Dark"
        c1, c2 = ((26, 40, 34), (18, 22, 38)) if is_dark else ((225, 245, 230), (220, 235, 250))
        img = Image.new("RGB", (1, h))
        pixels = img.load()
        for i in range(h):
            t = i / max(h - 1, 1)
            r = int(c1[0] + (c2[0] - c1[0]) * t)
            g = int(c1[1] + (c2[1] - c1[1]) * t)
            b = int(c1[2] + (c2[2] - c1[2]) * t)
            pixels[0, i] = (r, g, b)
        return img.resize((w, h), Image.NEAREST)

    def update_background(self, event=None):
        w, h = self.winfo_width(), self.winfo_height()
        if w < 10 or h < 10:
            return
        current_bg = self.config_data.get("background")
        if (hasattr(self, '_last_bg') and
                self._last_bg == (current_bg, w, h, ctk.get_appearance_mode())):
            return
        self._last_bg = (current_bg, w, h, ctk.get_appearance_mode())

        if current_bg and os.path.exists(current_bg):
            try:
                img = Image.open(current_bg).convert("RGB")
                ir = img.width / img.height
                wr = w / h
                if ir > wr:
                    nw = int(h * ir)
                    img = img.resize((nw, h), Image.LANCZOS)
                    left = (nw - w) // 2
                    img = img.crop((left, 0, left + w, h))
                else:
                    nh = int(w / ir)
                    img = img.resize((w, nh), Image.LANCZOS)
                    top = (nh - h) // 2
                    img = img.crop((0, top, w, top + h))
                dark = Image.new("RGB", (w, h), (0, 0, 0))
                img = Image.blend(img, dark, alpha=0.4)
            except Exception:
                img = self.get_default_background(w, h)
        else:
            img = self.get_default_background(w, h)

        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
        self.bg_label.configure(image=ctk_img)
        self.bg_image_ref = ctk_img
        self.bg_label.lower()

    def set_progress(self, value):
        if not on_ui_thread():
            self.after(0, lambda v=value: self.set_progress(v))
            return
        self._progress_value = max(0.0, min(1.0, value))
        self.update_idletasks()
        tw = self.progress_frame.winfo_width()
        if tw < 10:
            tw = self.winfo_width() - 40
        nw = int(tw * self._progress_value)
        self.progress.configure(width=max(1, nw))
        self.percent_label.configure(text=f"{int(self._progress_value * 100)}%")
        if 0 < self._progress_value < 1.0:
            if not self._glow_running:
                self._glow_running = True
                self.animate_glow()
        else:
            self._glow_running = False
            self.progress_glow.place(x=-100)

    def animate_glow(self):
        if not self._glow_running:
            return
        self.update_idletasks()
        tw = self.progress_frame.winfo_width()
        if tw < 10:
            tw = self.winfo_width() - 40
        self._glow_offset += 10
        if self._glow_offset > tw:
            self._glow_offset = -60
        fw = int(tw * self._progress_value)
        if self._glow_offset < fw:
            self.progress_glow.place(x=self._glow_offset, y=0, relheight=1)
        else:
            self.progress_glow.place(x=-100, y=0, relheight=1)
        self.after(30, self.animate_glow)

    def open_tools_window(self):
        ToolsWindow(self)

    def open_servers_window(self):
        ServerListWindow(self)

    def open_ely_auth(self):
        ElyAuthWindow(self, self.on_ely_success)

    def on_ely_success(self, result):
        self.ely_token = result["accessToken"]
        self.ely_uuid = result["uuid"]
        self.ely_username = result["name"]
        self.update_ely_status()
        self.set_status(f"✅ Вход: {self.ely_username}", "#4CAF50")

    def logout_ely(self):
        self.ely_token = None
        self.ely_uuid = None
        self.ely_username = None
        self.update_ely_status()
        self.set_status("Вышел из Ely.by", "gray")

    def update_ely_status(self):
        if self.ely_token and self.ely_username:
            self.ely_status.configure(text=f"✅ {self.ely_username} (выйти)",
                                       fg_color="#2d5a2d", hover_color="#3d7a3d")
            self.ely_status.configure(command=self.logout_ely)
            self.nick_entry.configure(state="disabled")
            self.nick_entry.delete(0, "end")
            self.nick_entry.insert(0, self.ely_username)
            self.update_skin_preview(self.ely_username)
        else:
            self.ely_status.configure(text="🔐 Войти в Ely.by",
                                       fg_color="#3a3a3a", hover_color="#4a4a4a")
            self.ely_status.configure(command=self.open_ely_auth)
            self.nick_entry.configure(state="normal")
            self.nick_entry.delete(0, "end")
            self.nick_entry.insert(0, self.config_data.get("nickname", "Steve"))
            self.update_skin_preview(self.nick_entry.get())

    def on_nick_change(self, event=None):
        if self.ely_token:
            return
        if self._nick_timer:
            self.after_cancel(self._nick_timer)
        self._nick_timer = self.after(600, self.update_skin_preview_from_entry)

    def update_skin_preview_from_entry(self):
        self.update_skin_preview(self.nick_entry.get().strip())

    def update_skin_preview(self, nickname):
        if not nickname:
            self.skin_preview.configure(image=None, text="👤")
            return

        def fetch():
            try:
                img = load_skin_image(nickname)
                if img:
                    head = crop_head_from_skin(img)
                    self.after(0, lambda h=head: self._apply_skin(h))
                else:
                    self.after(0, lambda: self.skin_preview.configure(image=None, text="👤"))
            except Exception as e:
                log(f"skin fetch error: {e}", "WARN")

        threading.Thread(target=fetch, daemon=True).start()

    def _apply_skin(self, pil_image):
        try:
            ctk_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image,
                                    size=(64, 64))
            self.skin_preview.configure(image=ctk_img, text="")
            self.skin_photo = ctk_img
        except Exception:
            self.skin_preview.configure(image=None, text="👤")

    def load_versions(self):
        self.set_status("Загрузка списка версий...")
        try:
            versions = minecraft_launcher_lib.utils.get_available_versions(LAUNCHER_DIR)
            releases = [v["id"] for v in versions if v["type"] == "release"]
            releases = sort_versions(releases)
            self.all_versions = releases
            self.set_status(f"Загружено версий: {len(releases)} ✅")
        except Exception as e:
            self.set_status(f"Ошибка: {str(e)[:50]} ❌")

    def refresh_instances(self):
        for widget in self.instances_scroll.winfo_children():
            widget.destroy()
        self.instance_widgets.clear()
        all_instances = list_instances()
        query = self.instance_search.get().strip().lower()
        instances = ([i for i in all_instances if query in i["name"].lower()]
                     if query else all_instances)

        if not all_instances:
            ctk.CTkLabel(self.instances_scroll,
                         text="Нет экземпляров.\nНажми ➕ Создать",
                         font=("Arial", 12), text_color="gray").pack(pady=30)
            return
        if not instances:
            ctk.CTkLabel(self.instances_scroll,
                         text=f"Ничего не найдено\nпо запросу «{query}»",
                         font=("Arial", 11), text_color="gray").pack(pady=20)
            return

        for inst in instances:
            name = inst["name"]
            version = inst["version"]
            ram = inst.get("ram", 2048)
            mod_loader = inst.get("mod_loader", "vanilla")

            text = f"🎮 {name}\n{version}"
            if mod_loader != "vanilla":
                text += f" [{mod_loader}]"
            text += f" · {ram} МБ"

            btn = ctk.CTkButton(self.instances_scroll, text=text,
                                 width=220, height=60, font=("Arial", 11),
                                 anchor="w",
                                 fg_color="#4CAF50" if name == self.selected_instance else "#2b2b2b",
                                 hover_color="#3d8b40",
                                 command=lambda n=name: self.select_instance(n))
            btn.pack(pady=3, padx=5, fill="x")
            self.instance_widgets[name] = btn

    def update_play_button(self):
        if not self.selected_instance:
            self.play_button.configure(text="▶  ИГРАТЬ", state="disabled")
            return
        try:
            with open(instance_config_path(self.selected_instance), "r",
                      encoding="utf-8") as f:
                data = json.load(f)
            version = data.get("version", "")
            launch_version = data.get("launch_version", version)
            if is_version_installed(self.selected_instance, launch_version):
                self.play_button.configure(text="▶  ИГРАТЬ", state="normal")
            else:
                self.play_button.configure(text="⬇  УСТАНОВИТЬ", state="normal")
        except Exception:
            pass

    def select_instance(self, name):
        self.selected_instance = name
        for n, btn in self.instance_widgets.items():
            btn.configure(fg_color="#4CAF50" if n == name else "#2b2b2b")
        try:
            with open(instance_config_path(name), "r", encoding="utf-8") as f:
                data = json.load(f)
            data.setdefault("ram", 2048)
            data.setdefault("mod_loader", "vanilla")

            info_text = f"Выбран: {data['name']}  ·  {data['version']}"
            if data.get("mod_loader", "vanilla") != "vanilla":
                info_text += f" [{data['mod_loader']}]"

            self.instance_info.configure(text=info_text,
                                          text_color=("black", "white"))
            self.ram_info.configure(text=f"💾 RAM: {data['ram']} МБ")
            self.delete_button.configure(state="normal")
            self.repair_button.configure(state="normal")
            self.edit_button.configure(state="normal")
            self.open_folder_button.configure(state="normal")
            self.mods_btn.configure(state="normal")
            self.profiles_btn.configure(state="normal")
            self.crash_button.configure(state="normal")
            self.safe_play_button.configure(state="normal")
            self.duplicate_button.configure(state="normal")
            self.update_state_panel(data)
            self.update_play_button()
        except Exception:
            pass

    def update_state_panel(self, data=None):
        if not self.selected_instance: return
        try:
            if data is None:
                with open(instance_config_path(self.selected_instance),"r",encoding="utf-8") as f: data=json.load(f)
            profile=get_active_profile(self.selected_instance); version=data.get("version","?"); loader=data.get("mod_loader","vanilla").upper(); launch=data.get("launch_version",version)
            java,major,warning=choose_java_for_version(version,profile.get("java_path") or self.config_data.get("java_path")); installed=is_version_installed(self.selected_instance,launch); stats=load_launch_stats(self.selected_instance)
            status="ГОТОВ" if installed and java else "НУЖНА ПРОВЕРКА"
            details=(f"MC: {version}  |  Loader: {loader}\nJava: {major or '—'}  |  RAM: {profile.get('ram',data.get('ram',2048))} МБ\nПрофиль: {profile.get('name','default')}  |  Установка: {'✓' if installed else '✗'}\nЗапусков: {stats.get('launches',0)}  |  Успешно: {stats.get('success',0)}  |  Крашей: {stats.get('crashes',0)}")
            self.state_label.configure(text=f"● {status}",text_color="#4CAF50" if status=="ГОТОВ" else "#f39c12"); self.state_details.configure(text=details)
        except Exception as e:
            self.state_label.configure(text="● ОШИБКА",text_color="#e74c3c"); self.state_details.configure(text=str(e)[:300])

    def duplicate_selected(self):
        if not self.selected_instance: return
        name=(ctk.CTkInputDialog(text="Новое имя копии:",title="Дублировать экземпляр").get_input() or "").strip()
        if not name: return
        try:
            duplicate_instance(self.selected_instance,name); self.refresh_instances(); self.select_instance(name); self.set_status(f"📑 Создана копия: {name}","#4CAF50")
        except Exception as e: messagebox.showerror("Дублирование",str(e))

    def start_safe_mode(self):
        self.start_game_thread(safe_mode=True)

    def run_preflight(self,name):
        problems=preflight_instance(name)
        if problems:
            return messagebox.askyesno("Проверка перед запуском","Перед запуском найдены проблемы:\n\n"+"\n".join("• "+p for p in problems)+"\n\nПродолжить?",parent=self)
        return True

    def edit_selected(self):
        if self.selected_instance:
            EditInstanceWindow(self, self.selected_instance, self.on_instance_edited)

    def on_instance_edited(self):
        self.refresh_instances()
        if self.selected_instance:
            self.select_instance(self.selected_instance)

    def repair_selected(self):
        if not self.selected_instance:
            return
        name = self.selected_instance
        problems = check_instance_integrity(name)
        if not problems:
            self.set_status("✅ Проверка завершена: проблем не найдено.", "#4CAF50")
            return
        if not messagebox.askyesno("Восстановление",
                                   "Найдены проблемы:\n\n" + "\n".join("• " + x for x in problems) +
                                   "\n\nПопробовать переустановить Minecraft-файлы?"):
            return
        def work():
            try:
                cfg_path = instance_config_path(name)
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                version = cfg.get("version") or cfg.get("launch_version")
                if not version:
                    raise ValueError("Версия Minecraft не указана")
                self.after(0, lambda: self.set_status("🔧 Восстановление Minecraft...", "#f39c12"))
                minecraft_launcher_lib.install.install_minecraft_version(
                    version, instance_minecraft_dir(name),
                    callback={"setStatus": lambda x: None})
                self.after(0, lambda: self.set_status("✅ Базовые файлы восстановлены. Проверь запуск.", "#4CAF50"))
            except Exception as e:
                log(f"Repair error: {e}\n{traceback.format_exc()}", "ERROR")
                self.after(0, lambda err=str(e): self.set_status(f"❌ Ошибка восстановления: {err}", "#e74c3c"))
        threading.Thread(target=work, daemon=True).start()

    def open_instance_folder(self):
        if not self.selected_instance:
            return
        mc_dir = instance_minecraft_dir(self.selected_instance)
        if os.path.exists(mc_dir):
            open_path(mc_dir)

    def delete_selected(self):
        if not self.selected_instance:
            return
        confirm = ctk.CTkToplevel(self)
        confirm.title("Подтверждение")
        confirm.geometry("360x180")
        confirm.resizable(False, False)
        confirm.grab_set()
        confirm.after(100, confirm.lift)
        set_icon(confirm)
        ctk.CTkLabel(confirm,
                     text=f"Удалить экземпляр\n«{self.selected_instance}»?",
                     font=("Arial", 13)).pack(pady=(20, 5))
        ctk.CTkLabel(confirm, text="Все миры и моды будут удалены!",
                     font=("Arial", 10), text_color="#e74c3c").pack()
        frame = ctk.CTkFrame(confirm, fg_color="transparent")
        frame.pack(pady=15)

        def do_delete():
            delete_instance(self.selected_instance)
            self.selected_instance = None
            self.instance_info.configure(text="Выбери экземпляр слева",
                                          text_color="gray")
            self.ram_info.configure(text="")
            self.play_button.configure(state="disabled", text="▶  ИГРАТЬ")
            self.delete_button.configure(state="disabled")
            self.repair_button.configure(state="disabled")
            self.edit_button.configure(state="disabled")
            self.open_folder_button.configure(state="disabled")
            self.mods_btn.configure(state="disabled")
            self.profiles_btn.configure(state="disabled")
            self.crash_button.configure(state="disabled")
            self.safe_play_button.configure(state="disabled")
            self.duplicate_button.configure(state="disabled")
            self.state_details.configure(text="Выбери экземпляр")
            self.refresh_instances()
            confirm.destroy()

        ctk.CTkButton(frame, text="Удалить", width=120, height=35,
                      fg_color="#e74c3c", hover_color="#c0392b",
                      command=do_delete).pack(side="left", padx=5)
        ctk.CTkButton(frame, text="Отмена", width=120, height=35,
                      fg_color="#555", hover_color="#333",
                      command=confirm.destroy).pack(side="left", padx=5)

    def open_create_window(self):
        if not self.all_versions:
            self.set_status("Версии загружаются...")
            return
        CreateInstanceWindow(self, self.all_versions, self.on_instance_created)

    def on_instance_created(self):
        self.refresh_instances()
        self.set_status("Экземпляр создан ✅", "#4CAF50")

    def open_crash_analyzer(self):
        if self.selected_instance:
            CrashAnalyzerWindow(self, self.selected_instance)

    def open_profiles_window(self):
        if self.selected_instance:
            ProfileManagerWindow(self, self.selected_instance, self.on_profile_changed)

    def on_profile_changed(self):
        if self.selected_instance:
            self.select_instance(self.selected_instance)

    def open_settings(self):
        SettingsWindow(self)

    def open_about(self):
        AboutWindow(self)

    def open_changelog(self):
        ChangelogWindow(self)

    def open_faq(self):
        FAQWindow(self)

    def open_network_window(self):
        NetworkWindow(self)

    def open_mods_window(self):
        if not self.selected_instance:
            self.set_status("Сначала выбери экземпляр", "#e74c3c")
            return
        try:
            with open(instance_config_path(self.selected_instance), "r",
                      encoding="utf-8") as f:
                data = json.load(f)
            mc_version = data.get("version", "1.20.1")
            ModsWindow(self, self.selected_instance, mc_version)
        except Exception as e:
            self.set_status(f"Ошибка: {e}", "#e74c3c")

    def set_status(self, text, color="gray"):
        if not on_ui_thread():
            self.after(0, lambda t=text, c=color: self.set_status(t, c))
            return
        self.status_label.configure(text=text, text_color=color)
        self.update_idletasks()

    def open_quick_connect(self, ip, port):
        if not self.selected_instance:
            self.set_status("Выбери экземпляр", "#e74c3c")
            return
        instance_name = self.selected_instance
        try:
            with open(instance_config_path(instance_name), "r",
                      encoding="utf-8") as f:
                inst_data = json.load(f)
            version = inst_data["version"]
            launch_version = inst_data.get("launch_version", version)
            ram = inst_data.get("ram", 2048)
            mc_dir = instance_minecraft_dir(instance_name)

            if not is_version_installed(instance_name, launch_version):
                self.set_status("Сначала установи версию", "#e74c3c")
                return

            use_ely = bool(self.ely_token and self.ely_uuid and self.ely_username)
            nickname = self.ely_username if use_ely else (
                self.nick_entry.get().strip() or "Player")

            console = None
            if self.config_data.get("show_console", True):
                console = ConsoleWindow(self, instance_name)
                console.add_message(f"Подключение к {ip}:{port}...", "info")

            if use_ely:
                options = {"username": self.ely_username, "uuid": self.ely_uuid,
                           "token": self.ely_token, "gameDirectory": mc_dir,
                           "jvmArguments": [f"-Xmx{ram}M", f"-Xms{min(ram, 1024)}M"] + list(profile.get("jvm_args", [])),
                                "executablePath": java_path}
                if os.path.exists(AUTHLIB_JAR):
                    options["jvmArguments"].insert(0, f"-javaagent:{AUTHLIB_JAR}=ely.by")
            else:
                options = {"username": nickname, "uuid": "0", "token": "0",
                           "gameDirectory": mc_dir,
                           "jvmArguments": [f"-Xmx{ram}M", f"-Xms{min(ram, 1024)}M"] + list(profile.get("jvm_args", [])),
                                "executablePath": java_path}

            command = minecraft_launcher_lib.command.get_minecraft_command(
                launch_version, mc_dir, options)
            command.extend(["--server", ip, "--port", str(port)])

            self.set_status(f"Запуск → {ip}:{port}", "#4CAF50")
            self.launch_process(command, mc_dir, console)
        except Exception as e:
            self.set_status(f"Ошибка: {e}", "#e74c3c")

    def start_game_thread(self, safe_mode=False):
        if not self.selected_instance:
            return
        try:
            current_text = self.play_button.cget("text")
            if not self.run_preflight(self.selected_instance):
                return
            self.play_button.configure(state="disabled", text="Загрузка...")
            threading.Thread(target=self.launch_game, args=(current_text, safe_mode), daemon=True).start()
        except Exception as e:
            import traceback
            log(f"start_game_thread ERROR: {traceback.format_exc()}", "ERROR")
            self.set_status(f"Ошибка: {str(e)[:60]}", "#e74c3c")
            self.play_button.configure(state="normal", text="▶  ИГРАТЬ")

    def launch_game(self, button_text, safe_mode=False):
        console = None
        safe_moved = []
        try:
            log(f"=== launch_game START ===")
            name = self.selected_instance
            use_ely = bool(self.ely_token and self.ely_uuid and self.ely_username)
            nickname = self.ely_username if use_ely else (
                self.nick_entry.get().strip() or "Player")
            if not use_ely:
                self.config_data["nickname"] = nickname
                save_config(self.config_data)

            with open(instance_config_path(name), "r", encoding="utf-8") as f:
                inst_data = json.load(f)
            version = inst_data["version"]
            launch_version = inst_data.get("launch_version", version)
            profile = get_active_profile(name)
            ram = int(profile.get("ram", inst_data.get("ram", 2048)))
            mc_dir = instance_minecraft_dir(name)
            profile_nickname = str(profile.get("nickname", "")).strip()
            if profile_nickname:
                nickname = profile_nickname
            configured_java = profile.get("java_path") or self.config_data.get("java_path")
            java_path, java_major, java_warning = choose_java_for_version(
                version, configured_java
            )
            if not java_path:
                # Предлагаем установить ровно ту Java, которая нужна этой версии Minecraft.
                decision = {"value": False}
                done = threading.Event()

                def ask_install():
                    try:
                        decision["value"] = messagebox.askyesno(
                            "Установить Java автоматически?",
                            f"{java_warning}\n\n"
                            f"CraftLauncher может скачать Java {required_java_major(version)} "
                            "с Eclipse Adoptium и установить её в свою папку runtime.\n\n"
                            "Системная Java при этом не изменяется.",
                            parent=self
                        )
                    finally:
                        done.set()

                ui_call(self, ask_install)
                done.wait()
                if not decision["value"]:
                    self.set_status(java_warning, "#e74c3c")
                    return

                required = required_java_major(version)
                self.set_status(f"Скачивание Java {required}...", "#f39c12")
                try:
                    java_path = download_and_install_java(
                        required,
                        lambda done_bytes, total: self.set_status(
                            f"Скачивание Java {required}: "
                            f"{int(done_bytes / total * 100)}%" if total else
                            f"Скачивание Java {required}...", "#f39c12"
                        )
                    )
                    java_major = required
                    java_warning = None
                    self.set_status(f"Java {required} установлена", "#4CAF50")
                except Exception as exc:
                    log(f"Automatic Java installation failed: {exc}", "ERROR")
                    self.set_status(f"Не удалось установить Java {required}", "#e74c3c")
                    ui_call(self, lambda e=exc: messagebox.showerror(
                        "Автоустановка Java",
                        f"Не удалось установить Java {required}.\n\n{e}",
                        parent=self
                    ))
                    return
            if java_warning:
                log(java_warning, "WARN")
                self.set_status(java_warning, "#f39c12")

            already_installed = is_version_installed(name, launch_version)
            is_installing = "УСТАНОВИТЬ" in button_text

            if already_installed and not is_installing:
                if self.config_data.get("show_console", True):
                    console = ConsoleWindow(self, name)
                    console.add_message(f"Версия: {launch_version}", "system")
                    console.add_message(f"Ник: {nickname}", "system")
                    if use_ely:
                        console.add_message("🎨 ONLINE (Ely.by)", "ok")
                    else:
                        console.add_message("💤 OFFLINE", "warn")

                if use_ely:
                    options = {"username": self.ely_username, "uuid": self.ely_uuid,
                               "token": self.ely_token, "gameDirectory": mc_dir,
                               "jvmArguments": [f"-Xmx{ram}M", f"-Xms{min(ram, 1024)}M"] + list(profile.get("jvm_args", [])),
                                "executablePath": java_path}
                    if os.path.exists(AUTHLIB_JAR):
                        options["jvmArguments"].insert(0, f"-javaagent:{AUTHLIB_JAR}=ely.by")
                else:
                    options = {"username": nickname, "uuid": "0", "token": "0",
                               "gameDirectory": mc_dir,
                               "jvmArguments": [f"-Xmx{ram}M", f"-Xms{min(ram, 1024)}M"] + list(profile.get("jvm_args", [])),
                                "executablePath": java_path}

                command = minecraft_launcher_lib.command.get_minecraft_command(
                    launch_version, mc_dir, options)
                if safe_mode:
                    safe_moved = prepare_safe_mode(name)
                    if console: console.add_message(f"🛡 Безопасный запуск: отключено модов {len(safe_moved)}", "warn")
                record_launch_start(name)
                self.launch_process(command, mc_dir, console, on_exit=lambda code: restore_safe_mode(safe_moved))
                self.set_status(f"«{name}» запущен! 🎮", "#4CAF50")
                return

            self.after(0, self.show_progress_bar)
            if self.config_data.get("show_console", True):
                console = ConsoleWindow(self, name)
                console.add_message(f"Установка Minecraft {version}...", "info")

            self.set_status(f"Установка {version}...")
            self.set_progress(0)
            self._progress_max = 1

            def scb(t): self.set_status(t[:60])
            def mcb(m): self._progress_max = m if m > 0 else 1
            def pcb(c):
                if self._progress_max > 0:
                    self.set_progress(c / self._progress_max)

            try:
                minecraft_launcher_lib.install.install_minecraft_version(
                    version, mc_dir,
                    callback={"setStatus": scb, "setProgress": pcb, "setMax": mcb})
            except Exception as e:
                self.set_status(f"Ошибка: {e}"[:80], "#e74c3c")
                self.after(0, self.hide_progress_bar)
                return

            self.set_progress(1.0)
            self.set_status("Ванилла установлена ✅")
            self.after(1500, self.hide_progress_bar)

            mod_loader = inst_data.get("mod_loader", "vanilla")
            if mod_loader != "vanilla":
                self.set_status(
                    f"Ванилла установлена. Установи {mod_loader.upper()} в настройках.",
                    "#f39c12"
                )
                self.after(0, self.update_play_button)
                return

            if not self.config_data.get("auto_launch_after_install", True):
                self.after(0, self.update_play_button)
                return

            if use_ely:
                options = {"username": self.ely_username, "uuid": self.ely_uuid,
                           "token": self.ely_token, "gameDirectory": mc_dir,
                           "jvmArguments": [f"-Xmx{ram}M", f"-Xms{min(ram, 1024)}M"] + list(profile.get("jvm_args", [])),
                                "executablePath": java_path}
                if os.path.exists(AUTHLIB_JAR):
                    options["jvmArguments"].insert(0, f"-javaagent:{AUTHLIB_JAR}=ely.by")
            else:
                options = {"username": nickname, "uuid": "0", "token": "0",
                           "gameDirectory": mc_dir,
                           "jvmArguments": [f"-Xmx{ram}M", f"-Xms{min(ram, 1024)}M"] + list(profile.get("jvm_args", [])),
                                "executablePath": java_path}

            command = minecraft_launcher_lib.command.get_minecraft_command(
                version, mc_dir, options)
            if safe_mode:
                safe_moved = prepare_safe_mode(name)
                if console: console.add_message(f"🛡 Безопасный запуск: отключено модов {len(safe_moved)}", "warn")
            record_launch_start(name)
            self.launch_process(command, mc_dir, console, on_exit=lambda code: restore_safe_mode(safe_moved))
            self.set_status(f"«{name}» запущен! 🎮", "#4CAF50")
        except Exception as e:
            import traceback
            err = traceback.format_exc()
            log(f"CRASH in launch_game: {err}", "ERROR")
            print(err)
            self.set_status(f"Ошибка: {str(e)[:80]}", "#e74c3c")
            self.after(0, self.hide_progress_bar)
        finally:
            self.after(0, lambda: self.update_play_button())

    def launch_process(self, command, cwd, console, on_exit=None):
        try:
            process = subprocess.Popen(
                command, cwd=cwd,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                **run_subprocess_kwargs(),
                bufsize=1, universal_newlines=True,
                encoding="utf-8", errors="replace")
            if console:
                console.process = process

            def read_output():
                capture_path = os.path.join(instance_minecraft_dir(self.selected_instance), "craftlauncher-last-run.log")
                try:
                    os.makedirs(os.path.dirname(capture_path), exist_ok=True)
                    with open(capture_path, "w", encoding="utf-8", errors="replace") as capture:
                        capture.write(f"CraftLauncher launch capture\\nCommand: {' '.join(map(str, command))}\\n\\n")
                        for line in iter(process.stdout.readline, ""):
                            if not line:
                                break
                            line = line.rstrip()
                            capture.write(line + "\\n")
                            capture.flush()
                            low = line.lower()
                            level = ("error" if any(k in low for k in
                                     ["error", "exception", "caused by", "fatal"])
                                     else "warn" if "warn" in low
                                     else "info" if "done" in low and "for help" in low
                                     else "normal")
                            if console:
                                try:
                                    console.after(0, lambda l=line, lv=level: console.append_log(l, lv))
                                except Exception:
                                    pass
                    code = process.wait()
                    with open(capture_path, "a", encoding="utf-8", errors="replace") as capture:
                        capture.write(f"\\nCraftLauncher exit code: {code}\\n")
                    try: record_launch_end(self.selected_instance, code)
                    except Exception: pass
                    if on_exit:
                        try: on_exit(code)
                        except Exception as e: log(f"on_exit error: {e}", "WARN")
                    try: self.after(0, self.update_state_panel)
                    except Exception: pass
                    if console:
                        try:
                            if code == 0:
                                console.after(0, lambda: console.add_message("Игра завершена", "ok"))
                            else:
                                console.after(0, lambda c=code: console.add_message(f"Код выхода: {c}", "error"))
                                failed_instance = self.selected_instance
                                if failed_instance:
                                    console.after(250, lambda n=failed_instance, c=code: CrashAnalyzerWindow(self, n, c))
                        except Exception:
                            pass
                except Exception as e:
                    log(f"Crash capture error: {e}", "ERROR")
                    try:
                        with open(capture_path, "a", encoding="utf-8", errors="replace") as capture:
                            capture.write(f"\\nCraftLauncher capture error: {e}\\n")
                    except Exception:
                        pass

            threading.Thread(target=read_output, daemon=True).start()
        except FileNotFoundError as e:
            if console:
                try:
                    console.after(0, lambda: console.add_message(f"Java не найдена!\n{e}", "error"))
                except Exception:
                    pass
        except Exception as e:
            if console:
                try:
                    console.after(0, lambda: console.add_message(f"Ошибка: {e}", "error"))
                except Exception:
                    pass


class JavaManagerWindow(ctk.CTkToplevel):
    def __init__(self, parent, owner=None):
        super().__init__(parent)
        self.parent = parent
        self.owner = owner
        self.title("☕ Java Manager")
        self.geometry("820x650")
        self.minsize(700, 560)
        self.transient(owner or parent)
        self.protocol("WM_DELETE_WINDOW", self.close)
        set_icon(self)

        ctk.CTkLabel(self, text="☕ Java Manager",
                     font=("Arial", 21, "bold"),
                     text_color="#4CAF50").pack(pady=(16, 3))
        ctk.CTkLabel(
            self,
            text="Поиск, проверка и автоматическая установка Java 8 / 17 / 21",
            font=("Arial", 10), text_color="gray"
        ).pack(pady=(0, 10))

        install = ctk.CTkFrame(self, fg_color="transparent")
        install.pack(fill="x", padx=20, pady=(0, 8))
        ctk.CTkLabel(install, text="Автоустановка:", font=("Arial", 11, "bold")).pack(side="left", padx=(0, 8))
        for major in (8, 17, 21):
            ctk.CTkButton(
                install, text=f"☕ Java {major}", width=130,
                command=lambda m=major: self.install_java(m)
            ).pack(side="left", padx=4)

        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(fill="x", padx=20, pady=(0, 5))
        self.progress.pack_forget()

        self.table = ctk.CTkScrollableFrame(self)
        self.table.pack(fill="both", expand=True, padx=20, pady=5)

        self.status = ctk.CTkLabel(self, text="Готово", text_color="gray", wraplength=760)
        self.status.pack(pady=5)

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=(5, 15))
        ctk.CTkButton(row, text="🔄 Сканировать", command=self.scan,
                      fg_color="#4CAF50").pack(side="left", expand=True, fill="x", padx=(0, 4))
        ctk.CTkButton(row, text="📁 Добавить Java", command=self.add,
                      fg_color="#3a3a3a").pack(side="left", expand=True, fill="x", padx=4)
        ctk.CTkButton(row, text="Закрыть", command=self.close,
                      fg_color="#555").pack(side="left", expand=True, fill="x", padx=(4, 0))

        self.scan()
        self.after(50, self._activate)

    def _activate(self):
        try:
            self.lift()
            self.focus_force()
            self.grab_set()
        except Exception:
            pass

    def close(self):
        try:
            self.grab_release()
        except Exception:
            pass
        try:
            self.destroy()
        finally:
            if self.owner is not None:
                try:
                    self.owner.grab_set()
                    self.owner.lift()
                    self.owner.focus_force()
                except Exception:
                    pass

    def scan(self):
        for w in self.table.winfo_children():
            w.destroy()
        runtimes = discover_java_runtimes()
        if not runtimes:
            ctk.CTkLabel(
                self.table, text="Java не найдена. Можно установить Java кнопками выше.",
                text_color="#e74c3c"
            ).pack(pady=30)
            self.status.configure(text="Java не найдена", text_color="#e74c3c")
            return
        for j in runtimes:
            row = ctk.CTkFrame(self.table)
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(
                row, text=f"Java {j['major']}", width=90,
                font=("Arial", 12, "bold")
            ).pack(side="left", padx=8)
            ctk.CTkLabel(
                row, text=j["path"], anchor="w"
            ).pack(side="left", fill="x", expand=True)
            ctk.CTkButton(
                row, text="Выбрать", width=90,
                command=lambda path=j["path"]: self.select(path)
            ).pack(side="right", padx=5)
        self.status.configure(
            text=f"Найдено Java: {len(runtimes)}. Автоматический выбор используется, если путь не задан.",
            text_color="#4CAF50"
        )

    def select(self, path):
        major = java_major_version(path)
        if not major:
            messagebox.showerror("Java", "Эта Java больше не проходит проверку.", parent=self)
            return
        self.parent.config_data["java_path"] = path
        save_config(self.parent.config_data)
        self.status.configure(
            text=f"Выбрана Java {major}: {path}",
            text_color="#4CAF50"
        )

    def install_java(self, major):
        if not messagebox.askyesno(
            "Автоустановка Java",
            f"Установить Java {major} в папку CraftLauncher?\n\n"
            "Java будет скачана с Eclipse Adoptium и не заменит системную Java.",
            parent=self
        ):
            return

        self.progress.pack(fill="x", padx=20, pady=(0, 5), before=self.table)
        self.progress.set(0)
        self.status.configure(text=f"Подготовка загрузки Java {major}...", text_color="gray")
        for child in self.winfo_children():
            # Do not disable the window itself; the worker will update status.
            pass

        def worker():
            try:
                def progress(done, total):
                    value = (done / total) if total else 0
                    self.after(0, lambda v=value: self.progress.set(min(1, v)))

                exe = download_and_install_java(major, progress)
                def done():
                    self.progress.pack_forget()
                    self.status.configure(
                        text=f"Java {major} установлена: {exe}",
                        text_color="#4CAF50"
                    )
                    self.scan()
                self.after(0, done)
            except Exception as exc:
                log(f"Java {major} installation failed: {exc}", "ERROR")
                def failed():
                    self.progress.pack_forget()
                    self.status.configure(
                        text=f"Ошибка установки Java {major}: {exc}",
                        text_color="#e74c3c"
                    )
                    messagebox.showerror(
                        "Автоустановка Java",
                        f"Не удалось установить Java {major}.\n\n{exc}",
                        parent=self
                    )
                self.after(0, failed)

        threading.Thread(target=worker, daemon=True).start()

    def add(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Выбери java executable",
            filetypes=[
                ("Java executable", "java.exe" if IS_WINDOWS else "java"),
                ("Все файлы", "*.*")
            ]
        )
        if not path:
            return
        exe = java_executable(path)
        major = java_major_version(exe) if exe else None
        if not exe or not major:
            messagebox.showerror("Java", "Файл не прошёл проверку.", parent=self)
            return
        self.status.configure(
            text=f"Java {major} добавлена в список сканирования: {exe}",
            text_color="#4CAF50"
        )
        self.scan()

# ============ ЗАПУСК ============
if __name__ == "__main__":
    try:
        app = Launcher()
        app.mainloop()
    except Exception as e:
        log(f"FATAL: {e}", "ERROR")
        import traceback
        log(traceback.format_exc(), "ERROR")
        raise
    finally:
        log("CraftLauncher closed")
