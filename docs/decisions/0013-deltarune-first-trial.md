# ADR-0013 — Deltarune ilk denenebilir paket

Tarih: 2026-10-18 (Europe/Riga). Durum: uygulandı / hedef oturum kabulü bekliyor.

## Karar

Kullanıcı Plague Tale'i gün boyu kullanıp kapanışını onayladıktan sonra ikinci
oyun olarak Deltarune'u önerdi. İlk genel siyah/beyaz/kalp konseptini Undertale'e
fazla yakın buldu; dünya/teori araştırması istedi, kendi Deltarune.webp görselini
seçti ve bu görsele hazırlanan son referansın ardından geliştirmeyi başlattı.

Görsel temel: siyah/camgöbeği boşluk, piksel font ve kesik köşeler, üç kahramanın
menü portreleri ve parti düzeninden türetilen gerçek masaüstü durum şeridi.
Teori yorumları görsel atmosfer içindir; kesinleşmiş lore bilgisi ilan edilmez.

## Uygulama ve sınır

Paket aynı backend/state/IPC ve kısayolları tüketir. Native alt pencere ortak
shell'e, görünümü PartyStrip view'ına aittir. Plague Tale'de false/boş view ile
gizlenir. Yeni ortak sözleşme ABI'yi `mct-shell-2.8` yapar; önce ortak kaynak
update, sonra paket apply gerekir. Font ve OFL metni belirli asset yollarına
izinlidir. İlk paket görünümü/günlük kullanım onayı korunur.

Alt şerit 80 mantıksal piksel ayırır; bu pencere alanı tercihinin canlı sonucu
kullanıcı denemesine açıktır. Sensör verisi mevcut hardware.py'den iki saniyede
bir gelir; uyuyan GPU koruması değişmez. Sensör yokluğu/mute/şarj ayrı görünür.

Kurulumsuz preview repo payload ve paketi geçici kökte birleştirir; native
servis yerine DemoContext yaratır. Gerçek Qt render'ı metadata preview'sıdır.
Fotoğraflı seçici UI ve onun konumu bu işte seçilmedi. Dış uygulama/SDDM,
lock parola/saat ve terminal madalyonu adaptasyonları takip eden revizyonda.

## Doğrulama

[VALIDATION](../VALIDATION.md#280--deltarune-ilk-deneme): mevcut etkileşim
sözleşmesi staged Deltarune'da yeniden koşuldu; ek testler yeni şerit veri ve
panel bağlantısını, dosya testi tema özel font/portrelerin dönüşünü denetler.
Offscreen test native Wayland kabulü değildir. [Kullanım](../DELTARUNE.md).
