

import sys
import ctypes
import os
import subprocess
import time

import psutil

counter = time.time()

IS_WIN = sys.platform.startswith("win")

def get_hosts_location():
    if IS_WIN:
        return "C:\\Windows\\System32\\drivers\\etc\\hosts"
    else:
        return "/etc/hosts"

if IS_WIN:
    if not ctypes.windll.shell32.IsUserAnAdmin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            print("Python Shell yönetici olarak başlatılmadı")
        except BaseException:
            print("Lütfen bu betiği yönetici ayrıcalıklarıyla çalıştırın.")

HOSTS_LOCATION = get_hosts_location()

BLOCK_STRING = """
# Spotify AdBlocker by 13mqn
# Generic ads below
127.0.0.1 adclick.g.doublecklick.net
127.0.0.1 adeventtracker.spotify.com
127.0.0.1 ads-fa.spotify.com
127.0.0.1 analytics.spotify.com
127.0.0.1 audio2.spotify.com
127.0.0.1 b.scorecardresearch.com
127.0.0.1 bounceexchange.com
127.0.0.1 bs.serving-sys.com
127.0.0.1 content.bitsontherun.com
127.0.0.1 core.insightexpressai.com
127.0.0.1 crashdump.spotify.com
127.0.0.1 d2gi7ultltnc2u.cloudfront.net
127.0.0.1 d3rt1990lpmkn.cloudfront.net
127.0.0.1 desktop.spotify.com
127.0.0.1 doubleclick.net
127.0.0.1 ds.serving-sys.com
127.0.0.1 googleadservices.com
127.0.0.1 googleads.g.doubleclick.net
127.0.0.1 gtssl2-ocsp.geotrust.com
127.0.0.1 js.moatads.com
127.0.0.1 log.spotify.com
127.0.0.1 media-match.com
127.0.0.1 omaze.com
127.0.0.1 open.spotify.com
127.0.0.1 pagead46.l.doubleclick.net
127.0.0.1 pagead2.googlesyndication.com
127.0.0.1 partner.googleadservices.com
127.0.0.1 pubads.g.doubleclick.net
127.0.0.1 redirector.gvt1.com
127.0.0.1 s0.2mdn.net
127.0.0.1 securepubads.g.doubleclick.net
127.0.0.1 spclient.wg.spotify.com
127.0.0.1 tpc.googlesyndication.com
127.0.0.1 v.jwpcdn.com
127.0.0.1 video-ad-stats.googlesyndication.com
127.0.0.1 weblb-wg.gslb.spotify.com
127.0.0.1 www.googleadservices.com
127.0.0.1 www.googletagservices.com
# End AdBlocker portion
"""

def kill_and_restart():
    spotify_procs = [p for p in psutil.process_iter() if p.name().lower().startswith("spotify")]

    for p in spotify_procs:
        for c in p.children(recursive=True):
            c.kill()

        print("Spotify Kapatılıyor.")
    print("Spotify Kapatıldı.")

    try:
        if IS_WIN or sys.platform.startswith("linux"):
            subprocess.call(spotify_procs[0].exe())
        elif sys.platform.startswith("darwin"):
            os.system("open -a /Applications/Spotify.app/Contents/MacOS/Spotify")
        print("Spotify Başlatılıyor...")
        print("Spotify Başlatıldı.")
    except IndexError:
        pass

def write_hosts():
    with open(HOSTS_LOCATION, "r") as f:
        contents = f.read()
    if BLOCK_STRING in contents:
        print("Zaten reklamları engelliyor. Dosya düzenlenemedi.")
    else:
        with open(HOSTS_LOCATION, "a") as f:
            f.write(BLOCK_STRING)
            print("Hosts dosyası düzenlendi.")
            kill_and_restart()

if IS_WIN and ctypes.windll.shell32.IsUserAnAdmin():
    write_hosts()
elif not IS_WIN:
    try:
        write_hosts()
    except BaseException:
        print("Hata: Dosya değiştirilemedi.\n Sudo ayrıcalıklarıyla çalıştırmayı deneyin.")
        exit(1)

print("İşlem {:.2f}saniye içinde bitirildi.".format(time.time() - counter))
