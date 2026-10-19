# Güncel kalanlar — 19 Ekim 2026 13:22 Europe/Riga

Kullanıcı tema çizgisini “çok güzel olmuş güzel de çalışıyor” diyerek onayladı.
Son paylaşılan kaynak a80d08e0fa80f3069f4e4c37fb49570b77ea568f; cihaz SHA'sı ayrıca
sorgulanmadı. Günlük kullanım için bildirilmiş açık hata kalmadı. Bu kayıt
kullanıcı onayıdır; bütün hata/donanım senaryolarına ait ölçüm değildir.

## Tamamlanan ve onaylanan

- Plague Tale günlük kullanım kapanışı (17 Ekim).
- Mevcut Deltarune görünüm/kullanımı ve son Dolphin düzeltmesi (19 Ekim 00:24).
- Yatay tema çizgisi, hover fotoğrafı ve yeni seçicinin normal çalışması
  (19 Ekim 13:22). Aynı kullanıcı kabulü tekrar istenmez.
- Ortak launcher/hesaplama, Alt+Tab, ayarlar, OSD/tray ve tek davranış kaynağı
  önceki kayıtlardaki kapsamıyla korunur.

## Henüz tamamlanmamış alanlar

1. **Harici uyarlamalar tek tema seçimine bağlı değil.** Shell/wallpaper/Hyprlock/
   Kitty core ile geçer; Dolphin/Spotify/SDDM/CP437 süsü ayrı kuruculardır. Bunların
   tek akışa bağlanması sıradaki geliştirme önerisidir; kullanıcı bu status
   sorusunda uygulanmasını henüz istemedi. Uygulama açıkken kapatma/restart,
   SDDM yetkisi ve gerçek kısmi sonuçların sunumu kararlaştırılmalıdır.
2. **Yayın/depo toparlama.** PR #13 19 Ekim sorgusunda açık; bu görev merge yapmadı.
   Uygun dal sırasıyla ana dala alma, sürüm/release paketi, güncel ekran görüntüleri
   ve sade kurulum belgeleri genel dağıtım hazırlığında kalır.
3. **Yayın kaydı ve taşınabilirlik.** Proje lisansı/varlık kökenlerinin yayın
   kapsamı henüz tamamlanmadı. QA-001: eski fixture bağımlılıklarının bir kısmı
   kalır; mevcut CI'nın 197 kontrolü bütün eski checks dosyalarının taşınabilir
   olduğu anlamına gelmez. Başka kullanıcı temiz kurulum/restore ve harici ekran
   gibi geniş matris ayrı yayın borcudur; aynı kullanıcı normal onayı tekrar istenmez.

## İsteğe bağlı / henüz taahhüt değil

- Launcher'da birim dönüşümü; aritmetik hesaplama mevcut ve kabul edilmiş.
- Daha farklı temalar; üçüncü oyun seçilmedi.

## Ertelenmiş veya kapsam dışı

- Oyun kütüphanesi ertelendi.
- Pano/ekran yakalama paneli, hava durumu/takvim/AI paneli onaylanmadı.

Bu liste yeni geliştirme başlatmaz, eski test kutularını kanıtsız topluca kapatmaz
ve lisans seçmez. Öncelik önerisi: önce mevcut tema geçişi ile harici uyarlamaların
birleştirilmesini konuşmak, sonra yayın hazırlığı. Kullanıcı başka sıra seçebilir.
