# ADR-0009 — Uzun içerikte panel sınırlarını koruma

Tarih: 2026-10-17. Durum: **2.5.1 uygulandı; native kullanıcı kabulü bekliyor**.

## Sorun ve karar

%120 font/900×600 önizlemesinde çok sayıda tray girdisi saat bölgesine giriyordu.
Uzun başlık ve sekiz oynatıcıyla medya listesi çerçevenin altına taşıyordu.
640×480 oturum menüsünde satırlar metnin gerektirdiği yüksekliğin altına iniyordu.
Bildirim eylemi ve oynatıcı adı butonun doğal genişliğini sınırsız büyütebiliyordu.

Tray görünümüne saat ile sağ eylemler arasında sınırlı bir viewport ve önceki/sonraki
okları eklendi. Uzun tarih gerektiğinde elide edilir; saat merkezde kalır.
Viewport tekerleği gezinmek için kullanmaz; simgenin scroll eylemi backend'e gider.
Native menü koordinatları taşınan simgeden bar köküne mapToItem ile hesaplanır.
Yeni popup/panel veya ikinci tray servisi yoktur.

Medya başlığı ve güç menüsü üst bilgisi sabit, uzun içerikleri kaydırılabilir.
Klavye ile odaklanan medya girdisi ve seçili güç işlemi görünür alana getirilir.
Güç panelinin tercih edilen yüksekliği font ölçeğini izler ve ekranla sınırlanır;
normal boyutta gereksiz kaydırma yoktur. Tehlikeli işlemler yine ayrıca onay ister.
Uzun medya/bildirim eylemi adları buton içinde kısaltılır; hover tam adı gösterir.

## Sınırlar ve doğrulama

Mevcut `checks/test_shell_ui.py` eski build/desktop-style bağımlılığından çıkarıldı.
7 gerçek Qt testi; panel sınırları/boş veri, tray gezinme ve sağ tık, uzun eylemler,
medya klavye seçimi, güç seçimini görünür tutma ve onay davranışı kontrol edildi.
Bar 900/1132/1200/1600 mantıksal genişlikte, paneller ayrıca 640×480'de denetlendi.
900'ün altında kalabalık tray için tam erişim bu revizyonun kabul kapsamı değildir;
en az 900 mantıksal genişlik bu yoğun barın kontrol edilen kullanım alanıdır.
Native Wayland popup yerleşimi, gerçek uygulama tray scroll ve çoklu ekran hâlâ
hedef oturumda denenmelidir. Bu kayıt tam M3/M4 kabulü değildir.
