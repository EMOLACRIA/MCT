20 Ekim 2026 hazırlama doğrulaması — Adventure 0.1.0:
163 unittest geçti: core 34, Adventure 42, Snowgrave regresyon 42, picker UI 6,
picker bridge 4, adaptörler 5, dört-skin greeter 20, dört-skin OSD 1,
lock layout 3, terminal 6. 168 QML bytecode derlemesi ve network imports geçti.
Komutlar: checks/test_theme_core.py, test_deltarune.py deltarune-adventure ve
 deltarune-snowgrave, test_theme_picker_ui.py, test_theme_picker.py,
 test_theme_adapters.py, test_greeter_themes.py, test_osd_themes.py,
 test_lock_layout.py, test_terminal_medallion.py, test_shell_syntax.py,
 test_shell_imports.py (hepsi python3 checks/ altında).
Qt: MCT_QT_TEST_PATH=build/qs-qt-check (workspace mutlak yolu kullanıldı).
Manifest Engine.load, dört PNG tam decode/3200×1800/SHA256 eşitliği, orijinal
JPEG birebir korunması, Python/Bash syntax ve git diff --check geçti.
Launcher/media/settings offscreen render'ları görsel incelendi. Native oturum,
PAM veya gerçek uygulamaları bu hazırlama ortamında çalıştırmadık.

20 Ekim 2026 — Güncel öncelik: kullanıcı Snowgrave'i beğenip normal görünümü
onayladı; Chapter 5 trailer/gün batımı referansı ayrı `deltarune-adventure` 0.1.0
paketi olarak uygulandı. Mürdüm/mercan/altın ve basamaklı çatı köşeleri; ortak
ABI/işlevler/kısayollar aynı. Yeni paketin canlı görünüm/kullanım kabulü beklenir.
Guardian sırada, henüz uygulanmadı. Önceki Snowgrave-bekliyor kayıtları tarihseldir.
Kullanım: docs/ADVENTURE.md; karar: docs/decisions/0018-adventure-theme.md.

# Güncel durum

Son inceleme: **2026-10-19**. Kaynak taban: **2.9.0 / Deltarune 0.3.1 / Snowgrave 0.1.0**.
Aşama: **Plague Tale ve Deltarune mevcut görünüm/kullanım onaylı; tema çizgisi görünüm/normal kullanım kullanıcı onaylı**. Genel yayın/lisans ve geniş dağıtım matrisi ayrı açık iş olarak kalır.
Bu kayıt uygulamaları kullanıcının cihazında çalıştırmış gibi yorumlanamaz.

## 19 Ekim 23:13 — Üçüncü tema: Snowgrave 0.1.0

Kullanıcı 23:11'de yeni ağaç/Kris görselini beğendiğini bildirdi; 0.3.1 cihaz SHA'sı
ve ayrı alt testleri raporlanmadı. Ardından üçüncü tema için Snowgrave'i seçti.
Yeni `deltarune-snowgrave` bağımsız paketi hazır: koyu umber/ivory/pas kırmızısı,
soluk altın, yumuşak dal/yaprak köşeleri ve ayrı kemer/boynuzlu silüet CP437 süsü.
Mevcut iki skin'in kaynakları değişmedi; işlevli surface/controller kopyalanmadı.

Wallpaper resmi Real-ESRGAN genel modeliyle 4× restore edildi. Tuval dokusunu fazla
keskinleştiren etki görsel kontrolde azaltıldı: %40 restorasyon + %60 Lanczos
orijinal; paket 3600×2025 RGB PNG. Orijinal 1200×675 JPEG korunur. Metadata/hash
restoration.json içinde. Bu sanatçının native yüksek çözünürlüklü kaynağı değildir.
Hyprland/Kitty/Hyprlock, ayrı Dolphin/Spotify/SDDM/terminal kaynakları tamamlandı;
harici kurucular hâlâ ayrıdır. Dolphin normal/seçili metni beyaz kaldı.

Seçicide üçüncü fotoğraflı kart, kısa ve ayırt edilebilir “Snowgrave” adı var.
Kart rengi/fontu artık id koşulundan değil bütünlüğü kontrol edilmiş Theme.qml
ve varlık envanterinden gelir. Hover/tek seçim/klavye/rollback davranışı korunur.
Ortak ABI mct-shell-2.9 değişmedi; kaynak alındıktan sonra update.sh gerekmez.
[Deneme](docs/SNOWGRAVE.md) · [Karar](docs/decisions/0017-snowgrave-theme.md).

Yerel hazırlama kontrolleri: **160 unittest**, **142 QML** bytecode derlemesi,
network imports, paket bütünlüğü, PNG decode/hash ve kaynak syntax kontrolleri.
Yeni Snowgrave görünümü/cihaz kabulü beklenir. Native Wayland, PAM, gerçek uygulama
veya fiziksel cihaz ölçümü bu ortamda yapılmadı; kaynak uygulanmış gibi sunulmaz.

## 19 Ekim 22:58 — Wallpaper 4× restorasyonu

22:57 kullanıcı 0.3.0 için başarılı check/apply ve GitHub push logunu paylaştı;
`feature/deltarune-hidden-tree`, commit `8464b3f749ebd60460783c736741c3771e48f36a`.
“Tamam bu hazır” dedi; tek yeni eksik düşük wallpaper kalitesi. Görünümün önceki
bekleyen kabulü bu beyanla güncellendi. 22:58'de önerilen Real-ESRGAN yolunu
denemeyi açıkça istedi.

Genel ve anime modelleri aynı Kris/ağaç bölgesinde karşılaştırıldı. Fırça dokusunu
daha fazla koruyan resmi `RealESRGAN_x4plus` seçildi; 1200×675 → 4800×2700 RGB
PNG üretildi. Sinir ağı restorasyonudur; sanatçının native yüksek çözünürlüklü
orijinali veya kaynak piksellerle eşit dönüşüm değildir. Orijinal JPEG değişmedi.
Model/source/output hash'leri ve işlem parametreleri
`themes/deltarune/restoration.json` içinde. Wallpaper, shell, lock cover fallback
ve ayrı SDDM kaynak görseli aynı PNG'yi kullanır; tema sürümü 0.3.1.
Ortak runtime, kısayollar, palet ve panel düzeni değişmedi. Yeni görüntünün
kullanıcının ekranındaki kalite kabulü beklenir; SDDM hâlâ ayrı kurucudur.

19 Ekim bu revizyon için dört RGB PNG'nin tam decode/4800×2700/hash eşitliği,
orijinal JPEG hash'inin korunması ve Engine.load manifest bütünlüğü denetlendi.
İki mevcut Qt Deltarune revizyon testi geçti (konum/merkez tercihi, font/alt şerit
ve kurulu wallpaper'ın yeni canonical PNG ile eşitliği). Launcher QML render'ı
görsel incelendi; diğer yüzey preview'ları da yeni wallpaper ile yenilendi.
Önceki 112 test/116 QML sonucu 0.3.0'a aittir; hepsi bu görsel revizyonda tekrar
çalıştırılmış gibi sunulmaz. Native oturuma bu ortamdan kurulmadı.

## 19 Ekim 21:34 — Dört referans, önce indigo/fuşya ağaç teması

Kullanıcı dört Deltarune referansını ayrı tema olarak kabul etti. Önce mevcut
`deltarune` son üretilen ağaç/Kris konseptine taşındı (0.3.0): indigo yüzeyler,
lavanta yazı/ikon, ince fuşya dal kırıkları; kompakt sol launcher, sağ medya ve
controls. Portre başlıkları yerine sade semboller var. Ayarlar/diğer yüzeyler aynı
Theme/OrnamentFrame üzerinden güncellendi. Plague Tale ve ortak runtime değişmedi.

Wallpaper kaynağı sağlanan 1200×675 JPEG; wallpaper/shell/lock fallback/SDDM
kopyaları kayıpsız PNG dönüşümü. Kitty, Hyprland border, Hyprlock ve ayrı
Dolphin/Spotify/SDDM/CP437 adaptörleri yeni görsel dile uyarlandı. Dolphin normal/
seçili metni beyaz kaldı. Bağımsız adaptörler otomatik kurulmaz, ilk yedek akışı
değişmedi. [Deneme ve sınırlar](docs/DELTARUNE.md).

Üç diğer orijinal/dört AI konsepti `design/deltarune/` içinde tasarım kaydıdır;
Guardian, neşeli gün batımı ve Snowgrave sonbahar henüz uygulanmış tema değildir.
`preview.png` ve güncel yüzey görüntüleri gerçek Qt render'ıdır. Yeni paket
görünümünün hedef oturumda kullanıcı kabulü açık; önceki 0.2.0 onayı yeni görsele
otomatik aktarılmadı. [ADR-0016](docs/decisions/0016-deltarune-four-worlds.md).

19 Ekim hazırlama kontrolü: **112 unittest** geçti (42 Deltarune, 33 core,
5 adapter, 10 greeter, 2 shared-surface, 1 iki-skin OSD, 3 lock layout,
6 terminal, 4 picker bridge, 6 picker UI). Yeni picker vakası aynı tema 0.2.0'dan
güncel sürüme geçişi kontrol eder; eski sabit aktif sürüm fixture'ı katalogdan
okunur. **116 QML** bytecode derlemesi (tema skin'leri dahil), network imports,
manifest bütünlüğü, Python/Bash syntax ve değişen belge linkleri geçti.
Gerçek Wayland, PAM, canlı uygulama veya fiziksel cihaz ölçümü yapılmadı.

## 19 Ekim 13:22 — Tema çizgisi kullanıcı onayı

Europe/Riga 13:22 kullanıcı: “oo bu çok güzel olmuş güzel de çalışıyor.”
Tema çizgisinin görünüm/normal kullanım kabulü kaydedildi. Son paylaşılan kaynak
`a80d08e0fa80f3069f4e4c37fb49570b77ea568f`; cihazdaki SHA ayrıca raporlanmadı.
Bu onay aynı arayüzün tekrar normal kullanım kabulünü istememek içindir; tek tek
reboot/harici ekran/felaket kurtarma senaryoları ölçülmüş gibi işaretlenmez.
Önceki yeni seçici-native-bekliyor notları bu beyanla güncellenmiştir.

Güncel kısa kalanlar [CURRENT_BACKLOG](docs/CURRENT_BACKLOG.md) içindedir. Şu an
kullanıcı tarafından bildirilmiş açık günlük kullanım hatası yok. Harici uygulama
uyarlamalarının otomatik tema geçişine bağlanması henüz uygulanmamış bir kapsam
seçeneğidir; bu durum eski kurucuların bozuk olduğu anlamına gelmez. Son onay
sonrası bu işte yeni özellik veya merge yapılmadı; yalnız kayıtlar güncellendi.

## 19 Ekim 01:07 — Tema çizgisi ve koşullu Super+G

Kullanıcı önceki ayrı uygulama/grid ve check→apply akışını rahat/stilize bulmadı.
Yeni talep: ortada çizgi, sıralı temalar, hover ile genişleyen fotoğraf, tek seçimle
arka planda kontrol/apply; Super+G yalnız boşsa. Bu yeni talep önceki açık konum
kararının yerini alır. Eski arayüzün beğenildiği veya son kabulü olduğu söylenmez.

`theme.sh menu` artık normal pencere değil, odaklı ekranda keyboard-exclusive
Wayland overlay açar. Warm katman `themes.toggle` IPC ile anında toggle edilir;
ana masaüstü shell restart'ında worker'ın kesilmemesi için ayrı QS yaşam döngüsü
korunur. UI'da FloatingWindow veya görünür ikinci uygulama yoktur. Başarılı geçiş
650 ms sonra kapanır; Esc/dışarı tıklama/Super+G gizler, devam eden işlemi kesmez.
Fotoğraf büyümesi hover'dır; click/Enter mevcut Engine.apply içindeki zorunlu
kontrolleri bir kez yapar, ikinci check düğmesi yoktur. Hata gerçek aktif temayı
korur ve panelde kalır. Kullanıcının fontScale/reduceMotion tercihleri okunur.

`theme.sh bind --check` canlı `hyprctl -j binds`, temiz config ve yeni overlay QML
compile kontrolü yapar. `theme.sh bind` ortak kilit altında tekrar kontrol eder,
yalnız sahipli Super+G bloğunu ekler ve reload sonucunu doğrular. Dolu/dinamik
keycode/bozuk JSON veya kişisel block değişikliği korunur. İlk masaüstü yedeği
oynamaz; ayrı binding yedeği tutulur. `theme.sh unbind` yalnız aynı bloğu kaldırır.
Yeni root/ABI/source update gerekmez. [Kullanım](docs/THEME_PICKER.md).
Native yeni layer/focus/Super+G sonucu kullanıcı cihazında hâlâ denenmelidir.

## 19 Ekim — Deltarune onayı ve fotoğraflı tema seçici

00:24 Europe/Riga kullanıcı: “Aynen dolphin de değişti. Devam edebiliriz.”
Önceki komutlar/diğer uyarlamalar çalışıyor beyanıyla birlikte son bilinen
Dolphin görsel sorunu kapanmıştır. Deltarune mevcut görünüm/kullanım onayı
alındı; her PAM/sensör/harici ekran alt testi ayrıca ölçülmüş sayılmaz.
Plague Tale'in önceki onayı korunur. Aşağıdaki bekleyen kabul kayıtları tarihsel.

`bash theme.sh menu` ayrı QuickShell penceresinde gerçek paket fotoğraflarını,
aktif sürümü, büyütülmüş resmi, kontrol/uygula ve onaylı önceki temaya dönüşü sunar.
Yerleşim/bar düğmesi/global kısayol seçilmedi. Pencere ana shell'in dosyalarını
ithal etmez ve durdurulan shell süreci değildir; görsel işlem mevcut core'un
snapshot/kilit/journal/geri dönüşünü kullanır. Sadece katalog açmak kurulum yapmaz.
Dolphin/Spotify/SDDM/terminal süsü ayrı kurucular olarak görünür biçimde açıklanır.

Seçici repo aracıdır: kurulu 2.9.0 üstüne git pull yeterli; update.sh/tema rollback
ve adaptörlerin tekrar kurulması gerekmez. [Kullanım](docs/THEME_PICKER.md).
Hazırlama kontrolü ve native sınırı [VALIDATION](docs/VALIDATION.md) içinde.
Yeni seçicinin hedef Wayland oturumunda denenmesi beklenir.

## 18 Ekim — 2.9 kullanıcı denemesi / Dolphin ikon düzeltmesi

Kullanıcı yükseltme rehberindeki komutların çalıştığını ve Dolphin dışındaki
uyarlamaların değiştiğini bildirdi. Bu, yeni kullanım geri bildirimidir; ayrı
ölçülmüş bütün PAM/donanım senaryolarının testi sayılmaz. Paylaşılan Dolphin
fotoğrafında koyu mavi zemin/beyaz yazılar uygulanmış, klasörler eski pirinç
rengindedir. Kaynakta Deltarune SVG klasörlerinin Plague Tale ile birebir aynı
olduğu doğrulandı; önceki adaptör tamamlama iddiasının bu kısmı hatalıydı.

14 klasör/yer SVG'si camgöbeği basamaklı biçime uyarlandı. Header/Complementary
zeminindeki kalan eski zeytin tonları giderildi. Ortak kurucu, beyaz yazılar,
başlatma yolları ve ilk yedek değişmedi. Var olan adaptör testi iki temada kurulan
ikonların kaynakla eşitliğini, farklılığını ve kullanıcının orijinal ikonunun
restore edilmesini de denetler. Qt render'ında 16/80 px örnekler incelendi.
Hedef cihazda yeni Dolphin görünümü onayı bekleniyor. Bu düzeltme için kaynak
update/tema rollback gerekmez; yalnız Dolphin adaptörü tekrar uygulanır.

## 2.9.0 — Ortak etkileşim ve Deltarune tamamlama

18 Ekim kullanıcı denetim bulgularını kapatmayı başlattı. `shell/surfaces/`
17 işlevli şablon ve ortak PanelSlot içerir; iki temanın ui view'ları görsel
property/delegate sağlayan wrapper'lardır. Menülerde komut, input veya onay
mantığının ikinci kopyası yok. Palet/font/çerçeve/yerleşim ayrılığı korunur.
Ortak kaynak düzeltmesi iki temaya da gider; yeni görsel tema salt paletle sınırlanmaz.

Panel ilk kullanımda yüklenip yeniden kullanılır. Eski Loader uyarısını üreten
12 tekrar geçti; iki temada 12 tur/4 panel yeniden boyutlandırma, tek instance ve
onay temizliği kontrolü de geçti. Aynı ayarlar/launcher/Alt+Tab sözleşmeleri her
iki temada çalıştırıldı. Sensör izlemesi panel kapalıyken hâlâ durur.

Hyprlock'un görsel layout'u source fragment oldu; stok eski görünüm güvenli
şekilde taşınır, özel config korunur ve tam tema check uyarlama ister. Deltarune
saat/parola/medya sunumu, Dolphin beyaz metinli palet/ikonları, Spotify CSS/paleti,
CP437 fountain süsü ve SDDM skin'i var. SDDM login controller'ı ortaktır. Harici
kurucular aynı first-backup/restore ve adblock başlatıcı korumasını kullanır;
shell apply bunları sessizce yeniden kurmaz.

ABI `mct-shell-2.9`. Eski aktif tema **eski kaynakla** geri alınmadan dal değiştirilmez.
[Yükseltme](docs/UPGRADE_2_9.md) · [Karar](docs/decisions/0014-shared-interaction-templates.md).
Yerel offscreen/mock doğrulama [VALIDATION](docs/VALIDATION.md) içinde. Gerçek yeni
lock/PAM/giriş, Spotify/Dolphin ve Wayland son kabulü açık. Fotoğraflı tema menüsü
bu işte eklenmedi; konumu hâlâ kullanıcı kararıdır. Önceki denetim aşağıda tarihsel kayıttır.

## Kaynakta bulunanlar

QuickShell bar; launcher; güç menüsü; kontrol paneli; bildirim geçmişi/toast/DND;
MPRIS medya; donanım paneli; sürüklenebilir OSD; pil/şarj durumu; Hyprlock medya
bölümü; ayrı SDDM teması; Dolphin/Spotify eklentileri; kurulum/güncelleme/restore.
Shell QML paleti/font aileleri/varlıkları/hareketi `Theme.qml`, dış yüzey ölçüleri
`SurfaceLayout.qml` üzerinden paylaşılır. Yerel çizim/iç düzen ölçüleri ve harici
adaptörler ayrı kalır; bu tam tema motoru değildir.
Alt+Tab ve hesaplamalı launcher normal kullanımı kullanıcı tarafından onaylandı.
Ortak ayarlar, terminal/Dolphin ve Plague Tale'in son canlı kabulü kullanıcı tarafından
onaylandı. Komut satırı tema çekirdeği vardır; görsel tema menüsü henüz yoktur.
Menünün yeri kullanıcı kararını bekler; Preferences konumu kabul edilmedi.
Önceki 17 Ekim karar kaydı: kullanıcı ortak davranış + görsel paket + uygulama adaptörleri
yaklaşımını ve gerçek ekran görüntülü tema önizleme kartlarını onayladı. Bu,
seçicinin uygulanması veya ikinci temanın başlaması değildir. O mesaj native giriş/kalıcılık/restore sonucunu içermiyordu;
aşağıdaki daha yeni kullanıcı onayı bu bekleme durumunun yerine geçer. Yalnız gereksinim belgeleri güncellendi;
yerel Markdown dosya bağlantıları ve `git diff --check` geçti, runtime değişmedi.

## 18 Ekim — Deltarune tamamlama denetimi

Kullanıcı eksik kontrolü, sorun yoksa tema değiştirme aşamasına geçilmesini
istedi. [Denetim](docs/DELTARUNE_AUDIT.md) sonucu kapı henüz kapanmadı: hızlı
panel/resize testinde tekrarlanabilir Loader uyarısı, view'larda çoğaltılmış
etkileşim mantığı, lock parola/saat ve SDDM/Dolphin/Spotify/terminal süsü görsel
eksikleri var. Fotoğraflı seçici bu işte başlatılmadı; menü yeri açık kalır.

31 core, 15 preferences, 12 file-manager ve mevcut iki tema Qt/OSD/syntax/API
kontrolleri çalıştırıldı. Deltarune 42'lik suite ilk koşuda 1 Loader uyarısı
nedeniyle başarısız, ikinci koşuda geçti; pozisyon testinin 12 tekrarından 9'u
aynı uyarıyla başarısız. Bu nedenle “tüm kontroller yeşil” veya native hata
kanıtı olarak sunulmaz. Runtime/installer değiştirilmedi. Ayrıntılı komutlar,
sınırlar ve kapanış koşulları denetim dosyasındadır.

## Deltarune 0.1.1 — ilk kullanıcı revizyonu

18 Ekim 14:50 Europe/Riga: kullanıcı canlı Deltarune masaüstü ekran görüntüsü
paylaştı ve üç revizyon istedi. Bu, paketin hedef oturumda açıldığını gösterir;
bütün işlevlerin veya yeni düzenin son kabulü değildir.

- Kontrol menüsü sağda; arama önceki sol konumunda. Mevcut merkez panel tercihi
  açıkça değiştirilmez; açıksa merkez önceliği korunur.
- Alttaki parti şeridi ve onun 80 piksel exclusive zone'u kaldırıldı. Ortak
  opsiyonel pencere sözleşmesi yerinde; Deltarune view'ı boş ve flag false.
  Sürekli sensör izleme de kapanır, yalnız Super+T donanım paneli açıkken sürer.
- Wallpaper, shell ve lock medya fallback'ı kullanıcının **images_upscaled.jpeg**
  dosyasından 2048×1151 PNG'ye dönüştürüldü. JPEG'in çözümlenen pikselleriyle
  eşitlik denetlendi; resize veya ikinci üretim yapılmadı. Kaynak JPEG saklandı.
  Görüntü cache'i içeriğe bağlı yeni yoldan yenilenir.

Ortak shell/ABI değişmedi; aktif Deltarune üstüne `git pull --ff-only`, sonra
`theme.sh check/apply deltarune` yeterli. Source update/restore gerekmez.
42 Qt + 31 core test geçti; yeni iki Qt kontrolü sağ/sol konum, merkez tercih,
şeridin yokluğu ve wallpaper/font yüklemesini doğrular. Yeni native revizyonun
kullanıcı kontrolü bekleniyor. [Rehber](docs/DELTARUNE.md).

## 2.8.0 — Deltarune ilk deneme (önceki kayıt)

18 Ekim 14:38 kullanıcı logu: kaynak update/check ve QML kontrolü başarılı;
`theme.sh check deltarune` aşırı dar QuickShell sürüm koşulunda durdu. Tema apply
çalışmadı; Deltarune görünümü henüz kullanıcı tarafından görülüp onaylanmış değil.
Güncelleyicinin >=0.3.1 kuralı ile yalnız tam 0.3.1 isteyen theme-core kontrolü
çelişiyordu. Core da aynı minimum semver kuralına taşındı; v öneki ve stderr
çıktısı kabul edilir, eski/okunamayan sürüm hatası gerçek çıktıyı gösterir.
Kullanıcının kesin güncel QuickShell sürümü bu logda bulunmuyor; tahmin edilmedi.
Aday QML compile ve otomatik rollback korunur. Fix yalnız repo CLI/test/belgelerdir;
başarılı source update'i tekrar çalıştırmak gerekmez.


18 Ekim Europe/Riga: kullanıcı araştırılmış konsepti ve kendi sağladığı
`Deltarune.webp` arka planına uyarlamayı gördükten sonra “Hadi başlayalım” dedi.
Bu, ikinci temanın geliştirilmesi için açık onaydır; son tasarım/kullanım kabulü
henüz değildir. [Rehber](docs/DELTARUNE.md) · [ADR-0013](docs/decisions/0013-deltarune-first-trial.md).

Siyah/camgöbeği kesik köşeler, paket içi Departure Mono fontu, gerçek oyun menü
portreleri, solda launcher/yan paneller, kompakt medya, kare slider ucu, Kitty
paleti ve lock medya renkleri eklendi. Bütün shell yüzeyleri aynı backend/state'i
kullanır. Üç bölümlü alt şerit mevcut sensör/ses/pil verilerini gösterir; unavailable,
mute ve charging durumları ayrı. Şerit her monitörde 80 mantıksal piksel ayırır.
2 saniyelik mevcut sensör okuyucu bu temada şerit için açık kalır; uyuyan GPU'yu
okumama koruması değişmedi. Plague Tale'de şerit kapalı, eski donanım izleme
sadece panel açıkken çalışır.

Paket ABI'si `mct-shell-2.8`: ortak shell isteğe bağlı PartyStrip pencere/view'ını
barındırır. Plague Tale uyumlu boş view/default false ile güncellendi; görünümü
aynı. Komutla apply/rollback ve kullanıcı tercihleri korunur. Menü konumu seçilmedi.
`bash preview.sh deltarune` kurmadan geçici DemoContext açar; canlı IPC/ayar/installer
çalıştırmaz. Paket preview PNG'si yapay zekâ referansı değil, gerçek Qt render'ıdır.

Doğrulama ve kalan sınırlar [VALIDATION](docs/VALIDATION.md#280--deltarune-ilk-deneme)
içinde. Gerçek Wayland, kullanıcı GPU/sensör, fontun 1.6 ölçek sonucu ve yeni tema
geçişi hedef oturumda denenmeyi bekliyor. SDDM, Dolphin, Spotify ve terminal
madalyonunun Deltarune görsel uyarlaması sonraki revizyonda; mevcut ayrı adaptörler
automatik değiştirilmez. Lock parola/saat alanı da bu paketin kapsamına alınmadı.

## 2.7.0 — Kullanıcı kapanışı ve tema paket çekirdeği

2026-10-17 Europe/Riga: kullanıcı önceki yanıttaki **1. son canlı kontrol maddesine**
“1 zaten tamam full + full kullandım gün boyunca gayet güzeldi” dedi; **2. geçiş
çekirdeğini** Codex'e bıraktı ve ikinci oyun seçimini bu işin sonrasına erteledi.
Kullanıcının açık tamamlandı beyanı, son kullanım/görsel kapanış onayı olarak
esas alındı. Tek tek log/cihaz ölçümü sunulmuş veya burada PAM testi yapılmış
sayılmaz; aynı kabul tekrar istenmez. PR #10 beklenen baş
`a7fe18d4fb8d430934c3b8180f3b31583a26a5b6` ile main'e alındı
(merge `b3cb98f565d20ba89fcf3ba92bc74df91a7279f9`).

`theme_core.py` ve `theme.sh`: list/status/check/apply/rollback/recover.
`themes/plague-tale/` manifest, gerçek mevcut masaüstü preview PNG'si ve 38
görsel dosya içerir. Ortak servis/state/IPC/kısayol kodu paket dışında kalır.
Engine salt ön kontrol, geçici QML derleme, işlem snapshot'ı, atomik dosya yazımı,
hazır olma denetimi ve otomatik geri dönüş yapar. Manuel dosya değişikliği,
symlink, başka kurulumun snapshot'ı ve bozuk paket reddedilir. Wallpaper yolları
monitör başına kaydedilir; fit modu mevcut hyprpaper config'inden okunur.
Update aynı kilidi kullanır; aktif temayı değiştirecek kaynak güncellemesi
önce açık tema rollback'i ister, sessizce varsayılana dönmez.

Bu çekirdek shell/görsel varlıklar, Hyprland appearance, lock **medya** alanı ve
Kitty include dosyasını yönetir. SDDM, Dolphin ve Spotify ayrı kuruculardır;
“uygulandı” sonucu onların yeniden kurulduğu anlamına gelmez. İlk paket mevcut
kabul edilmiş Plague Tale görünümüdür. İkinci tema seçilmedi/üretilmedi; menü
konumu açık, fotoğraflı kart gereksinimi kabul edilmiş fakat UI uygulanmamıştır.

Yerel çalışma ortamı bu tur kullanılamadı; GitHub üzerinden kaynaklar okundu ve
GitHub Actions runner'ında test çalıştırıldı. **28 çekirdek + 15 preferences +
12 file-manager = 55 test**, Python/Bash syntax başarılı:
[CI run](https://github.com/EMOLACRIA/MCT/actions/runs/39054714755),
kod başı `6d3b6f2eb9472256b49049e30c72efdb63ecc2a2`.
Süreç/Hyprland/Quickshell etkileşimi fake runtime ile kontrol edildi. Yeni
çekirdeğin gerçek Wayland/PAM/harici uygulama işlemi CI'da çalıştırılmadı.
[Rehber](docs/THEME_PACKAGES.md) · [ADR-0012](docs/decisions/0012-theme-package-core.md).

## 2.6.2 — Son cila ve kontroller (önceki kayıt)

17 Ekim: kullanıcı 2.6.1 normal kullanımını onayladı; PR #9 beklenen head
`136f43a29e56617597b77e78abbad4abda3abdc4` ile main'e alındı
(merge `bc40e3782753f9f51ee786bb6e2c5dcf7c779f40`).

SDDM wallpaper dosyasının kesilmiş olduğu Qt image decode ile bulundu; sağlam
ana PNG'nin birebir öneki olduğu denetlenip tam kopyayla onarıldı. Küçük ekran
saat/kart çakışması, kaydırma ve klavye görünürlüğü düzeltildi. Boş oturum listesi
girişe izin vermez. Hyprlock medya cache'i bozuk JSON/türlerde toparlanır.
Kesilmiş power preview'ı ve SDDM preview'ı güncel fixture'lardan render edildi.
Yeni işlev, tema seçici veya global kısayol yok. [ADR-0011](docs/decisions/0011-release-polish.md).

2026-10-17: 5 Qt greeter, 4 SDDM dosya install/restore/rollback ve 6 CP437
medallion testi geçti. Mevcut 12 shell UI, 10 ayarlar, 11 Alt+Tab, 7 calculator,
4 watcher Qt testleri; OSD/ikon, network import, gerçek Qt palet, 17 PNG decode;
37 QML derlemesi ve 122 QuickShell 0.3.1 binding kontrolü geçti. Watcher fixture'ı
ilk geniş koşuda Preferences.js yolu eksikliğiyle başarısız oldu; fixture'a logic
bağlantısı eklendi ve dört test yeniden geçti. Bu bir native bildirim hatası değildi.

12 file-manager, 10 süreç keşfi, 10 Spotify, 15 tercih, 6 binding stdlib testi;
uygulama kurucu/helper fixture'ları ve üç Node kontrolü de geçti. Hyprlock alanları
0.9.6 kaynağıyla karşılaştırıldı. 40 Python parse, 26 Bash syntax, yerel Markdown
dosya bağlantıları ve diff whitespace kontrolü geçti. Komutlar/sınırlar
[VALIDATION](docs/VALIDATION.md#262--son-cila-ve-kabul-sınırı) içinde.

Kod ve kontrollü test cilası tamamlandı; **M4 kapanmadı**. Native kalıcılık,
PAM/login/lock, fiziksel cihaz/çoklu ekran ve tam kullanıcı restore kabulü açık.
Lisans seçimi/varlık haklarının yayın kapsamı da açık karardır. Kullanıcının
istediği [tema geçiş araştırması](docs/THEME_SWITCHING_RESEARCH.md) bu kontrollerin
ardından tamamlandı: HyDE/ML4W/Caelestia/Noctalia/Vitreus birincil kaynakları,
gözlem/çıkarım ve runtime sınırları belgeli. Menü yeri kararlaştırılmadı.

## Son kullanıcı geri bildirimi ve açık işler

| Kimlik | Durum | Kanıt / sonraki adım |
|---|---|---|
| PT-001 | Doğrulandı | 2026-10-17: kullanıcı PR #1 dalını uygulayıp launcher/Super+E tutarlılığını “Aynen çalışıyor” diyerek onayladı. Kod: `62cfe809d0274fd2ec99a8aca4e37f117b20fe9f`; 12 regresyon kontrolü de geçti. |
| PT-002 | Çalışma onaylandı / adblock sonucu ayrıca ölçülmedi | 17 Ekim: kullanıcı “Yo çalışıyo bende” diyerek Spotify'ın çalıştığını onayladı. Sistem Spotify 1:1.3.4.258-2, adblock 1:1.1.1-1, CLI 2.45.3-1. Girdiler temalı sarmalayıcıya yönleniyor ve LD_PRELOAD korunmuş. Belgelenmiş Linux aralığı dışında olmak hata kanıtı değildir; 2.2.5 yalnız uyarı verir. Özel kopyanın kesin sürümü ve reklam engelleme ölçümü kayıtlı değil. |
| PT-003 | Kullanıcı onayı | 17 Ekim: kullanıcı PR #4'ün Dolphin/OSD/Steam kontrolleri sonrasında bildirim süresi dışında sorun olmadığını onayladı. Önceki gerçek Qt aktif/pasif metin ve kontrast kontrolü de geçti. |
| PT-004 | Kullanıcı onayı / süre tercihi uygulandı | 17 Ekim: PR #4 testleri için süre dışında sorun yok onayı geldi. Varsayılan/toast süresi 4500 ms yapıldı; 1200 ms yalnız önceki test komutuydu. Fiziksel şarj geçişi ayrıca raporlanmadı; M4 kabul listesinde korunur. |
| PT-005 | Normal güncelleme kullanıcı onayı / geniş restore kabulü M4'te | Kullanıcı kümülatif PR #4 dalında sorun bildirmedi. 10 kontrollü süreç keşfi testi geçti. Farklı kullanıcıyla fresh install/restore canlı testi yapılmış sayılmaz. |
| PT-010 | Normal kullanım kullanıcı onayı | 17 Ekim: kullanıcı “alt tab çok güzel çalışıyor” diyerek PR #5 kullanımını onayladı. Main merge `915a9990a7d835cba6281b43b08af1911328355f`. Çoklu monitör çıkarma ve yakalama gibi ayrı ayrıntılar raporlanmadı; M4 listesinde kalır. |
| PT-011 | Normal kullanım kullanıcı onayı | 17 Ekim: kullanıcı “Güzel çalışıyor devam edebilirsin” diyerek PR #6 akışını onayladı. Enter seçili satırı çalıştırır; Ctrl+Enter seçimden bağımsız hesap sonucunu kopyalar. Her alt test ayrı ayrı raporlanmış sayılmaz. |
| PT-012 | Son canlı kontrol kullanıcı onayı | Önceki uygulama açılışı onayına ek olarak 17 Ekim kullanıcı önceki son kontrol maddesinin tamamlandığını ve gün boyu full kullandığını söyledi. Bu kullanıcı beyanı kabul edildi; bağımsız cihaz logu ölçümü değildir. |
| PT-013 | Normal kullanımda sorun bildirilmedi / ayrıntılı kabul açık | 17 Ekim kullanıcı “Şuan bi sıkıntı yok gibi. Devam edelim” dedi. PR #8 ana dala `3c8b1e0215be52fbf465ee696f4a98e0ca7e1456` ile alındı (head `94814c7d91bcdc82851fb1e4e491d85ad4287748`). 2.5.1: tray, medya/power kaydırma ve uzun ad sınırları; 7 Qt testi. Her tray/ölçek/çoklu ekran alt testi tek tek raporlanmış sayılmaz. |
| PT-014 | İpucu düzeltmesi normal kullanım kullanıcı onayı / geniş kabul açık | 17 Ekim: kullanıcı 2.6.1 sonrası “Tamamdır gayer güzel” dedi. İncelenen head `f0525e0b19cbfca4a454b188681b7e79bdd79ed0`; ipucu düzeltmesi normal kullanımda onaylandı. 12 Qt testi, 37 QML, 122 native binding önceki kayıttadır. Bu bildirim bütün M3 yüzeyleri, çoklu ekran veya PT-012 kalıcılık kabulü değildir. |
| QA-001 | Kısmen açık | Dört stdlib uygulama/süreç kontrolü ve Node backend kontrolü bağımsız checkout'ta çalışır. Qt watcher, shell-revisions, app-revision23, shell-syntax ve artık shell-ui kendi checkout'unu bulur; Qt/Node/derleyici bağımlılıkları açıkça gerekir. Diğer eski fixture bağımlılıkları ve genel CI hâlâ açık. |
| ASSET-001 | Son canlı kontrol kullanıcı onayı | CP437 dosya/kurulum testlerine ek olarak 17 Ekim kullanıcı önceki son kontrol maddesinin tamamını onayladı; madalyon son görünümü bu beyanla kabul edildi. |

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

## 2.2.6 bildirim yaşam döngüsü ve M1 kontrolleri

2026-10-17: hedef QuickShell `v0.3.1` kaynakları incelendi. D-Bus `Notify`,
timeout'u `Notification::updateProperties` üzerinden doğrudan `bExpireTimeout`
alanına aktarır. Header açıklaması saniye dese de uygulama birim dönüşümü
yapmaz. Bizim tekrar 1000 ile çarpmamız kaldırıldı. Aynı nesnenin güncellenmesi
ayrı `notification` olayı üretmediği için property sinyalleri izleniyor.

`node checks/test_shell_backend.js` geçti: 5000/120 ms, varsayılan/süresiz süre,
yenilemede unread/kart/handler tekliği, timer temizliği, DND/geçmiş/eylemler,
transient geçişi ve sağ/sol/orta tray eylemleri kontrollü servislerle denetlendi.
`python3 checks/test_notification_watcher.py` — **4 gerçek Qt testi geçti**;
sinyal grubunu tek yenileme, eylem/süre/transient değişimi ve kapanış sonrası
bekleyen yenilemenin iptali kontrol edildi.

Qt 6.10.2 ile `test_shell_revisions.py` OSD hover, ses drag/parlaklık bırakma,
gizlenme gecikmesi, ikon merkezleri ve düşük pil çizimini geçti.
`test_app_revision23.py` gerçek Qt paleti/kontrastı, önceki yedek geçişi ve
kontrollü Spotify başlangıç/rollback kontrollerini geçti. Bu dosyalar artık
eski build/ klasörü yerine kendi checkout'larını kullanır.
`test_shell_syntax.py` 23 QML dosyasını bytecode'a derledi.
Aynı tarihte 30 Python dosyası parse, 25 Bash dosyası syntax, yerel Markdown
bağlantıları ve `git diff --check` kontrolü geçti.

Native QuickShell bildirim D-Bus oturumu, Steam menüsü, gerçek pil geçişi ve
Dolphin arayüzü burada çalıştırılmadı. Değişmeyen payload'la hiç property
sinyali üretmeyen bir Notify tekrarını bu watcher algılayamaz; ADR-0005 sınırı
açıklar. Sonraki kullanıcı onayı aşağıda ayrıca kaydedildi.

17 Ekim PR #4 sonrası kullanıcı “Onun dışında sorun yok devam edebilirsin”
diyerek istenen Dolphin/OSD/Steam kontrollerini onayladı. Bildirim varsayılanı
ve toast sınırı isteğiyle 4500 ms yapıldı; uygulamanın açıkça istediği daha kısa
süreler korunur. `node checks/test_shell_backend.js` yeni varsayılanla geçti.

## 2.3.0 — Alt+Tab ve ana dal durumu

17 Ekim: kullanıcının süre tercihi uygulandı; PR #2–4 onaylanan düzeltmeler
ana dala birleştirildi. Main başı `cc546faabcf926f2d09c01cacf699e5f6892be33`.
Yeni PT-010 bu tabandan geliştirildi; diğer M2 işlerine henüz başlanmadı.

`WindowSwitcherState` MRU sırasını açıkken sabit tutar; bütün alanları ve alan/ekran
etiketlerini gösterir. Açılan/kapanan pencere, dış odak ve boş liste ele alınır.
Alt bırakma/Enter commit, Esc iptal; ekran çıkarma iptal; isteğe bağlı tek kare
önizleme. Özel Alt/Tab bağları korunur. Mevcut Overlay'in Loader sonrasında
kalan ertelenmiş focus callback'i, Loader'a bağlı Timer ile düzeltildi.

2026-10-17 kontrolleri: `checks/test_window_switcher.py` **11 gerçek Qt testi**;
`checks/test_switcher_bindings.py` **6 stdlib testi**; `checks/test_file_manager.py`
**12 kontrollü kurulum/güncelleme/restore testi**. Backend Node testi geçerli/eksik/
kapanmış pencere ve Lua/legacy dispatch'i denetler. `checks/test_shell_api.py`
**99 native property/handler** için QuickShell v0.3.1 kaynak karşılaştırması;
`checks/test_shell_syntax.py` **25 QML dosyası** bytecode derlemesi. Qt önizlemesi
1600×1000'de görüntülenerek liste ve seçili satır incelendi; 500×400 sınırları da
test edildi. OSD/ikon regresyon kontrolü tekrar geçti. 32 Python kaynağı parse,
25 Bash syntax, yerel Markdown yolları ve git diff whitespace kontrolü geçti.

Bu kontroller native Hyprland katman odağı, global kısayol, monitör çıkarma veya
pencere yakalama çalıştırmaz. Bunlar [hedef kabul listesinde](docs/VALIDATION.md#pt-010-alttab-kontrolü)
o inceleme sırasında açıktı; sonraki normal kullanım onayı aşağıda kaydedildi.

## 2.4.0 — Launcher hesaplama

17 Ekim 2026: kullanıcı Alt+Tab için “çok güzel çalışıyor” dedi; PR #5 beklenen
baş `84f71dd0d594a6334277790d8204c9309e269c9b` kontrol edilerek main'e birleştirildi.
Normal kullanım kabulü PT-010'u kapatır; raporlanmayan çoklu ekran çıkarma ve
native yakalama ayrıntıları geniş M4 test listesinde korunur.

`logic/Calculator.js` ortak aritmetik modelidir; uygulama araması her zaman aynı
filtreyi kullanır. Sonuç ilk satırdır; Enter/fare kopyalar, Ctrl+Enter seçimden
bağımsız sonucu kopyalar. Launcher açık ve ifade yerinde kalır; Ctrl+C normal
metin seçimini kopyalar. Eksik/hatalı ifade satır içi mesajdır; komut çalıştırılmaz.
Yüzde daima `/100`; örneğin `200+10%=200.1`, `200*10%=20`. Ondalık nokta/virgül,
parantez, unary işaret, `^` ve bilimsel sayı gösterimi desteklenir. 12 anlamlı
basamak gösterilir/kopyalanır; IEEE-754 hesabı ve sınırları belgelenmiştir.

2026-10-17 doğrulama:

- `node checks/test_calculator.js`: aritmetik/öncelik, yüzde, eksik/hata, uygulama
  sorguları, uzunluk/derinlik sınırı ve 300 bozuk girdi örneği geçti.
- `checks/test_launcher_calculator.py`: **7 gerçek Qt testi**; Enter/fare/Ctrl+Enter,
  Ctrl+C, karma sonuç gezinmesi, uygulama açma, Esc ve 900×600 sınırları geçti.
- `checks/test_shell_imports.py`: manifest + göreli JS import'u Qt network URL ile
  yüklendi; hesap sonucu 14 olarak okundu. Test bağımsız checkout'a taşındı.
- Node backend clipboard adaptörü; QuickShell v0.3.1 header/uygulamasına karşı
  writable clipboardText kontrolü; 99 native binding ve 25 QML bytecode geçti.
- Mevcut 11 Alt+Tab Qt testi, OSD/ikon kontrolü ve 12 update/restore fixture'i geçti.

33 Python kaynağı parse, 25 Bash syntax, yerel Markdown yolları ve git diff
whitespace kontrolü geçti. 1600×1000 Qt launcher render'ı görüntülenerek incelendi. Gerçek QuickShell
Wayland pano teslimi/başka uygulamaya yapıştırma bu ortamda çalıştırılmadı;
[hedef kabulü](docs/VALIDATION.md#pt-011-launcher-hesaplama-kontrolü) o incelemede açıktı.
Sonraki normal kullanım onayı aşağıda kaydedildi.

## 2.5.0 — Ortak ayarlar ve kalıcı kullanıcı tercihleri

17 Ekim kullanıcı hesaplamalı launcher'ın çalışmasını onayladı. PR #6 beklenen
baş `e8d7165cd3043f395e0eaf6b6a1068b690647b80` kontrol edilerek main'e birleştirildi;
merge `7b5351c087dfe9975d01e29bc0413c14e30d6d9f`. PT-012 bu tabandan geliştirildi.

Ses/kontrol panelindeki dişli Preferences ekranını açar; yeni global kısayol yok.
Shell fontu %90–120, azaltılmış hareket, yüzey saydamlığı %75–100; floating bar,
tarih/tray görünürlüğü, yan panel ortalama, OSD üst/alt konumu uygulanmıştır.
Theme.fontSize/duration ve ortak yüzey rengi bütün ilgili shell bileşenlerine bağlıdır.
Harici uygulama/Hyprlock/SDDM fontu bu tercihle değiştirilmez.

Tercihler `$XDG_CONFIG_HOME/mct/preferences.json` içinde, tema payload'ının dışındadır.
Python yardımcı doğrulama + geçici dosya/fsync/os.replace ile yazar; başarılı
cevap gelmeden native görünümde yeni değer etkinleşmez. JS/Python aynı JSON şema
bloğunu kullanır. Preview sadece bellektir. Bozuk dosya korunur; açık reset önce
kopyasını saklar. Bozuk tercihler terminal/dosya yöneticisi kısayolunu engellemez;
yardımcılar varsayılan uygulamalara döner, ayarlar ekranı hatayı gösterir.

Super+Q ve launcher'ın terminal isteyen uygulamaları aynı terminal.py seçimine
ulaşır (kurulu Kitty/Alacritty/Foot). Super+E seçilen FileManager desktop girdisini
GIO ile açar; Dolphin kullanıcı/system önceliği korunur. Özel Q/E bağları update
ile sahiplenilmez. Harici MIME ilişkileri veya uygulamaların kendi ayarları değiştirilmez.

2026-10-17: `checks/test_preferences.py` **15 kontrollü Python testi**;
`checks/test_preferences_ui.py` **10 gerçek Qt testi** (7 görünüm + 3 gerçek
storage-helper/model alışverişi); `node checks/test_preferences_model.js` geçti.
Atomik hata, bozuk dosya/reset yedeği, mevcut dosyanın update/rollback'te korunması,
terminal argümanları, GIO girdisi ve özel kısayollar denetlendi. %120 fontta üst ve
alt Preferences görünümleri 1600×1000'de incelendi; 900×600 sınırları test edildi.

Önceki 7 launcher + 11 Alt+Tab Qt, OSD/ikon (yeni launcher/settings yüzeyleri dahil),
12 update/restore + 6 Alt/Tab geçiş kontrolü ve Node backend geçti. Qt network
import testi yeni paneli de oluşturdu. **30 QML bytecode**, **105 native binding**
ve DesktopEntry categories/id kaynağı karşılaştırması geçti.

37 Python kaynağı parse, 26 Bash syntax, yerel Markdown yolları ve git diff
whitespace kontrolü geçti. Native QuickShell Process yaşam döngüsü, gerçek restart sonrası tercih yüklemesi,
Wlr bar reserve/OSD konumu ve seçili terminal/dosya yöneticisi başlatması bu
ortamda çalıştırılmadı. [Hedef kabulü](docs/VALIDATION.md#pt-012-ortak-ayarlar-kontrolü)
açıktır; bu testler Plague Tale tamamlanma kapısını kapatmaz.

## Sonraki iş

PT-012 hedef oturum kabulü; ardından M3 görsel/ortak sözleşme denetimi. Tema
değiştirici ve ikinci tema M4 kapısından önce başlamaz. Adblock ölçümü, fiziksel
şarj geçişi ve farklı kullanıcıyla fresh install/restore M4 listesinde korunur.

## 2.5.1 — M3 ilk yerleşim denetimi

2026-10-17: terminal/Dolphin açılışı kullanıcı onayı kaydedildi; PR #7 birleştirildi.
Ayarların native yeniden başlatmada korunması ayrıca doğrulanmış sayılmadı.
Kalabalık tray saat bölgesini aşmıyor; oklarla son simge erişilebilir, eylemler aynı
backend'e gidiyor. Uzun medya listesi ve küçük güç menüsü kaydırılabilir; klavye
seçimi görünür tutulur. Uzun oynatıcı/bildirim eylemi adları paneli genişletmez.
Normal güç menüsü %100/%120 ve yeterli yükseklikte kaydırma gerektirmez.

`MCT_QT_TEST_PATH=... python3 checks/test_shell_ui.py` — **7 gerçek Qt testi geçti**.
Eski build/desktop-style bağımlılığı kaldırıldı. Bütün 7 panelde %90/%120 font,
1600×1000/900×600/640×480 sınırları; 900/1132/1200/1600 bar genişlikleri ve 40'a
kadar tray; sağ tık, uzun içerik, boş veri, medya/güç klavye görünürlüğü denetlendi.
PNG örnekleri incelendi. Barın kalabalık tray kabulü en az 900 mantıksal genişliktir;
640×480 panel kontrolü daha dar barın tam tray erişimi anlamına gelmez.
Mevcut 10 Qt preferences, shell-revisions ikon/OSD, network import, 30 QML bytecode,
105 native binding ve Node backend kontrolleri geçti. Sınırlar ve kullanıcı denemesi
`docs/VALIDATION.md`; karar `docs/decisions/0009-responsive-surfaces.md` içindedir.

Native tray menü konumu/tekerlek ve çoklu ekran hedef oturumda bekliyor.
Görsel sabitlerin tamamını ayırma, lock/SDDM/uygulama bütünlüğü denetimi ve M4
kabulü henüz tamamlanmadı. İkinci tema/tema değiştirici geliştirilmedi.

## 2.6.0 — M3 ortak shell sunumu

2026-10-17: 2.5.1 için normal kullanımda sorun bildirilmedi; PR #8 merge
`3c8b1e0215be52fbf465ee696f4a98e0ca7e1456`. Ayrıntılı native kabul/kalıcılık
onayı varsayılmadı. Shell QML literal paleti, gövde/başlık font aileleri,
varlık URL'leri ve açık görsel animasyon süreleri Theme'e bağlandı. SurfaceLayout
bar/panel/OSD/toast/Alt+Tab dış ölçülerini native/preview arasında paylaşır.
Yedi panel ortak başlık; toast/geçmiş ortak eylemler; koyu ve sarılan ipuçları;
preview'de paylaşılan toast yığını uygulandı. Uzun toast eylemi taşması giderildi.

`MCT_QT_TEST_PATH=... python3 checks/test_shell_ui.py` — **9 test geçti**.
Başlık close/ek eylemleri, uzun/boş içerik, toast eylem/close/gizleme ve önceki
ölçek/sınır/klavye kontrolleri. 10 preference, 7 launcher, 11 Alt+Tab Qt testi,
ikon/OSD drag-hover, network import ve **35 QML bytecode** kontrolü geçti.
QuickShell 0.3.1 kaynak karşılaştırmasında **105 native binding** aynı kaldı.
Qt software render örnekleri incelendi. Bunlar native session kabulü değildir.

Yüzey ve harici adaptör haritası `docs/THEME_SURFACES.md`; karar
`docs/decisions/0010-shared-shell-presentation.md`. Yerel çizim/iç yerleşim
ölçülerinin tamamı merkezileştirilmedi. Harici uygulama/lock/SDDM kaynakları
shell paletini doğrudan import etmez; otomatik tema üreticisi yoktur.
Bu sürüm tema seçici eklemez; M3/M4 ve PT-012 kalıcılık kabulü açık kalır.

## 2.6.1 — İpucunun bar düğmesini örtmesi

2026-10-17 kullanıcı bar ipucunun anında açıldığını, düğmeyi kaplayıp tıklamayı
engellediğini bildirdi. Önceki offscreen sahnenin tam ekranı bu native 48 px
pencere clamp sorununu yakalamamıştı. PR #9 ana dala alınmadan aynı dal düzeltildi.
600 ms hover; basma/ayrılmada iptal; owner değişince yeni süre. HintBubble görünümü
paylaşılır; native bar HintPopup (PopupWindow) kullanır: target +8 px aşağı,
yatay slide, grabFocus:false, boş Region input maskesi. Panel/preview fallback
etkileşimsizdir ve owner'ın dışında konumlanır.

`MCT_QT_TEST_PATH=... python3 checks/test_shell_ui.py` — **12 test geçti**.
Yeni gecikme/konum/açıkken fare tıklaması ve basma iptali, owner/leave, bütün bar
hint'lerinin presenter bağlantısı ve QObject Loader bridge yükleme/boşaltması.
`test_shell_syntax.py`: **37 QML**; `test_shell_api.py`: **122 native binding**,
boş maskenin WindowTransparentForInput ve grabFocus:false'ın Qt::ToolTip flag
karşılığı 0.3.1 kaynağından doğrulandı. Network import ve ikon/OSD testleri geçti.
Native PopupWindow burada çalıştırılmadı; gerçek bar click-through/konumu kullanıcı
oturumunda son kontrol bekliyor. Kapsamlı PT-012/M3/M4 kabulü açık kalır.
