# Deltarune tamamlama denetimi

18 Ekim 2026 · Kaynak 2.8.0 / paket 0.1.1.
İncelenen uzak commit: `7ae39b6086270d28df847c4e14831b1195d061c3`.
Yerel eşdeğer kaynak ağacı: `65c6d0e3c26f59a962f4940920568e0a13b4ad9a`.

**Sonuç: ikinci tema bütün masaüstü kapsamıyla tamamlanmış değil.** Komut satırı
geçiş çekirdeği var; fotoğraflı seçici arayüzünün uygulanmasına bu denetimle
geçilmedi. Kullanıcı önce eksik kontrolü, sorun yoksa tema değiştirme aşamasını
istedi. Menü konumu hâlâ seçilmedi.

## Açık bulgular

| Öncelik | Bulgu | Kaynak / kapanış koşulu |
|---|---|---|
| P1 | Hızlı panel geçişi ve yeniden boyutlandırmada Loader uyarısı tekrar üretildi. | Deltarune `Overlay.qml` içindeki Loader / `Launcher.qml`: `Cannot create delegate`, `Object or context destroyed during incubation`. Offscreen Qt bulgusu; native Wayland'de görünür bozulma olduğu henüz kanıtlanmadı. Nedeni ayrıştırılıp tekrarlı panel testi uyarısız geçmeli. |
| P1 | Ortak davranış ile tema görünümü ayrımı tamamlanmadı. | İki pakette `Power.qml`, `Controls.qml`, `Settings.qml`, `Notifications.qml`, `WindowSwitcher.qml` birebir aynı ayrı dosyalar. Launcher filtre/seçim/kopyalama, güç onayı/klavye ve OSD commit bağlantıları tema view'larında. Ortak backend düzeltmeleri paylaşılır; view davranışları otomatik paylaşılmaz. Ortak davranış tek kaynağa alınmalı ve iki sunum aynı etkileşim testlerinden geçmeli. |
| P2 | Hyprlock'un yalnız medya bölümü uyarlanmış. | `payload/hypr/hyprlock.conf` parola, saat ve tarih için hâlâ ilk temanın serif/krem/pirinç sunumunu taşır. Yeni wallpaper ve medya renkleri tam lock uyarlaması değildir. Güvenli parola akışı korunarak Deltarune sunumu tamamlanmalı. |
| P2 | SDDM, Dolphin, Spotify ve terminal süsü Deltarune'a uyarlanmamış. | Manifest'teki üç `separate-installer` kaydı gerçek Deltarune adaptörü değildir. `sddm/theme/Main.qml`, `apps/dolphin/`, `apps/spotify/` ve `terminal-medallion/` önceki görünümü taşır. Kitty paleti uyarlanmıştır. Ayrı adaptörlerin seçim/kurulum/restore sınırı tamamlanmalı; uygulamalar canlı değişmiş gibi sunulmamalı. |
| Kabul | Son 0.1.1 yerleşiminin native görsel kabulü açık. | İlk Deltarune'un hedef oturumda açıldığı kullanıcı ekran görüntüsüyle biliniyor. Sağ kontrol, kaldırılmış alt şerit, yeni wallpaper ve 1.6 ölçekli fontun son revizyon kabulü ayrıca gelmedi. Plague Tale'in gün boyu kullanım onayı tekrar istenmez. |

SDDM veya harici uygulama kurucuları bu denetimde çalıştırılmadı. Parola/giriş,
gerçek tray menüsü, donanım veya Wayland odak işlemi yapılmadı. Mevcut wallpaper
2048×1151; panel/font/çerçeve tercihleri ve aynı kısayollar ürün kapsamındadır.

## Yapılan kontroller

Testler mevcut çalışma dizininin commit dışı görsel değişikliğine dokunmadan,
incelenen commit'in geçici ve temiz kopyasında çalıştırıldı. PySide6 Essentials
6.10.2, offscreen/software render; servis komutları ilgili testlerde mock.

| Komut | 18 Ekim sonucu |
|---|---|
| `python3 checks/test_theme_core.py` | 31 geçti; gerçek iki paket arasında apply/switch/rollback, tema özel font/portre temizliği, ilk yedek/tercih koruması dahil. Native runtime sahte. |
| `python3 checks/test_preferences.py` | 15 geçti. |
| `python3 checks/test_file_manager.py` | 12 geçti. |
| `python3 checks/test_deltarune.py` | İlk koşuda 42 testin 1'i Loader uyarısıyla başarısız; ikinci tam koşuda 42 geçti. Yeşil tekrar ilk başarısızlığı kapatmaz. |
| `python3 -m unittest discover -s checks -p test_preferences_ui.py` | Varsayılan Plague Tale'de 10 geçti. |
| `python3 checks/test_shell_ui.py` | Plague Tale'de 12 geçti. Aynı 12 kontrol Deltarune suite'inin de parçası. |
| `python3 checks/test_switcher_bindings.py` | 6 geçti; kişisel bağlar korunur. |
| `node checks/test_shell_backend.js` | Bildirim yaşam döngüsü, tray/komut yönlendirme ve terminal/odak/yakalama kontrolleri geçti. |
| `node checks/test_calculator.js` | Aritmetik ve 300 bozuk ifade kontrolü geçti. |
| `python3 checks/test_shell_revisions.py` | İki ayrı staged görünümde de ikon merkezleri, OSD hover/drag, parlaklık release ve donanım toggle kontrolü geçti. |
| `python3 checks/test_shell_syntax.py` | İki staged görünümün her birinde 38 QML bytecode derlemesi geçti. |
| `python3 checks/test_shell_api.py` | v0.3.1 kaynak beyanlarına göre 132 native binding kontrolü geçti. |
| `python3 checks/test_revision_helpers.py` | Sensör/mock, uyuyan GPU koruması, lock medya ve OSD'nin bildirim fallback'i kullanmaması geçti; Hyprlock 0.9.6 kaynak alanları kontrol edildi. |

Qt komutları `MCT_QT_TEST_PATH`; syntax/API/helper komutları sırasıyla
`MCT_QMLCACHEGEN`, `MCT_QS_SOURCE`, `MCT_HYPRLOCK_SOURCE` ile yerel bağımlılığa
yönlendirildi. Bunlar kullanıcı cihazında native kabul değildir.

Loader için ayrıca aynı pozisyon testinin 12 yeni fixture ile tekrarı yapıldı;
9 koşu aynı uyarı yüzünden başarısız oldu. Sadece paralel yükten kaynaklandığı
varsayılmadı. Tekrar komutu (Qt ortamı hazırken, checkout kökünde):

```python
import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, 'checks')
import test_deltarune as d
with tempfile.TemporaryDirectory() as folder:
    d.theme_preview.stage('deltarune', Path(folder) / 'payload')
    d.qt.ROOT = Path(folder)
    suite = unittest.TestSuite(
        d.DeltaruneRevisionTests(
            'test_controls_right_launcher_left_and_center_preference_preserved')
        for _ in range(12))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
```

## Tamamlama sırası

Önce Loader bulgusu ayrıştırılır ve ortak etkileşim/görsel ayrımı bitirilir.
Ardından lock/SDDM ve uygulama/terminal sunum eksikleri kapatılır. İki tema aynı
özellik sözleşmesinden geçtikten sonra fotoğraflı tema değiştirme arayüzüne
geçilir. Seçicinin konumu bu denetimde kararlaştırılmadı.
