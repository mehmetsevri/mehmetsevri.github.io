# Mini-OBS 2 v2.11 — Açgözlü algoritmalar: sınav oturumu ataması ve en az salon (Hafta 12)

**Bu sürümün amacı:** Hafta 12'nin açgözlü stratejisini Mini-OBS'nin sınav programına uygulamak ve haftanın Büyük Sorusunu ("Her adımda o an en iyi görünen seçimi yapmak her zaman en iyi sonuca götürür mü?") iki karşıt örnekle yanıtlamak. Ortak öğrencisi olan iki dersin sınavı aynı oturuma konamaz: dersler bir **çakışma grafının** köşeleridir ve oturum ataması bir **graf renklendirmesidir**. Renk sayısını en aza indirmek NP-zordur; **Welsh–Powell** (derece azalan sıra, eşitlikte küçük ders kodu; sonra ilk uyan renk) hızlı ama **en iyiyi garanti etmeyen** bir açgözlü sezgiseldir — taç grafında en iyi 2 oturum varken 4 oturum kullanır (§ 4.3). Aynı gün içinde salon sayısını ise **aralık bölümleme** (başlangıca göre sırala, salonların bitiş zamanlarını en küçük öbekte tut) verir ve bu açgözlü algoritma **kanıtlanmış olarak en iyidir**: salon sayısı en çok eşzamanlı sınav sayısına (alt sınır) eşittir; program bunu her çalıştırmada ayrı bir süpürmeyle doğrular (§ 4.5). Küçük örneklerde (≤ 30 ders; ölçümde n = 10 ve n ≤ 28) açgözlü sonuç kaba kuvvetle bulunan kromatik sayıyla karşılaştırılır. Veri: v2.10'un KURGUSAL kataloğu ve `kayit_uret` ile üretilen KURGUSAL kayıtlar (300 öğrenci). Ölçüm (§ 8): Welsh–Powell V = 10⁶ derslik rastgele çakışma grafında (E ≈ 4·10⁶) 164,9 ms sürer, okunan komşu tam 2E'dir; aralık bölümleme 10⁶ sınavda 414,2 ms sürer ve her n'de salon = derinlik; n = 10 derslik 9 000 rastgele grafta Welsh–Powell'in en iyi (χ) sonucu verdiği grafların oranı yoğunluğa göre %88,0–%99,7, rastgele sıralı açgözlününki ise yalnız %60,5–%87,7.

Dosyalar (satır sayılarıyla): **`sinav.h`** (153) · **`sinav.c`** (667) · **`sinav_programi.c`** (396) · **`olcer_sinav.c`** (500) · `test_obs.c` (3305) · `test_kahin.c` (5708) · `Makefile` (772) · önceki sürümlerin bütün dosyaları · `ornek_veri/sinav_kayitlari.txt` (302 satır) · `testler/sinav_kotu.txt` ve `testler/sinav_kotu_katalog.txt` (taç grafı) · `testler/sinav_kucuk.txt` · `testler/sinav_bozuk.txt` · `olcum/renk.csv`, `olcum/derece.csv`, `olcum/salon.csv`, `olcum/kaba.csv`, `olcum/dagilim.csv`, `olcum/OLCUM_ORTAMI.txt` · `mini_obs_v2_11_ciktilar.txt` (1506 satır, gerçek çıktılar). Şekiller: `mini_obs_v2_11_tac.png`, `mini_obs_v2_11_salon.png`; grafik: `mini_obs_v2_11_olcum.png`.

Derleme: `make` (önceki programlar + **`sinav_programi`**, **`olcer_sinav`**), `make test`, `make olcum` (bu makinede 33 s), `make ornek`, `make asan`, `make valgrind`, `make temiz`. Bayraklar `-std=c17 -Wall -Wextra -pedantic -O2 -g`; 51 kaynak dosya `-O0 … -Os` düzeylerinde `-Werror` ile uyarısız. Çıkış kodları: 0; 1 (dosya okunamadı ya da biçim hatası, kayıt üretilemedi, bellek yetersiz, doğrulama hatası; testlerde uyuşmazlık); 2 (hatalı kullanım).

## 1. Amaç ve haftanın kavramıyla bağı

Hafta 12 açgözlü stratejiyi iki yüzüyle anlatır (Cormen vd., 2022; Kleinberg ve Tardos, 2006): kimi problemde yerel en iyi seçim **kanıtlanabilir biçimde** en iyi sonuca götürür (aralık çizelgeleme, aralık bölümleme, Huffman, Dijkstra, Kruskal), kimi problemde ise yalnızca hızlı bir **sezgiseldir** (graf boyama). Mini-OBS'nin sınav programı ikisini aynı çıktıda yan yana koyar:

- **Açgözlü sezgisel** (Konu: "Açgözlü sezgiseller: en iyiyi garanti etmeyen ama hızlı yöntemler (graf boyama, Welsh–Powell)"; Örnek 13): oturum ataması. Program açgözlü sonucu "en iyi" diye raporlamaz; bir **alt sınırla** (klik) birlikte yazar ve küçük örnekte **kaba kuvvetle** karşılaştırır (§ 4.2–4.4).
- **Karşı örnek** (ÖÇ 12.1; Hata Avcısı: "açgözlü ölçütün yanlış seçilmesi ve karşı örnekle sınanmaması"): taç grafında derece sırası işe yaramaz; Welsh–Powell 4, en iyi 2 oturum (§ 4.3, Şekil 1).
- **Aralık bölümleme** (Konu: "aralık çizelgeleme … ve aralık bölümleme (gereken salon sayısı)"; Örnek 3: "en az salon sayısı (öbekle)"): v2.6'nın öbeği (v2.10'da öncelik kuyruğu işlemleri eklendi) bitiş zamanlarını tutar; doğruluk "derinlik" alt sınırıyla kanıtlanır (Kleinberg ve Tardos, 2006; § 4.5).
- **Mühendis Gözüyle:** "Açgözlü çözüm ya kanıtlanır ya da karşı örnekle sınanır; sezgisel sonuçlar 'en iyi' diye raporlanmaz." Salon sayısı kanıtlanır ve programla doğrulanır; oturum sayısı alt sınır, üst sınır ve (küçük örnekte) kaba kuvvetle çerçevelenir.

Yol haritasındaki karşılığı (Tablo A.1): **H12 · v2.11 · Sınav oturumu ataması; en az salon sayısı · Açgözlü boyama, aralık bölümleme.**

## 2. v2.10'dan ne değişti?

| Konu | v2.10 (H11) | v2.11 (H12) |
|---|---|---|
| Sınav programı | — | **`sinav.h/.c`**: kayıt dosyası (`NO KOD [KOD …]`) okuyucu/yazıcı ve üreteç, çakışma grafı (ders çiftleri v2.9 karma tablosunda sayılır; ağırlık = ortak öğrenci), derece sırası (kararlı sayma sıralaması), ilk uyan boyama, Welsh–Powell, boyama denetimi, açgözlü klik (alt sınır), kaba kuvvet kromatik sayı (geri izleme), sınav süresi, aralık bölümleme (öbek), en çok eşzamanlı aralık (süpürme) |
| Graf | v2.10 CSR (yönlü önkoşul grafı) | aynı modül **yönsüz ve ağırlıklı** graf olarak kullanılır (değişiklik yok) |
| Öbek | öncelik kuyruğu (Kahn) | aynı işlemler salonların bitiş zamanları için (değişiklik yok) |
| Programlar | `ders_plani`, `olcer_graf`, `graf_uret` | + **`sinav_programi`** (çakışma grafı, oturumlar, alt/üst sınır, kaba kuvvet, salon planı), **`olcer_sinav`** (ölçüm ve renk sayısı dağılımı) |
| Testler | 414 birim; kâhin 675 383 denetim | 426 birim (+12 sınav); kâhin 678 664 denetim; `--hata-goster renk`, `--hata-goster sinir` |

Menü (`mini_obs`) ve önceki programların çıktıları değişmedi (v1.0'ın T2 oturumu yine yalnızca başlık ve arama istemi satırlarında farklıdır; `mini_obs_v2_11_ciktilar.txt`, Regresyon bölümü).

## 3. Mimari

| Modül / program | Sorumluluk | Bağımlılık |
|---|---|---|
| `sinav` (**yeni**) | kayıt verisi, çakışma grafı, renklendirme, alt sınır, kaba kuvvet, aralıklar | `graf` (CSR, yönsüz kurma), `onkosul` (katalog: kod → köşe, AKTS, dönem), `karma` (çift sayımı, numara tekliği), `obek` (salonlar), `ortak_rastgele` (üreteç), `metin`, `sayac` |
| `sinav_programi.c` (**yeni**) | komut satırı: oturumlar, sınırlar, kaba kuvvet, salon planı, doğrulama | `sinav`, `onkosul`, `graf`, `zamanlayici` |
| `olcer_sinav.c` (**yeni**) | ölçüm: Welsh–Powell ↔ rastgele sıra, aralık bölümleme ↔ süpürme, kaba kuvvet, renk sayısı dağılımı | `sinav`, `graf`, `deney`, `ortak_rastgele` |
| diğerleri | v2.10'dan aynen | — |

Makefile'da `sinav.o` `SINAV` grubundadır; testler ve iki yeni program onu `GRAF`, `KARMA` ve `SIRALAMA` gruplarıyla bağlar. `sinav` modülü öğrenci not kaydını (`obs.h`'nin `Ogrenci`'si) kullanmaz: v1.0 kaydında yalnız üç ders olduğu için çakışma grafı ayrı bir **ders kaydı** dosyasından kurulur (§ 4.1, § 11).

## 4. Algoritmalar ve veri yapıları

### 4.1 Kayıt verisi ve çakışma grafı

**Kayıt dosyası** öğrenci başına bir satırdır: `NO KOD [KOD …]` (`#` yorum, boş satırlar atlanır). Numara 1..10¹⁰ ve dosyada tek (karma kümesiyle denetlenir), kodlar katalogdadır (v2.10'un kod → köşe karma tablosu), bir satırda aynı kod iki kez olamaz, en çok 32 ders. Hatalar satır numarası ve Türkçe iletiyle bildirilir (çıkış 1). Örnek dosya `kayit_uret` ile üretildi (KURGUSAL; ortak LCG, tohum 42): her öğrenci rastgele bir dönemin katalog derslerini (her birini 7/8 olasılıkla) alır ve 1/3 olasılıkla önceki bir dönemden bir ders ekler (alttan ders).

**Çakışma grafı.** Köşeler en az bir öğrencisi olan derslerdir (kod sırası; rehber 14.2'nin "küçük köşe" kuralı yine "küçük ders kodu" demektir). Her öğrencinin k dersi için C(k, 2) çiftin her biri (a < b) v2.9'un **karma tablosunda** sayılır (anahtar a·V + b, değer ortak öğrenci sayısı); farklı anahtarlar kenarlardır ve CSR'ye yönsüz, ağırlıklı olarak yazılır. İş Σ C(k_ö, 2)'dir (k_ö: öğrencinin ders sayısı): ders başına öğrenci sayısından değil, öğrenci başına ders sayısından etkilenir. V×V'lik bir matris yerine karma tablosu kullanılır, çünkü kenar sayısı genelde V²'den çok küçüktür ve bellek sayılan çiftlerle orantılı kalır.

```
Katalog: ornek_veri/onkosul.txt · 48 ders
Kayıtlar: ornek_veri/sinav_kayitlari.txt · 300 öğrenci · 1665 kayıt (öğrenci başına 3..7 ders)
Çakışma grafı: 48 sınav (öğrencisi olan ders) · 469 kenar (ortak öğrencili ders çifti) · Σ C(k, 2) = 3927 çift sayıldı (karma tablosu, 3927 yoklama)
  en çok çakışan çift: BLM306–BLM308 (39 ortak öğrenci) · en büyük derece Δ = 36
Welsh–Powell sırası (derece azalan, eşitlikte küçük kod): ING101(36) BLM101(34) BLM104(34) BLM103(29) BLM201(29) MAT101(28) BLM204(25) ATA202(24) BLM208(24) BLM205(23) BLM306(23) BLM310(23) … (+36)
Oturum ataması (açgözlü renklendirme; okunan komşu 938): 12 oturum
  Oturum 1 (3 sınav): BLM201 ING101 TDL102
  Oturum 2 (4 sınav): BLM101 BLM204 BLM409 BLM410
  Oturum 3 (3 sınav): BLM104 BLM303 MAT101
  Oturum 4 (3 sınav): ATA202 BLM103 BLM301
  Oturum 5 (5 sınav): BLM208 BLM304 BLM402 IST201 MAT102
  Oturum 6 (5 sınav): BLM205 BLM306 BLM307 BLM401 ING102
  Oturum 7 (5 sınav): BLM305 BLM310 BLM405 MAT203 TDL101
  Oturum 8 (4 sınav): BLM309 BLM404 BLM411 MAT201
  Oturum 9 (4 sınav): BLM102 BLM202 BLM403 BLM406
  Oturum 10 (5 sınav): BLM206 BLM302 BLM407 BLM412 FIZ102
  Oturum 11 (6 sınav): BLM203 BLM210 BLM308 BLM408 FIZ101 IST301
  Oturum 12 (1 sınav): BLM312
Doğrulama: 469 çakışma kenarının hepsinde iki sınav farklı oturumda: EVET
…
```

Örnekte 300 öğrencinin 1 665 kaydından Σ C(k, 2) = 3 927 çift sayılır; bunlar 469 farklı ders çiftine (kenar) düşer (kenar başına ortalama 8,4 ortak öğrenci). 48 derslik grafın kenar yoğunluğu (kenar / olası çift) %41,6.

### 4.2 Oturum ataması: Welsh–Powell

```
algoritma WELSH-POWELL(G)                          ▷ Θ(V + E)
    sıra ← köşeler, derece AZALAN; eşitlikte KÜÇÜK numara (kod)   ▷ kararlı sayma sıralaması, Θ(V + Δ)
    her v için renk[v] ← yok
    i = 0 .. V − 1 için:
        v ← sıra[i]
        v'nin komşularının renklerini "yasak" diye damgala (damga = i)    ▷ derece(v) okuma
        renk[v] ← damgası i OLMAYAN en küçük renk                         ▷ ilk uyan (first fit)
    renk sayısı = en büyük renk + 1
```

- **Değişmez:** sıranın ilk i köşesi boyalıdır ve her kenarın boyalı iki ucu farklı renktedir. Yeni köşe, komşularının kullanmadığı bir rengi aldığı için değişmez korunur; sonda boyama geçerlidir (program her kenarı ayrıca denetler: "Doğrulama … EVET").
- **Ders kitabındaki anlatım** ("1. rengi al, listeyi baştan sona tara, 1. renge boyanmış hiçbir köşeye komşu olmayanları boya; sonra 2. renk …") **aynı boyamayı** verir: iki yöntemde de her köşe, kendisinden önce gelen komşularının kullanmadığı en küçük rengi alır. Renk renk tarama Θ(k·(V + E))'dir; damga dizisiyle tek geçiş Θ(V + E). Kâhin renk renk sürümünü komşuluk matrisiyle ayrıca yazar ve sonuçları karşılaştırır (§ 4.6).
- **Neden derece sırası?** Çok komşulu bir köşe sona kalırsa birçok renk yasaklanmış olur; büyük dereceliler önce boyanınca seçenek henüz boldur. Güvence (Welsh ve Powell, 1967): renk sayısı ≤ max_i min(d_i + 1, i) (i: köşenin sıradaki yeri, 1'den; d_i: derecesi) ≤ Δ + 1. Bu bir **üst sınırdır**, en iyiliğin güvencesi değildir.
- **Damga dizisi:** `yasak[c] == i + 1` ise c rengi i. köşenin bir komşusunda vardır. Damga her köşede farklı olduğu için dizi her adımda sıfırlanmaz; renk arama en çok derece(v) + 1 adımdır. Okunan komşu sayısı tam Σ derece = 2E'dir (sayaç; § 8.1).

```
Doğrulama: 469 çakışma kenarının hepsinde iki sınav farklı oturumda: EVET
Alt sınır: 11 derslik klik (her çifti çakışan dersler): BLM101 BLM102 BLM103 BLM104 BLM201 BLM203 BLM205 FIZ102 IST201 MAT201 MAT203
  → en az 11 oturum gerekir; açgözlü 12 (en iyiden en çok 1 fazla); üst sınır Δ + 1 = 37
```

Program açgözlü sonucu "en iyi" diye yazmaz: "en az 11 oturum gerekir; açgözlü 12 (en iyiden en çok 1 fazla)". Gerçek en iyi değer (χ) bu ikisinin arasındadır; 48 derste kaba kuvvet (§ 4.4) etkileşimli bir program için pratik değildir (kestirim § 8.3).

### 4.3 Açgözlü ne zaman kötü? Taç grafı

![Taç grafı](mini_obs_v2_11_tac.png)

*Şekil 1. `testler/sinav_kotu.txt`: A grubundan bir ve B grubundan bir ders alan 12 öğrenci; Ai ile Bi'yi (aynı sütun) alan öğrenci yoktur. Çakışma grafı **taç grafıdır** (K₄,₄'ten bir mükemmel eşleme çıkarılmış). (a) Bütün dereceler 3 olduğu için Welsh–Powell sırası kod sırasıdır (S1 S2 … S8) ve A, B dönüşümlü gelir; her yeni ders, önceki çiftin renklerini kullanan bir komşuya sahiptir → 4 oturum. (b) Kaba kuvvet: A grubu bir oturumda, B grubu ötekinde → χ = 2.*

```
Katalog: testler/sinav_kotu_katalog.txt · 8 ders
Kayıtlar: testler/sinav_kotu.txt · 12 öğrenci · 24 kayıt (öğrenci başına 2..2 ders)
Çakışma grafı: 8 sınav (öğrencisi olan ders) · 12 kenar (ortak öğrencili ders çifti) · Σ C(k, 2) = 12 çift sayıldı (karma tablosu, 13 yoklama)
  en çok çakışan çift: S1–S4 (1 ortak öğrenci) · en büyük derece Δ = 3
Welsh–Powell sırası (derece azalan, eşitlikte küçük kod): S1(3) S2(3) S3(3) S4(3) S5(3) S6(3) S7(3) S8(3)
Oturum ataması (açgözlü renklendirme; okunan komşu 24): 4 oturum
  Oturum 1 (2 sınav): S1 S2
  Oturum 2 (2 sınav): S3 S4
  Oturum 3 (2 sınav): S5 S6
  Oturum 4 (2 sınav): S7 S8
Doğrulama: 12 çakışma kenarının hepsinde iki sınav farklı oturumda: EVET
Alt sınır: 2 derslik klik (her çifti çakışan dersler): S1 S4
  → en az 2 oturum gerekir; açgözlü 4 (en iyiden en çok 2 fazla); üst sınır Δ + 1 = 4
Kaba kuvvet (geri izleme, k = 1, 2, …): kromatik sayı χ = 2 · 21 düğüm
  En iyi oturum 1: S1 S3 S5 S7
  En iyi oturum 2: S2 S4 S6 S8
Karşılaştırma: açgözlü 4 oturum, en iyi 2 → açgözlü EN İYİ DEĞİL
Salon planı (oturum = sınav günü; başlangıçlar KURGUSAL istekler: 09:00–15:00, ortak LCG tohum 11; süre AKTS'den: <= 4 → 60, 5 → 90, >= 6 → 120 dk):
  Oturum 1: 2 sınav · 1 salon (alt sınır: 09:00'da 1 sınav sürüyor)
    salon 1: S1 09:00–10:30 S2 15:00–16:30
  Oturum 2: 2 sınav · 1 salon (alt sınır: 10:00'da 1 sınav sürüyor)
    salon 1: S3 10:00–11:30 S4 13:00–14:30
  Oturum 3: 2 sınav · 1 salon (alt sınır: 10:30'da 1 sınav sürüyor)
    salon 1: S6 10:30–12:00 S5 12:00–13:30
  Oturum 4: 2 sınav · 2 salon (alt sınır: 14:30'da 2 sınav sürüyor)
    salon 1: S7 14:30–16:00
    salon 2: S8 14:30–16:00
En az salon sayısı: 2 (oturumların en büyüğü; alt sınır 2). Her oturumda salon = en çok eşzamanlı sınav: EVET; aynı salonda çakışan sınav yok: EVET
[çıkış kodu: 0]
```

Taç grafı açgözlü renklendirmenin bilinen kötü örneğidir: Kₙ,ₙ'den bir mükemmel eşleme çıkarılınca bu sırayla açgözlü n renk kullanır, oysa graf iki parçalıdır (χ = 2). Derece sırası burada yardım etmez, çünkü bütün dereceler eşittir ve eşitlik kuralı (küçük kod) kötü sırayı seçer. **Sıra her şeydir:** aynı grafta A'lar önce gelirse ilk uyan boyama 2 renk bulur (birim testi). Bu, haftanın "karşı örnekle sınama" ilkesinin Mini-OBS'deki karşılığıdır; kaba kuvvet χ = 2'yi yalnız 21 düğüm gezerek bulur.

### 4.4 Kaba kuvvet ve alt sınır

**Kaba kuvvet (`kromatik_kaba`).** k = 1, 2, … için geri izlemeyle k-renklendirme aranır: köşeler 0, 1, … sırasıyla renk alır, her atamada önceki komşularla çakışma denetlenir (komşuluk 32 bitlik maskelerde; V ≤ 30). **Simetri kırma:** renklerin adları önemsiz olduğu için i. köşe en çok "şimdiye kadar kullanılan en büyük renk + 1"i dener; aynı boyamanın k! adlandırması bir kez sayılır. İlk başarılı k kromatik sayıdır (χ). Üsteldir (§ 8.3); program yalnızca ≤ 30 sınavda çalıştırır ("Kaba kuvvet: 48 sınav > 30 — üstel arama yapılmadı").

**Alt sınır (`klik_bul`).** Karşılıklı komşu k ders (klik) k farklı oturum ister: klik boyu ≤ χ. En büyük kliği bulmak da NP-zordur; açgözlü bir klik yeter: derece sırasındaki ilk en çok 32 köşenin her birinden başlayıp, kliğin hepsine komşu olan köşeler sırayla eklenir. Klik bir **alt**, Welsh–Powell bir **üst** sınırdır; ikisi eşitse açgözlü sonuç kanıtlanmış olarak en iyidir.

Küçük gerçekçi örnek (`testler/sinav_kucuk.txt`; 3. dönem dersleri ve alttan 2. dönem dersleri):

```
2401000001 BLM201 BLM203 BLM205
2401000002 BLM201 MAT201 IST201
2401000003 BLM203 MAT203 BLM102
2401000004 BLM205 MAT201 FIZ102
2401000005 IST201 MAT203 MAT102
2401000006 BLM201 FIZ102
2401000007 BLM102 MAT102
2401000008 BLM205 IST201 BLM102
2401000009 MAT201 MAT203
2401000010 BLM203 IST201 FIZ102
```

```
Welsh–Powell sırası (derece azalan, eşitlikte küçük kod): IST201(8) BLM203(6) BLM205(6) BLM102(5) BLM201(5) FIZ102(5) MAT201(5) MAT203(5) MAT102(3)
Oturum ataması (açgözlü renklendirme; okunan komşu 48): 5 oturum
  Oturum 1 (1 sınav): IST201
  Oturum 2 (3 sınav): BLM203 MAT102 MAT201
  Oturum 3 (2 sınav): BLM205 MAT203
  Oturum 4 (2 sınav): BLM102 BLM201
  Oturum 5 (1 sınav): FIZ102
Doğrulama: 24 çakışma kenarının hepsinde iki sınav farklı oturumda: EVET
Alt sınır: 5 derslik klik (her çifti çakışan dersler): BLM201 BLM203 BLM205 FIZ102 IST201
  → en az 5 oturum gerekir; açgözlü 5 (en iyiden en çok 0 fazla); üst sınır Δ + 1 = 9
Kaba kuvvet (geri izleme, k = 1, 2, …): kromatik sayı χ = 5 · 83 düğüm
  En iyi oturum 1: BLM102 BLM201
  En iyi oturum 2: BLM203 MAT102 MAT201
  En iyi oturum 3: BLM205 MAT203
  En iyi oturum 4: FIZ102
  En iyi oturum 5: IST201
Karşılaştırma: açgözlü 5 oturum, en iyi 5 → açgözlü EN İYİ
```

Burada klik 5 = açgözlü 5: kaba kuvvet çalışmadan da açgözlü sonucun en iyi olduğu bellidir; kaba kuvvet 83 düğümde χ = 5'i doğrular. Öğrenci sayısı arttıkça alttan alınan dersler dönemleri birbirine bağlar ve çakışma grafı tam grafa yaklaşır: `--uret 2000` ile 48 dersin 1 059 çifti çakışır (olası 1 128 çift; kenar yoğunluğu %93,9); açgözlü 34, klik 33 oturum (`mini_obs_v2_11_ciktilar.txt`, bölüm 3). Gerçek bir fakültede bu yüzden sınav dönemi günlere ve saat dilimlerine birlikte bölünür (§ 11).

### 4.5 En az salon: aralık bölümleme

Oturum bir **sınav günüdür**: aynı oturumdaki sınavların ortak öğrencisi olmadığı için saatleri serbestçe çakışabilir; gün içinde gereken salon sayısını aynı anda süren sınavlar belirler. Her sınav bir yarı açık aralıktır: [başlangıç, bitiş) dakika. Başlangıçlar KURGUSAL isteklerdir (09:00–15:00 arası yarım saatlik dilimler; ortak LCG, tohum 11); süre AKTS'den gelir (≤ 4 AKTS → 60, 5 → 90, ≥ 6 → 120 dakika).

```
algoritma ARALIK-BÖLÜMLEME(a[1..n])                 ▷ Θ(n log n)
    a'yı başlangıca göre sırala (eşitlikte bitiş, kimlik)
    Ö ← boş en küçük öbek (salonların BİTİŞ zamanları)   ▷ v2.6 öbeği, v2.10 öncelik kuyruğu
    k ← 0
    her a[i] için (sırayla):
        Ö boş değil ve Ö.en_küçük ≤ a[i].başlangıç ise    ▷ yarı açık: biten salon hemen kullanılır
            s ← Ö'den çıkar (en erken boşalan salon)
        değilse
            s ← yeni salon (k ← k + 1)
        a[i]'yi s'ye koy;  s'nin bitişi ← a[i].bitiş;  s'yi Ö'ye ekle
```

**Neden en iyi?** *Derinlik* d, aynı anda süren en çok sınav sayısıdır; herhangi bir program en az d salon ister (o anda süren d sınav ayrı salonlardadır). Algoritma yeni salonu yalnızca **bütün açık salonlar doluyken** açar: k. salon a[i] için açıldığında öbekteki en erken bitiş a[i].başlangıç'tan büyüktür, yani açık k − 1 salonun her birinde a[i].başlangıç anında süren bir sınav vardır (hepsi daha önce başlamıştır). O anda a[i] ile birlikte k sınav sürer: k ≤ d. Demek ki k = d (Kleinberg ve Tardos, 2006, bölüm 4.1). Program bu kanıtın iki ucunu ayrı ayrı hesaplar: `salon_ata` (öbek) ve `en_cok_cakisma` (olayların süpürmesi: bitiş olayı aynı andaki başlangıçtan **önce** işlenir); ikisinin eşitliği her oturumda yazılır ("alt sınır: 11:00'da 3 sınav sürüyor").

![Salon planı](mini_obs_v2_11_salon.png)

*Şekil 2. Örnek programın en çok salon isteyen oturumu (Oturum 5): üç salon, 11:00'da üç sınav aynı anda sürer (kesikli çizgi). BLM208 10:30'da biter, IST201 11:00'da aynı salonda başlar; BLM402 ve MAT102 başka salonlardadır.*

```
Salon planı (oturum = sınav günü; başlangıçlar KURGUSAL istekler: 09:00–15:00, ortak LCG tohum 11; süre AKTS'den: <= 4 → 60, 5 → 90, >= 6 → 120 dk):
  Oturum 5: 5 sınav · 3 salon (alt sınır: 11:00'da 3 sınav sürüyor)
    salon 1: BLM208 09:00–10:30 IST201 11:00–12:00 BLM304 13:00–15:00
    salon 2: BLM402 10:00–12:00
    salon 3: MAT102 11:00–13:00
…
En az salon sayısı: 3 (oturumların en büyüğü; alt sınır 3). Her oturumda salon = en çok eşzamanlı sınav: EVET; aynı salonda çakışan sınav yok: EVET
```

**Sınır koşulu:** yarı açık aralıkta "salon boş" denetimi `bitiş ≤ başlangıç`'tır. `<` yazılırsa 10:30'da biten salona 10:30'da başlayan sınav konamaz ve salon sayısı derinlikten büyük çıkabilir — kasıtlı hata `--hata-goster sinir`'in yakaladığı yanılgı (§ 9).

### 4.6 Kâhinler

| Sınanan | Kâhin |
|---|---|
| `welsh_powell` (`derece_sirasi` + `ardisik_boya`) | ders kitabındaki **renk renk** Welsh–Powell: komşuluk **matrisi**, derece sırası seçmeyle (kararlı), her renk için listeyi baştan tarayıp o renge boyanmış hiçbir köşeye komşu olmayanları boyar — aynı renkler, aynı renk sayısı |
| `ardisik_boya` (rastgele sıra) | aynı matris üzerinde verilen sırayla doğrudan ilk uyan seçim; boyama geçerli |
| `kromatik_kaba` | **bağımsız kümeler üzerinden altküme DP'si**: χ(S) = 1 + min χ(S ∖ I), I ⊆ S bağımsız (O(3^V)); aynı χ, bulunan boyama geçerli ve χ renkli |
| `klik_bul` | bulunan kümenin her çifti komşu; klik ≤ χ ≤ Welsh–Powell |
| `salon_ata`, `en_cok_cakisma` | her tamsayı anda süren aralıkların **doğrudan sayımı**: en büyük sayı = derinlik = salon; aynı salonda kesişen iki aralık yok; her aralık bir salonda |
| `kayit_oku`, `cakisma_kur` | rastgele kayıt **dosyası** (yorum, boş satır, karışık sıra): ortak öğrenci sayıları V×V matriste doğrudan sayılır — aynı kenarlar ve ağırlıklar, Σ C(k, 2) |
| sayaçlar | `ardisik_boya`: okunan komşu = 2E |

Kâhin graflar V = 0..10 köşeli, kenar olasılığı her denemede rastgeledir (0..1); aralık kümeleri 0..12 aralıklıdır (küçük tamsayı uçlar, çok eşitlik). Uyuşmazlıkta girdi, V ≤ 4 köşeli bütün graflar (ya da ≤ 3 aralıklı bütün kümeler) denenerek **küçültülür** ve en küçük karşı örnek basılır (§ 9).

## 5. Bellek sahipliği

| Yapı | Kim ayırır | Kim serbest bırakır | Yaşam süresi |
|---|---|---|---|
| `KayitVerisi` (`no`, `bas`, `ders`) | `kayit_oku` / `kayit_uret` (büyüme × 2, `realloc` geçici işaretçiyle; hata yolunda hepsi geri verilir) | `kayit_verisi_birak` | program boyunca |
| `CakismaGrafi` (`ders`, `ogrenci`, `g`) | `cakisma_kur` (çift sayımının karma tablosu kendi içinde ayrılır ve bırakılır) | `cakisma_birak` | program boyunca |
| boyama ve sıra dizileri (`sira`, `renk`, `klik`) | çağıran (en az V öğe) | çağıran | çağrı boyunca |
| `yasak` damga dizisi, sayma dizisi, aralık kopyası, salon öbeği, olay dizisi | ilgili fonksiyon | aynı fonksiyon (her çıkış yolunda) | çağrı boyunca |
| `Aralik` ve salon dizileri | `sinav_programi` (oturum oturum) | `sinav_programi` | oturum boyunca |
| önceki sürümlerin yapıları | v2.10 § 5 | v2.10 § 5 | — |

`kayit_oku` biçim hatasında yarım veri bırakmaz (`kv.no == NULL`; birim testi altı hatalı girdide denetler). `make asan` (yeni programlar, 3 000 öğrencilik üretilmiş dosya, bozuk dosya, kasıtlı hata kipleri dahil) temiz; `make valgrind` 73 çalıştırmanın hepsinde "ERROR SUMMARY: 0 errors" ve "definitely lost: 0 bytes" (yeni ve test çalıştırmaları):

```
valgrind ./obs_test_vg → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 20 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 3 --hata-goster renk → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./test_kahin_vg --deneme 3 --hata-goster sinir → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./sinav_programi_vg → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./sinav_programi_vg testler/sinav_kotu.txt --katalog testler/sinav_kotu_katalog.txt --kaba → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./sinav_programi_vg testler/sinav_kucuk.txt --kaba → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./sinav_programi_vg --uret 500 --kaydet vg_kayit.txt --ozet → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./sinav_programi_vg testler/sinav_bozuk.txt → çıkış 1 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_sinav_vg wp --n 2,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_sinav_vg salon --n 1,300 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_sinav_vg kaba --n 7 --deneme 2 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_sinav_vg dagilim --n 7 --p 50 --deneme 10 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./kayit_vg ornek_veri/ogrenciler.csv --sinir 2 --komutlar ornek_veri/islem_komutlari.txt → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
valgrind ./olcer_yapi_vg gecmis_sinirli --n 300 --k 7 --tekrar 1 → çıkış 0 · ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) · definitely lost: 0 bytes (All heap blocks were freed -- no leaks are possible)
```

## 6. Kullanım

```
./sinav_programi [kayitlar.txt] [--katalog dosya] [--uret N [--tohum T] [--kaydet dosya]]
                 [--saat-tohum S] [--kaba] [--ozet]
./olcer_sinav İŞLEM [--n N1,N2,…] [--derece D] [--p P1,P2,…] [--deneme K] [--tekrar T]
              [--tohum S] [--csv dosya.csv [--ekle]]      İŞLEM: wp rastgele salon derinlik kaba dagilim
```

Varsayılan kayıt dosyası `ornek_veri/sinav_kayitlari.txt`, katalog `ornek_veri/onkosul.txt`'tir (v2.10). `--uret N` kayıtları dosya yerine üretir (`--kaydet` ile yazar); `--kaba` ≤ 30 sınavda kromatik sayıyı bulur; `--ozet` oturum listelerini ve salon planını yazmaz. Süreler yalnız stderr'e yazılır. Hatalar:

```
$ ./sinav_programi testler/sinav_bozuk.txt; ./sinav_programi --uret 5 testler/sinav_kucuk.txt; ./sinav_programi --katalog testler/graf_kucuk.txt --uret 3; ./sinav_programi yok.txt
Hata: testler/sinav_bozuk.txt okunamadı: dosya biçimi hatalı (satır 4: bilinmeyen ders kodu: BLM999)
Kullanım: ./sinav_programi [kayitlar.txt] [--katalog dosya] [--uret N [--tohum T] [--kaydet dosya]] [--saat-tohum S] [--kaba] [--ozet]
Hata: kayıt üretilemedi (katalogda dönem yok ya da bellek yetersiz)
Hata: yok.txt okunamadı: dosya bulunamadı
[çıkış kodu: 1]
```

## 7. Tasarım kararları

1. **Çakışma grafı karma tablosuyla.** Ders çiftleri v2.9'un tablosunda sayılır; bellek kenar sayısıyla orantılıdır ve aynı tablo v3.0'da gerçek kayıt hacmine ölçeklenir. V×V matris yalnız kâhindedir.
2. **Derece sırası kararlı sayma sıralamasıyla** (v2.6): dereceler 0..Δ aralığında küçük tamsayılardır; Θ(V + Δ), karşılaştırma yok ve eşitlikte küçük kod kendiliğinden korunur (rehber 14.2).
3. **İlk uyan boyama damga dizisiyle:** renk renk taramanın k geçişi yerine tek geçiş; her köşede yasak renkler O(derece) zamanda işaretlenir ve dizi sıfırlanmaz.
4. **Açgözlü sonuç sınırlarıyla raporlanır** (Mühendis Gözüyle): klik (alt), Welsh–Powell (üst) ve Δ + 1; "en iyi" sözcüğü yalnız kaba kuvvet ya da klik eşitliği kanıtladığında yazılır.
5. **Oturum = gün, salon = gün içi aralık bölümleme.** İki açgözlü problem ayrı tutulur: renklendirme öğrenci çakışmasını, aralık bölümleme salon kapasitesini çözer. Salon sayısının en iyiliği kanıtlanabildiği için program onu ayrı bir süpürmeyle doğrular ve eşitsizlikte 1 ile çıkar.
6. **Yarı açık aralıklar ve `≤`.** 10:30'da biten salon 10:30'da yeniden kullanılır; süpürmede de bitiş olayı başlangıçtan önce işlenir. İki yöntemin aynı sınır kuralını kullanması eşitliği anlamlı kılar.
7. **Kaba kuvvet sınırı 30 ders.** Komşuluk 32 bitlik maskelerde tutulur; ölçümde 28 derste graf başına ≈ 34,8 ms (§ 8.3). Daha büyük örneklerde açgözlü + alt sınır yeterli bilgi verir.

## 8. Ölçümler

**Düzen:** `-O2`; her nokta için önce sayaç açık bir çalıştırma (renk sayısı, kenar, karşılaştırma, taşıma, düğüm), sonra 1 ısınma + 5 tekrar (kaba kuvvette 3), ortanca; veri hazırlama (graf ve aralık üretimi, CSR) süre dışında. Çakışma grafı: V köşe, ortalama derece D (varsayılan 8; kenarlar düzgün rastgele çiftler, yinelenenler atılır). Aralıklar: n sınav, başlangıç düzgün [0, 10n) dakika, süre 60/90/120 (ortalama eşzamanlılık ≈ 9). Makine: Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine), L2 2 MiB, L3 33 MiB; gcc 13.3.0, glibc 2.39; tarih 2026-10-22 08:30. `make olcum` 33 s sürdü; en büyük noktalarda süreç belleğinin tepesi 116 MiB (Welsh–Powell, V = 10⁶) ve 44 MiB (aralık bölümleme, n = 10⁶). Ölçüm sırasında makinenin 1 dakikalık yük ortalaması başta 1,00, sonda 1,56 idi (2 çekirdek; aynı anda başka ajanların derleme ve ölçümleri çalışıyordu: süreler gürültülüdür; renk sayıları, kenar, karşılaştırma, taşıma ve düğüm sayaçları değildir).

![Ölçümler](mini_obs_v2_11_olcum.png)

*Şekil 3. Sol üst: süre ↔ ders (V) ya da sınav (n) sayısı (log–log; noktalı çizgi eğim 1). Sağ üst: V = 10⁵'te ortalama dereceye göre renk sayısı ve sınırları. Sol alt: kaba kuvvetin graf başına süresi ve düğüm sayısı (p = %50). Sağ alt: n = 10 derslik rastgele graflarda açgözlünün en iyi (χ) olduğu grafların oranı.*

### 8.1 Ders sayısına göre süre (Welsh–Powell)

| V (ders) | E | Welsh–Powell | ns / (V + E) | rastgele sıra | renk (WP) | renk (rastgele) | klik (alt sınır) | WP sınırı | Δ + 1 |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 3 989 | 28,4 µs | 5,7 | 22,8 µs | 6 | 7 | 3 | 16 | 18 |
| 2 000 | 7 983 | 75,3 µs | 7,5 | 71,1 µs | 6 | 7 | 3 | 17 | 19 |
| 5 000 | 19 988 | 212,9 µs | 8,5 | 256,5 µs | 7 | 7 | 3 | 17 | 21 |
| 10 000 | 39 985 | 432,0 µs | 8,6 | 490,1 µs | 7 | 7 | 3 | 18 | 23 |
| 20 000 | 79 981 | 912,4 µs | 9,1 | 973,7 µs | 7 | 8 | 2 | 19 | 24 |
| 50 000 | 199 983 | 2,4 ms | 9,8 | 7,4 ms | 7 | 8 | 2 | 20 | 24 |
| 100 000 | 399 985 | 5,1 ms | 10,2 | 7,3 ms | 7 | 8 | 2 | 21 | 25 |
| 200 000 | 799 977 | 13,9 ms | 13,9 | 22,8 ms | 7 | 8 | 3 | 22 | 27 |
| 500 000 | 1 999 979 | 49,7 ms | 19,9 | 68,0 ms | 7 | 8 | 2 | 22 | 26 |
| 1 000 000 | 3 999 988 | 164,9 ms | 33,0 | 228,5 ms | 7 | 8 | 2 | 23 | 26 |

*Tablo 1. Rastgele çakışma grafı, ortalama derece 8 (`olcum/renk.csv`). Her V'de okunan komşu (kenar sayacı) tam 2E; her boyama geçerli (ölçücü denetler). "WP sınırı": max_i min(d_i + 1, i).*

**Yorum.**

- **Süre doğrusaldır, sabit çarpan önbellekle büyür.** Log–log eğim V = 10³ → 10⁵'te 1,13, 10³ → 10⁶'da 1,25; (V + E) başına süre 5,7 ns'den (V = 1 000) 33,0 ns'ye (V = 1 000 000) çıkar. Okunan komşu sayısı her V'de tam 2E'dir (işin miktarı Θ(V + E)); `renk[komşu]` erişimleri rastgele köşelere gider ve çalışma kümesi (CSR ≈ 4(V + 2E) bayt + dört V öğelik dizi) önbelleği aşınca kaçırmalar artar — v2.10'daki planla aynı ders.
- **Renk sayısı neredeyse sabittir:** ortalama derece 8 sabitken Welsh–Powell 6, 7 renk, rastgele sıra 7, 8 renk kullanır (rastgele sıra 10 noktadan 8 tanesinde daha kötü). Δ + 1 sınırı ise V ile büyür (18 → 26): en büyük derece büyür, renk sayısını ise ortalama derece belirler.
- **Alt sınır zayıftır.** Rastgele seyrek grafta klik yalnız 2–3 köşedir; χ bu graflarda bilinmez (NP-zor) ve klik ile Welsh–Powell arasındaki aralıkta bir yerdedir. Büyük örnekte açgözlü sonucun ne kadar iyi olduğu ölçülemez; bu yüzden küçük graflarda kaba kuvvetle karşılaştırılır (§ 8.4).

| ortalama derece D | E | klik (alt sınır) | renk (WP) | renk (rastgele) | WP sınırı | Δ + 1 | WP ortanca | WP en az | rastgele ortanca | rastgele en az |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 2 | 100 000 | 2 | 4 | 5 | 10 | 12 | 2,8 ms | 2,2 ms | 3,5 ms | 3,2 ms |
| 4 | 199 999 | 2 | 5 | 7 | 14 | 15 | 3,4 ms | 3,2 ms | 5,3 ms | 5,0 ms |
| 8 | 399 985 | 2 | 7 | 8 | 21 | 25 | 5,4 ms | 5,2 ms | 8,1 ms | 7,9 ms |
| 16 | 799 931 | 3 | 10 | 11 | 32 | 38 | 25,3 ms | 12,9 ms | 16,7 ms | 15,9 ms |
| 32 | 1 599 719 | 3 | 14 | 16 | 53 | 59 | 27,9 ms | 22,4 ms | 31,7 ms | 31,5 ms |
| 64 | 3 198 924 | 3 | 22 | 24 | 91 | 103 | 49,8 ms | 45,2 ms | 57,6 ms | 56,9 ms |

*Tablo 2. V = 10⁵, ortalama derece D (`olcum/derece.csv`). Renk sayıları ve sınırlar sayaçtır; süreler gürültülüdür (ortanca ve en kısa tekrar birlikte verildi).*

D = 64'te Welsh–Powell 22 renk kullanır; Δ + 1 = 103, Welsh–Powell sınırı 91: güvenceler gerçek sonucun çok üstündedir. Derece sırası her D'de rastgele sıradan 1–2 renk daha azını kullanır. Süre E ile büyür (D = 2 → 64: E 32 kat, Welsh–Powell ortancası 17,8 kat). D = 16 noktasında Welsh–Powell'in ortancası rastgele sıranınkinden büyük çıktı; aynı noktanın en kısa tekrarı (12,9 ms) rastgele sıranın en kısasından (15,9 ms) küçüktür ve tekrarlar arasında iki katlık fark vardır: makine yükünün gürültüsüdür (iki yöntem aynı sayıda komşu okur).

### 8.2 Sınav sayısına göre süre (aralık bölümleme)

| n (sınav) | salon = derinlik | aralık bölümleme | ns / (n log₂ n) | süpürme | öbek karşılaştırması | karşılaştırma / n | öbek taşıması |
|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 000 | 20 | 202,8 µs | 20,35 | 119,0 µs | 8 373 | 8,37 | 9 143 |
| 2 000 | 20 | 447,2 µs | 20,39 | 282,6 µs | 17 284 | 8,64 | 18 635 |
| 5 000 | 21 | 1,3 ms | 20,42 | 864,9 µs | 43 965 | 8,79 | 47 150 |
| 10 000 | 22 | 2,7 ms | 20,58 | 1,7 ms | 91 129 | 9,11 | 95 600 |
| 20 000 | 24 | 4,4 ms | 15,27 | 3,6 ms | 186 853 | 9,34 | 193 745 |
| 50 000 | 25 | 12,1 ms | 15,50 | 10,4 ms | 456 400 | 9,13 | 479 435 |
| 100 000 | 25 | 26,8 ms | 16,16 | 21,4 ms | 940 046 | 9,40 | 974 852 |
| 200 000 | 26 | 71,4 ms | 20,29 | 44,7 ms | 1 878 207 | 9,39 | 1 943 930 |
| 500 000 | 26 | 198,7 ms | 20,99 | 127,1 ms | 4 804 880 | 9,61 | 4 907 675 |
| 1 000 000 | 29 | 414,2 ms | 20,78 | 282,9 ms | 9 758 355 | 9,76 | 9 919 797 |

*Tablo 3. n sınav aralığı (`olcum/salon.csv`). Her n'de salon sayısı süpürmeyle bulunan derinliğe eşit (sağlama). Öbek karşılaştırması ve taşıması sayaçtır; sıralama (`qsort`) sayılmaz.*

- **Θ(n log n):** süre n = 1 000 ile 1 000 000 arasında log–log eğim 1,10 (süpürme 1,13); süreye `qsort` hâkimdir (süpürme de 2n olayı sıralar; n = 10⁶'da süresi aralık bölümlemeninkinin %68 kadarıdır). (n log₂ n) başına süre 15,3–21,0 ns arasında dalgalanır; n ile belirgin bir eğilimi yoktur.
- **Öbek işi n log k'dir, n log n değil.** Öbekte en çok k = salon sayısı kadar öğe vardır; aralık başına karşılaştırma 8,37 (n = 1 000) ile 9,76 (n = 1 000 000) arasında kalır, çünkü derinlik yalnız 20 → 29 büyür (log₂ k ≈ 4,3–4,9; ekleme ve çıkarma birlikte birkaç düzey).
- **Derinlik yavaş büyür:** ortalama eşzamanlılık ≈ 9 iken en çok eşzamanlılık n büyüdükçe uç değer olarak artar (20 → 29).

### 8.3 Kaba kuvvet: üstel büyüme

| n (ders) | graf | ortalama χ | düğüm / graf | süre / graf | düğüm artışı (n − 2 → n) | ns / düğüm |
|--:|--:|--:|--:|--:|--:|--:|
| 4 | 20 | 2,30 | 12 | 69 ns | — | 5,9 |
| 6 | 20 | 3,00 | 29 | 162 ns | 2,5 | 5,5 |
| 8 | 20 | 3,70 | 67 | 397 ns | 2,3 | 6,0 |
| 10 | 20 | 3,90 | 109 | 782 ns | 1,6 | 7,2 |
| 12 | 20 | 4,30 | 291 | 2,6 µs | 2,7 | 8,8 |
| 14 | 20 | 4,95 | 1 291 | 16,4 µs | 4,4 | 12,7 |
| 16 | 20 | 5,15 | 4 553 | 52,5 µs | 3,5 | 11,5 |
| 18 | 20 | 5,55 | 4 836 | 57,2 µs | 1,1 | 11,8 |
| 20 | 20 | 5,90 | 24 344 | 252,7 µs | 5,0 | 10,4 |
| 22 | 20 | 6,20 | 101 280 | 1,2 ms | 4,2 | 11,6 |
| 24 | 20 | 6,45 | 134 119 | 1,6 ms | 1,3 | 11,9 |
| 26 | 20 | 6,75 | 654 439 | 9,3 ms | 4,9 | 14,2 |
| 28 | 20 | 7,00 | 2 290 412 | 34,8 ms | 3,5 | 15,2 |

*Tablo 4. n köşeli, kenar olasılığı %50 olan 20 rastgele graf için toplam süre ve düğüm (denenen renk ataması) sayısı (`olcum/kaba.csv`).*

Düğüm sayısı n = 16 → 28 aralığında her ders için ortalama 1,68 kat artar (hesap, Tablo 4'ten); n = 28'de graf başına 34,8 ms, düğüm başına 15,2 ns. Aynı büyümeyle örnek katalogun 48 sınavı için graf başına ≈ 73·10⁹ düğüm ve ≈ 18 dakika gerekirdi (**kestirim**: büyüme oranı ve düğüm süresi n ≤ 28'den dışa çekildi; gerçek grafın yoğunluğu %50 değil, ölçülmedi). Düğüm artışı düzgün değildir (ör. n = 16 → 18'de 1,1, 20 → 22'de 4,2 kat): aramanın kaç k değerini denediği ve χ'nin ne zaman bir artacağı grafa bağlıdır. Ortalama χ ders sayısıyla yavaş büyür; zor olan χ'yi bulmak değil, k − 1 rengin **yetmediğini** kanıtlamaktır (bütün ağaç gezilir).

### 8.4 Renk sayısı dağılımı: açgözlü ne sıklıkla en iyi?

| p (kenar olasılığı) | χ ort. | WP ort. | rastgele ort. | WP = χ | rastgele = χ | WP − χ = 1 / 2 / ≥ 3 | en büyük WP − χ | klik = χ | kaba düğüm ort. |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| %10 | 2,11 | 2,14 | 2,28 | %97,4 | %83,1 | 26 / 0 / 0 | 1 | %98,6 | 35,5 |
| %20 | 2,62 | 2,67 | 2,89 | %94,9 | %73,0 | 51 / 0 / 0 | 1 | %92,9 | 65,4 |
| %30 | 3,05 | 3,13 | 3,38 | %92,7 | %68,4 | 73 / 0 / 0 | 1 | %93,1 | 96,6 |
| %40 | 3,54 | 3,63 | 3,90 | %91,1 | %64,5 | 89 / 0 / 0 | 1 | %92,2 | 139,9 |
| %50 | 3,98 | 4,10 | 4,40 | %88,0 | %60,5 | 120 / 0 / 0 | 1 | %90,2 | 163,6 |
| %60 | 4,51 | 4,61 | 4,92 | %90,7 | %61,6 | 92 / 1 / 0 | 2 | %93,6 | 197,2 |
| %70 | 5,21 | 5,27 | 5,57 | %94,2 | %65,7 | 58 / 0 / 0 | 1 | %94,4 | 215,4 |
| %80 | 6,05 | 6,08 | 6,31 | %97,3 | %74,5 | 27 / 0 / 0 | 1 | %98,0 | 235,9 |
| %90 | 7,36 | 7,36 | 7,49 | %99,7 | %87,7 | 3 / 0 / 0 | 1 | %99,6 | 237,7 |

*Tablo 5. n = 10 ders, her p için 1000 rastgele graf (`olcum/dagilim.csv`); χ kaba kuvvetle. "rastgele": rastgele sıralı ilk uyan boyama.*

- Welsh–Powell'in en iyi olduğu grafların oranı %88,0 (p = %50) ile %99,7 (p = %90) arasındadır; 9 000 graftan 539 tanesinde 1, 1 tanesinde 2 fazla renk kullanır (2 fark yalnız p = %60'ta). En kötü yoğunluk orta yoğunluktur: seyrek grafta renk az, yoğun grafta graf neredeyse tam ve seçenek yoktur.
- Rastgele sıralı açgözlünün en iyi olduğu grafların oranı yalnız %60,5–%87,7; 97 grafta 2 fazla renk kullanır: **derece sırası** sezgiselin kalitesini belirgin biçimde artırır.
- Açgözlü kliğin χ'ye eşit olduğu grafların oranı %90,2–%99,6: küçük graflarda açgözlü klik çoğu zaman en iyiliği kaba kuvvete gerek kalmadan kanıtlar.
- Küçük graflar iyimser bir resim verir; taç grafı (§ 4.3) gibi yapılandırılmış girdiler sezgiseli çok daha kötü duruma düşürebilir. Bu dağılım "ortalama" davranıştır, güvence değildir.

### 8.5 Sınırlılıklar

Süreler paylaşılan bir sanal makinede yük altında ölçüldü; renk sayıları, kenar, karşılaştırma, taşıma ve düğüm sayaçları makineden bağımsızdır. Rastgele çakışma grafı gerçek ders kayıtlarından farklıdır (gerçek graflarda dönem içi dersler kümeler oluşturur; § 4.4'teki 2 000 öğrencilik örnek neredeyse tam graftır). Büyük graflarda χ bilinmediği için açgözlünün kalitesi yalnız n = 10'da ölçüldü. 48 derslik kaba kuvvet süresi kestirimdir.

## 9. Testler

- **Birim testleri** (`obs_test`): `426 doğrulama: 37 kural + 22 metin + 24 yapı + 16 dosya + 11 üreteç + 11 sayaç + 13 yinelenen + 16 seçmeli + 27 arama + 26 sıralama + 23 böl-fethet + 19 öbek-doğrusal + 79 bağlı liste + 29 yığın-kuyruk + 36 karma-desen + 25 graf-önkoşul + 12 sınav`. Sınav testleri: taç grafı (Welsh–Powell sırası S1 … S8, 4 renk; A'lar önce gelirse 2 renk; kaba kuvvet χ = 2); P4 yolu (0, 3, 1, 2 sırasıyla 3 renk, derece sırasıyla 2); derece sırasının kararlılığı (yıldız + yalıtık köşeler); kaba kuvvet K₄ → 4, C₅ → 3, kenarsız → 1, V > 30 → −1; geçersiz boyamanın reddi; arka arkaya iki sınavın aynı salonu kullanması (yarı açık); on aralıklı ders kitabı örneği (derinlik 3 → 3 salon, aynı salonda çakışma yok); sınav süreleri; kayıt dosyasından ortak öğrenci ağırlıkları (Σ C(k, 2) = 5); altı biçim hatası (satır numarası ve ileti; yarım veri bırakılmaz); dönemsiz katalogda üretecin reddi; üreteç belirliliği ve dosya gidiş-dönüşü; örnek veri (48 sınav, geçerli boyama, klik ≤ açgözlü).
- **Kâhin testleri** (`test_kahin`): 300 denemede 678 664, 1 000 denemede 2 275 138 denetim (sınav: 10 938), uyuşmazlık yok.
- **Kasıtlı hatalar.** (a) `--hata-goster renk` — Welsh–Powell'in yaygın yanlış okunuşu: her renk turunda yalnız turun **ilk** köşesine komşuluk denetlenir (aynı renge boyanan öbür köşelere bakılmaz). Kâhin geçersiz boyamayı yakalar; V ≤ 4 köşeli bütün graflar denenerek en küçük karşı örnek basılır (4 köşe, 2 kenar: 0–3 ve 1–2; sıra 0 1 2 3, 1 ve 2 ilk köşe 0'a komşu değil → ikisi de 1. renge):

```
$ ./test_kahin --hata-goster renk
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : welsh_powell
  n          : 10
  Beklenen   : 2 renk (renk renk tarama, matris): 0 0 0 0 0 0 1 0 0 1
  Bulunan    : 2 renk, GEÇERSİZ: 0 0 0 0 0 0 1 0 0 0
  En küçük karşı örnek (4 köşe, 2 kenar): 0–3 1–2
    welsh_powell: beklenen 2 renk (renk renk tarama, matris): 0 0 1 1; bulunan 2 renk, GEÇERSİZ: 0 0 0 1
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster renk
[çıkış kodu: 1]
```

  (b) `--hata-goster sinir` — salon yalnız `bitiş < başlangıç` ise yeniden kullanılır (kapalı aralık alışkanlığı); arka arkaya iki sınav iki salon ister:

```
$ ./test_kahin --hata-goster sinir
KÂHİN UYUŞMAZLIĞI (tohum 1)
  İşlev      : salon_ata / en_cok_cakisma
  n          : 9
  Beklenen   : 2 salon (her tamsayı anda sayım)
  Bulunan    : 3 salon, derinlik 2
  En küçük karşı örnek (2 aralık): [1, 2) [0, 1)
    salon_ata / en_cok_cakisma: beklenen 1 salon (her tamsayı anda sayım); bulunan 2 salon, derinlik 1
  Yeniden üretmek için: ./test_kahin --tohum 1 --deneme 1 --hata-goster sinir
[çıkış kodu: 1]
```

## 10. Ders notu için özet (Hafta 12 · Mini-OBS 2 adımı)

**Bu hafta:** Mini-OBS'ye **sınav programı** ekliyoruz. Ders kayıtlarından ortak öğrencisi olan dersleri birleştiren bir **çakışma grafı** kuruyoruz; **Welsh–Powell** açgözlü renklendirmesiyle sınavları oturumlara (günlere) atıyoruz ve sonucu bir **alt sınırla** (klik) birlikte raporluyoruz; küçük örneklerde **kaba kuvvetle** en iyi oturum sayısını (kromatik sayı) bulup açgözlü sonucu karşılaştırıyoruz ve açgözlünün **kötü** olduğu bir örnek (taç grafı) gösteriyoruz. Her gün için **aralık bölümleme** (öbekle) en az salon sayısını veriyor; bunun **en iyi** olduğunu derinlik (en çok eşzamanlı sınav) hesabıyla programda doğruluyoruz.

### Gereksinimler

- `sinav.h/.c`: kayıt dosyası (`NO KOD [KOD …]`; numara tek, kod katalogda, satırda aynı kod iki kez yok; hatada satır numarası, çıkış 1); çakışma grafı (her öğrencinin ders çiftleri **karma tablosunda** sayılır; ağırlık = ortak öğrenci; yönsüz CSR).
- Welsh–Powell: derece **azalan**, eşitlikte **küçük ders kodu** (kararlı sıralama); ilk uyan boyama; boyamanın geçerliliğini denetleyen fonksiyon.
- Alt sınır: açgözlü klik; üst sınır: Δ + 1 (ya da Welsh–Powell sınırı). Kaba kuvvet: geri izlemeyle k = 1, 2, … renklendirme (≤ 30 ders, en az 10 ders desteklenmeli).
- Aralık bölümleme: başlangıca göre sıralama + salon bitişlerinin **en küçük öbeği** (v2.6 öbeği); yarı açık aralık (`bitiş ≤ başlangıç` ise salon boş). Derinlik: olay süpürmesi (aynı anda bitiş önce).
- `sinav_programi`: oturumlar, doğrulama, alt/üst sınır, `--kaba` ile χ ve karşılaştırma, oturum oturum salon planı ve "salon = derinlik" doğrulaması.
- Testler: Welsh–Powell ↔ renk renk anlatım (matrisle); χ ↔ ikinci bir kesin yöntem (altküme DP'si ya da bütün renk atamalarının denenmesi); salon ↔ her anda doğrudan sayım; çakışma grafı ↔ matrisle sayım.
- Ölçüm: ders sayısına göre süre (V = 10³…10⁵, isteğe bağlı 10⁶); renk sayısı dağılımı (açgözlü ↔ χ ya da alt sınır).

### İpuçları

- Ders çiftlerini sayarken her öğrencinin ders listesini **sıralı** tutun ve yalnız a < b çiftlerini sayın; anahtar a·V + b tek bir `long long`'dur. Kenar sayısı farklı anahtar sayısıdır, Σ C(k, 2) değil.
- Derece sırasını `qsort` yerine kararlı sayma sıralamasıyla yapın (dereceler 0..Δ); eşitlikte küçük kod kendiliğinden korunur.
- İlk uyan boyamada her köşe için yasak renkleri bir **damga** dizisiyle işaretleyin (`yasak[c] = i + 1`); diziyi her adımda sıfırlamayın.
- Açgözlü sonucu "en iyi" diye yazmayın: klik = açgözlü ise ya da kaba kuvvet doğrularsa yazın; değilse "en iyiden en çok X fazla" deyin.
- Kaba kuvvette **simetri kırma** kullanın: i. köşe en çok "kullanılan en büyük renk + 1"i dener; yoksa her boyamayı k! kez gezersiniz.
- Aralık bölümlemede öbekte **salonların bitişlerini** tutun (sınavların değil); kökte en erken boşalan salon. Karşılaştırmada `<=` mı `<` mi olacağını aralığın yarı açık olmasından çıkarın ve arka arkaya iki sınavla test edin.
- Taç grafını kendiniz kurun: Ai–Bj kenarı yalnız i ≠ j iken. Bütün dereceler eşit olduğunda eşitlik kuralı sırayı belirler.

### Kabul ölçütleri (denetlenebilir)

1. `make` ve `make test` sıfır uyarıyla derlenir; v1.0'ın 99 doğrulaması ve önceki sürümlerin testleri dahil bütün birim testleri (426) ve `test_kahin` (300 deneme) geçer.
2. `./sinav_programi` (örnek kayıtlar) şunları basar: `Çakışma grafı: 48 sınav (öğrencisi olan ders) · 469 kenar`, `Oturum ataması (açgözlü renklendirme; okunan komşu 938): 12 oturum`, `Doğrulama: 469 çakışma kenarının hepsinde iki sınav farklı oturumda: EVET` ve `Alt sınır: 11 derslik klik`; "en iyi" sözcüğü kullanılmaz.
3. Aynı çıktıda `En az salon sayısı: 3 (oturumların en büyüğü; alt sınır 3). Her oturumda salon = en çok eşzamanlı sınav: EVET; aynı salonda çakışan sınav yok: EVET` satırı vardır.
4. `./sinav_programi testler/sinav_kotu.txt --katalog testler/sinav_kotu_katalog.txt --kaba` Welsh–Powell sırasını `S1(3) S2(3) … S8(3)`, 4 oturum, kromatik sayı χ = 2 ve `açgözlü EN İYİ DEĞİL` basar.
5. `./sinav_programi testler/sinav_kucuk.txt --kaba`: açgözlü 5, klik 5, χ = 5, `açgözlü EN İYİ`.
6. `./sinav_programi testler/sinav_bozuk.txt` `satır 4: bilinmeyen ders kodu: BLM999` iletisiyle 1 ile çıkar; `--kaba` 30'dan çok sınavda üstel aramayı yapmaz ve bunu yazar.
7. `./test_kahin --hata-goster renk` ve `--hata-goster sinir` uyuşmazlık ve en küçük karşı örnek basar, 1 ile çıkar; `make asan` ve `make valgrind` temizdir.
8. Ölçüm raporunda: V = 10³…10⁵ (en az dört nokta) Welsh–Powell süresi ve okunan komşu = 2E; aralık bölümlemede salon = derinlik; en az bir yoğunlukta n ≤ 10 derslik en az 100 rastgele grafta açgözlü ↔ χ dağılımı ve yorumu.

### Test senaryoları

| # | Girdi | Beklenen çıktı / davranış |
|---|---|---|
| 1 | taç grafı (8 ders, `sinav_kotu.txt`) | Welsh–Powell 4 oturum, χ = 2 (A grubu / B grubu) |
| 2 | aynı graf, sıra A1 A2 A3 A4 B1 … | ilk uyan 2 renk (sıra her şeydir) |
| 3 | P4 yolu 0–1–2–3, sıra 0 3 1 2 | 3 renk; derece sırasıyla 2 |
| 4 | K₄; C₅; kenarsız 5 köşe | χ = 4; 3; 1 |
| 5 | yıldız (merkez 2) + yalıtık köşeler | derece sırası 2, sonra küçük numaralar artan |
| 6 | [0, 60), [30, 90), [60, 120), [90, 150) | 2 salon; [60, 120) 1. salonda ([0, 60)'tan sonra) |
| 7 | [0, 1), [1, 2) | 1 salon (yarı açık; `<` ile 2 — hata) |
| 8 | on aralıklı ders kitabı örneği | derinlik 3 = 3 salon |
| 9 | `7 C A B / 8 B A / 9 C B` | kenarlar A–B (2), B–C (2), A–C (1); Σ C(k, 2) = 5 |
| 10 | `7 A D` (D katalogda yok) | biçim hatası, satır 1, `bilinmeyen ders kodu: D` |
| 11 | aynı numara iki satırda | `yinelenen öğrenci numarası`, satır 2 |
| 12 | `sinav_kucuk.txt` | açgözlü 5 = klik 5 = χ 5 |

### Başlangıç noktası (öğrenciye verilenler)

- **Verilir:** kendi v2.10'unuz (ya da referans v2.10), `sinav.h` (bildirimler, sözleşmeler, sahiplik), `ornek_veri/sinav_kayitlari.txt` ve dört test dosyası, `olcer_sinav`'ın ölçüm düzeneği (rastgele graf ve aralık üretimi, sayaç ve süre), Şekil 1'in taç grafı.
- **Yazılır:** `sinav.c` (kayıt, çakışma grafı, Welsh–Powell, klik, kaba kuvvet, aralık bölümleme, derinlik), `sinav_programi.c`; testler (birim + kâhin); ölçüm ve yorum.
- **Değiştirilmez:** v1.0 kuralları ve menü, v2.9'un karma tablosu, v2.10'un graf ve katalog modülleri, v2.6'nın öbeği, ortak modüller.
- **Meydan okuma:** (a) DSatur (Brélaz, 1979) sezgiselini ekleyip § 8.4'ün dağılımını tekrarlayın; (b) oturum sayısı sabitken (ör. 10 gün) aynı gün iki sınavı olan öğrenci sayısını en aza indiren yerel arama; (c) salon kapasitesi (öğrenci sayısı) eklenince aralık bölümleme neden artık en iyi değildir? Karşı örnek kurun; (d) kaba kuvveti en büyük klikle başlatıp (k = klik boyu) düğüm sayısındaki kazancı ölçün.

## 11. Bilinen sınırlılıklar

- Ders kayıtları ayrı bir KURGUSAL dosyadan gelir; v1.0 kaydındaki üç ders (ALG, MAT, FIZ) çakışma grafı için yeterli değildir (v3.0'da kayıt modülüyle birleştirilecek).
- Oturum ataması yalnızca "ortak öğrenci yok" kısıtını çözer: gün sayısı sınırı, öğrenci başına günde en çok bir sınav, salon kapasitesi ve gözetmen sayısı yoktur.
- Sınav başlangıç saatleri girdi (KURGUSAL istek) olarak alınır; aralık bölümleme saatleri değiştirmez, yalnız salon atar.
- Welsh–Powell sezgiseldir; büyük graflarda en iyi değer bilinmez (yalnız klik ↔ açgözlü aralığı). Kaba kuvvet ≤ 30 sınavla sınırlıdır; açgözlü klik en büyük klik değildir.
- Süreler paylaşılan makinede yük altında ölçüldü; rastgele çakışma grafı gerçek kayıtları temsil etmez (§ 8.5).

## 12. Kaynaklar

- Brélaz, D. (1979). New methods to color the vertices of a graph. *Communications of the ACM, 22*(4), 251–256. https://doi.org/10.1145/359094.359101
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Kleinberg, J., & Tardos, É. (2006). *Algorithm design*. Pearson/Addison-Wesley.
- Welsh, D. J. A., & Powell, M. B. (1967). An upper bound for the chromatic number of a graph and its application to timetabling problems. *The Computer Journal, 10*(1), 85–86. https://doi.org/10.1093/comjnl/10.1.85
