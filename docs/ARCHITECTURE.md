# Mimari: mevcut durum ve hedef

`payload/style/shell/behavior/` Launcher, Power, Feedback ve WindowSwitcher
controller'larını ayrıca sunar. Bunlar görsel geometri içermez; tamamen yeni
bir sunum bu controller'ları kullanabilir. `surfaces/` onların ortak varsayılan
çizimidir. Mevcut iki skin bu çizimi property/delegate ile özelleştirir.

## Mevcut 2.9.0

`payload/style/shell/surfaces/` 17 ortak etkileşim/sunum şablonu ve PanelSlot'u
barındırır. Paket `ui/` wrapper'ları yalnız görsel property/delegate seçer;
komut/input/onay tekrar etmez. Native servis/state/IPC önceki ortak yerde kalır.
Şablon varsayılan çizim de içerir; çok farklı tasarım için sunum delegate'i
verilir. Bu güvenilir QML kaynak modeli, sandbox değildir.

Hyprlock general/auth ana dosyadadır; tema layout ve media görsellerini taşır.
Dış adaptörler `adapter_assets.py` ile aynı kurucunun farklı kaynaklarını seçer.
SDDM tek login controller'ı ve ayrı LoginSkin'i kullanır. Tam sınırlar ve yaşam
döngüsü [ADR-0014](decisions/0014-shared-interaction-templates.md) içindedir.

## Önceki 2.7.0

Yeni CLI çekirdeği [THEME_PACKAGES](THEME_PACKAGES.md) ve
[ADR-0012](decisions/0012-theme-package-core.md) içindedir. Paket, görsel QML/varlık
ve izinli appearance/lock-medya/Kitty dosyalarını taşır; ortak state ve servisler
payload'da kalır. Mevcut bazı view dosyaları klavye/fare bağlantıları da içerir;
bütün etkileşim kodunun görsel bileşenlerden çıkarıldığı iddia edilmez. Gelecek
temalar özellik sözleşmesi testleriyle kabul edilir. Menü veya runtime göçü yoktur.

### Önceki 2.6.2 shell tabanı

`manage.py` ilk kurulum/restore; `update.py` revizyonlu güncelleme/rollback;
`payload/hypr/` Lua, hyprpaper ve hyprlock ayarları; `payload/style/scripts/`
oturum/süreç yönetimi; `shell/shell.qml` layer-shell pencereleri ve IPC;
`LiveContext.qml` native servisler; `DemoContext.qml` örnek veriler;
`ui/` paylaşılan görsel bileşenler. `apps/` ve `sddm/` ayrı kuruculardır.
2.6.2 SDDM form sınırı/klavye kaydırması ve lock medya cache doğrulaması ekler;
servis/tema arayüzü değişmez. [ADR-0011](decisions/0011-release-polish.md).

`ui/Theme.qml` shell QML renklerinin semantik kaynağıdır; font aileleri, font/motion
ölçekleme, köşe/wallpaper URL'leri de buradadır. `SurfaceLayout.qml` bar/panel/OSD/
toast/Alt+Tab dış ölçülerini, panel türü varsayılanlarını ve sınır hesabını paylaşır.
Canlı native pencere ile PreviewScene aynı değerleri tüketir. Çizim/iç düzen
ölçülerinin tamamı merkezileştirilmedi; harici adaptörler ayrı kaldı.
Dolayısıyla mevcut kod tam tema motoru değildir.

`PanelHeader` yedi panelin başlık/ek eylem/kapatma sunumudur. Eylemi parent'ın
closed sinyal bağlantısı yürütür; UiState kopyalanmaz. `NotificationActions`
toast ve geçmişin aynı backend eylemini kullanan genişliği sınırlı görünümüdür.
`ToastStack` canlı shell ile preview'de paylaşılır; preview DemoContext kullanır.
`SurfaceHint` palet/font ve metin sarması ortak olan ipucudur. Eylem/4500 ms
bildirim süresi gibi davranışlar tema token'larına taşınmaz.
2.6.1'de SurfaceHint 600 ms bekleme/iptal ve gösterim bileşeni seçimini yönetir; HintBubble
salt görünümdür. Native bar shell.qml'den HintPopup component'i alır; bu
QuickShell PopupWindow, anchor.item/rect ile düğmenin altına bağlanır. Boş Region
input maskesi ve grabFocus:false, pointer/focus engelini önler. Panel/preview
aynı bubble'ı etkileşimsiz Qt ToolTip ile gösterir; dar bar penceresine sıkıştırılmaz.
[Yüzey haritası](THEME_SURFACES.md) · [ADR-0010](decisions/0010-shared-shell-presentation.md).
Dolphin'in desktop girdisi Qt ortamını tanımlar. Super+E `scripts/file-manager.sh`
üzerinden kullanıcı/system XDG sırasında aynı girdiyi `gio launch` ile açar;
Exec satırını veya Qt ortamını ikinci kez üretmez. Girdi yoksa düz Dolphin'e döner;
mevcut girdi başarısız olursa temayı düşürerek ikinci kez uygulama açmaz.
Özel kullanıcı dosya yöneticisi/kısayolu update tarafından sahiplenilmez.
Ayrıntı: [ADR-0002](decisions/0002-dolphin-desktop-entry.md).

Spotify adaptörü sistem paketinin sürümünü ve CLI sürümünü preflight'ta okur;
CLI 2.45.3'ün belgelenmiş Linux aralığı dışında uyarı verir, uygulamayı engellemez.
Kullanıcının çalışan kurulum onayı belge aralığına göre geçersiz sayılmaz.
Başarılı süreç çıkışından
sonra CSS/palet/link/metadata denetlenir; eksik çıktı mevcut rollback yoluna gider.
Yeni özel kopyanın sürümleri kaydedilir. Salt okunur tanılama eski kopyanın
sürümünü uydurmaz. Ayrıntı: [ADR-0004](decisions/0004-spotify-output-validation.md).

`ui/WindowSwitcherState.qml` servislerden bağımsız MRU/seçim modelidir;
`ui/WindowSwitcher.qml` tema görünümü ve klavye/fare etkileşimidir. LiveContext
native pencere metadata'sı ve adres doğrulamalı odak komutunu sağlar. Shell,
GlobalShortcut kayıtları ve açıldığı ekrana bağlı özel layer yüzeyini kurar.
Preview aynı model/görünümü DemoContext ile kullanır, global kayıt oluşturmaz.
Tek kare yakalama bileşeni sadece seçici açıkken yaşar. Varsayılan kısayol bloğu
`switcher-bindings.lua` içinde; update özel bağları korur, ilk restore yedeğine
dokunmaz. [ADR-0006](decisions/0006-window-switcher.md).

`shell/logic/Calculator.js` görünüm/servis bağımsız, sınırlandırılmış recursive
descent aritmetik parser'ıdır. Launcher mevcut uygulama filtresine dokunmadan
hazır hesap sonucunu ilk satıra ekler. Eylem `backend.copyText` üzerinden gider;
LiveContext QuickShell 0.3.1'in Qt panosuna bağlı writable `clipboardText` alanını,
DemoContext yalnız test değeri kullanır. Yeni clipboard paketi/süreç veya global
kısayol eklenmez. [ADR-0007](decisions/0007-launcher-calculator.md).

`logic/Preferences.js` tek şema/default kaynağıdır. İşaretli strict JSON bloğunu
Python `scripts/preferences.py` da okur; JS ve Python doğrulayıcıları aynı kuralları
uygular. `PreferencesState` saf Qt durum/istek/cevap modeli; `PreferencesStore`
native Process adaptörü; `ui/Settings` görünümüdür. DemoContext ayrı bellek modeli
kullanır. Native değerler başarılı atomik kayıt cevabından sonra etkinleşir.

Tercihler `$XDG_CONFIG_HOME/mct/preferences.json` içindedir; varsayılan config kökü
`~/.config`. Dosya payload/snapshot dışında kalır. Terminal ve dosya yöneticisi
script'leri aynı dosyayı okur; stok Q/E bağları ortak yardımcıya yönelir. Theme
fontSize/duration/surface alpha'yı ve bar/panel konumunu bu modelden alır. Yeni
tema motoru veya global kısayol eklenmez. [ADR-0008](decisions/0008-user-preferences.md).

## Hedef ayrım

İlk M3 yerleşim düzenlemesi servis veya ayar şemasını değiştirmez. Tray viewport'u
görünümde yer kaplar; eylemler aynı backend'e ve native pencere koordinatına gider.
Medya/oturum kaydırması tema yüzeyinde kalır; komut/onay davranışı kopyalanmaz.
[ADR-0009](decisions/0009-responsive-surfaces.md).

1. **Ortak servisler/eylemler:** pencere, workspace, ses, medya, bildirim, cihaz,
   başlatma, oturum; görünümden bağımsız tek davranış.
2. **Ortak etkileşim:** panel aç/kapat durumu, klavye gezinme, MRU seçimi,
   calculator sonuç modeli, settings doğrulama/kalıcılık.
3. **Tema sunumu:** fontlar, malzeme, şekiller, süsler, yerleşim ve hareket;
   ortak veri/eylem arayüzünü tüketir. Sadece renk token'larıyla sınırlı değildir.
4. **Kullanıcı tercihi:** tema paketinden bağımsız, sürümlenebilir ayarlar.
5. **Uygulama adaptörleri:** Hyprland, terminal, Dolphin/Qt, Spotify, lock ve
   SDDM için üretilen dosyalar; her adaptörün apply/reload/restart/restore sınırı.

Bu ayrım planlanan sözleşmedir; bu belgede hayali klasörler mevcutmuş gibi
listelenmez. Somut dosya şeması refactor uygulanırken karar kaydıyla seçilir.

## Süreç seçimi

`scripts/session.py` yalnızca gerçek `qs`/`quickshell` başlatmalarındaki tek
`-p/--path` veya `-c/--config` seçicisini tanır. Dosya yolları normalize edilir;
IPC/list/log/kill/msg ve yardım/sürüm komutları shell değildir.

Eski HyprCADE için mevcut kullanıcı HOME/XDG dizininde gerçekten `shell.qml`
içeren standart profil veya orijinal restore manifest'inde kayıtlı tam seçici
kullanılır. Adı benziyor diye başka bir QuickShell profili seçilmez. Kurulumun
süreç yedeği aynı seçimi kullanır; restore yalnızca kayıtlı komutları geri açar.
Eski manifest'te süreç listesi hiç yoksa shell yolu uydurulmaz.
Ayrıntı ve otomatik keşfin sınırı: [ADR-0003](decisions/0003-shell-process-selection.md).

## Yaşam döngüsü ve uyum

Bildirim başına `NotificationWatcher` property değişimlerini tek event döngüsünde
birleştirir. Aynı native nesne için yeni kart, unread artışı veya ikinci closed
handler'ı oluşturulmaz. Süre ve toast timer'ları yenilemede/kapanışta iptal edilir;
generation kontrolü eski callback'lerin yeni durumu kapatmasını önler. Süre
QuickShell 0.3.1'in gerçek aktarımına göre milisaniyedir.
[ADR-0005](decisions/0005-notification-lifecycle.md) kaynak kanıtını ve sınırını kaydeder.

Tek QuickShell instance ve bildirim servisinin tek sahibi; IPC hazır kontrolü;
atomik durum yazımı; ilk restore yedeğini koruyan revizyonlar sürdürülür.
UI bir hesabı, cihazı veya bağımlılığı icat etmez; eksik yetenek gösterilir.
İlk hedefin sürümleri değişirse native API kaynakları tekrar kontrol edilir.

Vitreus'un güncel pleamar runtime'ına göç kararı yoktur. Caelestia'nın güncel
QuickShell-git ihtiyacı, bizim 0.3.1 paketimize doğrudan kod taşınabileceğini
kanıtlamaz. Mevcut runtime değişikliği ayrı gerekçeli teknik karardır.

## 2.8 opsiyonel sunum yüzeyi

Ortak shell/preview her iki pakette aynı `PartyStrip` arayüzünü yaratır.
`Theme.partyStripEnabled` ilk Deltarune denemesinde true idi; 18 Ekim kullanıcı
revizyonunda iki pakette de false/boş view. Native alt pencere oluşmaz. Native pencere
ve sensör izleme yetkisi ortak shell'e aittir; paket yalnız verileri çizer ve
mevcut uiState.toggle eylemlerine bağlanır. Bu yeni view/default sözleşmesi ABI'yi
mct-shell-2.8 yapar. [ADR-0013](decisions/0013-deltarune-first-trial.md).
