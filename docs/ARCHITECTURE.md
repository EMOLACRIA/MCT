# Mimari: mevcut durum ve hedef

## Mevcut 2.2.2

`manage.py` ilk kurulum/restore; `update.py` revizyonlu güncelleme/rollback;
`payload/hypr/` Lua, hyprpaper ve hyprlock ayarları; `payload/style/scripts/`
oturum/süreç yönetimi; `shell/shell.qml` layer-shell pencereleri ve IPC;
`LiveContext.qml` native servisler; `DemoContext.qml` örnek veriler;
`ui/` paylaşılan görsel bileşenler. `apps/` ve `sddm/` ayrı kuruculardır.

`ui/Theme.qml` ortak renk/fontların bir kısmını içerir. Bileşenlerde sabit renkler
ve ölçüler de vardır. Dolayısıyla mevcut kod “tam tema motoru” değildir.
Dolphin'in desktop girdisi Qt ortamını ayarlarken Super+E düz `dolphin` çalıştırır;
başlatma davranışı henüz tek yerde tanımlanmamıştır.

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

## Yaşam döngüsü ve uyum

Tek QuickShell instance ve bildirim servisinin tek sahibi; IPC hazır kontrolü;
atomik durum yazımı; ilk restore yedeğini koruyan revizyonlar sürdürülür.
UI bir hesabı, cihazı veya bağımlılığı icat etmez; eksik yetenek gösterilir.
İlk hedefin sürümleri değişirse native API kaynakları tekrar kontrol edilir.

Vitreus'un güncel pleamar runtime'ına göç kararı yoktur. Caelestia'nın güncel
QuickShell-git ihtiyacı, bizim 0.3.1 paketimize doğrudan kod taşınabileceğini
kanıtlamaz. Mevcut runtime değişikliği ayrı gerekçeli teknik karardır.
