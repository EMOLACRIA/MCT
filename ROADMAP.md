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

1. **PT-001 — Dolphin başlatma tutarlılığı:** 2.2.3 kodu uygulandı, canlı doğrulama
   bekliyor. Super+E aynı desktop girdisini kullanır; launcher ve Dolphin
   dosya/klasör açma akışının gerçek oturumdaki görünümü kontrol edilecek.
2. **PT-002 — Spotify ve adblock:** boş ekranın güncel pakette giderildiğini
   gerçek uygulamada doğrula; desteklenmeyen özel başlatıcı varsa uyumlandır.
   Adblock'un korunması kurulum çıktısı kadar gerçek başlatma ile de kontrol edilir.
3. **PT-003 — Dolphin okunabilirliği:** normal/seçili yazılar beyaz; menü,
   pasif pencere, araç çubuğu ve 16/22 px ikonlar gerçek Dolphin'de okunaklı olmalı.
4. **PT-004 — OSD ve tray:** fonksiyon tuşları, slider, sessize alma, şarj
   simgesi ve Steam sağ tık menüsü canlı oturumda yeniden kontrol edilmeli.
5. **PT-005 — Taşınabilirlik:** `session.py` içindeki eski `/home/emo/...`
   süreç yolu kaldırılmalı veya önceki kurulumun gerçekten doğrulanmış yolundan
   türetilmeli; geniş bir süreç öldürme eşleşmesine dönüştürülmemeli.
6. Kurulum, tekrar güncelleme, başarısız güncelleme ve restore; ilk yedeğin
   korunması ve sonradan değiştirilmiş kullanıcı ayarlarına saygı.

Çıkış: bu sorunların her biri kanıtla kapatılmış; kullanıcı oturumunda normal
kullanımda kayıp panel/çoğalan süreç, okunmayan metin ve hatalı oturum işlemi yok.

## M2 — İlk temanın ortak günlük kullanım özelliklerini bitir

### PT-010 — Alt+Tab pencere seçici

- Bütün çalışma alanlarındaki pencereler; uygulama simgesi, başlık ve alan numarası.
- MRU gezinme; Alt+Tab ileri, Alt+Shift+Tab geri, Alt bırakınca seç, Esc ile iptal.
- Odak kaybı/açılan-kapanan pencere ve çoklu monitör durumu ele alınır.
- Seçim doğru alana geçer ve pencereyi odaklar. Yalnızca mevcut alanda aramaz.
- Canlı önizleme, desteklenen yakalama API'siyle uygulanabiliyorsa eklenir.
  Önizleme olmaması veya erişim sorunu pencere seçimini bozamaz.
- Tam çalışma alanı düzenleme/drag-and-drop overview ayrı zorunlu özellik değildir.

### PT-011 — Launcher hesaplama

- Super+R mevcut tüm uygulama aramasını korur; yazarken aritmetik sonucu gösterir.
- Parantez, ondalık sayılar, negatif değerler, çarpma/bölme ve yüzde davranışı açıkça
  tanımlanır; sıfıra bölme veya yarım ifade hata penceresi oluşturmaz.
- Sonuç kopyalanabilir. Kısayollar ve seçili sonuç davranışı açıkça gösterilir.
- Girdi Python/JS `eval`, shell komutu veya dosya erişimi olarak çalıştırılmaz.
- Birim dönüşümü için yetenek/dependency değerlendirmesi yapılır; ilk aritmetik
  kabulünden ayrı karar verilir. Dosya/emoji/web araması şu an taahhüt değildir.

### PT-012 — Ortak ayarlar ekranı

- Yazı ölçeği, hareketi azaltma/animasyon, saydamlık, bar ve panel tercihleri.
- Varsayılan uygulamalar: terminal ve dosya yöneticisi dahil tek ortak tanım.
- Tanılama ve ayarı sıfırlama; hatalı ayar için anlaşılır mesaj ve geri dönüş.
- Kullanıcı tercihleri temadan ayrı saklanır; yeniden başlatma/güncellemede korunur.
- Henüz tema değiştirme UI'si yok; ilk tema içindeki ayarlar tamamlanır.

Çıkış: bu üç özellik Plague Tale görünümünde klavye/fare ile kullanılabilir,
davranış sözleşmesine yazılmış ve canlı oturumda kabul edilmiş olmalı.

## M3 — Plague Tale'i ortak sözleşmenin referans uygulaması yap

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
