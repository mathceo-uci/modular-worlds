"""Procedural watercolor painting toolkit for the Modular Worlds book.

Style target: loose hand-painted watercolor (layered transparent washes, granulating
pigment, darkened wet edges, white paper showing between shapes, wobbly ink lines),
inspired by Roberto Forero's M6 Mojadito illustrations.
"""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

ROBOTO = '/usr/local/lib/python3.13/dist-packages/font_roboto/files/'
MARKER = '/home/claude/mathceo-video-engine/fonts/PermanentMarker-Regular.ttf'


def hexc(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


class Painting:
    def __init__(self, W, H, seed=1, paper='#fbf7ef'):
        self.W, self.H = W, H
        self.rng = np.random.default_rng(seed)
        random.seed(seed)
        tex = self.noise(7, 7, 3) * 0.6 + self.noise(2.5, 2.5, 2) * 0.4
        self.paper_tex = tex
        base = hexc(paper)
        self.c = np.ones((H, W, 3)) * base * (1 - 0.035 * tex[..., None])

    # ---------- noise ----------
    def noise(self, sx=60, sy=60, octaves=4, persist=0.55):
        """Fractal value noise in [0,1]; sx, sy = feature size in px (anisotropic allowed)."""
        W, H = self.W, self.H
        out = np.zeros((H, W)); amp = 1; tot = 0
        for o in range(octaves):
            fx, fy = max(1.0, sx / 2 ** o), max(1.0, sy / 2 ** o)
            gw, gh = max(2, int(W / fx) + 2), max(2, int(H / fy) + 2)
            g = self.rng.random((gh, gw)).astype(np.float32)
            im = Image.fromarray((g * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
            out += amp * np.asarray(im, dtype=np.float32) / 255
            tot += amp; amp *= persist
        out /= tot
        out = (out - out.min()) / (out.max() - out.min() + 1e-9)
        return out

    # ---------- masks ----------
    def poly_mask(self, pts, blur=0):
        im = Image.new('L', (self.W, self.H), 0)
        ImageDraw.Draw(im).polygon([tuple(map(float, p)) for p in pts], fill=255)
        m = np.asarray(im, dtype=np.float32) / 255
        return gaussian_filter(m, blur) if blur else m

    def ellipse_mask(self, cx, cy, rx, ry):
        im = Image.new('L', (self.W, self.H), 0)
        ImageDraw.Draw(im).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
        return np.asarray(im, dtype=np.float32) / 255

    def rect_mask(self, x0, y0, x1, y1):
        m = np.zeros((self.H, self.W), np.float32)
        m[max(0, int(y0)):max(0, int(y1)), max(0, int(x0)):max(0, int(x1))] = 1
        return m

    def stroke_mask(self, pts, w0, w1=None, blur=0):
        """Tapered brush stroke along a polyline."""
        w1 = w0 if w1 is None else w1
        im = Image.new('L', (self.W, self.H), 0); d = ImageDraw.Draw(im)
        n = len(pts)
        for i in range(n - 1):
            t = i / max(1, n - 2)
            w = w0 + (w1 - w0) * t
            d.line([tuple(pts[i]), tuple(pts[i + 1])], fill=255, width=max(1, int(w)))
            r = w / 2
            d.ellipse([pts[i][0] - r, pts[i][1] - r, pts[i][0] + r, pts[i][1] + r], fill=255)
        m = np.asarray(im, dtype=np.float32) / 255
        return gaussian_filter(m, blur) if blur else m

    # ---------- painting ----------
    def wash(self, mask, color, strength=0.8, wobble=5, edge=0.5, gran=0.25, var=0.35, seed=None, rough=0.45, streak=None, reserve=None, halo=4):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        col = hexc(color) if isinstance(color, str) else np.array(color)
        H, W = self.H, self.W
        m = gaussian_filter(mask.astype(np.float32), wobble) if wobble else mask.astype(np.float32)
        n1 = self.noise(wobble * 6 + 20, wobble * 6 + 20, 3)
        m2 = np.clip((m + (n1 - 0.5) * rough - 0.5) * 5 + 0.5, 0, 1)
        m2 = m2 * (mask > 0.02) if wobble == 0 else m2
        if reserve is not None:
            rv = gaussian_filter(reserve.astype(np.float32), halo)
            rv = np.clip((rv + (self.noise(30, 30, 2) - 0.5) * 0.3 - 0.12) * 6, 0, 1)
            m2 = m2 * (1 - rv)
        rim = np.clip(m2 - gaussian_filter(m2, 3.5), 0, 1) * edge * 3.0
        if streak:
            nv = self.noise(streak[0], streak[1], 4)
        else:
            nv = self.noise(90, 90, 4)
        dens = strength * m2 * (1 - var / 2 + var * nv) + rim * m2
        fine = self.paper_tex
        dens = dens * (1 + gran * (fine - 0.5) * 2)
        dens = np.clip(dens, 0, 1)[..., None]
        self.c = self.c * (1 - dens * (1 - col))

    def glaze(self, mask, color, strength=0.5):
        col = hexc(color)
        d = np.clip(mask * strength, 0, 1)[..., None]
        self.c = self.c * (1 - d * (1 - col))

    def lift(self, mask, amount=0.7):
        paper = np.array([0.985, 0.97, 0.94])
        d = np.clip(mask * amount, 0, 1)[..., None]
        self.c = self.c * (1 - d) + paper * d

    def light(self, mask, color, amount=0.8):
        """Add glowing light (screen blend), for fire, lanterns, windows."""
        col = hexc(color)
        d = np.clip(mask * amount, 0, 1)[..., None]
        self.c = 1 - (1 - self.c) * (1 - d * col)

    def ink(self, pts, width=2.0, color='#1d2433', alpha=0.85, jitter=1.2, closed=False):
        """Wobbly hand-drawn ink line."""
        if closed:
            pts = list(pts) + [pts[0]]
        # densify and jitter
        dense = []
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            L = math.hypot(x1 - x0, y1 - y0); k = max(2, int(L / 6))
            for j in range(k):
                t = j / k
                dense.append([x0 + (x1 - x0) * t, y0 + (y1 - y0) * t])
        dense.append(list(pts[-1]))
        ph = random.random() * 10
        for i, p in enumerate(dense):
            p[0] += math.sin(i * 0.37 + ph) * jitter + random.uniform(-0.4, 0.4)
            p[1] += math.cos(i * 0.29 + ph) * jitter + random.uniform(-0.4, 0.4)
        S = 2
        im = Image.new('L', (self.W * S, self.H * S), 0); d = ImageDraw.Draw(im)
        for i in range(len(dense) - 1):
            w = width * S * (0.7 + 0.6 * abs(math.sin(i * 0.11 + ph)))
            d.line([(dense[i][0] * S, dense[i][1] * S), (dense[i + 1][0] * S, dense[i + 1][1] * S)], fill=255, width=max(1, int(w)))
        m = np.asarray(im.resize((self.W, self.H), Image.LANCZOS), dtype=np.float32) / 255
        col = hexc(color)
        a = (m * alpha)[..., None]
        self.c = self.c * (1 - a) + col * a * (0.85 + 0.15 * self.c)

    def text(self, xy, s, size=40, font=MARKER, color='#1d2433', alpha=0.9, anchor='mm', angle=0):
        f = ImageFont.truetype(font, size)
        im = Image.new('L', (self.W, self.H), 0); d = ImageDraw.Draw(im)
        d.text(xy, s, font=f, fill=255, anchor=anchor)
        if angle:
            im = im.rotate(angle, center=xy, resample=Image.BICUBIC)
        m = np.asarray(im, dtype=np.float32) / 255
        col = hexc(color); a = (m * alpha)[..., None]
        self.c = self.c * (1 - a) + col * a

    def splatter(self, n, color, region=None, rmin=1, rmax=4, strength=0.6):
        x0, y0, x1, y1 = region or (0, 0, self.W, self.H)
        im = Image.new('L', (self.W, self.H), 0); d = ImageDraw.Draw(im)
        for _ in range(n):
            x, y = random.uniform(x0, x1), random.uniform(y0, y1); r = random.uniform(rmin, rmax)
            d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        self.wash(np.asarray(im, dtype=np.float32) / 255, color, strength, wobble=0.8, edge=0.6, rough=0.2)

    def border(self, margin=0):
        """Ragged painted edge fading to paper, like a watercolor on a sheet."""
        if margin <= 0:
            return
        H, W = self.H, self.W
        yy, xx = np.mgrid[0:H, 0:W]
        dist = np.minimum.reduce([xx, yy, W - 1 - xx, H - 1 - yy]).astype(np.float32)
        n = self.noise(40, 40, 3)
        k = np.clip((dist - margin * (0.6 + 0.8 * n)) / 6, 0, 1)[..., None]
        paper = np.array([0.985, 0.97, 0.94])
        self.c = self.c * k + paper * (1 - k)

    def save(self, path, quality=88):
        im = Image.fromarray((np.clip(self.c, 0, 1) * 255).astype(np.uint8))
        if path.endswith('.jpg'):
            im.save(path, quality=quality, optimize=True, progressive=True)
        else:
            im.save(path)
        return im


def jag(x0, x1, y, amp, n, rng=random):
    """Jagged horizon polyline from x0 to x1 around height y."""
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y + rng.uniform(-amp, amp)))
    return pts
