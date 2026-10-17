## Bildirim / OSD / palet kontrolleri (2.2.6)

```bash
node checks/test_shell_backend.js
python3 checks/test_notification_watcher.py
python3 checks/test_shell_revisions.py
python3 checks/test_app_revision23.py
python3 checks/test_shell_syntax.py
```

Backend testi Node.js ve kontrollü servisler kullanır; gerçek D-Bus açmaz.
Watcher (4 test), shell-revisions ve app-revision23 için PySide6 gerekir;
app-revision23 ayrıca Node.js kullanır. PySide6 ayrı bir test dizinindeyse
`MCT_QT_TEST_PATH` onu içeren dizini belirtebilir; normal kurulumda gerekmez.
Syntax kontrolü Qt `qmlcachegen` ister: PATH'te yoksa `MCT_QMLCACHEGEN` tam
çalıştırılabilir dosya yoludur. Testler artık checkout'u kendi dosya konumundan
bulur; uygulama kurulumu veya kullanıcı oturumu üzerinde işlem yapmaz.

## Bağımsız PT-002 uygulama kontrolleri

```bash
python3 checks/test_spotify_install.py
python3 checks/test_app_installers.py
```

İlk komut 10 stdlib testi: sürüm uyarısı, aralık dışı sürümle devam etme, tema çıktısı,
fresh/update rollback, ilk yedek/adblock/restore, günlük ve salt okunur tanılama.
İkinci dosya artık checkout'u kendi konumundan bulur; Dolphin ve Spotify dosya
uygulama/restore örneklerini denetler. Native uygulama veya ağ çalıştırılmaz.

## Bağımsız PT-005 süreç tanıma kontrolü

```bash
python3 checks/test_session_discovery.py
```

Python stdlib ile 10 kontrollü test; gerçek süreç başlatmaz/durdurmaz.
HOME/XDG, taşınmış/symlink profil, restore kaydı, IPC ve ilgisiz shell ayrımı.

## Bağımsız PT-001 regresyon kontrolü

```bash
python3 checks/test_file_manager.py
```

Checkout kökünü kendi dosya konumundan bulur; Python stdlib yeterlidir. 12 kontrollü
test: başlatma girdisi, XDG/argümanlar, stock/manual/custom kısayol, fresh/update ve
restore/rollback. Gerçek GIO/Dolphin/Hyprland çalıştırılmaz.

## Önceki hazırlama kontrolleri

Bu klasör hazırlama sırasında çalıştırılan doğrulama kaynaklarını saklar.
Yukarıda taşınan kontroller dışındaki bazı testler hâlâ eski `build/` alanı,
1.4 masaüstü fixtureleri veya `tmp/` kaynakları ister. Önceki test ortamı PySide6
Essentials 6.10.2 ve QuickShell 0.3.1 kaynak kodlarıydı. Kullanıcı oturumunda
`bash update.sh --check` gerçek QuickShell QML derlemesini ve Hyprland durumunu
kontrol eder; offscreen Qt testinin yerine geçmeyen ayrı bir native kontroldür.

2.1 ek kontrolleri: test_shell_revisions.py gerçek Qt fare sürükleme/hover ve ikon merkezlerini; test_revision_helpers.py sensör hesapları, NVIDIA uyku durumu, Hyprlock metin/kapak yardımcıları ve bildirim üretmeyen OSD hata yolunu kontrol eder. Hyprlock alan adları için tmp/hyprlock-0.9.6/ConfigManager.cpp gerekir.

2.2: test_osd_routing.py, tmp/apps22/ipc-parser.cpp + CLI11.hpp (CLI11 2.5.0) ile derlenmiş tmp/apps22/ipc-parser dosyasını kullanır; eski show çakışmasını üretir ve üretim feedback.py çağrılarını gerçek ayrıştırıcıdan geçirir. test_app_installers.py uygulama eklentilerinin dosya işlemlerini ve hata sonrası geri dönüşünü denetler. Spotify patch işlemi bu testte kontrollü örnektir.


2026-10-17 GitHub temeli: bu dosyalar eski hazırlama çalışma alanından korunmuştur; bağımsız checkout CI paketi değildir. QA-001 ve ../docs/VALIDATION.md takip edilir.
