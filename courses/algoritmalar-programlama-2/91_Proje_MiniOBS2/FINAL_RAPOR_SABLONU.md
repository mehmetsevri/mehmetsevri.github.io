# Final Projesi Rapor Şablonu — tasarım, doğrulama ve dönem kıyaslaması raporu

**Ders:** Algoritma ve Programlama – II (C17) · Final projesi (sunum H14)

**Yönerge:** [FINAL_PROJE_YONERGESI.md](FINAL_PROJE_YONERGESI.md) · Başvuru örneği (varsayılan proje): [v3.0/mini_obs_v3_0_olcum_raporu.md](v3.0/mini_obs_v3_0_olcum_raporu.md) · Sürüm belgesi: [v3.0/mini_obs_v3_0.md](v3.0/mini_obs_v3_0.md)

Bu şablonu kopyalayıp `rapor/final_raporu.md` adıyla doldurun. `>` ile başlayan yönerge satırlarını silin; başlıkları, tablo ve şekil numaralarını koruyun; şekil satırlarının başındaki ve sonundaki ters tırnakları kaldırıp kendi dosya adlarınızı yazın. Şablon iki tür projeye uyar: **varsayılan proje** (Mini-OBS 2 v3.0) ve **seçenek havuzundan bir proje** (yönerge § 2.2). Seçenek havuzundaki projelerde "ilk sürüm" doğruluğu apaçık ama yavaş **taban çizgisi** (kaba kuvvet, doğrusal tarama, dizi tabanlı Dijkstra …), "son sürüm" ise sizin algoritmik gerçekleştiriminizdir. Başvuru raporu biçim için bir örnektir: **sayılarınız kendi makinenizden gelmelidir.**

## Biçim kuralları

- **Uzunluk:** en çok 15 sayfa (ekler hariç). **Dosyalar:** Markdown kaynağı + PDF + `sekiller/` + tabloları ve grafikleri CSV'den üreten betik.
- **Sayılar:** Türkçe biçim — ondalık virgül (77,5), binlik ayırıcı boşluk (4 932); birimler ns, µs, ms, s, dk. Süreler en çok 3–4 anlamlı basamakla verilir. Oranlar ve katlar CSV'den **betikle** hesaplanır; elle yazılmaz.
- **Tablolar:** numaralı ve başlıklı ("*Tablo 3. …*"); sütun adında birim (`süre (ms)`) ya da hücrede birim; sayılar sağa yaslı.
- **Şekiller:** numaralı, başlıklı; eksen adı, birim ve ölçek türü ("log") yazılı; büyüme karşılaştırmasında log–log eksen, büyük oranlar için logaritmik çubuk; kestirimler görsel olarak ayrışır (taralı çubuk, boş işaret, kesikli çizgi); yazı basılı sayfada ≥ 9 pt; renk tek başına anlam taşımaz.
- **Kaynak:** her sayı `olcum/*.csv`'den betikle üretilir; Ek B hangi tablonun hangi dosyadan geldiğini gösterir.
- **Kestirim:** ölçülemeyen değerler (ör. karesel bir yöntemin 10⁶'daki süresi) yöntemiyle (formül, dayandığı ölçüm noktası) birlikte "kestirim" diye etiketlenir; tabloda ayrı sütun ya da işaretle gösterilir.
- **Kaynakça:** APA 7.
- **PDF:** örneğin (pandoc ve wkhtmltopdf ile)

```bash
pandoc final_raporu.md -f markdown-implicit_figures -s -o final_raporu.pdf \
  --pdf-engine=wkhtmltopdf --pdf-engine-opt=--enable-local-file-access \
  -V maxwidth=100% -V margin-top=15mm -V margin-bottom=15mm \
  -V margin-left=15mm -V margin-right=15mm --metadata pagetitle="Final raporu"
```

Alternatif: Markdown'ı bir kelime işlemciye aktarıp PDF olarak kaydetmek; biçim kuralları aynıdır.

---

# <Proje adı> — Tasarım, Doğrulama ve Dönem Kıyaslaması Raporu

**Ad Soyad · Öğrenci no** · AP-2 Final Projesi · Seçenek: varsayılan (Mini-OBS 2 v3.0) / <havuzdan seçenek> · Depo etiketi: `v3.0` ya da `final` · Ölçüm tarihi: GG.AA.YYYY

## Özet

> En çok 250 sözcük. Proje ne yapıyor (bir cümle); kaç modül ve hangi algoritmalar; doğrulama (test sayıları, kâhinler, stres, bellek denetimi, kapsam yüzdesi); en önemli üç ölçüm bulgusu **sayılarla** (ör. "10⁶ kayıtta yinelenen tespiti tüm çiftlerle ≈ X dk sürerdi (kestirim), karma kümesiyle Y ms"); bir sınırlılık.

## 1. Amaç ve araştırma soruları

> Projenin problemini ve kullanıcısını bir paragrafta anlatın. Aşağıdaki soruları yanıtlayın; projenize özgü soru ekleyin (en az bir tane).

- **S1.** Her işlemin ilk (kaba kuvvet / taban çizgisi) ve son (algoritmik) gerçekleştirimi arasındaki fark büyük ölçekte (10⁵–10⁶) ne kadardır?
- **S2.** Ölçülen büyüme (oran testleri, log–log eğimler, sayaçlar) kuramsal karmaşıklıklarla uyuşuyor mu? Uyuşmuyorsa neden?
- **S3.** Algoritma değişikliğinin kazancı, derleyici iyileştirmesinin (-O0 → -O2) kazancıyla karşılaştırıldığında nerededir?
- **S4.** Darboğaz nerededir ve ölçülerek mi bulundu (profil, sayaç, stres testi)?
- **S5.** (NP-zor bir alt problem varsa) Sezgisel çözüm alt sınıra ve küçük örneklerde kesin çözüme göre ne kadar iyidir?
- **S6.** Sistemin ölçeklenebilirlik sınırı nedir (süre bütçesi, bellek)?

## 2. Sistem tasarımı

### 2.1 Mimari

`![Mimari](sekiller/mimari.png)` ← kendi şekliniz

*Şekil 1. Katmanlar ve modüller (giriş kipleri → komut katmanı → uygulama durumu → algoritma modülleri → çekirdek). Okların yönü "kullanır" ilişkisidir.*

> Modül sınırlarını anlatın: hangi modül hangisini kullanır, hangi modül hiçbir duruma sahip değildir, durum nerede tutulur. Döngüsel bağımlılık olmamalıdır.

### 2.2 Modüller

| Modül (`.h` + `.c`) | Sorumluluk | Dışa açık fonksiyon sayısı | Satır | Kullandığı modüller |
|---|---|--:|--:|---|
| | | | | |

*Tablo 1. Modüller ve sorumlulukları (satır sayıları `wc -l` ile).*

### 2.3 Veri yapıları ve bellek sahipliği

| Yapı | Kim ayırır | Kim serbest bırakır | Yaşam süresi |
|---|---|---|---|
| | | | |

*Tablo 2. Bellek sahipliği — projenin bütün yapıları TEK tabloda.*

> Her ayıran fonksiyonun başlık yorumunda sahiplik sözleşmesi bulunmalıdır. Önbellek ya da dizin tutuyorsanız geçersiz kılma kuralını (ne zaman yeniden kurulur) yazın.

### 2.4 Hata bildirimi, çıkış kodları ve yapılandırma

| Durum | Anlamı | Çıkış kodu | Örnek ileti |
|---|---|:-:|---|
| | | 0 / 1 / 2 | |

*Tablo 3. Tek tip hata bildirimi.*

> Yapılandırma dosyasının anahtarlarını (tür, aralık, varsayılan) ve geçersiz değer davranışını bir tabloyla verin.

## 3. Algoritma seçimleri

| İşlev | Algoritma / veri yapısı | En iyi | Ortalama | En kötü | Ek bellek | Gerekçe (ölçüm ya da kuram) | Değerlendirilen alternatif |
|---|---|:-:|:-:|:-:|:-:|---|---|
| | | | | | | | |

*Tablo 4. Algoritma kimlik kartları ve seçim gerekçeleri (en az: bir arama, bir sıralama, bir dinamik veri yapısı, bir graf ya da DP algoritması).*

| İşlem | İlk gerçekleştirim (sürüm / taban çizgisi) | Son gerçekleştirim | Beklenen kazanç (kuram) |
|---|---|---|---|
| | | | |

*Tablo 5. Dönem kıyaslamasının çiftleri: her işlemin ilk ve son gerçekleştirimi. İki gerçekleştirim AYNI programda, AYNI derlemeyle ölçülür.*

> NP-zor bir alt problem varsa (ör. sınav günü sayısı, AKTS sınırlı dönem planı, bulmaca) hangi sezgiseli, hangi alt sınırı ve hangi kesin yöntemi (küçük n) kullandığınızı yazın.

## 4. Doğrulama

| Test türü | Program / hedef | Sayı | Ne denetler? |
|---|---|--:|---|
| birim (elle izlenmiş) | | doğrulama | |
| kâhinle karşılaştırmalı | | deneme · denetim | |
| stres (rastgele işlem dizisi + büyük veri) | | işlem · kayıt | |
| regresyon | | karşılaştırma | |
| kasıtlı hata gösterimi | `--hata-goster …` | hata | |

*Tablo 6. Test paketi (`make test`).*

| Sınanan işlev | Kâhin (farklı yol) | Girdi üretimi | Sınır durumları |
|---|---|---|---|
| | | | |

*Tablo 7. Kâhinler. Kâhin sınanan fonksiyonu çağırmamalıdır.*

> Bellek denetimi: `make asan` ve `make valgrind` sonuçları (çalıştırma sayısı, "ERROR SUMMARY: 0 errors", "definitely lost: 0 bytes"). Stres testinin bulduğu bir hata ya da darboğaz varsa nasıl bulunduğunu ve nasıl giderildiğini anlatın.

## 5. Ölçüm yöntemi

### 5.1 Ortam (makine bilgisi)

| Öğe | Değer |
|---|---|
| İşlemci | model, çekirdek sayısı (sanal makine / WSL / doğrudan) |
| Önbellek | L1d, L2, L3 |
| Bellek | toplam RAM; ölçümlerdeki tepe süreç belleği |
| İşletim sistemi | dağıtım ve sürüm (WSL ise Windows sürümü de) |
| Derleyici ve bayraklar | `gcc --version`; `-std=c17 -Wall -Wextra -pedantic -O2 -g` (ve -O0 kıyası) |
| C kütüphanesi | glibc / MSVCRT / UCRT sürümü |
| Güç ve yük | prize takılı mı, güç kipi; başka işler; ölçüm başında ve sonunda yük ortalaması |
| Ölçüm tarihi ve süresi | `make olcum`'un toplam süresi |

*Tablo 8. Ölçüm ortamı (`olcum/OLCUM_ORTAMI.txt`).*

### 5.2 Girdiler ve düzen

> Veri üreteci ve tohum; her işlemin n listesi (algoritmik sürümler 10⁶'ya kadar; karesel sürümler 10⁴–10⁵); ısınma ve tekrar sayısı, raporlanan istatistik (ortanca) ve nedeni; sayaçların hangi çalıştırmada toplandığı; kontrol sağlamasının tanımı ve iki gerçekleştirimde aynı çıktığı; süre bütçesi ve bütçeyi aşan noktalarda ne yapıldığı.

### 5.3 Kestirim yöntemi

> Karesel yöntemlerde T(N) = T(n) · (N/n)²; üstel yöntemlerde (geri izleme) düğüm başına süre × kesin düğüm sayısı ya da büyüme oranı. Kestirimin hangi ölçüm noktasına dayandığını ve neden **alt sınır** olabileceğini (önbellek hiyerarşisi, bellek) yazın.

## 6. Sonuçlar

### 6.1 Dönem kıyaslaması

| İşlem | n | İlk gerçekleştirim | süre | Son gerçekleştirim | süre | kazanç (kat) | not |
|---|--:|---|--:|---|--:|--:|---|
| | 10⁶ | | (kestirim) | | | | |

*Tablo 9. İlk ve son gerçekleştirimlerin büyük ölçekte karşılaştırması. Kestirimler işaretli.*

`![Dönem kıyaslaması](sekiller/donem.png)` ← kendi şekliniz

*Şekil 2. Aynı n'de ilk ve son gerçekleştirimin süresi (yatay çubuk, logaritmik eksen); kestirimler taralı; sağda kazanç.*

### 6.2 Büyüme, oran testleri ve eğimler

| İşlem / gerçekleştirim | n aralığı | T(2n)/T(n) ya da T(10n)/T(n) | log–log eğim | kuram |
|---|---|--:|--:|---|
| | | | | |

*Tablo 10. Ölçülen büyüme ve kuramsal değer (Θ(n²) için T(2n)/T(n) = 4, eğim 2; Θ(n) için 10n'de 10; Θ(n log n) için [n₁, n₂] aralığında eğim 1 + ln(log n₂ / log n₁) / ln(n₂ / n₁)).*

`![Büyüme](sekiller/buyume.png)` ← kendi şekliniz

*Şekil 3. Süre (log) – n (log); her işlem ailesi bir panel; ölçüm dolu, kestirim boş işaret ve kesikli çizgi.*

### 6.3 Sayaçlar ve kapalı biçimler

| İşlem | Sayaç (ör. karşılaştırma, yoklama, taşıma, düğüm) | Ölçülen | Kapalı biçim | Uyum |
|---|---|--:|---|:-:|
| | | | ör. n(n − 1)/2 | birebir / yaklaşık |

*Tablo 11. Deterministik sayaçlar ve kuramsal formüller.*

### 6.4 Derleyici kazancı ↔ algoritma kazancı

| İşlem | n | -O0 | -O2 | derleyici kazancı | ilk / son (aynı n, -O2) | algoritma kazancı |
|---|--:|--:|--:|--:|--:|--:|
| | | | | | | |

*Tablo 12. Aynı algoritmanın iyileştirmesiz ve iyileştirmeli derlemesi; aynı n'de iki algoritma.*

### 6.5 (İsteğe bağlı) Profil ve darboğaz

> `gprof` (`-pg` ile ayrı derleme) ya da `perf` çıktısının özeti; darboğaz fonksiyonu, payı ve yaptığınız değişiklik. Profil çıktıları stdout'ta değil, ayrı dosyada "bu çalıştırmada" etiketiyle tutulur.

## 7. Kuramla karşılaştırma ve tartışma

> En az şunları tartışın; her iddiayı bir tabloya ya da şekle bağlayın:
>
> - oran testleri ve eğimlerin kuramla uyumu; sayaçların kapalı biçimlerle birebir uyumu;
> - süre oranlarının sayaç oranlarından sapması ve olası nedenleri (önbellek: veri L2/L3'ü aştığında; sabit çarpanlar; bellek ayırma);
> - küçük n'de karesel yöntemin daha hızlı olduğu bir durum varsa kesişim noktası ve nedeni;
> - algoritma kazancı ile derleyici kazancının büyüklük sırası (S3);
> - sezgisel çözümlerin alt sınıra uzaklığı ve küçük örneklerde kesin çözümle karşılaştırma (S5);
> - kuramla uyuşmayan her ölçüm ve olası nedeni.

## 8. Sınırlılıklar ve geçerlilik tehditleri

> En az beş madde; her biri için sonuca olası etkisi: ortam (tek makine, sanal makine, başka süreçler, güç kipi); girdi dağılımları (ölçülmeyen durumlar, en kötü girdi); kestirimlerin varsayımları (önbellek hiyerarşisi değişimi); ölçüm kapsamı (dosya okuma dahil mi, sayaçlar ayrı mı); derleyici ve bayraklar; kapsam dışı bırakılan özellikler.

## 9. Sonuç ve genişletme seçenekleri

> Bir paragraf: araştırma sorularının kısa yanıtları. Sonra projenin bir sonraki adımı olabilecek en az üç genişletme (gerekçesiyle, ör. artımlı dizin güncelleme, DSatur, uzunluk sınırlı Huffman kodları).

## Ek A. Yeniden üretme

```
cd v3.0                     # ya da proje klasörünüz
make && make test
make asan && make valgrind
make kapsam                 # gcov satır kapsamı (Ek C)
make olcum
python3 ../rapor/uret.py    # tablolar ve şekiller
```

> Tek bir ölçüm noktasının komutunu da verin (ör. `./olcer_donem yinelenen_karma --n 1000000 --tekrar 3`).

## Ek B. Ham veri dosyaları

| Dosya | İçerik | Kullanıldığı tablo/şekil |
|---|---|---|
| `olcum/*.csv` | ölçüm noktaları (sütunlar: işlem, sürüm, yöntem, derleme, n, q, tekrar, ortanca_ms, en_az_ms, sayaç, kontrol, kestirim) | Tablo 9–12, Şekil 2–3 |
| `olcum/OLCUM_ORTAMI.txt` | ortam | Tablo 8 |
| test ve bellek denetimi çıktıları | `make test`, `make asan`, `make valgrind` günlükleri | Tablo 6, bölüm 4 |
| `kapsam/KAPSAM.txt` | gcov satır kapsamı | Ek C |

## Ek C. Test kapsamı

| Kaynak | Satır | Çalışan | Yüzde | Çalışmayan satırların başlıca nedeni |
|---|--:|--:|--:|---|
| | | | | ör. bellek yetmezliği dalı, yalnız ölçümde kullanılan kod |
| **TOPLAM** | | | | |

*Tablo C.1. gcov ile satır kapsamı (bu makinede; `make kapsam`). Kapsama alınan testleri ve kapsam dışında tutulan dosyaları (ör. test programlarının kendisi) başlıkta yazın.*

> Kapsamın %100 olmasının hedef olmadığını, ama çalışmayan her önemli dalın bilinçli olarak açıklanması gerektiğini unutmayın: kapsam "bu satır testlerde çalıştı" demektir, "bu satır doğru" demek değildir. Kapsamı düşük bir modül için hangi testi eklediğinizi (ya da neden eklemediğinizi) yazın.

## Ek D. Beyan

> - Yararlanılan kaynaklar (kitap, ders materyali, çevrim içi kaynak).
> - Referans sürümlerden alınan dosyalar (dosya adlarıyla) — yoksa "yok".
> - Kullanılan araçlar (ör. derleyici dışında betik kütüphaneleri, profil araçları, yapay zekâ araçları) ve hangi amaçla, hangi bölümler için kullanıldıkları; kurumun ve dersin politikasına uygunluk.
> - "Bu rapordaki ölçümler teslim edilen CSV'lerden gelir ve kendi makinemde yapılmıştır." ifadesi, ad ve tarih.

## Kaynaklar

> APA 7. Asgari: Cormen vd. (2022); Sedgewick ve Wayne (2011); projenizin algoritmalarının özgün kaynakları (ör. Kahn, 1962; Dijkstra, 1959; Huffman, 1952; Kruskal, 1956) ve performans mühendisliği için Knuth (1974).

---

## Denetim listesi (teslimden önce silin)

- [ ] Tablo 1–12, Tablo C.1 ve Şekil 1–3 var; numaralı ve başlıklı.
- [ ] Mimari diyagram ve tek bellek sahipliği tablosu var.
- [ ] Her süre ortanca; tekrar sayıları ve süre bütçesi bölüm 5.2'de.
- [ ] Algoritmik gerçekleştirimler 10⁶'da (ya da projenin büyük ölçeğinde) ölçüldü; karesel/üstel olanlar 10⁴–10⁵'te ölçülüp kestirildi; kestirimler etiketli.
- [ ] Bütün büyüme grafikleri log–log; eksen adı, birim ve ölçek yazılı; yazı ≥ 9 pt.
- [ ] Oran testleri, eğimler ve sayaçlar kuramla yan yana.
- [ ] Derleyici ↔ algoritma kazancı tablosu var.
- [ ] Makine bilgisi, sınırlılıklar ve test kapsamı eki var.
- [ ] Bütün sayılar CSV'den betikle üretildi (Ek B).
- [ ] ≤ 15 sayfa (ekler hariç); PDF açılıyor.
