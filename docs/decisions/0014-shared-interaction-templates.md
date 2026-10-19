# ADR-0014 — Ortak etkileşim şablonları ve Deltarune adaptörleri

18 Ekim 2026 · 2.9.0 uygulandı / native kabul bekliyor.

Kullanıcı eksik denetiminden sonra açık bulguların kapatılmasını başlattı.
Denetimdeki 12 tekrarın 9'unda Loader/Launcher context uyarısı vardı. İlk düzeltme
denemelerinde yalnız deferred activation veya asynchronous Loader yeterli olmadı;
bunlar nihai yapıya alınmadı.

`payload/style/shell/behavior/` Launcher, Power, Feedback ve WindowSwitcher
controller'larını ayrıca sunar. Bunlar görsel geometri içermez; tamamen yeni
bir sunum bu controller'ları kullanabilir. `surfaces/` onların ortak varsayılan
çizimidir. Mevcut iki skin bu çizimi property/delegate ile özelleştirir.

## Ortak shell

`shell/surfaces/` 17 işlevli QML şablonunu taşır. Bar/tray eylemleri, launcher
filtre/hesap/kopyalama, güç onayı/klavye, OSD throttle/commit, medya kontrolleri,
ayar bağlantıları, bildirim eylemleri ve Alt+Tab etkileşimi burada tek kaynaktır.
İki paketin `ui/` dosyaları şablonları miras alır; font/çerçeve/ikon/layout ve
gerekli görsel property/delegate değişikliklerini sağlar. Deltarune'un yatay medya
metadata delegate'i salt veri okur; oynatıcı eylemlerini kopyalamaz. Yeni tema
sadece renklerle sınırlı değildir. Bu, güvenilmeyen QML'yi sandbox yapmaz.

Şablonlar ortak varsayılan çizim de içerir. Tamamen yeni bir görsel yerleşim
gerektiğinde ilgili şablona sunum delegate'i eklenir; olay/komut kodu yeni tema
view'ına kopyalanmaz. Her iki pakette davranış kopyalanmasını kontrol eden kaynak
testi ve aynı gerçek Qt etkileşim sözleşmesi vardır. Ortak kaynak güncellemesi
böylece iki görünümün de davranışını değiştirir.

`PanelSlot` her paneli ilk açılışta yaratıp shell ömrü boyunca yeniden kullanır.
Kapanışta yalnız görünüm/focus timer kapanır; geçiş sırasında kurulmakta olan
context yok edilmez. Panel başına bir instance vardır. İlk kez açılmayan panel
yaratılmaz. UiState close hâlâ search/confirmation'ı temizler; Settings activate
reset onayını temizler. Görünmeyen ComboBox popup'ı kapanır. Donanım polling'i
aynı ortak activePanel koşuluna bağlıdır; cache sürekli sensör izlemez.

Bu yeni ortak dizin tema sahipliği dışında ve ABI `mct-shell-2.9` içindedir.
Eski aktif tema eski kaynakla geri alınır, sonra source update ve yeniden apply
yapılır. İlk restore noktası korunur. Kaynak dizininin Python cache dosyaları
ABI karşılaştırmasına dahil edilmez.

## Lock ve dış adaptörler

Hyprlock general/auth akışı ana dosyada kalır. Kaynaklanan `layout.conf`
arka plan/saat/parola alanı sunumunu taşır; `media.conf` önceki medya arayüzüdür.
Paket artık layout'u da snapshot/check/apply/rollback kapsamına alır. Update
yalnız birebir bilinen eski stok görünümü source yapısına geçirir. Özel config
korunur; tam tema check eksik layout source'u açıkça bildirir.

`adapter_assets.py` gözden geçirilmiş iki temanın kaynaklarını seçer. Dolphin ve
Spotify aynı transaction/restore ve ortak başlatıcı kodunu kullanır. Spotify özel
client ve adblock ortamını korur; CSS/palet çıktısı seçilen kaynakla denetlenir.
Terminal aynı CP437/UTF-8 kurucuya ve ilk yedeğe yeni fountain çizimini verir.
SDDM aynı `Main.qml` login controller'ına `LoginSkin.qml`, font ve görseller
giydirir. SDDM seçimi sudo altında açık `--theme` ile yapılır.

Bu adaptörler shell apply ile otomatik yeniden kurulmaz. Uygulama kapatma,
SDDM sistem dosyası izni ve restart sınırları ayrı ve görünür kalır. Fotoğraflı
tema menüsünün yeri veya yeni kısayolu bu kararla seçilmedi.

Doğrulama ve yükseltme: [VALIDATION](../VALIDATION.md),
[2.9 rehberi](../UPGRADE_2_9.md). Native Wayland/PAM/gerçek uygulama kabulü açık.

### 18 Ekim — Dolphin kaynak düzeltmesi

Kullanıcı fotoğrafında palet uygulanmış fakat klasörler pirinç rengindeydi.
Deltarune ikonlarının eski SVG'lerle birebir aynı olduğu bulundu; ayrı basamaklı
cyan sunum ve kalan header/complementary zeminleri düzeltildi. Adaptör/restore
mimarisi değişmedi; aynı kurucu yeniden uygulanır. Yeni cihaz görünümü beklenir.
