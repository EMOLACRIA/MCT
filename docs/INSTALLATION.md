# Masaüstü görünümü — 2.2.2 QuickShell

2.2.2: Dolphin normal ve seçili metinleri saf beyaz, ikincil metinleri açık gri. Yalnızca `bash apps/install.sh dolphin` ile uygulanır.

2.2.1: Spotify başlangıç modülü yükleme düzeltmesi ve mevcut yerel adblock başlatıcılarını koruyan yönlendirme. Dolphin için başlangıç Qt paleti, açık dosya adları ve koyu tema ikonları. Bu revizyonu uygulamak için yalnızca `apps/README.md` adımlarını kullan; masaüstü `update.sh` gerekli değil. Dolphin için `qt6ct` ve `breeze-icons` gerekir.

2.2.0: OSD’nin IPC metodu `show` yerine `present` oldu. QuickShell 0.3.1 komut ayrıştırıcısındaki `ipc show` alt komutu, eski fonksiyon adını yakalayıp ses/parlaklık argümanlarını reddediyordu; aynı hata CLI11 ile yeniden üretildi, yeni çağrı geçti. Panel görünürlüğü artık kendi `screen` özelliğine bağlı değil, kökte hesaplanan ekran seçimini kullanır; görünürlük/ekran döngüsü kaldırıldı. `apps/` klasörüne Dolphin renk şeması/klasör ikonları ve Spotify Spicetify teması, ayrı kurulum/geri alma desteğiyle eklendi.

OSD düzeltmesi için normal güncelleme yeterli:

```bash
bash update.sh --check && bash update.sh
bash ~/.config/desktop-style/scripts/feedback.sh volume show
```

Dolphin ve Spotify eklentileri için `apps/README.md` dosyasını izle. Spicetify CLI ayrıca kurulmalıdır. Eklentiler açık uygulamaları kapatmanı ister; masaüstü güncellemesini engellemez.

2.1.0: Tepsi sağ tık menüleri için gerekli QApplication modu etkinleştirildi; ortak ikon düğmeleri yatay/dikey ortalandı. Pilin doluluk seviyesi, düşük pil ve şarj simgesi canlı duruma bağlı. Ses/parlaklık OSD'si sürüklenebilir; tutamaç üzerine gelince parlar, fare üzerindeyken kapanmaz. Dunst/notify-send geri dönüşü kaldırıldı. Super+T artık donanım panelini açıp kapatır. Hyprlock'a aynı seçili oynatıcıyı kullanan kapak, parça/sanatçı ve medya kontrolleri eklendi.

2.0.4: `Variants` üzerindeki yanlış `variants:` alanı, QuickShell 0.3.1'in `model:` alanıyla değiştirildi. Yerel kaynak karşılaştırması 65 native özellik/sinyal bağlantısını kontrol eder ve eski hatayı ayrıca yakalar. 21 QML dosyasının sözdizimi kontrolü de geçer. Gerçek QuickShell tip yüklemesini kendi oturumundaki `bash update.sh --check` doğrular; kaynak karşılaştırması canlı çalıştırma testi değildir.

2.0.3: Canlı shell'deki `anchors` grubundan sonraki fazla noktalı virgül ve LiveContext başlangıç nesnesinin eksik parantezleri düzeltildi. Qt'nin `qmlcachegen --only-bytecode` kontrolü canlı giriş dosyaları dahil 21 QML dosyasının tamamında çalıştırıldı. İki eski hata ayrıca bozuk örneklerle yeniden üretilerek bu kontrolün onları yakaladığı doğrulandı. Bu sürüm Wayland metin girişi odak uyarılarının giderildiğini iddia etmez; giriş yöntemi ayarları korunur.

2.0.2: Önizlemedeki duvar kâğıdı ve ortak köşe süsleri `shell/assets/` içine alındı. QuickShell'in kök klasör dışına çıkan göreli URL'leri engellemesi nedeniyle oluşan `qrc:/qs-blackhole` görsel uyarıları düzeltildi. Eski masaüstü bileşenlerinin kullandığı görseller de yerinde korunur.

2.0.1: QuickShell'in bileşen yükleyicisi için `ui/qmldir` listesi tamamlandı. Önizlemede görülen `Feedback is not a type` hatası düzeltildi.

Mevcut kömür, taş ve soluk pirinç renkleri; işlemeli köşeler ve kendi ekran görüntün korunur. Bar, uygulama menüsü, güç menüsü, kontrol paneli, bildirim merkezi, medya paneli ve ses/parlaklık göstergesi artık aynı QuickShell arayüzünde çalışır. Görünen arayüzde oyun veya tema adı yer almaz.

Gönderdiğin Hyprland 0.56.2 Lua ayarları ve QuickShell 0.3.1 temel alınmıştır. Pencere yerleşimi, monitör/ölçek/240 Hz, NVIDIA, VRR, giriş ayarları ve animasyon dosyaları bu güncellemede değiştirilmez. Terminaldeki CP437 madalyon ekine dokunulmaz. SDDM teması korunur. Hyprlock dosyasına yönetilen bir medya kaynağı eklenir; tıklanabilir kontroller için imleç görünür yapılır. Diğer kilit ekranı ayarların korunur.

## Önce önizle

Yeni ZIP'i ayrı bir klasöre çıkar ve `desktop-style` klasörüne gir:

```bash
bash preview.sh
```

Normal bir pencere açılır. Pencerenin kendi barındaki mercek, güç, ses, bildirim, donanım ve müzik düğmelerini dene. Önizleme aynı QML bileşenlerini örnek veriyle kullanır; dosya/config yazmaz, ses/parlaklık veya oturum işlemi uygulamaz. Açık mevcut masaüstünü değiştirmez. Örnek uygulama ve müzik verileri yalnızca bu pencerede gösterilir.

`previews/` klasöründe masaüstü, uygulama menüsü, güç menüsü, kontroller, bildirim merkezi medya, donanım paneli ve OSD’nin Qt ile alınmış PNG önizlemeleri de var.

## Mevcut görünümü güncelle — senin için bu adım

Önizlemeyi kapattıktan sonra aynı klasörde:

```bash
bash update.sh --check
bash update.sh
```

Normal kullanıcınla, açık Hyprland oturumunda çalıştır. Sudo kullanma. Önce restore çalıştırmana gerek yok. `--check` gerekli programları, mevcut config hatalarını ve QuickShell QML derlemesini dosyaları değiştirmeden kontrol eder. QML doğrulayıcısı canlı shell'i oluşturmaz; bar açmaz veya bildirim servisini devralmaz.

Güncelleme eski Waybar/Wofi/feedback süreçlerini ve Dunst'u durdurur, yeni shell'i başlatır. Kendi kullanıcı servislerinde `waybar.service` veya `dunst.service` etkinse çakışmayı önlemek için önceki etkinlik durumları yedeklenerek devre dışı bırakılır. Geri dönüşte bu durumlar geri yüklenir. Sistem genelindeki servislere işlem uygulanmaz.

QuickShell IPC yanıtı ve `org.freedesktop.Notifications` servisinin yeni shell'e ait olduğu doğrulanır. Başlatma, reload veya bu doğrulama başarısız olursa önceki görünüm ve kısayollar otomatik geri yüklenir. İlk kurulumun orijinal geri dönüş işareti korunur. Önceki Wofi dosyaları ve 30/30 gibi kişisel ofsetlerin saklanır; yeni R/M menüleri bu eski ofsetleri kullanmaz.

Güncelleme öncesindeki görünüm ve kısayollar `~/.local/state/desktop-style/revisions/` altında yedeklenir.

## Kullanım

| İşlem | Davranış |
|---|---|
| Super+R | Doğrudan bütün uygulamalarda arama. Aynı kısayola tekrar basınca kapanır. |
| Super+T / bardaki işlemci simgesi | İşlemci yükü/sıcaklığı, RAM, disk, GPU, sıcaklık ve fan sensörleri. Tekrar basınca kapanır. |
| Super+L | Hyprlock; sol altta kapak ve tıklanabilir medya kontrolleri. |
| Super+M | Arama çubuğu olmayan beş seçenekli güç/oturum menüsü. Tekrar basınca kapanır. |
| Super+B | Bildirim geçmişi, temizleme ve rahatsız etmeyin paneli. |
| Bardaki ses / ağ / pil | Kontrol paneli: ses, mikrofon, çıkış cihazı, parlaklık, pil ve ağ bağlantısı. |
| Bardaki nota | Medya paneli: kapak, parça/sanatçı, oynatıcı seçimi ve desteklenen kontroller. |
| Çalışma alanı numarası | İlgili alana geç. 1–10 numaraları sürekli görünür; dolu alanın altında nokta, aktif alanda çizgi vardır. |
| Esc / panel dışına tıkla | Açık paneli kapat. |
| Ses / mikrofon / parlaklık tuşları | Alt ortada sürüklenebilir OSD. Üzerindeyken açık kalır; ayrıldıktan 1,4 saniye sonra kapanır. Bildirim göndermez. |

R/M/T menüleri **odaklı ekranın merkezinde** açılır. Kontrol, bildirim ve medya panelleri odaklı ekranda üst sağda açılır. Bar her bağlı ekranda oluşturulur. Koordinatlar Qt/Wayland'ın ekran ölçülerinden hesaplanır; sabit fiziksel piksel ofseti kullanılmaz.

R/M ve diğer paneller tek ortak açık-panel durumunu kullanır. R'den M'ye geçince önceki panel kapanır, aynı menü iki kez oluşturulmaz. Aramada yukarı/aşağı ve Enter; güç menüsünde yukarı/aşağı, Enter ve Tab kullanılabilir. Oturumdan çıkış, yeniden başlatma ve kapatma ikinci bir onay ister. Diğer mevcut kısayollar korunur.

## Bildirimler, ses ve medya

Bildirimlerin son 100 kaydı `~/.local/state/desktop-style/notifications.json` içinde yerel olarak saklanır. DND ve okunmamış sayısı da korunur. Dosya atomik olarak yazılır; arşivden geri yüklenen bildirimlerde artık geçerli olmayan uygulama eylemleri gösterilmez. Geçici olarak işaretlenmiş bildirimler arşivlenmez. DND açıldığında yeni açılır bildirimler gösterilmez; arşive alınmaya devam eder.

İlk geçişte mevcut Dunst geçmişi erişilebiliyorsa yeni merkeze aktarılır. Var olan QuickShell geçmişinin üzerine yazılmaz. Yeni bildirimlerde uygulamanın sağladığı eylem düğmeleri yalnızca bildirim nesnesi hayattayken kullanılabilir.

Ses, mikrofon ve çıkış cihazları QuickShell'in PipeWire servisine bağlıdır. Parlaklık mevcut `brightnessctl` ile değiştirilir ve tekrar ölçülür. Ağ adı mevcut `nmcli` ile okunur; `nm-connection-editor` varsa Settings düğmesi onun penceresini açar. Yeni ağ profili kurucu tarafından oluşturulmaz.

MPRIS destekleyen aktif oynatıcıdan gerçek parça, sanatçı ve kapak alınır. Birden fazla oynatıcı arasında seçim yapılabilir. Desteklenmeyen önceki/sonraki/oynat-duraklat düğmeleri pasiftir. Oynatıcı yokken panel bunu gösterir.


## Donanım paneli ve kilit ekranında müzik

Super+T paneli açıkken yaklaşık iki saniyede bir `/proc` ve `/sys` verileri okunur. İşlemci sıcaklığı, fan veya GPU yükü donanım/sürücü tarafından sunulmuyorsa bilinmeyen değerler sıfır gibi gösterilmez. Uyuyan NVIDIA GPU uyandırılmaz; `nvidia-smi` yalnızca mevcut NVIDIA ekran kartlarının tamamı aktifken ve komut kuruluysa kullanılır. Panel kapanınca periyodik okuma durur. Ek sensör paketi kurulması zorunlu değildir.

Hyprlock medya bölümü `~/.config/desktop-style/hyprlock/media.conf` içindedir. Kontroller kilit ekranının kendi tıklanabilir widget'larıdır. Şifre alanı ve kilit davranışı Hyprlock'a aittir. QuickShell medya panelinde seçtiğin oynatıcı kontrol edilir. Bir parça başlatıp Super+L ile deneyebilirsin. Parça bilgileri yaklaşık bir saniyede, kapak iki saniyede yenilenir. Kapak yoksa madalyon gösterilir; web kapakları arka planda sınırlı boyutla indirilip yerel önbelleğe alınır. İnternet gerektirmeyen yerel kapaklar da desteklenir.

OSD ses ikonuna tıklayınca sessize alma/açma çalışır. Parlaklık sürgüsünün alt sınırı %1'dir. Ses/parlaklık kısayolları cihazı değiştirip ölçülen değeri gösterir. Shell çalışmıyorsa bir Dunst bildirimi üretmek yerine `feedback.log` içine hata yazar; `bash ~/.config/desktop-style/scripts/start.sh` ile yeniden başlatılabilir. Güvenli kilit oturumu üzerinde masaüstü OSD’si çizilmez; bu katman Hyprlock'un yerini almaz.

## Bu güncellemeyi geri al

Bir önceki masaüstü revizyonuna dönmek için:

```bash
bash rollback-update.sh --check
bash rollback-update.sh
```

Güncelleme sonrası shell dosyalarında yaptığın düzenlemeler geri dönüş öncesi ayrıca `before-rollback` klasörüne kopyalanır. Kısayol veya Hyprlock dosyanı sonradan değiştirdiysen otomatik geri dönüş üzerine yazmak yerine durur; yedek üzerinden uyarlamak gerekir.

Temayı tamamen kaldırıp ilk kurulumdan önceki masaüstüne dönmek için:

```bash
bash restore.sh
```

Bu komut terminal madalyon ekini veya ayrı kurulmuş SDDM temasını kaldırmaz. SDDM için `sudo bash sddm/restore.sh`; terminal eki için kendi paketindeki `restore.sh` kullanılır.

## İlk kurulum

Tema henüz kurulu değilse:

```bash
bash install.sh --check
bash install.sh
```

Kurucu, ilk gönderdiğin Lua dosyalarının hashlerini doğrular ve yerel yedek alır. Dosya/uygulama klasörü sembolik bağlantıları yerel kopyaya ayrılır; hedef dosyalarına yazılmaz. Config veya görünüm başlatma hatasında geri dönüş yapılır. Paket program indirmez veya sistem paketi kurmaz.

Gerekli komutlar: `hyprctl`, `kitty`, `hyprlock`, `hyprpaper`, `brightnessctl`, `wpctl`, `quickshell`, `notify-send`, `busctl` ve Python 3. QuickShell'de Hyprland, PipeWire, MPRIS, UPower, SystemTray ve Notifications modülleri bulunmalıdır; eksik modül QML kontrolünde yakalanır. Pil için UPower servisinin çalışıyor olması gerekir. Ağ bilgisi/ayarları için `nmcli` ve `nm-connection-editor` isteğe bağlıdır.

## SDDM

Mevcut Qt6 teması korunmuştur. Ayrı önizleme ve kurulum:

```bash
bash sddm/preview.sh
sudo bash sddm/install.sh --check
sudo bash sddm/install.sh
```

SDDM servisi yeniden başlatılmaz; açık oturum kapanmaz. Tema sonraki gerçek giriş ekranında görünür. Önizleme greeter'ın desteklediği test seçeneğini algılar.

## Düzenleme ve tanılama

Renkler ve fontlar: `~/.config/desktop-style/shell/ui/Theme.qml`. Bar: `ui/Bar.qml`. Her panelin kendi QML dosyası `ui/` klasöründe bulunur. Boyut ve açılma konumları `ui/Overlay.qml` içinde. QuickShell dosya değişikliklerini yeniden yükler; bu dosyaları düzenleyerek revize edebilirsin.

```bash
hyprctl configerrors
cat ~/.local/state/desktop-style/shell.log
cat ~/.local/state/desktop-style/feedback.log
bash ~/.config/desktop-style/scripts/start.sh
```

`start.sh` çalışan shell'i çoğaltmaz; IPC ve bildirim sahipliğini kontrol eder. Bildirim merkezinin eski Dunst'la aynı anda çalışması amaçlanmaz.

Göstergeyi elle dene:

```bash
bash ~/.config/desktop-style/scripts/feedback.sh volume show
bash ~/.config/desktop-style/scripts/feedback.sh brightness show
```

## Doğrulama sınırı

2.1.0: Ortak Qt bileşenlerinde yedi görünüm render edildi; ikonların gerçek merkez koordinatları, OSD üzerinde bekleme, canlı sürükleme ve kapanma gecikmesi test edildi. 22 QML kaynağı bytecode sözdizimi kontrolünden, 70 native özellik/sinyal bağlantısı QuickShell 0.3.1 kaynak karşılaştırmasından geçti. CPU/RAM/sensör hesapları, uyuyan NVIDIA kartını sorgulamama, medya metni kaçışlama/önbellek ve bildirim üretmeyen hata yolu kontrollü testlerle doğrulandı. Hyprlock medya alanlarının adları 0.9.6 kaynağıyla karşılaştırıldı. Gerçek Steam DBus menüsü ve Hyprlock kilit oturumu bu ortamda çalıştırılmadı.

Qt 6.10.2'de gerçek ortak QML bileşenleri render edildi. Altı görünüm, uygulama filtreleme, aynı paneli tekrar kapatma, panel değişimi, onaylı güç seçimi, Escape, gösterge ve küçük ekran boyut sınırları test edildi. Üretim JS koduyla bildirim arşivi/DND/geçici bildirim/eylem/geçersiz eski eylem temizliği, güncellenen bildirimin zamanlayıcı nesilleri, ses sınırlaması ve Lua dispatch doğrulandı. Kullanılan native servis API adları QuickShell 0.3.1 kaynaklarıyla karşılaştırıldı.

2.0.1 kontrolünde Qt'nin ağ URL'leri üzerinden dizin import davranışı da test edildi: eski eksik listeyle `Feedback is not a type` hatası üretildi; tam listeyle ortak önizleme sahnesi başarıyla yüklendi ve oluşturuldu. `qmldir` içindeki kayıtların bütün UI bileşenlerini kapsadığı kontrol edildi. Bu kontrol, QuickShell'in kendi çalıştırılmasının yerine geçmez.

2.0.2 kontrolünde Qt QUrl ile eski görsel yollarının QuickShell kök sınırını aştığı yeniden üretildi. Güncel beş yolun shell klasörü içinde kaldığı, gerçek dosyalara ulaştığı ve Qt Image nesnelerinin `Image.Ready` durumuna geçtiği doğrulandı. Ortak arayüzün altı görünümü yeniden render edildi. Wayland text-input odak uyarıları ayrı Qt/Wayland davranışıdır; bu ortamda canlı Wayland oturumu olmadığından doğrulanmadı.

2.0.3 hazırlığında `checks/test_shell_syntax.py`, yalnızca önizlemede kullanılmayan `shell.qml` ve `LiveContext.qml` dosyalarını da kapsayacak şekilde bütün QML kaynaklarını Qt bytecode derleyicisinden geçirir. Bu kontrol sözdizimini kapsar; QuickShell modüllerinin çalışma zamanındaki tip/API denetiminin yerine geçmez. Yerel hazırlama ortamında QuickShell çalıştırılmadı. Kullanıcının `update.sh --check` adımı gerçek QuickShell ile tip/API yüklemesini, kurulum adımı da servislerin hazır olmasını doğrular.

2.0.4 hazırlığında `checks/test_shell_api.py`, native QML nesnelerine verilen özellik ve sinyal işleyici adlarını QuickShell v0.3.1'in C++ bildirimleri, ilgili taban sınıfları ve FileView QML sarmalayıcısıyla karşılaştırır. Eski `Variants.variants` alanıyla negatif örnek başarısız olur; güncel kaynaklarda 65 bağlantı kabul edilir. Bu, servis davranışını, özellik tip dönüşümlerini veya JS içindeki bütün dinamik nesne erişimlerini doğrulamaz.

Kontrollü dosya/süreç testlerinde yeni kurulum ve tam restore, 1.4'ten geçiş, orijinal geri dönüş noktasının/özel kısayolların/Wofi ofsetlerinin/monitör ve NVIDIA ayarlarının korunması, başlatma hatasında geri dönüş ve revizyon geri dönüşü doğrulandı. Python ve Bash sözdizimleri kontrol edildi.

Bu ortamda gerçek Hyprland, QuickShell Wayland katman oturumu ve masaüstü DBus servisleri bulunmuyor. Canlı ekran/klavye odak davranışı, cihazlar ve gerçek oturum işlemleri burada uygulanmadı. Bu nedenle kurucu senin oturumunda önce QML derlemesini, sonra IPC ve bildirim servisi sahipliğini doğrular; başarısızlıkta önceki masaüstünü geri getirir.

## Teknik kaynaklar

- https://quickshell.org/docs/v0.3.1/types/Quickshell/PanelWindow/
- https://quickshell.org/docs/v0.3.1/types/Quickshell.Hyprland/Hyprland/
- https://quickshell.org/docs/v0.3.1/types/Quickshell/DesktopEntries/
- https://quickshell.org/docs/v0.3.1/types/Quickshell.Services.Pipewire/Pipewire/
- https://quickshell.org/docs/v0.3.1/types/Quickshell.Services.Mpris/MprisPlayer/
- https://quickshell.org/docs/v0.3.1/types/Quickshell.Services.Notifications/NotificationServer/
- https://quickshell.org/docs/v0.3.1/types/Quickshell.Io/FileView/
- https://github.com/quickshell-mirror/quickshell/tree/v0.3.1

- https://github.com/hyprwm/hyprlock/tree/v0.9.6
- https://wiki.hypr.land/Hypr-Ecosystem/hyprlock/
