import sys, math, random
import numpy as np
sys.path.insert(0, '/home/claude/modular-worlds/art')
from wc import Painting, jag, ROBOTO, MARKER

W, H = 1600, 800
OUT = '/home/claude/modular-worlds/book/art/'


def palm(p, x, y, h, lean=0.0, seed=0, colors=('#1d6fa5', '#2f8f6f', '#0c5f73')):
    random.seed(seed)
    top = (x + lean * h, y - h)
    trunk = [(x + lean * h * t * t, y - h * t) for t in np.linspace(0, 1, 12)]
    p.wash(p.stroke_mask(trunk, 16, 8), '#3a2a2a', 0.85, wobble=1.5, edge=0.4, rough=0.25)
    for k in range(9):
        a = -math.pi / 2 + (k - 4) * 0.42 + random.uniform(-0.15, 0.15)
        L = h * random.uniform(0.35, 0.55)
        pts = []
        for t in np.linspace(0, 1, 10):
            ang = a + 0.9 * t * t * (1 if math.cos(a) > 0 else -1)
            pts.append((top[0] + math.cos(ang) * L * t, top[1] + math.sin(ang) * L * t * 0.8 + 18 * t * t))
        p.wash(p.stroke_mask(pts, 14, 3), random.choice(colors), 0.85, wobble=1.2, edge=0.6, rough=0.3)


def stars(p, n, region, seed=3):
    random.seed(seed)
    x0, y0, x1, y1 = region
    for _ in range(n):
        x, y = random.uniform(x0, x1), random.uniform(y0, y1)
        r = random.uniform(1.5, 4.5)
        p.lift(p.ellipse_mask(x, y, r, r), 0.95)
    for _ in range(n // 6):
        x, y = random.uniform(x0, x1), random.uniform(y0, y1); s = random.uniform(5, 9)
        p.ink([(x - s, y), (x + s, y)], 1.2, '#ffffff', 0.9, 0.3); p.ink([(x, y - s), (x, y + s)], 1.2, '#ffffff', 0.9, 0.3)


def sky_bands(p, y0, y1, colors, reserve=None, n=9, gap=6, strength=0.8, seed=0):
    """A sky made of real-looking horizontal brushstrokes: tapered rounded ends, wavy edges,
    pigment pooling along the bottom edge, white paper between and inside strokes."""
    rnd = random.Random(seed)
    rows = int(n * 1.6)
    ys = np.linspace(y0 - 6, y1 + 4, rows + 1)
    for i in range(rows):
        yc = (ys[i] + ys[i + 1]) / 2; thick = (ys[i + 1] - ys[i]) * rnd.uniform(0.8, 1.25) - rnd.uniform(0, gap)
        x = rnd.uniform(-120, 60)
        while x < W + 40:
            L = rnd.uniform(0.35, 1.0) * W
            col = rnd.choice(colors); mixc = rnd.choice(colors)
            k = 26; pts = []
            ph = rnd.uniform(0, 6.3); amp = rnd.uniform(2, 7); tilt = rnd.uniform(-10, 10)
            top, bot = [], []
            for j in range(k + 1):
                u = j / k; xx = x + L * u
                taper = min(1, u / 0.06, (1 - u) / 0.1) ** 0.6
                wv = math.sin(u * 9 + ph) * amp + math.sin(u * 23 + ph * 2) * amp * 0.4 + tilt * (u - 0.5)
                th = thick * (0.75 + 0.25 * math.sin(u * 5 + ph)) * max(0.05, taper)
                top.append((xx, yc + wv - th / 2)); bot.append((xx, yc + wv + th / 2 + rnd.uniform(-1.5, 1.5)))
            m = p.poly_mask(top + bot[::-1])
            p.wash(m, col, strength * rnd.uniform(0.65, 1.05), wobble=2.2, edge=0.55, rough=0.5, streak=(240, 14), var=0.6,
                   reserve=reserve, halo=5, mix=mixc if rnd.random() < 0.5 else None, pool=0.9, tooth=0.45, gran=0.35)
            x += L + rnd.uniform(-60, 40)


def fill_strokes(p, region, colors, y0, y1, thick=40, overlap=0.25, strength=0.7, seed=0, angle=0.0, reserve=None, bloom=0, amp=4):
    """Fill a region with overlapping brushstrokes (visible strokes, darker overlaps), clipped to the region."""
    rnd = random.Random(seed)
    y = y0 - thick * 0.3
    while y < y1 + thick * 0.3:
        th = thick * rnd.uniform(0.8, 1.3)
        x = rnd.uniform(-200, 0)
        while x < W + 60:
            L = rnd.uniform(0.3, 0.8) * W; ph = rnd.uniform(0, 6.3)
            top, bot = [], []
            for j in range(21):
                u = j / 20; xx = x + L * u
                taper = min(1, u / 0.05, (1 - u) / 0.08) ** 0.5
                yy = y + math.sin(u * 7 + ph) * amp + angle * (xx - W / 2)
                hh = th * max(0.1, taper) * (0.8 + 0.2 * math.sin(u * 4 + ph))
                top.append((xx, yy - hh / 2)); bot.append((xx, yy + hh / 2))
            m = p.poly_mask(top + bot[::-1]) * region
            if m.max() > 0:
                p.wash(m, rnd.choice(colors), strength * rnd.uniform(0.6, 1.0), wobble=2, edge=0.5, rough=0.45, var=0.5,
                       streak=(200, 20), mix=rnd.choice(colors) if rnd.random() < 0.4 else None, reserve=reserve, halo=4,
                       pool=0.7, tooth=0.4, gran=0.45, bloom=bloom if rnd.random() < 0.3 else 0)
            x += L - rnd.uniform(0, 80)
        y += th * (1 - overlap)


def balance_reserve(p):
    r = p.stroke_mask([(560, 700), (560, 325)], 24) + p.stroke_mask([(900, 700), (900, 325)], 24) + p.stroke_mask([(530, 328), (930, 328)], 24)
    r += p.stroke_mask([(608, 385), (852, 385)], 16)
    for cx in (620, 840):
        r += p.poly_mask([(cx - 66, 518), (cx + 66, 518), (cx + 48, 549), (cx - 48, 549)])
    r += p.rect_mask(565, 483, 675, 521) + p.rect_mask(790, 476, 895, 521)
    return np.clip(r, 0, 1)


def ch3():
    p = Painting(W, H, seed=33)
    moon = p.ellipse_mask(300, 150, 54, 54)
    bal = balance_reserve(p)
    palms = p.stroke_mask([(120, 640), (80, 340)], 30) + p.stroke_mask([(230, 650), (255, 430)], 26)
    arch = [(1210, 615), (1210, 500), (1240, 450), (1300, 435), (1360, 450), (1390, 500), (1390, 615)]
    archm = p.poly_mask(arch)
    cliffm = p.poly_mask([(980, 800), (1010, 520), (1080, 400), (1150, 300), (1260, 232), (1370, 192), (1480, 212), (1610, 172), (1610, 800)])
    res = np.clip(moon + bal + archm + cliffm, 0, 1)
    # sky in streaky bands
    sky_bands(p, 0, 476, ['#24308f', '#3b2f8f', '#1f3fa0', '#5a3d9a', '#2a3a96', '#1b2a7a'], reserve=res, n=8, gap=2, strength=0.85, seed=2)
    stars(p, 120, (20, 20, 980, 380))
    p.wash(moon, '#f3df8a', 0.45, wobble=2, edge=0.7)
    p.ink([(300 + 54 * math.cos(t), 150 + 54 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 40)], 1.6, '#3a3420', 0.6)
    # sea
    sea = p.poly_mask([(-10, 478), (1010, 470), (1030, 605), (-10, 612)])
    fill_strokes(p, sea, ['#1f5fb8', '#2b6fc8', '#1a4fa0', '#2b8fc0'], 470, 612, thick=26, overlap=0.15, strength=0.8, seed=4, reserve=res)
    random.seed(5)
    for y in (500, 522, 548, 575, 598):
        xs = random.uniform(0, 300)
        p.lift(p.stroke_mask([(xs, y), (xs + random.uniform(250, 650), y + random.uniform(-3, 3))], 4, 2), 0.9)
    # cliff
    cliff = [(980, 800), (1010, 520), (1080, 400), (1150, 300), (1260, 232), (1370, 192), (1480, 212), (1610, 172), (1610, 800)]
    p.wash(p.poly_mask(cliff), '#6a5a84', 0.55, wobble=4, edge=0.8, seed=5, reserve=archm, mix='#4a5a7a', bloom=2)
    fill_strokes(p, p.poly_mask(cliff), ['#5b4a74', '#3a3048', '#4a3f62'], 180, 800, thick=70, overlap=0.1, strength=0.45, seed=6, angle=-0.35, reserve=archm, amp=10)
    for k in range(6):
        x = 1050 + k * 90
        p.ink([(x, 330 + k * 8 - 40), (x + 30, 420), (x + 10, 520)], 1.3, '#2a2236', 0.5, 2)
    # forge mouth
    p.wash(archm, '#ffcf5a', 0.6, wobble=1.5, edge=0.9)
    inner = p.poly_mask([(1232, 615), (1232, 515), (1262, 472), (1300, 462), (1338, 472), (1368, 515), (1368, 615)])
    p.wash(inner, '#ff7a1a', 0.6, wobble=4, edge=1.0, var=0.7)
    p.wash(p.poly_mask([(1250, 615), (1270, 560), (1300, 520), (1330, 560), (1350, 615)]), '#c8301a', 0.5, wobble=4, edge=1.0)
    p.lift(p.ellipse_mask(1300, 585, 34, 22), 0.55); p.wash(p.ellipse_mask(1300, 585, 34, 22), '#ffe9a0', 0.4, wobble=3)
    glow = np.clip(gaussian(archm, 45) * 2.2 - archm, 0, 1)
    p.lift(glow, 0.55); p.wash(glow, '#ffb04a', 0.5, wobble=0, edge=0, tooth=0, pool=0)
    p.ink(arch, 2.6, '#1d1010', 0.85)
    for x in (1250, 1300, 1350):
        p.ink([(x, 615), (x + 6, 600)], 1.2, '#3a1a10', 0.6)
    random.seed(9)
    for _ in range(70):
        a = random.uniform(-2.5, -0.6); r = random.uniform(40, 240)
        x, y = 1300 + math.cos(a) * r, 440 + math.sin(a) * r * 1.05; s = random.uniform(2, 4.5)
        mk = p.ellipse_mask(x, y, s, s); p.lift(mk, 1.0); p.wash(mk, random.choice(['#ffb000', '#ff7a1a', '#ffd84a']), 0.85, wobble=0.6, edge=0.3, rough=0.1)
    # beach
    beach = p.poly_mask([(-10, 605), (1040, 596), (1610, 640), (1610, 810), (-10, 810)])
    p.wash(beach, '#3a3440', 0.55, wobble=3, seed=7, reserve=np.clip(bal + cliffm, 0, 1), mix='#2a2a38', gran=0.6, bloom=2)
    fill_strokes(p, beach, ['#3a3440', '#2a2630', '#4a4050', '#24202a'], 600, 810, thick=60, overlap=0.5, strength=0.4, seed=7, reserve=np.clip(bal + cliffm, 0, 1), amp=9)
    p.splatter(160, '#15131a', (0, 620, 1000, 800), 1, 3, 0.5)
    sp = gaussian(p.poly_mask([(1150, 615), (1450, 615), (1610, 800), (1000, 800)]), 30)
    p.lift(sp, 0.35); p.wash(sp, '#f0a050', 0.35, wobble=0, edge=0, tooth=0, pool=0)
    random.seed(11)
    for y in (650, 700, 750):
        x = random.uniform(0, 300); p.lift(p.stroke_mask([(x, y), (x + random.uniform(300, 600), y + 6)], 2.5, 1), 0.35)
    # the balance, painted on reserved paper
    wood = '#9a6230'
    for x in (560, 900):
        p.wash(p.stroke_mask([(x, 690), (x, 330)], 15, 12), wood, 0.85, wobble=1.5, edge=0.6)
        p.ink([(x - 8, 690), (x - 6, 332)], 1.8, '#2a1a10', 0.85); p.ink([(x + 8, 690), (x + 6, 332)], 1.8, '#2a1a10', 0.85)
    p.wash(p.stroke_mask([(540, 328), (920, 328)], 16), wood, 0.85, wobble=1.5, edge=0.6)
    p.ink([(538, 320), (922, 320)], 1.9, '#2a1a10', 0.85); p.ink([(538, 337), (922, 337)], 1.6, '#2a1a10', 0.7)
    p.ink([(730, 338), (730, 380)], 2.2, '#4a4a4a', 0.9, 0.3)
    p.wash(p.stroke_mask([(612, 385), (848, 385)], 10), '#d9a54a', 0.9, wobble=1, edge=0.6)
    p.ink([(612, 380), (848, 380)], 1.4, '#3a2510', 0.8)
    p.wash(p.ellipse_mask(730, 385, 12, 12), '#e2b23a', 0.9, wobble=1); p.ink([(730 + 12 * math.cos(t), 385 + 12 * math.sin(t)) for t in np.linspace(0, 6.3, 20)], 1.3, '#3a2510', 0.8)
    for cx in (620, 840):
        for dx in (-44, 0, 44):
            p.ink([(cx, 390), (cx + dx * 1.2, 520)], 1.3, '#5a5040', 0.85, 0.5)
        pan = [(cx - 64, 520), (cx + 64, 520), (cx + 46, 547), (cx - 46, 547)]
        p.wash(p.poly_mask(pan), '#d48a2a', 0.9, wobble=1.2, edge=0.8)
        p.ink(pan, 2.0, '#3a2510', 0.85, closed=True)
    for x in (583, 620, 657):
        r = [(x - 16, 485), (x + 16, 485), (x + 16, 519), (x - 16, 519)]
        p.wash(p.poly_mask(r), '#e8452a', 0.88, wobble=1.2, edge=0.8); p.ink(r, 1.4, '#5a1a10', 0.8, closed=True)
        p.text((x, 503), 'O', 22, ROBOTO + 'Roboto-Bold.ttf', '#fff6e8', 0.95)
    for x in (810, 850):
        r = [(x - 18, 478), (x + 18, 478), (x + 18, 519), (x - 18, 519)]
        p.wash(p.poly_mask(r), '#2a6fd0', 0.88, wobble=1.2, edge=0.8); p.ink(r, 1.4, '#0f2a5a', 0.8, closed=True)
        p.text((x, 499), 'N', 22, ROBOTO + 'Roboto-Bold.ttf', '#f0f6ff', 0.95)
    p.wash(p.ellipse_mask(883, 509, 10, 10), '#f2c230', 0.95, wobble=1, edge=0.8)
    palm(p, 120, 640, 300, -0.15, seed=4); palm(p, 232, 650, 220, 0.12, seed=7)
    p.border(16)
    return p.save(OUT + 'ch3.jpg')


def gaussian(m, s):
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(m, s)




# ---------------- shared props ----------------
RB = ROBOTO + 'Roboto-Bold.ttf'


def quad(p, pts, color, strength=0.85, outline=True, ink='#1d2433', lw=1.8, wobble=1.2, edge=0.7):
    p.wash(p.poly_mask(pts), color, strength, wobble=wobble, edge=edge, rough=0.3)
    if outline:
        p.ink(pts, lw, ink, 0.8, closed=True)


def house(p, x, y, w, h, color, roof='#c8401a', seed=0):
    random.seed(seed)
    body = [(x, y), (x + w, y), (x + w, y - h), (x, y - h)]
    quad(p, body, color, 0.8)
    rf = [(x - 6, y - h), (x + w + 6, y - h), (x + w / 2, y - h - h * 0.45)]
    quad(p, rf, roof, 0.85)
    for k in range(2):
        wx = x + w * (0.22 + 0.4 * k)
        win = [(wx, y - h * 0.62), (wx + w * 0.18, y - h * 0.62), (wx + w * 0.18, y - h * 0.38), (wx, y - h * 0.38)]
        quad(p, win, '#2b4fa8', 0.7, lw=1.2)
    d = [(x + w * 0.42, y), (x + w * 0.58, y), (x + w * 0.58, y - h * 0.3), (x + w * 0.42, y - h * 0.3)]
    quad(p, d, '#5a3a24', 0.8, lw=1.2)


def rings(p, items, size=44):
    """Molecule badges in the style of the M6 atom cards: coloured rings with a letter."""
    cols = {'H': '#f0b9b0', 'O': '#e8452a', 'N': '#2a5fc0', 'C': '#3fb08a'}
    for (x, y, el) in items:
        p.wash(p.ellipse_mask(x, y, size, size), cols[el], 0.85, wobble=2, edge=0.9)
        p.lift(p.ellipse_mask(x, y, size * 0.55, size * 0.55), 0.95)
        p.ink([(x + size * math.cos(t), y + size * math.sin(t)) for t in np.linspace(0, 6.3, 36)], 1.4, '#2a2a3a', 0.6)
        p.text((x, y + 1), el, int(size * 0.7), RB, '#1d2433', 0.9)


def boat(p, x, y, L, hull='#7a3b1a', sail='#f6f1e7', flag=None, seed=0):
    h = [(x - L / 2, y - L * 0.12), (x + L / 2, y - L * 0.12), (x + L * 0.38, y + L * 0.06), (x - L * 0.4, y + L * 0.06)]
    quad(p, h, hull, 0.9)
    p.ink([(x, y - L * 0.12), (x, y - L * 0.9)], 2.2, '#2a1a10', 0.9)
    sl = [(x + 4, y - L * 0.85), (x + 4, y - L * 0.18), (x + L * 0.38, y - L * 0.2)]
    p.wash(p.poly_mask(sl), sail, 0.25, wobble=1.5, edge=0.9); p.ink(sl, 1.4, '#2a2a3a', 0.7, closed=True)
    if flag:
        f = [(x, y - L * 0.9), (x - L * 0.2, y - L * 0.84), (x, y - L * 0.78)]
        quad(p, f, flag, 0.95, lw=1.0)


def reeds(p, x0, x1, y, n, color='#5a7a2a', h=40, seed=0):
    random.seed(seed)
    for _ in range(n):
        x = random.uniform(x0, x1); hh = h * random.uniform(0.6, 1.3); lean = random.uniform(-8, 8)
        p.ink([(x, y), (x + lean * 0.5, y - hh * 0.5), (x + lean, y - hh)], random.uniform(1.0, 2.0), color, 0.75, 0.6)


def papel_picado(p, x0, y0, x1, y1, n=12, seed=0):
    random.seed(seed)
    cols = ['#e63946', '#ffbe0b', '#3a86ff', '#8338ec', '#06d6a0', '#ff006e', '#fb5607']
    pts = [(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + 30 * math.sin(t * math.pi)) for t in np.linspace(0, 1, 30)]
    p.ink(pts, 1.4, '#3a3a3a', 0.8, 0.3)
    for k in range(n):
        t = (k + 0.5) / n; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t + 30 * math.sin(t * math.pi)
        w = (x1 - x0) / n * 0.8
        fl = [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + w * 0.9), (x + w / 4, y + w * 1.05), (x, y + w * 0.9), (x - w / 4, y + w * 1.05), (x - w / 2, y + w * 0.9)]
        p.wash(p.poly_mask(fl), cols[k % len(cols)], 0.8, wobble=1, edge=0.8)
        p.lift(p.ellipse_mask(x, y + w * 0.45, w * 0.14, w * 0.14), 0.95)


# ---------------- Chapter 0: the Entrance Exam ----------------
def ch0():
    p = Painting(W, H, seed=10)
    VP = (1300, 360)
    wall_top = lambda x: 110 + (VP[1] - 110 - 40) * (x / VP[0])
    wall_bot = lambda x: 660 + (VP[1] + 90 - 660) * (x / VP[0])
    wallm = p.poly_mask([(0, wall_top(0)), (1260, wall_top(1260)), (1260, wall_bot(1260)), (0, wall_bot(0))])
    floorm = p.poly_mask([(560, 800), (1610, 800), (1610, 520), (1080, 500)])
    sky_bands(p, 0, 470, ['#f2a541', '#e9875f', '#c26aa0', '#8e5aa8', '#f4c06a'], reserve=np.clip(wallm, 0, 1), n=9, gap=10, strength=0.7, seed=3)
    # distant sea and hills
    p.wash(p.poly_mask(jag(1150, 1610, 430, 10, 8) + [(1610, 505), (1150, 505)]), '#7a6aa8', 0.55, wobble=3, reserve=wallm)
    p.wash(p.poly_mask([(1150, 470), (1610, 462), (1610, 515), (1150, 515)]), '#3a6fc0', 0.7, wobble=3, streak=(300, 10), reserve=wallm)
    # the wall of doors
    p.wash(wallm, '#e7b97a', 0.6, wobble=3, edge=0.7)
    p.wash(p.poly_mask([(0, wall_top(0)), (1260, wall_top(1260)), (1260, wall_top(1260) + 14), (0, wall_top(0) + 40)]), '#c4573a', 0.8, wobble=2)
    p.wash(p.poly_mask([(0, wall_bot(0) - 40), (1260, wall_bot(1260) - 8), (1260, wall_bot(1260)), (0, wall_bot(0))]), '#9a6a4a', 0.5, wobble=2)
    p.ink([(0, wall_top(0)), (1260, wall_top(1260))], 2.2); p.ink([(0, wall_bot(0)), (1260, wall_bot(1260))], 2.0)
    cols = ['#0c8f8f', '#e8452a', '#f2b134', '#2a5fc0', '#8338ec', '#2f8f4f']
    xs = [0]
    while xs[-1] < 1230:
        x = xs[-1]; step = 150 * (1 - x / 1450) ** 1.25 + 8
        xs.append(x + step)
    for i in range(len(xs) - 1):
        a, b = xs[i] + (xs[i + 1] - xs[i]) * 0.18, xs[i + 1] - (xs[i + 1] - xs[i]) * 0.18
        if b > 1250: break
        ta, tb = wall_top(a), wall_top(b); ba, bb = wall_bot(a), wall_bot(b)
        ha, hb = (ba - ta), (bb - tb)
        ya, yb = ba - ha * 0.55, bb - hb * 0.55
        arc = [((a + b) / 2 + (b - a) / 2 * math.cos(t), (ya + yb) / 2 - (b - a) * 0.45 * math.sin(t)) for t in np.linspace(0, math.pi, 12)]
        d = [(a, ba), (b, bb)] + arc + [(a, ba)]
        n = i + 1
        opened = n in (1, 4, 9)
        quad(p, d, '#140f18' if opened else cols[i % len(cols)], 0.85 if not opened else 0.97, lw=max(1.0, 2.0 * (1 - a / 1400)))
        if opened:
            p.light(gaussian(p.poly_mask(d), 6) * 0.5, '#ffb03a', 0.5)
            leaf = [(a, ba), (a + (b - a) * 0.3, ba + 4), (a + (b - a) * 0.3, ya - (b - a) * 0.2), (a, ya)]
            quad(p, leaf, cols[i % len(cols)], 0.9, lw=1.2)
        sz = max(10, int(38 * (1 - a / 1350)))
        topy = (ya + yb) / 2 - (b - a) * 0.45
        p.text(((a + b) / 2, topy - sz * 0.75), str(n), sz, MARKER, '#1d2433', 0.85)
    p.text((1268, wall_bot(1268) - 50), '… 100', 18, MARKER, '#1d2433', 0.7, anchor='lm')
    # broken floor: 8x8 checkerboard in perspective, two opposite corners missing
    def fp(u, v):  # u across, v depth (0 near, 1 far)
        xl = 560 + (1080 - 560) * v; xr = 1610 + (1610 - 1610) * v; y = 800 + (505 - 800) * v
        return (xl + (xr - xl) * u, y)
    for i in range(8):
        for j in range(8):
            if (i, j) in ((0, 0), (7, 7)):
                continue
            v0, v1 = (j / 8) ** 0.85, ((j + 1) / 8) ** 0.85
            q = [fp(i / 8, v0), fp((i + 1) / 8, v0), fp((i + 1) / 8, v1), fp(i / 8, v1)]
            quad(p, q, '#f4ead2' if (i + j) % 2 else '#c4573a', 0.75, lw=1.0, ink='#5a3a2a', wobble=0.8)
    for (i, j) in ((0, 0), (7, 7)):
        v0, v1 = (j / 8) ** 0.85, ((j + 1) / 8) ** 0.85
        q = [fp(i / 8, v0), fp((i + 1) / 8, v0), fp((i + 1) / 8, v1), fp(i / 8, v1)]
        quad(p, q, '#2a2028', 0.85, lw=1.6)
        cx, cy = np.mean([a for a, _ in q]), np.mean([b for _, b in q])
        for k in range(4):
            ang = random.uniform(0, 6.3); p.ink([(cx, cy), (cx + math.cos(ang) * 40, cy + math.sin(ang) * 14)], 1.0, '#2a2028', 0.6)
    # plaza ground left of floor
    p.wash(p.poly_mask([(0, wall_bot(0) - 2), (1260, wall_bot(1260)), (1080, 500), (560, 800), (0, 800)]), '#d9b07a', 0.55, wobble=3, reserve=floorm)
    p.text((470, 205), 'HALL OF A HUNDRED DOORS', 46, MARKER, '#5a2a1a', 0.85, angle=-8.5)
    papel_picado(p, 640, 60, 1580, 120, n=11, seed=2)
    palm(p, 1520, 505, 190, 0.1, seed=12)
    p.border(16)
    return p.save(OUT + 'ch0.jpg')




def rain(p, n, region, seed=0, color='#cfe0ff'):
    random.seed(seed)
    x0, y0, x1, y1 = region
    for _ in range(n):
        x, y = random.uniform(x0, x1), random.uniform(y0, y1); L = random.uniform(18, 40)
        p.ink([(x, y), (x - L * 0.25, y + L)], random.uniform(0.8, 1.5), color, 0.55, 0.1)


# ---------------- Chapter 1: Mojadito, home port ----------------
def ch1():
    p = Painting(W, H, seed=11)
    lh = p.poly_mask([(1330, 470), (1390, 470), (1378, 230), (1342, 230)])
    shipm = p.poly_mask([(560, 600), (900, 600), (880, 640), (580, 640)]) + p.poly_mask([(700, 600), (705, 300), (830, 590)])
    sign = p.rect_mask(90, 520, 470, 640)
    res = np.clip(lh + shipm + sign, 0, 1)
    sky_bands(p, 0, 420, ['#6d7fb3', '#8a86b8', '#5a6fa8', '#9aa6c8', '#7a6aa8'], reserve=res, n=9, gap=8, strength=0.65, seed=5)
    # hills with houses
    random.seed(4)
    cols = ['#f2b134', '#e8452a', '#f4ead2', '#4fb3c8', '#e17aa8', '#f28c28', '#8fc95a']
    spots = [(60, 470), (150, 455), (250, 470), (345, 440), (440, 462), (520, 430), (610, 455), (700, 425), (790, 450), (880, 420), (960, 445), (1050, 430), (130, 400), (300, 385), (480, 380), (660, 370), (850, 365), (1010, 380)]
    hs = [(x, y, random.uniform(55, 80), random.uniform(40, 60)) for x, y in spots]
    hres = sum(p.poly_mask([(x - 8, y + 2), (x + w + 8, y + 2), (x + w + 8, y - h), (x + w / 2, y - h - h * 0.5), (x - 8, y - h)]) for x, y, w, h in hs)
    hres = np.clip(hres, 0, 1)
    hill = jag(-10, 1250, 300, 45, 6) + [(1250, 520), (-10, 520)]
    p.wash(p.poly_mask(hill), '#3f8f6f', 0.65, wobble=5, edge=0.8, reserve=np.clip(res + hres, 0, 1), halo=3)
    p.wash(p.poly_mask(jag(880, 1610, 360, 30, 5) + [(1610, 520), (880, 520)]), '#2f7a5f', 0.6, wobble=5, reserve=np.clip(res + hres, 0, 1), halo=3)
    for k, (x, y, w, h) in enumerate(hs):
        house(p, x, y, w, h, cols[k % len(cols)], random.choice(['#c8401a', '#7a3b1a', '#2b4fa8']), seed=k)
    # lighthouse
    quad(p, [(1330, 470), (1390, 470), (1378, 230), (1342, 230)], '#f6f1e7', 0.2)
    for yb in (290, 350, 410):
        quad(p, [(1336 - (yb - 230) * 0.04, yb), (1384 + (yb - 230) * 0.04, yb), (1386 + (yb - 230) * 0.04, yb + 25), (1334 - (yb - 230) * 0.04, yb + 25)], '#e8452a', 0.85, lw=1.0)
    quad(p, [(1335, 230), (1385, 230), (1380, 200), (1340, 200)], '#2a2a3a', 0.8)
    p.light(p.ellipse_mask(1360, 214, 14, 10), '#ffd25a', 1.0)
    p.lift(gaussian(p.poly_mask([(1360, 214), (1020, 120), (1030, 250)]), 10), 0.5); p.wash(gaussian(p.poly_mask([(1360, 214), (1020, 120), (1030, 250)]), 10), '#ffe9a0', 0.35, wobble=0, edge=0)
    # sea
    sea = p.poly_mask([(-10, 520), (1610, 515), (1610, 810), (-10, 810)])
    p.wash(sea, '#2b6fb8', 0.75, wobble=3, streak=(420, 14), var=0.6, reserve=np.clip(shipm + sign, 0, 1))
    p.wash(p.poly_mask([(-10, 640), (1610, 630), (1610, 810), (-10, 810)]), '#1f4f9a', 0.45, wobble=4, streak=(420, 12), reserve=sign)
    random.seed(8)
    for _ in range(40):
        x, y = random.uniform(0, 1600), random.uniform(560, 790); r = random.uniform(6, 16)
        p.ink([(x + r * math.cos(t), y + 0.35 * r * math.sin(t)) for t in np.linspace(0, 6.3, 16)], 1.0, '#d8e8ff', 0.6, 0.3)
    # pier and ship
    for x in range(520, 1000, 60):
        p.wash(p.stroke_mask([(x, 610), (x, 700)], 10), '#5a3a24', 0.85, wobble=1)
    quad(p, [(500, 600), (1000, 600), (1000, 615), (500, 615)], '#9a6230', 0.9)
    boat(p, 730, 600, 300, hull='#7a3b1a', sail='#f6f1e7', flag='#0c5f73')
    for k, x in enumerate((540, 575, 960)):
        fl = [(x - 9, 600), (x + 9, 600), (x + 9, 585), (x + 4, 578), (x + 4, 568), (x - 4, 568), (x - 4, 578), (x - 9, 585)]
        quad(p, fl, '#c87533', 0.9, lw=1.0)
    # harbor sign with a water molecule
    quad(p, [(90, 520), (470, 520), (470, 640), (90, 640)], '#9a6230', 0.75)
    p.wash(p.stroke_mask([(150, 640), (150, 760)], 12), '#5a3a24', 0.9, wobble=1); p.wash(p.stroke_mask([(410, 640), (410, 760)], 12), '#5a3a24', 0.9, wobble=1)
    p.text((280, 560), 'MOJADITO', 54, MARKER, '#fff6e0', 0.95)
    rings(p, [(235, 612, 'H'), (280, 600, 'O'), (325, 612, 'H')], size=20)
    rain(p, 260, (0, 0, 1600, 800), seed=3)
    palm(p, 1180, 520, 230, -0.1, seed=21); palm(p, 1500, 540, 260, 0.12, seed=22)
    p.border(16)
    return p.save(OUT + 'ch1.jpg')


# ---------------- Chapter 2: Ammonia Bay ----------------
def ch2():
    p = Painting(W, H, seed=12)
    c1 = [(-10, 300), (90, 262), (180, 250), (300, 214), (420, 236), (470, 246), (560, 268), (680, 330), (760, 430), (760, 470), (-10, 470)]
    c2 = [(840, 470), (900, 390), (990, 320), (1090, 296), (1200, 270), (1320, 288), (1400, 286), (1500, 262), (1610, 280), (1610, 470)]
    cl = np.clip(p.poly_mask(c1) + p.poly_mask(c2), 0, 1)
    sky_bands(p, 0, 440, ['#d9e8a0', '#bfe3c8', '#f2e6a0', '#a8d8c8', '#e8eab0'], n=8, gap=10, strength=0.55, seed=7, reserve=cl)
    p.wash(p.poly_mask(c1), '#d4a86a', 0.7, wobble=4, edge=0.9)
    p.wash(p.poly_mask(c2), '#c4945a', 0.7, wobble=4, edge=0.9)
    random.seed(2)
    for k in range(9):
        y = 330 + k * 15; p.ink(jag(10, 740, y, 3, 8), 1.0, '#8a6a3a', 0.45, 1); p.ink(jag(880, 1590, y + 20, 3, 8), 1.0, '#7a5a2a', 0.45, 1)
    p.wash(p.poly_mask(jag(-10, 760, 420, 10, 6) + [(760, 470), (-10, 470)]), '#a07a4a', 0.45, wobble=3)
    random.seed(3)
    for (x, y) in ((180, 252), (470, 248), (1090, 298), (1400, 288)):
        p.wash(p.ellipse_mask(x, y + 4, 18, 7), '#4a3a2a', 0.85, wobble=1)
        for k in range(7):
            m = p.ellipse_mask(x + random.uniform(-14, 14) + k * 8, y - 18 - k * 30, 22 + k * 10, 16 + k * 6)
            p.lift(gaussian(m, 7), 0.6)
    walk = p.poly_mask([(260, 810), (560, 810), (1180, 470), (1110, 470)])
    bay = p.poly_mask([(-10, 470), (1610, 465), (1610, 810), (-10, 810)])
    p.wash(bay, '#3fb0a8', 0.7, wobble=3, streak=(400, 12), var=0.6, reserve=walk)
    p.wash(p.poly_mask([(-10, 620), (1610, 610), (1610, 810), (-10, 810)]), '#1f8f9a', 0.4, wobble=4, streak=(400, 12), reserve=walk)
    random.seed(5)
    for y in range(495, 800, 26):
        x = random.uniform(600, 1500); p.lift(p.stroke_mask([(x, y), (x + random.uniform(100, 300), y + 2)], 2.5, 1.5), 0.6)
    quad(p, [(260, 810), (560, 810), (1180, 470), (1110, 470)], '#b07a46', 0.75, lw=1.6)
    for k in range(1, 16):
        t = k / 16; xl = 260 + (1110 - 260) * t; xr = 560 + (1180 - 560) * t; y = 810 + (470 - 810) * t
        p.ink([(xl, y), (xr, y)], 1.0, '#5a3a24', 0.5)
    nums = list(range(13, 26))
    for idx, n in enumerate(nums):
        t = idx / (len(nums) - 1); sc = 1 - 0.62 * t
        x = 250 + (1100 - 250) * t - 10 * (1 - t); y = 808 + (472 - 808) * t
        h = 150 * sc; w = 12 * sc + 2
        p.wash(p.stroke_mask([(x, y), (x, y - h)], w), '#6a4228', 0.9, wobble=0.8)
        pl = [(x - 18 * sc - 6, y - h * 0.5 - 13 * sc - 4), (x + 18 * sc + 6, y - h * 0.5 - 13 * sc - 4), (x + 18 * sc + 6, y - h * 0.5 + 13 * sc + 4), (x - 18 * sc - 6, y - h * 0.5 + 13 * sc + 4)]
        p.lift(p.poly_mask(pl), 0.9); p.ink(pl, 1.0, '#3a2a1a', 0.7, closed=True)
        p.text((x, y - h * 0.5), str(n), max(13, int(30 * sc)), RB, '#1d2433', 0.95)
        water, amm = (n - 13) % 4 == 0, (n - 13) % 6 == 0
        r = 15 * sc + 3
        if water and amm:
            p.light(gaussian(p.ellipse_mask(x, y - h - r, r * 2.8, r * 2.6), 7), '#ffd25a', 0.95)
        if water:
            p.wash(p.ellipse_mask(x - (r if amm else 0), y - h - r, r, r), '#2a6fd0', 0.92, wobble=1, edge=0.8)
            p.ink([(x - (r if amm else 0) + r * math.cos(q), y - h - r + r * math.sin(q)) for q in np.linspace(0, 6.3, 18)], 1.0, '#0f2a5a', 0.7)
        if amm:
            p.wash(p.ellipse_mask(x + (r if water else 0), y - h - r, r, r), '#2fb04f', 0.92, wobble=1, edge=0.8)
            p.ink([(x + (r if water else 0) + r * math.cos(q), y - h - r + r * math.sin(q)) for q in np.linspace(0, 6.3, 18)], 1.0, '#0f3a1a', 0.7)
    rings(p, [(1330, 660, 'N'), (1265, 712, 'H'), (1395, 712, 'H'), (1330, 594, 'H')], size=28)
    p.text((1330, 755), 'AMMONIA BAY', 40, MARKER, '#1d2433', 0.85)
    p.border(16)
    return p.save(OUT + 'ch2.jpg')


# ---------------- Chapter 4: Diophantine Delta ----------------
def ch4():
    p = Painting(W, H, seed=14)
    sun = p.ellipse_mask(1150, 170, 60, 60)
    signm = p.rect_mask(70, 470, 560, 640)
    sky_bands(p, 0, 400, ['#f6d3b0', '#f2e6c8', '#c8dcef', '#e8c8c8', '#d8e4f0'], reserve=np.clip(sun, 0, 1), n=8, gap=12, strength=0.5, seed=9)
    p.wash(sun, '#f6d35a', 0.5, wobble=2, edge=0.8)
    # water, then reed islands that leave winding channels
    p.wash(p.poly_mask([(-10, 380), (1610, 376), (1610, 810), (-10, 810)]), '#8fb4d0', 0.6, wobble=3, streak=(420, 10), reserve=signm)
    p.wash(p.poly_mask([(-10, 560), (1610, 556), (1610, 810), (-10, 810)]), '#5f8fb8', 0.35, wobble=3, streak=(420, 10), reserve=signm)
    random.seed(6)
    rows = [(400, 0.3), (450, 0.5), (520, 0.75), (620, 1.05), (740, 1.4)]
    for j, (yc, sc) in enumerate(rows):
        x = random.uniform(-200, 50)
        while x < 1650:
            w = random.uniform(380, 900) * sc; hh = random.uniform(14, 30) * sc * 1.6
            pts = [(x + w / 2 + w / 2 * math.cos(t) * (1 + 0.15 * math.sin(3 * t + j)), yc + hh * math.sin(t) * (0.6 if math.sin(t) < 0 else 1)) for t in np.linspace(0, 2 * math.pi, 24)]
            p.wash(p.poly_mask(pts), random.choice(['#7a9a3a', '#6f8f3a', '#8aa848']), 0.75, wobble=2.5, edge=0.8, reserve=signm)
            p.wash(p.poly_mask([(px, py) for px, py in pts if py >= yc]), '#4a6a2a', 0.35, wobble=2)
            reeds(p, x + w * 0.1, x + w * 0.9, yc, int(w / 12), '#3f5f22', 30 * sc + 6, seed=j * 10 + int(x))
            x += w + random.uniform(120, 420) * sc
    # fog
    for yy in (400, 470, 560):
        p.lift(gaussian(p.rect_mask(0, yy, 1600, yy + 30), 14), 0.45)
    # ferries with black flags
    boat(p, 820, 470, 110, hull='#5a3a24', flag='#14181b')
    boat(p, 1180, 430, 70, hull='#5a3a24', flag='#14181b')
    boat(p, 1360, 600, 170, hull='#7a3b1a', flag='#14181b')
    # dock and toll sign
    for x in (110, 520):
        p.lift(p.stroke_mask([(x, 640), (x, 800)], 18), 1.0); p.wash(p.stroke_mask([(x, 640), (x, 800)], 16), '#5a3a24', 0.9, wobble=1)
    p.lift(p.rect_mask(66, 466, 564, 644), 1.0)
    quad(p, [(70, 470), (560, 470), (560, 640), (70, 640)], '#f4ead2', 0.5)
    p.text((315, 510), 'FIVES AND SEVENS ONLY', 34, MARKER, '#1d2433', 0.9)
    p.text((315, 560), 'NO CHANGE', 48, MARKER, '#c8401a', 0.95)
    for (x, n) in ((200, '5'), (430, '7')):
        p.wash(p.ellipse_mask(x, 605, 22, 22), '#e0b154', 0.9, wobble=1, edge=0.9)
        p.ink([(x + 22 * math.cos(t), 605 + 22 * math.sin(t)) for t in np.linspace(0, 6.3, 24)], 1.4, '#6a4a10', 0.8)
        p.text((x, 606), n, 24, RB, '#5a3a10', 0.95)
    quad(p, [(-10, 690), (640, 680), (640, 710), (-10, 720)], '#9a6230', 0.85)
    p.border(16)
    return p.save(OUT + 'ch4.jpg')



# ---------------- The archipelago map ----------------
NAMES = ['The Entrance Exam', 'Mojadito', 'Ammonia Bay', "Euclid's Forge", 'Diophantine Delta', 'Prime Peaks', 'Clockwork Isles', 'The Calendar Isles', "Fermat's Lighthouse", 'Secret Tides', 'Return to Earth']


def blob(cx, cy, r, seed, n=40, sq=0.75):
    rnd = random.Random(seed); ph = [rnd.uniform(0, 6.3) for _ in range(4)]
    pts = []
    for t in np.linspace(0, 2 * math.pi, n, endpoint=False):
        rr = r * (1 + 0.16 * math.sin(2 * t + ph[0]) + 0.1 * math.sin(3 * t + ph[1]) + 0.06 * math.sin(5 * t + ph[2]))
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t) * sq))
    return pts


def archipelago(unlocked=5):
    MW_, MH_ = 1600, 1200
    global W, H
    W0, H0 = W, H; W, H = MW_, MH_
    p = Painting(MW_, MH_, seed=40)
    pts = [(210, 890), (450, 690), (290, 450), (580, 300), (800, 560), (1030, 330), (1270, 240), (1430, 470), (1190, 660), (960, 880), (1320, 960)]
    R = [88, 105, 88, 92, 100, 88, 82, 90, 80, 85, 95]
    isl = [blob(x, y, R[i], seed=i * 7 + 1) for i, (x, y) in enumerate(pts)]
    allm = np.clip(sum(p.poly_mask(b) for b in isl), 0, 1)
    sky_bands(p, 0, MH_, ['#3f8fc0', '#2b6fb8', '#4fa8c8', '#2f7fb0', '#5ab0c8'], reserve=allm, n=16, gap=8, strength=0.6, seed=12)
    random.seed(13)
    for _ in range(70):
        x, y = random.uniform(30, MW_ - 60), random.uniform(160, MH_ - 40)
        if allm[int(min(MH_ - 1, y)), int(min(MW_ - 1, x))] > 0: continue
        p.ink([(x, y), (x + 8, y - 5), (x + 16, y), (x + 24, y - 5)], 1.2, '#e8f4fb', 0.75, 0.3)
    # route
    for i in range(10):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 40
        for t in np.linspace(0.12, 0.88, 9):
            x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1; y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1
            m = p.ellipse_mask(x, y, 5, 5)
            if i < unlocked - 1: p.wash(m, '#fff6e0', 0.0); p.lift(m, 0.95)
            else: p.lift(m, 0.5)
    cols = ['#e7b97a', '#5aa86a', '#d4b06a', '#5b4a74', '#8aa848']
    for i, b in enumerate(isl):
        m = p.poly_mask(b); x, y = pts[i]
        if i < unlocked:
            p.wash(m, cols[i], 0.75, wobble=4, edge=0.9)
            p.wash(p.poly_mask(blob(x, y + 10, R[i] * 0.95, seed=i * 7 + 1)), '#000000', 0.0)
            p.ink(b + [b[0]], 1.8, '#3a2a1a', 0.7, closed=False)
            p.wash(np.clip(p.poly_mask(blob(x, y, R[i] * 1.15, seed=i * 7 + 1)) - m, 0, 1), '#e8f4fb', 0.0)
        else:
            p.wash(m, '#a89cc0', 0.5, wobble=5, edge=0.7)
            p.ink(b + [b[0]], 1.2, '#5b5470', 0.4)
    # landmarks on unlocked islands
    x, y = pts[0]
    for k in range(6):
        quad(p, [(x - 60 + k * 20, y + 10), (x - 46 + k * 20, y + 10), (x - 46 + k * 20, y - 18), (x - 60 + k * 20, y - 18)], ['#0c8f8f', '#e8452a', '#f2b134', '#2a5fc0', '#8338ec', '#2f8f4f'][k], 0.9, lw=1.0)
    x, y = pts[1]
    for k, (dx, dy) in enumerate([(-50, 0), (-15, -18), (20, 2), (50, -14)]):
        house(p, x + dx - 14, y + dy + 10, 28, 22, ['#f2b134', '#e8452a', '#4fb3c8', '#e17aa8'][k], '#c8401a', seed=k)
    rain(p, 30, (x - 90, y - 90, x + 90, y + 40), seed=2)
    x, y = pts[2]
    for k, dx in enumerate((-30, 25)):
        for j in range(4):
            p.lift(gaussian(p.ellipse_mask(x + dx + j * 4, y - 20 - j * 16, 12 + j * 5, 9 + j * 3), 4), 0.7)
    rings(p, [(x + 40, y + 30, 'N')], size=16)
    x, y = pts[3]
    p.wash(p.poly_mask([(x - 30, y + 30), (x - 30, y), (x, y - 20), (x + 30, y), (x + 30, y + 30)]), '#ff8a2a', 0.9, wobble=1.5, edge=0.9)
    random.seed(4)
    for _ in range(20):
        a = random.uniform(-2.6, -0.5); r = random.uniform(20, 70); mk = p.ellipse_mask(x + math.cos(a) * r, y - 10 + math.sin(a) * r, 2.5, 2.5); p.lift(mk, 1); p.wash(mk, '#ffb000', 0.9, wobble=0.5)
    x, y = pts[4]
    for k in range(3):
        p.wash(p.stroke_mask([(x - 90, y - 30 + k * 28), (x - 20, y - 20 + k * 30), (x + 40, y - 34 + k * 30), (x + 95, y - 22 + k * 28)], 7, 5), '#6fa8d8', 0.85, wobble=1)
    # fog over the locked lands
    for i in range(unlocked, 11):
        x, y = pts[i]
        p.lift(gaussian(p.ellipse_mask(x, y, R[i] * 1.5, R[i] * 1.0), 30), 0.28)
    # labels
    for i, (x, y) in enumerate(pts):
        ly = y + R[i] * 0.75 + 34
        fs = 32 if i < unlocked else 28
        p.lift(gaussian(p.rect_mask(x - len(NAMES[i]) * fs * 0.29, ly - fs * 0.62, x + len(NAMES[i]) * fs * 0.29, ly + fs * 0.62), 6), 0.85)
        p.text((x, ly), NAMES[i], fs, RB, '#1d2433' if i < unlocked else '#5b6168', 0.95 if i < unlocked else 0.7)
        cy = y - R[i] * 0.75 - 4
        p.lift(p.ellipse_mask(x, cy, 26, 26), 1.0)
        p.wash(p.ellipse_mask(x, cy, 26, 26), '#9a6b12' if i < unlocked else '#9a96a8', 0.9 if i < unlocked else 0.5, wobble=1.2, edge=0.8)
        p.text((x, cy + 1), str(i), 30, RB, '#ffffff', 0.95)
    # ship heading to the next land
    sx, sy = (pts[unlocked - 1][0] + pts[unlocked][0]) / 2, (pts[unlocked - 1][1] + pts[unlocked][1]) / 2 - 60
    boat(p, sx, sy, 110, hull='#7a3b1a', flag='#c8401a')
    # title and compass
    p.lift(gaussian(p.rect_mask(40, 40, 760, 122), 10), 0.92)
    p.text((60, 80), 'The Modular Archipelago', 64, MARKER, '#1d2433', 0.92, anchor='lm')
    cx, cy = MW_ - 130, 150
    for a, L, c in ((0, 80, '#c8401a'), (math.pi, 80, '#f6f1e7'), (math.pi / 2, 60, '#f6f1e7'), (-math.pi / 2, 60, '#f6f1e7')):
        tip = (cx + math.sin(a) * L, cy - math.cos(a) * L)
        side1 = (cx + math.cos(a) * 14, cy + math.sin(a) * 14); side2 = (cx - math.cos(a) * 14, cy - math.sin(a) * 14)
        quad(p, [tip, side1, side2], c, 0.85, lw=1.4)
    p.lift(gaussian(p.ellipse_mask(cx, cy - 98, 22, 22), 4), 0.9)
    p.text((cx, cy - 98), 'N', 30, MARKER, '#1d2433', 0.95)
    p.border(18)
    out = p.save(OUT + 'map.jpg')
    W, H = W0, H0
    return out



# ---------------- Chapter 5: Prime Peaks ----------------
def ridge(x0, x1, base, peaks, seed=0, rough=10):
    """Mountain silhouette: peaks = [(x, top_y)], returns polygon down to base."""
    rnd = random.Random(seed); pts = [(x0, base)]
    xs = sorted(set(np.linspace(x0, x1, 90).tolist() + [px for px, _ in peaks]))
    for x in xs:
        y = base
        for (px, py) in peaks:
            w = (base - py) * 0.62
            y = min(y, py + abs(x - px) * (base - py) / w + (0 if x == px else rnd.uniform(-rough, rough) * 0.5))
        pts.append((x, y))
    pts.append((x1, base)); return pts


def ch5():
    p = Painting(W, H, seed=55)
    sun = p.ellipse_mask(1112, 66, 40, 40)
    signm = p.rect_mask(120, 520, 560, 690)
    sky_bands(p, 0, 430, ['#f3d6b8', '#f6e8cc', '#d6e2f2', '#ecd2d8', '#cfdcf0'], reserve=np.clip(sun + signm, 0, 1), n=8, gap=12, strength=0.5, seed=15)
    p.wash(sun, '#f6d35a', 0.5, wobble=2, edge=0.8)
    # back range (pale), middle range with the six prime peaks, front hills
    back = ridge(-20, 1620, 470, [(80, 250), (330, 210), (600, 260), (900, 200), (1180, 240), (1480, 215)], seed=2, rough=14)
    fill_strokes(p, p.poly_mask(back), ['#b9c4de', '#c8c2dc', '#aab8d4'], 190, 470, thick=34, strength=0.5, seed=21, angle=-0.05, reserve=signm)
    PK = [(170, 150, '2'), (430, 120, '3'), (700, 95, '5'), (980, 135, '7'), (1250, 110, '11'), (1500, 160, '13')]
    mid = ridge(-20, 1620, 560, [(x, y) for x, y, _ in PK], seed=5, rough=12)
    midm = p.poly_mask(mid)
    snow = np.zeros_like(midm)
    for x, y, _ in PK:
        s = [(x - 34, y + 34), (x - 16, y + 26), (x - 2, y + 38), (x + 14, y + 25), (x + 34, y + 33)]
        snow += p.poly_mask([(x, y - 2)] + s)
    snow = np.clip(snow, 0, 1) * midm
    p.wash(midm, '#9aa6c8', 0.35, wobble=3, edge=0.7, reserve=np.clip(snow + signm, 0, 1), mix='#b8a8c8', pool=0.8)
    fill_strokes(p, midm, ['#7f8fb4', '#8d7fa8', '#7486a8', '#9aa0bc'], 90, 560, thick=46, strength=0.45, seed=31, angle=0.0, reserve=np.clip(snow + signm, 0, 1), bloom=0.3)
    p.wash(snow, '#c4d0e8', 0.45, wobble=1.5, edge=0.9)
    # shadow side of each peak
    for x, y, _ in PK:
        p.wash(p.poly_mask([(x, y + 4), (x + 230, 560), (x + 30, 560)]) * midm * (1 - snow), '#4a5482', 0.2, wobble=2.5, edge=0.4, pool=0.3)
    # pennants on the summits, each with its prime
    for x, y, n in PK:
        p.ink([(x, y + 14), (x, y - 46)], 2.2, '#3a2a2a', 0.9, 0.5)
        flag = [(x, y - 46), (x + 52, y - 36), (x, y - 24)]
        p.lift(p.poly_mask(flag), 1.0)
        p.wash(p.poly_mask(flag), '#c8401a' if n in ('2', '7', '13') else '#e0b154', 0.9, wobble=1, edge=0.8)
        p.text((x + 18, y - 36), n, 17 if len(n) > 1 else 19, RB, '#ffffff' if n in ('2', '7', '13') else '#1d2433', 0.97)
    # front hills and terraces (the sieve fields)
    front = [(-20, 560)] + [(x, 600 + 40 * math.sin(x / 260) + 20 * math.sin(x / 90)) for x in np.linspace(-20, 1620, 60)] + [(1620, 820), (-20, 820)]
    fm = p.poly_mask(front)
    fill_strokes(p, fm, ['#7a9a3a', '#8aa848', '#6f8f3a', '#9aa84a'], 560, 800, thick=30, strength=0.7, seed=41, angle=-0.02, reserve=signm)
    rnd = random.Random(8)
    for k in range(7):  # terrace lines
        y = 640 + k * 24
        p.ink([(x, y + 6 * math.sin(x / 70 + k)) for x in np.linspace(700 + k * 20, 1560, 30)], 1.4, '#4a6a2a', 0.55, 1.0)
    # a grid of sieve plots on the terraces: some crossed out, some left with a stone
    for i in range(10):
        for j in range(3):
            n = 1 + i + 10 * j
            cx, cy = 840 + i * 68 + j * 14, 650 + j * 46
            if n == 1 or any(n % q == 0 and n != q for q in (2, 3, 5)):
                p.ink([(cx - 12, cy - 8), (cx + 12, cy + 8)], 2.2, '#5a3a24', 0.8, 0.8)
                p.ink([(cx - 12, cy + 8), (cx + 12, cy - 8)], 2.2, '#5a3a24', 0.8, 0.8)
            else:
                p.lift(p.ellipse_mask(cx, cy, 17, 12), 1.0)
                p.wash(p.ellipse_mask(cx, cy, 15, 10), '#cfc6b4', 0.9, wobble=1, edge=0.9)
                p.ink([(cx + 15 * math.cos(t), cy + 10 * math.sin(t)) for t in np.linspace(0, 6.3, 18)], 1.3, '#3a3a3a', 0.75)
    # winding path up to the ring
    path = [(380, 820), (430, 720), (520, 650), (640, 600), (720, 562)]
    p.lift(p.stroke_mask(path, 60, 10), 0.85)
    p.wash(p.stroke_mask(path, 52, 8), '#d9b98a', 0.6, wobble=2, edge=0.7)
    # signpost
    for x in (150, 530):
        p.lift(p.stroke_mask([(x, 680), (x, 800)], 16), 1.0); p.wash(p.stroke_mask([(x, 680), (x, 800)], 14), '#5a3a24', 0.9, wobble=1)
    p.lift(p.rect_mask(116, 516, 564, 694), 1.0)
    quad(p, [(120, 520), (560, 520), (560, 690), (120, 690)], '#f4ead2', 0.5)
    p.text((340, 565), 'PRIME PEAKS', 46, MARKER, '#1d2433', 0.92)
    p.text((340, 625), 'HILBERT MARKET  1, 5, 9, 13, ...', 25, MARKER, '#c8401a', 0.95)
    p.text((340, 664), 'every stone unbreakable', 20, ROBOTO + 'Roboto-Italic.ttf', '#5a3a24', 0.9)
    p.border(16)
    return p.save(OUT + 'ch5.jpg')


# ---------------- Chapter 6: Clockwork Isles ----------------
def gear(cx, cy, r, teeth, depth=0.18, rot=0.0):
    """Gear outline polygon with square-ish teeth."""
    pts = []
    for k in range(teeth):
        a0 = rot + 2 * math.pi * k / teeth; da = 2 * math.pi / teeth
        for f, rr in ((0.0, r), (0.12, r * (1 + depth)), (0.45, r * (1 + depth)), (0.57, r)):
            a = a0 + f * da; pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def clockface(p, x, y, R, marks, hand=0.0, seed=0):
    face = p.ellipse_mask(x, y, R, R)
    p.lift(face, 1.0)
    p.wash(face, '#f6ecd0', 0.55, wobble=1.2, edge=0.9)
    p.ink([(x + R * math.cos(t), y + R * math.sin(t)) for t in np.linspace(0, 6.3, 40)], 2.0, '#3a2a1a', 0.85)
    for k in range(marks):
        a = -math.pi / 2 + 2 * math.pi * k / marks
        p.ink([(x + R * 0.72 * math.cos(a), y + R * 0.72 * math.sin(a)), (x + R * 0.92 * math.cos(a), y + R * 0.92 * math.sin(a))], 2.0 if k else 3.2, '#1d2433', 0.9, 0.2)
    a = -math.pi / 2 + hand
    p.ink([(x, y), (x + R * 0.6 * math.cos(a), y + R * 0.6 * math.sin(a))], 2.4, '#c8401a', 0.95, 0.2)


def ch6():
    p = Painting(W, H, seed=66)
    SEA = 455
    gate_m = p.poly_mask([(1110, 800), (1110, 420), (1150, 360), (1260, 320), (1370, 360), (1410, 420), (1410, 800)])
    signm = p.rect_mask(90, 560, 560, 720)
    sky_bands(p, 0, SEA, ['#f2b98a', '#e9a6a0', '#c9a3c8', '#f5d2a0', '#b8aad6'], reserve=np.clip(gate_m + signm, 0, 1), n=9, gap=10, strength=0.55, seed=61)
    sun = p.ellipse_mask(820, SEA - 8, 70, 70) * (np.mgrid[0:H, 0:W][0] < SEA)
    p.wash(sun, '#f6b14a', 0.55, wobble=2, edge=0.8)
    # sea
    sea = p.rect_mask(0, SEA, W, H)
    fill_strokes(p, sea, ['#0c5f73', '#1d7f8f', '#2f8f9a', '#145a6e'], SEA, H, thick=26, strength=0.6, seed=62, angle=0.0, reserve=np.clip(gate_m + signm, 0, 1), amp=3)
    rnd = random.Random(7)
    for _ in range(55):
        x, y = rnd.uniform(20, 1080), rnd.uniform(SEA + 20, 790)
        p.ink([(x, y), (x + 10, y - 4), (x + 20, y), (x + 30, y - 4)], 1.1, '#e8f4fb', 0.6, 0.3)
    # six islands with clock towers: 4, 7, 9, 10, 11, 12 marks
    ISL = [(110, 4, 40), (290, 7, 52), (470, 9, 46), (640, 10, 58), (850, 11, 50), (1010, 12, 62)]
    for i, (x, marks, R) in enumerate(ISL):
        top = SEA - 6 - (i % 2) * 14
        isl = blob(x, top + 18, R * 1.9, seed=60 + i, sq=0.32)
        m = p.poly_mask(isl) * (np.mgrid[0:H, 0:W][0] < SEA + 30)
        p.wash(m, ['#6f8f3a', '#8aa848', '#7a9a3a'][i % 3], 0.8, wobble=3, edge=0.8, mix='#c9a46a')
        th = R * 2.6; tw = R * 0.9
        body = [(x - tw / 2, top + 6), (x + tw / 2, top + 6), (x + tw * 0.42, top - th), (x - tw * 0.42, top - th)]
        quad(p, body, ['#d8b48a', '#c99a7a', '#d6c2a0'][i % 3], 0.8, lw=1.4)
        roof = [(x - tw * 0.55, top - th), (x + tw * 0.55, top - th), (x, top - th - R * 0.9)]
        quad(p, roof, ['#c8401a', '#2b6fb8', '#8338ec'][i % 3], 0.85, lw=1.2)
        clockface(p, x, top - th * 0.62, R * 0.42 + 4, marks, hand=2 * math.pi * (i + 1) / marks, seed=i)
        p.light(p.ellipse_mask(x, top - th * 0.18, 5, 7), '#ffcf6a', 0.8)
        for k in range(3):
            p.ink([(x - R * 1.4 + k * 8, top + 30 + k * 6), (x + R * 1.4 - k * 8, top + 30 + k * 6)], 1.0, '#e8f4fb', 0.5, 0.6)
    # gears half-sunk in the shallows
    for (gx, gy, gr, n, col) in ((690, 600, 72, 12, '#b8862a'), (840, 655, 46, 9, '#9a6b12'), (985, 575, 54, 10, '#c89a3a')):
        g = p.poly_mask(gear(gx, gy, gr, n, rot=0.2)) * (np.mgrid[0:H, 0:W][0] < gy + 8)
        hole = p.ellipse_mask(gx, gy, gr * 0.28, gr * 0.28)
        p.lift(np.clip(g - hole, 0, 1), 0.9)
        p.wash(np.clip(g - hole, 0, 1), col, 0.85, wobble=1.5, edge=0.9, gran=0.4)
        p.ink([(gx - gr * 1.3, gy + 8), (gx + gr * 1.3, gy + 8)], 1.6, '#e8f4fb', 0.75, 1.0)
        for k in range(4):
            a = 0.2 + k * math.pi / 4
            p.ink([(gx - gr * 0.25 * math.cos(a), gy - gr * 0.25 * math.sin(a)), (gx - gr * 0.85 * math.cos(a), gy - gr * 0.85 * math.sin(a))], 2.2, '#5a3a14', 0.6, 0.3)
    # the stone gate with a dial lock
    p.lift(gate_m, 1.0)
    p.wash(gate_m, '#a8a092', 0.6, wobble=2, edge=0.9, gran=0.5, mix='#8a8478')
    fill_strokes(p, gate_m, ['#9a9284', '#b0a898', '#8c8476'], 330, 800, thick=36, strength=0.3, seed=63)
    for y in range(430, 800, 52):
        p.ink([(1112, y), (1408, y)], 1.2, '#5a5448', 0.45, 0.8)
    p.ink([(1110, 800), (1110, 420), (1150, 360), (1260, 320), (1370, 360), (1410, 420), (1410, 800)], 2.2, '#3a352c', 0.8)
    dx, dy, dr = 1260, 500, 92
    dial = p.ellipse_mask(dx, dy, dr, dr)
    p.wash(dial, '#c89a3a', 0.75, wobble=1.5, edge=0.9, gran=0.4)
    p.lift(p.ellipse_mask(dx, dy, dr * 0.78, dr * 0.78), 0.9)
    p.wash(p.ellipse_mask(dx, dy, dr * 0.78, dr * 0.78), '#f2e4c0', 0.5, wobble=1, edge=0.9)
    for k in range(7):
        a = -math.pi / 2 + 2 * math.pi * k / 7
        px, py = dx + dr * 0.6 * math.cos(a), dy + dr * 0.6 * math.sin(a)
        p.text((px, py), str(k), 22, RB, '#1d2433', 0.92)
    p.ink([(dx, dy), (dx + dr * 0.38 * math.cos(-math.pi / 2 + 2 * math.pi * 6 / 7), dy + dr * 0.38 * math.sin(-math.pi / 2 + 2 * math.pi * 6 / 7))], 3.2, '#c8401a', 0.95, 0.2)
    p.ink([(dx + dr * math.cos(t), dy + dr * math.sin(t)) for t in np.linspace(0, 6.3, 50)], 2.4, '#3a2a1a', 0.85)
    # carved congruence: 3x  ≡  4 (mod 7), the three bars drawn by hand
    ty = 660
    p.lift(p.rect_mask(1136, ty - 34, 1404, ty + 34), 0.55)
    p.text((1188, ty), '3x', 40, RB, '#2a2620', 0.92)
    for k in (-9, 0, 9):
        p.ink([(1222, ty + k), (1250, ty + k)], 3.0, '#2a2620', 0.92, 0.2)
    p.text((1264, ty + 2), '4 (mod 7)', 30, RB, '#2a2620', 0.92, anchor='lm')
    # jetty and sign
    jet = [(0, 735), (600, 705), (600, 735), (0, 770)]
    quad(p, jet, '#7a5232', 0.85, lw=1.6)
    for x in (60, 200, 340, 480):
        p.wash(p.stroke_mask([(x, 740), (x, 800)], 14), '#5a3a24', 0.9, wobble=1)
    for x in (130, 520):
        p.lift(p.stroke_mask([(x, 700), (x, 740)], 16), 1.0); p.wash(p.stroke_mask([(x, 700), (x, 740)], 14), '#5a3a24', 0.9, wobble=1)
    p.lift(signm, 1.0)
    quad(p, [(94, 564), (556, 564), (556, 706), (94, 706)], '#f4ead2', 0.5)
    p.text((325, 610), 'CLOCKWORK ISLES', 44, MARKER, '#1d2433', 0.92)
    p.text((325, 668), 'every number comes back around', 22, ROBOTO + 'Roboto-Italic.ttf', '#5a3a24', 0.9)
    p.border(16)
    return p.save(OUT + 'ch6.jpg')

if __name__ == '__main__':
    which = sys.argv[1:] or ['ch3']
    for w in which:
        globals()[w]()
        print('done', w)
