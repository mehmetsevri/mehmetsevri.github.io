# Mini-OBS 2 v2.6 — Sıralama Algoritmalarının Karşılaştırmalı Ölçüm Raporu

**Ara proje referans raporu** · AP-2 Algoritma ve Programlama II, Hafta 7 · Mini-OBS 2 v2.6 · Ölçüm tarihi: 2026-10-13 07:39

---

## Özet

Bu rapor, Mini-OBS 2'nin v2.3–v2.6 sürümlerinde gerçeklenen dokuz sıralama yöntemini — seçmeli, kabarcık, araya ekleme, birleştirmeli, hızlı, öbek, sayma ve taban sıralaması ile C kütüphanesinin `qsort`'u — aynı ölçüm düzeneğinde, aynı öğe türüyle (16 baytlık anahtar–indis çifti) ve dört girdi türünde (karışık, sıralı, ters, çok tekrarlı) karşılaştırır. Karesel üç yöntem n = 8 000'e (karışıkta 16 000'e), diğerleri n = 10⁶'ya kadar ölçüldü; her noktada 1 ısınma ve 5 tekrarın ortancası alındı. Bulgular kuramla büyük ölçüde tutarlıdır: karesel yöntemlerin karışık girdideki log–log eğimi 1,98–2,01 (kuram 2), Θ(n log n) yöntemlerinki 1,06–1,26 (bu aralıkta kuram 1,09); sayma ve taban sıralamasının eğimi 1,13–1,70 ile kuramsal 1'in üstündedir — 10⁶ öğede dizi ve tamponu önbelleğe sığmaz. 10⁶ karışık öğrenci numarasında en hızlı yöntem taban sıralaması olmuştur (79,3 ms); birleştirmeli sıralamadan 3,4 kat hızlıdır. Sıralı girdide uyarlanabilir yöntemler doğrusal çalışır (n = 8 000'de araya ekleme 171,9 µs, karışık girdiden 613 kat hızlı). Çok tekrarlı girdide kararlılık sağlaması, kuramın kararsız saydığı üç yöntemi (seçmeli, hızlı, öbek) ayırır. Anahtar aralığı deneyi sayma sıralamasının Θ(n + K) bedelini, öbek uygulamaları deneyi ilk-k ve çok yollu birleştirmenin Θ(n log k) davranışını gösterir. Mini-OBS'nin kendi işlerinde aynı algoritmalar 10⁵ kayıtta numarayla bulmayı 730 kat, yinelenen tespitini 187 kat hızlandırmış; 10⁶ kaydın yüklenmesini kestirilen ≈ 1,6 saatten 2,28 s süreye indirmiştir. Rapor, veri özelliklerine göre bir algoritma seçim rehberiyle biter.

## 1. Amaç ve araştırma soruları

Mini-OBS'nin sıralama ihtiyaçları farklı veri özellikleri taşır: başarı listesi (çok anahtarlı, kararlılık gerekir), not dağılımı (anahtar 0–100), numara sırası (10 haneli tamsayı), yükleme (çoğu kez zaten sıralı ya da neredeyse sıralı dosyalar). Rapor şu soruları yanıtlar:

- **S1.** Hangi algoritma hangi girdi türünde ve boyutta en hızlıdır?
- **S2.** Ölçülen büyüme hızları (log–log eğimleri, oran testleri) kuramsal karmaşıklıklarla uyuşuyor mu?
- **S3.** Karşılaştırma sayıları kuramsal değerlere ve Ω(n log n) alt sınırına göre nerededir?
- **S4.** Kararlılık ölçümde nasıl görünür?
- **S5.** Sayma ve taban sıralaması anahtar aralığına nasıl tepki verir?
- **S6.** Bütün listeyi sıralamak yerine öbekle ilk-k ve çok yollu birleştirme ne kazandırır?
- **S7.** Arama ve sıralama algoritmaları Mini-OBS'nin kendi işlerini (numarayla bulma, yükleme, yinelenen tespiti) ne kadar hızlandırdı?

## 2. Yöntem

### 2.1 Ortam

| Öğe | Değer |
|---|---|
| İşlemci | Intel(R) Xeon(R) Processor @ 2.80GHz, 2 çekirdek (sanal makine) |
| Önbellek | L2 2 MiB (2 × 1 MiB), L3 33 MiB |
| Derleyici | gcc 13.3.0, `-std=c17 -Wall -Wextra -pedantic -O2 -g` |
| C kütüphanesi | glibc 2.39 |
| Ölçüm tarihi | 2026-10-13 07:39 |
| Yük ortalaması (1 dk) | başta 0,49, sonda 0,89 (makine başka işlerle paylaşıldı) |
| Toplam ölçüm süresi | `make olcum`: 1 dakika 33 s |

### 2.2 Algoritmalar ve kimlik kartları

| algoritma | en iyi | ortalama | en kötü | ek bellek | kararlı | yerinde | uyarlanabilir | karşılaştırmalı |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| seçmeli | Θ(n²) | Θ(n²) | Θ(n²) | Θ(1) | hayır | evet | hayır | evet |
| kabarcık (erken çıkış) | Θ(n) | Θ(n²) | Θ(n²) | Θ(1) | evet | evet | evet | evet |
| araya ekleme | Θ(n) | Θ(n²) | Θ(n²) | Θ(1) | evet | evet | evet | evet |
| birleştirmeli | Θ(n log n) | Θ(n log n) | Θ(n log n) | Θ(n) | evet | hayır | zayıf | evet |
| hızlı (Hoare, üçün ortancası) | Θ(n log n) | Θ(n log n) | Θ(n²) | Θ(log n) yığın | hayır | evet | hayır | evet |
| öbek | Θ(n log n) | Θ(n log n) | Θ(n log n) | Θ(1) | hayır | evet | hayır | evet |
| sayma (aralık K) | Θ(n + K) | Θ(n + K) | Θ(n + K) | Θ(n + K) | evet | hayır | — | hayır |
| taban (LSD, 256; d bayt) | Θ(d(n + 256)) | Θ(d(n + 256)) | Θ(d(n + 256)) | Θ(n) | evet | hayır | — | hayır |
| qsort (C kütüphanesi) | — | — | — | — | güvence yok | — | — | evet |

*Tablo 1. Kuramsal özellikler. "Uyarlanabilir": sıralı ya da neredeyse sıralı girdide daha az iş yapar. Hızlı sıralamanın en kötü durumu üçün ortancasıyla sıralı ve ters girdide oluşmaz; özel girdilerde Θ(n²) kalır. Gerçeklemeler: `siralama.c` (v2.4), `bolfethet.c` (v2.5), `obek.c` ve `dogrusal.c` (v2.6); hepsi `qsort` arayüzündedir (taban, n, boyut, karşılaştırıcı ya da anahtar fonksiyonu).*

### 2.3 Girdiler

Öğe: `{long long anahtar; int indis;}` (16 bayt); karşılaştırıcı yalnızca anahtarı karşılaştırır, indis girdideki sırayı taşır. Veri `veri_uret`'in üreteciyle (tohum 42) üretilir:

| Girdi | Anahtar | Farklı anahtar | Not |
|---|---|---|---|
| karışık | öğrenci numaraları, üreteç sırası (rastgele permütasyon) | n | sayma: K = n; taban: 4 geçiş (numaralar < 2³²) |
| sıralı | aynı numaralar, artan | n | uyarlanabilir yöntemlerin en iyi durumu |
| ters | aynı numaralar, azalan | n | araya ekleme ve kabarcığın en kötü durumu |
| çok tekrarlı | yuvarlanmış ALG notu (0–100), üreteç sırası | 101 | kararlılık sınaması; sayma: K = 101; taban: 1 geçiş |

### 2.4 Ölçüm düzeni

- Her (algoritma, girdi, n) noktası ayrı bir süreçte ölçülür: veri hazırlanır (ölçülmez), **1 ısınma + 5 tekrar** çalıştırılır, ortanca raporlanır (Sedgewick & Wayne, 2011); n = 10⁶'da 3 tekrar, karesel üçlüde n = 16 000'de 3 tekrar. Her çalıştırma başlangıç dizisini kopyalar (Θ(n), ölçüme dahil).
- Sayaçlar (karşılaştırma, taşıma, toplama) ısınma çalıştırmasında toplanır: süre ölçümü sayaçsızdır. `qsort`'un karşılaştırmaları bir sarıcı karşılaştırıcıyla sayılır; taşıması ölçülemez.
- Kuramın kesin değer verdiği durumlarda (seçmeli sıralamanın n(n − 1)/2 karşılaştırması, birleştirmeli sıralamanın sıralı ve ters girdideki sayıları, sayma ve taban sıralamasının n + K ve d(n + 256) adımı, …) `olcer` sayaçları otomatik karşılaştırır: bu ölçümde **100** "kuram: UYUMLU", **0** uyumsuzluk.
- **Kontrol sağlaması:** sıralı dizinin Σ (i + 1)·indis toplamı; doğru ve kararlı her yöntemde aynıdır. Sıralı olmayan bir sonuç −1 verir (hiç görülmedi).

### 2.5 Doğruluk

Ölçülen bütün gerçeklemeler birim testleri (245 doğrulama) ve kâhin testleriyle (1 000 rastgele denemede 1 172 771 denetim; kâhin: `qsort` + indis, öbek özelliği, sayaçların tanımdan hesabı) sınanmıştır; AddressSanitizer, UBSan ve Valgrind temizdir (`mini_obs_v2_6_ciktilar.txt`).

## 3. Sonuçlar

### 3.1 Karesel yöntemler

| algoritma | girdi | 1 000 | 2 000 | 4 000 | 8 000 | 16 000 | T(8 000) / T(4 000) |
|:--|:--|--:|--:|--:|--:|--:|--:|
| seçmeli | karışık | 2,5 ms | 10,0 ms | 40,7 ms | 159,6 ms | 653,6 ms | 3,92 |
|  | sıralı | 2,4 ms | 9,6 ms | 40,0 ms | 159,6 ms | — | 3,99 |
|  | ters | 2,5 ms | 9,8 ms | 39,7 ms | 172,1 ms | — | 4,33 |
|  | çok tekrarlı | 2,5 ms | 10,0 ms | 41,8 ms | 176,8 ms | — | 4,23 |
| kabarcık | karışık | 5,9 ms | 24,4 ms | 73,3 ms | 296,5 ms | 1,47 s | 4,05 |
|  | sıralı | 9,8 µs | 18,4 µs | 38,5 µs | 68,8 µs | — | 1,79 |
|  | ters | 8,0 ms | 22,2 ms | 91,7 ms | 501,2 ms | — | 5,47 |
|  | çok tekrarlı | 4,4 ms | 17,9 ms | 101,0 ms | 388,7 ms | — | 3,85 |
| araya ekleme | karışık | 1,6 ms | 6,4 ms | 25,6 ms | 105,4 ms | 411,2 ms | 4,12 |
|  | sıralı | 21,9 µs | 42,5 µs | 85,2 µs | 171,9 µs | — | 2,02 |
|  | ters | 4,0 ms | 13,2 ms | 51,7 ms | 159,7 ms | — | 3,09 |
|  | çok tekrarlı | 1,1 ms | 4,6 ms | 24,6 ms | 77,0 ms | — | 3,13 |

*Tablo 2. Seçmeli, kabarcık ve araya ekleme sıralaması (ortanca). Son sütun oran testidir: Θ(n²) için 4.*

![Dört girdi türü](mini_obs_v2_6_olcum_girdiler.png)

*Şekil 1. Dokuz algoritma, dört girdi türü (log–log; süre ortanca).*

### 3.2 Θ(n log n) ve doğrusal yöntemler

| girdi | algoritma | 10³ | 1,6·10⁴ | 10⁵ | 10⁶ | T(10⁶) / T(10⁵) |
|:--|:--|--:|--:|--:|--:|--:|
| karışık | birleştirmeli | 141,1 µs | 2,5 ms | 19,5 ms | 273,1 ms | 14,0 |
|  | hızlı | 142,3 µs | 3,2 ms | 23,6 ms | 254,5 ms | 10,8 |
|  | öbek | 138,7 µs | 3,3 ms | 26,3 ms | 599,1 ms | 22,8 |
|  | sayma | 10,2 µs | 181,2 µs | 1,9 ms | 197,1 ms | 104,6 |
|  | taban (LSD) | 28,4 µs | 582,7 µs | 3,8 ms | 79,3 ms | 20,9 |
|  | qsort | 102,1 µs | 2,5 ms | 23,4 ms | 257,7 ms | 11,0 |
| sıralı | birleştirmeli | 41,8 µs | 923,4 µs | 7,0 ms | 118,0 ms | 16,7 |
|  | hızlı | 38,0 µs | 1,0 ms | 6,2 ms | 145,9 ms | 23,5 |
|  | öbek | 128,4 µs | 2,7 ms | 19,0 ms | 242,9 ms | 12,8 |
|  | sayma | 10,3 µs | 169,6 µs | 1,5 ms | 25,1 ms | 17,3 |
|  | taban (LSD) | 28,4 µs | 752,1 µs | 4,1 ms | 77,3 ms | 18,8 |
|  | qsort | 33,5 µs | 819,4 µs | 5,8 ms | 86,0 ms | 14,9 |
| ters | birleştirmeli | 41,0 µs | 893,1 µs | 7,5 ms | 160,2 ms | 21,3 |
|  | hızlı | 96,9 µs | 1,0 ms | 9,5 ms | 111,2 ms | 11,8 |
|  | öbek | 120,7 µs | 2,5 ms | 19,3 ms | 261,9 ms | 13,6 |
|  | sayma | 10,2 µs | 171,7 µs | 1,3 ms | 26,6 ms | 19,9 |
|  | taban (LSD) | 28,1 µs | 573,9 µs | 4,0 ms | 92,3 ms | 23,1 |
|  | qsort | 36,9 µs | 867,8 µs | 6,8 ms | 108,1 ms | 15,9 |
| çok tekrarlı | birleştirmeli | 98,0 µs | 2,1 ms | 16,1 ms | 230,0 ms | 14,3 |
|  | hızlı | 98,7 µs | 2,2 ms | 14,6 ms | 226,3 ms | 15,5 |
|  | öbek | 147,6 µs | 3,1 ms | 22,9 ms | 407,1 ms | 17,8 |
|  | sayma | 9,4 µs | 156,8 µs | 1,3 ms | 37,1 ms | 28,9 |
|  | taban (LSD) | 11,1 µs | 191,1 µs | 1,5 ms | 35,6 ms | 23,4 |
|  | qsort | 95,1 µs | 2,0 ms | 14,6 ms | 193,5 ms | 13,2 |

*Tablo 3. Altı hızlı yöntem (ortanca). Son sütun: n on kat büyüdüğünde sürenin kaç kat arttığı (Θ(n) için 10, Θ(n log n) için 10 · log 10⁶ / log 10⁵ = 12,0).*

![n = 8 000'de dokuz algoritma](mini_obs_v2_6_olcum_cubuk.png)

*Şekil 2. n = 8 000'de dokuz algoritmanın dört girdi türündeki süresi (logaritmik ölçek).*

### 3.3 Büyüme eğimleri

| algoritma | karışık | sıralı | ters | çok tekrarlı | kuram |
|:--|--:|--:|--:|--:|:--|
| seçmeli | 2,01 | 2,03 | 2,07 | 2,07 | 2 (n² ve uyarlanabilir yöntemlerde sıralı girdide 1) |
| kabarcık | 1,98 | 0,95 | 2,25 | 2,22 | 2 (n² ve uyarlanabilir yöntemlerde sıralı girdide 1) |
| araya ekleme | 2,00 | 1,01 | 1,80 | 2,04 | 2 (n² ve uyarlanabilir yöntemlerde sıralı girdide 1) |
| birleştirmeli | 1,13 | 1,18 | 1,26 | 1,14 | 1,09 (n log n) |
| hızlı | 1,06 | 1,20 | 1,13 | 1,13 | 1,09 (n log n) |
| öbek | 1,26 | 1,09 | 1,12 | 1,18 | 1,09 (n log n) |
| sayma | 1,70 | 1,21 | 1,22 | 1,33 | 1 |
| taban (LSD) | 1,19 | 1,13 | 1,23 | 1,27 | 1 |
| qsort | 1,12 | 1,13 | 1,17 | 1,10 | 1,09 (n log n) |

*Tablo 4. log t – log n doğrusunun eğimi (en küçük kareler): karesel üçlü için n = 2 000 – 16 000, diğerleri için n = 16 000 – 10⁶. Θ(n log n)'in bu aralıktaki kuramsal eğimi: 1,09 (1 + Δln log n / Δln n).*

### 3.4 Karşılaştırma ve iş sayıları

| algoritma (n: karesel 8 000, diğerleri 10⁶) | karışık | sıralı | ters | çok tekrarlı |
|:--|--:|--:|--:|--:|
| seçmeli | 308,466 | 308,466 | 308,466 | 308,466 |
| kabarcık | 308,398 | 0,077 | 308,466 | 308,298 |
| araya ekleme | 154,288 | 0,077 | 308,466 | 152,952 |
| birleştirmeli | 0,937 | 0,496 | 0,505 | 0,933 |
| hızlı | 1,399 | 1,152 | 1,152 | 1,254 |
| öbek | 1,846 | 1,891 | 1,806 | 1,845 |
| qsort | 0,937 | 0,496 | 0,505 | 0,933 |

*Tablo 5. Karşılaştırma sayısının n log₂ n'ye oranı. Ω(n log n) alt sınırı log₂ n! karşılaştırmadır: oranı 10⁶'da 0,928, 8 000'de 0,889.*

| algoritma (n = 10⁶) | girdi | K ya da geçiş | toplama (sayaç adımı) | taşıma | süre |
|:--|:--|--:|--:|--:|--:|
| sayma | karışık | 1 000 000 | 2 000 000 | 2 000 000 | 197,1 ms |
|  | sıralı | 1 000 000 | 2 000 000 | 2 000 000 | 25,1 ms |
|  | ters | 1 000 000 | 2 000 000 | 2 000 000 | 26,6 ms |
|  | çok tekrarlı | 101 | 1 000 101 | 2 000 000 | 37,1 ms |
| taban (LSD) | karışık | 4 | 4 001 024 | 4 000 000 | 79,3 ms |
|  | sıralı | 4 | 4 001 024 | 4 000 000 | 77,3 ms |
|  | ters | 4 | 4 001 024 | 4 000 000 | 92,3 ms |
|  | çok tekrarlı | 1 | 1 000 256 | 2 000 000 | 35,6 ms |

*Tablo 6. Karşılaştırmasız yöntemlerin iş sayıları (n = 10⁶): karşılaştırma 0; "toplama" sayaç dizisindeki artırma ve önek toplamı adımlarıdır (sayma n + K, taban d(n + 256)); taşıma, çıktıya yazma ve sonucun geri kopyalanmasıdır.*

### 3.5 Kararlılık

| algoritma | kontrol (n = 8 000, çok tekrarlı) | kararlı yöntemlerle | kuramda kararlı |
|:--|--:|:-:|:-:|
| seçmeli | 63989112217 | FARKLI | hayır |
| kabarcık | 64159142098 | aynı | evet |
| araya ekleme | 64159142098 | aynı | evet |
| birleştirmeli | 64159142098 | aynı | evet |
| hızlı | 63907028575 | FARKLI | hayır |
| öbek | 63861088068 | FARKLI | hayır |
| sayma | 64159142098 | aynı | evet |
| taban (LSD) | 64159142098 | aynı | evet |
| qsort | 64159142098 | aynı | güvence yok |

*Tablo 7. Çok tekrarlı girdide (101 farklı anahtar) indis sağlaması. Eşit anahtarlı öğelerin girdi sırasını koruyan her yöntem aynı değeri verir.*

### 3.6 Anahtar aralığı

| K | sayma | sayma: toplama (n + K) | taban | geçiş | birleştirmeli | birleştirmeli / sayma |
|--:|--:|--:|--:|--:|--:|--:|
| 10 | 1,2 ms | 100 010 | 1,4 ms | 1 | 13,6 ms | 11,1 |
| 100 | 1,3 ms | 100 100 | 1,4 ms | 1 | 16,0 ms | 12,4 |
| 1 000 | 1,4 ms | 101 000 | 2,0 ms | 2 | 17,4 ms | 12,7 |
| 10 000 | 1,4 ms | 110 000 | 2,0 ms | 2 | 25,1 ms | 17,4 |
| 100 000 | 2,5 ms | 200 000 | 2,7 ms | 3 | 18,5 ms | 7,3 |
| 1 000 000 | 9,2 ms | 1 100 000 | 3,2 ms | 3 | 18,9 ms | 2,0 |
| 10 000 000 | 105,0 ms | 10 100 000 | 2,9 ms | 3 | 25,1 ms | 0,2 |

*Tablo 8. n = 10⁵ öğe, anahtarlar [0, K) aralığında düzgün rastgele. Taban sıralamasının geçiş sayısı (K − 1)'in bayt uzunluğudur.*

### 3.7 Öbek uygulamaları: ilk-k ve çok yollu birleştirme

| k | ilk-k (öbek) | karşılaştırma | kars. / n | bütün liste / ilk-k |
|--:|--:|--:|--:|--:|
| 1 | 7,5 ms | 99 999 | 1,00 | 51,4 |
| 10 | 6,3 ms | 100 457 | 1,00 | 61,1 |
| 100 | 7,3 ms | 108 207 | 1,08 | 52,5 |
| 1 000 | 18,7 ms | 194 593 | 1,95 | 20,5 |
| 10 000 | 171,1 ms | 882 331 | 8,82 | 2,2 |
| 100 000 | 681,0 ms | 3 119 378 | 31,19 | 0,6 |

*Tablo 9. Başarı listesinin (YANO ↓, soyad ↑, ad ↑, numara ↑; Türkçe karşılaştırıcı; işaretçi dizisi) ilk k'sı, n = 10⁵. Bütün listenin birleştirmeli sıralanması 383,0 ms.*

| n (k = 10) | ilk-10 (öbek) | karşılaştırma | bütün liste (birleştirmeli) |
|--:|--:|--:|--:|
| 10 000 | 557,3 µs | 10 300 | 25,7 ms |
| 100 000 | 6,3 ms | 100 457 | 383,0 ms |
| 1 000 000 | 61,2 ms | 1 000 542 | — |

*Tablo 10. İlk-10'un n ile büyümesi.*

| k | süre (n = 10⁶) | karşılaştırma | kars. / (n log₂ k) |
|--:|--:|--:|--:|
| 2 | 169,5 ms | 999 999 | 1,00 |
| 4 | 138,1 ms | 2 499 561 | 1,25 |
| 8 | 153,0 ms | 3 999 778 | 1,33 |
| 16 | 173,6 ms | 5 624 111 | 1,41 |
| 64 | 237,6 ms | 9 218 026 | 1,54 |

*Tablo 11. 10⁶ kaydın k şubeden çok yollu birleştirilmesi (öbekte k baş). Karşılaştırma için: iki işaretçili birleştirme 128,0 ms, şubeleri uç uca ekleyip kayıtları sıralamak 881,2 ms.*

![Anahtar aralığı ve ilk-k](mini_obs_v2_6_olcum_obek.png)

*Şekil 3. Sol: anahtar aralığının etkisi (n = 10⁵); sağ: ilk-k'nın k ile büyümesi ve bütün listenin sıralanması (kesikli çizgi).*

### 3.8 Mini-OBS'ye yansıması: arama, yükleme ve yinelenen tespiti (S7)

| işlem, n | önceki yöntem | süre | yeni yöntem | süre | hızlanma (kat) | kaynak |
|:--|:--|--:|:--|--:|--:|:--|
| numarayla bulma (arama başına), 10⁵ | doğrusal arama (v1.0) | 190,5 µs | ikili arama (v2.3) | 261 ns | 730 | v2.3 `arama.csv` |
| numarayla bulma (arama başına), 10⁶ | doğrusal arama (v1.0) | 6,8 ms | ikili arama (v2.3) | 757 ns | 9 041 | v2.3 `arama.csv` |
| yükleme, 32 000 kayıt (karışık) | her kayıtta tam tarama (v1.0) | 1,33 s | sıralı ekleme (v2.3) | 1,66 s | 0,80 | v2.5 `yukleme.csv` |
| yükleme, 32 000 kayıt (karışık) | her kayıtta tam tarama (v1.0) | 1,33 s | toplu: oku, sırala (v2.5) | 71,2 ms | 18,7 | v2.5 `yukleme.csv` |
| yükleme, 10⁶ kayıt (karışık) | v1.0 (kestirim, v2.0) | ≈ 1,6 saat | toplu (v2.5) | 2,28 s | ≈ 2 540 | v2.0 kestirimi, v2.5 `yukleme.csv` |
| yinelenen numara tespiti, 10⁵ | tüm çiftler (v2.1) | 4,33 s | sırala, komşuları karşılaştır (v2.5) | 23,1 ms | 187 | v2.5 `yinelenen.csv` |

*Tablo 12. v2.3–v2.5'in Mini-OBS işlemlerine etkisi (ortanca). Her satırın iki süresi aynı ölçüm oturumunda ve aynı programda ölçülmüştür; yalnızca 10⁶ yükleme satırının "önceki" değeri v2.0'ın kestirimidir. Kaynağı farklı satırlar farklı ölçüm oturumlarındandır; aralarında süre karşılaştırılmamalıdır. 1'den küçük hızlanma yavaşlamadır.*

Tablo 12'nin üçüncü satırı arama ile sıralamanın ilişkisini gösterir: v2.3'ün sıralı eklemesi mükerrer denetiminin karşılaştırmasını Θ(n²)'den Θ(n log n)'e indirir, ama her ekleme ortalama n/4 kaydı kaydırdığı için süre azalmaz (darboğaz karşılaştırmadan taşımaya geçer). Kaydırmayı ortadan kaldıran, v2.5'in "önce oku, sonra bir kez sırala" düzenidir: sıralı dizi ikili aramanın önkoşuludur ve en ucuz yoldan sıralama ile kurulur.

## 4. Tartışma

### 4.1 Kuramla tutarlılık (S2, S3)

- **Karesel üçlü:** oran testleri ve eğimler 2'ye yakındır (Tablo 2 ve 4). Seçmeli sıralama girdiye kördür: dört girdide de tam n(n − 1)/2 karşılaştırma ve aynı süre. Kabarcık ve araya ekleme sıralı girdide n − 1 karşılaştırmayla biter (eğim ≈ 1): uyarlanabilirlik kuramda olduğu gibi görünür.
- **Θ(n log n) yöntemler:** karışık girdide eğimler kuramsal 1,09 değerine yakındır (birleştirmeli 1,13). Karışık girdide eğimi en büyük olan öbek sıralamasıdır (1,26): dizi 10⁶ öğede 16 MB'tır ve L2'ye sığmaz; aşağı süzmenin i → 2i + 1 atlamaları her düzeyde önbellek kaçırması üretir. Karşılaştırma sayıları beklendiği gibidir (Tablo 5): birleştirmeli sıralama alt sınıra en yakın yöntemdir; hızlı sıralama onun 1,49 katı, öbek sıralaması 1,97 katı karşılaştırma yapar.
- **Doğrusal yöntemler:** taban sıralamasının karışık girdideki eğimi 1,19, sayma sıralamasınınki 1,70: ikisi de kuramsal 1'in üstündedir. İş sayıları tam olarak doğrusaldır (Tablo 6, "kuram: UYUMLU"); süredeki fazlalık bellek hiyerarşisinden gelir: n = 16 000'de dizi (256 KB) önbellekteyken 10⁶'da dizi ve tampon (2 × 16 MB) L3'ü doldurur. Sayma sıralamasının eğimi sıralı girdide (1,21) karışık girdidekinden belirgin küçüktür. Fark aynı kuramsal işin (n + K adım) farklı bellek erişim düzenidir: karışık girdide çıktı dizisinin rastgele konumlarına yazılır (10⁶ öğede 16 MB'lık hedef), sıralı girdide ardışık yazılır. 10⁶ karışık girdide sayma sıralaması taban sıralamasından 2,5 kat yavaştır; sıralı girdiye göre 7,9 kat yavaştır. **Karmaşıklık işlem sayısını tahmin eder; süreyi bellek hiyerarşisi de belirler.**
- **qsort:** bu makinedeki C kütüphanesinin (glibc 2.39) `qsort` işlevi bu ölçümlerde birleştirmeli sıralamamızla her noktada birebir aynı sayıda karşılaştırma yaptı ve çok tekrarlı girdide kararlı davrandı: bu kütüphane bu boyutlarda birleştirmeli sıralama kullanıyor. C standardı ne algoritmayı ne kararlılığı güvence eder; başka bir platformda farklı olabilir.

### 4.2 Hangi algoritma, hangi veri? (S1, S4, S5, S6)

| Veri durumu | Öneri | Ölçümdeki gerekçe |
|---|---|---|
| küçük n (≲ 50) ya da neredeyse sıralı | araya ekleme | sıralı girdide n = 8 000'de 171,9 µs; karışık girdide karesel (105,4 ms) |
| genel amaçlı, kararlılık gerekli | birleştirmeli sıralama | Θ(n log n) her girdide, kararlı; 10⁶ karışık: 273,1 ms |
| genel amaçlı, kararlılık gerekmiyor, bellek sınırlı | hızlı sıralama (üçün ortancası) | 10⁶ karışık: 254,5 ms (birleştirmelinin 0,93 katı), yerinde |
| en kötü durum güvencesi + Θ(1) bellek | öbek sıralaması (ya da introsort) | Θ(n log n) her durumda ama önbellek dostu değil: hızlı sıralamanın 2,4 katı |
| tamsayı anahtar, küçük aralık (K ≲ n) | sayma sıralaması | n = 10⁵, K ≤ 10⁵'te birleştirmeliden ≈ 7 kat hızlı; K = 10⁷'de 105,0 ms |
| tamsayı anahtar, büyük aralık (numara) | taban sıralaması (LSD, 256) | 10⁶ karışık numara: 79,3 ms; K = 10⁷'de bile 2,9 ms (n = 10⁵) |
| yalnızca ilk k (k ≪ n) | k boyutlu öbek | n = 10⁵, k = 10: bütün listeden 61 kat hızlı; avantaj k ≈ 100 000 civarında biter |
| k sıralı listenin birleştirilmesi | çok yollu birleştirme (öbek) | Θ(n log k); 10⁶ kayıt, 16 şube: 173,6 ms |
| hazır çözüm yeterli | `qsort` | 10⁶ karışık: 257,7 ms (birleştirmelinin 0,94 katı); kararlılık güvencesi yok |

*Tablo 13. Algoritma seçim rehberi (ÖÇ 7.5).*

Karesel yöntemlerin genel amaçlı kullanımı yoktur: n = 8 000 karışık girdide en iyisi (araya ekleme) bile 105,4 ms sürer; kabarcık sıralaması (296,5 ms) en yavaşıdır, çünkü her ters çevrimi bir komşu takasıyla (3 taşıma) düzeltir. Seçmeli sıralama (159,6 ms) en az taşımayı yapar (en çok n − 1 takas): taşımanın çok pahalı olduğu durumlarda (büyük kayıtlar) bu özellik değer kazanır.

## 5. Geçerlilik tehditleri ve sınırlılıklar

- **Tek makine, paylaşılan ortam:** ölçümler tek bir 2 çekirdekli sanal makinede yapıldı; yük ortalaması başta 0,49, sonda 0,89. Ortanca, tek tük kesintilere karşı dayanıklıdır ama uzun süreli yük değişimlerine değil. Sayaçlar makineden bağımsızdır; süreler değildir.
- **Tek öğe türü:** öğeler 16 bayttır ve karşılaştırma ucuzdur (iki tamsayı). Büyük kayıtlarda taşıma, pahalı karşılaştırıcılarda (ör. Türkçe dizgi karşılaştırması) karşılaştırma sayısı baskınlaşır (v2.4 ve v2.5 bulguları: başarı listesinde hızlı sıralama birleştirmeliden yavaştı).
- **Girdi dağılımları:** "karışık" girdi bir rastgele permütasyondur; gerçek veride kısmi sıralılık ve kümelenme olabilir. Hızlı sıralamanın üçün ortancasını bozan özel girdileri ölçülmedi.
- **Ölçüm kapsamı:** her çalıştırma başlangıç dizisinin kopyasını içerir (Θ(n)); karşılaştırmasız yöntemlerde bu kopya toplam sürenin hissedilir bir parçasıdır.
- **Derleyici ve bayraklar:** yalnızca `-O2` ölçüldü; `-O3` ya da `-march=native` sonuçları değiştirebilir.

## 6. Sonuç

Ölçümler kuramın öngördüğü sıralamayı doğrular ve onu üç noktada inceltir: (1) aynı Θ sınıfında sabitler ve bellek erişim düzeni belirleyicidir (öbek sıralaması ve karışık girdide sayma sıralaması önbellek yüzünden yavaştır); (2) karşılaştırmasız yöntemler, anahtar varsayımları geçerli olduğunda (küçük aralık, sabit uzunluk) karşılaştırmalı yöntemlerin en iyisinden bile hızlıdır; (3) bütün listeye gerek yoksa (ilk-k, birleştirme) öbek, sıralamayı Θ(n log k)'ye indirir. Mini-OBS için sonuç: başarı listesi birleştirmeli (kararlı) kalmalı; not dağılımı sayma, numara sırası taban sıralamasıyla; ilk-k ve şube birleştirme öbekle yapılmalıdır.

## Ek A. Yeniden üretme

```
cd v2.6
make            # programlar
make test       # birim + kâhin testleri
make olcum      # olcum/*.csv ve olcum/OLCUM_ORTAMI.txt (bu makinede 1 dakika 33 s)
```

Tek bir nokta: `./olcer kiyas_taban --sira karisik --n 1000000 --tekrar 3` (stdout: sayaçlar ve kuram; stderr: süreler). Tablolar ve grafikler CSV'lerden betikle üretilmiştir; elle girilmiş sayı yoktur.

## Ek B. Ham veri dosyaları

| Dosya | İçerik |
|---|---|
| `olcum/kiyas.csv` | 9 algoritma × 4 girdi × n (sütunlar: islem, n, sira, parametre, tekrar, ic_tekrar, ortanca_ms, ortalama_ms, en_az_ms, en_cok_ms, ilk_ms, isinma_ms, kontrol, karsilastirma, tasima, toplama) |
| `olcum/aralik.csv` | anahtar aralığı deneyi (parametre = K) |
| `olcum/ilk_k.csv`, `olcum/ilk_k_tam.csv` | ilk-k (parametre = k) ve bütün liste |
| `olcum/cok_yollu.csv`, `olcum/cok_yollu_kiyas.csv` | çok yollu birleştirme (parametre = k) ve karşılaştırmalar |
| `olcum/OLCUM_ORTAMI.txt` | makine, derleyici, tarih, yük ortalaması |
| `../v2.3/olcum/arama.csv`, `../v2.5/olcum/yukleme.csv`, `../v2.5/olcum/yinelenen.csv` | Tablo 12'nin kaynakları (sürümlerin kendi ölçüm oturumları) |

## Kaynaklar

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Knuth, D. E. (1998). *The art of computer programming: Vol. 3. Sorting and searching* (2nd ed.). Addison-Wesley.
- Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley.
