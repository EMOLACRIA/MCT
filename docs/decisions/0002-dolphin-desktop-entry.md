# ADR-0002 — Dolphin için tek desktop girdisi

Tarih: 2026-10-17. Durum: **Uygulandı ve kullanıcı tarafından 2026-10-17 tarihinde doğrulandı**.

## Sorun

Launcher temalı `org.kde.dolphin.desktop` girdisindeki Qt ortamını kullanırken
Super+E düz `dolphin` çalıştırıyordu. Ortamı Lua'ya kopyalamak iki ayarın
zamanla ayrılmasına ve eklenti restore edilince eski ayarın kalmasına neden olur.

## Karar

Super+E, ortak `file-manager.sh`/`.py` üzerinden kullanıcı `XDG_DATA_HOME`, sonra
`XDG_DATA_DIRS` sırasında Dolphin desktop girdisini bulur. `gio launch` desktop
Exec alanını işler; Python bunu shell olarak ayrıştırmaz veya çalıştırmaz.
Kurulum/güncelleme `gio` gereksinimini dosya yazmadan kontrol eder (Arch: glib2).

Girdi yoksa kurulu Dolphin'e geçilir. Mevcut girdi varsa GIO/başlatma hatasında
sessizce düz Dolphin açılmaz. Eklenti restore sonraki açılışta doğal olarak
sistem girdisine geçer. Kullanıcının farklı dosya yöneticisi veya özel E eylemi
migrasyonda değiştirilmez. Dosya/URL argümanları ayrı argv öğeleri olarak aktarılır.

## Bedel ve kapsam

GIO CLI bağımlılığı eklenir. Doğrudan terminalde `dolphin` çalıştırmak bu yardımcıyı
kullanmaz; terminal için aynı helper belgelenir. Kullanıcının MIME varsayılanı
başka uygulamaysa zorla değiştirilmez. Tam varsayılan uygulama ayar ekranı M2 işidir.

## Kaynaklar

- https://docs.gtk.org/gio/method.AppInfo.launch.html
- https://archlinux.org/packages/core/x86_64/glib2/files/

## Kullanıcı kabulü

PR #1 dalındaki `62cfe809d0274fd2ec99a8aca4e37f117b20fe9f` uygulandıktan sonra
kullanıcı launcher/Super+E karşılaştırmasını “Aynen çalışıyor” diyerek onayladı.
