# Görsel yüzey haritası

2026-10-17 · **2.6.1 kaynak durumu**. Bu harita mevcut Plague Tale sunumunu
tanımlar. Yeni bir tema paketi yükleyicisi veya tema seçici uygulanmış değildir.
İkinci tema M4 sonrasında başlar. İşlevlerin kaynağı [özellik sözleşmesidir](FEATURE_CONTRACT.md).

## Shell içinde ortak sunum

| Kaynak | Sorumluluk | Davranış sınırı |
|---|---|---|
| `payload/style/shell/ui/Theme.qml` | Semantik palet, gövde/başlık font ailesi, font/motion ölçekleme, köşe/wallpaper URL'leri | Kullanıcı tercihlerini tüketir; uygulama veya oturum komutu yürütmez |
| `ui/SurfaceLayout.qml` | Bar/panel/OSD/toast/Alt+Tab dış ölçüleri, panel türü varsayılanları ve sınır hesabı | Mantıksal piksel; monitör çözünürlüğü/ölçeği değiştirilmez |
| `ui/OrnamentFrame.qml`, `Glyph.qml` | Çerçeve ve vektör çizimi | Şekil/geometri sunumdur; pil şarj/level değerini backend sağlar |
| `ui/PanelHeader.qml` | Yedi panelde ikon, başlık, durum, ek eylem ve kapatma | `closed` sinyali parent tarafından UiState'e bağlanır; ikinci durum makinesi yoktur |
| `ui/ActionButton.qml`, `SurfaceHint.qml` | Hover/focus/selected/disabled; koyu ve sarılabilen ipucu | Native komut içermez; parent eylemi bağlar |
| `ui/HintBubble.qml`, `payload/style/shell/HintPopup.qml` | Aynı bubble'ın Qt fallback veya ayrı native popup sunumu | 600 ms sonrası; native boş input maskesi, grabFocus:false; tıklamayı engellemez |
| `ui/NotificationActions.qml`, `ToastStack.qml` | Toast/geçmiş eylemlerinin genişlik sınırı; paylaşılan toast yığını | Aynı notification key/action backend'e gider; süre/DND/unread kopyalanmaz |
| `shell.qml`, `PreviewScene.qml` | Native pencere veya örnek sahne | Aynı ölçüler/sunum; yalnız native LiveContext gerçek servisleri kullanır |

`ui/` kısaltması `payload/style/shell/ui/` içindir. Gövde metinleri ve input/choice
fontları Theme.bodyFont kullanır; dekoratif başlıklar/saat Theme.displayFont seçer.
Boyutlar Theme.fontSize, açık animasyonlar Theme.duration üzerinden geçer.
Palet dışındaki literal shell QML renkleri import kontrolünde reddedilir;
`transparent` kompozisyon değeri buna dahil değildir.

Köşe SVG'leri kendi boyama verilerini taşır. Theme'de URL/ölçek seçilmesi bu SVG'lerin
otomatik yeniden renklendirildiği anlamına gelmez. Bir sonraki tema farklı varlık ve
şekiller kullanabilir. Yerel ikon koordinatları, kart içi aralıklar ve yazı boyutu
tercihleri hâlâ ilgili görsel bileşendedir; bütün sayılar tek dosyaya yığılmamıştır.

## Yüzeyler ve ortak işlevler

| Yüzey | Sunum | Ortak veri/işlev |
|---|---|---|
| Bar / tray / çalışma alanları | `ui/Bar.qml` | LiveContext workspace/tray; aynı native menü koordinatı ve eylem |
| Launcher / hesap | `ui/Launcher.qml` | Calculator.js; ortak application/copyText adaptörü |
| Güç menüsü | `ui/Power.qml` | UiState confirmation; backend.sessionAction |
| Ses / cihaz / ayarlar | `ui/Controls.qml`, `Settings.qml` | PreferencesState/Store ve ortak Python tercih kaynağı |
| Medya | `ui/Media.qml` | MPRIS oyuncu/seçim/kontrol adaptörü |
| Bildirim geçmişi / toast / DND | `ui/Notifications.qml`, `Toast.qml`, paylaşılan eylemler | NotificationWatcher ve LiveContext lifecycle; varsayılan 4500 ms korunur |
| OSD | `ui/Feedback.qml` | UiState feedback; volume/mic/brightness komutları ve IPC `feedback.present` |
| Donanım | `ui/Hardware.qml` | İhtiyaçta izleme; uyuyan GPU'yu uyandırmayan yardımcılar |
| Alt+Tab | `ui/WindowSwitcher.qml` | WindowSwitcherState MRU/iptal/seçim; native tek kare adaptörü |

Tema sunumu farklılaşabilir; bu tablodaki işlevler, onaylar ve kısayollar kaybolmaz.
Yeni tema içine Calculator/PreferencesState/backend komutlarının ikinci kopyası
konulmaz. Bu sürüm dinamik tema bileşeni seçen bir loader eklememiştir.

## Ayrı adaptörler ve yeniden yükleme sınırı

| Yüzey | Mevcut kaynak | Etkinleştirme / açık kabul |
|---|---|---|
| Hyprland görünümü | `payload/hypr/appearance.lua` | Ana kurucu/güncelleme ve Hyprland reload; monitör/GPU ayarı değildir |
| Wallpaper | `payload/hypr/hyprpaper.conf`, `payload/style/wallpaper.png` | Hyprpaper ayrı süreç; shell preview wallpaper URL'si tek başına oturum wallpaper'ını değiştirmez |
| Hyprlock | `payload/hypr/hyprlock.conf`, `scripts/lock-media.py` | Sonraki lock süreci; gerçek parola/media/unlock kabulü M4'te açık |
| SDDM | `sddm/theme/Main.qml`, `theme.conf`, varlıklar | Ayrı sistem kurucusu; preview gerçek sonraki login kabulü değildir |
| Dolphin | `apps/dolphin/DesktopStyle.colors`, ikon seti; `apps/manage.py` | Eklenti uygulama/yeniden açma; özel desktop girdisi ortak launcher/Super+E yolunda korunur |
| Spotify | `apps/spotify/color.ini`, `user.css`; `apps/manage.py` | Ayrı özel kopya/Spicetify apply ve yeniden açma; paket güncellemesinden sonra tekrar apply gerekebilir |
| Terminal / madalyon | Kitty payload'ı ve `terminal-medallion/` | Yeni terminal; madalyon ayrı kurucu/CP437–UTF-8 adaptörü; son görsel kabul açık |

Dolphin'in beyaz metinleri kullanıcının özel okunabilirlik tercihidir; shell'in
krem metnine körlemesine dönüştürülmez. Bu adaptörler Theme.qml'yi doğrudan
import etmez; shell rengini değiştirmek dış uygulamaları canlı güncellemez.
Gelecekte bunlar için üretim/apply/rollback gerekir; böyle bir üretici henüz yoktur.

## Kalan kapı

2.5.1 normal kullanımında sorun bildirilmedi. 2.6.0'da bar ipucu regresyonu
bildirildi; 2.6.1 düzeltmesi aynı dalda kabul bekliyor. Hazırlama kontrolleri
[VALIDATION](VALIDATION.md) içinde; native yeni başlık/hint/toast yerleşimi ayrıca
kontrol edilmeli. Ayarların restart sonrası kalıcılığı, lock/SDDM gerçek giriş,
çoklu ekran ve kapsamlı restore kabulü açıktır. Bu harita M3/M4'ü kapatmaz.
