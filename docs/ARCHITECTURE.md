# Mimari: mevcut durum ve hedef

## Mevcut 2.2.5

`manage.py` ilk kurulum/restore; `update.py` revizyonlu güncelleme/rollback;
`payload/hypr/` Lua, hyprpaper ve hyprlock ayarları; `payload/style/scripts/`
oturum/süreç yönetimi; `shell/shell.qml` layer-shell pencereleri ve IPC;
`LiveContext.qml` native servisler; `DemoContext.qml` örnek veriler;
`ui/` paylaşılan görsel bileşenler. `apps/` ve `sddm/` ayrı kuruculardır.

`ui/Theme.qml` ortak renk/fontların bir kısmını içerir. Bileşenlerde sabit renkler
ve ölçüler de vardır. Dolayısıyla mevcut kod “tam tema motoru” değildir.
Dolphin'in desktop girdisi Qt ortamını tanımlar. Super+E `scripts/file-manager.sh`
üzerinden kullanıcı/system XDG sırasında aynı girdiyi `gio launch` ile açar;
Exec satırını veya Qt ortamını ikinci kez üretmez. Girdi yoksa düz Dolphin'e döner;
mevcut girdi başarısız olursa temayı düşürerek ikinci kez uygulama açmaz.
Özel kullanıcı dosya yöneticisi/kısayolu update tarafından sahiplenilmez.
Ayrıntı: [ADR-0002](decisions/0002-dolphin-desktop-entry.md).

Spotify adaptörü sistem paketinin sürümünü ve CLI sürümünü preflight'ta okur;
bilinen CLI 2.45.3 Linux sınırı dışında uygulama yapmaz. Başarılı süreç çıkışından
sonra CSS/palet/link/metadata denetlenir; eksik çıktı mevcut rollback yoluna gider.
Yeni özel kopyanın sürümleri kaydedilir. Salt okunur tanılama eski kopyanın
sürümünü uydurmaz. Ayrıntı: [ADR-0004](decisions/0004-spotify-output-validation.md).

## Hedef ayrım

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

Tek QuickShell instance ve bildirim servisinin tek sahibi; IPC hazır kontrolü;
atomik durum yazımı; ilk restore yedeğini koruyan revizyonlar sürdürülür.
UI bir hesabı, cihazı veya bağımlılığı icat etmez; eksik yetenek gösterilir.
İlk hedefin sürümleri değişirse native API kaynakları tekrar kontrol edilir.

Vitreus'un güncel pleamar runtime'ına göç kararı yoktur. Caelestia'nın güncel
QuickShell-git ihtiyacı, bizim 0.3.1 paketimize doğrudan kod taşınabileceğini
kanıtlamaz. Mevcut runtime değişikliği ayrı gerekçeli teknik karardır.
