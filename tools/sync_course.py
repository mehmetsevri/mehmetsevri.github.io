"""Algoritma ve Programlama-1 ders sitesini kişisel siteye eşitler.

Kaynak klasördeki 99_Web_Crash_Course/index.html sayfasını
courses/algoritmalar-programlama-1/ altına kopyalar; sayfanın kullandığı
görselleri ve haftalık materyalleri aynı göreli yollarla taşır.

Varsayılan yayın politikası (ders sahibinin tercihi):
  - Ders notu PDF'leri ve kod ZIP'leri yayınlanır.
  - Sunumlar (PPTX) PowerPoint ile PDF'e çevrilir; bağlantılar PDF'i gösterir.
  - Word (DOCX) dosyaları yayınlanmaz; bağlantıları sayfadan kaldırılır.

Yalnızca sayfanın başvurduğu dosyalar kopyalanır (beyaz liste). Örneğin
92_Degerlendirme (çözümler, soru bankası) hiçbir zaman yayına girmez.

Kullanım (depo kökünden, Windows + PowerPoint gerekir):
    python tools/sync_course.py
    python tools/sync_course.py --exclude docx --exclude zip   # ZIP'leri de yayınlama
    python tools/sync_course.py --keep-pptx                    # sunumları PPTX olarak bırak
    python tools/sync_course.py --src "D:/baska/yol/Sunum ve Materyaller"
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SRC = r"C:\Users\sevri\OneDrive\Desktop\DERSLER\Algoritma ve Programlama - 1\Sunum ve Materyaller"
DEST = os.path.join(ROOT, "courses", "algoritmalar-programlama-1")
PAGE = os.path.join("99_Web_Crash_Course", "index.html")

IMG_RE = re.compile(r"""(["'])\.\./(H\d\d_[^"'<>]+?\.(?:png|jpe?g|webp|svg|gif))\1""", re.I)
MAT_A_RE = re.compile(r'<a data-mat="([^"]+)">(.*?)</a>', re.S)
CFG_RE = re.compile(r'window\.AP1_MAT_BASE="[^"]*";window\.AP1_PDF_ONLY=(?:true|false);')

# Ana siteye dönüş bağlantısı: ders sitesinin kendi renk değişkenlerini kullanır.
BACKLINK = (
    '<a class="ms-home" href="../../" title="Mehmet Sevri — ana sayfa" '
    'style="display:inline-flex;align-items:center;gap:6px;margin:4px 0 10px;padding:6px 10px;'
    'border:1px solid var(--line);border-radius:8px;color:var(--muted);font-size:13px;'
    'text-decoration:none">&larr; Mehmet Sevri &middot; Ana sayfa</a>'
)

PS_CONVERT = r"""
$ErrorActionPreference = 'Stop'
$pairs = Get-Content -LiteralPath $args[0] -Encoding UTF8
$pp = New-Object -ComObject PowerPoint.Application
try {
  foreach ($line in $pairs) {
    if (-not $line) { continue }
    $src, $dst = $line -split "`t"
    $pres = $pp.Presentations.Open($src, -1, 0, 0)   # ReadOnly, Untitled=false, WithWindow=false
    try { $pres.SaveAs($dst, 32) } finally { $pres.Close() }   # 32 = ppSaveAsPDF
    Write-Output ("pdf: " + $dst)
  }
} finally { $pp.Quit() }
"""


def convert_pptx(jobs):
    """jobs: [(src_pptx_abs, dst_pdf_abs)] — PowerPoint COM ile PDF'e çevirir."""
    if not jobs:
        return
    with tempfile.TemporaryDirectory() as tmp:
        lst = os.path.join(tmp, "jobs.txt")
        ps1 = os.path.join(tmp, "convert.ps1")
        with open(lst, "w", encoding="utf-8") as fh:
            fh.write("\n".join(f"{s}\t{d}" for s, d in jobs))
        with open(ps1, "w", encoding="utf-8-sig") as fh:
            fh.write(PS_CONVERT)
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1, lst],
                           capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("PPTX → PDF dönüşümü başarısız (PowerPoint gerekli):\n" + r.stdout + r.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=DEFAULT_SRC, help="'Sunum ve Materyaller' klasörü")
    ap.add_argument("--exclude", action="append", default=None, metavar="UZANTI",
                    help="yayınlanmayacak materyal uzantısı (tekrarlanabilir; varsayılan: docx)")
    ap.add_argument("--keep-pptx", action="store_true", help="sunumları PDF'e çevirmeden PPTX olarak yayınla")
    ap.add_argument("--no-backlink", action="store_true", help="ana siteye dönüş bağlantısını ekleme")
    ap.add_argument("--dest", default=DEST, help=argparse.SUPPRESS)
    args = ap.parse_args()
    dest = args.dest
    exclude = {e.lower().lstrip(".") for e in (args.exclude or ["docx"])}

    page_path = os.path.join(args.src, PAGE)
    if not os.path.isfile(page_path):
        sys.exit(f"Ders sayfası bulunamadı: {page_path}")
    html = open(page_path, encoding="utf-8").read()

    images = sorted({m.group(2) for m in IMG_RE.finditer(html)})

    # Materyal bağlantıları: hariç tutulanları kaldır, PPTX'leri PDF'e yönlendir.
    copies = {}       # yayın yolu -> kaynak yolu (birebir kopya)
    conversions = {}  # yayın yolu (.pdf) -> kaynak .pptx

    def rewrite(m):
        rel, inner = m.group(1), m.group(2)
        ext = rel.rsplit(".", 1)[-1].lower()
        if ext in exclude:
            return ""
        if ext == "pptx" and not args.keep_pptx:
            pub = rel[:-5] + ".pdf"
            conversions[pub] = rel
            inner = inner.replace("(PPTX)", "(PDF)").replace(".pptx", ".pdf").replace("PPTX", "PDF")
            return f'<a data-mat="{pub}">{inner}</a>'
        copies[rel] = rel
        return m.group(0)

    html = MAT_A_RE.sub(rewrite, html)

    # Sayfa düzenlemeleri: görsel yolları kök dizine, materyal tabanı aynı klasöre.
    html, n_img = IMG_RE.subn(lambda m: f"{m.group(1)}{m.group(2)}{m.group(1)}", html)
    html, n_cfg = CFG_RE.subn('window.AP1_MAT_BASE="./";window.AP1_PDF_ONLY=false;', html, count=1)
    if n_cfg != 1:
        sys.exit("AP1_MAT_BASE / AP1_PDF_ONLY ayarı sayfada bulunamadı; sayfa yapısı değişmiş olabilir.")
    if not args.no_backlink and 'class="ms-home"' not in html:
        html, n_bl = re.subn(r'(<aside class="side"[^>]*>)', r"\1" + BACKLINK, html, count=1)
        if n_bl != 1:
            print("Uyarı: kenar çubuğu bulunamadı, dönüş bağlantısı eklenmedi.")
    if 'rel="icon"' not in html:
        html = html.replace("</head>", '<link rel="icon" href="../../assets/img/favicon.svg" type="image/svg+xml"></head>', 1)

    sources = images + list(copies.values()) + list(conversions.values())
    missing = [p for p in sources if not os.path.isfile(os.path.join(args.src, p))]
    if missing:
        sys.exit("Kaynakta eksik dosyalar:\n  " + "\n  ".join(missing))

    wanted = {"index.html"} | {p.replace("\\", "/") for p in images + list(copies) + list(conversions)}

    # Hedefi temiz eşitle: listede olmayan eski dosyaları kaldır.
    os.makedirs(dest, exist_ok=True)
    removed = 0
    for dirpath, _, files in os.walk(dest):
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), dest).replace("\\", "/")
            if rel not in wanted:
                os.remove(os.path.join(dirpath, f))
                removed += 1
    for dirpath, _, _ in sorted(os.walk(dest), key=lambda t: -len(t[0])):
        if dirpath != dest and not os.listdir(dirpath):
            os.rmdir(dirpath)

    def stale(src, dst):
        return not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src)

    copied = 0
    for rel in images + list(copies):
        src, dst = os.path.join(args.src, rel), os.path.join(dest, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if stale(src, dst) or os.path.getsize(dst) != os.path.getsize(src):
            shutil.copy2(src, dst)
            copied += 1

    jobs = []
    for pub, rel in sorted(conversions.items()):
        src, dst = os.path.abspath(os.path.join(args.src, rel)), os.path.abspath(os.path.join(dest, pub))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if stale(src, dst):
            jobs.append((src, dst))
    if jobs:
        print(f"PowerPoint ile {len(jobs)} sunum PDF'e çevriliyor…")
    convert_pptx(jobs)

    with open(os.path.join(dest, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)

    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(dest) for f in fs)
    big = [os.path.join(dp, f) for dp, _, fs in os.walk(dest) for f in fs
           if os.path.getsize(os.path.join(dp, f)) > 50 * 1024 * 1024]
    for b in big:
        print(f"Uyarı: {b} 50 MB'tan büyük (GitHub sınırı 100 MB).")
    print(f"Ders sitesi eşitlendi → {os.path.relpath(dest, ROOT)}")
    print(f"  görsel: {len(images)} (yol düzeltilen {n_img}); materyal: {len(copies)} kopya + "
          f"{len(conversions)} PDF sunum; hariç: {', '.join(sorted(exclude)) or '-'}")
    print(f"  kopyalanan: {copied}, çevrilen: {len(jobs)}, kaldırılan eski dosya: {removed}; toplam {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
