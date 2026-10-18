# Varlıklar ve lisans kaydı

Bu dosya köken kaydıdır; mevcut hakları değiştiren bir lisans değildir.

- Ana duvar kâğıdı kullanıcı tarafından sağlanan oyun ekran görüntüsünden gelir.
  `payload/style/wallpaper.png` ve shell içindeki kopyası aynı işlevsel varlıktır;
  2.6.2 denetiminde SDDM dosyasının aynı PNG'nin kesilmiş bir öneki olduğu bulundu;
  sağlam ana kopyayla tamamlandı. SDDM görünümü QML katmanlarıyla uyarlanır.
  Oyunun üçüncü taraf hakları devredilmiş
  veya kamu malı olarak kabul edilmiş değildir.
- `previews/` ortak QML arayüzünden hazırlama sırasında alınmış tanıtım görselleridir;
  son kullanıcının özel bildirim/hesap ekran görüntülerini içermez.
  17 Ekim 2.6.2: bozuk `power.png` güncel DemoContext'ten, `sddm.png` sahte SDDM
  modellerinden yeniden render edildi; gerçek giriş/kimlik doğrulama kanıtı değildir.
- SVG köşe süsleri, Dolphin klasör ikonları, Spotify CSS ve shell kaynakları önceki
  proje çalışmasının parçalarıdır. Genel bir üçüncü taraf lisansı uydurulmaz.
- CP437 terminal madalyonu kullanıcı tarafından `terminal-medallion/` altında
  MCT başlangıcına eklendi. CP437 byte dosyaları ve UTF-8 Fastfetch sürümleri
  mevcut; ilk temayla entegrasyon/canlı kabul ASSET-001 ile takip ediliyor.
- Bu görevde Vitreus/Caelestia kodu veya görselleri kopyalanmadı. Referans linkleri
  `INSPIRATION.md` içindedir. Gelecekte alınan dosya için kaynak commit'i, lisans,
  değiştirme ve bildirim gereksinimi bu kayda eklenir.
- Proje için yeni bir MIT/GPL lisansı bu görevde kullanıcı adına seçilmedi.
  Açık kaynak lisansı seçimi ve varlıkların kapsamı genel yayından önce netleştirilir.

2.7.0 tema paketindeki 38 dosya mevcut payload'ın birebir kopyalarıdır;
`themes/plague-tale/preview.png`, mevcut `previews/desktop.png` dosyasının birebir
kopyasıdır. Yeni dış görsel/font/kod alınmadı. Manifest git blob kimlikleriyle
kaynak eşitliğini doğrular; bu kayıt yeni lisans veya üçüncü taraf hak devri değildir.


## Deltarune — 18 Ekim 2026

- `themes/deltarune/files/style/wallpaper.png` ve shell kopyası kullanıcının
  sağladığı **Deltarune.webp** görselinin Qt ile kayıpsız PNG format dönüşümüdür;
  piksel eşitliği denetlendi. Çizim yeniden üretilmedi, resize/repaint yapılmadı.
  Cover fallback aynı görseldir. Toby Fox/oyunun üçüncü taraf hakları korunur;
  kullanıcı dosyasının sağlanması yeniden lisanslama değildir.
- Battle menu portreleri, 18 Ekim doğrudan değişmeden indirildi:
  [Kris](https://deltarune.wiki/w/File:Kris_face_battlemenu.png),
  [Susie](https://deltarune.wiki/w/File:Susie_face_battlemenu.png),
  [Ralsei](https://deltarune.wiki/w/File:Ralsei_face_battlemenu.png).
  Dosyalar `https://deltarune.wiki/images/NAME_face_battlemenu.png` adreslerinden.
  Bunlar oyun sprite'larıdır; wiki metin lisansı görseller için varsayılmadı.
  Oyun görsellerinin hak sahibi Toby Fox ve ilgili katkıcılardır.
- Departure Mono 1.500, Helena Zhang; **SIL OFL 1.1**. Kaynak
  [rektdeckard/departure-mono](https://github.com/rektdeckard/departure-mono/tree/75152a3f1e6dacdd248a6c397c97dbf27e33eea0/public/assets),
  font blob `e0b2502131fcb7befea378d6648d380c2591b3a5`. Değiştirilmedi.
  `FONT-LICENSE.txt` ve kurulan `assets/departure-mono-license.txt` tam font lisansıdır.
- Yeni kesik köşe/ikon çizimleri ve lock medya SVG düğmeleri bu işte kodla çizildi;
  PNG düğmeler paket yanındaki SVG kaynaklarının Qt render'larıdır.
- `themes/deltarune/preview.png` ve `previews/deltarune/` gerçek Qt DemoContext
  render'larıdır; konsept üretim görseli ürün ekran görüntüsü diye kullanılmadı.
