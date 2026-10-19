# ADR-0016 — Tek seçimli Wayland tema çizgisi / koşullu Super+G

19 Ekim 2026 01:07 Europe/Riga. Kullanıcı önceki ayrı uygulama, grid ve
check→apply akışını rahat/stilize bulmadı. Orta çizgi, hover genişleme/fotoğraf,
tek seçimle arka plan kontrolleri ve boşsa Super+G istedi. Bu talep önceki açık
konum kararını ve ADR-0015'in sunumunu değiştirir; engine sözleşmesini değiştirmez.

PickerState/Qt sunum ve Python Engine köprüsü korunur. FloatingWindow kaldırıldı;
PanelWindow overlay odaklı ekranda exclusive keyboard ile açılır. Temalar yatay
spine üzerinde genişler, Plague Tale serif/pirinç ve Deltarune pixel/cyan sunumu
ayrıdır. Paket fotoğrafları mevcut gerçek Qt render'larıdır. Yeni dış sanat veya
ikon alınmadı. Font kaynağı existing OFL Departure Mono'dur. Kullanıcı fontScale/
reduceMotion okunur; yazılmaz. Hover apply değildir, click/Enter aynı apply olur.

Overlay sıcak kalır, themes.toggle IPC ile yeniden pencere yaratmadan toggle
edilir. Başarılı işlem 650 ms sonra gizlenir. Gizlemek worker'ı durdurmaz. Ana
shell restart'ında işlem worker'ının öldürülmemesi için ayrı QuickShell process
ömrü korunur; kullanıcıya normal uygulama penceresi/taskbar girdisi açılmaz.
Açılış önce mevcut desktop panelini IPC ile kapatır. Kaynak/ABI güncellemesi yoktur.

Engine.apply zaten prepare/preflight/aday compile ve kilit tekrar kontrolünü
yapar. Önceki ayrı UI check turu kalktı; korumalar veya hata geri dönüşü kalkmadı.
Geçersiz/pending/verisi okunamayan seçim pasiftir; başarısız apply gerçek aktif
kaydı yeniler. External uygulama/SDDM kurucuları bu taleple yeniden tasarlanmadı.

`theme_bindings.py` canlı Hyprland JSON'unu sorgular. Super+G doluysa veya Super
keycode binding'inde klavye yerleşimi yüzünden boşluk kanıtlanamıyorsa durur.
Bilinmeyen/bozuk veri boş kabul edilmez. Sahipli Lua bloğu haricindeki metin
korunur; orijinal uygulama restore point'i değişmez, ayrı binding yedeği tutulur.
Ortak update.lock altında tekrar check, QML compile, atomik replace, reload ve
tek canlı bağ doğrulaması vardır. Hata mevcut keybind/pointer'a döner. unbind
yalnız değişmemiş sahipli bloğu kaldırır, sonradan eklenen başka bağları bırakır.

Hyprland 0.56.2 JSON alanlarının birincil kaynağı:
[bindsRequest](https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/debug/HyprCtl.cpp).
QuickShell 0.3.1 PanelWindow/WlrLayershell/IpcHandler/Process kaynak kontratları
kontrol edilir. Bunlar hedef native oturum testinin yerine geçmez.

Lua sahiplik doğrulaması özellikle [hlBind kaynağına](https://github.com/hyprwm/Hyprland/blob/v0.56.2/src/config/lua/bindings/LuaBindingsToplevel.cpp)
bağlıdır: dispatcher `__lua`, arg değişebilen Lua registry ref'idir. `exec` ve
komut arg'ı beklenmez. Sahipli kaynak bloğu + özel description + tek canlı G bağı
birlikte doğrulanır; keycode veya başka description/duplicate korunur. Test
fixture'ı da gerçek biçimi ve reload sonrasında ref değişimini kullanır.
