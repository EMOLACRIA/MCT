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
