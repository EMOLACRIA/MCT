# ADR-0017 — Üçüncü tema: Deltarune · Snowgrave

19 Ekim 2026, 23:13 Europe/Riga. Kullanıcı Guardian yerine Snowgrave ile önce
başlamayı seçti. Mevcut ağaç/Kris restorasyon görünümünü 23:11'de beğendiğini
bildirdi. Bu beyan yeni kalite/görünüm onayıdır; ayrı bütün native alt testlerin
ölçüldüğü veya 0.3.1 SHA'sının cihazda raporlandığı iddia edilmez.

- Yeni paket: `deltarune-snowgrave` 0.1.0, ABI mct-shell-2.9. Mevcut iki paket
  yeniden stillenmez; üçüncü tema seçicide ayrı karttır.
- Görsel kaynak, design/deltarune/snowgrave-source.jpg ve onaylanan
  snowgrave-reference.png. Koyu kahverengi, kırık beyaz, pas kırmızısı ve soluk
  altın; ince organik dal/yaprak çerçeveleri, ayrı terminal silüeti.
- Ortak surface/controller kaynakları ve kısayollar kopyalanmaz. Görsel wrapper'lar,
  layout/palet/font/ikon ve dış adaptörler ayrı pakettir. Alt şerit eklenmez.
- Önceki kabul edilen restorasyon yöntemiyle kaynak korunarak yüksek çözünürlüklü
  wallpaper hazırlanır. Kaynak/model/hash ve varsa son ölçekleme kayıtlıdır.
- Paket kaynakları manifest bütünüyle doğrulanır. Katalog rengi/font varlığı
  doğrulanmış Theme.qml ve envanterinden çıkarılır; bilinmeyen tema id'si için
  görsel davranış tahmini yapan yeni switch dalları gerekmez.
- Harici adaptör allowlist'ine üçüncü paket eklendi; özel kurucular, ilk yedek,
  adblock başlatıcısı ve geri dönüş akışı korunur. Otomatik uygulama/SDDM geçişi
  bu işin kapsamında değildir.
- Mevcut davranış suite'i iki Deltarune skin'ine parametreyle uygulanır; üçlü
  switch/noop/chained rollback, üç kart, üç skin OSD/SDDM ve adaptör roundtrip
  kontrolleri doğrulanır. Native yeni görünüm/kullanım kullanıcıda denenmelidir.

Sonraki iki görsel paket Guardian ve neşeli gün batımıdır. Sıraları bu işte
seçilmedi; uygulanmamış kart veya eksik paket seçiciye eklenmez.
