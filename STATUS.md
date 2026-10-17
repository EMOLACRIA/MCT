# Güncel durum

Son inceleme: **2026-10-17**. Kaynak taban: **2.2.3 geliştirme sürümü**.
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
| PT-001 | Uygulandı / canlı doğrulama bekliyor | 2.2.3: Super+E, XDG sırasıyla aynı Dolphin desktop girdisini GIO üzerinden açıyor. Stock ve yayımlanmış elle düzeltme update sırasında taşınıyor; özel tercihler korunuyor. 12 regresyon kontrolü geçti. Gerçek Dolphin görünümü kullanıcı oturumunda bekliyor. |
| PT-002 | Canlı doğrulama bekliyor | 16 Ekim: Spotify boş ekran, adblock girişinde tema yok. 2.2.1 bootstrap/başlatıcı düzeltmeleri kaynakta; son kullanıcı sonucu henüz gelmedi. |
| PT-003 | Canlı doğrulama bekliyor | Dolphin yazıları/ikonları zor okunuyordu. 2.2.2 beyaz normal/seçili metin ayarı kaynakta; bütün başlatma yolları kontrol edilmedi. |
| PT-004 | Canlı doğrulama bekliyor | OSD 2.2.0 IPC `present` düzeltmesi; önceki raporda tuşlar çalışıyor fakat OSD yoktu. Son gerçek sonuç ayrıca kaydedilmeli. Steam menüsü/şarj durumu da kabul kontrolünde. |
| PT-005 | Açık | `payload/style/scripts/session.py` eski HyprCADE yolunu kullanıcıya özel sabit tutuyor. Genelleştirme henüz yapılmadı. |
| QA-001 | Kısmen açık | `python3 checks/test_file_manager.py` bağımsız checkout içinde çalışır. Diğer eski kontroller çalışma alanı/Qt fixturelerine bağlı; genel CI henüz yok. |
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

## Sonraki iş

PT-001'in canlı kontrolü: güncel dalda `bash update.sh --check && bash update.sh`;
bütün Dolphin pencerelerini kapatıp launcher ve Super+E ile aç. Metin/palet/ikon
aynılığı ile `hyprctl configerrors` sonucunu kaydet. Sonra PT-002 Spotify tanılaması.
Alt+Tab, hesaplama ve ayarlar henüz uygulanmadı; ROADMAP sırası korunuyor.
