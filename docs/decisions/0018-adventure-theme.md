# ADR-0018 — Chapter 5 trailer / Adventure

Tarih: 20 Ekim 2026, Europe/Riga. Kullanıcı Snowgrave'in görünümünü beğendiğini
bildirip Chapter 5 trailer fotoğrafıyla devam edilmesini istedi. Snowgrave normal
görünüm/kullanım onaylandı; bütün donanım alt testlerinin ölçüldüğü iddia edilmez.

Dört-referans kararının dördüncü kurulu paketi `deltarune-adventure` 0.1.0 olur.
Mürdüm, mercan, sıcak beyaz ve altın; sonbahar dalları yerine basamaklı çatı
saçakları, bar köşeleri, klasör hatları ve özgün CP437 gün batımı çizimi kullanılır.
Başka temaların kaynakları ve ortak ABI değişmez. Yeni davranış eklenmez.

Kart katalogdan gelir; adaptör izinli paket listesine ve terminal vurgu tablosuna
kimlik eklenir. Var olan çoklu-tema geçiş, adaptör restore, picker bounds/klavye,
OSD ve QML kontrolleri dört paketi kapsar. Yeni temanın bütün ortak etkileşim
kontrolleri aynı staging/harness üstünde çalışır. Harici adaptörleri otomatik
kurmak bu işin kapsamı değildir. İlk yedekler ve kullanıcı tercihleri korunur.

2048×1152 kullanıcı kaynağı korunur; dağıtılan 3200×1800 PNG Lanczos'tur. Önceki
Snowgrave/hidden-tree sinir ağı restorasyonu bu görsele uygulanmış sayılmaz.
Hash ve yöntem paket metadata'sındadır. AI referansı ürün ekran görüntüsü değildir.
Native görünüm/kullanım kabulü yeni pakette beklenir. Guardian hâlâ planlıdır.
