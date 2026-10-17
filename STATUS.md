# Güncel durum

Son inceleme: **2026-10-17**. Kaynak taban: **2.2.5 geliştirme sürümü**.
Aşama: **M0 tamamlandı; M1 — mevcut kurulumu sağlamlaştırma**. Plague Tale tamamlanmış değildir.
Bu kayıt uygulamaları kullanıcının cihazında çalıştırmış gibi yorumlanamaz.

## Kaynakta bulunanlar

QuickShell bar; launcher; güç menüsü; kontrol paneli; bildirim geçmişi/toast/DND;
MPRIS medya; donanım paneli; sürüklenebilir OSD; pil/şarj durumu; Hyprlock medya
bölümü; ayrı SDDM teması; Dolphin/Spotify eklentileri; kurulum/güncelleme/restore.
`Theme.qml` vardır fakat bütün görsel değerler henüz bu dosyada toplanmış değildir.
Ayarlar ekranı, Alt+Tab seçici, launcher hesaplama ve tema değiştirici **yoktur**.

## Son kullanıcı geri bildirimi ve açık işler

| Kimlik | Durum | Kanıt / sonraki adım |
|---|---|---|
| PT-001 | Doğrulandı | 2026-10-17: kullanıcı PR #1 dalını uygulayıp launcher/Super+E tutarlılığını “Aynen çalışıyor” diyerek onayladı. Kod: `62cfe809d0274fd2ec99a8aca4e37f117b20fe9f`; 12 regresyon kontrolü de geçti. |
| PT-002 | Çalışma onaylandı / adblock sonucu ayrıca ölçülmedi | 17 Ekim: kullanıcı “Yo çalışıyo bende” diyerek Spotify'ın çalıştığını onayladı. Sistem Spotify 1:1.3.4.258-2, adblock 1:1.1.1-1, CLI 2.45.3-1. Girdiler temalı sarmalayıcıya yönleniyor ve LD_PRELOAD korunmuş. Belgelenmiş Linux aralığı dışında olmak hata kanıtı değildir; 2.2.5 yalnız uyarı verir. Özel kopyanın kesin sürümü ve reklam engelleme ölçümü kayıtlı değil. |
| PT-003 | Canlı doğrulama bekliyor | Dolphin yazıları/ikonları zor okunuyordu. 2.2.2 beyaz normal/seçili metin ayarı kaynakta; bütün başlatma yolları kontrol edilmedi. |
| PT-004 | Canlı doğrulama bekliyor | OSD 2.2.0 IPC `present` düzeltmesi; önceki raporda tuşlar çalışıyor fakat OSD yoktu. Son gerçek sonuç ayrıca kaydedilmeli. Steam menüsü/şarj durumu da kabul kontrolünde. |
| PT-005 | Uygulandı / hedef oturum doğrulaması bekliyor | 2.2.4: mevcut HOME/XDG HyprCade profilleri veya ilk yedekte kayıtlı tam komut seçicileri kullanılır. IPC/list/kill/log istemcileri shell sayılmaz. 10 kontrollü süreç keşfi testi geçti; gerçek sinyal gönderilmedi. |
| QA-001 | Kısmen açık | File-manager, session-discovery, spotify-install ve app-installers kontrolleri bağımsız checkout içinde çalışır. Diğer eski kontroller çalışma alanı/Qt fixturelerine bağlı; genel CI henüz yok. |
| ASSET-001 | Entegrasyon / canlı doğrulama bekliyor | Kullanıcı `terminal-medallion/` kaynaklarını ilk MCT commit'ine ekledi; README, kurucu ve CP437/UTF-8 çizimler doğrulandı. Ana temayla son kurulum/görünüm kabulü henüz yapılmadı. |

## Önceki hazırlama kontrolleri

Önceki oturumlarda bildirilen sonuçlar: Qt 6.10.2 render/etkileşim, QML bytecode,
QuickShell 0.3.1 kaynak API karşılaştırması, yardımcı script ve dosya rollback
fixtureleri. Bunlar native Hyprland/Spotify/Dolphin/Steam/Hyprlock oturumu değildir.
2.2.1 testleri adblock Exec ortam/argüman koruması, JS modül yükleme sırası ve Qt
aktif/pasif metin paletini kontrollü örneklerle denetledi. 2.2.2 beyaz palet
rolleri okundu. Ayrıntılar eski kurulum belgesi ve `checks/README.md` içinde.

## GitHub başlangıcı

- [x] Kullanıcı tam kaynakları `EMOLACRIA/MCT` ana dalına pushladı.
- [x] Başlangıç commit'i: `dd146961f82e2a02034152e9ba6e3501ee4af5e1` (2026-10-17).
- [x] AGENTS, brief, roadmap ve kabul sözleşmeleri depodan tekrar okundu.
- [x] Vitreus/Caelestia referansları korundu; yeni tema veya runtime göçü başlamadı.

## Bu revizyondaki doğrulama

2026-10-17: `python3 checks/test_file_manager.py` — **12 test geçti**.
User/system desktop önceliği, XDG yolları, argümanların ayrı tutulması, eklenti
restore sonrası yeniden çözümleme, eksik GIO/exec hata yolu, stock/manual/custom
kısayollar, fresh install/full restore, update preflight/update/rollback ve
başarısız update geri dönüşü kontrollü örneklerle denetlendi.
Ayrıca 27 Python kaynağı `ast.parse`, 25 Bash kaynağı `bash -n`, yerel Markdown
bağlantıları ve `git diff --check` kontrol edildi.
GIO/Dolphin native başlatması ve Hyprland oturumu bu ortamda çalıştırılmadı.

## 2.2.4 süreç tanıma kontrolü

2026-10-17: `python3 checks/test_session_discovery.py` — **10 test geçti**;
Dolphin/kurulum kontrolü `python3 checks/test_file_manager.py` — **12 test geçti**.
Farklı kullanıcı ve taşınmış/symlink profil, tam kayıtlı eski komut, eksik/bozuk
manifest, ilgisiz profiller, IPC/list/log/kill çağrıları ve restore davranışı
kontrol edildi. `os.kill` kontrollü örnekte değiştirilerek yalnızca beklenen
PID'lerin seçildiği doğrulandı; gerçek süreç durdurulmadı.
PR #1 kullanıcı onayından sonra `b32cea4412cf0b3f3e5997b4e475f96ae7b739b7`
merge commit'iyle ana dala birleştirildi.

## 2.2.5 Spotify tanılama ve kurulum kontrolü

2026-10-17 kullanıcı tanılaması: normal/adblock masaüstü girdilerinde sarmalayıcı
ve LD_PRELOAD doğru görünüyor. `apply.log` sadece stdout kaydettiğinden başarılı
apply ilerlemesinin stderr satırları eksik olabilir; günlük tek başına kısmi
uygulama kanıtı değildir. Sistem paket sürümü eski özel kopyayı tanımlamaz.

Upstream `v2.45.3` sürüm notları aynı tarihte kontrol edildi: Linux Spotify
`1.2.14–1.2.96`. Belgelenmiş aralık dışı birleşim için kurucu preflight uyarısı,
birleştirilmiş günlük ve gerçek tema dosyası denetimleri eklendi.

`python3 checks/test_spotify_install.py` — **10 test geçti**. Sürüm uyarısı,
belgelenmiş aralık dışında check/apply devamı, eksik çıktıda fresh/update rollback, ilk yedek,
adblock ortam/eylemleri, restore, stdout/stderr ve salt okunur tanılama denetlendi.
`python3 checks/test_app_installers.py` — Dolphin ve Spotify uygulama/restore
kontrolleri geçti; dosya kendi konumundan checkout'u bulacak şekilde taşındı.
Gerçek Spotify arayüzü veya reklam engelleme sonucu bu ortamda doğrulanmadı.
Aynı tarihte mevcut 12 file-manager ve 10 session-discovery testi de tekrar geçti.
29 Python kaynağı parse edildi; 25 Bash dosyası, yerel Markdown bağlantıları ve
`git diff --check` kontrolü geçti.

17 Ekim kullanıcı düzeltmesi: Spotify çalışıyor. Sürüm notlarından kesin
uyumsuzluk çıkarımı yapılarak eklenen otomatik engel kaldırıldı; yerine uyarı
kondu. Bu onay mevcut kurulum içindir; yeni özel kopya veya bütün 1.3.4 paketleri
canlı doğrulanmış sayılmaz. Kullanıcıdan çalışan kurulumu yeniden uygulaması
veya geri alması istenmiyor.

## Sonraki iş

PT-001 ve mevcut Spotify çalışma durumu kullanıcı tarafından onaylandı.
Sürüm aralığına dayalı Spotify engeli yok. PT-003/004 için Dolphin okunabilirliği,
OSD/tray/şarj kabulü sırada; adblock'un ölçülmüş sonucu ayrı kabul maddesi olarak
korunuyor. PT-005 PR #2'de; gerçek oturum kabulü bekliyor.
Alt+Tab, hesaplama ve ayarlar henüz uygulanmadı; ROADMAP sırası korunuyor.
