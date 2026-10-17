# ADR-0001 — Önce tamamlanmış Plague Tale, sonra farklı temalar

Tarih: 2026-10-17. Durum: **Kabul edildi — kullanıcının açık kararı**.

## Bağlam

Amaç HyprCADE'in daha bütünlüklü devamını yapmak. Kullanıcı Vitreus ve
Caelestia'yı beğeniyor; ileride görsel açıdan çok farklı temalar istiyor.
Bir temada bulunan işlevin diğerinde eksik kalmasını ve alışkanlıkların
bozulmasını özellikle istemiyor. Mevcut tema hâlâ canlı düzeltme gerektiriyor.

## Karar

- Plague Tale referans tema olarak tüm kabul edilen temel işlevlerle bitirilir.
- Yakın kapsam: Alt+Tab seçici, launcher hesaplama, ortak ayarlar ekranı.
- Pano/yeni yakalama paneli şimdilik alınmaz; oyun kütüphanesi ertelenir.
- Ortak işlev ve kısayollar temadan ayrılır. Farklı görseller aynı sözleşmeyi karşılar.
- İlk temanın M4 kabulü tamamlanmadan tema değiştirici ve ikinci tema başlamaz.
- Vitreus/Caelestia ilhamdır; runtime değişimi veya bütün özelliklerini alma kararı yok.

## Sonuçlar / bedeller

İkinci temanın başlangıcı gecikir. Bunun karşılığında ilk tema ortak özelliklerin
referans uygulaması olur; sonradan her temaya ayrı ayrı özellik yetiştirme riski azalır.
Yalnızca duvar kâğıdı/rengi değiştiren bir sistem hedefi karşılamaz. Şekil, malzeme,
font, animasyon ve düzen farklılaşırken eylemler ve kullanıcı tercihleri sabit kalır.

## Değişiklik

Yeni kullanıcı kararı gelirse bu kayıt sessizce yeniden yazılmaz; yerine geçen
karar ve gerekçesi bağlanır. Teknik uygulama ayrıntıları henüz seçilmiş sayılmaz.
