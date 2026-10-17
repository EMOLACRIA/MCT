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

## Eski checks kaynakları

`checks/` hazırlama oturumunun test kaynaklarıdır. Bir bölümü çalışma alanında
`build/desktop-style`, eski 1.4 fixture'ı, `tmp/` altında upstream kaynak/binary ve
özel PySide6 kurulumunu arar. Bunlar temiz checkout içinde mevcut değildir.
Bu görevde bağımsız test paketine dönüştürülmedi ve CI varmış gibi sunulmadı.
QA-001 bu borcu M1/M4 için izler. Gereksiz test dosyası eklemek yerine ilgili
kontroller bağımsız fixture/dependency düzenine taşınmalıdır.

Native Hyprland, QuickShell Wayland, gerçek Spotify/Dolphin/Steam ve güvenli
Hyprlock/SDDM oturumu hazırlama ortamında yoktur. Bu davranışlar hedef cihazda
kontrol edilmeden “tamamlandı” sayılmaz.
