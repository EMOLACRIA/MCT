# Güncel durum

Son inceleme: **2026-10-17**. Kaynak taban: **2.2.2**.
Aşama: **M0 — dokümantasyon hazır; GitHub push işlemini kullanıcı devraldı**. Plague Tale tamamlanmış değildir.
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
| PT-001 | Açık | 17 Ekim: launcher ile Super+E Dolphin farklı. Payload hâlâ `local fileManager = "dolphin"`; sohbette verilen elle env düzeltmesi kullanıcının cihazında uygulanmış varsayılmaz. |
| PT-002 | Canlı doğrulama bekliyor | 16 Ekim: Spotify boş ekran, adblock girişinde tema yok. 2.2.1 bootstrap/başlatıcı düzeltmeleri kaynakta; son kullanıcı sonucu henüz gelmedi. |
| PT-003 | Canlı doğrulama bekliyor | Dolphin yazıları/ikonları zor okunuyordu. 2.2.2 beyaz normal/seçili metin ayarı kaynakta; bütün başlatma yolları kontrol edilmedi. |
| PT-004 | Canlı doğrulama bekliyor | OSD 2.2.0 IPC `present` düzeltmesi; önceki raporda tuşlar çalışıyor fakat OSD yoktu. Son gerçek sonuç ayrıca kaydedilmeli. Steam menüsü/şarj durumu da kabul kontrolünde. |
| PT-005 | Açık | `payload/style/scripts/session.py` eski HyprCADE yolunu kullanıcıya özel sabit tutuyor. Genelleştirme henüz yapılmadı. |
| QA-001 | Açık | `checks/` dosyaları eski `build/desktop-style`, `tmp/` kaynakları ve Qt ortamı varsayıyor. Bağımsız checkout test komutu/CI henüz yok. |
| ASSET-001 | Açık | CP437 terminal madalyonu önceki ayrı eklentiydi; ana payload içinde fastfetch/CP437 teslimi bulunmadı. İlk tema kabulünden önce kaynağı ve kurulumu doğrulanmalı. |

## Önceki hazırlama kontrolleri

Önceki oturumlarda bildirilen sonuçlar: Qt 6.10.2 render/etkileşim, QML bytecode,
QuickShell 0.3.1 kaynak API karşılaştırması, yardımcı script ve dosya rollback
fixtureleri. Bunlar native Hyprland/Spotify/Dolphin/Steam/Hyprlock oturumu değildir.
2.2.1 testleri adblock Exec ortam/argüman koruması, JS modül yükleme sırası ve Qt
aktif/pasif metin paletini kontrollü örneklerle denetledi. 2.2.2 beyaz palet
rolleri okundu. Ayrıntılar eski kurulum belgesi ve `checks/README.md` içinde.

## Bu görevde yapılanlar

- [x] GitHub bağlantısı üzerinden Vitreus ve Caelestia README'leri incelendi.
- [x] AGENTS.md, README ve karar kaydı yaklaşımı resmî/proje kaynaklarından araştırıldı.
- [x] Kullanıcının kabul ettiği ve ertelediği kapsam kaydedildi.
- [x] Yol haritası, özellik sözleşmesi, yayın kontrolü ve güncel durum dosyaları yazıldı.
- [x] 2026-10-17: 24 Python kaynağı `ast.parse`, 21 Bash kaynağı `bash -n` ile kontrol edildi; Markdown yerel bağlantıları çözüldü. Runtime kaynakları önceki 2.2.2 ZIP ile byte düzeyinde aynı.
- [x] `EMOLACRIA/HyprCade` içinde `plague-tale-foundation` dalı açıldı.
- [ ] Yeni proje kaynakları GitHub'a commit/push edilmedi. Görsel nesnelerinin aktarımı takıldı; 2026-10-17 kullanıcının isteğiyle yükleme bırakıldı ve ZIP teslimine geçildi. Push işlemini kullanıcı yapacak.
- [x] Yeni masaüstü özelliği uygulanmadı; kaynak tabanı 2.2.2 korundu.

## Sonraki önerilen iş

M1 / PT-001: varsayılan dosya yöneticisi ve başlatma ayarını ortak bir eylemden
çalıştırmak; installer/update/restore davranışı ve launcher/Super+E görünümüyle doğrulamak.
Yeni özellik geliştirmeye bundan sonra, ROADMAP sırasıyla geçilir.
