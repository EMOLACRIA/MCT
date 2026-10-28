<!-- little-prince-0.1.0 -->
# Little Prince 0.1.0 — 28 Ekim 2026

Sekizinci bağımsız tema paketi: `little-prince`, ABI `mct-shell-2.9`. Düzen mevcut
temalarla aynıdır; ortak shell değişmez, `update.sh` gerekmez.

## Fikir: kâğıt diorama, alacakaranlık gökyüzü

- Paneller %80 opak alacakaranlık mavisi kâğıttır (`surfaceOpacity` ile çarpılır);
  arkalarında elle kesilmiş gibi hafif dalgalı kehribar ve gül renkli iki kâğıt katmanı
  kayık durur. Panelin altındaki kısım silinir, yarı saydam yüzeyden yalnız kenarlar görünür.
- Bar aynı yarı saydam mavi; altında ince kehribar ve gül şeritleri.
- Vurgu yıldız sarısı. İki ses: Lora italik saat ve başlıklarda; sistem metni sans-serif.
- Kitty, Dolphin, Spotify opak koyu mavidir (okunurluk); Dolphin'de yazı beyaz kalır.
- Kilit ekranı ve Fastfetch: `TEND THE ROSE YOU CHOSE.` (özgün cümle, kitaptan alıntı değil).

Saydamlık sadece renk alfası: blur ve gölge kapalı, animasyon eklenmedi. Kâğıt katmanları
statik Canvas; yalnız boyut değişince yeniden çizilir. Karakter, sembol veya logo çizilmez.

## Palet

| Rol | Kabuk (yarı saydam) | Uygulamalar (opak) |
|---|---|---|
| Yüzey | `#2b3260` × 0.80 | `#1e2344` |
| Metin | `#f7eed6` | `#f7eed6` / Dolphin `#ffffff` |
| İkincil | `#c3c2dc` | `#8a8fb8` |
| Seçim | `#a0505aa0` | `#454f8a` |
| Vurgu | `#f2c35a` | `#f2c35a` |
| Kâğıt katmanları | `#e39a3a`, `#c94a5a` | — |

## Üretim ve kayıtlar

`design/little-prince/build.py` paketi Snowgrave Frost'un yapısından üretir.
Lora Italic: SIL OFL 1.1 (değişken TTF, Türkçe harfler dahil).
Ortak dosyalarda: `theme_core.allowed` artık lisans dosyasıyla eşleşen her
`ad.ttf/.otf` fontuna izin verir; lisanssız font içeren paket yüklenmez
(`checks/test_theme_fonts.py`). Ayrıca `adapter_assets`, terminal vurgusu, Fastfetch alıntısı
ve picker UI testinin tema listesi.

## Kurulum

```fish
sudo python3 sddm/sync_setup.py install --user $USER --check
sudo python3 sddm/sync_setup.py install --user $USER
bash theme.sh check little-prince; and bash theme.sh apply little-prince
```

## Sınırlar

Hazırlama ortamında QML render'ları, sandbox apply/geçiş/rollback, adaptör fixture'ları ve
SDDM greeter UI testleri geçti. Gerçek Wayland oturumunda yarı saydam panellerin NVIDIA'da
ek yük getirip getirmediği, Spotify, Dolphin ve giriş ekranı kullanıcıda doğrulanacak.
