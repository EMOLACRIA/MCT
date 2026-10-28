<!-- spider-punk-0.1.0 -->
# Spider-Punk 0.1.0 — 28 Ekim 2026

Yedinci bağımsız tema paketi: `spider-punk`, ABI `mct-shell-2.9`. Düzen mevcut
temalarla aynıdır; ortak shell değişmez, `update.sh` gerekmez.

## Fikir: fotokopi fanzin

- Paneller yırtık kâğıt; her panelin arkasında birkaç piksel kaymış camgöbeği ikinci
  mürekkep katmanı var (hizasız baskı). Bar'ın altında pembe çizgi ve camgöbeği izi.
- Masaüstü kabuğu, kilit ekranı ve giriş ekranı açık "Zine" yüzleridir: fotokopi kâğıdı,
  siyah mürekkep, pembe seçim.
- Çalışılan uygulamalar (Kitty, Dolphin, Spotify) siyah fotokopidir. Dolphin'de beyaz yazı
  kuralı korunur; uzun kullanımda koyu yüzey göz yormaz.
- İki ses: keçeli kalem (Permanent Marker) saat ve başlıklarda; sistem metni sans-serif.
- Kilit ekranı ve Fastfetch: `BREAK THE CANON.` (özgün cümle, filmden alıntı değil).

Karakter, sembol veya logo çizilmez. Duvar kâğıdı kullanıcının resmidir, renkleri değişmez.
Bütün süsler statik Canvas/dikdörtgen; animasyon ve blur yok.

## Palet

| Rol | Zine (kabuk) | Xerox (uygulamalar) |
|---|---|---|
| Yüzey | `#ece8de` | `#111111` |
| Metin | `#111111` | `#eeeae0` / Dolphin `#ffffff` |
| İkincil | `#5c5850` | `#a09c94` |
| Çizgi | `#b9b3a6` | `#3a3a3a` |
| Üzerine gelme / seçim | `#f4dce2` / `#f2a9bb` | `#262626` / `#4a1a28` |
| Vurgu | `#e8285a` | `#e8285a` |
| İkinci mürekkep | `#2fb3e8` | `#2fb3e8` |

## Üretim ve kayıtlar

`design/spider-punk/build.py` paketi Snowgrave Frost'un yapısından üretir (kabuk için
Zine, Dolphin/Spotify için Xerox renk eşlemesi). Permanent Marker: Apache 2.0
(npm `@fontsource/permanent-marker` 5.3.0, latin alt kümesi, WOFF2'den TTF'e).
Ortak dosyalarda: `theme_core.allowed` iki dosya adı, `adapter_assets`, terminal vurgusu,
Fastfetch alıntısı. Gravity Falls Dolphin şemasının adı da düzeltildi (Frost adı kalmıştı).

## Kurulum

```fish
sudo python3 sddm/sync_setup.py install --user $USER --check
sudo python3 sddm/sync_setup.py install --user $USER
bash theme.sh check spider-punk; and bash theme.sh apply spider-punk
```

## Sınırlar

Hazırlama ortamında QML render'ları, sandbox apply/geçiş/rollback, Dolphin/Spotify/terminal
adaptör fixture'ları ve SDDM greeter UI testleri geçti. Gerçek Wayland oturumu, Spotify,
Dolphin ve giriş ekranı kullanıcıda doğrulanacak. Permanent Marker latin alt kümesi Türkçe
özel harfleri içermez.
