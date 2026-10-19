# MCT — Plague Tale geliştirmesi

HyprCADE'in daha bütünlüklü devamı için geliştirilen Hyprland/QuickShell masaüstü.
İlk görsel tema **A Plague Tale**; masaüstü yüzeylerinde oyun veya tema markası yok.
Önce bu tema tamamen bitirilecek; ardından aynı işlev/kısayollarla görsel açıdan
çok farklı temalar ve bir tema değiştirici gelecek.

**Durum:** 2.9.0 / Deltarune 0.2.0 denemesi. Plague Tale son kullanım onayı
korunur. İki tema ortak etkileşim şablonlarını kullanır; Deltarune lock, SDDM,
Dolphin, Spotify ve karakter terminal uyarlamaları eklendi; kullanıcı mevcut
Deltarune görünümünü de onayladı. Fotoğraflı seçici `bash theme.sh menu` ile
masaüstü üzerinde yatay tema çizgisi olarak denenebilir. Hover önizleme,
tek seçimle kontrollü geçiş; `bash theme.sh bind` boşsa Super+G ekler.
[Seçici kullanımı ve kapsamı](docs/THEME_PICKER.md).

**2.8'den geçiş:** dal değiştirmeden önce eski aktif tema geçişlerini eski
kaynakla geri al, sonra source update ve yeni apply yap.
[Komutlar ve ayrı uygulama/SDDM adımları](docs/UPGRADE_2_9.md).

## Projeyi okumaya buradan başla

| Dosya | Amacı |
|---|---|
| [PROJECT_BRIEF.txt](PROJECT_BRIEF.txt) | Kullanıcının amacı, sınırlar ve kesin kararlar |
| [AGENTS.md](AGENTS.md) | Kod asistanları için kısa çalışma talimatları |
| [ROADMAP.md](ROADMAP.md) | Plague Tale'den yeni temalara aşamalar ve çıkış koşulları |
| [STATUS.md](STATUS.md) | Kaynakta olanlar, açık sorunlar, doğrulama durumu |
| [Özellik sözleşmesi](docs/FEATURE_CONTRACT.md) | Her temada aynı kalan işlev ve alışkanlıklar |
| [Mimari](docs/ARCHITECTURE.md) | Mevcut yapı ile planlanan ayrım |
| [Görsel yüzey haritası](docs/THEME_SURFACES.md) | Shell'in ortak sunumu ve ayrı lock/SDDM/uygulama adaptörleri |
| [Yayın kontrolü](docs/RELEASE_CHECKLIST.md) | İlk tema ne zaman bitmiş sayılır? |
| [Vitreus / Caelestia](docs/INSPIRATION.md) | Referanslar, incelenen sürümler ve alınacak fikirler |
| [Tema geçiş araştırması](docs/THEME_SWITCHING_RESEARCH.md) | HyDE, ML4W, Caelestia, Noctalia ve Vitreus; yöntemler ve öneriler |
| [Doğrulama sınırları](docs/VALIDATION.md) | Gerçekten çalıştırılan ile hedef oturum kontrolü farkı |
| [Kurulum ve sürüm geçmişi](docs/INSTALLATION.md) | Mevcut paketin ayrıntılı kullanımı |
| [GitHub'a yükleme](docs/GITHUB_PUSH.md) | ZIP içeriğini kaynak repo olarak yükleme |
| [Uygulama eklentileri](apps/README.md) | Dolphin ve Spotify kurulumu / geri alma |

## 2.7.0 — Tema paket çekirdeği

İlk paket Plague Tale; mevcut masaüstünün gerçek PNG önizlemesi ve görsel dosya
envanteriyle gelir. Menü eklenmedi. [Tam rehber](docs/THEME_PACKAGES.md).

```bash
bash theme.sh list
bash theme.sh status
bash theme.sh check plague-tale
bash theme.sh apply plague-tale
bash theme.sh rollback --check
bash theme.sh rollback
```

check hiçbir kurulu dosyayı değiştirmez. apply yalnız MCT shell'i yeniden açar;
oturumu kapatmaz. Tercihler, kişisel kısayollar ve ilk restore yedeği korunur.
Görünüm aynı kalabilir: ilk apply mevcut Plague Tale'i kayıtlı paket haline getirir.
SDDM/Dolphin/Spotify ayrı kurucularıyla kalır. Kaynak update aktif tema dosyalarını
değiştirecekse önce açık tema rollback'i gerekir; sessiz görünüm sıfırlaması yapılmaz.

28 çekirdek + 27 mevcut izole test ve syntax CI'da geçti. Gerçek cihazda ilk
çekirdek denemesi yukarıdaki check/apply/rollback akışıdır. Eski Plague Tale
kullanım onayı bu yeni komutların native çalıştırılmış olduğu anlamına gelmez.

## 2.6.2 — Son cila ve yayın öncesi denetim

SDDM'nin kesilmiş PNG'si sağlam proje kopyasıyla onarıldı; giriş kartı küçük
ekranda saatle çakışmaz, klavye odağı kaydırılan işlemi görünür tutar. Oturum
listesi boşsa giriş pasiftir. Parola hata/yeniden deneme ve güç iptali Qt fixture'ıyla
kontrol edildi; gerçek kimlik doğrulama ayrıca gerekir. Hyprlock medya yardımcısı
bozuk/tipsiz önbellekte toparlanır, yanlış türleri oynatma durumu saymaz.

CP437 kurulum/variant/restore, SDDM dosya rollback'i ve mevcut shell kontrolleri
geçti. [Kanıt ve kalan canlı kabul](docs/VALIDATION.md#262--son-cila-ve-kabul-sınırı).
Tema menüsünün yeri kullanıcı kararını bekliyor; arayüz eklenmedi.

Shell güncellemesi `bash update.sh --check && bash update.sh` ile uygulanır.
SDDM ayrı kurucudur: `bash sddm/preview.sh` yalnız preview açar. Önceden kurulu
SDDM temasını yenilemek için `sudo bash sddm/restore.sh`, ardından
`sudo bash sddm/install.sh --check && sudo bash sddm/install.sh` kullanılır.
Aktif oturum/servis yeniden başlatılmaz. Terminal madalyonu bağımsız ektir;
görseli değişmedi, yeniden kurulması gerekmez.

## 2.6.1 — Bar ipucu tıklamayı engellemez

İpucu 600 ms hover sonrası açılır; düğmeye basınca veya imleç ayrılınca kapanır.
Barın 48 px penceresine sıkıştırılmaz: ayrı, odak almayan ve tıklamaları geçiren
QuickShell popup'ı düğmenin 8 px altında açılır. Panel/preview Qt ipuçları da
etkileşime girmez ve düğmenin dışında konumlanır. Gecikme hareketi azaltma
seçeneğinden bağımsızdır. Düzeltme mevcut `refactor/shared-shell-presentation`
dalındadır; ayrı kurulum/restore gerektirmez.

12 Qt yerleşim/etkileşim testi, 37 QML derlemesi ve 122 native binding kontrolü
geçti. Native Wayland popup konumu yine hedef cihazda denenmelidir.

## 2.6.0 — Ortak shell sunumu

Shell renkleri, yazı aileleri, süs varlıkları ve hareket süreleri `Theme.qml`;
bar/panel/OSD/toast/Alt+Tab dış ölçüleri `SurfaceLayout.qml` üzerinden yönetilir.
Canlı shell ile önizleme aynı yüzey ölçülerini kullanır. Yedi panelin başlıkları
ve kapatma düğmeleri ortak bileşendedir; medya/arayüz eylemleri korunur.

Uzun bildirim butonları toast ve geçmişte aynı bileşenle sığdırılır. İpuçları
koyu paleti izler ve uzun metni sarar. Toast'lar artık önizlemede de gösterilebilir.
Bu iç düzenleme yeni bir tema seçici değildir; lock/SDDM/Dolphin/Spotify ayrı
adaptörlerdir. [Yüzey haritası ve sınırlar](docs/THEME_SURFACES.md).

9 yerleşim/etkileşim testi, mevcut ayar/launcher/Alt+Tab/OSD kontrolleri, network
import ve 35 QML derlemesi geçti. Hedef oturum kabulü ayrıca gerekir.

## 2.5.1 — Uzun içerik ve dar panel düzeltmeleri

Kalabalık tray saat ve kontrol düğmelerinin üzerine büyümez; yan oklarla bütün
simgelere erişilir. Simgenin sağ tık ve tekerlek eylemleri kendi uygulamasına gider.
Uzun tarih gerektiğinde kısaltılır; saat ortada kalır. Medyada uzun oynatıcı adları
panel genişliğine sığar, kalabalık liste kaydırılır. Güç menüsünde satırlar sıkışmaz;
klavye seçimi görünür tutulur. Uzun bildirim eylemleri de kart sınırına uyar.

7 gerçek Qt yerleşim testi ve mevcut ayar/OSD/ikon/import/derleme kontrolleri geçti.
Bu ilk M3 denetimidir; native oturum ve geniş yayın kapısı hâlâ açıktır.
[Doğrulama ve deneme adımları](docs/VALIDATION.md#m3-ilk-yerleşim-denetimi-251).

## 2.5.0 — Ortak ayarlar

Bardaki ses düğmesi → kontrol panelinin üstündeki **dişli** → Preferences.
Shell yazı ölçeği, hareketi azaltma, yüzey saydamlığı, floating bar, tarih/tray,
yan panellerin ortalanması ve OSD üst/alt konumu buradan değişir.
Terminal (Super+Q ve terminal isteyen uygulamalar) ile dosya yöneticisi (Super+E)
aynı kalıcı tercih kaynağını kullanır. Özel kullanıcı kısayolları korunur.

Tercihler tema dosyalarından ayrı saklanır ve güncelleme/rollback'te korunur.
Kaydetme hatası görünür; reset önce eski dosyayı saklar. Preview'de yapılanlar
bellekte kalır. [Ayarlar rehberi](docs/SETTINGS.md) aralıkları ve sınırları açıklar.

15 Python ve 10 gerçek Qt ayar testi, mevcut Alt+Tab/launcher/OSD/update kontrolleri,
30 QML bytecode ve 105 native binding karşılaştırması geçti. Gerçek QuickShell
restart kabulü hedef cihazda bekliyor. Terminal/Dolphin açılışı 17 Ekim kullanıcı
tarafından onaylandı; bu bildirim kalıcılık testinin yapıldığı anlamına gelmez.

## 2.4.0 — Launcher içinde hesaplama

Super+R'de doğrudan `(12+3)*4`, `1,5+2.25`, `200*10%` veya `2^3` yaz.
Sonuç ilk satırda görünür; eşleşen uygulamalar listede kalır. ↑/↓ ile seç,
Enter ile seçili sonucu kopyala veya uygulamayı aç. **Ctrl+Enter** doğrudan sonucu
kopyalar; Copy düğmesi de kullanılabilir. İfade ve menü açık kalır. Ctrl+C normal
metin kopyalamadır. Eksik/hatalı ifadeler satır içinde açıklanır.

`%` daima 100'e böler: `200+10% = 200.1`; yüzde oranını bulmak için `200*10% = 20`.
Ondalık nokta/virgül kabul edilir; sonuç noktalı ve en fazla 12 anlamlı basamaktır.
Birim dönüşümü henüz yoktur. Pano için ek paket gerekmez.

Node parser kontrolleri, 7 gerçek Qt etkileşim testi, network JS import ve mevcut
Alt+Tab/OSD/update regresyonları geçti. Native Wayland panosuna başka uygulamada
**yapıştırma burada denenmedi**. 17 Ekim kullanıcı normal kullanımın çalıştığını onayladı; PR #6 ana dala birleştirildi. [Doğrulama](docs/VALIDATION.md#pt-011-launcher-hesaplama-kontrolü) ·
[ADR-0007](docs/decisions/0007-launcher-calculator.md).

```bash
bash preview.sh
bash update.sh --check && bash update.sh
```

## 2.3.0 — Çalışma alanları arasında Alt+Tab

Alt+Tab ileri, Alt+Shift+Tab geri seçer. Alt bırakılınca seçili pencere açılır;
Enter da onaylar, Esc veya dışarı tıklama iptal eder. Listede bütün çalışma
alanlarının uygulama simgesi/adı, pencere başlığı, alan ve monitör bilgisi vardır.
MRU sırası seçim boyunca sabittir; yeni pencere sona eklenir, kapanan kaldırılır.

Seçici açıldığı ekranda kalır. Desteklenen toplevel yakalamasında seçili pencerenin
tek karesi gösterilir; yakalama yoksa uygulama bilgisiyle seçim devam eder.
Kapalıyken yakalama bileşeni kaldırılır. Mevcut özel Alt/Tab kısayolu bulunursa
güncelleme onu korur ve seçici bağlarını eklemediğini bildirir.

```bash
bash preview.sh
bash update.sh --check && bash update.sh
```

Preview örnek pencereler kullanır. 11 gerçek Qt durum/klavye/yerleşim testi,
6 kısayol geçiş testi, backend ve QML kaynak kontrolleri geçti. 17 Ekim kullanıcı normal Alt+Tab kullanımını onayladı; PR #5 ana dala birleştirildi.
Ekran çıkarma/yakalama ayrıntıları geniş M4 listesinde kalır.
[Doğrulama](docs/VALIDATION.md#pt-010-alttab-kontrolü) ·
[ADR-0006](docs/decisions/0006-window-switcher.md).

## 2.2.6 — Bildirim süresi ve güncellenen kartlar

QuickShell 0.3.1'in aktardığı bildirim süresi doğrudan milisaniye olarak kullanılır;
5000 ms artık 5000 saniyeye dönüşmez. `-1` varsayılan 4,5 saniye, `0` süresizdir.
Bir bildirimin başlık/metin/eylem değişiklikleri mevcut kartı günceller; okunmamış
sayısı tekrar artmaz. Önceki zamanlayıcılar yenilemede/kapanışta temizlenir.

Node davranış kontrolleri, gerçek Qt watcher sinyalleri (4 test), OSD hover/drag,
ikon merkezleri ve Dolphin aktif/pasif palet kontrastı geçti. 23 QML dosyası Qt
6.10.2 bytecode kontrolünden geçti. Bunlar native QuickShell/Steam/Dolphin kabulü
değildir; PR #4 sonrası normal Dolphin/OSD/Steam akışı kullanıcı tarafından onaylandı. Ayrıntı: [doğrulama](docs/VALIDATION.md).

## 2.2.5 — Spotify kurulumunu doğrulama

17 Ekim tanılamasında sistem Spotify paketi `1:1.3.4.258-2`, Spicetify CLI
`2.45.3-1`. Kullanıcı aynı gün Spotify'ın çalıştığını onayladı. Bu CLI'nin
belgelenmiş Linux aralığı `1.2.14–1.2.96` olsa da çalışan kurulumu engellemez;
yalnız uyarı verir. Sistem paket sürümü özel kopyanın sürümünü kanıtlamaz.

Kurucu artık stdout/stderr günlüğünü birlikte saklar ve CSS, palet, HTML
bağlantıları ile tema metadata'sını kontrol eder. Eksik çıktı önceki kopyaya
geri döner. Tanılama özel kopyanın kayıtlı sürümlerini ayrıca gösterir; eski
kurulumun sürümünü sistem paketinin sürümünden tahmin etmez.

Kontroller: `python3 checks/test_spotify_install.py` (10 test) ve
`python3 checks/test_app_installers.py` (uygulama/restore örnekleri).
Ayrıntı ve mevcut kurulumu geri alma: [uygulama eklentileri](apps/README.md).

## 2.2.4 — Eski shell profillerini tanıma

Eski HyprCADE yolu kullanıcı adına bağlı sabit bir dizin değildir. Mevcut HOME/XDG
profilinden veya ilk restore yedeğinin kaydettiği tam komuttan bulunur. İlgisiz
QuickShell profilleri ve IPC/list/kill/log istemcileri çalışan shell olarak seçilmez.
Restore, kaydedilmemiş bir eski shell komutunu tahmin ederek başlatmaz.

```bash
python3 checks/test_session_discovery.py
```

10 kontrollü keşif testi ve önceki 12 Dolphin/kurulum testi geçti; gerçek oturum
süreçlerine bu ortamda sinyal gönderilmedi. Dolphin düzeltmesi kullanıcı tarafından
onaylandı ve PR #1 ana dala birleştirildi.

## 2.2.3 — Dolphin başlatma tutarlılığı

Super+E artık launcher'ın kullandığı `org.kde.dolphin.desktop` girdisini açar;
Dolphin tema ayarı tek yerde kalır. Mevcut temalı girdi varsa eklentiyi yeniden
kurman gerekmez. Kullanıcıya özel farklı dosya yöneticisi/kısayol korunur.

Kurulu görünümü güncellemek için kaynak klasöründe:

```bash
bash update.sh --check && bash update.sh
```

Sonra Dolphin pencerelerini tamamen kapatıp Super+R ve Super+E ile kontrol et.
`gio` gerekir (Arch/CachyOS: `glib2` paketi). Yeni regresyon kontrolü:

```bash
python3 checks/test_file_manager.py
```

Bu komut kontrollü dosya/komut testidir; canlı Dolphin/Hyprland testi değildir.

## Mevcut kaynak

`payload/style/shell/`: bar, launcher, kontroller, medya, bildirimler, donanım ve OSD.
`payload/hypr/`: Hyprland Lua ayarları. `apps/`: bağımsız uygulama temaları.
`terminal-medallion/`: bağımsız CP437 terminal eki. `sddm/`: giriş ekranı. Kurulum, update, revizyon rollback ve restore scriptleri kökte.

Hedef: CachyOS/Arch, Hyprland **0.56.2 Lua**, QuickShell **0.3.1**, Hyprlock **0.9.6**.
Genel dağıtım/sürüm uyumu iddia edilmez. Native uygulamalar hazırlama ortamında
çalıştırılmadı; açık sorunlar STATUS'ta takip edilir.

Önizleme (gerekli paketler mevcutken, checkout kökünden):

```bash
bash preview.sh
```

Kurulum veya güncelleme için önce [kurulum belgesini](docs/INSTALLATION.md) oku.
Önizleme ile gerçek oturumu değiştiren kurucu aynı şey değildir.

## Çalışma ve varlıklar

Katkı düzeni [CONTRIBUTING.md](CONTRIBUTING.md); kararların gerekçesi
[ADR-0001](docs/decisions/0001-plague-tale-first.md); görsel/kod kökenleri
[varlık kaydında](docs/ASSETS_AND_LICENSES.md). Vitreus ve Caelestia bu görevde
kopyalanmadı veya kurulmadı. Yeni açık kaynak lisansı henüz seçilmedi.


## Deltarune ilk denemesi — 2.8.0

İkinci tema paketi hazır: [kullanım ve sınırlar](docs/DELTARUNE.md).
`bash preview.sh deltarune` kurmadan açar; canlı geçiş `theme.sh check/apply`
üzerinden yapılır. [Gerçek Qt önizlemesi](themes/deltarune/preview.png).
Görsel tema seçicinin yeri henüz kararlaştırılmadı.
