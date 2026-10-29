<!-- theme-config-0.1.0 -->
# Tema ayarları — 29 Ekim 2026

Preferences paneli üç sekmedir: **Shell** (eski ayarlar, anında kaydedilir), **Layout**
(bütün temalarda ortak) ve **aktif tema** (yalnız o tema). Layout ve tema sekmesindeki
değişiklikler taslaktır; **Apply** basılınca uygulanır.

| Sekme | Ayar | Kapsam |
|---|---|---|
| Layout | Pencere arası boşluk 0–20, ekran kenarı 0–40, kenarlık 0–6, köşe 0–20 px; "Use each theme's own layout" | Bütün temalar |
| Tema | Duvar kâğıdı (masaüstü / kilit ekranı ayrı) | Aktif tema |
| Tema | İki satırlık cümle (≤18 karakter; harf, rakam, boşluk, `. , ! ? ' - : ; ( )`) | Aktif tema |
| Tema | 8 renk: accent, surface, raised, selection, text, secondary, line, warning (+ saydamlık) | Aktif tema |

Blur, gölge ve pencere animasyonu bilerek yoktur (NVIDIA + Hyprland kararlılığı).

## Nasıl çalışır

- Ayarlar `~/.config/mct/theme-config.json` (0600); seçilen resim
  `~/.config/mct/wallpapers/<tema>.png` olarak kopyalanır (JPEG/WebP için python-pillow
  ya da imagemagick gerekir; PNG doğrudan). Tema paketi hiç değişmez.
- Apply = normal tema geçişi: `theme_core` paketi doğrular, üstüne ayarları uygular
  (`payload/style/scripts/theme_config.py: resolve`) ve aynı işlemle kurar. Shell bir an
  yeniden başlar; `theme.sh rollback` geri alır. Sonuç `~/.local/state/desktop-style/
  theme-config-last.json` ve bildirim olarak gelir.
- Renklerin hepsi shell'i değiştirir. Accent ayrıca Hyprland kenarlığı, Kitty, Hyprlock,
  Fastfetch, Dolphin ve Spotify'a gider. Dolphin yazısı her durumda beyaz kalır.
- Cümle: kilit ekranında yalnız cümlesi olan temalarda (Gravity Falls, Spider-Punk,
  Little Prince) değişir; Fastfetch'te her temada. Fastfetch görseli Apply anında panelde
  temanın fontuyla çizilir; görsel cümle/accent ile eşleşmezse varsayılan cümle kalır.
- Panel MCT klasörünü `~/.local/state/desktop-style/theme-core/source.json` ile bulur;
  bu kayıt her tema apply'ında yazılır. Yoksa "Apply a theme once with Super+G" der.
- "Reset theme" o temanın ayarlarını siler (Apply sonrası onaylı görünüm). Rollback
  dosyaları geri alır ama kayıtlı ayarları silmez; panel bunu "Saved settings are not
  applied" diye gösterir.
- Bozuk ayar dosyası bütün tema uygulamalarını durdurur ve yolunu söyler; dosyayı düzelt
  ya da sil.

## Henüz yok (2. aşama)

- Giriş ekranı (SDDM) duvar kâğıdı: root yardımcısının kullanıcı resmini kabul etmesi ve
  yeniden `sudo sddm/sync_setup.py install` gerekir.
- Kitty/Dolphin/Spotify/kilit ekranının tam paleti (şimdilik yalnız accent).
- Super+G önizlemeleri paketin orijinal resmini gösterir.
