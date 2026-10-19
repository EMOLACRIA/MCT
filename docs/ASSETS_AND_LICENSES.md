# Varlıklar ve lisans kaydı

Bu dosya köken kaydıdır; mevcut hakları değiştiren bir lisans değildir.

## 19 Ekim 22:58 — Kullanıcı onaylı 4× restorasyon

- Deltarune **0.3.1** wallpaper'ı, orijinal 1200×675 JPEG'den resmi
  [RealESRGAN_x4plus modeli](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth)
  ve [BasicSR RRDBNet mimarisi](https://github.com/XPixelGroup/BasicSR/blob/master/basicsr/archs/rrdbnet_arch.py)
  ile 4800×2700 RGB PNG'ye restore edildi. Kullanıcı bu yöntemi açıkça istedi.
- Genel/anime modelleri aynı küçük bölgede karşılaştırıldı; genel model fırça
  dokusunu daha iyi koruduğu için seçildi. Ek keskinleştirme veya renk düzenleme
  yapılmadı. `previews/deltarune/upscale-comparison.png` gerçek sonuç örnekleridir.
- Bu çıktı sanatçının native yüksek çözünürlüklü orijinali değildir; 0.3.0'daki
  piksel eşit format dönüşümü iddiası bu sürüme uygulanmaz. Orijinal JPEG aynen
  saklanır. Kaynak/model/mimari/çıktı SHA256 ve tile parametreleri
  [restoration.json](../themes/deltarune/restoration.json) içinde.
- Model ağırlıkları, PyTorch ortamı ve upstream mimari kodu depoya eklenmedi.
  İşlem üçüncü taraf çizimin haklarını değiştirmez; önceki hak kaydı korunur.

## 19 Ekim — Dört Deltarune referansı / yeni wallpaper

- Mevcut `deltarune` 0.3.0 wallpaper kaynağı kullanıcının gönderdiği
  `e3c07bb8f6f794ad31a025ae54440c50.jpg` (1200×675), depoda
  `themes/deltarune/wallpaper-source.jpeg`. Shell/wallpaper/lock fallback/SDDM
  PNG'leri aynı JPEG'in çözülmüş pikselleridir; AI repaint veya upscale yoktur.
- `design/deltarune/` diğer üç orijinali ve dört AI referansını korur. Referanslar
  bu konuşmada built-in imagegen ile üretilmiş görsel konseptlerdir; gerçek QML
  ekran görüntüsü değildir. Yeni paket preview'sı gerçek Qt render'ından gelir.
- Guardian kaynağı üstte `ART BY MANVJLL` kredi satırı taşır; orijinal dosya ve
  konsept bu satırı korur. Diğer dosyalarda sanatçı/kaynak bilgisi sağlanmadı;
  isim/hak sahipliği uydurulmaz. Sağlanan dosyalar açık lisanslı kabul edilmez.
- Kullanıcının sahne/lore açıklamaları tasarım bağlamı olarak kaydedildi;
  bağımsız resmî Chapter/rota doğrulaması yapıldığı iddia edilmez.
- Yeni dal köşeleri, klasör konturları ve CP437 ağaç sunumu proje içinde üretildi.
  Mevcut Departure Mono OFL bildirimi ve oyun görsellerinin hak kayıtları korunur.

Aşağıdaki 18 Ekim wallpaper kayıtları önceki paket sürümlerinin kökenidir.

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


### Deltarune 0.1.1 wallpaper değişimi

18 Ekim: kullanıcı ilk wallpaper kalitesini yetersiz bulup **images_upscaled.jpeg**
sağladı. Tam 2048×1151 kaynak `themes/deltarune/wallpaper-source.jpeg` içinde
birebir saklandı. SHA256: `bd8a46c7f008a18b45081c8f7506727ab4a803550399e029a3b56a789af0d3e3`.
Üç runtime PNG kopyası Qt ile format dönüştürüldü; decode edilmiş RGBA pikselleri
kaynağa eşit. Ek upscale, yeniden çizim veya yeniden JPEG sıkıştırması yapılmadı.
Preview PNG'leri yeni wallpaper ve şeritsiz düzenle yeniden Qt'den render edildi.

### Deltarune 0.2.0 adaptör varlıkları

SDDM wallpaper aynı kullanıcı PNG'sinin birebir kopyasıdır; Departure Mono ve
OFL metni greeter'in kendi sürecinde fontu kaydetmesi için değişmeden kopyalandı.
Yeni cyan kesik köşe SVG'leri ve CP437/UTF-8 fountain terminal çizimi bu işte
kod/metin olarak yazıldı. Deltarune Dolphin/Spotify palet/CSS ve klasör ikonları
mevcut proje kaynaklarından uyarlanır; harici tema kodu alınmadı. LoginSkin
sunum verisidir; Main.qml ortak giriş kodudur. previews/deltarune/login.png ve
previews/greeters/ görselleri gerçek Qt sahneleri, sahte SDDM modelleridir; PAM
girişi veya gerçek kullanıcı oturumu ekran görüntüsü diye sunulmaz.

18 Ekim Dolphin düzeltmesi: Deltarune klasör/yer SVG'lerinin 14'ü projedeki
mevcut çizimlerden camgöbeği basamaklı dış hatlara düzenlendi. Yeni harici ikon
paketi alınmadı; Breeze uygulama/eylem ikon mirası korundu.
