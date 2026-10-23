# Ara Proje Rapor Şablonu — Mini-OBS 2 v2.6 sıralama ölçüm raporu

**Ders:** Algoritma ve Programlama – II (C17) · Ara proje (H7, teslim H8 başı)

**Yönerge:** [ARA_PROJE_YONERGESI.md](ARA_PROJE_YONERGESI.md) · Başvuru örneği: [v2.6/mini_obs_v2_6_olcum_raporu.md](v2.6/mini_obs_v2_6_olcum_raporu.md)

Bu şablonu kopyalayıp `rapor/ara_proje_raporu.md` adıyla doldurun. `>` ile başlayan yönerge satırlarını silin; başlıkları, tablo ve şekil numaralarını koruyun; şekil satırlarının başındaki ve sonundaki ters tırnakları kaldırıp kendi dosya adlarınızı yazın. Başvuru raporu biçim için bir örnektir: **sayılarınız kendi makinenizden gelmelidir.**

## Biçim kuralları

- **Uzunluk:** en çok 12 sayfa (ekler hariç). **Dosyalar:** Markdown kaynağı + PDF + `sekiller/` + tabloları ve grafikleri CSV'den üreten betik.
- **Sayılar:** Türkçe biçim — ondalık virgül (77,5), binlik ayırıcı boşluk (4 932); birimler ms, µs, s. Süreler en çok 3–4 anlamlı basamakla verilir.
- **Tablolar:** numaralı ve başlıklı ("*Tablo 3. …*"); sütun adında birim (`süre (ms)`) ya da hücrede birim; sayılar sağa yaslı.
- **Şekiller:** numaralı, başlıklı; eksen adı, birim ve ölçek türü ("log") yazılı; büyüme karşılaştırmasında log–log eksen; lejant veriyi örtmez; yazı basılı sayfada ≥ 9 pt; renk tek başına anlam taşımaz (işaret ya da çizgi türü de farklı).
- **Kaynak:** her sayı `olcum/*.csv`'den betikle üretilir; Ek B hangi tablonun hangi dosyadan geldiğini gösterir. Elle kopyalanmış sayı yoktur.
- **Kestirim:** ölçülemeyen değerler yöntemiyle birlikte "kestirim" diye etiketlenir.
- **Kaynakça:** APA 7.
- **PDF:** örneğin (pandoc ve wkhtmltopdf ile; başvuru raporu bu komutla 10 sayfa)

```bash
pandoc ara_proje_raporu.md -f markdown-implicit_figures -s -o ara_proje_raporu.pdf \
  --pdf-engine=wkhtmltopdf --pdf-engine-opt=--enable-local-file-access \
  -V maxwidth=100% -V margin-top=15mm -V margin-bottom=15mm \
  -V margin-left=15mm -V margin-right=15mm --metadata pagetitle="Ara proje raporu"
```

Alternatif: Markdown'ı bir kelime işlemciye aktarıp PDF olarak kaydetmek; biçim kuralları aynıdır.

---

# Mini-OBS 2 v2.6 — Sıralama Algoritmalarının Karşılaştırmalı Ölçüm Raporu

**Ad Soyad · Öğrenci no** · AP-2 Ara Proje · Mini-OBS 2 v2.6 (depo etiketi: `v2.6`) · Ölçüm tarihi: GG.AA.YYYY

## Özet

> En çok 200 sözcük. Ne ölçüldü (yöntemler, girdiler, n aralığı, düzen), en önemli dört bulgu **sayılarla** (ör. eğim aralıkları, 10⁶'da en hızlı yöntem ve kaç kat, uyarlanabilirlik, kararlılık) ve Mini-OBS için sonuç.

## 1. Amaç ve araştırma soruları

> Mini-OBS'nin sıralama ihtiyaçlarını (başarı listesi, not dağılımı, numara sırası, yükleme) bir paragrafta bağlayın. Aşağıdaki soruları yanıtlayın; isterseniz yenisini ekleyin.

- **S1.** Hangi algoritma hangi girdi türünde ve boyutta en hızlıdır?
- **S2.** Ölçülen büyüme hızları (oran testleri, log–log eğimleri) kuramsal karmaşıklıklarla uyuşuyor mu?
- **S3.** Karşılaştırma sayıları kuramsal değerlere ve Ω(n log n) alt sınırına göre nerededir?
- **S4.** Kararlılık ölçümde nasıl görünür?
- **S5.** Sayma ve taban sıralaması anahtar aralığına nasıl tepki verir?
- **S6.** Bütün listeyi sıralamak yerine öbekle ilk-k ve çok yollu birleştirme ne kazandırır?
- **S7.** Arama ve sıralama algoritmaları Mini-OBS'nin kendi işlerini (numarayla bulma, yükleme, yinelenen tespiti) ne kadar hızlandırdı?

## 2. Yöntem

### 2.1 Ortam

| Öğe | Değer |
|---|---|
| İşlemci | model, çekirdek sayısı (sanal makine / WSL / doğrudan) |
| Önbellek | L1d, L2, L3 |
| Bellek | toplam RAM |
| İşletim sistemi | dağıtım ve sürüm (WSL ise Windows sürümü de) |
| Derleyici ve bayraklar | `gcc --version`; `-std=c17 -Wall -Wextra -pedantic -O2 -g` |
| C kütüphanesi | glibc / MSVCRT / UCRT sürümü |
| Güç ve yük | prize takılı mı, güç kipi; ölçüm başında ve sonunda yük ortalaması (Linux: `uptime`) |
| Ölçüm tarihi ve süresi | `make olcum`'un toplam süresi |

> Bilgilerin çoğu `olcum/OLCUM_ORTAMI.txt`'de olmalıdır. Linux/WSL: `lscpu`, `free -h`, `gcc --version`, `ldd --version`, `uptime`. MSYS2: `gcc --version`; işlemci ve önbellek için Görev Yöneticisi → Performans.

### 2.2 Algoritmalar ve kimlik kartları

| algoritma | en iyi | ortalama | en kötü | ek bellek | kararlı | yerinde | uyarlanabilir | karşılaştırmalı |
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| seçmeli | | | | | | | | |
| kabarcık (erken çıkış) | | | | | | | | |
| araya ekleme | | | | | | | | |
| birleştirmeli | | | | | | | | |
| hızlı (pivot kuralınız) | | | | | | | | |
| öbek | | | | | | | | |
| sayma (aralık K) | | | | | | | | |
| taban (LSD, 256; d bayt) | | | | | | | | |
| `qsort` (C kütüphanesi) | | | | | | | | |

*Tablo 1. Kuramsal özellikler.*

> Hücreleri Θ gösterimiyle doldurun. Hızlı sıralamanın pivot kuralını ve en kötü durumunun hangi girdide oluştuğunu yazın. `qsort` için standardın neyi güvence etmediğini belirtin.

### 2.3 Girdiler

| Girdi | Anahtar | Farklı anahtar sayısı | Not |
|---|---|---|---|
| karışık | | | |
| sıralı | | | |
| ters | | | |
| çok tekrarlı | | | |

> Öğe türünü (ör. 16 baytlık anahtar–indis çifti), veri üretecini ve tohumu yazın. Sayma için K'nin, taban için geçiş sayısının her girdide kaç olduğunu belirtin.

### 2.4 Ölçüm düzeni

> Isınma ve tekrar sayısı (n'e göre değişiyorsa hangi n'de kaç), raporlanan istatistik (ortanca) ve nedeni; her tekrarda başlangıç dizisinin kopyalanması; sayaçların hangi çalıştırmada toplandığı; `qsort`'un karşılaştırmalarının nasıl sayıldığı; "kontrol sağlaması"nın tanımı; `olcer`'in kuram denetimlerinde kaç "UYUMLU", kaç uyumsuzluk çıktığı.

### 2.5 Doğruluk

> Birim test sayısı, kâhin deneme ve denetim sayısı, kâhinlerin neler olduğu, kasıtlı hata gösterimleri, ASan/UBSan sonucu. Ölçülen kodun doğru olduğu gösterilmeden süresi raporlanmaz.

## 3. Sonuçlar

### 3.1 Karesel yöntemler

| algoritma | girdi | 1 000 | 2 000 | 4 000 | 8 000 | 16 000 | T(8 000) / T(4 000) |
|:--|:--|--:|--:|--:|--:|--:|--:|
| seçmeli | karışık | | | | | | |
| | sıralı | | | | | — | |
| | ters | | | | | — | |
| | çok tekrarlı | | | | | — | |
| kabarcık | … | | | | | | |
| araya ekleme | … | | | | | | |

*Tablo 2. Karesel üçlünün süreleri (ortanca) ve oran testi (Θ(n²) için 4).*

`![Dört girdi türü](sekiller/girdiler.png)` ← kendi şekliniz

*Şekil 1. Dokuz algoritma, dört girdi türü — süre (ms, log) – n (log). Her girdi türü ayrı bir panelde.*

### 3.2 Θ(n log n) ve doğrusal yöntemler

| girdi | algoritma | 10³ | 1,6·10⁴ | 10⁵ | 10⁶ | T(10⁶) / T(10⁵) |
|:--|:--|--:|--:|--:|--:|--:|
| karışık | birleştirmeli | | | | | |
| | hızlı | | | | | |
| | öbek | | | | | |
| | sayma | | | | | |
| | taban (LSD) | | | | | |
| | qsort | | | | | |
| sıralı · ters · çok tekrarlı | … | | | | | |

*Tablo 3. Altı yöntemin süreleri (ortanca). Son sütun: n on kat büyüyünce süre kaç kat artar (Θ(n) için 10; Θ(n log n) için 10 · log 10⁶ / log 10⁵ = 12).*

`![Çubuk grafik](sekiller/cubuk.png)` ← kendi şekliniz

*Şekil 2. Sabit bir n'de (ör. 8 000) dokuz algoritmanın dört girdideki süresi (logaritmik ölçek).*

### 3.3 Büyüme eğimleri

| algoritma | karışık | sıralı | ters | çok tekrarlı | kuram |
|:--|--:|--:|--:|--:|:--|
| seçmeli … qsort (9 satır) | | | | | |

*Tablo 4. log t – log n doğrusunun eğimi (en küçük kareler) ve kuramsal değer.*

> Eğimi en az üç n noktasından en küçük karelerle hesaplayın; kullandığınız n aralığını yazın. Θ(n log n)'in [n₁, n₂] aralığındaki kuramsal eğimi: 1 + ln(log n₂ / log n₁) / ln(n₂ / n₁) (16 000 – 10⁶ için ≈ 1,09).

### 3.4 Karşılaştırma ve iş sayıları

| algoritma (n: karesel 8 000, diğerleri 10⁶) | karışık | sıralı | ters | çok tekrarlı |
|:--|--:|--:|--:|--:|
| seçmeli … qsort (karşılaştırmalı 7 yöntem) | | | | |

*Tablo 5. Karşılaştırma sayısı / (n log₂ n). Alt sınırın (log₂ n!) aynı orandaki değerini başlıkta verin.*

| algoritma (n = 10⁶) | girdi | K ya da geçiş | toplama | taşıma | süre |
|:--|:--|--:|--:|--:|--:|
| sayma | 4 girdi | | | | |
| taban (LSD) | 4 girdi | | | | |

*Tablo 6. Karşılaştırmasız yöntemlerin iş sayıları ve kapalı biçimleri (sayma n + K; taban d(n + 256)).*

### 3.5 Kararlılık

| algoritma | kontrol (çok tekrarlı) | kararlı yöntemlerle | kuramda kararlı |
|:--|--:|:-:|:-:|
| 9 satır | | aynı / FARKLI | evet / hayır |

*Tablo 7. Çok tekrarlı girdide kontrol sağlaması.*

### 3.6 Anahtar aralığı

| K | sayma | sayma: toplama | taban | geçiş | birleştirmeli | birleştirmeli / sayma |
|--:|--:|--:|--:|--:|--:|--:|
| 10 … 10⁷ (7 satır) | | | | | | |

*Tablo 8. n = 10⁵, anahtarlar [0, K) aralığında.*

### 3.7 Öbek uygulamaları

| k | ilk-k (öbek) | karşılaştırma | karşılaştırma / n | bütün liste / ilk-k |
|--:|--:|--:|--:|--:|
| 1, 10, 100, 1 000, 10 000, 100 000 | | | | |

*Tablo 9. Başarı listesinin ilk k'sı, n = 10⁵ (bütün listenin sıralanma süresini başlıkta verin).*

| n (k = 10) | ilk-10 (öbek) | karşılaştırma | bütün liste (birleştirmeli) |
|--:|--:|--:|--:|
| 10⁴, 10⁵, 10⁶ | | | |

*Tablo 10. İlk-10'un n ile büyümesi.*

| k | süre (n = 10⁶) | karşılaştırma | karşılaştırma / (n log₂ k) |
|--:|--:|--:|--:|
| 2, 4, 8, 16, 64 | | | |

*Tablo 11. k şubenin çok yollu birleştirilmesi (karşılaştırma için iki işaretçili birleştirme ve uç uca ekleyip sıralama süreleri başlıkta).*

`![Anahtar aralığı ve ilk-k](sekiller/obek.png)` ← kendi şekliniz

*Şekil 3. Sol: anahtar aralığının etkisi (log–log); sağ: ilk-k'nın k ile büyümesi ve bütün listenin sıralanması (yatay çizgi).*

### 3.8 Mini-OBS'ye yansıması

| işlem, n | önceki yöntem | süre | yeni yöntem | süre | hızlanma (kat) | kaynak |
|:--|:--|--:|:--|--:|--:|:--|
| numarayla bulma, 10⁵ | doğrusal (v1.0) | | ikili (v2.3) | | | |
| yükleme, ≥ 3,2 · 10⁴ | v1.0 | | sıralı ekleme (v2.3) | | | |
| yükleme, ≥ 3,2 · 10⁴ | v1.0 | | toplu (v2.5) | | | |
| yükleme, 10⁶ | v1.0 (kestirim) | | toplu (v2.5) | | | |
| yinelenen tespiti, 10⁵ | tüm çiftler (v2.1) | | sıralayarak (v2.5) | | | |

*Tablo 12. v2.3–v2.5'in Mini-OBS işlemlerine etkisi.*

> Her satırın iki süresi aynı ölçüm oturumundan gelmelidir; kestirimi açıkça belirtin. v2.3'ün yükleyicisinin neden hızlanmadığını taşıma sayısıyla açıklayın.

## 4. Tartışma

### 4.1 Kuramla tutarlılık (S2, S3)

> En az şunları tartışın, her iddiayı bir tabloya ya da şekle bağlayın:
>
> - karesel üçlünün oran testleri ve eğimleri; uyarlanabilir yöntemlerin sıralı girdideki davranışı;
> - Θ(n log n) yöntemlerin eğimleri ve kuramsal eğim; karşılaştırma oranları ve alt sınır; hızlı ve öbek sıralamasının birleştirmeliye göre karşılaştırma fazlası;
> - doğrusal yöntemlerde iş sayılarının tam doğrusallığı ile sürenin doğrusallıktan sapması (önbellek, bellek erişim düzeni);
> - `qsort`'un bu platformda nasıl davrandığı (karşılaştırma sayıları, kararlılık) ve bunun neden genellenemeyeceği;
> - kuramla uyuşmayan her ölçüm ve olası nedeni.

### 4.2 Algoritma seçim rehberi (S1, S4, S5, S6)

| Veri durumu | Öneri | Ölçümünüzdeki gerekçe |
|---|---|---|
| küçük n ya da neredeyse sıralı | | |
| genel amaçlı, kararlılık gerekli | | |
| genel amaçlı, kararlılık gerekmiyor, bellek sınırlı | | |
| en kötü durum güvencesi + Θ(1) bellek | | |
| tamsayı anahtar, küçük aralık | | |
| tamsayı anahtar, büyük aralık | | |
| yalnızca ilk k | | |
| k sıralı listenin birleştirilmesi | | |
| hazır çözüm yeterli | | |

*Tablo 13. Algoritma seçim rehberi (ÖÇ 7.5).*

## 5. Geçerlilik tehditleri ve sınırlılıklar

> En az dört madde: ortam (tek makine, yük, güç kipi, sanal makine); öğe türü ve karşılaştırma maliyeti; girdi dağılımları (ölçülmeyen durumlar, ör. hızlı sıralamanın en kötü girdisi); ölçüm kapsamı (kopya, sayaç); derleyici ve bayraklar. Her madde için sonuca olası etkisini yazın.

## 6. Sonuç

> Bir paragraf: araştırma sorularının kısa yanıtları ve Mini-OBS için öneriler (hangi işte hangi algoritma ve neden).

## Ek A. Yeniden üretme

```
cd v2.6
make && make test
make olcum
python3 ../rapor/uret.py      # tablolar ve şekiller
```

> Tek bir ölçüm noktasının komutunu da verin (ör. `./olcer kiyas_taban --sira karisik --n 1000000 --tekrar 3`).

## Ek B. Ham veri dosyaları

| Dosya | İçerik | Kullanıldığı tablo/şekil |
|---|---|---|
| `olcum/kiyas.csv` | 9 algoritma × 4 girdi × n | Tablo 2–7, Şekil 1–2 |
| `olcum/aralik.csv` | anahtar aralığı | Tablo 8, Şekil 3 |
| `olcum/ilk_k*.csv`, `olcum/cok_yollu*.csv` | öbek uygulamaları | Tablo 9–11, Şekil 3 |
| v2.3/v2.5 ölçüm CSV'leri | Mini-OBS'ye yansıma | Tablo 12 |
| `olcum/OLCUM_ORTAMI.txt` | ortam | bölüm 2.1 |

## Ek C. Beyan

> - Yararlanılan kaynaklar (kitap, ders materyali, çevrim içi kaynak).
> - Referans sürümden alınan dosyalar (dosya adlarıyla) — yoksa "yok".
> - Kullanılan araçlar (ör. derleyici dışında betik kütüphaneleri, yapay zekâ araçları) ve hangi amaçla, hangi bölümler için kullanıldıkları; kurumun ve dersin politikasına uygunluk.
> - "Bu rapordaki ölçümler teslim edilen CSV'lerden gelir ve kendi makinemde yapılmıştır." ifadesi, ad ve tarih.

## Kaynaklar

> APA 7. Asgari: Cormen vd. (2022); Sedgewick ve Wayne (2011); kullandıysanız Knuth (1998).

---

## Denetim listesi (teslimden önce silin)

- [ ] Tablo 1–13 ve Şekil 1–3 var; numaralı ve başlıklı.
- [ ] Her süre ortanca; tekrar sayıları bölüm 2.4'te.
- [ ] Bütün büyüme grafikleri log–log; eksen adı, birim ve ölçek yazılı; yazı ≥ 9 pt.
- [ ] Eğimler ve oranlar hesaplandı; kuramsal değerlerle yan yana.
- [ ] Kararlılık sağlaması ve anahtar aralığı deneyi yorumlandı.
- [ ] Kestirimler etiketli; makine bilgisi ve sınırlılıklar var.
- [ ] Bütün sayılar CSV'den betikle üretildi (Ek B).
- [ ] ≤ 12 sayfa (ekler hariç); PDF açılıyor.
