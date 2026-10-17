# ADR-0006 — Pencere seçimi ve Alt bırakma

Tarih: 2026-10-17. Durum: normal kullanım kullanıcı tarafından onaylandı.

## Karar

PT-010, ayrı `WindowSwitcherState` ve tema görünümüyle uygulanır. LiveContext
bütün Hyprland toplevel'larını uygulama/başlık/alan/monitör/adres modeline aktarır.
MRU, mevcut süreçte gözlenen odak geçmişini; ilk açılışta kalan pencereler için
`focusHistoryID` bilgisini kullanır. Seçim boyunca sıra dondurulur; başlıklar
canlı güncellenir, kapanan kaldırılır ve yeni pencere sona eklenir. Odak komutu
öncesi adres biçimi ve güncel listede bulunma kontrol edilir.

Shell üç GlobalShortcut kaydeder. Lua bağları ileri/geri ve sol/sağ Alt bırakmayı
iletir. Release bağı `ignore_mods` ve `non_consuming` kullanır; kilit ekranında
çalışacak bir seçenek eklenmez. Seçici Exclusive layer klavye odağı alır; normal
klavye tesliminde Alt-up/Enter onaylar, Esc iptal eder. Hızlı Alt bırakma için
global accept olayı da aynı idempotent commit'e gider. Açıldığı ekran sabittir;
ekran kaybı, dış pencere odağı veya başka panel açılması iptal eder.

Yakalama bağımsız, isteğe bağlı tek karedir (`ScreencopyView.live=false`). Native
`createContext()` kaynak/buffer hazır olunca ilk kareyi zaten alır; erken manual
captureFrame çağrısı yapılmaz. Kaynak değişince bağlam yeniden kurulur. Yakalama
yoksa sembol ve uygulama adı gösterilir. Loader seçici kapandığında kaldırılır.
Preview yalnız DemoContext pencereleriyle çalışır, global kısayol kaydetmez.

Update yalnız kendi tam eşleşen bloğunu tanır. Kullanıcının değiştirdiği blok
veya çakışan Alt/Tab bağı korunur. Kullanıcı sonradan çakışan bağ eklemişse bizim
değişmemiş blok kaldırılır. İlk restore yedeği ve revizyon rollback'i korunur.
Bu, genel bir Lua parser'ı değildir: başka dosyadaki/dinamik oluşturulan gizli
bağları keşfetmez. Böyle bir kurulumda bağlar kullanıcıyla uyarlanmalıdır.

## Sürüm kaynağı

QuickShell v0.3.1:

- [Hyprland IPC](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/wayland/hyprland/ipc/qml.hpp): activeToplevel, toplevels, refreshToplevels, usingLua, dispatch.
- [Toplevel](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/wayland/hyprland/ipc/hyprland_toplevel.hpp): address, title, workspace, monitor, lastIpcObject, wayland.
- [GlobalShortcut](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/wayland/hyprland/global_shortcuts/qml.hpp): appid/name, pressed/released.
- [ScreencopyView](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/wayland/screencopy/view.hpp) ve [uygulaması](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/wayland/screencopy/view.cpp): toplevel captureSource, hasContent/sourceSize, live, otomatik ilk kare.

Hyprland v0.56.2:

- [Lua dispatcher](https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/config/lua/bindings/LuaBindingsDispatchers.cpp): `hl.dsp.global(string)`, `hl.dsp.focus({window=...})`.
- [Lua bind](https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/config/lua/bindings/LuaBindingsToplevel.cpp): lone Alt_L/Alt_R, release, ignore_mods, non_consuming.

## Doğrulama ve sınır

17 Ekim: 11 gerçek Qt durum/klavye/yerleşim testi; 6 stdlib kısayol geçiş testi;
12 mevcut kurulum/update/restore testi; Node valid/stale adres dispatch testi;
25 QML bytecode ve 99 native binding kaynak kontrolü geçti. Qt render 1600×1000
incelendi; 500×400 sınırları test edildi. Overlay'deki ertelenmiş Loader callback'i
nesne yok olduktan sonra çalışabildiği için Loader'a bağlı Timer'a taşındı.

Bu ortamda Hyprland layer odağı/global release, çalışma alanı geçişi, monitör
çıkarma veya native yakalama denenmedi. Kaynak/API ve offscreen Qt doğrulaması,
hedef oturumun yerine geçmez. Canlı kabul listesi `../VALIDATION.md` içindedir.

17 Ekim kullanıcı “alt tab çok güzel çalışıyor” diyerek normal kullanımı onayladı.
PR #5 ana dala birleştirildi. Çoklu monitör çıkarma/yakalama ayrıntıları bu kısa
onaydan çıkarılmaz; M4 geniş kabul listesinde kalır.
