# Deltarune — 0.2.0 denemesi

Ortak kaynak 2.9.0, ABI mct-shell-2.9. Güncel komutlar ve güvenli geçiş sırası:
[2.9 yükseltme rehberi](UPGRADE_2_9.md).

![Qt launcher önizlemesi](../themes/deltarune/preview.png)

Siyah/camgöbeği çerçeveler, Departure Mono, karakter portreleri ve kullanıcının
2048×1151 wallpaper'ı korunur. Kontrol sağda, arama solda; merkez panel tercihi
öncelikli. Alt şerit yok. Super+R/M/T/B/Q/E/L, Alt+Tab ve hesaplama aynı kalır.
Panel/eylem mantığı artık iki görünümde tek ortak kaynaktır.

Kilit parola/saat/medya görünümü paketle değişir. Dolphin beyaz metin/ikonları,
Spotify CSS/paleti, SDDM giriş skin'i ve CP437 fountain terminal süsü ayrı
adaptörlerde hazır. Uygulama/terminal kurucuları --theme deltarune alır; SDDM
ayrı sudo adımıdır. Shell apply bu kurucuları otomatik çalıştırmaz.

Kurulumsuz bakmak: `bash preview.sh deltarune` ve
`bash sddm/preview.sh --theme deltarune`. Demo verileri/PAM'siz greeter fixture'ı
gerçek cihaz kabulü değildir. [Giriş render'ı](../previews/deltarune/login.png).

[Önceki denetim](DELTARUNE_AUDIT.md) tarihsel bulguları,
[ADR-0014](decisions/0014-shared-interaction-templates.md) uygulanan düzeltmeyi
kaydeder. Fotoğraflı seçicinin menü konumu hâlâ açık. Yeni native görsel kabulü beklenir.
