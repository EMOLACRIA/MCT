# Doğrulama sınırları

## 2.9.0 — Ortak davranış ve Deltarune adaptörleri (18 Ekim 2026)

Temiz geliştirme dalında son seri: **183 unittest vakası / 16 komut, tamamı geçti**.
PySide6 Essentials 6.10.2 offscreen/software; geçici HOME/dizinler, mock servisler.

| Komut (`checks/` altında) | Sonuç |
|---|---|
| test_theme_core.py | 33; ortak şablon tamper ve özel lock config koruması dahil |
| test_preferences.py / test_file_manager.py | 15 / 12 |
| test_theme_adapters.py / test_lock_layout.py | 5 / 3 |
| test_spotify_install.py / test_terminal_medallion.py / test_sddm_install.py | 10 / 6 / 4 |
| test_deltarune.py | 42; settings/tray/launcher/Alt+Tab ve paket revizyonu |
| test_shared_surfaces.py | 2; iki skin kaynak kopya koruması, 12 tur × 4 panel ve tek instance/onay temizliği |
| test_osd_themes.py | 1; iki ayrı Qt sürecinde gerçek mouse drag/hover/ikon sözleşmesi |
| test_greeter_themes.py | 10; iki skin'de aynı 5 giriş/boş model/yeniden deneme/power Esc testi |
| test_preferences_ui.py / test_shell_ui.py / test_launcher_calculator.py / test_window_switcher.py | Plague Tale 10 / 12 / 7 / 11 |

Qt komutları `MCT_QT_TEST_PATH` ile bu ortama yönlendirildi. `test_shell_imports.py`
ortak behavior/surfaces qmldir ve Calculator.js'i HTTP import yolunda yükledi.
`test_shell_syntax.py` **60 QML** bytecode derlemesi geçti (MCT_QMLCACHEGEN).
`test_shell_api.py` **132 native binding** için v0.3.1 kaynak sözleşmesini geçti
(MCT_QS_SOURCE). İki lock layout'unda **76 property binding** Hyprlock 0.9.6
ConfigManager.cpp beyanlarıyla eşleşti. `test_revision_helpers.py`, Node backend
ve preferences şeması kontrolleri de geçti. Python/Bash syntax ve belge linkleri
kontrol edildi. Genişletilen GitHub workflow aynı 183 vakayı çalıştıracak şekilde
kaynakla kaydedildi; yerel sonuç CI sonucu yerine sunulmaz.

Eski Loader bulgusu yaşam döngüsüyle giderildi: yalnız async/deferred denemeleri
uyarıyı bitirmedi; nihai lazy/kalıcı PanelSlot sonrasında önceki 12 tekrar ve iki
skin'in tekrarlı etkileşim testi geçti. Ara refactor sırasında OSD drag kontrolünde
bir başarısızlık da görüldü; nihai controller ve her skin için taze süreçli OSD
kontrolüyle son seride geçti. Eski başarısız kayıtlar final yeşil seriye karıştırılmaz.

Gerçek Wayland input/focus, PAM, sonraki SDDM girişi, çalışan Spotify/adblock ve
Dolphin, fiziksel sensör veya native kaynak upgrade burada çalıştırılmadı.
[Deneme ve geri dönüş sırası](UPGRADE_2_9.md). Fotoğraflı seçici henüz uygulanmadı.


## Bu checkout'ta çalıştırılabilen statik kontroller

Python dosyaları çalıştırılmadan `ast.parse` ile okunabilir; Bash dosyaları
`bash -n PATH` ile incelenebilir. Bu, gerçek masaüstü davranışını doğrulamaz.
Yeni docs bağlantıları ve kaynak listesi ayrıca kontrol edilir.

## Hedef kullanıcı oturumu

- `bash preview.sh`: ortak QML bileşenleri örnek veriyle normal pencerede.
- `bash update.sh --check`: kurulu görünüm + gerçek Hyprland/QuickShell ön kontrolü.
- `bash apps/install.sh dolphin --check` / `spotify --check`: uygulama eklentisi ön kontrolü.
- `bash apps/diagnose.sh`: mevcut sürümler/başlatıcılar ve Spotify başlangıç dosyaları.

`--check` son kullanıcı kabulünün veya native uygulama içeriğinin yerine geçmez.
Kurucuların gerçek uygulama adımları dosya/süreç değiştirir; preview ile karıştırılmaz.

## PT-001 için bağımsız regresyon kontrolü

Checkout kökünden `python3 checks/test_file_manager.py` (stdlib, 12 test).
Geçici dizin ve kontrollü servis/komut örnekleri kullanır; kullanıcının oturumunu,
dosyalarını veya servislerini değiştirmez. Native GIO/Dolphin/Hyprland testi değildir.

## PT-005 için bağımsız regresyon kontrolü

`python3 checks/test_session_discovery.py` — 10 stdlib testi. Süreç ve sinyal
işlemleri kontrollü örneklerle değiştirilir; gerçek süreçlere sinyal gönderilmez.
Profilin başka kullanıcı altında/başka dizinde bulunması ve ilgisiz shell/IPC
istemcilerinin korunması bu kapsamda kontrol edilir.

## PT-002 için bağımsız regresyon kontrolü

`python3 checks/test_spotify_install.py` — 10 stdlib testi. Sürüm uyarısı,
belgelenmiş aralık dışında preflight/uygulamaya devam etme,
eksik tema çıktısı, fresh/update rollback, adblock ortamı ve eylemleri, ilk yedek,
restore, gerçek stdout/stderr birleştirmesi ve salt okunur tanılama kontrol edilir.
`python3 checks/test_app_installers.py` de bağımsız checkout'ta çalışır.
2026-10-17: iki komut geçti. Spotify yerine geçici dosyalar/kontrollü CLI kullanılır;
hesap, gerçek Spotify/Spicetify veya ağ erişimi kullanılmaz.

## 2.2.6 Qt / bildirim kontrolleri

Checkout kökünde:

```bash
node checks/test_shell_backend.js
python3 checks/test_notification_watcher.py
python3 checks/test_shell_revisions.py
python3 checks/test_app_revision23.py
python3 checks/test_shell_syntax.py
```

Node testi üretim JS fonksiyonlarını kontrollü servislerle çalıştırır. Watcher
testi (4 vaka) gerçek Qt sinyal/event döngüsünü kullanır. OSD/ikon testi mevcut
PreviewScene'i; palet testi Qt QSettings/QPalette/QGraphicsWidget'ı kullanır.
23 QML bytecode kontrolü native QuickShell modüllerini instantiate etmez.
2026-10-17: hepsi Node.js ve Qt 6.10.2 ile geçti. PySide6 normal import yolunda
yoksa `MCT_QT_TEST_PATH`; qmlcachegen PATH'te yoksa `MCT_QMLCACHEGEN` kullanılır.
Gereken bağımlılık eksikse bu komutlar başarılı sayılmaz veya native teste dönüşmez.

### Hedef oturum kabulü

Yeni dal hedef Hyprland oturumunda `bash update.sh --check && bash update.sh`
ile uygulanır. Ses/parlaklık tuşları, OSD slider hover/drag, mute, Steam sağ tık,
pil şarj geçişi ve Dolphin'in aktif/pasif metni kullanıcı tarafından kontrol edilir.
Bu kaynak incelemesinde Dolphin renkleri ve OSD görünümü değiştirilmedi.

`notify-send` varsa süre ve aynı kartta yenileme kontrolü:

```bash
notify-send -t 4500 "Bildirim" "Yaklaşık 4,5 saniyede kapanmalı"
notice_id=$(notify-send -p -t 8000 "Aktarım" "Başladı")
notify-send -r "$notice_id" -t 8000 "Aktarım" "Yüzde 75"
```

İkinci/üçüncü komut aynı kartı günceller; unread ikinci kez artmamalı.
Süre dolunca toast/canlı eylemler kapanır, geçmiş metni kalabilir. `0` süreli
bildirimin toast'ı 4,5 saniye sonra saklanabilir; native bildirim canlı kalır.

## PT-010 Alt+Tab kontrolü

2.3.0 için `python3 checks/test_window_switcher.py` (PySide6, 11 test),
`python3 checks/test_switcher_bindings.py` (stdlib, 6 test), Node backend,
25 QML bytecode ve 99 native binding kaynak kontrolü 2026-10-17'de geçti.
API kontrolü `MCT_QS_SOURCE` ile QuickShell v0.3.1 checkout'unu alır;
Qt/derleyici bağımlılıkları yukarıdakiyle aynıdır. Kaynaklar/karar:
[ADR-0006](decisions/0006-window-switcher.md).

Hedef oturumda `bash update.sh --check && bash update.sh` sonrasında:

1. Alan 4 ve 9 gibi farklı alanlarda pencereler aç; Alt+Tab listesinde ikisini,
   başlıkları ve alan numaralarını gör. Alt basılıyken Tab/Shift+Tab ile dolaş;
   Alt bırakınca seçili pencerenin alanına geçip doğru pencereyi odaklamalı.
2. Hızlı Alt+Tab, tekrarlı Tab, sağ/sol Alt ve Alt basılı Esc iptalini dene.
   Esc sonrası Alt bırakma eski seçimi açmamalı. Enter ve fare seçimi de çalışmalı.
3. Seçili pencereyi dışarıdan kapat; yeni pencere aç; liste boşalsın. Kapanmış
   adres odaklanmamalı, liste seçim sırasında kendiliğinden yeniden sıralanmamalı.
4. İkinci ekran varsa farklı ölçeklerde dene: başladığı ekranda kalmalı;
   ekran çıkarıldığında veya dışarı odak gidince iptal edilmeli. Başka shell paneli
   açılması da seçimi iptal etmeli. Tek ekran kullanımı bu çoklu ekran kabulü değildir.
5. Desteklenen yakalamada tek kare görünmeli; görüntü çıkmasa da liste/odak/iptal
   çalışmalı. Kapalıyken yakalama devam etmemeli. `shell.log` hata kaydını kontrol et.
6. Özel Alt/Tab bağı varsa update bunu korur ve yeni bağ eklemediğini yazar;
   otomatik geçiş yapılmadığı durumda eski kısayolun çalışması beklenir.

17 Ekim kullanıcı Alt+Tab için “çok güzel çalışıyor” diyerek normal kullanımı
onayladı. Çoklu ekran çıkarma/yakalama ayrıntıları ayrıca raporlanmadı; M4 listesi
bu kabulü daha geniş test yapılmış gibi yorumlamaz.

## PT-011 Launcher hesaplama kontrolü

2026-10-17: `node checks/test_calculator.js`, `checks/test_launcher_calculator.py`
(7 gerçek Qt testi), `checks/test_shell_imports.py` (network JS import), Node
backend clipboard adaptörü, 99 native binding + clipboard kaynak karşılaştırması,
25 QML bytecode, 11 Alt+Tab Qt ve mevcut OSD/ikon + 12 update/restore kontrolü geçti.
PySide6 için `MCT_QT_TEST_PATH`, qmlcachegen için `MCT_QMLCACHEGEN` ve QuickShell
v0.3.1 kaynakları için `MCT_QS_SOURCE` aynı biçimde kullanılır. Network import
kontrolü yalnız yerel test HTTP sunucusunu açar; gerçek shell servisi açmaz.

Hedef oturumda update sonrası:

1. Super+R'de `(12+3)*4` yaz: 60 sonucu. Enter ve Copy ile ayrı ayrı kopyala;
   başka uygulamada Ctrl+V ile **60** gelmeli. Launcher ve ifade açık kalmalı.
2. `200*10%` → 20, `200+10%` → 200.1, `1,5+2.25` → 3.75, `2^-2` → 0.25.
3. `2+` tamamlanma mesajı, `1/0` hata göstermeli. Enter eski sonucu kopyalamamalı.
   Yeni girdi sonrası eski “Copied” durumu kaldırılmalı.
4. Uygulama araması/↑↓/Enter ve Esc/Super+R kapatma aynı çalışmalı. Sayıyla
   eşleşen uygulama varsa sonuç satırından aşağı geçerek açılabilmeli.
5. Sonuç varken Ctrl+Enter kopyalamalı; metin seçip Ctrl+C normal seçili ifadeyi
   kopyalamalı. Clipboard kontrolü başka uygulamaya yapıştırılarak yapılır;
   yalnız kartta “Copied” görmek native pano kabulü sayılmaz.

Preview hesaplar fakat DemoContext yalnız test pano değerini kaydeder; sistem
panosuna sonuç yazmaz. Gerçek clipboard yalnız kurulu QuickShell adaptöründedir.

## PT-012 Ortak ayarlar kontrolü

2026-10-17: `python3 checks/test_preferences.py` (15 stdlib),
`checks/test_preferences_ui.py` (10 gerçek Qt), `node checks/test_preferences_model.js`
geçti. 15 test geçici HOME/XDG ve kontrollü komutlar kullanır. Qt testlerinden üçü
üretim Python storage helper'ı ile saf modelin JSON alışverişini çalıştırır;
QuickShell Process modülünü instantiate etmez. Yeni panel/JS network import'u,
30 QML bytecode, 105 native binding + DesktopEntry categories/id kaynağı denetlendi.
Önceki launcher/Alt+Tab/OSD, 12 update/restore ve 6 Alt/Tab geçiş testi de geçti.

Hedef oturumda `bash update.sh --check && bash update.sh` sonrasında:

1. Ses/kontrol panelindeki dişliden Preferences aç; font/saydamlık/motion ayarlarını
   değiştir. Menü/OSD/bar/Alt+Tab okunaklı kalmalı; diğer paneller de tercihi almalı.
2. Bar floating/tarih/tray, yan panel ortalama ve OSD üst/alt seçeneklerini dene.
   Native bar reserve ve OSD yerleşimini gerçek monitör/ölçekte kontrol et.
3. Kapat/aç ve QuickShell'i `bash ~/.config/desktop-style/scripts/start.sh` ile yeniden
   başlat; tercihler korunmalı. Normal update ve rollback sonrası da dosya kalmalı.
4. Kurulu bir terminal seç; Super+Q ve Terminal=true uygulama aynı terminali açmalı.
   Dosya yöneticisini seçip Super+E'yi kontrol et; Dolphin seçiminde temalı desktop
   girdisi korunmalı. Özel Q/E bağı değiştirilmişse o komut korunmalıdır.
5. Tanılamada gerçek sürüm/path görünmeli. Reset önce onay istemeli; eski dosya
   preferences-before-reset-*.json olarak kalmalı. Preview bunu diskte yapmaz.

Bozuk dosya/kayıt hatası/korumalı alanlar otomatik fixture ile kontrol edildi;
canlı kullanıcı dosyasını sırf test için bozmak gerekmez. Gerçek Process, uygulama
başlatma ve restart kabulü raporlanmadan PT-012 kapanmaz.

17 Ekim PT-011 normal kullanım kullanıcı onayı kaydedildi. Bu, her clipboard alt
testinin tek tek bildirildiği anlamına gelmez; önceki ortam sınırları korunur.

## Bar ipucu tıklama regresyonu (2.6.1)

17 Ekim kullanıcı 2.6.0'da ipucunun anında düğmeyi örterek tıklamayı engellediğini
bildirdi. PR #9 onaylanmış veya ana dala alınmış sayılmadı. Aynı dalda düzeltme:
SurfaceHint 600 ms gecikme/iptal; native bar ayrı PopupWindow ve boş Region maskesi,
grabFocus:false; panel/preview ToolTip etkileşimsiz ve düğme dışındadır.

2026-10-17: `MCT_QT_TEST_PATH=... python3 checks/test_shell_ui.py` — **12 test geçti**.
Yeni üç test: gecikme/konum/açıkken tıklama ve basmada gizleme; owner değişimi ve
ayrılmada iptal; bütün bar hint'lerine native component aktarımı ve non-Item Loader
bridge yükleme/boşaltması. Native presenter bu son testte QtObject fixture'ıdır;
gerçek PopupWindow açıldığı anlamına gelmez. Qt 6.10.2 software/offscreen.

`test_shell_syntax.py` — **37 QML**; `test_shell_api.py` — **122 native binding**;
PopupWindow.anchor alanları ve Region kaynak sözleşmesine eklendi. 0.3.1
proxywindow.cpp boş non-null maskede WindowTransparentForInput; popupwindow.cpp
grabFocus false iken Qt::ToolTip flag yolunu doğruladı. Network import ve mevcut
ikon/OSD etkileşim kontrolü geçti. Kaynak/karar ek notu ADR-0010'dadır.

Hedef oturumda aynı dalda `git pull --ff-only`, ardından
`bash update.sh --check && bash update.sh`. İmleci barın bir düğmesine götür:
ilk anda ipucu olmamalı; kısa beklemeden sonra aşağıda görünmeli. Açıkken aynı
düğmeye basılabilmeli; imleç ayrılınca kapanmalı. Native scale/kenar yerleşimi ve
click-through son kabulü kullanıcı oturumundadır.

## M3 ortak shell sunumu (2.6.0)

17 Ekim: kullanıcı “Şuan bi sıkıntı yok gibi. Devam edelim” diyerek 2.5.1 normal
kullanımında sorun bildirmedi. PR #8 merge `3c8b1e0215be52fbf465ee696f4a98e0ca7e1456`.
Bu, bütün native tray/ölçek/kalıcılık alt testlerinin ayrı ayrı raporu değildir.

2026-10-17: `MCT_QT_TEST_PATH=... python3 checks/test_shell_ui.py` — **9 test geçti**.
Önceki 7 yerleşim testine yedi ortak başlığın close eylemi, Controls ↔ Settings,
paylaşılan preview toast eylemi/kapatma/panel açıkken gizlenmesi eklendi.
1600×1000 ve dar alan örnekleri; sarılan koyu ipuçları/uzun toast butonu görsel
olarak incelendi. Qt 6.10.2 software/offscreen kullanıldı; gerçek D-Bus yoktur.

Aynı tarihte: `test_preferences_ui.py` (10), `test_launcher_calculator.py` (7),
`test_window_switcher.py` (11), `test_shell_revisions.py` (ikon/OSD etkileşimi),
`test_shell_imports.py` (yeni qmldir ve network import, palet sınırı),
`test_shell_syntax.py` (**35 QML**), `test_shell_api.py` (**105 native binding**,
QuickShell 0.3.1 kaynak) geçti. Hazırlama kontrolü native Qt/Wayland popup kabulü
değildir. Yeni bir QuickShell API'si veya ayar şeması eklenmedi.

Hedef oturumda yeni dalı uygulayınca:

1. R/M/T/B ve medya/kontrol/ayar panellerinde başlık/kapatmayı dene; dişliyle
   Preferences, oradan Controls dönüşü çalışmalı. Kısayollar aynı kalmalı.
2. Uzun başlık/eylem taşıyan normal bir bildirime bak; toast ve geçmişte butonlar
   sığmalı. Hover ipucu koyu ve okunaklı, uzun metin sarılmış olmalı.
3. Bar/OSD konum ve reserve alanının önceki gibi kaldığını kontrol et. Yeni font
   aile bağları aynı varsayılanı kullanır; %90/%120 metin hâlâ okunmalı.
4. Önceki PT-012 restart/kalıcılık kabulü ayrıca açıktır. Native lock/SDDM gerçek
   login ve çoklu ekran geniş kabulü bu shell düzenlemesiyle kapanmaz.

Preview yeni ToastStack'i kullanır fakat sistem bildirimi almaz/göndermez. Kod
haritası [THEME_SURFACES](THEME_SURFACES.md); yeni tema/tema seçici yoktur.

## M3 ilk yerleşim denetimi (2.5.1)

17 Ekim: kullanıcı terminal ve Dolphin açılışını onayladı. PR #7 merge
`683686f68729ae58cf277d7fb174bb687dfd328a`; PT-012 restart/kalıcılık kabulü açık.

2026-10-17: `MCT_QT_TEST_PATH=... python3 checks/test_shell_ui.py` — **7 test geçti**.
Qt 6.10.2 software/offscreen: yedi panelin 1600×1000/900×600/640×480 sınırları,
%90/%120 font ve boş listeler; barın 900/1132/1200/1600 genişliğinde 0/1/12/40 simgesi;
gezintiyle son tray simgesine sağ tık; uzun medya adı/eylem sınırı ve klavye odağını
görünür tutma; küçük güç menüsü ve onay korunması. PNG'ler görsel olarak incelendi.
Bar için 900 mantıksal genişlik ve üzeri kontrol edildi; daha dar alanda kalabalık
tray'e tam erişim iddia edilmez. 640×480 kontrolü panel içeriği/sınırları içindir.

Aynı tarihte mevcut `test_preferences_ui.py` (10), `test_shell_revisions.py`
(ikon/OSD/drag/hover), `test_shell_imports.py`, `test_shell_syntax.py` (30 QML),
`test_shell_api.py` (105 native binding, 0.3.1 kaynak) ve Node backend kontrolü geçti.
Kontroller gerçek Qt render/etkileşimi veya kontrollü adaptörlerdir; native oturum
ve gerçek uygulama tekerlek/sağ tık kabulü yerine geçmez.

Hedef oturumda yeni dalı uyguladıktan sonra:

1. Normal ekranda saat/simgeler hizalı kalmalı. Tray çoksa oklarla son simgeye git;
   Steam sağ tık menüsü doğru yerde açılmalı, uygulama tekerlek eylemi korunmalı.
2. Ayarlarda %120 yazı seçip medya, güç ve bildirim paneline bak. Uzun oynatıcı
   adları/eylemler çerçeveyi aşmamalı; gerekince kaydırma çalışmalı.
3. Küçük kullanılabilir alanda Super+M, ↑/↓ ile son satıra git; seçili işlem görünmeli.
   Enter yalnız onay ekranına geçmeli; testi Esc ile kapatabilirsin.
4. PT-012 için ayarı kapat/aç ve normal shell restart sonrası korunduğunu ayrıca
   bildir. Uygulama açılışı onayı tek başına bu testi kapatmaz.

Bu revizyon ikinci tema veya tema değiştirici eklemez; M3/M4 tamamlanmış değildir.

## 2.6.2 — Son cila ve kabul sınırı

17 Ekim 2026, kontrollü HOME/dosya ve Qt 6.10.2 offscreen ortamı. Sürüm 2.6.2.
Bu komutların hepsi başarılı tamamlandı:

```bash
python3 checks/test_file_manager.py
python3 checks/test_session_discovery.py
python3 checks/test_spotify_install.py
python3 checks/test_app_installers.py
python3 checks/test_preferences.py
python3 checks/test_switcher_bindings.py
python3 checks/test_terminal_medallion.py
python3 checks/test_sddm_install.py
node checks/test_shell_backend.js
node checks/test_calculator.js
node checks/test_preferences_model.js
```

PySide6 erişimi için bu ortamda `MCT_QT_TEST_PATH` ayrı Qt 6.10.2 kurulumuna
ayarlandı. Aşağıdaki kontroller aynı ortam değişkeniyle geçti:

```bash
python3 checks/test_shell_ui.py
python3 checks/test_preferences_ui.py
python3 checks/test_window_switcher.py
python3 checks/test_launcher_calculator.py
python3 checks/test_notification_watcher.py
python3 checks/test_shell_revisions.py
python3 checks/test_app_revision23.py
python3 checks/test_shell_imports.py
python3 checks/test_shell_assets.py
python3 checks/test_sddm_ui.py
```

12/10/11/7/4 Qt suite testi; OSD/ikon ve palet etkileşimleri; network import;
17 PNG decode; 5 greeter testi. Watcher'ın ilk koşusunda fixture'a logic import
yolu eksikti; düzeltmeden sonra 4 test geçti. SDDM modeli sahtedir: parola gerçek
bir servise verilmez, reboot/powerOff sayaçtan ibarettir. 1600×1000 ve 640×480
render'ları görüntülenerek saat/kart/scroll sınırı incelendi. SDDM dosya kontrolü
4, CP437 testi 6 stdlib senaryosudur; ilk backup, symlink hedefi ve manuel dosya
değişikliği korunur. CP437 byte/UTF-8 eşitliği ve 61×29 / 39×17 boyutları geçti.

```bash
MCT_HYPRLOCK_SOURCE=/path/to/hyprlock-0.9.6/ConfigManager.cpp python3 checks/test_revision_helpers.py
MCT_QMLCACHEGEN=/path/to/qmlcachegen python3 checks/test_shell_syntax.py
MCT_QS_SOURCE=/path/to/quickshell-0.3.1 python3 checks/test_shell_api.py
```

Helper sensör/medya/OSD hata kontrolleri ve Hyprlock alanları; 37 QML bytecode,
122 native binding kontrolü geçti. 40 Python `ast.parse`, 26 `bash -n`, yerel
Markdown dosya yolları ve `git diff --check` geçti. Tam CI paketi iddiası yoktur.

### Hedef oturumda kalan kabul

Önceki normal kullanım onayları tekrar istenmez. Henüz ayrı kanıtı olmayanlar:

1. **Kalıcılık:** bir görünüm tercihini kaydet, paneli ve normal shell restart'ını
   dene; update/rollback sonrasında tercih ve özel kısayol/ofset korunmalı.
2. **Giriş/kilit:** ayrı SDDM preview; sonraki doğal girişte hesap/oturum seçimi ve
   gerçek giriş. Hyprlock parola hatası/başarı, seçili oyuncu, parça değişimi ve
   kontrol davranışı. Buradaki fake SDDM testleri bunları kapatmaz.
3. **Donanım:** şarj tak/çıkar, kayıp sensör/oynatıcı, çoklu oynatıcı, normal
   suspend/resume; imkân varsa ikinci ekran ve çıkarma/odak. Olmayan donanım için
   açık N/A kaydı tutulur; yapılmış sayılmaz.
4. **Uygulamalar/terminal:** Spotify adblock girdisinde tema + gerçek reklam
   engelleme; yeni terminalde CP437 madalyonunun bilgi sütunuyla son görsel onayı.
5. **Geri dönüş:** kullanıcı cihazında güvenli bir yedek/test oturumu planıyla
   fresh install/full restore; ilk backup, monitor/input/GPU ve özel dosyalar.
   Günlük oturum sırf test için kapatılmadı, hizmet restart edilmedi.

Güncel iki örnek: [Power](../previews/power.png), [SDDM](../previews/sddm.png).
M4, native kabul ve yayın/lisans maddeleri tamamlanana kadar açıktır. Tema
menüsünün konumu kullanıcı kararını bekler; bu cila arayüz eklemez.

## Kalan eski checks kaynakları

`checks/` hazırlama oturumunun test kaynaklarıdır. Bir bölümü çalışma alanında
`build/desktop-style`, eski 1.4 fixture'ı, `tmp/` altında upstream kaynak/binary ve
özel PySide6 kurulumunu arar. Bunlar temiz checkout içinde mevcut değildir.
Yukarıda belirtilenler dışındaki kontroller bağımsız test paketine dönüştürülmedi;
CI varmış gibi sunulmadı.
QA-001 bu borcu M1/M4 için izler. Gereksiz test dosyası eklemek yerine ilgili
kontroller bağımsız fixture/dependency düzenine taşınmalıdır.

Native Hyprland, QuickShell Wayland, gerçek Spotify/Dolphin/Steam ve güvenli
Hyprlock/SDDM oturumu hazırlama ortamında yoktur. Bu davranışlar hedef cihazda
kontrol edilmeden “tamamlandı” sayılmaz.

## 2.7.0 — Kullanıcı son kabulü ve yeni CLI çekirdeği

17 Ekim: kullanıcı önceki son canlı kontrol maddesinin tamamını bitirdiğini ve
gün boyu full kullandığını onayladı. Bu Plague Tale ürün/kullanım kapanışıdır;
aynı eski son kabul yeniden istenmez. Ayrı ayrı ölçüm/log sunulmuş sayılmaz.

Yeni çekirdek kodu `6d3b6f2eb9472256b49049e30c72efdb63ecc2a2`,
[GitHub Actions 39054714755](https://github.com/EMOLACRIA/MCT/actions/runs/39054714755):
`python3 checks/test_theme_core.py` **28**, preferences **15**, file-manager
**12** test; Python py_compile ve `bash -n theme.sh` geçti. Yerel executor
kullanılamadı; sonuçlar GitHub runner job log'undan okundu. Core testleri geçici
dosya kökü/fake runtime kullanır; gerçek servis, kilit veya oturum çalıştırmaz.

Bu koddan sonraki yalnız belge commit'i için Markdown dosya yolları ve trailing
whitespace JavaScript ile kontrol edilir; runtime testi tekrar çalıştırılmış
gibi gösterilmez. Yeni CLI'nin ilk native kabul komutları
[THEME_PACKAGES](THEME_PACKAGES.md) içindedir. Paket mevcut render'ı kullanır;
menü/ikinci tema yoktur. Adaptör otomasyonu sınırı ve update guard belgelenmiştir.


## 2.8.0 — Deltarune ilk deneme

2026-10-18: yerel Python 3, Node ve PySide6/Qt **6.10.2**; bütün UI testleri
`QT_QPA_PLATFORM=offscreen`, `QT_QUICK_BACKEND=software`. Qt bağımlılığı ayrı
hazırlama dizinindeydi; aşağıdaki Qt komutlarında `MCT_QT_TEST_PATH` kullanıldı.
Gerçek installer, servis devralma, güç veya kullanıcı oturumu çalıştırılmadı.

- `python3 checks/test_theme_core.py`: **29** geçici dosya/fake runtime testi.
  Yeni Deltarune → Plague Tale → iki rollback; tema özel font/portrelerin kaldırılıp
  geri gelmesi ve ilk backup/tercihlerin korunması dahil.
- `python3 checks/test_deltarune.py`: aynı mevcut sözleşme staged pakette **42**
  gerçek Qt testi: 10 ayar, 12 shell UI, 7 calculator, 11 Alt+Tab, 2 yeni parti.
  İlk ilave parti testinde QObject.findChild görsel delegate'i bulamadı; fixture
  mevcut visual_child yordamına geçirildi, tekrar koşuda 42 test geçti.
- Baseline `checks/test_preferences_ui.py`: **10**; `checks/test_shell_ui.py`:
  **12** geçti. Plague Tale'de opsiyonel alt şerit kapalıdır.
- `checks/test_preferences.py`: **15**, `checks/test_file_manager.py`: **12**;
  `node checks/test_shell_backend.js`: mevcut eylem/bildirim/tray kontrolü geçti.
- `checks/test_shell_syntax.py`: ortak **38** QML bytecode; geçici Deltarune
  kökündeki **38** QML ayrıca qmlcachegen ile derlendi.
- `checks/test_shell_api.py`: **132** native property/handler QuickShell **0.3.1**
  kaynaklarıyla eşleşti. Yeni pencerenin screen.width alanı ayrıca
  `src/core/qmlscreen.hpp` Q_PROPERTY(width) ile denetlendi.
- `checks/test_shell_imports.py`: tam qmldir ve network import geçti.
- **45** Python parse, **27** Bash syntax, **90** yerel Markdown dosya bağlantısı;
  `git diff --check` geçti. Paket load blob/PNG bütünlüğünü doğruladı.

`checks/render_theme.py` her yüzeyi ayrı taze Qt sürecinde render eder; bu,
çok sayıda test penceresi sonrasında software renderer'ın eksik dirty-region
karelerini yayın önizlemesi olarak kaydetmeyi önler. Preview PNG ile üç ilave
render 1600×1000 DemoContext'ten üretildi. Bu gerçek kullanıcı sensör verisi değil.

```bash
python3 checks/render_theme.py deltarune /tmp/deltarune-preview.png --panel launcher
```

Native Wayland/Steam tray sağ tık, her monitörde alt şerit reserve/odak,
1.6 ölçek font/ikon görünümü, fiziksel şarj/sensör, hyprpaper ve tema check/apply/
rollback hedef kullanıcı kabulünü bekler. Kullanıcının Plague Tale gün boyu
kullanım onayı bu yeni tema için uydurulmuş bir kabul kaydı sayılmaz.
Dış uygulama/SDDM/lock-auth/terminal madalyonu Deltarune uyarlamaları bu pakette yok.


### 18 Ekim — QuickShell sürüm gate regresyonu

Kullanıcının source update'i başarılı, tema check'i tam 0.3.1 regex'inde durdu.
Native kontrol güncelleyicinin minimum >=0.3.1 semver kuralına taşındı.
`python3 checks/test_theme_core.py`: **31 test geçti**; yeni iki test v önekli,
revision ekli, stdout/stderr, 0.3.1/0.3.2/0.3.10/0.4.0 ve eski/bozuk/boş çıktıyı
kontrollü preflight üzerinden denetler. İlk fixture stderr varyantında Hyprland
çıktısını da stderr'e taşıdı; yalnız QuickShell çıktısı değişecek şekilde
fixture düzeltildi ve suite yeniden geçti. Native Quickshell çalıştırılmadı;
kullanıcının asıl sürümü verilmedi, aday tema check/apply kabulü hâlâ bekleniyor.


### 18 Ekim — Deltarune 0.1.1 düzen ve wallpaper

`python3 checks/test_theme_core.py`: 31 geçti. `python3 checks/test_deltarune.py`:
42 geçti (10 ayar, 12 UI, 7 calculator, 11 Alt+Tab, 2 revizyon).
Önceki şerit testlerinin yerine 1600/900/640 genişlikte kontrol sağ/arama sol,
merkez tercih, görünür alt şeridin yokluğu, font ve 2048×1151 PNG'nin repo JPEG'iyle
decode piksel eşitliği denetlendi. Source ABI değişmedi; mevcut native opsiyonel
pencere/izleme koşulu flag false ile kapanır. Native ekran reserve/konum sonucu
bu revizyon için kullanıcı kabulünü bekliyor.

Launcher ve controls/media/osd/switcher Qt önizlemeleri taze süreçlerde yenilendi.
Native Hyprland oturumu ve fiziksel wallpaper IPC burada çalıştırılmadı.

## 2026-10-18 — Dolphin native geri bildirimi sonrası görsel düzeltme

Kullanıcı: rehber komutları çalışıyor, Dolphin dışındaki uyarlamalar değişmiş.
Fotoğrafta mavi/siyah palet + beyaz yazı, eski pirinç klasör ikonları görüldü.
Kaynakta 14 Deltarune SVG'si önceki paketle aynıydı; düzeltildi. Canlı yeni
Dolphin sonucu henüz alınmadı.

- `python3 checks/test_theme_adapters.py`: 5 test geçti; tema başına kurulan
  ikon dosyaları, farklılık, ilk yedek, orijinal kullanıcı ikonuna restore dahil.
- `MCT_QT_TEST_PATH=.../build/qs-qt-check python3 checks/test_app_revision23.py`:
  üç regresyon grubu geçti; gerçek Qt palette/kontrast, launcher göçü ve restore.
- Qt 6.10.2 QSvgRenderer: klasör/home/documents/download/music/pictures 16 ve
  80 px offscreen çizildi ve görsel incelendi. Bu, native Dolphin testi değildir.
- `git diff --check`: geçti.

Ortak shell/ABI değişmedi; 2.9 yükseltmesi tekrarlanmaz.

## 2026-10-19 — Fotoğraflı seçici / kullanıcı kabulü

19 Ekim 00:24 Europe/Riga kullanıcı Dolphin'in de değiştiğini onaylayıp devam
istedi. Önceki diğer uyarlamalar/komutlar çalışıyor beyanıyla Deltarune mevcut
kullanım/görünüm kabulü kaydedildi. Ayrı PAM/sensör alt testleri yapıldığı iddia
edilmez. Son Dolphin kaynak düzeltmesinin push/PR CI koşuları
[39141160782](https://github.com/EMOLACRIA/MCT/actions/runs/39141160782) ve
[39141164701](https://github.com/EMOLACRIA/MCT/actions/runs/39141164701) başarılı.

Yeni repo seçicisi için hazırlama ortamında:

| Komut | Sonuç / kapsam |
|---|---|
| `python3 checks/test_theme_core.py` | 33 geçti; mevcut core/transaction korumaları. |
| `python3 checks/test_theme_picker.py` | 4 geçti; readonly katalog/bozuk paket, check/apply/noop/rollback, failed start recovery ve manuel dosya koruması, bağımsız başlatma. Fake native runtime. |
| `MCT_QT_TEST_PATH=.../build/qs-qt-check python3 checks/test_theme_picker_ui.py` | 5 geçti; gerçek Qt fotoğraf yükleme/seçim, check ömrü/hata, ikinci geri dönüş onayı, Esc, 1080×760/640×480/480×400 düğme sınırları, kaydırma, pending/bozuk/boş katalog. Helper istekleri yakalanır, uygulanmaz. |
| `MCT_QMLCACHEGEN=.../qmlcachegen python3 checks/test_shell_syntax.py` | Payload + seçicinin 65 QML dosyası bytecode'a derlendi; eski iki syntax hatası negatif kontrolle yakalandı. |
| `MCT_QS_SOURCE=.../quickshell-0.3.1 python3 checks/test_shell_api.py` | 152 native property/handler kaynağa uyuyor; seçici FloatingWindow/Process dahil. Gerçek QS instance testi değildir. |
| `python3 -m py_compile theme_picker.py checks/test_theme_picker.py checks/test_theme_picker_ui.py`; `bash -n theme.sh`; `git diff --check` | Geçti. |

Qt render'ları normal ve küçük boyutta görsel incelendi. İlk koşuda 760 px
pencerede işlem düğmelerinin kısmen dışarıda kaldığı bulundu; sabit footer'a
alındı ve fare/input/bounds kontrolleri yeniden geçti. Native Process stdout/
close sıralaması, ana shell restart'ı sırasında pencerenin kalması ve gerçek
Wayland tema apply/rollback yeni arayüzle cihazda henüz çalıştırılmadı.
SDDM/uygulama/PAM işlemi yapılmadı. ABI/kurulu shell dosyaları değişmedi.

## 2026-10-19 01:07 talebi — Wayland tema çizgisi

Kullanıcı ilk seçiciyi yeterince stilize/rahat bulmadı; normal uygulama ve iki
adımlı geçişi değiştirmeyi istedi. Kabul edilen tasarım: orta yatay çizgi, hover
fotoğrafı, tek seçim/apply, canlı boşsa Super+G. İlk seçici kabul edilmiş sayılmaz.

Hazırlama ortamı kontrolleri:

- `python3 checks/test_theme_picker.py`: 4 geçti; katalog/bozuk paket, core
  check/apply/noop/rollback/recovery, warm IPC toggle ve yalnız yoksa daemon
  başlatma. Gerçek session process seçicisi overlay'i masaüstü shell'i saymıyor.
- `python3 checks/test_theme_bindings.py`: 5 geçti; geçici config ve fake canlı
  binds. Readonly check, dolu G/keycode/okunamayan veri, idempotent kurulum/ilk
  binding yedeği, özel blok koruması, reload hatası geri dönüşü, unbind sonrasındaki
  yeni kullanıcı bağlarının kalması. Hiç gerçek compositor değişmedi.
- `MCT_QT_TEST_PATH=.../build/qs-qt-check python3 checks/test_theme_picker_ui.py`:
  5 geçti; hover seçimi apply değil, click/Enter tek apply, busy duplicate red,
  hata/aktif kayıt, restore onayı, Esc, 1600×1000/900×600/640×480/480×400 ve
  %90/%120 yazıda orta çizgi/fotoğraf sınırları; animasyon ve reduceMotion.
  Asenkron image testinde sabit bekleme yerine gerçek Ready durumuna sınırlı
  beklenir. D→PT font değişimindeki boş URL uyarısı font kaynağını koruyarak giderildi.
- `MCT_QMLCACHEGEN=.../qmlcachegen python3 checks/test_shell_syntax.py`: 65 QML
  geçti. Kullanılmayan PickerButton kalktı; native-only validate.qml eklendi.
- `MCT_QS_SOURCE=.../quickshell-0.3.1 python3 checks/test_shell_api.py`: 159
  native property/handler kaynağa uyuyor. Layer/IPC tipi gerçek compositor testi değil.
- Python compile, `bash -n theme.sh` ve `git diff --check` geçti.

Qt render'ında demo backdrop ile çizgi/hover sunumu incelendi; canlı ekran
fotoğrafı değildir. Yeni PanelWindow/IPC toggle, exclusive odak, Super+G'nin
boşluğu ve Lua reload'u hedef oturumda binder tarafından kontrol edilmeli.
Burada kullanıcının klavyesine bağ eklenmedi; yeni native kabul bekler.
Ortak payload/ABI değişmedi ve ana restore yedeği değiştirilmedi.

Binding adapter'ı yayımlanmadan önce 0.56.2 `hlBind` birincil kaynağı ayrıca
okundu: Lua `__lua` + değişken registry ref üretir. İlk taslaktaki `exec`/command
JSON varsayımı bu nedenle kaldırıldı. Yeni fixture gerçek Lua biçimini ve ref
42→84 değişimini denetler; 5 test tekrar geçti. Native canlı reload sonucu
hâlâ kullanıcı oturumundaki bind kurucusuna aittir.
# 19 Ekim — Deltarune 0.3.0 görsel revizyonu

Yerel offscreen Qt 6.10.2, `MCT_QT_TEST_PATH=build/qs-qt-check` bağımlılık
diziniyle 112 unittest geçti: `test_deltarune` 42, `test_theme_core` 33,
`test_theme_adapters` 5, `test_greeter_themes` 10, `test_shared_surfaces` 2,
`test_osd_themes` 1, `test_lock_layout` 3, `test_terminal_medallion` 6,
`test_theme_picker` 4, `test_theme_picker_ui` 6. Komutlar `python3 checks/NAME.py`.

Yeni picker yükseltme kontrolü eski aktif sürümün yeniden uygulanabilir olmasını
ve yeni sürüm sonrası noop'u denetler. İlk koşuda eski fixture'ın sabit 0.2.0
değeri eski sürümü gerçekten güncellenebilir gösterdiği için noop beklentisi
başarısız oldu; fixture aktif sürümü katalogdan okuyacak şekilde düzeltildi.
Kaynakta bu nedenle core/picker davranışı değiştirilmedi.

`test_shell_syntax.py`: **116 QML** bytecode derlemesi geçti; kontrol artık
paketlerin görsel QML skin'lerini de kapsar. `test_shell_imports.py` network Qt
imports ve palet ayrımını doğruladı. İki Engine.load manifest/bütünlük kontrolü,
değişen Python parse, Bash syntax, yerel belge linkleri ve diff whitespace geçti.
Wallpaper decode piksel eşitliği mevcut Deltarune testinde korunur (1200×675).

Gerçek QML launcher/medya/controls/OSD/switcher render'ları ve sahte SDDM
1600/900/640 render'ları üretildi; launcher/medya/controls/login görsel incelendi.
Paket preview'sı QML launcher render'ıdır; AI konseptiyle karıştırılmaz.

Installer'lar geçici dizin/mock altında test edildi. Gerçek Hyprland/QuickShell
servis devralma, PAM/login, kullanıcı cihaz tuşları veya Spotify/Dolphin uygulaması
bu ortamda çalıştırılmadı; yeni native görünüm/kullanım kabulü beklenir.
