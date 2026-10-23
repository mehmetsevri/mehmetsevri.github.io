"""Ders sitelerini kişisel siteye eşitler (Algoritmalar ve Programlama I ve II).

Her dersin kaynak klasöründeki 99_Web_Crash_Course/index.html sayfası
courses/<ders>/ altına kopyalanır; sayfanın kullandığı görseller ve haftalık
materyaller aynı göreli yollarla taşınır.

Yayın politikası (ders sahibinin tercihi):
  - Ders notu PDF'leri, kod ZIP'leri ve proje yönergeleri (Markdown) yayınlanır.
  - Sunumlar (PPTX) PowerPoint ile PDF'e çevrilir; bağlantılar PDF'i gösterir.
  - Word (DOCX) dosyaları yayınlanmaz; bağlantıları sayfadan kaldırılır.
  - Derse özel gizli dosyalar (ör. AP-2 final projesi referans çözümü) kopyalanmaz;
    sayfadaki bağlantıları pasif ("dersin klasöründe") görünür.

Yalnızca sayfanın başvurduğu dosyalar kopyalanır (beyaz liste). Örneğin
92_Degerlendirme (çözümler, soru bankası) hiçbir zaman yayına girmez.

Kullanım (depo kökünden, Windows + PowerPoint gerekir):
    python tools/sync_course.py                 # tüm dersler
    python tools/sync_course.py --course ap2    # yalnız bir ders
    python tools/sync_course.py --course ap1 --src "D:/baska/yol/Sunum ve Materyaller"
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DERSLER = r"C:\Users\sevri\OneDrive\Desktop\DERSLER"
COURSES = {
    "ap1": {
        "src": os.path.join(DERSLER, "Algoritma ve Programlama - 1", "Sunum ve Materyaller"),
        "dest": os.path.join(ROOT, "courses", "algoritmalar-programlama-1"),
        "private": [],
    },
    "ap2": {
        "src": os.path.join(DERSLER, "Algoritma ve Programlama - 2", "Sunum ve Materyaller"),
        "dest": os.path.join(ROOT, "courses", "algoritmalar-programlama-2"),
        # final projesi referans çözümü: yayınlanmaz
        "private": ["91_Proje_MiniOBS2/v3.0/"],
    },
}
PAGE = os.path.join("99_Web_Crash_Course", "index.html")

IMG_RE = re.compile(r"""(["'])\.\./(H\d\d_[^"'<>]+?\.(?:png|jpe?g|webp|svg|gif))\1""", re.I)
MAT_A_RE = re.compile(r'<a data-mat="([^"]+)"([^>]*)>(.*?)</a>', re.S)
CFG_RE = re.compile(r'window\.(AP\d+)_MAT_BASE="[^"]*";window\.\1_PDF_ONLY=(?:true|false);')

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


def sync_course(key, src, dest, private, exclude, keep_pptx, backlink):
    page_path = os.path.join(src, PAGE)
    if not os.path.isfile(page_path):
        sys.exit(f"[{key}] Ders sayfası bulunamadı: {page_path}")
    html = open(page_path, encoding="utf-8").read()

    images = sorted({m.group(2) for m in IMG_RE.finditer(html)})

    copies = {}       # yayın yolu -> kaynak yolu (birebir kopya)
    conversions = {}  # yayın yolu (.pdf) -> kaynak .pptx
    hidden = set()    # pasifleştirilen özel dosyalar

    def rewrite(m):
        rel, attrs, inner = m.group(1), m.group(2), m.group(3)
        ext = rel.rsplit(".", 1)[-1].lower()
        if ext in exclude:
            return ""
        if any(rel.startswith(p) for p in private):
            hidden.add(rel)
            attrs = re.sub(r'\s(?:title|class)="[^"]*"', '', attrs)
            return ('<a class="off" title="Bu dosya dersin paylaşılan klasöründe: ' + rel + '"' + attrs + '>' + inner +
                    '<span class="klasor">dersin klasöründe</span></a>')
        if ext == "pptx" and not keep_pptx:
            pub = rel[:-5] + ".pdf"
            conversions[pub] = rel
            inner = inner.replace("(PPTX)", "(PDF)").replace(".pptx", ".pdf").replace("PPTX", "PDF")
            return f'<a data-mat="{pub}"{attrs}>{inner}</a>'
        copies[rel] = rel
        return m.group(0)

    html = MAT_A_RE.sub(rewrite, html)

    # Sayfa düzenlemeleri: görsel yolları kök dizine, materyal tabanı aynı klasöre.
    html, n_img = IMG_RE.subn(lambda m: f"{m.group(1)}{m.group(2)}{m.group(1)}", html)
    html, n_cfg = CFG_RE.subn(lambda m: f'window.{m.group(1)}_MAT_BASE="./";window.{m.group(1)}_PDF_ONLY=false;',
                              html, count=1)
    if n_cfg != 1:
        sys.exit(f"[{key}] *_MAT_BASE / *_PDF_ONLY ayarı sayfada bulunamadı; sayfa yapısı değişmiş olabilir.")
    if backlink and 'class="ms-home"' not in html:
        html, n_bl = re.subn(r'(<aside class="side"[^>]*>)', r"\1" + BACKLINK, html, count=1)
        if n_bl != 1:
            print(f"[{key}] Uyarı: kenar çubuğu bulunamadı, dönüş bağlantısı eklenmedi.")
    if 'rel="icon"' not in html:
        html = html.replace("</head>", '<link rel="icon" href="../../assets/img/favicon.svg" type="image/svg+xml"></head>', 1)

    sources = images + list(copies.values()) + list(conversions.values())
    missing = [p for p in sources if not os.path.isfile(os.path.join(src, p))]
    if missing:
        sys.exit(f"[{key}] Kaynakta eksik dosyalar:\n  " + "\n  ".join(missing))

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

    def stale(s, d):
        return not os.path.exists(d) or os.path.getmtime(d) < os.path.getmtime(s)

    copied = 0
    for rel in images + list(copies):
        s, d = os.path.join(src, rel), os.path.join(dest, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if stale(s, d) or os.path.getsize(d) != os.path.getsize(s):
            shutil.copy2(s, d)
            copied += 1

    jobs = []
    for pub, rel in sorted(conversions.items()):
        s, d = os.path.abspath(os.path.join(src, rel)), os.path.abspath(os.path.join(dest, pub))
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if stale(s, d):
            jobs.append((s, d))
    if jobs:
        print(f"[{key}] PowerPoint ile {len(jobs)} sunum PDF'e çevriliyor…")
    convert_pptx(jobs)

    with open(os.path.join(dest, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)

    total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(dest) for f in fs)
    for dp, _, fs in os.walk(dest):
        for f in fs:
            if os.path.getsize(os.path.join(dp, f)) > 50 * 1024 * 1024:
                print(f"[{key}] Uyarı: {os.path.join(dp, f)} 50 MB'tan büyük (GitHub sınırı 100 MB).")
    print(f"[{key}] Ders sitesi eşitlendi → {os.path.relpath(dest, ROOT)}")
    print(f"  görsel: {len(images)} (yol düzeltilen {n_img}); materyal: {len(copies)} kopya + "
          f"{len(conversions)} PDF sunum; hariç: {', '.join(sorted(exclude)) or '-'}; "
          f"yayınlanmayan özel dosya: {len(hidden)}")
    print(f"  kopyalanan: {copied}, çevrilen: {len(jobs)}, kaldırılan eski dosya: {removed}; toplam {total / 1e6:.1f} MB")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--course", choices=sorted(COURSES), action="append",
                    help="eşitlenecek ders (tekrarlanabilir; varsayılan: tümü)")
    ap.add_argument("--src", help="tek ders için 'Sunum ve Materyaller' klasörü")
    ap.add_argument("--exclude", action="append", default=None, metavar="UZANTI",
                    help="yayınlanmayacak materyal uzantısı (tekrarlanabilir; varsayılan: docx)")
    ap.add_argument("--keep-pptx", action="store_true", help="sunumları PDF'e çevirmeden PPTX olarak yayınla")
    ap.add_argument("--no-backlink", action="store_true", help="ana siteye dönüş bağlantısını ekleme")
    ap.add_argument("--dest", help=argparse.SUPPRESS)
    args = ap.parse_args()

    keys = args.course or sorted(COURSES)
    if (args.src or args.dest) and len(keys) != 1:
        sys.exit("--src/--dest yalnızca tek bir --course ile kullanılabilir.")
    exclude = {e.lower().lstrip(".") for e in (args.exclude or ["docx"])}
    for key in keys:
        c = COURSES[key]
        sync_course(key, args.src or c["src"], args.dest or c["dest"], c["private"], exclude,
                    args.keep_pptx, not args.no_backlink)


if __name__ == "__main__":
    main()
