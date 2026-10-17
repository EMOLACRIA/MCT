# ADR-0007 — Launcher aritmetiği ve sonuç kopyalama

Tarih: 2026-10-17. Durum: normal kullanım kullanıcı tarafından onaylandı.

## Karar

`logic/Calculator.js` yalnız sayılar ve aritmetik için tokenizer + recursive
descent parser sağlar; tema/uygulama/servis erişimi içermez. Eval, Function,
shell komutu veya harici matematik süreci kullanılmaz. 512 karakter, 256 token,
32 iç içe ifade sınırı gereksiz parser işini sınırlar. Birim dönüşümü ayrı iştir.

Öncelik: postfix `%`, üs `^` (sağ birleşim), unary işaret, çarpma/bölme,
toplama/çıkarma. Unary, üs sağında da kullanılabilir: `-2^2=-4`, `2^-2=0.25`.
Yüzde her zaman `/100`: bağlamsal indirim veya modulo yoktur. Görünür kartta
bu anlam belirtilir. Ondalık `.`/`,` ve bilimsel gösterim desteklenir; binlik
ayırma ve örtük çarpma yoktur. IEEE-754 double aritmetiği kullanılır; sonuç 12
anlamlı basamakla biçimlenir ve aynı metin kopyalanır. Sonsuz/NaN reddedilir.
Bu, keyfi hassasiyetli/finansal bir hesaplayıcı iddiası değildir.

Otomatik tanıma aritmetik karakter kümesini ve sayı/işaret/parantezle başlayan
girdiyi kabul eder. `1password` gibi adlar normal aramada kalır. `=` açık hesap
niyetidir; yanlış ifade satır içi hata üretir. Eksik ifade ayrı durumdur. Hata
ve eksik durumda önceki hazır sonuç erişilebilir kalmaz.

Launcher mevcut uygulama filtresini korur; hazır sonuç ilk satıra eklenir.
↑/↓ bütün listeyi dolaşır; Enter seçili satırı açar/kopyalar. Ctrl+Enter seçimden
bağımsız sonucu kopyalar; Ctrl+C TextField'ın normal davranışıdır. Kopyalama
menüyü/ifadeyi korur; yeni girdide kopyalama bildirimi sıfırlanır. Karttaki Copy
fare ve Tab gezinmesiyle erişilebilirdir; yeni global kısayol eklenmez.

## Pano adaptörü ve sürüm kanıtı

QuickShell v0.3.1 [qmlglobal.hpp](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/core/qmlglobal.hpp)
writable `clipboardText` alanını bildirir.
[qmlglobal.cpp](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/core/qmlglobal.cpp)
setter'ı Qt clipboard `setText` çağrısına yönlendirir. LiveContext `copyText` bu
alanı kullanır. Odaklı launcher bir Qt Wayland yüzeyidir; native pano teslimi
hedef oturumda test edilir. Yeni wl-copy bağımlılığı veya subprocess yoktur.
DemoContext sadece test değerini kaydeder; preview sistem panosunu değiştirmez.

## Doğrulama ve sınır

17 Ekim: Node aritmetik/öncelik/bozuk girdi/sınır kontrolleri ve 300 bozuk ifade;
7 gerçek Qt etkileşim testi; Qt network import ile aynı JS modülü; native clipboard
header/uygulama karşılaştırması ve Node adaptör testi geçti. 25 QML bytecode,
11 Alt+Tab Qt, OSD/ikon ve 12 update/restore fixture'i de geçti.
1600×1000 render incelendi; 900×600 yerleşim sınırları denetlendi.

Native QuickShell Wayland panosundan başka uygulamaya yapıştırma bu ortamda
doğrulanmadı. Qt fixture'ı ve UI'daki “Copied” metni bunun kanıtı değildir.
Kullanıcı kabulü `../VALIDATION.md` içindedir.

17 Ekim kullanıcı “Güzel çalışıyor devam edebilirsin” diyerek normal kullanımı
onayladı. PR #6 ana dala birleştirildi. Her klavye/pano alt testi ayrıca raporlanmış
sayılmaz; hazırlanma ortamında native Wayland panosu çalıştırılmadığı kaydı korunur.
