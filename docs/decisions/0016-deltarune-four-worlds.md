# ADR-0016 — Deltarune dört ayrı görsel tema

Tarih: 2026-10-19, 21:34 Europe/Riga. Durum: kullanıcı kararı kabul edildi;
ilk görsel paket uygulandı, yeni cihaz/görünüm kabulü bekleniyor.

Kullanıcı dört wallpaper için üretilen referansların tamamını ayrı tema olarak
istedi. Önce mevcut `deltarune` son üretilen ağaç/Kris referansına uyarlanacak;
kalan üç referans bundan sonra ayrı paketler olacak. Önceki mevcut Deltarune'un
camgöbeği fountain tasarımını sürdürme kararı bu taleple değişti.

| Referans | Görsel yön | Paket durumu |
|---|---|---|
| 4 — Kris/ağaç; kullanıcının Forgotten Man görüşme yeri açıklaması | Indigo, lavanta, ince fuşya dal kırıkları | `deltarune` 0.3.0, bu işin kapsamı |
| 1 — kullanıcının Chapter 4 Guardian savaşı açıklaması | Gece laciverti, lavanta, buz mavisi dört uçlu ışık | Ayrı tema kabul edildi; uygulama sırada |
| 2 — kullanıcının Chapter 5 trailer açıklaması | Mürdüm, mercan pembesi, kayısı sarısı; neşeli macera | Ayrı tema kabul edildi; uygulama sırada |
| 3 — kullanıcının Chapter 5 Snowgrave açıklaması | Koyu kahverengi, kırık beyaz, pas kırmızısı; sessiz sonbahar | Ayrı tema kabul edildi; uygulama sırada |

Sahne/rota adları kullanıcının verdiği bağlamdır; burada bağımsız oyun/lore
doğrulaması yapıldığı iddia edilmez. Yeni üç temanın ürün adları/kimlikleri henüz
seçilmedi. `design/deltarune/` etiketleri yalnız çalışma adlarıdır. Seçicide yarım
veya uygulanmamış paket gösterilmez.

Ortak davranış, servisler, kısayollar, tercihler ve ABI `mct-shell-2.9` korunur.
Tema farkı yalnız renkle sınırlanmaz: çerçeve, font, ikon, ölçü, yerleşim ve
hareket sunum katmanına aittir. Launcher solda, controls sağda; medya ve geçmiş
sağdadır. Kullanıcının `centerPanels` tercihi öncelikli kalır. Alt şerit yoktur.

0.3.0'daki görsel kapsam: wallpaper, tüm shell yüzeylerinin ortak tema token'ları,
dal çerçeveleri, kompakt launcher/medya, portre yerine sade başlık ikonları,
Hyprland border, Kitty, Hyprlock, ayrı Dolphin/Spotify/SDDM/CP437 adaptörleri.
Normal/seçili Dolphin yazıları beyaz kalır. Medya gerçek mevcut MPRIS kontrol
yeteneklerini kullanır; referanstaki dekoratif progress çizgisi var diye sahte
çalma süresi/seek işlevi çizilmez.

Wallpaper sağlanan 1200×675 JPEG'den piksel eşit PNG dönüşümüdür. AI ile yeniden
boyanmadı veya çözünürlüğü artırılmış gibi sunulmadı. Görsel referans PNG'leri AI
konseptidir; `themes/deltarune/preview.png` gerçek offscreen QML render'ıdır.
Kalan üç orijinal ve dört konsept depoda tasarım kaydı olarak korunur.

Harici uygulamaları tek seçimle otomatik kurmak bu kararın parçası değildir.
Mevcut bağımsız adaptör kurucuları/yedekleri korunur. İlk masaüstü restore noktası,
kişisel monitör/GPU/VRR/giriş ayarları veya Plague Tale paketi değiştirilmez.

23:13 ilerleme: kullanıcı üçüncü tema için Snowgrave seçti; paket uygulaması
[ADR-0017](0017-snowgrave-theme.md) ile kaydedildi. Guardian ve gün batımı sırada.
