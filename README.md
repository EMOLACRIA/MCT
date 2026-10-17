# MCT — Plague Tale geliştirmesi

HyprCADE'in daha bütünlüklü devamı için geliştirilen Hyprland/QuickShell masaüstü.
İlk görsel tema **A Plague Tale**; masaüstü yüzeylerinde oyun veya tema markası yok.
Önce bu tema tamamen bitirilecek; ardından aynı işlev/kısayollarla görsel açıdan
çok farklı temalar ve bir tema değiştirici gelecek.

**Durum:** 2.5.1 geliştirme sürümü. Alt+Tab, hesaplamalı launcher ve terminal/Dolphin açılışı onaylandı. Ayarların native kalıcılık kabulü bekliyor. Plague Tale henüz tamamlanmadı.
M3 ortak/görsel denetimi başladı; tema değiştirici M4 sonrasında.

## Projeyi okumaya buradan başla

| Dosya | Amacı |
|---|---|
| [PROJECT_BRIEF.txt](PROJECT_BRIEF.txt) | Kullanıcının amacı, sınırlar ve kesin kararlar |
| [AGENTS.md](AGENTS.md) | Kod asistanları için kısa çalışma talimatları |
| [ROADMAP.md](ROADMAP.md) | Plague Tale'den yeni temalara aşamalar ve çıkış koşulları |
| [STATUS.md](STATUS.md) | Kaynakta olanlar, açık sorunlar, doğrulama durumu |
| [Özellik sözleşmesi](docs/FEATURE_CONTRACT.md) | Her temada aynı kalan işlev ve alışkanlıklar |
| [Mimari](docs/ARCHITECTURE.md) | Mevcut yapı ile planlanan ayrım |
| [Yayın kontrolü](docs/RELEASE_CHECKLIST.md) | İlk tema ne zaman bitmiş sayılır? |
| [Vitreus / Caelestia](docs/INSPIRATION.md) | Referanslar, incelenen sürümler ve alınacak fikirler |
| [Doğrulama sınırları](docs/VALIDATION.md) | Gerçekten çalıştırılan ile hedef oturum kontrolü farkı |
| [Kurulum ve sürüm geçmişi](docs/INSTALLATION.md) | Mevcut paketin ayrıntılı kullanımı |
| [GitHub'a yükleme](docs/GITHUB_PUSH.md) | ZIP içeriğini kaynak repo olarak yükleme |
| [Uygulama eklentileri](apps/README.md) | Dolphin ve Spotify kurulumu / geri alma |

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
