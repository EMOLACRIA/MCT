# Tema paket çekirdeği — 2.8.0

Paketler `plague-tale` ve ilk deneme `deltarune`. Görsel menü yoktur; önizleme PNG'si paket metadata'sında
hazırdır. Kullanıcı menünün konumunu daha sonra belirleyecek. [Deltarune deneme rehberi](DELTARUNE.md).

## Kullanım

Depo kökünde, normal masaüstü kullanıcısıyla:

```bash
bash theme.sh list
bash theme.sh status
bash theme.sh check plague-tale
bash theme.sh apply plague-tale
bash theme.sh rollback --check
bash theme.sh rollback
```

list/status Hyprland oturumu istemez. check/apply/rollback hedef Hyprland 0.56.2,
QuickShell >=0.3.1, çalışan MCT shell/notification sahipliği ve hyprpaper IPC ister.
İlk kurulum için eski install.sh/update.sh akışı geçerlidir; theme.sh kurucu değildir.

İlk apply mevcut Plague Tale'i kayıtlı paket haline getirir; görünümün değişmemesi
normaldir. Zaten aynı paket aktifse yeni snapshot/restart yapılmaz. apply yalnız
MCT shell'ini yeniden açar; başka QuickShell profili, Dunst, oturum veya sistem
servisini durdurmaz. Kullanıcı preferences, keybind, monitor/GPU/input ve bildirim
geçmişine yazmaz. İlk install/restore yedeği korunur.

## Paket ve sınır

`themes/plague-tale/manifest.json` şema 1, id/name/version, `mct-shell-2.8` ABI,
preview, zorunlu yüzey beyanları, dosya envanteri ve ayrı uygulama adaptörlerini
tanımlar. 38 görsel kaynak `files/` altında; preview gerçek mevcut Qt masaüstü
render'ının PNG'sidir. Kaynaklar git blob kimlikleriyle ve PNG yapısı/CRC ile
denetlenir. Bu bütünlük kontrolü bir imza veya lisans değildir.

İzinli hedefler: görsel QML view'ları, shell assets, wallpaper, Hyprland
appearance.lua, Kitty include dosyası ve lock medya fragment/görselleri.
Ortak UI state/Preferences/MRU/notification watcher, JS logic, native shell,
servisler, script ve kısayollar tema paketi hedefi olamaz. Bazı mevcut view'larda
klavye/fare bağlantıları da bulunur; bütün etkileşim henüz ayrı bir katmana
taşınmış değildir. Yeni tema aynı özellik sözleşmesi testlerinden geçmelidir.

Paket hook/exec/komut alanı kabul edilmez; fakat QML/Lua kaynak koddur. Bu model
güvenilir, incelenmiş repo paketleri içindir; indirilen kodu sandbox'a dönüştürmez.

SDDM, Dolphin ve Spotify ayrı kurucularıyla yönetilir. Apply sonucu bunları
yeniden kurmaz; active kaydı bunu `separate-installer` olarak gösterir.
Mevcut kurulumları ve adblock launcher ortamını değiştirmez. Yeni bir temanın
harici uygulama renk/asset uyarlamaları ayrıca hazırlanmalı; bu sürümün CLI'si
tek tıkla bütün uygulama adaptörlerini otomatik uygulamış sayılmaz.
Lock medya paketi, parola/auth yapılandırmasının yeniden yazılması değildir.
Terminal kapsamı mevcut Kitty include'udur; diğer terminal paletleri aynı
işlemde otomatik yeniden stillenmez.

## Kurulumsuz tema önizlemesi

```bash
bash preview.sh deltarune
```

`theme_preview.py` repo payload'ını ve doğrulanmış paket kaynaklarını geçici köke
birleştirir; DemoContext penceresi kapandığında temizler. Kurulu tema dosyası,
canlı shell, IPC, tercihler ve ilk yedek değişmez. Paket ABI 2.8 isteğe bağlı
PartyStrip view'ı ve native alt pencereyi içerir. Plague Tale'de kapalıdır.
Departure Mono fontu ve OFL metni yalnız belirli izinli asset yollarına taşınır.

## İşlem ve geri dönüş

1. Kurulum/ABI, aktif dosya sahipliği, paket ve görüntü doğrulanır. Aday görseller
   geçici tam shell köküne konur; validate.qml yalnız QML component'ini derler,
   native shell'i yaratmaz. Lua/config hatası reload aşamasında da denetlenir.
2. `~/.local/state/desktop-style/update.lock` updater ile paylaşılır. Snapshot ve
   pending journal kurulur; dosya içerikleri, modları, önceki active/last kaydı
   ve monitör başına wallpaper yolları saklanır.
3. Yalnız MCT durdurulur; dosyalar atomik değiştirilir; Hyprland reload,
   hyprpaper wallpaper ve shell IPC/notification hazır olma kontrolü yapılır.
4. Başarılıysa aktif kayıt ve işlem pointer'ı güncellenir. Hata dosyaları, kayıtları
   ve önceki wallpaper yollarını geri yükler. Kurtarma da başarısızsa journal
   silinmez, snapshot yolu bildirilir.

Hyprpaper fit modu mevcut config'ten okunur; sourced/karmaşık yapı adaptasyon
ister. Monitör çözünürlüğü/ölçeği/VRR ayarı değiştirilmez. Yeni görüntüler içerik
hash'li cache yolundan gösterilir; aynı dosya yolu cache'inin eski görüntüyü
tutması önlenir. Wallpaper IPC'si [resmî belgelerdeki wallpaper/listactive](https://wiki.hypr.land/Hypr-Ecosystem/hyprpaper/)
yolunu kullanır; bu turda gerçek 0.8.4 oturumu çalıştırılmadı.

Elektrik kesilmesi/kill ile yarım kalırsa:

```bash
bash theme.sh status
bash theme.sh recover
```

recover elle düzenlenmiş dosyayı ezmez. Commit tamamlanmış ve yalnız journal
temizliği kalmışsa işlemi tekrar uygulamaz. Snapshot başka bir ilk kurulum
yedeğine aitse geri yüklenmez; yeniden kurulum sonrası eski theme-core kayıtları
ayrıca arşivlenip uyarlanmalıdır. Bütün restore yedeklerini silmek çözüm değildir.

## Kaynak güncellemesi

Byte-identical aktif görsel dosyalarla update yapılabilir. Yeni kaynak aktif
temayı değiştirecekse updater ön kontrolde ve kilit içinde tekrar durur.
`bash theme.sh rollback` ile status'ta active null olana kadar önceki apply'lar
geri alınır; sonra update ve istenen tema için check/apply yapılır. Böylece eski
bir güncelleme aktif görünümü sessizce varsayılana sıfırlamaz.
Aktif skin'i otomatik yeni sürüme taşıma bu ilk çekirdeğin kapsamı değildir.

Theme rollback yalnız theme apply işlemini geri alır. `rollback-update.sh`
masaüstü kaynak revizyonunu, `restore.sh` ilk masaüstü kurulumunu geri alır;
birbirlerinin yerine kullanılmazlar. Görsel QML değişmişse hash koruması açık
adaptasyon ister; elle yapılan değişiklik üzerine yazılmaz.

## Doğrulama

17 Ekim 2026: [CI run 39054714755](https://github.com/EMOLACRIA/MCT/actions/runs/39054714755),
kod `6d3b6f2eb9472256b49049e30c72efdb63ecc2a2`: 28 çekirdek, 15 preferences ve
12 file-manager testi, Python/Bash syntax geçti. Tam geçici HOME/dizinler ve fake
runtime kullanıldı. Gerçek kullanıcı shell'i, PAM veya güç/servis işlemi yapılmadı.

```bash
python3 checks/test_theme_core.py
python3 checks/test_preferences.py
python3 checks/test_file_manager.py
```

Yeni çekirdeğin ilk native kabulü check → apply → status → rollback --check →
rollback akışıdır. Eski Plague Tale günlük kullanım onayı, bu yeni komutların
cihazda çalıştırıldığına dair bir test kaydı değildir.


18 Ekim sürüm kontrolü düzeltmesi: API kaynak referansı QuickShell 0.3.1'dir;
bu bilgi başka sürümün otomatik reddi değildir. Native gate güncelleyiciyle aynı
>=0.3.1 kuralını kullanır, stdout/stderr ve v önekini okur. Yeni sürümde aday QML
kontrolü yine geçmek zorundadır; genel sürüm uyumu garanti edilmiş sayılmaz.
