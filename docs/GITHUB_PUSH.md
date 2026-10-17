# ZIP içeriğini GitHub'a yükleme

Bu arşiv tam kaynakları, görselleri ve proje belgelerini içerir. `.git`, Python
önbelleği, log, kurulum yedeği ve yerel bağımlılık ortamı içermez.
`PROJECT_BRIEF.txt` ürün hedefini, `ROADMAP.md` aşamaları ve `AGENTS.md` asistan
çalışma kurallarını tutar. `STATUS.md` açık sorunları gizlemeden kaydeder.

## Yeni bir boş depo kullanacaksan

GitHub'da istediğin adla boş bir repo aç. README/lisans/.gitignore ekletme;
bu ZIP'teki dosyalar ilk commit olacak. ZIP'i temiz bir klasöre çıkarıp içindeki
`desktop-style` klasöründe:

```bash
git init -b main
git add .
git status --short
git commit -m "Import Plague Tale desktop sources and project roadmap"
```

Ardından kendi deponun gerçek URL'sini ekle:

```bash
git remote add origin https://github.com/EMOLACRIA/DEPO_ADI.git
git push -u origin main
```

`DEPO_ADI` seçtiğin gerçek repo adıyla değiştirilmeli.

## Mevcut HyprCade deposu

Hazırlama sırasında `plague-tale-foundation` dalı mevcut `main` commit'inden
oluşturuldu. Bu proje o dala henüz commit edilmedi; dal yeni kaynakları içermiyor.
Mevcut bir repo kullanacaksan önce o deponun kendi clone'unda çalış; bu yeni
ZIP klasöründen mevcut branch üzerine force push yapma. Kaynak yerleşimini
bilerek seçip `git status`/diff'i gözden geçirerek normal commit/push kullan.

Bu belge otomatik bir uploader çalıştırmaz ve kurulum scripti çalıştırmayı gerektirmez.
