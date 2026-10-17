# Doğrulama sınırları

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
