# Tema değiştirme araştırması

İnceleme: **2026-10-17**, Plague Tale 2.6.2 cila/kontrollü testlerinden sonra.
Durum: **araştırma ve öneri; uygulanmış tema motoru değildir**. Menünün yeri
kullanıcı kararını bekler. M4 kapısı açık; ikinci tema başlamadı.

## Projelerde görülen yöntemler

| Proje / incelenen birincil kaynak | Belgelenmiş yöntem | MCT için çıkarımımız |
|---|---|---|
| [HyDE](https://github.com/HyDE-Project/HyDE) ve [hyde-themes](https://github.com/HyDE-Project/hyde-themes) | Temalar ayrı depoda/dallarda; themepatcher / `hydectl theme import` ile alınır. Paketler tek başına çalışmaz, HyDE gerektirir. | Paket kurma/güncelleme ile etkinleştirmeyi ayrı tutabiliriz. Tema seçimi her seferinde dotfiles kurulumuna dönüşmemeli. |
| [ML4W Global Themes](https://ml4w.com/os/usage/themes) ve [Configuration Variations](https://ml4w.com/os/customization/variants) | Sidebar üzerinden Glass/Modern genel görünümü seçilir. Ayrı variation sistemi animasyon, düzen, monitor, keybind gibi ayarları dropdown ile seçer; kullanıcı kendi variation dosyasını oluşturur. | Genel görünüm ile kişisel ayarı ayırmak yararlı. Bizim sözleşmemizde monitor ve kısayol tema paketine dahil edilmeyecek. |
| [Caelestia CLI](https://github.com/caelestia-dots/cli#user-templates) | `scheme` ve `wallpaper` ayrı komutlar. Kullanıcı renk şablonları config altında; üretilen dosyalar state/theme altında. Uygulama başına enable seçenekleri ve postHook bulunur. | Dolphin/terminal/Spotify gibi adaptörler aynı semantik renklerden çıktı alabilir; her adaptörün reload/restart sınırı ayrıca tanımlanmalı. |
| [Noctalia Theme Switcher v0.2.0](https://noctalia.dev/plugins/community/theme-switcher) | Topluluk eklentisi: başlık, screenshot, palet kaynağı ve duvar kâğıtlarını kart/carousel halinde saklar. Uygulama sırası wallpaper → color-scheme-set → templates-apply; kayıt themes.json içinde. | Kart gerçek masaüstü önizlemesi gösterebilir. Aynı tema içindeki wallpaper seçimi ayrı tutulabilir. Bu, tek başına farklı panel geometrisi sağlayan bir skin sistemi kanıtı değil. |
| [Vitreus](https://github.com/natepayn3/Vitreus#-features) | Dört görünüm, ayrı typeface/malzeme: Glass, Retro, UwU, Cyber. Glass, Iris ile wallpaper'dan renklendirilir. Güncel runtime pleamar. | Birbirinden çok farklı temalar hedefimize en yakın görsel fikir: yalnız palet değil biçim, font ve yüzey de değişebilir. Runtime/kod taşıma kararı çıkarılamaz. |

[Noctalia v5 belgeleri](https://docs.noctalia.dev/noctalia/theming/) palet kaynağını
builtin/wallpaper/community/custom olarak ayırıyor; uygulama modu ile shell modu
da ayrı. Aynı belgelerde QuickShell sürümü **v4 legacy** olarak listeleniyor.
Bu nedenle bugünkü Noctalia eklenti API'si MCT QuickShell 0.3.1 için doğrudan
uygulanabilir bir API örneği sayılmadı. İnceleme proje kurulumunu gerektirmedi;
harici installer çalıştırılmadı, kod/görsel kopyalanmadı.

## MCT için seçenekler ve öneri

| Yaklaşım | Kazanç | Sınırı |
|---|---|---|
| Palet + wallpaper preset'i | Hızlı, az adapter işi | Çok farklı şekil/malzeme hedefine tek başına yetmez. |
| Bütün dotfiles klasörünü profil olarak değiştirmek | Sınırsız fark yaratır | Komut/kısayol/özellik ve kişisel ayarların ayrışmasını önlemek zorlaşır. |
| Ortak davranış + ayrı görsel paket + uygulama adaptörleri | Aynı işlevle çok farklı yüzeyler; mevcut sözleşmeyle uyumlu | Zorunlu yüzey doğrulaması, geçiş ve geri dönüş açıkça tasarlanmalı. |

**Önerimiz üçüncü yaklaşım.** Bu, kullanıcı tarafından onaylanmış yeni bir dosya
formatı/mimari kararı değildir. Mevcut Theme/SurfaceLayout ve ortak state'ler
başlangıç sağlar; şu an tam tema motoru yoktur.

M4 sonrasında tasarımda şu sınırlar değerlendirilmeli:

1. Tema metadata'sı kimlik/sürüm/uyumluluk, gerçek önizleme ve zorunlu yüzeyleri
   açıklamalı. Yarım paket etkinleştirilmemeli; kullanıcıya eksik bölüm söylenmeli.
2. Kısayol, launcher hesaplama, MRU, bildirim süresi, oynatıcı ve preferences tek
   ortak davranışta kalmalı. Skin yalnız bu arayüzü tüketmeli.
3. Önce geçici alanda dosya/QML/varlık doğrulaması, sonra snapshot ve uygulama;
   shell hazır değilse önceki duruma dönüş. Dış uygulamaların tamamı tek atomik
   işlem sayılmamalı: hangi bölüm uygulandı/hangisi restart bekliyor görünmeli.
4. SDDM sistem yetkisi ve sonraki giriş yaşam döngüsüyle ayrı kalmalı. Spotify
   yeniden apply/restart gereksinimi, Dolphin Qt başlangıç ortamı ve terminal
   paleti açık adaptör durumları olmalı. Tema değiştirmek logout zorlamamalı.
5. Küratörlü paletler ilk seçenek olabilir. Wallpaper'dan otomatik renk üretimi
   ayrıca değerlendirilebilir; Plague Tale'in bilinçli pirinç/taş paletini her
   wallpaper değişiminde yeniden üretmek şu an bir ihtiyaç değil.

Kart grid'i, carousel veya liste seçimi ile menünün **nereden açılacağı** ayrı
kararlardır. Araştırma bunlardan birini kullanıcı adına seçmez. Sonraki adım
Plague Tale'in [kalan native kabulünü](VALIDATION.md#hedef-oturumda-kalan-kabul)
tamamlamak; ardından tek mevcut paketle güvenli geçiş modelini tasarlamaktır.

## Kanıt sınırı

Yukarıdaki proje satırları erişilen resmî README/belgelerdeki davranışları özetler;
projeler burada kurulup çalıştırılmadı. Üçüncü sütun ve öneri bizim çıkarımımızdır.
Erişilemeyen eski HyDE wiki/raw-script yollarından uygulama detayı çıkarılmadı;
kaynak kod düzeyinde transaction/rollback garantileri bu araştırmada doğrulanmadı.
Bağlantılar hareketli main/master ve canlı belgelerdir; entegrasyon tasarımında
seçilen sürüm/commit yeniden sabitlenmeli. Bu araştırma lisans/uyumluluk onayı veya
harici runtime'a göç talebi değildir.
