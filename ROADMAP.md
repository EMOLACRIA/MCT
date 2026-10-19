# 19 Ekim 21:34 — Yeni öncelik: dört Deltarune görsel dünyası

Kullanıcı dört konsepti de ayrı tema olarak istedi. Önce mevcut `deltarune`
son ağaç/Kris referansına taşınır (0.3.0); kalan üç paket sonra geliştirilir.

1. **Şimdi:** indigo/lavanta/fuşya ağaç görünümü; shell, lock, Kitty ve bağımsız
   uygulama adaptörleri, gerçek Qt önizlemeleri ve ortak davranış regresyonu.
   22:57 kullanıcı 0.3.0 check/apply ve görünümü onayladı. Tek yeni eksik wallpaper
   kalitesi; 22:58 onayıyla 0.3.1 Real-ESRGAN 4× restorasyonu yapılır. Yeni görüntü
   için cihaz kalite kabulü beklenir.
2. **Sonra:** Guardian, neşeli gün batımı ve Snowgrave sonbahar için üç ayrı
   tam görsel paket. Kesin paket adları ve aralarındaki uygulama sırası açık.
   Boş/yarım tema seçiciye eklenmez.
3. Harici adaptörleri otomatik geçişe bağlama, yayın/lisans ve geniş donanım
   matrisi önceki durumlarıyla kalır. Bu işte tamamlanmış sayılmaz.

[Karar](docs/decisions/0016-deltarune-four-worlds.md) ·
[Tasarım kaynakları](design/deltarune/README.md) · [Deneme](docs/DELTARUNE.md).
Aşağıdaki önceki aşamalar tarihsel temeldir; yeni kullanıcı önceliği üstündür.

# Yol haritası

Karar tarihi: **18 Ekim 2026**. Ürün kapsamı: [PROJECT_BRIEF.txt](PROJECT_BRIEF.txt).
Durumlar: **planlandı**, **uygulandı / doğrulama bekliyor**, **doğrulandı**, **ertelendi**.
Tarihler taahhüt edilmedi; bir aşama kendi çıkış koşulları karşılanınca kapanır.

## Güncel özet — 19 Ekim 13:22

Kullanıcı yeni tema çizgisinin görünümünü ve normal çalışmasını onayladı.
Plague Tale, mevcut Deltarune ve yeni seçici için aynı kabul tekrar istenmez.
Kalan işler, sınırlar ve henüz seçilmemiş fikirler
[CURRENT_BACKLOG](docs/CURRENT_BACKLOG.md) içinde ayrıdır. Aşağıdaki aşama tarihçesi
bu üst kayıtla birlikte okunur; eski bekleme cümleleri güncel açık hata sayılmaz.

## M0 — Projeyi kayıt altına al ve GitHub'a taşı — tamamlandı

Bu görevde yapılan iş. Ürün ve ajan talimatları; güncel durum; referanslar;
ortak özellik sözleşmesi; mimari ve yayın kontrol listesi oluşturulur.
Mevcut 2.2.2 kaynakları sürüm kontrolüne alınır. Yeni arayüz özelliği uygulanmaz.

Çıkış: dosyalar gözden geçirilmiş, kaynaklar erişilebilir bir Git dalına yüklenmiş,
commit kimliği ve kontrol sonuçları `STATUS.md` içinde izlenebilir olmalı.

## M1 — Mevcut Plague Tale kurulumunu sağlamlaştır

Öncelik sırası:

1. **PT-001 — Dolphin başlatma tutarlılığı:** **doğrulandı**. Kullanıcı 17 Ekim
   2026 tarihinde PR #1 dalını uygulayıp launcher ve Super+E açılışını onayladı.
   Sonraki değişikliklerde bu davranış korunacak.
2. **PT-002 — Spotify ve adblock:** boş ekranın güncel pakette giderildiğini
   gerçek uygulamada doğrula; desteklenmeyen özel başlatıcı varsa uyumlandır.
   Adblock'un korunması kurulum çıktısı kadar gerçek başlatma ile de kontrol edilir.
   17 Ekim: kullanıcı Spotify'ın çalıştığını onayladı. Sistem paketi 1.3.4 /
   CLI 2.45.3, belgelenmiş Linux aralığı dışında olsa da otomatik engel değildir.
   2.2.5 sürüm uyarısı ve çıktı denetimleri var; reklam engelleme sonucu ayrı
   olarak ölçülmedi. Genel 1.3.4 uyumu iddia edilmez.
3. **PT-003 — Dolphin okunabilirliği:** normal/seçili yazılar beyaz; menü,
   pasif pencere, araç çubuğu ve 16/22 px ikonlar gerçek Dolphin'de okunaklı olmalı.
   17 Ekim PR #4 sonrası istenen kullanım kontrolü kullanıcı tarafından onaylandı.
4. **PT-004 — OSD ve tray:** fonksiyon tuşları, slider, sessize alma, şarj
   simgesi ve Steam sağ tık menüsü canlı oturumda yeniden kontrol edilmeli.
   2.2.6: bildirimlerde milisaniye süresi, property değişimlerinin aynı karta
   yansıması ve zamanlayıcı temizliği düzeltildi. Qt OSD/ikon ve kontrollü tray
   eylem testleri geçti. PR #4 sonrası istenen OSD/Steam kontrolleri kullanıcı
   tarafından onaylandı; varsayılan/toast 4500 ms. Fiziksel pil geçişi M4'te kalır.
5. **PT-005 — Taşınabilirlik:** 2.2.4 kodu uygulandı. Mevcut HOME/XDG profili
   veya ilk yedekte kayıtlı tam seçici kullanılır; ilgisiz QuickShell profilleri
   ve IPC istemcileri korunur. 10 kontrollü test geçti; normal güncelleme onaylandı.
   Farklı kullanıcıyla fresh install/restore geniş kabulü M4 listesinde kalır.
6. Kurulum, tekrar güncelleme, başarısız güncelleme ve restore; ilk yedeğin
   korunması ve sonradan değiştirilmiş kullanıcı ayarlarına saygı.

Çıkış: bu sorunların her biri kanıtla kapatılmış; kullanıcı oturumunda normal
kullanımda kayıp panel/çoğalan süreç, okunmayan metin ve hatalı oturum işlemi yok.

## M2 — İlk temanın ortak günlük kullanım özelliklerini bitir

### PT-010 — Alt+Tab pencere seçici

**2.3.0: normal kullanım 17 Ekim kullanıcı onayıyla doğrulandı.** Çoklu ekran
çıkarma/yakalama ayrıntıları ayrıca raporlanmadı; M4 listesinde korunur. 11 gerçek Qt testi,
6 kısayol geçiş kontrolü ve kaynak API karşılaştırması geçti. Önizleme tek kare;
canlı video zorunlu kabul ölçütü değildir. [Karar](docs/decisions/0006-window-switcher.md).

- Bütün çalışma alanlarındaki pencereler; uygulama simgesi, başlık ve alan numarası.
- MRU gezinme; Alt+Tab ileri, Alt+Shift+Tab geri, Alt bırakınca seç, Esc ile iptal.
- Odak kaybı/açılan-kapanan pencere ve çoklu monitör durumu ele alınır.
- Seçim doğru alana geçer ve pencereyi odaklar. Yalnızca mevcut alanda aramaz.
- Canlı önizleme, desteklenen yakalama API'siyle uygulanabiliyorsa eklenir.
  Önizleme olmaması veya erişim sorunu pencere seçimini bozamaz.
- Tam çalışma alanı düzenleme/drag-and-drop overview ayrı zorunlu özellik değildir.

### PT-011 — Launcher hesaplama

**2.4.0: 17 Ekim normal kullanım kullanıcı tarafından onaylandı.** Ortak parser, karma sonuç
listesi ve pano adaptörü; Node, 7 gerçek Qt etkileşimi ve network JS import
kontrolleri geçti. Yüzde `/100`, kopyalanan metin 12 anlamlı basamaktır.
[Karar](docs/decisions/0007-launcher-calculator.md).

- Super+R mevcut tüm uygulama aramasını korur; yazarken aritmetik sonucu gösterir.
- Parantez, ondalık sayılar, negatif değerler, çarpma/bölme ve yüzde davranışı açıkça
  tanımlanır; sıfıra bölme veya yarım ifade hata penceresi oluşturmaz.
- Sonuç kopyalanabilir. Kısayollar ve seçili sonuç davranışı açıkça gösterilir.
- Girdi Python/JS `eval`, shell komutu veya dosya erişimi olarak çalıştırılmaz.
- Birim dönüşümü için yetenek/dependency değerlendirmesi yapılır; ilk aritmetik
  kabulünden ayrı karar verilir. Dosya/emoji/web araması şu an taahhüt değildir.

### PT-012 — Ortak ayarlar ekranı

**2.5.0: uygulandı / kalıcılık kabulü bekliyor.** 17 Ekim terminal ve Dolphin
açılışı kullanıcı tarafından onaylandı; restart/tercih korunması ayrıca raporlanmadı. Görünüm/bar/panel ve shell
varsayılan uygulamaları; ayrı sürümlü JSON, doğrulama, atomik kayıt, yedekli reset
ve tanılama. 15 Python + 10 Qt testi geçti. [Rehber](docs/SETTINGS.md) ·
[Karar](docs/decisions/0008-user-preferences.md). Henüz tema değiştirici yoktur.

- Yazı ölçeği, hareketi azaltma/animasyon, saydamlık, bar ve panel tercihleri.
- Varsayılan uygulamalar: terminal ve dosya yöneticisi dahil tek ortak tanım.
- Tanılama ve ayarı sıfırlama; hatalı ayar için anlaşılır mesaj ve geri dönüş.
- Kullanıcı tercihleri temadan ayrı saklanır; yeniden başlatma/güncellemede korunur.
- Henüz tema değiştirme UI'si yok; ilk tema içindeki ayarlar tamamlanır.

Çıkış: bu üç özellik Plague Tale görünümünde klavye/fare ile kullanılabilir,
davranış sözleşmesine yazılmış ve canlı oturumda kabul edilmiş olmalı.

## M3 — Plague Tale'i ortak sözleşmenin referans uygulaması yap

**Başladı — PT-013 / 2.5.1:** ilk dar ekran/uzun içerik denetiminde tray-saat
çakışması, medya ve güç menüsü taşması, uzun bildirim eylemleri düzeltildi.
7 Qt testi ve görsel örnekler kontrol edildi. 17 Ekim kullanıcı normal kullanımda
sorun bildirmedi; ayrıntılı tray/çoklu ekran testleri ayrıca raporlanmadı.
[Karar](docs/decisions/0009-responsive-surfaces.md).

**PT-014 / 2.6.0 uygulandı:** shell paleti/font/varlık/hareket ve dış yüzey ölçüleri
ortaklaştırıldı; başlık, ipucu, toast/geçmiş eylemleri paylaşılıyor. 9 Qt testi,
35 QML derlemesi ve önceki etkileşim kontrolleri geçti. [Yüzey haritası](docs/THEME_SURFACES.md) ·
[Karar](docs/decisions/0010-shared-shell-presentation.md).
Hedef oturum kabulü, lock/SDDM/uygulama bütünlüğü ve sözleşmenin tamamı hâlâ açık.
2.6.1: kullanıcı bar ipucunun tıklamayı engellediğini bildirdi. Gecikmeli,
input-transparent ayrı bar popup'ı uygulandı. 17 Ekim kullanıcı “Tamamdır gayer güzel”
diyerek düzeltmenin normal kullanımını onayladı; geniş M3/M4 ve PT-012 kabulü açık.

- Görsel kimlik: font, ikon, çerçeve, panel, OSD, bildirim, medya, settings,
  Alt+Tab, launcher, Hyprlock, SDDM ve uygulama eklentilerinin bütünlüğü.
- Ortak eylemler/veri ve tema görselleri birbirinden ayrılır. Yeni işlev tek
  ortak yerde uygulanır; her tema içine kopyalanmaz.
- Tema paletinin dışındaki sabit renkler, konum/boyutlar ve malzeme ayarları
  denetlenir. Yapı yalnızca renk dosyasına indirgenmez.
- Eklentiler/harici uygulamalar için yeniden başlatma gereksinimi dürüstçe
  belirtilir; her uygulamanın canlı renk değiştireceği varsayılmaz.
- `docs/FEATURE_CONTRACT.md` matrisinde temel özellik için eksik/yüzeysel tema
  uygulaması kalmaz. Eksik cihaz ile eksik özellik ayrılır.

Çıkış: ilk tema tam sözleşmeyi karşılar; yeni bir temanın tüm zorunlu yüzeyleri
nereden alacağı tanımlıdır. İkinci tema hâlâ başlatılmaz.

## M4 — Plague Tale tamamlanma ve yayın kapısı

**17 Ekim güncellemesi:** kullanıcı önceki son canlı kontrol maddesini tamamladığını
ve gün boyu full kullandığını onayladı. Plague Tale ürün/kullanım kapanışı kabul
edildi ve M5 çekirdeğine geçiş açıkça yetkilendirildi. Genel dağıtım/lisans ve
ayrı raporlanmamış donanım alt testleri geniş yayın kaydında korunur; kullanıcının
aynı son kabulü tekrar vermesi beklenmez. Aşağıdaki eski kapı metni bu güncel
kullanıcı beyanıyla birlikte okunur.

[RELEASE_CHECKLIST](docs/RELEASE_CHECKLIST.md) uygulanır. Açık zorunlu özellik veya
bilinen kullanım engeli kalmaz. Gerçek oturumda restart/login, çoklu ekran/ölçek,
boş durumlar, uygulama başlatma ve güvenilir restore kontrol edilir.
Güncel görüntüler, kullanılan sürümler, sınırlamalar ve kurulum adımları kaydedilir.
Kullanıcı ilk temanın bitmiş görünümünü ve kullanımını onaylar.

**M4 kapanmadan M5 ve M6 başlamaz.** Paket numarası tek başına bu kapının
kapanmış olduğu anlamına gelmez.

## M5 — Tema değiştirici

**19 Ekim 01:07 revizyonu uygulandı; 13:22 görünüm/normal kullanım kullanıcı onaylı.** Kullanıcı
önceki arayüzü yeterince stilize/rahat bulmadı. Ortada yatay çizgi, hover ile
fotoğrafı genişleyen temalar ve tek seçimle arka plan kontrollü geçiş geldi.
Ayrı app penceresi kalktı, sıcak Wayland katmanı IPC ile toggle olur. Super+G
canlı boşluk kontrolüyle ayrı bind kurucusunda eklenir; doluysa korunur.
Menü yeri artık açık karar değildir; eski kayıtlar aşağıda tarihseldir.

**19 Ekim: fotoğraflı ilk arayüz uygulandı.** `bash theme.sh menu` ayrı repo
penceresidir; kartlar, büyük resim, aktif tema, kontrol→uygula, iki aşamalı geri
dönüş vardır. Yeni bar/ayar yeri veya global kısayol atanmadı. Mevcut core işlem
korumaları kullanılır. Harici uygulama/SDDM adaptörleri ayrı kalır ve arayüzde
belirtilir. Yeni arayüzün native kullanıcı denemesi beklenir.
[Rehber](docs/THEME_PICKER.md). Aşağıdaki önceki M5 kayıtları tarihsel temeldir.

**2.7.0: CLI paket çekirdeği uygulandı.** Manifest + gerçek fotoğraf + 38 görsel
kaynak; doğrulama/uygulama/rollback/recover, tercih koruma, güncelleme çakışma
koruması. 28 çekirdek ve 27 mevcut izole test geçti. [Rehber](docs/THEME_PACKAGES.md).
Görsel menü ve kartlar uygulanmadı; menünün konumu açık. SDDM/Spotify/Dolphin ayrı
kuruculardır; tek tıkla bütün uygulamaların canlı yeniden stillenmesi yoktur.

**Menünün konumu açık:** kullanıcı düşünüp seçecek. Preferences yerleşimi
kararlaştırılmadı. 17 Ekim talebiyle M4 cila kontrollerinden sonra
[tema değiştirme yöntemleri araştırıldı](docs/THEME_SWITCHING_RESEARCH.md);
bu, M5 arayüzünün başlaması değildir.

17 Ekim kullanıcı onayı: ortak davranış + ayrı görsel paket + uygulama adaptörleri;
her tema için gerçek ekran görüntülü önizleme kartı. Kartların dizilimi ve menünün
konumu açık kalır. Bu onay M4 native testlerinin yapıldığı anlamına gelmez.

M4 sonrasında: fotoğraflı önizleme kartları, tema metadata/manifest'i, uyumluluk ve zorunlu
yüzey kontrolü, uygulama/geri alma, tercihleri koruma, gerekli restart bildirimleri.
Önce tek mevcut Plague Tale paketiyle akış tamamlanır. Yarım tema etkinleştirilmez.

## M6 — Görsel açıdan farklı sonraki temalar

Her tema aynı özellik sözleşmesinden geçer. Farklı şekiller, malzeme, font,
animasyon ve düzen olabilir; alışılmış kısayollar/eylemler değişmez.
Tema listesi kullanıcıyla ayrıca seçilir. Vitreus ve Caelestia görünüm referansıdır;
bir sonraki temanın bunlardan biri olacağı kararlaştırılmadı.

## Ertelenen / kapsam dışı

- Pano geçmişi ve yeni ekran yakalama paneli: şu an kapsam dışı.
- Oyun kütüphanesi: ertelendi, yol haritası için engel değil.
- AI sohbeti, takvim/hava durumu, masaüstü notları: talep edilmedi.

## M6 — Deltarune mevcut görünüm/kullanım onaylı

19 Ekim 00:24 Europe/Riga: kullanıcı Dolphin'in de değiştiğini onaylayıp devam
istedi. Önceki diğer uyarlamalar/komutlar çalışıyor beyanıyla son bilinen sorun
kapandı; yeni tema seçicisine geçildi. Tek tek PAM/sensör alt testleri icat edilmez.
Aşağıdaki 18 Ekim denetim ve revizyon beklemeleri tarihsel kayıttır.

18 Ekim tamamlama denetiminde açık eksikler bulundu:
[bulgular ve kapanış koşulları](docs/DELTARUNE_AUDIT.md). Tema seçiciye geçiş
koşulu henüz karşılanmadı. 2.9.0'da Loader yaşam döngüsü/ortak davranış ayrımı ve harici görsel adaptörler
uygulandı; offscreen/mock kontrolleri geçti. Yeni native görünüm/işlev kabulü
beklenir. [Deneme adımları](docs/UPGRADE_2_9.md).

18 Ekim kullanıcı ikinci temanın geliştirilmesini başlattı. Seçilen wallpaper,
siyah/camgöbeği piksel dil ve karakter portreleri ilk pakette var. 18 Ekim ilk
revizyonda kullanıcı parti şeridini kaldırdı; kontrol menüsü sağa taşındı ve
yeni images_upscaled.jpeg wallpaper kullanıldı. Ortak launcher/hesaplama/Alt+Tab/tray/OSD/ayar sözleşmesi korunur.

1. Kullanıcı gerçek oturumda paketi deneyip görsel ve kullanım revizyonlarını verir.
2. Bu sonuçla panel ölçüleri ve fontun 1.6 ölçekteki görünümü cilalanır.
3. Lock parola/saat sunumu, SDDM, Dolphin/Spotify ve terminal madalyonu için ayrı
   görsel adaptasyon tamamlanır. Mevcut uygulama kurulumu sessizce değiştirilmez.
4. Tema seçicinin yerini kullanıcı belirler; gerçek Qt önizlemesi metadata'da hazır.

Plague Tale'in son kullanım onayı tekrar istenmez. Deltarune ilk denemesi henüz
ikinci temanın bütün adaptörleriyle tamamlandığı anlamına gelmez.

18 Ekim 2.9 denemesi: kullanıcı komutları ve Dolphin dışındaki uyarlamaları
çalışır bildirdi. Dolphin fotoğrafı eski klasör renklerini gösterdi; kaynakta
aynı SVG'lerin taşındığı doğrulandı ve cyan basamaklı ikonlar düzeltildi.
Yeni Dolphin görünümünün cihazdaki onayı açık; tema seçicisi henüz başlamadı.
