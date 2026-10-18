## Son cila (2.6.2)

```bash
python3 checks/test_sddm_install.py
python3 checks/test_terminal_medallion.py
python3 checks/test_sddm_ui.py
python3 checks/test_shell_assets.py
MCT_HYPRLOCK_SOURCE=/path/to/hyprlock-0.9.6/ConfigManager.cpp python3 checks/test_revision_helpers.py
```

İlk iki komut stdlib ile 4 SDDM dosya transaction ve 6 medallion kontrolü yapar;
bütün yollar geçici köke yönlendirilir, gerçek installer/servis/oturum çalışmaz.
Greeter'in 5 Qt testi sahte SDDM modelleriyle parola hata/yeniden deneme/success
temizliği, çift login engeli, boş kullanıcı/oturum, güç Esc, küçük ekran
saat/kart ve klavye kaydırma kontrolüdür. PAM/gerçek giriş değildir.
`MCT_GREETER_PREVIEW_DIR=/tmp/greeter-review` isteğe bağlı render alır.

Qt testleri PySide6 ve gerekirse `MCT_QT_TEST_PATH` ister. Asset kontrolü artık
kendi checkout'unu kullanır; Theme URL'lerini ve repo PNG'lerinin tam decode'unu
denetler. Helper testi kendi payload'ını bulur; sensör/IPC süreçleri mock'tur,
Hyprlock property kontrolü için belirtilen 0.9.6 kaynak dosyası ayrıca gerekir.
Notification watcher fixture'ı Theme'in dolaylı Preferences.js import'unu içerir.
Bu düzenleme kalan `test_shell_fresh.py`, `test_shell_update.py`,
`test_osd_routing.py` eski fixture/binary bağımlılıklarını ortadan kaldırmaz.

## Ortak sunum / yerleşim (2.6.1)

```bash
python3 checks/test_shell_ui.py
```

12 gerçek Qt testi. PySide6 gerekir; ayrı kurulum için `MCT_QT_TEST_PATH` kullanılır.
Artık eski build/desktop-style ağacına bağlı değildir; checkout'u kendi bulur.
`MCT_UI_PREVIEW_DIR=/tmp/mct-review` isteğe bağlı beş PNG üretir; varsayılan test
repo içine görsel yazmaz. 7 panel, %90/%120 font, 1600×1000/900×600/640×480 sınırları;
bar 900/1132/1200/1600 genişlik, 0/1/12/40 tray; son simge sağ tık, medya/oturum
klavye görünürlüğü, güç onayı, uzun eylem ve boş veri kontrol edilir.
2.6.0 ayrıca yedi ortak başlığın kapatması, Controls ↔ Settings ve preview toast'ın
eylem/kapatma/panel açıkken gizlenmesini kontrol eder. Ortak `qmldir`, asset URL'leri
ve komponentler network import testinden de geçer; Theme dışı literal shell paleti
bu kontrolde reddedilir. Saydam kompozisyon ve SVG varlık verileri ayrı tutulur.
2.6.1: 200 ms'de gizli/700 ms'de görünür ipucu; düğmenin altında olma, açık ipucuna
rağmen gerçek fare tıklaması; basma/ayrılma iptali; owner değişince yeni süre;
bütün bar hint'lerinin native component bağlantısı ve QObject Loader bridge
yükleme/boşaltması denetlenir. Son test native pencere yerine QtObject kullanır.
API kontrolü PopupWindow/anchor/Region alanlarını 0.3.1 kaynağından, boş maskenin
WindowTransparentForInput ve grabFocus:false'ın ToolTip flag yolunu denetler.
Native Wayland/tray/power komutu çalışmaz. 900 altındaki kalabalık tray tam erişimi
bu kabulün kapsamı değildir. `test_preferences_ui.py` ortak Qt harness'ını kullanır.

## Ortak ayarlar (2.5.0)

```bash
python3 checks/test_preferences.py
node checks/test_preferences_model.js
python3 checks/test_preferences_ui.py
```

15 stdlib kontrolü: atomik dosya/0600, bozuk/eksik/sürümlü JSON, kayıt hatası,
yedekli reset, XDG, salt okunur tanılama, terminal argümanları, GIO, stok/özel Q ve
update/rollback'te dosyanın korunması. Node aynı şema JS doğrulamasını çalıştırır.
10 Qt testi (PySide6, `MCT_QT_TEST_PATH`) görünüm/slider/popup/klavye/reset ve üretim
storage-helper/model protokolünü kontrol eder. Gerçek QuickShell Process ve native
uygulama açılışı değildir. Schema JSON bloğunu değiştirmek iki doğrulayıcıyı da
etkiler; yeni alan testlerinde ikisini çalıştır.

## Launcher hesaplama (2.4.0)

```bash
node checks/test_calculator.js
python3 checks/test_launcher_calculator.py
python3 checks/test_shell_imports.py
```

İlk kontrol yalnız Node.js; aritmetik, uygulama sorguları, bozuk/eksik girdi,
512 karakter/256 token/32 derinlik sınırları ve 300 bozuk ifade denetimi yapar.
7 etkileşim testi gerçek PySide6 ile Enter/fare/Ctrl+Enter, normal Ctrl+C,
karma app/sonuç gezinmesi ve yerleşimi denetler. DemoContext clipboard değeri
fixture'dır; gerçek Wayland panosu değildir. `MCT_QT_TEST_PATH` desteklenir.
Import kontrolü kendi checkout'unu bulur, yerel HTTP sunucusunda Qt network
import yoluyla tam manifest ve göreli Calculator.js yüklemesini çalıştırır.
Native clipboard alanı ayrıca `test_shell_api.py` ve backend fixture'ında kontrol
edilir; hedef oturumda başka uygulamaya yapıştırma yine gerekir.

## Alt+Tab kontrolleri (2.3.0)

```bash
python3 checks/test_switcher_bindings.py
python3 checks/test_window_switcher.py
node checks/test_shell_backend.js
python3 checks/test_shell_syntax.py
MCT_QS_SOURCE=/path/to/quickshell-0.3.1 python3 checks/test_shell_api.py
```

Kısayol testi stdlib, pencere testi PySide6 ister (`MCT_QT_TEST_PATH` desteklenir).
11 Qt testi gerçek state/event/klavye ve 1600×1000 / 500×400 yerleşimini kullanır;
6 geçiş testi stock/idempotent/custom bağları kontrol eder. QtTest modifier-up
sentezlediği için fiziksel Alt basılıyken Tab-up doğrudan QKeyEvent ile iletilir.
API testi upstream **v0.3.1** kaynak checkout'u ister; uygulama kurmaz. Screencopy
native alanları header'dan, üç QtQuick.Item alanı açık temel listeden denetlenir.
Bu testler gerçek Hyprland odak geçişi/global kısayol/yakalama kanıtı değildir.

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

## Tema paket çekirdeği (2.7.0)

```bash
python3 checks/test_theme_core.py
```

28 stdlib testi, geçici kök ve fake runtime: paket/preview bütünlüğü, kaynak
eşitliği, path/symlink/şema/yüzey/hook redleri; readonly check, apply/iki varyant
rollback, dosya modları, preferences/keybind/backup korunması; config/readiness/
state kayıt hatasında otomatik geri dönüş; kesinti/commit journal toparlama;
manuel düzenleme, snapshot bozulması ve önceki kurulum epoch koruması; ortak
kilit ve gerçek updater'ın kilit içi koruması; idempotent apply, native wallpaper
komut argümanları ve yalnız MCT process seçimi. Fixture varyantı tmp altında
üretilir, ikinci ürün teması değildir.

GitHub workflow `theme-core.yml` bu suite'i ve 15 preferences / 12 file-manager
testini, Python/Bash syntax'ı çalıştırır. Başka eski checks dosyalarının hepsinin
CI'a taşındığı iddia edilmez. Native komutlar mock'tur; PAM/gerçek desktop yoktur.


## Deltarune paketi (2.8.0)

```bash
python3 checks/test_theme_core.py
python3 checks/test_deltarune.py
python3 checks/render_theme.py deltarune /tmp/deltarune-preview.png --panel media
```

İkinci komut PySide6 gerektirir ve mevcut etkileşim testlerini geçici Deltarune
köküne yönlendirir: 42 Qt testi. Yeni şerit testleri unavailable/0°C/mute/şarj,
font yükleme ve mevcut panel toggle bağlantısını denetler. Render komutu her yüzey
için taze süreçte gerçek QML ekran görüntüsü üretir; native Quickshell çalıştırmaz.
MCT_QT_TEST_PATH desteklenir. Core suite 29 stdlib/fake-runtime testidir.
