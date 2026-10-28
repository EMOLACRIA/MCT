<!-- gravity-falls-0.1.0 -->
# Gravity Falls 0.1.0 — 28 Ekim 2026

Altıncı bağımsız tema paketi: `gravity-falls`, ABI `mct-shell-2.9`. Düzen mevcut
beş temayla aynıdır (yüzen paneller, ortak işlevler, kısayollar); ortak shell
(`payload/style/shell`) değişmez, `update.sh` gerekmez.

## Fikir: günlük ve şifre

Kasaba sıradan görünür, her yüzeyin altında bir sır vardır. Masaüstü sakin bir
alacakaranlık ormanıdır; sırlar ayrıntılardadır:

- Kilit ekranı ve Fastfetch, Sezar +3 ile şifrelenmiş bir cümle gösterir:
  `WKH ZRRGV UHPHPEHU ZKDW WKH WRZQ IRUJHWV.` (her harfi üç geri kaydırarak okunur).
- Üzerine gelinen ve seçilen öğe ısınır; vurgu eski tabelanın turuncusudur.
- Panel köşelerinde günlüğe yapıştırılmış fotoğraf gibi iki kâğıt bant.
- İki ses: daktilo (Courier Prime) saat ve başlıklarda; sistem metni masaüstünün sans-serif'i.

Dizinin karakter, sembol ve logoları kullanılmaz. Duvar kâğıdı kullanıcının seçtiği
resimdir, renkleri değiştirilmez.

## Palet (Alacakaranlık)

| Rol | Renk |
|---|---|
| Panel | `#140f12` |
| Yükseltilmiş / üzerine gelme | `#2c1f1b` |
| Seçim | `#3e2a1f` |
| Çizgi | `#4a3429` |
| Metin (kâğıt) | `#f4e7d0` |
| İkincil | `#b39e8c` |
| Vurgu (tabela turuncusu) | `#f0a84a` |
| Hata | `#e0574a` |
| Çam yeşili | `#9cc28a` |

Kitty ANSI renkleri ayrı ve okunur tutuldu (kırmızı, çam yeşili, kehribar, alacakaranlık
mavisi, gökyüzü moru, turkuaz).

## Kaynak ve üretim

`design/gravity-falls/build.py` paketi Snowgrave Frost'un yapısından üretir: bütün
adaptör renkleri rol eşlemesiyle taşınır, Theme/OrnamentFrame/Bar, Kitty, Hyprland,
Hyprlock, terminal medallion ve Fastfetch şifre görseli yazılır.
Courier Prime: SIL OFL 1.1 (npm `@fontsource/courier-prime` 5.3.0, latin alt kümesi,
WOFF2'den TTF'e çevrildi). Kaynak ayrıntısı: `themes/gravity-falls/provenance.json`.

## Ortak dosyalarda değişenler

- `theme_core.allowed`: `courier-prime-regular.ttf`, `courier-prime-bold.ttf`,
  `courier-prime-license.txt` (kullanıcı onayı 28 Ekim).
- Kimlik kayıtları: `adapter_assets.THEMES`, terminal vurgusu, `fastfetch_quotes.QUOTES`.
- `checks/test_theme_picker_ui.py`: altı kartlı şeritte kartı görünür yapar.

## Kurulum

```fish
sudo python3 sddm/sync_setup.py install --user $USER --check
sudo python3 sddm/sync_setup.py install --user $USER
bash theme.sh check gravity-falls; and bash theme.sh apply gravity-falls
```

## Sınırlar

Hazırlama ortamında QML render'ları, sandbox apply/geçiş/rollback, Dolphin/Spotify/terminal
adaptör fixture'ları ve SDDM greeter UI testleri geçti. Gerçek Wayland oturumu, Spotify,
Dolphin ve giriş ekranı kullanıcıda doğrulanacak. Courier Prime latin alt kümesi
Türkçe özel harfleri içermez; Qt bu harflerde yedek fonta düşer.
