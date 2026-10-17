# ADR-0005 — Bildirim süresi ve aynı nesnenin güncellenmesi

Tarih: 2026-10-17. Durum: uygulandı; native oturum kabulü bekliyor.

## Kanıt

Hedef QuickShell `v0.3.1` kaynakları ve Desktop Notifications protokolü incelendi:

- [Protokol: Notify](https://specifications.freedesktop.org/notification/latest/protocol.html):
  `expire_timeout` milisaniye; `0` süresiz, `-1` sunucu varsayılanı.
- [server.cpp](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/services/notifications/server.cpp):
  `Notify` değeri doğrudan updateProperties'e geçirir; mevcut nesne güncellendiğinde
  yeni notification olayı göndermez.
- [notification.cpp](https://github.com/quickshell-mirror/quickshell/blob/v0.3.1/src/services/notifications/notification.cpp):
  `bExpireTimeout = expireTimeout` atamasında dönüşüm yoktur. Header'ın saniye
  açıklamasına rağmen bu sürümün gerçek aktarımı milisaniyedir. Özellik değişim
  sinyalleri vardır; tüm alanları aynı kalan tekrarda sinyal garantisi yoktur.

Eski shell süreyi tekrar 1000'le çarpıyordu; 5000 ms, 5000 saniye oluyordu.
Kartlar ilk receive anında kopyalandığından sonradan değişen metin/eylemler eski
kalıyordu. receive'in tekrar çağrılması da unread ve closed handler'larını çoğaltıyordu.

## Karar

- Pozitif süre doğrudan Qt Timer'a milisaniye verilir; varsayılan 5000 ms,
  `0` için expiry timer yoktur. Qt int aralığı gözetilir.
- Her native nesne için bir watcher; başlık, gövde, uygulama, eylem, süre ve
  transient property sinyalleri event döngüsü sonunda tek refresh üretir.
- Mevcut kart/geçmiş kaydı güncellenir. Unread ve closed handler yalnız ilk
  takibe aittir. Önceki expiry/toast timer'ları yenilemede/kapanışta temizlenir.
- Native bildirim kapanınca watcher bekleyen refresh'i iptal edip kaldırılır.
  Süre dolunca arşiv metni korunur, canlı eylemler kaldırılır.

## Doğrulama ve sınırlar

Üretim JS fonksiyonları Node'da kontrollü servislerle; watcher gerçek Qt sinyal
ve timer döngüsüyle denetlendi. Native QuickShell/uygulama D-Bus testi değildir.
Hiç property değişmeyen Notify tekrarı bu API'de gözlenemeyebilir; o durumda
ömrün yenileneceği garanti edilmez. Gelecek QuickShell sürümleri için bu birim
kararı yeniden kaynakla doğrulanmalıdır.
