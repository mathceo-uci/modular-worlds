"""Line layouts for hand-painting: re-run a scene, record its shapes instead of painting them."""
import sys, math, inspect
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import wc
REC=[]; SKIP={'sky_bands','fill_strokes','stars','rain','splatter'}
def skipping():
    return any(f.function in SKIP for f in inspect.stack()[2:12])
P=wc.Painting
_poly,_ell,_rect,_stroke=P.poly_mask,P.ellipse_mask,P.rect_mask,P.stroke_mask
def poly(self,pts,blur=0):
    if not skipping(): REC.append(('poly',[tuple(map(float,q)) for q in pts]))
    return _poly(self,pts,blur)
def ell(self,cx,cy,rx,ry):
    if not skipping() and rx>4: REC.append(('ell',(cx,cy,rx,ry)))
    return _ell(self,cx,cy,rx,ry)
def rect(self,x0,y0,x1,y1):
    if not skipping() and not (x1-x0>1200 and y1-y0<60): REC.append(('poly',[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]))
    return _rect(self,x0,y0,x1,y1)
def stroke(self,pts,w0,w1=None,blur=0):
    if not skipping() and w0>=6: REC.append(('stroke',([tuple(map(float,q)) for q in pts],w0,w1 if w1 is not None else w0)))
    return _stroke(self,pts,w0,w1,blur)
def ink(self,pts,width=2.0,color='#1d2433',alpha=0.85,jitter=1.2,closed=False):
    if not skipping(): REC.append(('line',([tuple(map(float,q)) for q in pts],closed)))
def text(self,xy,s,size=40,font=wc.MARKER,color='#1d2433',alpha=0.9,anchor='mm',angle=0):
    REC.append(('text',(xy,s,size,anchor,angle)))
noop=lambda *a,**k: None
P.poly_mask,P.ellipse_mask,P.rect_mask,P.stroke_mask,P.ink,P.text=poly,ell,rect,stroke,ink,text
for m in ('wash','glaze','lift','light','splatter','border','finish'): setattr(P,m,noop)
P.save=lambda self,path,**k: path
import scenes
scenes.OUT='/tmp/'

EXCL={'ch1':lambda k,d: k=='poly' and (1360.0,214.0) in d,
 'ch3':lambda k,d: k=='poly' and (1150.0,615.0) in d and (1450.0,615.0) in d,
 'ch5':lambda k,d: k=='poly' and len(d)==3 and d[1][1]==560.0}
def render(name, S=2.0625, line=(150,150,150), out=None):
    REC.clear(); getattr(scenes,name)()
    ex=EXCL.get(name)
    if ex: REC[:]=[(k,d) for k,d in REC if not ex(k,d)]
    W,H=int(1600*S),int(800*S)
    im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    f=lambda q:(q[0]*S,q[1]*S); lw=max(2,int(1.3*S))
    seen=set()
    for kind,data in REC:
        key=(kind,str(data)[:400])
        if key in seen: continue
        seen.add(key)
        if kind=='poly':
            pts=[f(q) for q in data]
            if len(pts)>2: d.line(pts+[pts[0]],fill=line,width=lw,joint='curve')
        elif kind=='ell':
            cx,cy,rx,ry=data; d.ellipse([ (cx-rx)*S,(cy-ry)*S,(cx+rx)*S,(cy+ry)*S ],outline=line,width=lw)
        elif kind=='line':
            pts,closed=data; pts=[f(q) for q in pts]
            if len(pts)>1: d.line(pts+([pts[0]] if closed else []),fill=line,width=lw,joint='curve')
        elif kind=='stroke':
            pts,w0,w1=data
            if len(pts)==2:
                (x0,y0),(x1,y1)=pts; dx,dy=x1-x0,y1-y0; L=math.hypot(dx,dy) or 1; nx,ny=-dy/L,dx/L
                a=w0/2; b=w1/2
                q=[(x0+nx*a,y0+ny*a),(x1+nx*b,y1+ny*b),(x1-nx*b,y1-ny*b),(x0-nx*a,y0-ny*a)]
                d.line([f(z) for z in q]+[f(q[0])],fill=line,width=lw)
            else: d.line([f(z) for z in pts],fill=line,width=lw,joint='curve')
    # lettering areas: dashed box + tiny label of the words, in blue
    font=ImageFont.truetype(wc.ROBOTO+'Roboto-Regular.ttf',int(9*S))
    for kind,data in REC:
        if kind!='text': continue
        (x,y),s,size,anchor,angle=data
        w=0.62*size*len(s)*S; h=size*1.05*S; cx,cy=x*S,y*S
        if anchor=='lm': cx+=w/2
        box=[(cx-w/2,cy-h/2),(cx+w/2,cy-h/2),(cx+w/2,cy+h/2),(cx-w/2,cy+h/2)]
        if angle:
            t=math.radians(-angle); box=[(cx+(px-cx)*math.cos(t)-(py-cy)*math.sin(t),cy+(px-cx)*math.sin(t)+(py-cy)*math.cos(t)) for px,py in box]
        for i in range(4):
            (ax,ay),(bx,by)=box[i],box[(i+1)%4]; n=int(math.hypot(bx-ax,by-ay)/(6*S))+1
            for k in range(0,n,2):
                t0,t1=k/n,min(1,(k+1)/n); d.line([(ax+(bx-ax)*t0,ay+(by-ay)*t0),(ax+(bx-ax)*t1,ay+(by-ay)*t1)],fill=(120,160,220),width=max(1,lw-1))
        d.text((cx,cy),s,font=font,fill=(120,160,220),anchor='mm')
    if out: im.save(out)
    return im, REC[:]
if __name__=='__main__':
    for n in sys.argv[1:]:
        im,r=render(n,out=f'kit/{n}_lines.png'); print(n,len(r),'shapes')
