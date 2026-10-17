# ADR-0004 — Spotify sürüm sınırı ve gerçek tema çıktısı

Tarih: 2026-10-17. Durum: kurucu korumaları uygulandı; PT-002 açık.

## Kanıt

Kullanıcı: Spotify `1:1.3.4.258-2`, spotify-adblock `1:1.1.1-1`, Spicetify CLI
`2.45.3-1`. Normal/adblock girdileri sarmalayıcıya yönleniyor; LD_PRELOAD korunmuş.
Bu bilgi temalı özel kopyanın sürümünü veya UI/adblock sonucunu belirlemez.

[Upstream v2.45.3 sürüm notları](https://github.com/spicetify/cli/releases/tag/v2.45.3)
aynı tarihte incelendi: Linux desteği `1.2.14–1.2.96`. Upstream `src/utils/print.go`
apply spinner'ını stderr'e yazar; yalnız stdout tutan eski günlük uygulamanın
tamamlanıp tamamlanmadığını kanıtlamaz. `src/apply/apply.go` user.css, colors.css
ve `src/cmd/apply.go` spicetify-config.json çıktılarının biçimini tanımlar.

## Karar

- Pacman sistem paketi ve CLI sürümü uygulama öncesi okunur. Bilinen 2.45.3 Linux
  aralığı dışı durur; gelecekteki CLI sürümlerinin desteği tahmin edilmez.
- stdout/stderr tek günlükte toplanır. Başarılı çıkış tek başına yeterli değildir:
  HTML'de CSS bağlantıları, beklenen user.css, palet ve tema metadata'sı denetlenir.
- Eksik çıktı önceki kopya/başlatıcı rollback yolunu kullanır. Başarılı kopya,
  kaynak paket ve CLI sürümlerini kendi `versions.json` dosyasında saklar.
- Tanılama yalnız dosyaları okur. Eski kopyada sürüm kaydı yoksa bunu açıklar;
  kullanıcı hesabı/tercihlerini sürüm bulmak için okumaz.
- Restore sürüm kontrolünden bağımsız kalır. Otomatik downgrade, indirme,
  uyumsuz istemciye ek JavaScript yaması veya adblock kaldırma yapılmaz.

## Sınırlar

Bu değişiklik Spotify 1.3.4'e tema desteği eklemez. Uyumlu paket/CLI ve native UI
ile adblock kabulü olmadan PT-002 kapanmaz. Yeni CLI sürümleri için destek aralığı
belgelenene kadar uyarı ve çıktı kontrolü vardır; uyum garantisi yoktur.
