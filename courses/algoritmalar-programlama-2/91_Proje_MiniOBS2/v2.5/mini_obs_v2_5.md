# Mini-OBS 2 v2.5 — Böl ve Fethet: toplu yükleme, sıralayarak yinelenen tespiti, şube birleştirme ve ortanca (Hafta 6)

**Bu sürümün amacı:** Hafta 6'nın böl ve fethet algoritmalarını — **birleştirmeli sıralama**, **hızlı sıralama** ve **quickselect** — Mini-OBS'nin dört somut sorununa uygulamak: (1) yükleyici, kayıtları önce okuyup sonra (numara, satır) anahtarlarını birleştirmeli sıralamayla sıralar ve komşuları karşılaştırarak mükerrer numarayı bulur: v2.0'da ≈ 1,6 saat kestirilen 10⁶ kayıtlık yükleme bu makinede **2,28 s** sürer (ortanca; en az 2,24 s); (2) yinelenen numara tespiti O(n²)'den O(n log n)'e iner: 10⁵ kayıtta v2.1'in 4,33 s süren tüm çiftler taraması 23,1 ms'ye düşer (187 kat), sonuç aynıdır; (3) iki şubenin numara sırasındaki listeleri birleştirmenin **birleştir** adımıyla Θ(nA + nB)'de birleşir; (4) ders ortalamalarının **ortancası** sıralamadan, quickselect ile ortalama doğrusal zamanda bulunur. Her yeni algoritma rastgele girdilerde bir kâhine (qsort, v2.1, v1.0 yükleyicisi, uç uca ekleme + sıralama) karşı sınanır; iki tipik hata (birleştirmede kuyruğu unutmak, Hoare bölümlemesinin dönüş indisini pivotun yeri sanmak) kâhinle yakalanır ve 1..7 öğeli bütün girdiler denenerek en küçük karşı örnekleri bulunur.

Dosyalar (satır sayılarıyla): `bolfethet.h` (66) · `bolfethet.c` (324) · `sube.h` (27) · `sube.c` (48) · `birlestir.c` (218) · `ortanca.c` (156) · `yinelenen.h` (57) · `yinelenen.c` (183) · `denetle.c` (188) · `dosya.h` (106) · `dosya.c` (544) · `liste.h` (95) · `liste.c` (270) · `listele.c` (205) · `olcer.c` (1352) · `test_obs.c` (1589) · `test_kahin.c` (2244) · `main.c` (342) · `arama.h` (120) · `arama.c` (258) · `ara.c` (232) · `obs.h` (141) · `obs.c` (673) · `turkce.h` (51) · `turkce.c` (135) · `siralama.h` (47) · `siralama.c` (141) · `sayac.h` (49) · `sayac.c` (21) · `metin.h` (35) · `metin.c` (340) · `secmeli.h` (102) · `secmeli.c` (330) · `ders_sec.c` (184) · `uretec.h` (54) · `uretec.c` (160) · `veri_uret.c` (94) · `deney.h` (28) · `deney.c` (32) · `ortak_rastgele.h` (43) · `ortak_rastgele.c` (50) · `zamanlayici.h` (34) · `zamanlayici.c` (63) · `Makefile` (316) · `ornek_veri/sube_b.csv` (B şubesi, 6 kayıt), `testler/sube_cakisma.csv` (A ile çakışan numara) ve önceki sürümlerin test girdileri · `olcum/yukleme.csv`, `olcum/yinelenen.csv`, `olcum/siralama.csv`, `olcum/sube.csv`, `olcum/ortanca.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_5_ciktilar.txt` (1086 satır, gerçek çıktılar). Şekiller: `mini_obs_v2_5_agac.png`, `mini_obs_v2_5_toplu.png`; grafikler: `mini_obs_v2_5_olcum_yukleme.png`, `mini_obs_v2_5_olcum_siralama.png`.

Derleme: `make` (`mini_obs`, `veri_uret`, `olcer`, `denetle`, `ders_sec`, `ara`, `listele`, **`ortanca`**, **`birlestir`**), `make test`, `make olcum` (bu makinede 2 dakika 20 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 27 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0, 1 (dosya okunamadı, bellek yetersiz, şubelerde çakışma, yinelenen numara var ya da `--denetle` uyuşmazlık buldu; testlerde uyuşmazlık), 2 (hatalı kullanım).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 6'nın sorusu: bir problemi yarıya bölüp parçaları ayrı ayrı çözmek ve sonra birleştirmek, işi neden n²'den n log n'e indirir? Mini-OBS'de bu sorunun dört yanıtı vardır:

- **Böl, fethet, birleştir** (ÖÇ 6.1–6.2): iki sıralı diziyi doğrusal zamanda birleştiren `birlestir_genel`, onun üstüne kurulan birleştirmeli sıralama (yukarıdan aşağıya ve aşağıdan yukarıya) ve aynı adımın doğrudan uygulaması olan **şube birleştirme**. Özyineleme ağacı (Şekil 1) T(n) = 2T(n/2) + Θ(n) bağıntısını görünür kılar: her düzeyde Θ(n) iş, ⌈log₂ n⌉ düzey (ÖÇ 6.4).
- **Bölümleme ve pivot** (ÖÇ 6.3): Hoare bölümlemeli hızlı sıralama, üçün ortancası pivot, küçük parçaya özyineleme (derinlik ≤ ⌊log₂ n⌋ + 1). Lomuto ile Hoare arasındaki fark — dönen indis pivotun yeri midir? — kâhinle sınanan bir hata olarak (`--hata-goster hoare`).
- **Seçim** (ÖÇ 6.5): ortanca, k. küçük öğedir; quickselect yalnızca k'yı içeren parçaya iner ve ortalama Θ(n)'de biter. Kâhin sıralamadır: Ω(n log n) alt sınırı olan bir işi, Θ(n)'lik bir işin doğruluğunu sınamak için kullanırız.
- **Mühendis gözüyle — algoritmayı darboğaza uygula:** v2.3, karşılaştırmaları 3 081 kat azaltmış ama yüklemeyi hızlandıramamıştı: darboğaz kaydırmaydı (≈ n²/4 kayıt taşıma). v2.5 aynı sonucu (numara sırasında, mükerrersiz kayıt dizisi ve v1.0 ile aynı hata satırı) başka bir sırayla üretir: önce hepsini oku, sonra **bir kez** sırala, sonra **bir kez** taşı.

Yol haritasındaki karşılığı (Tablo A.1): **H6 · v2.5 · Büyük veri sıralama; şube listelerini birleştirme; ortanca not; O(n log n) yinelenen tespiti · Birleştirmeli sıralama, quickselect.** Yinelenen tespiti sarmalının ikinci basamağıdır: H2 (v2.1) tüm çiftler O(n²) → **H6 (v2.5) sırala + komşuları karşılaştır O(n log n)** → H10 (v2.9) karma tablosu, ortalama O(n). v2.1, v2.5'in kâhinidir.

## 2. v2.4'ten ne değişti?

| Konu | v2.4 (H5) | v2.5 (H6) |
|---|---|---|
| Böl ve fethet | — | **`bolfethet.h/.c`**: `birlestir_genel`, `birlestirmeli_sirala_say` (tek tampon), `birlestirmeli_asagidan_say`, `hizli_sirala_say` (Hoare, üçün ortancası, derinlik), `k_inci_kucuk` (üç yollu bölümleme), `ortanca_quickselect` |
| Yükleyici (`sinif_yukle`) | SIRALI kip (v2.3): ikili arama + kaydırma, Θ(n²) taşıma | **TOPLU kip**: oku → (numara, satır) anahtarlarını kararlı sırala → komşuları karşılaştır → bir kez taşı; Θ(n log n). v1.0 ile aynı hata satırı |
| Yinelenen tespiti | tüm çiftler (v2.1) | + **`yinelenen_bul_siralama`**, `yinelenen_var_mi_siralama` (aynı çiftler, aynı sıra); `denetle --yontem siralama|ciftler` (varsayılan siralama) |
| Şubeler | — | **`sube.h/.c`**: `sube_birlestir` (çakışma bildirimi); **`birlestir`** programı (`--olcut no|basari`, `--cikti`) |
| Ortanca | — | **`ortanca`** programı: üç dersin ortancası, `--denetle` (kâhin: sıralama) |
| `listele` | 5 yöntem, varsayılan araya ekleme | + `birlestirmeli` (**varsayılan**), `hizli` |
| `olcer` | sıralama, arama, yükleme | + `anahtar_birlestirmeli/asagidan/hizli/qsort`, `liste_birlestirmeli/hizli`, `yinelenen_siralama`, `yukleme_toplu`, `sube_birlestir/sirala`, `ortanca_quickselect/siralama`; kuramla otomatik karşılaştırma |
| Testler | 203 birim; kâhin 345 505 | 226 birim (+23 böl-fethet); kâhin 350 751 denetim; `--hata-goster kuyruk`, `--hata-goster hoare` (en küçük karşı örnekle) |

Menü değişmedi; `mini_obs` yalnızca yükleyicisi yenilenmiş hâliyle çalışır. v1.0'ın T2 oturumu yine yalnızca başlık ve arama istemi satırlarında farklıdır (çıktılar dosyası, regresyon bölümü).

## 3. Mimari

| Modül / program | Sorumluluk | Bağımlılık |
|---|---|---|
| `bolfethet` (**yeni**) | birleştirme, iki birleştirmeli sıralama, hızlı sıralama, quickselect, ortanca | yalnız `sayac` ve `siralama.h`'deki `Karsilastirici` türü: öğe türünü bilmez |
| `sube` (**yeni**) | numara sırasındaki iki sınıfın birleştirilmesi, çakışmalar | `obs`, `sayac` |
| `dosya` | + TOPLU kip (`toplu_bitir`, satır numaraları) | + `bolfethet` |
| `yinelenen` | + sıralayarak tespit (`NoIndis` anahtarları, gruplar) | + `bolfethet` |
| `liste` | + `SIRALA_BIRLESTIRMELI`, `SIRALA_HIZLI` | + `bolfethet` |
| `ortanca.c`, `birlestir.c` (**yeni**) | komut satırı araçları | `bolfethet`, `sube`, `liste`, `dosya` |
| diğerleri | v2.4'ten aynen (yorum güncellemeleri dışında) | — |

`bolfethet.o` çekirdek nesne grubundadır (`CEKIRDEK`): yükleyici onu kullandığı için her program onunla bağlanır. `bolfethet` v2.4'ün `siralama` modülüyle aynı arayüzdedir — `(taban, n, boyut, kars, Sayac *)` — ve aynı sayaç tanımlarını kullanır (karşılaştırma = karşılaştırıcı çağrısı; taşıma = öğe kopyası). Böylece v2.4'ün üç karesel algoritması ile v2.5'in Θ(n log n) algoritmaları aynı tabloda karşılaştırılabilir.

## 4. Algoritmalar

### 4.1 Birleştirme ve birleştirmeli sıralama

```
algoritma BİRLEŞTİR(A[0..na−1], B[0..nb−1]) → C          ▷ A ve B sıralı
    i ← 0; j ← 0; k ← 0
    i < na ve j < nb olduğu sürece                   ▷ değişmez: C[0..k−1] = A[0..i−1] ∪ B[0..j−1], sıralı
        eğer B[j] < A[i] ise C[k] ← B[j]; j ← j + 1
        değilse               C[k] ← A[i]; i ← i + 1   ▷ eşitte A'dan: KARARLI
        k ← k + 1
    kalan A[i..] ve B[j..] C'ye kopyalanır            ▷ en çok na + nb − 1 karşılaştırma

algoritma BİRLEŞTİRMELİ-SIRALA(a[lo..hi−1], t)          ▷ t: TEK paylaşılan tampon
    eğer hi − lo < 2 ise dön                          ▷ 0 ya da 1 öğe: sıralı
    orta ← lo + (hi − lo) / 2                         ▷ böl
    BİRLEŞTİRMELİ-SIRALA(a[lo..orta−1]); BİRLEŞTİRMELİ-SIRALA(a[orta..hi−1])   ▷ fethet
    t[lo..hi−1] ← a[lo..hi−1]; a[lo..hi−1] ← BİRLEŞTİR(t[lo..orta−1], t[orta..hi−1])   ▷ birleştir
```

![Birleştirmeli sıralamanın özyineleme ağacı](mini_obs_v2_5_agac.png)

*Şekil 1. 5 2 4 6 1 3 dizisinde birleştirmeli sıralama (Cormen vd., 2022'nin örneği; `bolfethet.c` ile aynı bölme kuralı). Üstte bölme, altta birleştirme düzeyleri; her birleştirmenin yanında karşılaştırma sayısı. Toplam 11 karşılaştırma ve 32 taşıma birim testinde programın sayaçlarıyla doğrulanır.*

**Çözümleme.** T(n) = T(⌊n/2⌋) + T(⌈n/2⌉) + Θ(n): özyineleme ağacının her düzeyinde toplam iş Θ(n), düzey sayısı ⌈log₂ n⌉ → Θ(n log n), **her girdide** (ana teoremin a = b = 2, f(n) = Θ(n) durumu). Kesin sayaçlar (programla ve kâhinle doğrulandı):

- **Karşılaştırma:** en çok n⌈log₂ n⌉ − 2^⌈log₂ n⌉ + 1 (Knuth, 1998). Sıralı girdide her birleştirme yalnızca A'nın boyu (⌊m/2⌋) kadar, ters girdide B'nin boyu (⌈m/2⌉) kadar karşılaştırır; ikisi de ≈ (n/2) log₂ n'dir. Örnek: n = 1 000 sıralı girdide 4 932 karşılaştırma (`olcer`, "kuram: UYUMLU").
- **Taşıma:** her iç düğümde m öğe tampona ve m öğe geri: T(n) = T(⌊n/2⌋) + T(⌈n/2⌉) + 2n, n = 2^k için 2n log₂ n. Girdiden bağımsızdır.
- **Bellek:** Θ(n) ek bellek; tampon **bir kez** ayrılır ve bütün özyineleme boyunca paylaşılır (her çağrıda `malloc` yapmak hem yavaştır hem bellek parçalar). Özyineleme derinliği ⌈log₂ n⌉.

**Aşağıdan yukarıya sürüm** (`birlestirmeli_asagidan_say`): genişlik 1, 2, 4, … olan ardışık parçaları birleştirir; tampon ile dizi her geçişte yer değiştirir ("ping-pong"), bu yüzden her geçişte n taşıma yapılır (yukarıdan aşağıya sürümün 2n'si yerine). Sonuç aynıdır; ölçümde bu fark görünür (bölüm 7.4).

**Hata Avcısı — hangi kuyruk gerekli?** Yukarıdaki düzende `t`'den `a`'ya birleştirirken B'nin kalanı **zaten son yerindedir**: A biterse k = j olur ve a[j..hi−1] B'nin kalanının kopyasıdır. A'nın kalanı ise kopyalanmazsa kaybolur. `--hata-goster kuyruk` A'nın kalanını unutan sürümü kâhine verir; kâhin en küçük karşı örneği bulur: **[2, 1] → [1, 1]** (bölüm 8).

### 4.2 Hızlı sıralama

```
algoritma HIZLI(a[lo..hi])                          ▷ kapalı aralık
    lo < hi olduğu sürece
        p ← ÜÇÜN-ORTANCASI(a[lo], a[orta], a[hi])     ▷ pivot DEĞERİ (kopya)
        j ← HOARE-BÖLÜMLE(a, lo, hi, p)             ▷ son koşul: a[lo..j] ≤ p ≤ a[j+1..hi], lo ≤ j < hi
        eğer j − lo < hi − j ise HIZLI(a[lo..j]); lo ← j + 1     ▷ KÜÇÜK parçaya özyineleme,
        değilse                 HIZLI(a[j+1..hi]); hi ← j        ▷ büyüğüne döngü
algoritma HOARE-BÖLÜMLE(a, lo, hi, p)
    i ← lo; j ← hi
    sonsuz döngü
        a[i] < p olduğu sürece i ← i + 1            ▷ eşitte DURUR
        a[j] > p olduğu sürece j ← j − 1            ▷ eşitte DURUR
        eğer i ≥ j ise j'yi döndür
        a[i] ↔ a[j]; i ← i + 1; j ← j − 1
```

- **Pivot:** üçün ortancası, sıralı ve ters girdide bölmeyi tam ortadan yapar (en kötü durum Θ(n²) bu girdilerde oluşmaz); karışık girdide rastgele pivottan biraz daha dengelidir. Bu düzende en kötü durum yine vardır (ortancayı bozan özel girdiler); bunu sınırlamanın yolu introsort'tur (H7, öbek sıralamasıyla).
- **Eşit anahtarlar:** iki işaretçi de pivota eşit öğede durur ve takas eder: hepsi eşit bir dizide bile bölme ortadan olur (birim testi: 1 000 eşit öğe, derinlik ≤ 10).
- **Derinlik:** özyineleme her zaman **küçük** parçaya yapılır; küçük parça en çok yarı boydadır, bu yüzden derinlik ≤ ⌊log₂ n⌋ + 1 (Sedgewick, 1978). Ölçüm: n = 10⁵ karışık girdide derinlik 13, sıralı girdide 17 (= ⌊log₂ n⌋ + 1: bölmeler tam ortadan olduğunda sınıra ulaşılır).
- **Kararsızdır:** uzak takaslar eşit öğelerin sırasını bozar. `testler/kararlilik.csv`'de üç ECE KAYA kaydı …062, …061, …066 sırasına düşer (bölüm 5.4). Başarı listesinin varsayılanı bu yüzden birleştirmeli sıralamadır.
- **Hata Avcısı — Lomuto mu, Hoare mu?** Lomuto bölümlemesi pivotu son yerine koyar ve onun indisini döndürür: özyineleme [lo, p−1] ve [p+1, hi]'ye yapılır. Hoare'un döndürdüğü j ise pivotun yeri **değildir**; doğru özyineleme [lo, j] ve [j+1, hi]'dir. İki alışkanlığı karıştıran sürüm (`--hata-goster hoare`) a[j]'yi hiç yerleştirmez; en küçük karşı örnek **[2, 3, 1] → [2, 1, 3]**.

### 4.3 Quickselect ve ortanca

```
algoritma K-İNCİ-KÜÇÜK(a[0..n−1], k)               ▷ ön koşul: k < n
    lo ← 0; hi ← n − 1
    lo < hi olduğu sürece                           ▷ değişmez: aranan sıra a[lo..hi] içinde
        p ← ÜÇÜN-ORTANCASI(a[lo], a[orta], a[hi])
        a[lo..hi]'yi üçe böl: < p | = p | > p        ▷ Hollanda bayrağı (Dijkstra, 1976)
        eğer k < lt ise hi ← lt − 1
        değilse eğer k > gt ise lo ← gt + 1
        değilse p'yi döndür                         ▷ a[lt..gt] = p ve k bu aralıkta
    a[k]'yı döndür
```

Ortanca: n tekse sıralı dizinin (n − 1)/2. öğesi; çiftse (n/2 − 1). ve (n/2). öğelerin ortalaması. Çift n'de önce alt ortanca bulunur; quickselect'in son koşulu (a[k+1..n−1] ≥ a[k]) sayesinde üst ortanca, sağ parçanın **en küçüğüdür**: bir doğrusal tarama yeter. İşlev diziyi değiştirmemek için kopya üzerinde çalışır. Beklenen maliyet Θ(n)'dir: bölmeler dengeli olsaydı n + n/2 + n/4 + … < 2n öğe ziyareti. Rastgele pivotla ortanca için beklenen karşılaştırma ≈ 2(1 + ln 2)n ≈ 3,39n'dir (Knuth, 1971; iki yollu bölümleme). Burada üç yollu bölümleme kullanılır: öğe başına 1 ya da 2 karşılaştırma, ama pivota eşit **bütün** öğeler tek turda elenir — ders ortalamaları gibi çok tekrarlı veride önemlidir. Ölçülen karşılaştırma n'nin 4,4–6,2 katıdır (bölüm 7.6).

### 4.4 Toplu yükleme

![Toplu yükleme](mini_obs_v2_5_toplu.png)

*Şekil 2. Toplu yükleme, iki mükerrer numaralı küçük bir dosyada (bölüm 5.1'deki `mukerrer.csv`). Anahtarlar kararlı sıralandığı için eşit numaralar dosya sırasında yan yana gelir; her grubun ikinci öğesi, numaranın ikinci kez görüldüğü satırdır. Raporlanan satır (5) programın çıktısından doğrulanmıştır.*

1. Bütün satırlar v1.0 kurallarıyla, **mükerrer denetimi yapılmadan** okunur; her kaydın dosya satırı ayrı bir dizide tutulur. Bozuk bir satırda (satır L) okuma durur.
2. (numara, indis) anahtarları (16 bayt) birleştirmeli sıralamayla **kararlı** sıralanır: 144 baytlık kayıtlar değil anahtarlar taşınır.
3. Komşu anahtarlar karşılaştırılır (n − 1). Her eşit grubun ikinci öğesinin satırı bir **ikinci geçiştir**; v1.0'ın raporladığı satır bunların en küçüğüdür, çünkü v1.0 dosyayı sırayla okur ve ilk ikinci geçişte durur. Bozuk satır varsa ondan önceki kayıtlar arasında mükerrer aranır; yoksa bozuk satır raporlanır — v1.0 ile **aynı durum, aynı satır** (birim testleri ve kâhin, kopyalanmış numaralar ve araya konmuş bozuk satırlarla).
4. Mükerrer yoksa kayıtlar sıralı yerlerine **bir kez** taşınır (n kayıt kopyası).

Toplam: Θ(n) okuma + Θ(n log n) anahtar sıralaması + (n − 1) karşılaştırma + n taşıma. 10⁶ kayıtta 19 673 895 karşılaştırma ve 40 902 848 taşıma (anahtarların ve kayıtların), v1.0'ın 499 999 500 000 karşılaştırmasına karşı. Sonuç v2.3'ün SIRALI kipiyle **bayt bayt aynıdır** (birim testi). İkili (`.dat`) dosyada da aynı kip kullanılır.

### 4.5 Sıralayarak yinelenen tespiti ve şube birleştirme

`yinelenen_bul_siralama`, (numara, indis) anahtarlarını kararlı sıralar, grupları ve her kaydın sıralı dizideki yerini (`konum`) çıkarır. Çiftler, her i için i'nin grubunda ondan **sonra** gelen indisler yazılarak üretilir: sözlük sırası (önce i, sonra j) v2.1'inkiyle aynıdır. Toplam çift sayısı Σ C(g, 2)'dir (g: grup boyu). Maliyet Θ(n log n + P) (P: yazılan çift sayısı); karşılaştırma = sıralamanınkiler + (n − 1).

`sube_birlestir`, birleştirme adımının kayıt düzeyindeki hâlidir: iki işaretçi, her adımda küçük numaralı kayıt; aynı numara iki şubede de varsa (veri hatası) A'nın kaydı **bir kez** girer ve numara çakışma listesine yazılır. Adım başına bir üç yollu karşılaştırma sayılır: en çok nA + nB − 1 karşılaştırma, nA + nB − (çakışma) taşıma. Başarı listelerinin birleştirilmesinde (`birlestir --olcut basari`) her şubenin listesi birleştirmeli sıralanır ve iki liste `birlestir_genel` ile birleşir; öğe, şube etiketini taşıyan küçük bir yapıdır (ilk üyesi kayıt işaretçisi olduğu için `liste.h` karşılaştırıcıları onda da çalışır).

### 4.6 Kâhinler

| Sınanan | Kâhin |
|---|---|
| iki birleştirmeli sıralama, hızlı sıralama | `qsort`; beş girdi türü (sıralı, ters, çok tekrarlı, az tekrarlı, organ borusu); karşılaştırma üst sınırı, taşıma tanımdan, derinlik ≤ ⌊log₂ n⌋ + 1 |
| kararlılık | (anahtar, kimlik) çiftlerinde `qsort` + kimlik |
| `birlestir_genel` | iki sıralı listeyi uç uca ekleyip kararlı sıralamak |
| `k_inci_kucuk`, `ortanca_quickselect` | sıralı kopyanın k. öğesi ve ortası; son koşul (solda ≤, sağda ≥), çoklu kümenin korunması |
| `yinelenen_bul_siralama`, `yinelenen_var_mi_siralama` | v2.1 `yinelenen_bul`, `yinelenen_var_mi`: aynı çiftler, aynı sıra, aynı ilk çift |
| TOPLU yükleyici | v1.0 `csv_oku` + `qsort`; aynı durum ve satır (kopyalanmış numara, araya konmuş bozuk satır) |
| `sube_birlestir` | uç uca ekleme + `qsort`; beklenen çakışma listesi |

## 5. Kullanım

### 5.1 Toplu yükleme (`mini_obs`, `ara`)

İki mükerrer numaralı dosyada v2.5 ve v1.0 aynı satırı raporlar:

```
$ printf 'no;ad;soyad;ALG_vize;ALG_final;MAT_vize;MAT_final;FIZ_vize;FIZ_final\n30;CAN;KAYA;70;85;90;95;40;60\n10;ECE;ÖZ;70;85;90;95;40;60\n20;ALİ;AK;70;85;90;95;40;60\n10;NUR;ER;70;85;90;95;40;60\n30;DEFNE;ŞEN;70;85;90;95;40;60\n' > mukerrer.csv; cat mukerrer.csv
no;ad;soyad;ALG_vize;ALG_final;MAT_vize;MAT_final;FIZ_vize;FIZ_final
30;CAN;KAYA;70;85;90;95;40;60
10;ECE;ÖZ;70;85;90;95;40;60
20;ALİ;AK;70;85;90;95;40;60
10;NUR;ER;70;85;90;95;40;60
30;DEFNE;ŞEN;70;85;90;95;40;60
$ ./mini_obs mukerrer.csv > /dev/null     # yalnızca stderr
Hata: mukerrer.csv okunamadı: dosya biçimi hatalı (satır 5)
[çıkış kodu: 1]
$ v1.0/mini_obs mukerrer.csv > /dev/null
Hata: mukerrer.csv okunamadı: dosya biçimi hatalı (satır 5)
[çıkış kodu: 1]
```

10⁶ kayıt (≈ 43 MB) üretilip `ara`, `denetle` ve `ortanca` ile okunur; her biri dosyayı toplu kipte yükler:

```
$ ./veri_uret --n 1000000 --tohum 42 --cikti u1m.csv; ls -l u1m.csv; ./ara u1m.csv --no 2400500000; ./denetle u1m.csv; ./ortanca u1m.csv --denetle
42740682 bayt
Dosya: u1m.csv · kayıt: 1000000 (numaraya göre sıralı: EVET)
Süre: yükleme 2620.237 ms
Aranan numara: 2400500000
İkili arama (yarı açık [lo, hi)) : sıra 500000 · 19 inceleme (en çok ⌊log2 n⌋ + 1 = 20)
İkili arama (kapalı [lo, hi])    : sıra 500000 · 1 inceleme
Öğrenci no  : 2400500000
Ad Soyad    : ŞULE ASLAN
Algoritma ve Prog. I   56.40  DC  ŞARTLI BAŞARILI (YANO ≥ 2,00 ise)
Matematik I            35.20  FF  BAŞARISIZ (final barajı)
Fizik I                39.00  FF  BAŞARISIZ (final barajı)
YANO        : 0.53
Süre: ikili 4.041 µs
Dosya: u1m.csv · kayıt: 1000000
Yöntem: sıralayarak (yinelenen_bul_siralama)
Karşılaştırma: 19673895 (üst sınır 19951424; tüm çiftler n(n-1)/2 = 499999500000)
Yinelenen çift: 0
Sonuç: yinelenen numara yok.
Süre: 328.905 ms
Dosya: u1m.csv · kayıt: 1000000
Ders   ortanca   quickselect karşılaştırma   kâhin (sıralama) karşılaştırma   aynı
ALG      57.60                     4758243                           18598077   EVET
Süre (ALG): quickselect 25.123 ms · sıralama 188.840 ms
MAT      57.40                     5478911                           18596356   EVET
Süre (MAT): quickselect 17.025 ms · sıralama 229.549 ms
FIZ      57.60                     4731817                           18597684   EVET
Süre (FIZ): quickselect 17.009 ms · sıralama 199.683 ms
[çıkış kodu: 0]
```

### 5.2 `denetle`

```
./denetle dosya.csv [--yontem siralama|ciftler] [--erken] [--goster K]
```

```
$ ./denetle testler/yinelenen_k3.csv
Dosya: testler/yinelenen_k3.csv · kayıt: 30
Yöntem: sıralayarak (yinelenen_bul_siralama)
Karşılaştırma: 139 (üst sınır 148; tüm çiftler n(n-1)/2 = 435)
Yinelenen çift: 3
  sıra      8 ↔ sıra     11 · numara 2400000017 · MEHMET KESKİN / ŞULE KAYA
  sıra     10 ↔ sıra     29 · numara 2400000028 · ECE KOÇ / NİSA CAN
  sıra     17 ↔ sıra     30 · numara 2400000023 · ZEYNEP ASLAN / TOLGA KESKİN
Sonuç: yinelenen numara VAR; dosya mini_obs ile yüklenemez.
Süre: 0.004 ms
[çıkış kodu: 1]
```

```
$ ./denetle testler/yinelenen_k3.csv --yontem ciftler
Dosya: testler/yinelenen_k3.csv · kayıt: 30
Yöntem: tüm çiftler (yinelenen_bul)
Karşılaştırma: 435 (n(n-1)/2 = 435)
Yinelenen çift: 3
  sıra      8 ↔ sıra     11 · numara 2400000017 · MEHMET KESKİN / ŞULE KAYA
  sıra     10 ↔ sıra     29 · numara 2400000028 · ECE KOÇ / NİSA CAN
  sıra     17 ↔ sıra     30 · numara 2400000023 · ZEYNEP ASLAN / TOLGA KESKİN
Sonuç: yinelenen numara VAR; dosya mini_obs ile yüklenemez.
Süre: 0.001 ms
[çıkış kodu: 1]
```

### 5.3 `birlestir`

```
./birlestir subeA.csv subeB.csv [--olcut no|basari] [--ilk K] [--cikti C.csv]
```

```
$ ./birlestir ornek_veri/ogrenciler.csv ornek_veri/sube_b.csv
Şube A: ornek_veri/ogrenciler.csv · 8 kayıt
Şube B: ornek_veri/sube_b.csv · 6 kayıt
Birleşik: 14 kayıt (numara sırasında) · 10 karşılaştırma, 14 taşıma
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010041  BURAK AKSOY                69.20 CB   61.60 CC   73.00 BB   2.47
   2  2301010043  ELİF ŞİMŞEK                89.80 AA   78.80 BB   72.00 CB   3.21
   3  2301010045  AYŞE NUR YILMAZ            79.00 BB   93.00 AA   52.00 DC   2.91
   4  2301010046  MEHMET ALİ KAYA            46.80 FF   59.20 DC   66.00 CB   1.26
   5  2301010047  İSMAİL ÖZTÜRK              90.40 AA   69.00 CB   39.00 FF   2.29
   6  2301010048  CAN YILMAZ                 88.35 BA  100.00 AA   30.00 FD   2.79
   7  2301010049  ZEYNEP ÇELİK               76.00 BB   63.00 CC   53.00 DC   2.21
   8  2301010050  EMRE ÇINAR                 96.80 AA   69.60 CB   78.60 BB   3.18
   9  2301010051  ŞULE DOĞAN                 55.60 DC   56.20 DC   57.60 DC   1.50
  10  2301010052  ILGAZ ŞAHİN                36.00 FF   86.80 BA   77.00 BB   2.12
  11  2301010053  GÖKHAN ERDOĞAN             47.20 DD   59.20 DC   48.00 DD   1.18
  12  2301010055  İREM KOÇ                   93.80 AA   88.00 BA   91.00 AA   3.82
  13  2301010057  OĞUZ ÇETİN                 58.00 DC   67.60 CB   59.60 CC   2.00
  14  2301010059  SELİN ÖZDEMİR              81.60 BA   87.60 BA   76.40 BB   3.35
Süre: birleştirme 0.001 ms
[çıkış kodu: 0]
```

B şubesinin iki kaydı A'nın bütün kayıtlarından küçük, dördü büyüktür: 2 + 8 = 10 karşılaştırmadan sonra A biter ve B'nin kalanı karşılaştırmasız kopyalanır. Çakışma ve başarı listelerinin birleştirilmesi:

```
$ ./birlestir ornek_veri/ogrenciler.csv testler/sube_cakisma.csv
Şube A: ornek_veri/ogrenciler.csv · 8 kayıt
Şube B: testler/sube_cakisma.csv · 3 kayıt
Birleşik: 10 kayıt (numara sırasında) · 9 karşılaştırma, 10 taşıma
ÇAKIŞMA: 1 numara iki şubede de var: 2301010047
Süre: birleştirme 0.001 ms
[çıkış kodu: 1]
```

```
$ ./birlestir ornek_veri/ogrenciler.csv ornek_veri/sube_b.csv --olcut basari
Şube A: ornek_veri/ogrenciler.csv · 8 kayıt
Şube B: ornek_veri/sube_b.csv · 6 kayıt
Başarı listeleri: A 8 (sıralama 16 karşılaştırma) · B 6 (10) · birleştirme 13 karşılaştırma, 14 taşıma
Sıra  Şube  Öğrenci no  Ad Soyad                   YANO
   1     B  2301010055  İREM KOÇ                   3.82
   2     B  2301010059  SELİN ÖZDEMİR              3.35
   3     B  2301010043  ELİF ŞİMŞEK                3.21
   4     A  2301010050  EMRE ÇINAR                 3.18
   5     A  2301010045  AYŞE NUR YILMAZ            2.91
   6     A  2301010048  CAN YILMAZ                 2.79
   7     B  2301010041  BURAK AKSOY                2.47
   8     A  2301010047  İSMAİL ÖZTÜRK              2.29
   9     A  2301010049  ZEYNEP ÇELİK               2.21
  10     A  2301010052  ILGAZ ŞAHİN                2.12
  11     B  2301010057  OĞUZ ÇETİN                 2.00
  12     A  2301010051  ŞULE DOĞAN                 1.50
  13     A  2301010046  MEHMET ALİ KAYA            1.26
  14     B  2301010053  GÖKHAN ERDOĞAN             1.18
Süre: birleştirme 0.002 ms
[çıkış kodu: 0]
```

### 5.4 `ortanca` ve `listele`

```
$ ./ortanca ornek_veri/ogrenciler.csv --denetle
Dosya: ornek_veri/ogrenciler.csv · kayıt: 8
Ders   ortanca   quickselect karşılaştırma   kâhin (sıralama) karşılaştırma   aynı
ALG      77.50                          33                                 15   EVET
Süre (ALG): quickselect 0.001 ms · sıralama 0.001 ms
MAT      69.30                          40                                 16   EVET
Süre (MAT): quickselect 0.000 ms · sıralama 0.001 ms
FIZ      55.30                          30                                 15   EVET
Süre (FIZ): quickselect 0.000 ms · sıralama 0.000 ms
[çıkış kodu: 0]
```

Küçük n'de quickselect sıralamadan **çok** karşılaştırma yapar (8 kayıtta 33 ↔ 15): sabit çarpanlar ve pivot seçimi baskındır; fark büyük n'de tersine döner (bölüm 7.6).

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
[çıkış kodu: 0]
```

```
$ ./listele testler/kararlilik.csv --yontem hizli --denetle
Dosya: testler/kararlilik.csv · kayıt: 8
Ölçüt: basari — YANO ↓, soyad ↑, ad ↑ (başarı sırası)
Yöntem: hizli · karşılaştırma 50 · toplama 0 · çarpma 0 · taşıma 25
Sıra  Öğrenci no  Ad Soyad                        ALG        MAT        FIZ   YANO
   1  2301010063  ALİ ŞEN                    93.00 AA   93.00 AA   93.00 AA   4.00
   2  2301010067  İPEK IŞIK                  83.00 BA   83.00 BA   83.00 BA   3.50
   3  2301010068  ŞULE ÜNAL                  83.00 BA   83.00 BA   83.00 BA   3.50
   4  2301010065  CEM CAN                    66.00 CB   66.00 CB   66.00 CB   2.50
   5  2301010064  ÜMİT ÇAKIR                 66.00 CB   66.00 CB   66.00 CB   2.50
   6  2301010062  ECE KAYA                   66.00 CB   66.00 CB   66.00 CB   2.50
   7  2301010061  ECE KAYA                   66.00 CB   66.00 CB   66.00 CB   2.50
   8  2301010066  ECE KAYA                   66.00 CB   66.00 CB   66.00 CB   2.50
Kâhin (qsort + numara): FARKLI (ilk fark: sıra 6)
Eşit kayıtlar numara sırasında (kararlılık): HAYIR
Süre (hizli): 0.015 ms
[çıkış kodu: 1]
```

## 6. Tasarım kararları

1. **Yükleyicide sırayı değiştir, sonucu değiştirme.** v2.3'ün sorunu, her kaydın gelir gelmez yerine yerleştirilmesiydi (çevrimiçi ekleme, Θ(n²) taşıma). Toplu yükleme çevrimdışıdır: bütün veri elde olduğunda bir kez sıralamak yeter. Menüden tek kayıt eklemek ise çevrimiçi kalır (`sinif_sirali_ekle`, v2.3): tek ekleme Θ(n) taşımadır ve etkileşimli kullanımda fark edilmez.
2. **Kaydı değil anahtarı sırala.** Yükleyici 16 baytlık (numara, indis) anahtarlarını sıralar ve kayıtları sonunda bir kez taşır: birleştirmeli sıralamanın 2n log₂ n taşıması 144 baytlık kayıtlarda 10⁶ kayıt için ≈ 4 · 10⁷ kayıt kopyası (≈ 5,8 GB bellek trafiği) olurdu. Şube kıyasında (bölüm 7.5) uç uca ekleyip **kayıtları** sıralamanın bedeli görülür.
3. **Kararlılık, hata satırını doğru verir.** Anahtarlar numaraya göre kararlı sıralandığında eşit numaralar dosya sırasında kalır; grubun ikinci öğesi "ikinci geçiş"tir. Kararsız bir sıralama (hızlı sıralama) grubu bulur ama ikinci geçişi bulamaz; v1.0 ile aynı hata satırını vermek için ya kararlı sıralama ya da numara + satır tam anahtarı gerekir.
4. **Tek tampon.** Birleştirmeli sıralama tamponu bir kez ayırır; özyinelemede `malloc`/`free` yoktur. Bellek yetmezse işlev `false` döner ve dizi değişmez (yükleyici `DOSYA_BELLEK_YETERSIZ` döndürür).
5. **Hızlı sıralama da var ama varsayılan değil.** Başarı listesinin varsayılanı birleştirmelidir: kararlıdır (eşit kayıtlar numara sırasında kalır) ve en kötü durumu da Θ(n log n)'dir. Hızlı sıralama karşılaştırma ve ölçüm için `--yontem hizli` ile seçilebilir.
6. **Üç yollu quickselect.** Notlar çok tekrarlıdır (10⁶ kayıtta ≈ 10⁴ farklı ortalama): iki yollu bölümlemede pivota eşit öğeler turdan tura taşınır; üç yollu bölümleme onları tek turda eler.
7. **Şube çakışması hata değil rapor.** İki şubede aynı numara bir veri hatasıdır; `birlestir` birleşik listeyi kaydetmez, çakışan numaraları listeler ve 1 ile çıkar. Kayıt dizisinin değişmezi (numaralar benzersiz) böylece korunur.
8. **Kâhinler önceki sürümlerdir.** v2.1'in tüm çiftler yöntemi ve v1.0'ın yükleyicisi silinmedi; `denetle --yontem ciftler`, `olcer yukleme_v10` ve kâhin testleri onları kullanır. Sarmalın her basamağı bir öncekiyle aynı sonucu vermek zorundadır.

## 7. Ölçümler

### 7.1 Ölçüm düzeni ve ortam

Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB, L3 33 MiB; gcc 13.3.0, glibc 2.39, `-std=c17 -Wall -Wextra -pedantic -O2 -g`; tarih 2026-10-13 07:18. Düzen: 1 ısınma + 5 tekrar, ortanca (Sedgewick & Wayne, 2011); ucuz yükleme ölçümlerinde 9 tekrar, 10⁶ kayıtlık yüklemede 3, en pahalı noktalarda 1 tekrar (tablolarda belirtilir). Veri: `veri_uret` üreteci, tohum 42, yinelenen yok (aksi belirtilmedikçe). Sayaçlar ısınma çalıştırmasında toplanır ve kuramın kesin değer verdiği her durumda `olcer` onları otomatik karşılaştırır: bu ölçümde 14 "kuram: UYUMLU", 0 uyumsuzluk ya da aşılmış üst sınır. `make olcum` 2 dakika 20 s sürdü. Ölçüm sırasında makinenin 1 dakikalık yük ortalaması başta 0,77, sonda 1,07 idi (2 çekirdek; başka işlerle paylaşıldı): süreler gürültülüdür. Bu yüzden yükleme tablolarında ortancanın yanında en küçük süre de verilir; sayaçlar deterministiktir.

### 7.2 Yükleme: v1.0 → v2.3 → v2.5

| n | v1.0 (doğrusal denetim) | v2.3 (ikili arama + kaydırma) | v2.5 toplu | yalnız ayrıştırma | v1.0 / v2.5 | v2.3 / v2.5 |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 1,7 ms | 2,2 ms | 1,7 ms | 2,5 ms | 1,0 | 1,3 |
| 4 000 | 13,2 ms | 15,8 ms | 6,3 ms | 4,8 ms | 2,1 | 2,5 |
| 16 000 | 225,2 ms | 302,2 ms | 25,5 ms | 17,8 ms | 8,8 | 11,8 |
| 32 000 | 1,33 s | 1,66 s | 71,2 ms (51,9 ms) | 65,5 ms (37,4 ms) | 18,7 | 23,3 |
| 100 000 | 19,05 s ᵃ | 20,75 s ᵃ | 240,2 ms (182,8 ms) | 128,7 ms (113,3 ms) | 79,3 | 86,4 |
| 1 000 000 | ≈ 1,6 saat ᵇ | ≈ 35 dk ᵇ | 2,28 s | 1,39 s | 2 540 | — |

*Tablo 1. Karışık sıralı CSV'nin yüklenmesi (ortanca; parantez: en küçük süre, ortancadan %10'dan fazla küçükse). ᵃ v2.3'ün ölçümü (aynı makine, 1 tekrar). ᵇ Kestirim: v2.0 (v1.0 yükleyicisi, ölçülen eğriye uydurulan model) ve v2.3 (taşıma başına maliyetle; alt sınır).*

![Yükleme süreleri](mini_obs_v2_5_olcum_yukleme.png)

*Şekil 3. Yükleme süresi (log–log). v1.0 ve v2.3 eğimi ≈ 2 olan doğrulardır; noktalı çizgiler en büyük ölçümden c·n² ile 10⁶'ya uzatılmıştır (alt sınır kestirimi). Yıldız, v2.0'ın kestirimidir. Toplu yükleme ayrıştırma tabanına paralel (eğim ≈ 1) gider.*

- **10⁶ kayıt 2,28 s'de yüklenir** (ortanca, 3 tekrar; en az 2,24 s): v2.0'ın ≈ 1,6 saatlik (5 785 s) kestirimine göre ≈ 2 540 kat, v2.3'ün ≈ 35 dakikalık kestirimine göre ≈ 922 kat. Aynı boyutta yalnızca ayrıştırma 1,39 s sürer. c·n² ile kaba uzatma v1.0 için ≈ 32 dakika verir; v2.0'ın modeli bundan büyüktür, çünkü 10⁵'in üstünde dizi önbelleğe sığmaz ve karşılaştırma başına maliyet artar.
- **Karesel ve n log n eğrileri küçük n'de bile ayrışır:** n = 32 000'de v1.0 ile toplu yükleme arasındaki oran 18,7, v2.3 ile 23,3; 10⁵'te (v2.3'ün ölçümleriyle) 79 ve 86 kat.
- **Sıralamanın payı küçüktür:** 10⁵ anahtarın sıralanması 27,4 ms, 10⁶ anahtarınki 277,3 ms sürer (Tablo 4); yükleme süresinin çoğu metni ayrıştırmaktır. Toplu yükleme ile yalnız ayrıştırma arasındaki fark (ortancalar) 111,5 ms (10⁵) ve 882,2 ms (10⁶) olur: anahtar sıralaması, komşu denetimi, satır dizisi ve son taşıma (10⁶'da 144 MB'lık yeni dizi). Küçük n'deki oranlar (ör. 4 000) paylaşılan makinede gürültüye açıktır; parantezdeki en küçük süreler farkın büyüklüğünü daha iyi gösterir.

| girdi sırası (n = 100 000) | karşılaştırma | taşıma | süre (en az) |
|:--|--:|--:|--:|
| karışık (üreteç sırası) | 1 636 284 | 3 437 856 | 240,2 ms (182,8 ms) |
| numara sırasında | 915 023 | 3 437 856 | 137,9 ms |
| ters sırada | 953 903 | 3 437 856 | 164,1 ms (127,1 ms) |

*Tablo 2. Toplu yüklemenin girdi sırasına duyarlılığı (n = 100 000, 9 tekrar). Taşıma girdiden bağımsızdır; karşılaştırma sıralı girdide en azdır.*

Birleştirmeli sıralama girdiye karşı **duyarsızdır**: sıralı girdide 915 023, karışık girdide 1 636 284 karşılaştırma (oran 1,79); taşıma her durumda aynı. v2.3'te aynı fark 0 ile 2,5·10⁹ taşıma arasındaydı (sıralı ↔ karışık). Sıralı ve ters girdinin karşılaştırma sayıları kuramla birebir uyuşur.

### 7.3 Yinelenen numara: v2.1 ↔ v2.5

| n | v2.1 tüm çiftler | karşılaştırma | v2.5 sıralayarak | karşılaştırma | hızlanma | eşit çift (kontrol) |
|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 440,9 µs | 499 500 | 105,5 µs | 9 729 | 4 | 0 = 0 |
| 4 000 | 6,6 ms | 7 998 000 | 537,7 µs | 46 901 | 12 | 0 = 0 |
| 16 000 | 135,1 ms | 127 992 000 | 2,7 ms | 219 265 | 50 | 0 = 0 |
| 64 000 | 1,61 s | 2 047 968 000 | 13,1 ms | 1 005 248 | 123 | 0 = 0 |
| 100 000 | 4,33 s (1 tekrar) | 4 999 950 000 | 23,1 ms | 1 636 284 | 187 | 0 = 0 |
| 1 000 000 | — | — | 354,5 ms | 19 673 895 | — | 0 |

*Tablo 3. Yinelenen numara tespiti: v2.1 (numara dizisinde tüm çiftler) ↔ v2.5 (sırala + komşu). Son sütun, iki yöntemin bulduğu eşit çift sayısıdır (yinelenen yok).*

- **Aynı sonuç:** her n'de iki yöntemin `kontrol` değeri (eşit çift sayısı) aynıdır; 3 kasıtlı yinelenenli veride (n = 16 000) ikisi de 3 çift bulur (87,9 ms ↔ 4,3 ms). Çiftlerin kendisinin ve sırasının aynı olduğunu kâhin testleri gösterir.
- **Ölçülen hızlanma:** 64 000 kayıtta 123 kat, 10⁵ kayıtta 187 kat; büyüme sınıfı farkı olduğu için oran n ile büyür. 10⁶ kayıtta v2.5 354,5 ms sürer; v2.1 için c·n² ile kestirim ≈ 7 dakikadır (**kestirim**, ölçülmedi).
- **Karşılaştırma sayıları kuramla uyumlu:** v2.1 tam n(n − 1)/2; v2.5 ≤ n⌈log₂ n⌉ − 2^⌈log₂ n⌉ + 1 + (n − 1) (her ölçümde "içinde").

![Yinelenen ve başarı listesi](mini_obs_v2_5_olcum_siralama.png)

*Şekil 4. Sol: yinelenen tespiti; sağ: başarı listesinin (Türkçe karşılaştırıcı, işaretçi dizisi) sıralanması — v2.4'ün araya eklemesi ve v2.5'in üç Θ(n log n) yöntemi (log–log).*

### 7.4 Birleştirmeli ↔ hızlı ↔ qsort

| algoritma | n | süre | karşılaştırma | kars. / (n log₂ n) | taşıma | ns / (n log₂ n) |
|:--|--:|--:|--:|--:|--:|--:|
| birleştirmeli (yukarıdan aşağıya) | 10 000 | 2,1 ms | 120 382 | 0,906 | 267 232 | 15,51 |
|  | 100 000 | 27,4 ms | 1 536 285 | 0,925 | 3 337 856 | 16,47 |
|  | 1 000 000 | 277,3 ms | 18 673 896 | 0,937 | 39 902 848 | 13,91 |
| birleştirmeli (aşağıdan yukarıya) | 10 000 | 2,8 ms | 123 621 | 0,930 | 140 000 | 21,32 |
|  | 100 000 | 35,5 ms | 1 566 783 | 0,943 | 1 800 000 | 21,36 |
|  | 1 000 000 | 297,3 ms | 18 715 497 | 0,939 | 20 000 000 | 14,91 |
| hızlı (Hoare, üçün ortancası) | 10 000 | 1,4 ms | 195 481 | 1,471 | 105 807 | 10,46 |
|  | 100 000 | 16,7 ms | 2 402 390 | 1,446 | 1 286 094 | 10,08 |
|  | 1 000 000 | 207,2 ms | 27 875 705 | 1,399 | 15 255 804 | 10,39 |
| qsort (glibc 2.39) | 10 000 | 1,5 ms | 120 382 | 0,906 | — | 11,00 |
|  | 100 000 | 18,5 ms | 1 536 285 | 0,925 | — | 11,12 |
|  | 1 000 000 | 250,0 ms | 18 673 896 | 0,937 | — | 12,54 |

*Tablo 4. 16 baytlık (numara, indis) anahtarlarının karışık sırada sıralanması (yükleyicinin iç işi). Son iki sütun, sayaç ve süre için n log₂ n'ye bölünmüş değerlerdir: sabit kalması n log n büyümesinin imzasıdır.*

| algoritma (n = 100 000) | karışık: süre · kars. | sıralı: süre · kars. | ters: süre · kars. | neredeyse sıralı: süre · kars. |
|:--|--:|--:|--:|--:|
| birleştirmeli (yukarıdan aşağıya) | 27,4 ms · 1 536 285 | 17,3 ms · 815 024 | 18,0 ms · 853 904 | 17,5 ms · 818 172 |
| birleştirmeli (aşağıdan yukarıya) | 35,5 ms · 1 566 783 | 6,3 ms · 877 968 | 11,0 ms · 815 024 | 6,3 ms · 880 357 |
| hızlı (Hoare, üçün ortancası) | 16,7 ms · 2 402 390 | 5,3 ms · 1 968 925 | 10,3 ms · 1 968 927 | 5,2 ms · 1 973 939 |
| qsort (glibc 2.39) | 18,5 ms · 1 536 285 | 6,2 ms · 815 024 | 8,7 ms · 853 904 | 8,9 ms · 818 172 |

*Tablo 5. Girdi sırasının etkisi, n = 100 000 (süre · karşılaştırma).*

- **Hızlı sıralama daha çok karşılaştırır, daha az taşır:** karışık girdide karşılaştırması birleştirmelininkinin 1,56 katı, taşıması 0,39 katıdır. Bu anahtarlarda karşılaştırma ucuz (iki tamsayı), taşıma görece pahalıdır (16 baytlık `memcpy`). Süreler: hızlı sıralama yukarıdan aşağıya birleştirmeliye göre 10⁵'te hızlıdır (16,7 ms ↔ 27,4 ms), 10⁶'da hızlıdır (207,2 ms ↔ 277,3 ms).
- **Aynı algoritma, yarı taşıma:** aşağıdan yukarıya sürüm her geçişte n taşıma yapar (yukarıdan aşağıya sürüm 2n; Tablo 4'te 20 000 000 ↔ 39 902 848, n = 10⁶); karşılaştırma sayıları neredeyse aynıdır. Süre olarak 10⁵'te yavaştır, 10⁶'da yaklaşık aynı sürededir (297,3 ms ↔ 277,3 ms). Yarı taşımaya karşın yavaş olması **önbellekle** açıklanır: aşağıdan yukarıya sürüm her geçişte bütün diziyi baştan sona dolaşır (⌈log₂ n⌉ geçiş), yukarıdan aşağıya sürüm ise küçük alt dizileri önbellekteyken bitirir. Taşıma sayısı tek başına süreyi belirlemez.
- **qsort:** bu makinedeki kütüphanenin (glibc 2.39) `qsort` işlevi bu ölçümlerde yukarıdan aşağıya birleştirmeli sıralamamızla **her girdide birebir aynı sayıda** karşılaştırma yaptı (ör. 10⁵ karışık: 1 536 285). Bu, bu kütüphanenin bu boyutlarda aynı bölme kuralıyla birleştirmeli sıralama kullandığını gösterir; C standardı algoritmayı ve kararlılığı **güvence etmez** (v2.4'teki gözlem de buydu). `qsort`'un taşıma sayısı ölçülemez (kütüphanenin içi).
- **Sıralı ve neredeyse sıralı girdi** bütün yöntemleri hızlandırır: birleştirmeli sıralamada karşılaştırma yarıya iner; hızlı sıralamada üçün ortancası bölmeyi tam ortadan yapar ve takas neredeyse hiç olmaz.

| n | araya ekleme (v2.4) | birleştirmeli | hızlı | qsort |
|--:|--:|--:|--:|--:|
| 1 000 | 12,4 ms | 1,2 ms | 2,1 ms | 1,7 ms |
| 4 000 | 190,8 ms | 7,5 ms | 10,8 ms | 10,6 ms |
| 16 000 | 2,65 s | 45,7 ms | 54,9 ms | 64,2 ms |
| 100 000 | — | 452,9 ms | 664,6 ms | 442,5 ms |
| 1 000 000 | — | 6,71 s (1 tekrar) | — | — |

*Tablo 6. Başarı listesi (YANO ↓, soyad ↑, ad ↑; Türkçe karşılaştırıcı; işaretçi dizisi), karışık girdi.*

- **Kesişme yok, uçurum var:** 1 000 kayıtta bile birleştirmeli sıralama araya eklemeden 10 kat hızlıdır; 16 000 kayıtta fark 58 kat. Araya ekleme yalnızca çok küçük ya da neredeyse sıralı girdide kazanır (v2.4); bu yüzden gerçek kütüphaneler onu küçük parçalarda kullanır.
- **Pahalı karşılaştırıcıda karşılaştırma sayısı belirleyicidir:** başarı ölçütünde hızlı sıralama 2 316 417, birleştirmeli 1 536 453 karşılaştırma yapar (10⁵) ve daha yavaştır (664,6 ms ↔ 452,9 ms). Anahtar sıralamasındaki sıralama (Tablo 4) burada tersine döner: maliyeti taşıma değil Türkçe dizgi karşılaştırması belirler.
- **Kararlılık sağlaması:** 10⁵ kayıtta birleştirmeli sıralama ile `qsort`'un `kontrol` değeri aynıdır; hızlı sıralamanınki farklıdır: eşit kayıtların sırası değişmiştir.
- 10⁶ kayıtlık başarı listesi birleştirmeli sıralamayla 6,71 s sürer (1 tekrar); araya eklemeyle saatler sürerdi.

### 7.5 Şube birleştirme

| n = nA + nB | birleştir | kars. | taşıma | uç uca + sırala | kars. | taşıma | oran | aynı liste |
|--:|--:|--:|--:|--:|--:|--:|--:|:-:|
| 10 000 | 169,7 µs | 9 998 | 10 000 | 1,9 ms | 74 390 | 277 232 | 11,2 | EVET |
| 100 000 | 5,0 ms | 99 999 | 100 000 | 46,5 ms | 914 109 | 3 437 856 | 9,4 | EVET |
| 1 000 000 | 134,0 ms | 999 999 | 1 000 000 | 918,3 ms | 10 880 781 | 40 902 848 | 6,9 | EVET |

*Tablo 7. n kayıt rastgele ikiye bölünür (her kayıt yazı-tura ile A ya da B); iki şube numara sırasındadır. "Uç uca + sırala": iki dizi art arda kopyalanır ve **kayıtlar** (144 B) birleştirmeli sıralanır. "Aynı liste": iki yöntemin sıra sağlaması.*

Birleştirme Θ(n)'dir: karşılaştırma n − 1'e çok yakın, taşıma tam n. Uç uca ekleyip sıralamak Θ(n log n) karşılaştırma ve ≈ 2n log₂ n kayıt taşıması yapar: 10⁵'te 9,4, 10⁶'da 6,9 kat yavaştır. 10⁶'da birleştirmenin kendisi de 134,0 ms sürer: 144 MB'lık yeni dizinin ayrılması ve bir kez yazılması (bellek bant genişliği) baskındır.

### 7.6 Ortanca: quickselect ↔ sıralama

| n | ortanca (ALG) | quickselect | kars. | kars. / n | sıralama | kars. | oran | aynı |
|--:|--:|--:|--:|--:|--:|--:|--:|:-:|
| 10 000 | 57,60 | 135,2 µs | 43 511 | 4,35 | 1,4 ms | 120 122 | 10,7 | EVET |
| 100 000 | 57,60 | 1,5 ms | 458 692 | 4,59 | 28,2 ms | 1 531 341 | 18,7 | EVET |
| 1 000 000 | 57,60 | 22,0 ms | 6 238 472 | 6,24 | 208,2 ms | 18 598 116 | 9,5 | EVET |

*Tablo 8. ALG ders ortalamalarının ortancası. "kars. / n": quickselect'in karşılaştırma sayısının n'ye oranı (doğrusal büyümenin imzası).*

Quickselect'in karşılaştırma sayısı n ile **doğrusal** büyür (oran 4,35–6,24); sıralama kâhini n log n büyür. 10⁶ kayıtta quickselect 9,5 kat hızlıdır ve her n'de aynı ortancayı verir. Oranın büyük n'de artması veriden gelir: ortalamalar iki ondalıklıdır ve 10⁶ kayıtta çok tekrar eder; üç yollu bölümlemede pivota eşit olmayan her öğe iki karşılaştırma yapar.

### 7.7 Sonuç ve H7'ye köprü

Böl ve fethet, Mini-OBS'nin büyük veri sorunlarını kapattı: 10⁶ kayıt saniyeler içinde yüklenir, yinelenenler saniyenin altında bulunur, iki şube doğrusal zamanda birleşir, ortanca sıralamasız bulunur. Bütün bu yöntemler **karşılaştırmaya dayalıdır** ve Ω(n log n) alt sınırına tabidir (ortanca hariç: seçim sıralamadan kolaydır). H7'de bu sınırın dışına çıkacağız: notlar 0–100 aralığında olduğu için **sayma sıralaması**, numaralar sabit uzunlukta olduğu için **taban sıralaması** Θ(n)'de sıralar; ilk-k listesi için bütün listeyi sıralamak yerine k boyutlu bir **öbek** yeter. v2.6'nın ölçüm raporu, bu sürümün yöntemlerini o yöntemlerle aynı tabloda karşılaştıracak.

## 8. Testler

- **Birim testleri** (`obs_test`): `226 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama + 26 sıralama + 23 böl-fethet`. Böl-fethet testleri: birleştirmede kararlılık ve elle izlenen sayaçlar (6 karşılaştırma, 7 taşıma), boş liste; CLRS örneğinde 11 karşılaştırma ve 32 taşıma (yukarıdan aşağıya), 9 ve 24 (aşağıdan yukarıya); sıralı ve ters girdide kapalı biçimler (n = 7: 9 ve 11); (2, 0) (2, 1) (1, 2) dizisinde birleştirmeli kararlı, hızlı kararsız; n = 0, 1 ve 300 baytlık öğe; hızlı sıralamada dört girdi türünde derinlik ≤ 10 (n = 1 000); quickselect her k için ve son koşulu; ortanca tek/çift/tek öğe ve hepsi eşit (17 karşılaştırma); sıralayarak yinelenen = v2.1 sonucu (aynı dört çift, aynı sıra, 11 + 5 karşılaştırma); toplu yükleyici = SIRALI kip (bayt bayt), mükerrer ve bozuk satır birlikteyken v1.0 ile aynı satır, ikili dosya; şube birleştirme (10 karşılaştırma, 14 taşıma), çakışma (A'nın kaydı kalır) ve boş şube.
- **Kâhin testleri** (`test_kahin`): 300 denemede 350 751, 1 000 denemede 1 158 416 denetim (böl ve fethet: 11 748; sıralayarak yinelenen, toplu yükleme ve şube: 5 704), uyuşmazlık yok.
- **Kasıtlı hatalar ve küçük kapsam araması.** Kâhin bir uyuşmazlık bulduğunda rastgele (büyük) karşı örnek kolayca okunmaz. Bu sürümde test aracı ayrıca 1..7 öğeli **bütün** permütasyonları (en çok 5 913 girdi) sözlük sırasıyla dener ve hatayı gösteren **en küçük** girdiyi basar. (a) `--hata-goster kuyruk`: birleştirmede A'nın kalanı kopyalanmaz:

```
$ ./test_kahin --hata-goster kuyruk
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : birlestirmeli_sirala
  n          : 98
  Beklenen   : sıralı dizi; karşılaştırma ≤ 559, taşıma 1312
  Bulunan    : SIRALI DEĞİL; karşılaştırma 0, taşıma 0, derinlik -1
  Girdi    = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, ...]
  Bulunan  = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...]
  En küçük karşı örnek (1..7 öğeli bütün permütasyonlar denendi; 2 öğe):
  Girdi    = [2, 1]
  Beklenen = [1, 2]
  Bulunan  = [1, 1]
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster kuyruk
[çıkış kodu: 1]
```

  (b) `--hata-goster hoare`: Hoare bölümlemesinin j'si pivotun yeri sanılır:

```
$ ./test_kahin --hata-goster hoare
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : hizli_sirala
  n          : 98
  Beklenen   : sıralı dizi; derinlik ≤ ⌊log2 n⌋ + 1 = 7
  Bulunan    : SIRALI DEĞİL; karşılaştırma 0, taşıma 0, derinlik 0
  Girdi    = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, ...]
  Bulunan  = [0, 1, 2, 1, 4, 3, 5, 5, 6, 7, 7, 8, 8, 3, 9, 10, 10, 11, 12, 13, 6, 14, 15, 16, ...]
  En küçük karşı örnek (1..7 öğeli bütün permütasyonlar denendi; 3 öğe):
  Girdi    = [2, 3, 1]
  Beklenen = [1, 2, 3]
  Bulunan  = [2, 1, 3]
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster hoare
[çıkış kodu: 1]
```

- **Bellek:** `make asan` temiz (yeni programlar, `olcer`'in bütün böl-fethet işlemleri n = 1, 2, 3, 300 ve dört girdi sırasıyla, çakışmalı ve boş şubeler dahil); `make valgrind`: 10 çalıştırmanın 10 tanesinde "0 errors", 10 tanesinde "All heap blocks were freed" (yeni programlar dahil).

## 9. Ders notu için özet (Hafta 6 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'nin büyük veri sorunlarını böl ve fethetle çözüyoruz. Birleştirmeli sıralamayı (tek tampon, kararlı) ve Hoare bölümlemeli hızlı sıralamayı v2.4'ün qsort arayüzünde yazıyoruz; yükleyiciyi "oku → anahtarları sırala → komşuları karşılaştır → bir kez taşı" düzenine çeviriyoruz; yinelenen numara tespitini sıralamayla O(n log n)'e indiriyoruz; iki şubenin listelerini birleştirme adımıyla birleştiriyoruz; ortancayı quickselect ile buluyoruz. Her yeni algoritma bir önceki sürümün yöntemine (kâhin) karşı sınanır.

### Gereksinimler

- `bolfethet.h/.c`: `birlestir_genel` (kararlı; değişmez yorumu), `birlestirmeli_sirala_say` (tek tampon, bir kez ayrılır), `hizli_sirala_say` (Hoare bölümlemesi, üçün ortancası, küçük parçaya özyineleme; isteğe bağlı derinlik çıktısı), `k_inci_kucuk`, `ortanca_quickselect`; arayüz ve sayaçlar v2.4 ile aynı.
- Yükleyici (`sinif_yukle`) toplu kipte: sonuç numara sırasında; mükerrer ya da bozuk satırda v1.0 ile **aynı durum ve satır**; Θ(n log n).
- `yinelenen_bul_siralama`: v2.1 ile aynı çiftler, aynı sözlük sırası; `denetle --yontem siralama|ciftler`.
- `sube_birlestir` + `birlestir` programı: numara sırasında birleşik liste, çakışmaların raporu, çıkış kodu 1.
- `ortanca` programı: üç dersin ortancası; `--denetle` ile sıralama kâhini.
- `listele`'ye `birlestirmeli` (varsayılan) ve `hizli`.
- Testler: elle izlenmiş sayaçlar; kâhinler (qsort, v2.1, v1.0 + qsort, uç uca ekleme + sıralama); kararlılık.
- Ölçüm raporu: yükleme (v1.0, v2.3, v2.5; 10³–10⁶), yinelenen tespiti (v2.1 ↔ v2.5; aynı sonuç ve hızlanma), birleştirmeli ↔ hızlı ↔ qsort (en az 10⁴–10⁶, girdi sırası), şube birleştirme ↔ uç uca + sırala, quickselect ↔ sıralama; tablolar, log–log grafikler, yorum.

### İpuçları

- Orta noktayı `lo + (hi − lo) / 2` ile hesaplayın (v2.3); yarı açık aralıkta [lo, orta) ve [orta, hi).
- Birleştirmede eşitlikte **soldan** alın (`b < a` ise sağdan): kararlılık bu tek karşılaştırmadadır.
- Tamponu özyinelemenin dışında bir kez ayırın; özyinelemeli yardımcı fonksiyona işaretçi olarak verin.
- Hoare bölümlemesinde pivotun **değerini** bir kenara kopyalayın: takaslar sırasında pivotun bulunduğu hücre değişebilir.
- Hoare'un döndürdüğü j ile [lo, j] ve [j + 1, hi]; Lomuto'nun döndürdüğü p ile [lo, p − 1] ve [p + 1, hi]. İkisini karıştırmayın (`--hata-goster hoare`).
- Yükleyicide satır numaralarını ayrı bir dizide tutun; anahtar (numara, indis) olsun, kayıt değil.
- Quickselect'i kopya üzerinde çalıştırın: ortanca bulmak sınıfın kayıt sırasını değiştirmemelidir.
- Kâhin uyuşmazlık bulursa önce küçük girdileri deneyin: 3–4 öğelik bir karşı örnek, 300 öğelik olandan çok daha kolay izlenir.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri ve `test_kahin` (300 deneme) geçer.
2. `olcer anahtar_birlestirmeli --sira artan --n 1000` karşılaştırma 4 932, taşıma 19 952 ("kuram: UYUMLU"); `--sira azalan` karşılaştırma 5 044.
3. `olcer anahtar_hizli --sira artan --n 1024`: derinlik 11 (= ⌊log₂ n⌋ + 1); karışık girdide derinlik bu sınırın altında.
4. İki mükerrer numaralı dosyada (bölüm 5.1) `mini_obs` "satır 5" raporlar ve 1 ile çıkar — v1.0 ile aynı.
5. `denetle testler/yinelenen_k3.csv` ve `--yontem ciftler` aynı üç çifti aynı sırada yazar; ikisi de 1 ile çıkar; sıralayarak yöntemin karşılaştırması 148'i aşmaz.
6. `birlestir ornek_veri/ogrenciler.csv ornek_veri/sube_b.csv`: 14 kayıt, 10 karşılaştırma, 14 taşıma, çıkış 0; `testler/sube_cakisma.csv` ile "ÇAKIŞMA: 1 numara … 2301010047", çıkış 1.
7. `ortanca ornek_veri/ogrenciler.csv --denetle`: ALG 77,50, MAT 69,30, FIZ 55,30; üçünde "aynı EVET".
8. `listele testler/kararlilik.csv --yontem hepsi`: birlestirmeli "EVET / EVET", hizli "HAYIR / HAYIR".
9. Kendi makinenizde 10⁶ kayıtlık dosya toplu kipte 1 dakikanın altında yüklenir (bu makinede 2,28 s); 10⁵ kayıtta yinelenen tespiti v2.1'den en az 50 kat hızlıdır (bu makinede 187 kat).
10. `--hata-goster kuyruk` ve `--hata-goster hoare` uyuşmazlığı ve en küçük karşı örneği basar, 1 ile çıkar; `make asan` temizdir.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | birleştir [1, 3, 5, 7] + [2, 3, 6] (anahtar, kimlik) | 1 2 3ᴬ 3ᴮ 5 6 7; 6 karşılaştırma, 7 taşıma |
| 2 | birleştirmeli sırala 5 2 4 6 1 3 | 1 2 3 4 5 6; 11 karşılaştırma, 32 taşıma |
| 3 | (2, 0) (2, 1) (1, 2): birleştirmeli ↔ hızlı | (1, 2) (2, 0) (2, 1) ↔ (1, 2) (2, 1) (2, 0) |
| 4 | hızlı sırala 1 000 eşit öğe | sıralı; derinlik ≤ 10 |
| 5 | k_inci_kucuk(7 2 9 4 4 1 8, k = 3) | 4; solunda ≤ 4, sağında ≥ 4 |
| 6 | ortanca {4, 1, 3, 2} · {70 × 6} | 2,5 · 70 (17 karşılaştırma) |
| 7 | yinelenen numaralar 7 3 7 5 3 7 | (0,2) (0,5) (1,4) (2,5); 11 + 5 karşılaştırma |
| 8 | CSV: 5, 2, 9, 9, 2 (satır 1–5) | mükerrer, satır 4 (v1.0 ile aynı) |
| 9 | CSV: 5, 5, bozuk satır | mükerrer, satır 2 |
| 10 | CSV: 5, 2, bozuk satır, 2 | biçim hatası, satır 3 |
| 11 | `birlestir` A + `testler/sube_cakisma.csv` | çakışma 2301010047; birleşik listede ÖZTÜRK (A'nın kaydı); çıkış 1 |
| 12 | `test_kahin --hata-goster kuyruk` / `hoare` | en küçük karşı örnek [2, 1] → [1, 1] / [2, 3, 1] → [2, 1, 3]; çıkış 1 |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.4'ünüz (ya da referans v2.4), `bolfethet.h` ve `sube.h` (bildirimler, sözleşmeler, sayaç tanımları), `ornek_veri/sube_b.csv`, `testler/sube_cakisma.csv`, `olcer`'in yeni işlemleri için ölçüm düzeneği (veri hazırlama, sağlama, kuram fonksiyonları).
- **Yazılır:** `bolfethet.c`, `sube.c`, `ortanca.c`, `birlestir.c`; `dosya.c`'ye toplu kip; `yinelenen.c`'ye sıralayarak tespit; `denetle.c`'ye `--yontem`; `liste.c`'ye iki yöntem; testler; `Makefile`.
- **Değiştirilmez:** v1.0 kuralları ve hata satırı sözleşmesi, kayıt dizisinin numara sırası (v2.3 değişmezi), önceki sürümlerin yöntemleri (kâhin olarak kalırlar), ortak modüller.
- **Meydan okuma:** (a) küçük parçalarda (m ≤ 16) araya eklemeye geçen **melez** birleştirmeli sıralama yazın ve eşiği ölçerek seçin; (b) birleştirmeyi yalnızca A'yı tampona kopyalayarak yapın (yarım tampon) ve taşıma sayısını yeniden hesaplayın; (c) Lomuto bölümlemeli hızlı sıralamayı yazıp çok tekrarlı girdide (notlar) Hoare'la karşılaştırın; (d) aşağıdan yukarıya birleştirmeli sıralamada dizide zaten var olan sıralı koşuları (run) kullanan "doğal birleştirmeli sıralama"yı deneyin.

## 10. Bilinen sınırlılıklar

- Toplu yükleme, kayıtlar ve satır numaraları için ek Θ(n) bellek kullanır; 10⁶ kayıtta yükleme sırasında bellekte geçici olarak iki kayıt dizisi (≈ 2 × 144 MB) bulunur.
- Hızlı sıralamanın en kötü durumu Θ(n²) olarak kalır (üçün ortancasını bozan özel girdiler); introsort'la sınırlanmadı. Başarı listesinin ve yükleyicinin varsayılanı bu yüzden birleştirmeli sıralamadır.
- Quickselect'in de en kötü durumu Θ(n²)'dir (ortancaların ortancası ile Θ(n) en kötü durum güvencesi bu sürümde yok).
- Menüden tek kayıt ekleme v2.3'teki gibi Θ(n) taşımadır.
- glibc `qsort`'unun gözlenen davranışı (birleştirmeli sıralama, kararlılık) kütüphanenin belgelediği bir güvence değildir; başka bir platformda farklı olabilir.
- Süreler tek ve paylaşılan bir sanal makinede ölçüldü; yükleme ölçümlerinde ortanca ile en küçük süre arasında belirgin farklar vardır. Sayaçlar makineden bağımsızdır.
- **Sonradan bulunan hata (v2.6'da düzeltildi):** ders ortalaması ölçütleri (`alg`, `mat`, `fiz`) ortalamaları kayan nokta olarak karşılaştırır. 0,4·vize + 0,6·final, matematiksel olarak eşit iki ortalamayı son bitte farklı hesaplayabilir (ör. 0,4·3 + 0,6·0 = 1,2000000000000002, 0,4·0 + 0,6·2 = 1,2); bu kayıtlar soyada göre değil bu farka göre sıralanır. Kâhin aynı karşılaştırıcıyı kullandığı için hatayı göremedi; v2.6'nın sayma sıralaması (tamsayı anahtar) onu ortaya çıkardı. Başarı ölçütü (tamsayı YANO) etkilenmez.

## 11. Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Dijkstra, E. W. (1976). *A discipline of programming*. Prentice Hall.
- Hoare, C. A. R. (1961). Algorithm 65: Find. *Communications of the ACM, 4*(7), 321–322.
- Hoare, C. A. R. (1962). Quicksort. *The Computer Journal, 5*(1), 10–16. https://doi.org/10.1093/comjnl/5.1.10
- Knuth, D. E. (1971). Mathematical analysis of algorithms. In *Information Processing 71: Proceedings of IFIP Congress 71* (Vol. 1, pp. 19–27). North-Holland.
- Knuth, D. E. (1998). *The art of computer programming: Vol. 3. Sorting and searching* (2nd ed.). Addison-Wesley.
- Sedgewick, R. (1978). Implementing Quicksort programs. *Communications of the ACM, 21*(10), 847–857. https://doi.org/10.1145/359619.359631
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
