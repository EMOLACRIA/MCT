# GitHub çalışma düzeni

Ana depo: https://github.com/EMOLACRIA/MCT
Başlangıç commit'i: `dd146961f82e2a02034152e9ba6e3501ee4af5e1`.
Tam kaynaklar kullanıcı tarafından ana dala yüklendi; eski ZIP yükleme notları
artık güncel akış değildir. `.gitignore` önbellek/log/yedekleri dışarıda tutar.

Yerel kaynak klasöründe önce `git status`, sonra `git fetch origin` ile mevcut
çalışma kontrol edilir. Geliştirme dallarında küçük, doğrulanabilir değişiklikler
hazırlanır; kullanıcı düzenlemeleri silinmez ve force push kullanılmaz.

PR #1 Dolphin düzeltmesi kullanıcı tarafından denendi ve ana dala birleştirildi.
Güncel ana dalı almak için, yerel düzenleme yoksa:

```bash
git fetch origin
git switch main
git pull --ff-only
```

Yeni geliştirme PR'ları kendi dallarından denenebilir. Hedef Hyprland oturumunda
uygulama: `bash update.sh --check && bash update.sh`.
Spotify sonucu için salt okunur tanılama: `bash apps/diagnose.sh`.
