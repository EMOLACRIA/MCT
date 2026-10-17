# MCT — Plague Tale geliştirmesi

HyprCADE'in daha bütünlüklü devamı için geliştirilen Hyprland/QuickShell masaüstü.
İlk görsel tema **A Plague Tale**; masaüstü yüzeylerinde oyun veya tema markası yok.
Önce bu tema tamamen bitirilecek; ardından aynı işlev/kısayollarla görsel açıdan
çok farklı temalar ve bir tema değiştirici gelecek.

**Durum:** 2.2.5 geliştirme sürümü. M0 tamamlandı; M1 sağlamlaştırma sürüyor. Plague Tale henüz tamamlanmadı.
Alt+Tab, launcher hesaplama ve ortak ayarlar ekranı planlandı; henüz uygulanmadı.

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
