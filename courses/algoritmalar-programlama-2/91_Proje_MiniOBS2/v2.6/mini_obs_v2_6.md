# Mini-OBS 2 v2.6 — Sıralamanın Ötesi: not dağılımı, ilk-k listesi, taban sıralaması ve ölçüm raporu (Hafta 7 · ara proje)

**Bu sürümün amacı:** Karşılaştırmaya dayalı sıralamanın Ω(n log n) sınırının **dışına** çıkmak ve öbeği (heap) Mini-OBS'nin iki sorusuna uygulamak: (1) **not dağılımı** — yuvarlanmış notlar 0–100 aralığında olduğu için sıklıklar Θ(n + 101)'de sayılır; dağılım, ortanca ve "notu en yüksek K öğrenci" listesi sıralama yapmadan (kararlı **sayma sıralamasıyla**) çıkar (10⁵ kayıtta sıklık sayımı 3,2 ms); (2) **ilk-k listesi** — başarı listesinin ilk 10'u k boyutlu bir **öbekle** Θ(n log k)'de bulunur: 10⁵ kayıtta 6,3 ms, bütün listeyi sıralamak ise 383,0 ms; (3) **taban sıralaması** — 10 haneli öğrenci numaraları dört baytlık geçişle sıralanır: 10⁶ anahtarda 79,3 ms (birleştirmeli sıralama 273,1 ms, `qsort` 257,7 ms); (4) **çok yollu birleştirme** — k şubenin listesi k boyutlu en küçük öbekle birleşir. Ara projenin ölçüm raporu (`mini_obs_v2_6_olcum_raporu.md`) dokuz algoritmayı (seçmeli, kabarcık, araya ekleme, birleştirmeli, hızlı, öbek, sayma, taban, `qsort`) dört girdi türünde ve n = 10³–10⁶ aralığında karşılaştırır. Bu sürümün kâhin testleri ayrıca v2.4'ten beri fark edilmemiş bir hatayı buldu: ders ortalaması ölçütleri matematiksel olarak eşit ortalamaları kayan noktadaki son bit farkına göre sıralıyordu (bölüm 4.7).

Dosyalar (satır sayılarıyla): `obek.h` (61) · `obek.c` (153) · `dogrusal.h` (52) · `dogrusal.c` (149) · `dagilim.c` (285) · `ilk_k.c` (130) · `sube.h` (42) · `sube.c` (149) · `birlestir.c` (243) · `liste.h` (109) · `liste.c` (362) · `listele.c` (217) · `olcer.c` (1667) · `test_obs.c` (1786) · `test_kahin.c` (2711) · `bolfethet.h` (66) · `bolfethet.c` (324) · `ortanca.c` (156) · `yinelenen.h` (57) · `yinelenen.c` (183) · `denetle.c` (188) · `dosya.h` (106) · `dosya.c` (544) · `main.c` (342) · `arama.h` (120) · `arama.c` (258) · `ara.c` (232) · `obs.h` (141) · `obs.c` (673) · `turkce.h` (51) · `turkce.c` (135) · `siralama.h` (47) · `siralama.c` (141) · `sayac.h` (49) · `sayac.c` (21) · `metin.h` (35) · `metin.c` (340) · `secmeli.h` (102) · `secmeli.c` (330) · `ders_sec.c` (184) · `uretec.h` (54) · `uretec.c` (160) · `veri_uret.c` (94) · `deney.h` (28) · `deney.c` (32) · `ortak_rastgele.h` (43) · `ortak_rastgele.c` (50) · `zamanlayici.h` (34) · `zamanlayici.c` (63) · `Makefile` (363) · `ornek_veri/sube_c.csv` (C şubesi, 6 kayıt) ve önceki sürümlerin örnek ve test girdileri · `olcum/kiyas.csv`, `olcum/aralik.csv`, `olcum/ilk_k.csv`, `olcum/ilk_k_tam.csv`, `olcum/cok_yollu.csv`, `olcum/cok_yollu_kiyas.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_6_ciktilar.txt` (1766 satır, gerçek çıktılar) · **`mini_obs_v2_6_olcum_raporu.md`** (ara projenin referans ölçüm raporu). Şekiller: `mini_obs_v2_6_obek.png`, `mini_obs_v2_6_sayma.png`, `mini_obs_v2_6_taban.png`; grafikler: `mini_obs_v2_6_olcum_girdiler.png`, `mini_obs_v2_6_olcum_cubuk.png`, `mini_obs_v2_6_olcum_obek.png`.

Derleme: `make` (`mini_obs`, `veri_uret`, `olcer`, `denetle`, `ders_sec`, `ara`, `listele`, `ortanca`, `birlestir`, **`dagilim`**, **`ilk_k`**), `make test`, `make olcum` (bu makinede 1 dakika 33 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 31 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0, 1 (dosya okunamadı, bellek yetersiz, şubelerde çakışma ya da `--denetle` uyuşmazlık buldu; testlerde uyuşmazlık), 2 (hatalı kullanım; ör. `sayma` yöntemi soyad ölçütüne).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 7'nin sorusu: karşılaştırmayla sıralamanın aşılamaz bir sınırı varsa (karar ağacının n! yaprağı: en az log₂ n! ≈ n log₂ n − 1,44n karşılaştırma), sayma ve taban sıralaması bu sınırı nasıl "aşar"? Yanıt: aşmazlar, **sınırın varsayımını** değiştirirler — öğeleri karşılaştırmaz, anahtarlarını bir dizinin indisi olarak kullanırlar. Mini-OBS'de bu, verinin özelliklerine bakmak demektir:

- **İkili öbek ve öbek sıralaması** (ÖÇ 7.1–7.2): dizi gösterimi (çocuklar 2i + 1, 2i + 2), aşağı süzme, aşağıdan yukarıya kurma Θ(n), öbek sıralaması Θ(n log n) yerinde ama kararsız (Şekil 1).
- **Öncelik kuyruğu uygulamaları** (ÖÇ 7.3): ilk-k listesi (k boyutlu öbek) ve çok yollu birleştirme (k şubenin sıradaki kayıtları öbekte).
- **Sayma ve taban sıralaması** (ÖÇ 7.4): notlar 0–100 aralığında → sayma (Θ(n + K)); numaralar sabit uzunlukta → LSD taban sıralaması (Θ(d·n)); taban sıralamasının doğruluğu **her geçişin kararlı olmasına** bağlıdır (`--hata-goster lsd`).
- **Algoritma seçimi** (ÖÇ 7.5): ölçüm raporu, dokuz algoritmayı dört girdi türünde karşılaştırır ve verinin boyutu, anahtar aralığı, sıralılığı ve kararlılık gereksinimine göre bir seçim tablosu verir.
- **Mühendis gözüyle — kâhin bağımsız olmalı:** v2.4'ten beri liste testlerinin kâhini, sınanan karşılaştırıcıyla aynı karşılaştırıcıyı (`qsort` + aynı ölçüt) kullanıyordu; ortak bir hatayı göremezdi. v2.6'nın tamsayı anahtarlı sayma sıralaması **bağımsız** bir yol olduğu için uyuşmazlık hemen göründü.

Yol haritasındaki karşılığı (Tablo A.1): **H7 · v2.6 (ara proje) · Not dağılımı (sayma sıralaması), başarı sıralamasında ilk-k listesi (öbek), öğrenci numarasında taban sıralaması ve tüm sıralama algoritmalarını karşılaştıran ölçüm raporu · Sayma/taban sıralaması, öbek.** Ara projenin yönergesi: `../ARA_PROJE_YONERGESI.md`; rapor şablonu: `../ARA_PROJE_RAPOR_SABLONU.md`.

## 2. v2.5'ten ne değişti?

| Konu | v2.5 (H6) | v2.6 (H7) |
|---|---|---|
| Öbek | — | **`obek.h/.c`**: `asagi_suz_say`, `obek_kur_say` (Θ(n)), `obek_mi`, `obek_sirala_say`, `ilk_k_say` (Θ(n log k)) |
| Doğrusal sıralama | — | **`dogrusal.h/.c`**: `sayma_sirala_say` (kararlı, artan/azalan, Θ(n + K)), `sayma_dagilimi`, `taban_sirala_say` (LSD, taban 256, geçiş sayısı en büyük anahtardan) |
| Not dağılımı | — | **`dagilim`**: yuvarlanmış not sıklıkları, aralık tablosu ve çubuklar, ortanca ve en sık not, `--liste K` (kararlı sayma), `--denetle` |
| İlk-k | — | **`ilk_k`**: ölçüte göre ilk K kayıt (öbek), `--denetle` (kâhin: bütün liste) |
| Şube birleştirme | iki şube | + **çok yollu** (3–26 şube, `subeler_birlestir`, en küçük öbek); `--yontem obek` |
| `listele` | 7 yöntem | + `obek` (her ölçüt), `sayma` (basari, alg, mat, fiz: iki kararlı geçiş), `taban` (no) |
| Ders ölçütü karşılaştırıcısı | ortalama `double` olarak | **tamsayı (× 500)** — eşit ortalamalarda soyad karar verir (bölüm 4.7) |
| `olcer` | böl ve fethet | + `kiyas_*` (9 algoritma × 4 girdi), `aralik_*` (anahtar aralığı), `liste_ilk_k`, `subeler_obek`; `--sira tekrarli`, `--k`; CSV'de `parametre` ve `toplama` sütunları |
| Testler | 226 birim; kâhin 350 751 | 245 birim (+19 öbek-doğrusal); kâhin 354 990 denetim; `--hata-goster lsd`, `--hata-goster suzme` |

Menü ve yükleyici değişmedi; v1.0'ın T2 oturumu yine yalnızca başlık ve arama istemi satırlarında farklıdır.

## 3. Mimari

| Modül / program | Sorumluluk | Bağımlılık |
|---|---|---|
| `obek` (**yeni**) | ikili öbek, öbek sıralaması, ilk-k | `sayac`, `siralama.h` (`Karsilastirici`): öğe türünü bilmez |
| `dogrusal` (**yeni**) | sayma ve taban sıralaması, sıklık | yalnız `sayac`: anahtar, `AnahtarFn` ile dışarıdan verilir |
| `sube` | + çok yollu birleştirme (numara, şube) öbeği | `obs`, `sayac` |
| `liste` | + üç yöntem; ders ölçütü tamsayı karşılaştırması | + `obek`, `dogrusal` |
| `dagilim.c`, `ilk_k.c` (**yeni**) | komut satırı araçları | `liste`, `dogrusal`, `obek`, `bolfethet` (kâhin) |
| `birlestir.c` | + k şube | `sube` |
| diğerleri | v2.5'ten aynen | — |

`obek.o` ve `dogrusal.o` `SIRALAMA` nesne grubundadır (liste onları kullanır). İki yeni modül de v2.4'ten beri süren arayüz sözleşmesini sürdürür: öğe türünü bilmeyen `(taban, n, boyut, …, Sayac *)` imzası ve aynı sayaç tanımları. Sayma ve taban sıralaması karşılaştırıcı yerine bir **anahtar fonksiyonu** alır (`unsigned long long (*)(const void *)`); karşılaştırma sayaçları 0, çalışma `toplama` (sayaç artırma ve önek toplamı) ve `tasima` sayaçlarında görünür.

## 4. Algoritmalar

### 4.1 İkili öbek ve öbek sıralaması

![Öbek kurma](mini_obs_v2_6_obek.png)

*Şekil 1. Aşağıdan yukarıya öbek kurma, Cormen vd. (2022) Şekil 6.3'ün girdisiyle. Dizi gösteriminde işaretçi yoktur: i'nin çocukları 2i + 1 ve 2i + 2'dir. Sonuç (16 14 10 8 7 9 3 2 4 1) ve sayaçlar (14 karşılaştırma, 17 taşıma) birim testinde programla doğrulanır.*

```
algoritma AŞAĞI-SÜZ(a[0..m−1], i)                   ▷ i'nin alt ağaçları öbek
    g ← a[i]                                         ▷ "delik" yöntemi: takas yerine kaydırma
    sonsuz döngü
        c ← 2i + 1; eğer c ≥ m ise çık
        eğer c + 1 < m ve a[c+1] > a[c] ise c ← c + 1      ▷ büyük çocuk
        eğer a[c] ≤ g ise çık
        a[i] ← a[c]; i ← c
    a[i] ← g
algoritma ÖBEK-SIRALA(a[0..n−1])
    i ← ⌊n/2⌋ − 1'den 0'a: AŞAĞI-SÜZ(a, i)           ▷ kurma: Θ(n)
    m ← n − 1'den 1'e:                                ▷ değişmez: a[m+1..n−1] sıralı, en büyükler
        a[0] ↔ a[m]; AŞAĞI-SÜZ(a[0..m−1], 0)
```

- **Kurma Θ(n)'dir**, n log n değil: yüksekliği h olan en çok ⌈n / 2^(h+1)⌉ düğüm vardır ve her biri en çok h düzey iner; Σ h·n/2^(h+1) < n. Süzme düzey başına en çok iki karşılaştırma yaptığından kurma ≤ 2(n − 1) karşılaştırmadır (Floyd, 1964).
- **Öbek sıralaması** Θ(n log n) her durumda, yerinde (Θ(1) ek bellek), **kararsız** (Williams, 1964): `testler/kararlilik.csv`'de üç ECE KAYA kaydının sırası bozulur (bölüm 5.4). Ölçüm raporunda öbek sıralaması, Θ(n log n) yöntemlerin en yavaşıdır: 10⁶ karışık anahtarda 599,1 ms (hızlı sıralama 254,5 ms). Sebep **önbellektir**: aşağı süzme dizinin uzak konumlarına (i → 2i + 1) atlar.
- **Hata Avcısı — sağ çocuk unutulursa:** `--hata-goster suzme` yalnızca sol çocuğa bakan süzmeyi kâhine verir; 2..6 öğeli bütün girdiler denenerek bulunan en küçük karşı örnek 3 öğedir (bölüm 8).

### 4.2 İlk-k listesi

```
algoritma İLK-K(a[0..n−1], k)                      ▷ kars sırasına göre ilk k
    ö ← a[0..k−1]; ÖBEK-KUR(ö)                      ▷ kök: seçilenlerin EN KÖTÜSÜ
    i ← k'dan n−1'e:                                 ▷ değişmez: ö = a[0..i−1]'in ilk k'sı
        eğer a[i] kökten önce geliyorsa: ö[0] ← a[i]; AŞAĞI-SÜZ(ö, 0)
    ÖBEK-SIRALA(ö); ö'yü döndür
```

Her kayıt kökle **bir kez** karşılaştırılır; yalnızca ilk k'ya girenler öbekte Θ(log k) iş yapar. Rastgele sırada gelen kayıtlarda i. kaydın ilk k'ya girme olasılığı k/i'dir; beklenen yer değiştirme sayısı ≈ k ln(n/k), yani k ≪ n için iş ≈ n karşılaştırmadır. Ölçüm (n = 10⁵, Tablo 3): k = 10 için 100 457 karşılaştırma (≈ n), bütün listeyi birleştirmeli sıralamak 1 536 453. Sonucun tek olması için ölçüt **numarayla tamamlanır** (tam sıralama): eşit başarılı iki kayıttan hangisinin listeye girdiği öbeğin iç düzenine bırakılmaz. Kâhin, bütün listenin kararlı (birleştirmeli) sıralamasının ilk k'sıdır.

### 4.3 Çok yollu birleştirme

v2.5'in iki işaretçili birleştirmesi k şubeye genellenir: her şubenin sıradaki kaydı (numara, şube sırası) anahtarıyla k boyutlu bir **en küçük öbekte** tutulur; kök alınır, aynı şubenin sonraki kaydı köke konur ve aşağı süzülür. Θ(n log k) karşılaştırma, Θ(k) ek bellek (çıktı hariç). Aynı numara birden çok şubede varsa en küçük sıradaki şubenin kaydı bir kez girer ve numara çakışma listesine yazılır (k = 2 için `sube_birlestir` ile **aynı** sonuç ve çakışma; birim testi ve kâhin).

### 4.4 Sayma sıralaması ve not dağılımı

![Sayma sıralaması](mini_obs_v2_6_sayma.png)

*Şekil 2. Sayma sıralaması (birim testindeki örnek; K = 4): sıklık, ilk konum (önek toplamı), girdi sırasıyla yerleştirme. 1·b ile 1·d ve 3·a ile 3·f girdi sıralarını korur: kararlı.*

```
algoritma SAYMA-SIRALA(a[0..n−1], anahtar, K) → c
    say[0..K−1] ← 0;  i ← 0..n−1: say[anahtar(a[i])]++               ▷ n adım
    toplam ← 0;  k ← 0..K−1: (kon[k], toplam) ← (toplam, toplam + say[k])   ▷ K adım
    i ← 0..n−1: c[kon[anahtar(a[i])]++] ← a[i]                        ▷ girdi sırasıyla: KARARLI
```

Θ(n + K) zaman ve ek bellek; hiçbir öğe başka bir öğeyle karşılaştırılmaz. **Azalan** sıra için önek toplamı büyük anahtardan başlar (yine kararlı). `dagilim` yalnızca ilk adımı kullanır: sıklıklar → aralık tablosu ve çubuklar; birikimli sıklık → ortanca ((n − 1)/2. ve n/2. konumdaki notlar) ve en sık not. `--liste K`, notu en yüksek K öğrenciyi kararlı sayma sıralamasıyla verir: eşit notlular numara sırasında kalır. Kâhin: notların birleştirmeli sıralanması (koşu uzunlukları = sıklıklar; ortadaki öğeler = ortanca; aynı anahtarla kararlı liste).

**K'nın bedeli.** K, n'ye göre büyüdükçe sayaç dizisi baskınlaşır: n = 10⁵'te K = 10⁷ olduğunda sayma 105,0 ms, birleştirmeli sıralama 25,1 ms sürer (Tablo 2). Bu ölçümde sayma, birleştirmeliden ilk kez K = 10 000 000 değerinde yavaş kalır.

### 4.5 Taban sıralaması (LSD)

![Taban sıralaması](mini_obs_v2_6_taban.png)

*Şekil 3. LSD taban sıralaması, Cormen vd. (2022) Şekil 8.3'ün girdisiyle (gösterim taban 10). Her geçiş bir basamağa göre kararlı sıralamadır; üç geçişten sonra dizi sıralıdır. Kod taban 256 kullanır.*

```
algoritma TABAN-SIRALA(a[0..n−1], anahtar)
    d ← en büyük anahtarın bayt uzunluğu              ▷ 10 haneli numara < 2³² → d = 4
    g ← 0'dan d−1'e:                                   ▷ değişmez: a, anahtarın son g baytına göre sıralı
        a ← g. bayta göre KARARLI SAYMA (K = 256)        ▷ tampon ile dizi yer değiştirir
```

Θ(d·(n + 256)) zaman, Θ(n) ek bellek, kararlı. Ölçüm raporunun en hızlı genel amaçlı sıralamasıdır: 10⁶ karışık numarada 79,3 ms — karışık girdide aynı boyuttaki sayma sıralamasından (197,1 ms, K = 10⁶) bile hızlıdır. Sayma bu girdide çıktı dizisinin rastgele konumlarına yazar (önbellek kaçırmaları); taban sıralamasının 256 kovası ise önbelleğe sığar. Karşılaştırma tabanlı yöntemler 10⁶ öğede en az log₂ n! ≈ 18,5 · n karşılaştırma yapmak zorundadır.

**Hata Avcısı — kararlılık bir doğruluk koşuludur:** `--hata-goster lsd` her geçişi kararsız yapar (öğeler sondan başa dolaşılır). Tek geçişte sonuç yine anahtara göre sıralıdır, yalnızca eşitlerin sırası bozulur; iki geçişte ise sıralama **yanlıştır**. En küçük karşı örnek iki öğedir: [257, 256] → [257, 256] (birinci geçiş düşük baytı doğru sıralar, ikinci geçiş eşit yüksek baytlı iki öğenin sırasını tersine çevirir; bölüm 8).

### 4.6 Ω(n log n) alt sınırı

Karşılaştırmaya dayalı her sıralama algoritması bir **karar ağacıdır**: her iç düğüm bir karşılaştırma, her yaprak girdinin bir permütasyonudur. Ağaç n! permütasyonu ayırt etmek zorunda olduğundan en az n! yaprağı ve en az ⌈log₂ n!⌉ yüksekliği vardır; log₂ n! = n log₂ n − n log₂ e + O(log n) (Stirling). Birleştirmeli sıralamanın en kötü durumu n⌈log₂ n⌉ − 2^⌈log₂ n⌉ + 1 bu sınıra çok yakındır (Knuth, 1998). Sayma ve taban sıralaması karşılaştırma yapmadığı için bu modelin dışındadır; bedelleri anahtar hakkında bir **varsayımdır** (küçük aralık ya da sabit uzunluk).

### 4.7 Listelerde sayma ve bir bulgu: kayan nokta eşitliği

`listele --yontem sayma`, çok anahtarlı ölçütü **iki kararlı geçişle** sıralar: önce ikincil anahtarlar (soyad ↑, ad ↑) birleştirmeli sıralamayla, sonra birincil anahtar sayma sıralamasıyla (başarı: YANO × 100 ∈ [0, 400]; ders: ortalama × 500 ∈ [0, 50 000]). v2.4'ün çok geçişli sıralamasının (bölüm 4.3) ve taban sıralamasının ortak fikri budur: kararlı son geçiş önceki sırayı eşitlerde korur.

Bu yöntemi kâhinle (`qsort` + numarayla tamamlanmış ölçüt) karşılaştıran ilk kâhin testi **başarısız** oldu: ALG ölçütünde iki liste farklıydı. Sebep v2.4'ten beri var olan bir hataydı. Ders ortalaması 0,4·vize + 0,6·final olarak `double`'da hesaplanır; matematiksel olarak eşit iki ortalama son bitte farklı olabilir (ör. 0,4·3 + 0,6·0 = 1,2000000000000002 ama 0,4·0 + 0,6·2 = 1,2; 0–100 tamsayı notlarda 388 farklı ortalama değerinde bu olur). v2.4–v2.5'in karşılaştırıcısı `double`'ları doğrudan karşılaştırdığı için bu kayıtları soyada göre değil son bit farkına göre sıralıyordu. Kâhin de **aynı** karşılaştırıcıyı kullandığı için hatayı göremiyordu; tamsayı anahtarlı sayma sıralaması bağımsız bir yol olduğundan farkı gösterdi. Düzeltme: ortalamalar tamsayı olarak (× 500, tam) karşılaştırılır — v2.4'te YANO için verilen kararın (tamsayı YANO) derslere genişletilmesi. Gösterim (v2.5 ↔ v2.6):

```
$ printf '…\n2301010091;CAN;ZEN;3;0;…\n2301010092;CAN;AK;0;2;…' > esit.csv; v2.5/listele esit.csv --olcut alg; ./listele esit.csv --olcut alg; ./listele esit.csv --olcut alg --yontem sayma --denetle
no;ad;soyad;ALG_vize;ALG_final;MAT_vize;MAT_final;FIZ_vize;FIZ_final
2301010091;CAN;ZEN;3;0;50;50;50;50
2301010092;CAN;AK;0;2;50;50;50;50
--- v2.5:
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010091  CAN ZEN                     1.20 FF   50.00 DC   50.00 DC   0.97
   2  2301010092  CAN AK                      1.20 FF   50.00 DC   50.00 DC   0.97
--- v2.6:
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010092  CAN AK                      1.20 FF   50.00 DC   50.00 DC   0.97
   2  2301010091  CAN ZEN                     1.20 FF   50.00 DC   50.00 DC   0.97
Kâhin (qsort + numara): AYNI
Eşit kayıtlar numara sırasında (kararlılık): EVET
[çıkış kodu: 0]
```

### 4.8 Kâhinler

| Sınanan | Kâhin |
|---|---|
| `sayma_sirala` (artan, azalan), `taban_sirala` | (anahtar, kimlik) çiftlerinde `qsort` + kimlik: kararlı sıranın tek tanımı; anahtar aralığı 2 … 2·10⁹; sayaçlar n + K, d·(n + 256) ve geçiş sayısı tanımdan |
| `obek_kur`, `obek_sirala` | öbek özelliği; `qsort` ile aynı anahtar dizisi; karşılaştırma ≤ 2n⌊log₂ n⌋ + 2n |
| `ilk_k` | tam sıralamada `qsort`'un ilk k öğesi (k > n dahil) |
| `subeler_birlestir` | k = 1..6 şubeyi uç uca ekleyip `qsort`; beklenen çakışmalar |
| `listele --yontem sayma`/`taban` | `qsort` + numarayla tamamlanmış ölçüt |
| `dagilim` | notların birleştirmeli sıralanması (sıklık, ortanca, liste) |
| `ilk_k` (program) | bütün listenin birleştirmeli sıralanması |

## 5. Kullanım

### 5.1 `dagilim`

```
./dagilim dosya.csv|dosya.dat [--ders ALG|MAT|FIZ] [--genislik G] [--liste K] [--denetle]
```

```
$ ./dagilim ornek_veri/ogrenciler.csv --liste 5 --denetle
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8 · ders: ALG (yuvarlanmış ortalama, 0–100)
 Aralık   Öğrenci   Yüzde   Birikimli
0–9             0     0.0           0
10–19           0     0.0           0
20–29           0     0.0           0
30–39           1    12.5           1   ███████████████
40–49           1    12.5           2   ███████████████
50–59           1    12.5           3   ███████████████
60–69           0     0.0           3
70–79           2    25.0           5   ██████████████████████████████
80–89           1    12.5           6   ███████████████
90–100          2    25.0           8   ██████████████████████████████
Ortanca: 77.5 · en sık not: 36 (1 öğrenci)
Notu en yüksek 5 öğrenci (sayma sıralaması, azalan, kararlı) · karşılaştırma 0 · toplama 109 · çarpma 0 · taşıma 8
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010050  EMRE ÇINAR                 96.80 AA   69.60 CB   78.60 BB   3.18
   2  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
   3  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
   4  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   5  2301010049  ZEYNEP ÇELİK               76.00 BB   63.00 CC   53.00 DC   2.21
Kâhin (birleştirmeli sıralama): AYNI (sıklıklar, ortanca ve liste)
Süre: sıklık 0.001 ms · sayma sıralaması 0.001 ms
[çıkış kodu: 0]
```

### 5.2 `ilk_k`

```
./ilk_k dosya.csv|dosya.dat [--k K] [--olcut basari|alg|mat|fiz|soyad|ad|no|soyad_bayt] [--denetle]
```

```
$ ./ilk_k u100k.csv --k 10 --denetle
Dosya: u100k.csv · kayıt: 100000
Ölçüt: basari — YANO ↓, soyad ↑, ad ↑ (başarı sırası); eşitlikte numara ↑
İlk 10 (k boyutlu öbek) · karşılaştırma 100457 · toplama 0 · çarpma 0 · taşıma 548
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2400091663  AHMET ACAR                 97.00 AA   95.60 AA   94.40 AA   4.00
   2  2400007791  AYŞE ACAR                 100.00 AA   95.20 AA   90.00 AA   4.00
   3  2400059429  AYŞE ACAR                  93.40 AA   90.40 AA   94.80 AA   4.00
   4  2400086773  BERK ACAR                  93.20 AA   90.40 AA   98.80 AA   4.00
   5  2400014548  BEYZA ACAR                100.00 AA  100.00 AA   95.80 AA   4.00
   6  2400036562  BURAK ACAR                 96.80 AA   90.00 AA   93.20 AA   4.00
   7  2400061695  BURAK ACAR                100.00 AA   92.60 AA   94.40 AA   4.00
   8  2400065812  BURAK ACAR                 92.40 AA   89.80 AA   92.80 AA   4.00
   9  2400006059  BÜŞRA ACAR                 92.00 AA   90.80 AA   97.80 AA   4.00
  10  2400012135  CAN ACAR                  100.00 AA   94.00 AA   95.80 AA   4.00
Kâhin (bütün liste birleştirmeli, ilk 10): AYNI · karşılaştırma 1536453 (öbek: 100457)
Süre: öbek 5.855 ms · bütün liste 334.273 ms
[çıkış kodu: 0]
```

### 5.3 `birlestir` (k şube)

```
$ ./birlestir ornek_veri/ogrenciler.csv ornek_veri/sube_b.csv ornek_veri/sube_c.csv --ilk 8
Şube A: ornek_veri/ogrenciler.csv · 8 kayıt
Şube B: ornek_veri/sube_b.csv · 6 kayıt
Şube C: ornek_veri/sube_c.csv · 6 kayıt
Birleşik: 20 kayıt (numara sırasında; çok yollu, öbek) · 32 karşılaştırma, 20 taşıma
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010040  ARDA KURT                  75.60 BB   68.00 CB   82.40 BA   2.97
   2  2301010041  BURAK AKSOY                69.20 CB   61.60 CC   73.00 BB   2.47
   3  2301010042  BERRA YAVUZ                86.80 BA   93.80 AA   79.00 BB   3.53
   4  2301010043  ELİF ŞİMŞEK                89.80 AA   78.80 BB   72.00 CB   3.21
   5  2301010044  CEREN POLAT                61.60 CC   52.60 DC   64.60 CC   1.82
   6  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   7  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
   8  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
  ... (12 kayıt daha)
Süre: birleştirme 0.002 ms
[çıkış kodu: 0]
```

```
$ ./birlestir ornek_veri/ogrenciler.csv ornek_veri/sube_c.csv testler/sube_cakisma.csv --ilk 0
Şube A: ornek_veri/ogrenciler.csv · 8 kayıt
Şube B: ornek_veri/sube_c.csv · 6 kayıt
Şube C: testler/sube_cakisma.csv · 3 kayıt
Birleşik: 16 kayıt (numara sırasında; çok yollu, öbek) · 27 karşılaştırma, 16 taşıma
ÇAKIŞMA: 1 numara birden çok şubede var: 2301010047
Süre: birleştirme 0.002 ms
[çıkış kodu: 1]
```

### 5.4 `listele`: öbek, sayma, taban

```
$ ./listele testler/kararlilik.csv --yontem hepsi
Dosya: testler/kararlilik.csv · kayıt: 8
Ölçüt: basari — YANO ↓, soyad ↑, ad ↑ (başarı sırası)
Yöntem        karşılaştırma        taşıma   kâhinle aynı   eşitler numara sırasında
araya                    23            31   EVET           EVET
Süre (araya): 0.004 ms
secmeli                  28            12   HAYIR          HAYIR
Süre (secmeli): 0.003 ms
kabarcik                 27            51   EVET           EVET
Süre (kabarcik): 0.002 ms
qsort                     -             -   EVET           EVET
Süre (qsort): 0.002 ms
cok_gecisli              52            77   EVET           EVET
Süre (cok_gecisli): 0.003 ms
birlestirmeli             15            48   EVET           EVET
Süre (birlestirmeli): 0.002 ms
hizli                    50            25   HAYIR          HAYIR
Süre (hizli): 0.009 ms
obek                     24            52   HAYIR          HAYIR
Süre (obek): 0.003 ms
sayma                    17            64   EVET           EVET
Süre (sayma): 0.003 ms
[çıkış kodu: 0]
```

## 6. Tasarım kararları

1. **Anahtar fonksiyonu, karşılaştırıcı değil.** Sayma ve taban sıralaması karşılaştırıcıyla çalışamaz; öğeden tamsayı anahtar çıkaran bir fonksiyon alırlar. Mini-OBS'de anahtarlar doğal olarak tamsayıdır (yuvarlanmış not, YANO × 100, ortalama × 500, numara).
2. **Sayma kararlıdır, çünkü yerleştirme girdi sırasıyla yapılır.** Bu özellik `dagilim --liste`'yi (eşit notlular numara sırasında), iki geçişli liste sıralamasını ve taban sıralamasının doğruluğunu taşır.
3. **Taban 256.** Bayt başına bir geçiş: 10 haneli numaralarda 4 geçiş, notlarda 1 geçiş. Taban 10'a göre geçiş sayısı az, kova dizisi (256 × 8 bayt) önbelleğe sığar. Geçiş sayısı en büyük anahtardan hesaplanır: gereksiz geçiş yapılmaz.
4. **Öbek sıralaması yerinde, ama varsayılan değil.** Θ(1) ek bellek ve Θ(n log n) en kötü durum güvencesi değerlidir (introsort'un yedeği budur); ama kararsızdır ve bu makinede en yavaş Θ(n log n) yöntemdir. Başarı listesinin varsayılanı birleştirmeli kalır.
5. **İlk-k tam sıralamayla.** Eşitlerin hangisinin listeye girdiği öbeğe bırakılmaz: ölçüt numarayla tamamlanır ve sonuç bütün listenin ilk k'sıyla aynıdır.
6. **Ders ortalaması tamsayı karşılaştırılır.** Kayan nokta eşitliğine dayanan sıralama tanımsız değil ama **kararsızdır** (anlamca): aynı ortalamalı iki öğrencinin sırası hesaplama yoluna bağlı olur. × 500 dönüşümü veri biçiminden (iki ondalık) gelen tam bir eşlemedir.
7. **Ölçüm düzeneği tek öğe türü kullanır.** Raporun dokuz algoritması aynı 16 baytlık (anahtar, indis) öğesini sıralar: karşılaştırma maliyeti (iki tamsayı) ve taşıma maliyeti (16 bayt) bütün yöntemlerde aynıdır; farklar algoritmadan gelir. Kararlılık, indis sağlamasıyla (kontrol) her ölçümde görünür.

## 7. Ölçümler (özet)

Ayrıntılı rapor: **`mini_obs_v2_6_olcum_raporu.md`** (yöntem, dokuz algoritmanın kimlik kartları, dört girdi türünde tablolar ve grafikler, büyüme eğimleri, karşılaştırma sayıları, kararlılık, anahtar aralığı, öbek uygulamaları, seçim rehberi, geçerlilik tehditleri). Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB, L3 33 MiB; gcc 13.3.0, glibc 2.39; tarih 2026-10-13 07:39; 1 ısınma + 5 tekrar, ortanca (10⁶'da 3 tekrar). `make olcum` 1 dakika 33 s sürdü. Ölçüm sırasında makinenin 1 dakikalık yük ortalaması başta 0,49, sonda 0,89 idi (2 çekirdek; başka işlerle paylaşıldı). Bu ölçümde 100 "kuram: UYUMLU", 0 uyumsuzluk.

| algoritma | karışık, 8 000 | sıralı, 8 000 | ters, 8 000 | çok tekrarlı, 8 000 | karışık, 10⁶ | sıralı, 10⁶ | ters, 10⁶ | çok tekrarlı, 10⁶ |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| seçmeli | 159,6 ms | 159,6 ms | 172,1 ms | 176,8 ms | — | — | — | — |
| kabarcık | 296,5 ms | 68,8 µs | 501,2 ms | 388,7 ms | — | — | — | — |
| araya ekleme | 105,4 ms | 171,9 µs | 159,7 ms | 77,0 ms | — | — | — | — |
| birleştirmeli | 1,1 ms | 399,6 µs | 420,1 µs | 984,6 µs | 273,1 ms | 118,0 ms | 160,2 ms | 230,0 ms |
| hızlı | 1,5 ms | 391,2 µs | 437,7 µs | 1,3 ms | 254,5 ms | 145,9 ms | 111,2 ms | 226,3 ms |
| öbek | 1,5 ms | 1,3 ms | 1,2 ms | 1,4 ms | 599,1 ms | 242,9 ms | 261,9 ms | 407,1 ms |
| sayma | 102,0 µs | 81,8 µs | 82,0 µs | 75,2 µs | 197,1 ms | 25,1 ms | 26,6 ms | 37,1 ms |
| taban (LSD) | 278,6 µs | 320,2 µs | 277,2 µs | 86,8 µs | 79,3 ms | 77,3 ms | 92,3 ms | 35,6 ms |
| qsort | 1,2 ms | 377,8 µs | 371,2 µs | 973,0 µs | 257,7 ms | 86,0 ms | 108,1 ms | 193,5 ms |

*Tablo 1. 16 baytlık öğelerin sıralanma süresi (ortanca): n = 8 000 (dokuz algoritma) ve n = 10⁶ (karesel üçlü hariç). Girdi türleri: karışık (öğrenci numaraları üreteç sırasında), sıralı, ters, çok tekrarlı (anahtar: yuvarlanmış ALG notu, 101 farklı değer).*

![Dört girdi türü](mini_obs_v2_6_olcum_girdiler.png)

*Şekil 4. Dokuz algoritma, dört girdi türü (log–log). Karesel üçlünün eğimi 2'ye, diğerlerininki 1'e yakındır; ölçülen eğimler ve önbellek etkisi: ölçüm raporu, Tablo 4.*

- **En hızlılar (n = 10⁶):** karışık girdide taban sıralaması — 79,3 ms; sıralı girdide sayma sıralaması — 25,1 ms; ters girdide sayma sıralaması — 26,6 ms; çok tekrarlı girdide taban sıralaması — 35,6 ms. n = 8 000'de sıralı girdinin en hızlısı kabarcık sıralaması — 68,8 µs: uyarlanabilir yöntemler sıralı girdide doğrusaldır.
- **Kararlılık** (çok tekrarlı girdi, n = 8 000, indis sağlaması): kabarcık, araya ekleme, birleştirmeli, sayma, taban (LSD), qsort aynı sağlamayı verir (kararlı); seçmeli, hızlı, öbek farklıdır (kararsız).

| K (anahtar aralığı) | sayma | taban | taban geçiş | birleştirmeli |
|--:|--:|--:|--:|--:|
| 10 | 1,2 ms | 1,4 ms | 1 | 13,6 ms |
| 100 | 1,3 ms | 1,4 ms | 1 | 16,0 ms |
| 1 000 | 1,4 ms | 2,0 ms | 2 | 17,4 ms |
| 10 000 | 1,4 ms | 2,0 ms | 2 | 25,1 ms |
| 100 000 | 2,5 ms | 2,7 ms | 3 | 18,5 ms |
| 1 000 000 | 9,2 ms | 3,2 ms | 3 | 18,9 ms |
| 10 000 000 | 105,0 ms | 2,9 ms | 3 | 25,1 ms |

*Tablo 2. Anahtar aralığının etkisi (n = 10⁵, anahtarlar [0, K) aralığında düzgün rastgele). Taban sıralamasının geçiş sayısı K'nın bayt uzunluğudur.*

| k (n = 100 000) | ilk-k (öbek) | karşılaştırma | kars. / n | bütün liste / ilk-k |
|--:|--:|--:|--:|--:|
| 1 | 7,5 ms | 99 999 | 1,00 | 51,4 |
| 10 | 6,3 ms | 100 457 | 1,00 | 61,1 |
| 100 | 7,3 ms | 108 207 | 1,08 | 52,5 |
| 1 000 | 18,7 ms | 194 593 | 1,95 | 20,5 |
| 10 000 | 171,1 ms | 882 331 | 8,82 | 2,2 |
| 100 000 | 681,0 ms | 3 119 378 | 31,19 | 0,6 |

*Tablo 3. Başarı listesinin ilk k'sı (öbek) ↔ bütün listenin birleştirmeli sıralanması (383,0 ms, n = 10⁵).*

| k şube (n = 10⁶) | süre | karşılaştırma | kars. / n | log₂ k |
|--:|--:|--:|--:|--:|
| 2 | 169,5 ms | 999 999 | 1,00 | 1,00 |
| 4 | 138,1 ms | 2 499 561 | 2,50 | 2,00 |
| 8 | 153,0 ms | 3 999 778 | 4,00 | 3,00 |
| 16 | 173,6 ms | 5 624 111 | 5,62 | 4,00 |
| 64 | 237,6 ms | 9 218 026 | 9,22 | 6,00 |

*Tablo 4. 10⁶ kaydın k şubeden çok yollu birleştirilmesi. Karşılaştırma ≈ n·log₂ k ile 2n·log₂ k arasındadır (süzmede düzey başına 1–2 karşılaştırma). Karşılaştırma için: iki işaretçili birleştirme 128,0 ms, uç uca ekleyip kayıtları sıralamak 881,2 ms.*

![Öbek uygulamaları](mini_obs_v2_6_olcum_obek.png)

*Şekil 5. Sol: anahtar aralığı K'nın sayma, taban ve birleştirmeli sıralamaya etkisi; sağ: ilk-k'nın k ile büyümesi ve bütün listenin sıralanması.*

## 8. Testler

- **Birim testleri** (`obs_test`): `245 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama + 26 sıralama + 23 böl-fethet + 19 öbek-doğrusal`. Öbek-doğrusal testleri: CLRS'nin öbek kurma örneği (sonuç ve elle izlenen 14 karşılaştırma, 17 taşıma), bozuk öbek, öbek sıralaması (CLRS 5 2 4 6 1 3: 16 karşılaştırma ≤ 36), (2, 0) (2, 1) (1, 2) dizisinde kararsızlık, 300 baytlık öğe; ilk-k (k < n, k > n, k = 0, n = 0; girdi değişmez); sayma (kararlı sıra, toplama n + K, taşıma n; azalan; yerinde: + n kopya; aralık dışı anahtar reddedilir ve dizi değişmez; sıklık); taban (en büyük anahtar 255 → 1 geçiş, 256 → 2, 0 → 0; kararlılık; sayaçlar); listelerde sayma (basari, alg) ve taban (no) = kâhin; uygunsuz yöntem reddi; kayan nokta eşitliği (AK, ZEN'den önce); çok yollu birleştirme (A + B + C = 20 kayıt), k = 2 = iki işaretçili birleştirme (aynı kayıtlar, aynı çakışma), k = 1.
- **Kâhin testleri** (`test_kahin`): 300 denemede 354 990, 1 000 denemede 1 172 771 denetim (öbek, sayma, taban, ilk-k, çok yollu: 14 355), uyuşmazlık yok.
- **Kasıtlı hatalar ve küçük kapsam araması.** (a) `--hata-goster lsd` — kararsız taban geçişi; küçük kapsam araması **yalnız anahtar sırasını** denetler, böylece "kararsız ama sıralı" değil "sıralı değil" örneği bulur:

```
$ ./test_kahin --hata-goster lsd
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : taban_sirala
  n          : 188
  Beklenen   : kararlı sıra (qsort + kimlik); 1 geçiş
  Bulunan    : FARKLI (kararlılık ya da sıra); 1 geçiş
  Girdi    = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), ...]
  Bulunan  = [(0, 80), (0, 79), (0, 78), (0, 77), (0, 76), (0, 75), (0, 74), (0, 73), (0, 72), (0, 71), (0, 70), (0, 69), ...]
  En küçük SIRALAMA hatası (2..6 öğe; anahtarlar 0, 1, 255, 256, 257; yalnız anahtar sırası; 2 öğe):
  Girdi    = [(257, 0), (256, 1)]
  Beklenen = [(256, 1), (257, 0)]
  Bulunan  = [(257, 0), (256, 1)]
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster lsd
[çıkış kodu: 1]
```

  (b) `--hata-goster suzme` — aşağı süzmede sağ çocuğun unutulması:

```
$ ./test_kahin --hata-goster suzme
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : obek_sirala
  n          : 188
  Beklenen   : öbek özelliği; sıralı anahtarlar; karşılaştırma ≤ 3008
  Bulunan    : öbek EVET; SIRALI DEĞİL; karşılaştırma 0
  Girdi    = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), ...]
  Bulunan  = [(0, 0), (1, 95), (0, 1), (1, 159), (0, 2), (1, 111), (0, 3), (1, 143), (0, 4), (1, 87), (0, 5), (1, 103), ...]
  En küçük karşı örnek (2..6 öğe, anahtarlar 0..4; 3 öğe):
  Girdi    = [(0, 0), (0, 1), (1, 2)]
  Bulunan  = [(0, 1), (1, 2), (0, 0)]
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster suzme
[çıkış kodu: 1]
```

- **Kararlılık sağlaması (ölçüm düzeneği):** çok tekrarlı girdide `kontrol`, eşit anahtarlıların sırasına duyarlıdır:

```
$ for y in secmeli kabarcik araya birlestirmeli hizli obek sayma taban qsort; do ./olcer kiyas_$y --sira tekrarli --n 2000 --tekrar 1; done      # süre satırları süzüldü
kiyas_secmeli n =     2000  kontrol = 994996964  sıra = tekrarli  sayaç: karşılaştırma 1999000 · toplama 0 · çarpma 0 · taşıma 5880
kiyas_kabarcik n =     2000  kontrol = 997514096  sıra = tekrarli  sayaç: karşılaştırma 1992330 · toplama 0 · çarpma 0 · taşıma 3002817
kiyas_araya n =     2000  kontrol = 997514096  sıra = tekrarli  sayaç: karşılaştırma 1002930 · toplama 0 · çarpma 0 · taşıma 1004937
kiyas_birlestirmeli n =     2000  kontrol = 997514096  sıra = tekrarli  sayaç: karşılaştırma 19359 · toplama 0 · çarpma 0 · taşıma 43904  üst sınır 19953: içinde
kiyas_hizli n =     2000  kontrol = 993472944  sıra = tekrarli  sayaç: karşılaştırma 32805 · toplama 0 · çarpma 0 · taşıma 23752  derinlik = 9
kiyas_obek n =     2000  kontrol = 992907721  sıra = tekrarli  sayaç: karşılaştırma 37695 · toplama 0 · çarpma 0 · taşıma 30136
kiyas_sayma n =     2000  kontrol = 997514096  sıra = tekrarli  sayaç: karşılaştırma 0 · toplama 2101 · çarpma 0 · taşıma 4000  kuram: UYUMLU  K = 101
kiyas_taban n =     2000  kontrol = 997514096  sıra = tekrarli  sayaç: karşılaştırma 0 · toplama 2256 · çarpma 0 · taşıma 4000  kuram: UYUMLU  geçiş = 1
kiyas_qsort n =     2000  kontrol = 997514096  sıra = tekrarli  sayaç: karşılaştırma 19359 · toplama 0 · çarpma 0
[çıkış kodu: 0]
```

- **Bellek:** `make asan` temiz (yeni programlar; `olcer`'in bütün yeni işlemleri n = 1, 2, 3, 300, dört girdi türü ve K = 1, 2, 255, 256, 70 000 ile; çok yollu birleştirme k = 1, 2, 3, 64); `make valgrind`: 13 çalıştırmanın 13 tanesinde "0 errors", 13 tanesinde "All heap blocks were freed".

## 9. Ders notu için özet (Hafta 7 · Mini-OBS 2 adımı · ara proje)

**Bu hafta:** Öbeği ve karşılaştırmasız sıralamayı Mini-OBS'ye ekliyoruz: not dağılımı (sayma), başarı listesinin ilk-k'sı (öbek), öğrenci numarasına taban sıralaması ve k şubenin birleştirilmesi (öbek). Ara projede v2.3–v2.6'nın bütün sıralama yöntemlerini aynı düzenekte ölçüp bir **ölçüm raporu** yazıyoruz (yönerge: `../ARA_PROJE_YONERGESI.md`).

### Gereksinimler

- `obek.h/.c`: `asagi_suz_say`, `obek_kur_say` (aşağıdan yukarıya), `obek_sirala_say`, `ilk_k_say`; değişmez yorumları; v2.4 arayüzü ve sayaçları.
- `dogrusal.h/.c`: `sayma_sirala_say` (kararlı; artan ve azalan; aralık dışı anahtarda false), `taban_sirala_say` (LSD, taban 256, geçiş sayısı en büyük anahtardan).
- `dagilim` programı: aralık tablosu (genişlik seçilebilir), ortanca, en sık not, `--liste K` (kararlı sayma), `--denetle`.
- `ilk_k` programı: ölçüte göre ilk K (öbek, Θ(n log k)), numarayla tamamlanmış ölçüt, `--denetle`.
- `listele`'ye `obek`, `sayma` (basari/alg/mat/fiz; iki kararlı geçiş), `taban` (no).
- Testler: elle izlenen sayaçlar (öbek kurma), kararlılık (sayma, taban), kâhinler (qsort + kimlik; bütün liste; uç uca + qsort).
- Ölçüm raporu: dokuz algoritma × dört girdi türü × n (karesel üçlü ≥ 8 000'e, diğerleri ≥ 10⁶'ya kadar); tablolar, log–log grafikler, eğim ve kuramla karşılaştırma, kararlılık sağlaması, anahtar aralığı deneyi, seçim rehberi, makine bilgisi, sınırlılıklar.

### İpuçları

- Öbekte indisleri kâğıtta çizin: 0 tabanlı dizide çocuklar 2i + 1 ve 2i + 2; son iç düğüm ⌊n/2⌋ − 1.
- Aşağı süzmede iki çocuğu da karşılaştırın; sağ çocuk yoksa (2i + 2 ≥ m) yalnız sol çocuk.
- Kurma döngüsünü `size_t` ile geriye doğru yazarken `for (size_t i = n / 2; i-- > 0; )` kalıbını kullanın (i ≥ 0 koşulu işaretsizde hep doğrudur).
- Sayma sıralamasında önek toplamını "İLK konum" olarak tutun ve girdiyi **baştan sona** dolaşın: kararlılık buradadır. Sondan başa dolaşacaksanız "son konum" tutmalısınız.
- Taban sıralamasında tampon ile diziyi her geçişte değiştirin; tek sayıda geçişte sonucu diziye geri kopyalamayı unutmayın.
- İlk-k için öbeğin kökü "seçilenlerin en kötüsü" olmalıdır: başarı listesinde kökte en DÜŞÜK başarılı durur.
- Kayan nokta değerleri `==` ile eşitlik için karşılaştırmayın; iki ondalıklı veriyi tamsayıya çevirip karşılaştırın.
- Rapor için önce CSV'yi üretin, tabloları ve grafikleri betikle oluşturun: sayıları elle kopyalamayın.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri ve `test_kahin` (300 deneme) geçer.
2. Öbek kurma 4 1 3 2 16 9 10 14 8 7 → 16 14 10 8 7 9 3 2 4 1; öbek sıralaması (2,0) (2,1) (1,2) dizisini (1,2) (2,1) (2,0) yapar (kararsız).
3. Sayma sıralaması anahtarlar 3 1 2 1 0 3 için kimlikleri 4 1 3 2 0 5 sırasında verir (kararlı); `toplama` n + K = 10.
4. Taban sıralaması en büyük anahtar 255 iken 1, 256 iken 2 geçiş yapar; 10 haneli öğrenci numaralarında 4 geçiş (`olcer kiyas_taban`: "geçiş = 4", "kuram: UYUMLU").
5. `dagilim ornek_veri/ogrenciler.csv --liste 5 --denetle`: ortanca 77,5; liste EMRE ÇINAR, İSMAİL ÖZTÜRK, CAN YILMAZ, AYŞE NUR YILMAZ, ZEYNEP ÇELİK; "Kâhin … AYNI"; çıkış 0.
6. `ilk_k ornek_veri/ogrenciler.csv --k 3 --denetle`: 2301010050, 2301010045, 2301010048; "AYNI"; çıkış 0.
7. `birlestir` A + B + C: 20 kayıt numara sırasında, ilk kayıt 2301010040; A + C + çakışma dosyası: "ÇAKIŞMA: 1 numara … 2301010047", çıkış 1.
8. `listele testler/kararlilik.csv --yontem hepsi`: birlestirmeli ve sayma "EVET / EVET"; obek, hizli ve secmeli "HAYIR / HAYIR".
9. İki kayıtlık eşit ortalama dosyasında (bölüm 4.7) `listele --olcut alg` AK'yi ZEN'den önce verir.
10. Kendi makinenizde 10⁶ karışık numarada taban sıralaması birleştirmeli sıralamadan hızlıdır (bu makinede 3,4 kat); n = 10⁵'te ilk-10, bütün listeyi sıralamaktan en az 10 kat hızlıdır (bu makinede 61 kat).
11. `--hata-goster lsd` ve `--hata-goster suzme` uyuşmazlığı ve en küçük karşı örneği basar, 1 ile çıkar; `make asan` temizdir.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | öbek kur: 4 1 3 2 16 9 10 14 8 7 | 16 14 10 8 7 9 3 2 4 1; 14 karşılaştırma |
| 2 | öbek sırala: 5 2 4 6 1 3 | 1 2 3 4 5 6; 16 karşılaştırma |
| 3 | ilk-3: 5 1 9 3 7 2 | 1 2 3; girdi değişmez |
| 4 | sayma: (3,a) (1,b) (2,c) (1,d) (0,e) (3,f), K = 4 | e b d c a f; azalan: a f c b d e |
| 5 | sayma, anahtar 7 ≥ K = 4 | false; dizi değişmez |
| 6 | taban: 255, 3, 255, 0 | 0 3 255 255 (kimlik sırası korunur); 1 geçiş |
| 7 | taban: 257, 256 (kararsız geçişle) | 257, 256 — YANLIŞ (`--hata-goster lsd`) |
| 8 | `dagilim ... --genislik 0` | kullanım iletisi; çıkış 2 |
| 9 | `listele ... --olcut soyad --yontem sayma` | "uygulanamaz"; çıkış 2 |
| 10 | `birlestir` A + B + C | 20 kayıt; çok yollu |
| 11 | `birlestir` A + B `--yontem obek` | iki işaretçiyle aynı liste ve sayılar |
| 12 | ALG: ZEN (3, 0) ↔ AK (0, 2) | AK önce (eşit ortalama, soyad) |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.5'iniz (ya da referans v2.5), `obek.h` ve `dogrusal.h` (bildirimler, sözleşmeler), `ornek_veri/sube_c.csv`, `olcer`'in `kiyas_*` ölçüm düzeneği (öğe türü, girdi türleri, kontrol sağlaması), ara proje yönergesi ve rapor şablonu.
- **Yazılır:** `obek.c`, `dogrusal.c`, `dagilim.c`, `ilk_k.c`; `sube.c`'ye çok yollu birleştirme; `liste.c`'ye üç yöntem; testler; ölçüm raporu.
- **Değiştirilmez:** v1.0 kuralları, kayıt dizisinin numara sırası, önceki sürümlerin yöntemleri (kâhin olarak kalırlar), ortak modüller.
- **Meydan okuma:** (a) introsort: hızlı sıralamada derinlik 2⌊log₂ n⌋'yi aşınca öbek sıralamasına, küçük parçalarda araya eklemeye geçen **melez** sıralama; (b) taban 2¹⁶ ile iki geçişli taban sıralaması ve önbellek etkisinin ölçümü; (c) MSD taban sıralamasıyla soyadlarının (UTF-8) sıralanması; (d) d-li öbek (d = 4) ile ilk-k ve çok yollu birleştirmenin yeniden ölçülmesi.

## 10. Bilinen sınırlılıklar

- Sayma sıralaması anahtar aralığı K için Θ(K) bellek ayırır; K ≫ n olduğunda (ör. numaraların kendisi, K ≈ 2,4·10⁹) kullanılamaz. `listele --yontem sayma` bu yüzden yalnızca küçük aralıklı ölçütlerde açıktır.
- Taban sıralaması yalnızca negatif olmayan tamsayı anahtarlarla çalışır; dizgi anahtarlar (soyad) için MSD varyantı gerekir (meydan okuma).
- Öbek sıralaması kararsızdır ve bu makinede önbellek davranışı yüzünden Θ(n log n) yöntemlerin en yavaşıdır.
- Ölçüm raporundaki öğeler 16 baytlıktır; büyük kayıtlarda taşıma maliyeti (ör. öbek sıralamasının takasları) farklı bir sıralama verebilir (v2.3–v2.4 bulguları).
- Süreler tek ve paylaşılan bir sanal makinede ölçüldü; sayaçlar makineden bağımsızdır.

## 11. Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Floyd, R. W. (1964). Algorithm 245: Treesort 3. *Communications of the ACM, 7*(12), 701.
- Knuth, D. E. (1998). *The art of computer programming: Vol. 3. Sorting and searching* (2nd ed.). Addison-Wesley.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
- Williams, J. W. J. (1964). Algorithm 232: Heapsort. *Communications of the ACM, 7*(6), 347–348.
