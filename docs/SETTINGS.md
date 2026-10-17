# Ortak ayarlar — 2.5.0

Bardaki ses düğmesi → kontrol panelinin üstündeki dişli → **Preferences**.
Esc kapatır. Panelde aşağı kaydırarak uygulama seçimi, tanılama ve reset'e ulaşılır.
Yeni global kısayol yoktur; gerekirse `python3 ~/.config/desktop-style/scripts/shellctl.py settings`.

| Tercih | Aralık / seçenek | Varsayılan |
|---|---|---|
| Shell text size | %90–120, %5 adım | %100 |
| Surface opacity | %75–100 | %96 |
| Reduce motion | Açık/kapalı; shell'in tanımlı geçişleri | Kapalı |
| Floating bar | Kenarlardan ayrılmış / kenara dayalı | Açık |
| Show date / system tray | Ayrı görünürlük tercihleri | İkisi açık |
| Center side panels | Controls, media ve notifications ortalanır | Kapalı |
| Volume and brightness position | Üst / alt | Alt |
| Terminal | Kurulu Kitty / Alacritty / Foot | Kitty |
| File manager | Kayıtlı FileManager desktop girdileri | Dolphin |

Yazı ölçeği shell içindir. Hyprlock, SDDM ve harici uygulamalar ayrı adaptörlerdir.
Saydamlık ana çerçeve yüzeyini değiştirir; metin soldurulmaz. Bar tercihi compositor'ın
ayırdığı alanı da değiştirir; monitör çözünürlüğü/ölçeği veya GPU ayarı değiştirilmez.

Terminal seçimi stok Super+Q ve launcher'ın terminal isteyen uygulamalarında ortaktır.
Dosya yöneticisi stok Super+E içindir; aynı kullanıcı/system desktop girdisi GIO ile
çalışır. Özel kişisel kısayol/komut varsa update onu korur. İsimle aradığın Kitty,
Dolphin vb. kendi girdisini açar. OS dosya ilişkilendirmeleri değiştirilmez.
Yeni seçilen terminalin kendi paleti/konfigürasyonu ayrıca kalır.

## Kayıt ve geri dönüş

Gerçek shell'de değişiklikler doğrulanıp otomatik kaydedilir. Kayıt hatasında aktif
eski değer kalır ve mesaj görünür. Preview yalnız bellektir; gerçek ayarlara yazmaz.

Dosya `$XDG_CONFIG_HOME/mct/preferences.json`; XDG_CONFIG_HOME boş/geçersizse
`~/.config/mct/preferences.json`. Tema payload'ı dışında olduğu için update,
revizyon rollback ve full restore dosyayı silmez. Eski shell sürümü tercihi
kullanmıyorsa dosya yine korunur.

Reset ikinci onay ister; varsa önceki dosya aynı klasörde
`preferences-before-reset-TARIH.json` olarak saklanır. Bu yalnız shell tercihlerini
sıfırlar; ilk masaüstü restore yedeğini, bildirimleri veya uygulama temalarını silmez.
Bozuk/gelecek sürümlü dosyaya otomatik yazılmaz. Terminal/dosya yöneticisi yardımcıları
bu durumda varsayılanlarını kullanır; ayarlar ekranı hatayı açıklar.

Elle düzenleme sonrası **Reload preferences** veya shell yeniden başlatma gerekir.
Ayar paneli açılırken de yeniden okunur. Aynı anda elle ve panelden düzenleme yapma;
panel son okuduğu tercihlerin tamamını kaydeder. Dosya sürümü 1'dir; eksik bilinen
alanlar varsayılanla tamamlanır, bilinmeyen alan/sürüm hata olarak korunur.

**Refresh diagnostics** yalnız tercih yolunu, seçilen uygulamaları, Hyprland ve
QuickShell sürüm çıktısını okur. Paket kurmaz, servis değiştirmez veya veri göndermez.

Doğrulama ve henüz yapılmamış native kontroller: [VALIDATION](VALIDATION.md#pt-012-ortak-ayarlar-kontrolü).
