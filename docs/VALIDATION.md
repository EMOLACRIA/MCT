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
