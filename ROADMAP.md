# Yol haritası

Karar tarihi: **17 Ekim 2026**. Ürün kapsamı: [PROJECT_BRIEF.txt](PROJECT_BRIEF.txt).
Durumlar: **planlandı**, **uygulandı / doğrulama bekliyor**, **doğrulandı**, **ertelendi**.
Tarihler taahhüt edilmedi; bir aşama kendi çıkış koşulları karşılanınca kapanır.

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
input-transparent ayrı bar popup'ı uygulandı; aynı inceleme dalında kabul bekliyor.

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

[RELEASE_CHECKLIST](docs/RELEASE_CHECKLIST.md) uygulanır. Açık zorunlu özellik veya
bilinen kullanım engeli kalmaz. Gerçek oturumda restart/login, çoklu ekran/ölçek,
boş durumlar, uygulama başlatma ve güvenilir restore kontrol edilir.
Güncel görüntüler, kullanılan sürümler, sınırlamalar ve kurulum adımları kaydedilir.
Kullanıcı ilk temanın bitmiş görünümünü ve kullanımını onaylar.

**M4 kapanmadan M5 ve M6 başlamaz.** Paket numarası 2.2.2 olması bu kapının
kapanmış olduğu anlamına gelmez.

## M5 — Tema değiştirici

M4 sonrasında: önizleme kartları, tema metadata/manifest'i, uyumluluk ve zorunlu
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
