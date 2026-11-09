<!-- treasure-planet-0.1.0 -->
# Treasure Planet 0.1.0 — 9 Kasım 2026

Dokuzuncu tema paketi: `treasure-planet`, ABI `mct-shell-2.9`. Düzen diğer temalarla
aynıdır; ortak shell değişmez, `update.sh` gerekmez.

## Fikir: geminin navigasyon plakaları, etherium üstünde

- Paneller %88 opak koyu etherium mavisi; çevresinde çift çizgi, köşelerde perçinli gümüş
  köşebentler ve her kenarın ortasında küçük pusula çentiği. Statik Canvas; yalnız boyut
  değişince çizilir.
- Bar aynı cam şerit; altında gümüş ve koyu iki ince çizgi.
- Vurgu açık turkuaz, bağlantı parçaları gümüş, iyon yeşili küçük vurgularda.
  Kullanıcı isteği: hiçbir yerde sarı yok (ANSI sarı soluk limon tonuna çekildi).
- Başlık ve saat Cinzel (harita/gravür harfleri, Türkçe tam); sistem metni sans-serif.
- Kitty, Dolphin, Spotify opak koyu mavi; Dolphin yazısı beyaz.
- Kilit ekranı ve Fastfetch: `CHART YOUR OWN COURSE.` (özgün cümle, filmden alıntı değil).

Blur, gölge ve animasyon kapalı. Karakter, gemi tasarımı veya logo çizilmez; terminalde
yalnız halkalı bir gezegen ve yıldızlar var.

## Palet (Nebula)

| Rol | Kabuk | Uygulamalar |
|---|---|---|
| Yüzey | `#0b1d28` × 0.88 | `#0e2230` |
| Metin | `#eef8ff` | `#eef8ff` / Dolphin `#ffffff` |
| İkincil | `#a3c2cf` | `#6f93a3` |
| Seçim | `#b01a4a5e` | `#23506a` |
| Vurgu | `#7fe3ef` | `#7fe3ef` |
| Bağlantı / çizgi | `#b9cdd2`, `#34586a` | — |

Kullanıcı önce Etherium/Solar Sail/Montressor (pirinç) denemelerini gördü, sarıyı
istemedi; sarısız Solar Sail/Nebula/Deep Space arasından Nebula'yı seçti.

## Kurulum

```fish
sudo python3 sddm/sync_setup.py install --user $USER --check
sudo python3 sddm/sync_setup.py install --user $USER
bash theme.sh check treasure-planet; and bash theme.sh apply treasure-planet
```

## Sınırlar

Hazırlama ortamında bütün paneller, Super+G rayı ve SDDM greeter render edildi; sandbox
apply/geçiş/rollback, adaptör fixture'ları ve tema ayarları testleri geçti. Gerçek oturumda
kilit ekranı (Hyprlock, yazı tipi `serif`), Spotify, Dolphin ve giriş ekranı kullanıcıda
doğrulanacak.
