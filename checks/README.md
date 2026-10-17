Bu klasör hazırlama sırasında çalıştırılan doğrulama kaynaklarını saklar. Testler `build/` çalışmaalanı, 1.4 masaüstü fixtureleri, PySide6 Essentials 6.10.2 ve QuickShell 0.3.1 kaynak kodlarıyla çalıştırılmıştır. Testlerin bu bağımlılık ve klasör düzeni README'deki doğrulama sınırlarıyla birlikte değerlendirilmelidir. Kullanıcı oturumundaki kontrol için `bash update.sh --check` kendi QuickShell QML derlemesini ve canlı Hyprland durumunu kontrol eder.

2.1 ek kontrolleri: test_shell_revisions.py gerçek Qt fare sürükleme/hover ve ikon merkezlerini; test_revision_helpers.py sensör hesapları, NVIDIA uyku durumu, Hyprlock metin/kapak yardımcıları ve bildirim üretmeyen OSD hata yolunu kontrol eder. Hyprlock alan adları için tmp/hyprlock-0.9.6/ConfigManager.cpp gerekir.

2.2: test_osd_routing.py, tmp/apps22/ipc-parser.cpp + CLI11.hpp (CLI11 2.5.0) ile derlenmiş tmp/apps22/ipc-parser dosyasını kullanır; eski show çakışmasını üretir ve üretim feedback.py çağrılarını gerçek ayrıştırıcıdan geçirir. test_app_installers.py uygulama eklentilerinin dosya işlemlerini ve hata sonrası geri dönüşünü denetler. Spotify patch işlemi bu testte kontrollü örnektir.


2026-10-17 GitHub temeli: bu dosyalar eski hazırlama çalışma alanından korunmuştur; bağımsız checkout CI paketi değildir. QA-001 ve ../docs/VALIDATION.md takip edilir.
