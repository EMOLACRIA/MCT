# GitHub çalışma düzeni

Ana depo: https://github.com/EMOLACRIA/MCT
Başlangıç commit'i: `dd146961f82e2a02034152e9ba6e3501ee4af5e1`.
Tam kaynaklar kullanıcı tarafından ana dala yüklendi; eski ZIP yükleme notları
artık güncel akış değildir. `.gitignore` önbellek/log/yedekleri dışarıda tutar.

Yerel kaynak klasöründe önce `git status`, sonra `git fetch origin` ile mevcut
çalışma kontrol edilir. Geliştirme dallarında küçük, doğrulanabilir değişiklikler
hazırlanır; kullanıcı düzenlemeleri silinmez ve force push kullanılmaz.

PT-001 değişikliğini denemek için, yerel düzenleme yoksa:

```bash
git fetch origin
git switch --track origin/fix/dolphin-launch-consistency
bash update.sh --check && bash update.sh
```

Dal yerelde zaten varsa `git switch fix/dolphin-launch-consistency` kullanılır.
Bu kurulum işlemi yalnızca kullanıcının hedef Hyprland oturumunda yapılır.
