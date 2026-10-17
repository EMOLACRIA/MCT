# Spotify ve Dolphin

Masaüstünün kömür, taş ve soluk pirinç paleti kullanılır. Arayüze tema veya oyun logosu eklenmez. Bu eklentiler `update.sh` tarafından kendiliğinden uygulanmaz.

## Dolphin

2.2.1, dosya adlarının siyah kalmasını önlemek için Qt paletini uygulama açılırken yükler. Bir kez gereken paketleri kur:

```bash
sudo pacman -S --needed qt6ct breeze-icons
```

`qt6ct-kde` zaten kuruluysa onun yerine normal `qt6ct` kurmana gerek yok. Dolphin pencerelerini kapat; ana `desktop-style` klasöründe:

```bash
bash apps/install.sh dolphin --check && bash apps/install.sh dolphin
```

Sonra **Super+R veya Super+E üzerinden aç** (Super+E düzeltmesi için 2.2.3 masaüstü güncellemesi uygulanmış olmalı). Dosya adları, menü/düğme yazıları ve seçili metinler saf beyazdır (`#ffffff`); ikincil metinler açık gridir. Seçimler koyu pirinç zemindedir. Aktif ve pasif pencereler aynı okunaklı paleti kullanır. Araç çubuğu ikonları Breeze Dark'tan gelir; klasör çizgileri güçlendirildi.

`org.kde.dolphin.desktop` girdisi yalnızca Dolphin için `QT_QPA_PLATFORMTHEME=qt6ct` ve `QT_STYLE_OVERRIDE=Fusion` kullanır. Oturumun genel ortam değişkenleri değiştirilmez. Terminalden doğrudan açmak için:

```bash
bash ~/.config/desktop-style/scripts/file-manager.sh
```

2.2.3 Super+E yardımcısı `.desktop` girdisini her açılışta yeniden bulur; eklentiyi geri alınca eski Qt ortamı kısayolda kalmaz. `gio` komutu Arch/CachyOS `glib2` paketindedir.

`dolphinrc` içindeki renk/ikon seçimi ile `qt6ct.conf` dosyasındaki Appearance grubunun ilgili beş anahtarı yedeklenir. Qt6ct kullanan başka uygulamalar da bu paleti okuyabilir; mevcut yazı tipi ve diğer ayarlar korunur. Qt6ct arayüzünü ayrıca açıp bir şey seçmene gerek yok.

Geri almak için Dolphin kapalıyken:

```bash
bash apps/restore.sh dolphin
```

## Spotify

Yerel Spotify paketi ve ayrı temalı kopya kullanılır. **17 Ekim güncel durum:**
`spotify 1:1.3.4.258-2`, `spicetify-cli 2.45.3-1`. CLI 2.45.3'ün resmî Linux
uyum aralığı **1.2.14–1.2.96**; bu birleşimde kurucu artık dosyaları değiştirmeden
durur. Spotify 1.3.4 teması şu anda doğrulanmış değildir. Yeni bir CLI sürümü
için Linux sürüm notları ayrıca kontrol edilmelidir; farklı CLI'ye geçmek tek
başına native UI kabulü sayılmaz. Kurucu paket sürümü düşürmez veya güncellemez.

Uyumlu bir Spotify/CLI birleşiminde önce Spicetify CLI kur:

```bash
paru -S --needed spicetify-cli
```

Paru yerine yay kullanıyorsan `yay -S --needed spicetify-cli` uygundur. Kurulum sırasında AUR paketinin sunduğu değişiklikleri gözden geçirebilirsin. Bu paket bir paket yöneticisi çalıştırmaz veya internetten betik indirip yürütmez.

Spotify'da en az bir kez oturum açılmış olmalı. Spotify'ı tamamen kapat, ardından:

```bash
bash apps/install.sh spotify --check && bash apps/install.sh spotify
```

Sonra **Super+R menüsünden kullandığın Spotify veya Spotify (adblock) girişini aç**. Kömür arka plan, pirinç düğmeler, ince çerçeveler ve köşe süsüyle masaüstü müzik çalarına uyumlu görünüm uygulanır. Tema yalnızca CSS/renklerden oluşur; eklenti veya tema JavaScript'i yüklemez.

Sistem paketinin dosyaları ve izinleri değiştirilmez. Spotify, `~/.local/share/desktop-style-apps/spotify/client` içine kopyalanır. Bu ek disk alanı kullanır; `--check` boyutu ve boş alanı kontrol eder. Spicetify ayarları/çalışma dosyaları da bu eklenti klasörü içinde tutulur. Mevcut Spotify hesabı ve ayarları kullanılmaya devam eder. Yerel Spotify başlatıcıları temalı kopyayı başlatır. `Exec=env LD_PRELOAD=… spotify …` biçimindeki mevcut adblock girdileri de bulunur; adblock kütüphanesi, komut seçenekleri ve masaüstü eylemleri korunarak yalnızca Spotify hedefi değiştirilir. Yeni adblock kurulmaz. Bu destek yerel `spotify-adblock` içindir; Flatpak ve özel kabuk betikleri otomatik dönüştürülmez, desteklenmeyen girdiler kurulumda `Skipped unsupported Spotify launcher` olarak belirtilir. Normal Spicetify kurulumundaki JavaScript uzantıları bu ayrı kopyaya aktarılmaz. Terminalden `/usr/bin/spotify` orijinal sürümü açar.

Spotify paketini güncellediğinde, uygulamayı kapatıp `bash apps/install.sh spotify` komutunu yeniden çalıştır. Böylece yeni paket kopyalanır ve tema tekrar uygulanır. Spicetify yeni Spotify sürümünü desteklemiyorsa uygulama aşaması hata verebilir; kurucu başarısızlıkta önceki temalı kopyayı korur. Bu ortamda senin Spotify sürümünde canlı görsel test yapılmadı.

2.2.5: bilinen CLI 2.45.3 uyumsuzluğu preflight'ta kontrol edilir. Diğer CLI
sürümleri destek tablosunda kayıtlı değilse uyarı gösterilir; desteklendiği
iddia edilmez. Başarılı CLI çıkışı sonrası CSS içeriği, bütün tema renkleri,
HTML stylesheet bağlantıları ve DesktopStyle/Ash metadata'sı doğrulanır.
Eksik/yanlış çıktı başarı sayılmaz, önceki kopya ve başlatıcılar geri gelir.
Günlük stdout ile stderr'i birlikte tutar. Yeni özel kopyanın paket/CLI sürümleri
`versions.json` içine yazılır. Eski kopyanın sürümü kayıt yoksa bilinmiyor sayılır.

2.2.1, CSS-only Spicetify uygulamasında `xpui-modules.js` dosyasının `xpui-snapshot.js` öncesinde yüklenmesini sağlar; eksik başlangıç dosyaları bulunduğunda önceki kuruluma döner. Bu, kaynak kodunda bulunan bir yükleme eksikliğini giderir; ekran görüntüsündeki boşluğun tek olası nedeni olduğunu iddia etmez.

Boş ekran devam ederse önce Spotify'ı tamamen kapatıp aynı adblock girişinden yeniden aç. Ardından şu çıktıyı paylaş:

```bash
bash apps/diagnose.sh
```

Tanılama sürümleri, başlatıcı komutlarını, uygulama günlüğünü, başlangıç dosya
boyutlarını, özel kopyanın kayıtlı sürümlerini ve tema çıktı kontrolünü gösterir;
Spotify hesap/tercih dosyasını okumaz. Tema dosyalarının geçerli olması native
UI'nin veya adblock'un çalıştığını doğrulamaz. Özel başlatıcı komutuna gizli
bilgi eklediysen paylaşmadan önce sil.

Geri almak için Spotify kapalıyken:

```bash
bash apps/restore.sh spotify
```

Bu işlem orijinal başlatıcıları geri getirir ve temalı kopyayı kaldırır. Spotify hesabını veya çalma listelerini silmez. Mevcut normal Spicetify kurulum ayarlarına dokunulmaz.
Sürüm uyumsuzluğu bu geri alma işlemini engellemez. Orijinal adblock girdisi
yedekteyse o da geri gelir; adblock'un yeni Spotify ile çalışma durumu ayrıdır.

## Yedek ve doğrulama

İlk uygulamadan önceki durum `~/.local/state/desktop-style-apps/backups/` altında saklanır. Tekrarlanan uygulama ilk yedeği değiştirmez. Masaüstü `restore.sh`/`rollback-update.sh` komutları bu ayrı uygulama eklentilerini kaldırmaz; yukarıdaki uygulamaya özel geri alma komutları kullanılır.

Kontrollü dosya testleri: tekrar uygulama, orijinal yedeğin korunması, Dolphin'in ilgisiz tercihlerinin korunması, Spotify paketinin değişmemesi, ayrı Spicetify ayar/çalışma klasörleri, başarısız uygulamada geri dönüş ve orijinal başlatıcının geri yüklenmesi. Dolphin 26.08.2 ve KDE ColorScheme/IconThemes kaynaklarıyla kullanılan ayar adları kontrol edildi. Gerçek Dolphin/Spotify uygulamaları bu hazırlama ortamında çalıştırılmadı; Spotify arayüz güncellemeleri bazı CSS seçicilerini etkileyebilir.

Kaynaklar:
- https://github.com/spicetify/cli/releases/tag/v2.45.3
- https://spicetify.app/docs/customization/themes
- https://spicetify.app/docs/getting-started
- https://spicetify.app/docs/cli/commands
- https://github.com/spicetify/cli/blob/main/src/utils/path-utils.go
- https://github.com/KDE/dolphin/tree/v26.08.2
- https://api.kde.org/kcolorschememanager.html

2.2.1 doğrulaması: eski yedek biçiminden geçiş; adblock ortamının ve başlatıcı seçeneklerinin korunması; başarısız kurulumda tüm başlatıcıların geri dönüşü; Node ile başlangıç modül sırası; gerçek Qt ile palet dosyası okuma ve QGraphicsWidget aktif/pasif metin renkleri. Normal metin rollerinde kontrast en az 4.5:1, devre dışı metinlerde en az 3:1 olarak kontrol edildi.
