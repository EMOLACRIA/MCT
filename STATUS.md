# Güncel durum

Son inceleme: **2026-10-17**. Kaynak taban: **2.6.2 geliştirme sürümü**.
Aşama: **M0 tamamlandı; M1 normal kullanım onaylandı; M2 kalıcılık kabulü bekliyor; M3 ortak shell sunumu uygulandı / kabul bekliyor**. Plague Tale tamamlanmış değildir.
Bu kayıt uygulamaları kullanıcının cihazında çalıştırmış gibi yorumlanamaz.

## Kaynakta bulunanlar

QuickShell bar; launcher; güç menüsü; kontrol paneli; bildirim geçmişi/toast/DND;
MPRIS medya; donanım paneli; sürüklenebilir OSD; pil/şarj durumu; Hyprlock medya
bölümü; ayrı SDDM teması; Dolphin/Spotify eklentileri; kurulum/güncelleme/restore.
Shell QML paleti/font aileleri/varlıkları/hareketi `Theme.qml`, dış yüzey ölçüleri
`SurfaceLayout.qml` üzerinden paylaşılır. Yerel çizim/iç düzen ölçüleri ve harici
adaptörler ayrı kalır; bu tam tema motoru değildir.
Alt+Tab ve hesaplamalı launcher normal kullanımı kullanıcı tarafından onaylandı.
Ortak ayarlar ekranı ve kalıcı tercihler uygulandı; terminal/Dolphin açılışı onaylandı,
yeniden başlatmada kalıcılık kabulü bekliyor.
Tema değiştirici **yoktur**.
Menünün yeri kullanıcı kararını bekler; Preferences konumu kabul edilmedi.
17 Ekim yeni karar: kullanıcı ortak davranış + görsel paket + uygulama adaptörleri
yaklaşımını ve gerçek ekran görüntülü tema önizleme kartlarını onayladı. Bu,
seçicinin uygulanması veya ikinci temanın başlaması değildir. Son mesaj 2.6.2
native giriş/kalıcılık/restore testlerinin yapıldığına dair sonuç içermiyor;
mevcut kabul durumları korunur. Yalnız gereksinim belgeleri güncellendi;
yerel Markdown dosya bağlantıları ve `git diff --check` geçti, runtime değişmedi.

## 2.6.2 — Son cila ve kontroller

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
| PT-012 | Uygulama açma onaylandı / kalıcılık kabulü bekliyor | 17 Ekim kullanıcı “konsol da dolphin de düzgün açılıyor” dedi. PR #7 ana dala `683686f68729ae58cf277d7fb174bb687dfd328a` ile alındı. Bu bildirim ayarların restart/update/rollback sonrası korunduğu, native bar reserve/OSD tercihlerinin tek tek denendiği anlamına gelmez. 15 Python + 10 Qt kontrollü testi önceki kayıttadır. |
| PT-013 | Normal kullanımda sorun bildirilmedi / ayrıntılı kabul açık | 17 Ekim kullanıcı “Şuan bi sıkıntı yok gibi. Devam edelim” dedi. PR #8 ana dala `3c8b1e0215be52fbf465ee696f4a98e0ca7e1456` ile alındı (head `94814c7d91bcdc82851fb1e4e491d85ad4287748`). 2.5.1: tray, medya/power kaydırma ve uzun ad sınırları; 7 Qt testi. Her tray/ölçek/çoklu ekran alt testi tek tek raporlanmış sayılmaz. |
| PT-014 | İpucu düzeltmesi normal kullanım kullanıcı onayı / geniş kabul açık | 17 Ekim: kullanıcı 2.6.1 sonrası “Tamamdır gayer güzel” dedi. İncelenen head `f0525e0b19cbfca4a454b188681b7e79bdd79ed0`; ipucu düzeltmesi normal kullanımda onaylandı. 12 Qt testi, 37 QML, 122 native binding önceki kayıttadır. Bu bildirim bütün M3 yüzeyleri, çoklu ekran veya PT-012 kalıcılık kabulü değildir. |
| QA-001 | Kısmen açık | Dört stdlib uygulama/süreç kontrolü ve Node backend kontrolü bağımsız checkout'ta çalışır. Qt watcher, shell-revisions, app-revision23, shell-syntax ve artık shell-ui kendi checkout'unu bulur; Qt/Node/derleyici bağımlılıkları açıkça gerekir. Diğer eski fixture bağımlılıkları ve genel CI hâlâ açık. |
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
