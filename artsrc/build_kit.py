import math
from PIL import Image, ImageDraw, ImageFont
import layout
R='/usr/local/lib/python3.13/dist-packages/font_roboto/files/'
F=lambda s,b=False,i=False: ImageFont.truetype(R+('Roboto-BoldItalic.ttf' if b and i else 'Roboto-Bold.ttf' if b else 'Roboto-Italic.ttf' if i else 'Roboto-Regular.ttf'),s)
PW,PH=3300,2550; M=150; INK=(29,36,51); MUTE=(100,106,115); SEA=(12,95,115); EMBER=(200,64,26)
ART='/home/claude/modular-worlds/book/art/'
def page(): return Image.new('RGB',(PW,PH),'white')
def wrap(d,text,font,width):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=font)<=width: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
def para(d,xy,text,font,width,fill=INK,gap=1.35):
    x,y=xy
    for ln in wrap(d,text,font,width):
        d.text((x,y),ln,font=font,fill=fill); y+=int(font.size*gap)
    return y
def header(d,left,right=''):
    d.text((M,90),left,font=F(40,True),fill=SEA); 
    if right: d.text((PW-M,90),right,font=F(34),fill=MUTE,anchor='ra')
def footer(d,text):
    d.text((M,PH-110),text,font=F(30),fill=MUTE)

S={
'ch1':dict(n='1',title='Mojadito, home port',es='Mojadito, puerto de origen',pilot=True,
 keep=[('The harbour sign carries a water molecule: one O between two H, joined.','El letrero del puerto lleva una molécula de agua: una O entre dos H, unidas.',(280,605)),
       ('The flasks on the pier are hammered copper, never plastic bottles.','Los frascos del muelle son de cobre martillado, nunca botellas plásticas.',(555,585)),
       ('It is raining: Mojadito is always a little wet.','Está lloviendo: Mojadito siempre está un poco mojado.',(1100,90))],
 free=('The houses (how many, colours, shapes), hills, lighthouse, palms, ship, sea, sky, light and mood.','Las casas (cuántas, colores, formas), las colinas, el faro, las palmas, el barco, el mar, el cielo, la luz y el ambiente.'),
 letters='MOJADITO on the sign; H, O, H on the molecule.',lettersES='MOJADITO en el letrero; H, O, H en la molécula.',
 moving='the ship, the rain, the lighthouse beam',movingES='el barco, la lluvia, el haz del faro'),
'ch0':dict(n='0',title='The Entrance Exam: the Hall of a Hundred Doors',es='El Examen de Entrada: la Sala de las Cien Puertas',
 keep=[('A row of doors along the wall, numbered from 1 and shrinking into the distance: 19 are visible, then “… 100”.','Una fila de puertas a lo largo del muro, numeradas desde 1 y cada vez más pequeñas: se ven 19 y luego “… 100”.',(300,250)),
       ('Only doors 1, 4 and 9 are open (the perfect squares). All the others are closed.','Solo las puertas 1, 4 y 9 están abiertas (los cuadrados perfectos). Todas las demás están cerradas.',(470,420)),
       ('The floor is an 8 × 8 checkerboard with exactly two opposite corner squares broken out.','El piso es un tablero de 8 × 8 con exactamente dos casillas de esquinas opuestas rotas.',(640,775))],
 free=('Door colours, the wall, the sky, the papel picado, the palm, the plaza.','Los colores de las puertas, el muro, el cielo, el papel picado, la palma, la plaza.'),
 letters='The door numbers, “… 100”, and HALL OF A HUNDRED DOORS.',lettersES='Los números de las puertas, “… 100” y HALL OF A HUNDRED DOORS.',
 moving='the papel picado, the palm',movingES='el papel picado, la palma'),
'ch3':dict(n='3',title='Euclid’s Forge',es='La Forja de Euclides',
 keep=[('A two-pan balance, level. Left pan: three red O weights. Right pan: two blue N weights and one small yellow bead (3 × 5 = 2 × 7 + 1).','Una balanza de dos platillos, nivelada. Platillo izquierdo: tres pesas rojas O. Derecho: dos pesas azules N y una cuenta amarilla pequeña (3 × 5 = 2 × 7 + 1).',(730,450)),
       ('The forge glows from an arched opening in the cliff, at night.','La forja brilla desde una abertura en arco en el acantilado, de noche.',(1300,520))],
 free=('The moon, the stars, the palms, the sea, the shape of the cliff, the sparks.','La luna, las estrellas, las palmas, el mar, la forma del acantilado, las chispas.'),
 letters='O and N on the weights.',lettersES='O y N en las pesas.',
 moving='the sparks, the forge glow, the sea',movingES='las chispas, el brillo de la forja, el mar'),
'ch4':dict(n='4',title='Diophantine Delta',es='El Delta Diofántico',
 keep=[('The toll board shows exactly two coins, 5 and 7, and no other values.','El tablero del peaje muestra exactamente dos monedas, 5 y 7, y ningún otro valor.',(315,600)),
       ('Ferries fly black flags, and the water winds between reed islands.','Los ferris llevan banderas negras, y el agua serpentea entre islas de juncos.',(1360,560))],
 free=('How many islands and ferries, the fog, the sun, the colours.','Cuántas islas y ferris, la niebla, el sol, los colores.'),
 letters='FIVES AND SEVENS ONLY, NO CHANGE, and 5 and 7 on the coins.',lettersES='FIVES AND SEVENS ONLY, NO CHANGE, y 5 y 7 en las monedas.',
 moving='the ferries, the fog',movingES='los ferris, la niebla'),
'ch5':dict(n='5',title='Prime Peaks',es='Los Picos Primos',
 keep=[('Exactly six peaks with pennants, for 2, 3, 5, 7, 11 and 13 from left to right.','Exactamente seis picos con banderines, para 2, 3, 5, 7, 11 y 13 de izquierda a derecha.',(700,60)),
       ('The sieve fields: 30 plots in 3 rows of 10 (1–10, 11–20, 21–30). Round stones on the primes 2, 3, 5, 7, 11, 13, 17, 19, 23, 29; a cross on every other plot, including 1.','Los campos de la criba: 30 parcelas en 3 filas de 10 (1–10, 11–20, 21–30). Piedras redondas en los primos 2, 3, 5, 7, 11, 13, 17, 19, 23, 29; una cruz en todas las demás, incluida la 1.',(1150,700)),
       ('The signpost board stays blank: three lines of lettering go there later.','El tablero del poste queda en blanco: allí van después tres líneas de texto.',(340,600))],
 free=('The shapes of the mountains, the snow, the sky, the sun, the path, the terraces.','La forma de las montañas, la nieve, el cielo, el sol, el camino, las terrazas.'),
 letters='The numbers on the pennants, and PRIME PEAKS / HILBERT MARKET 1, 5, 9, 13, … / every stone unbreakable.',lettersES='Los números de los banderines, y PRIME PEAKS / HILBERT MARKET 1, 5, 9, 13, … / every stone unbreakable.',
 moving='the pennants, the clouds',movingES='los banderines, las nubes')}
ORDER=['ch1','ch0','ch3','ch4','ch5']

def layout_page(key,dark):
    s=S[key]; pg=page(); d=ImageDraw.Draw(pg)
    header(d,f'Modular Worlds · Chapter {s["n"]} · {s["title"]}','Layout B: darker, for tracing on a lightbox / Plantilla B: más oscura, para calcar' if dark else 'Layout A: light, to paint over directly / Plantilla A: clara, para pintar encima')
    col=(130,130,130) if dark else (200,200,200)
    im,_=layout.render(key,S=1.875,line=col)  # 3000 x 1500
    x0,y0=(PW-3000)//2,430; pg.paste(im,(x0,y0))
    d.rectangle([x0,y0,x0+3000,y0+1500],outline=(170,170,170),width=2)
    for (cx,cy) in ((x0,y0),(x0+3000,y0),(x0,y0+1500),(x0+3000,y0+1500)):
        for dx,dy in ((1,0),(0,1)):
            sx=-1 if cx>x0 else 1; sy=-1 if cy>y0 else 1
            d.line([(cx-sx*40*dx-sx*90*dx if False else cx-sx*(130 if dx else 0),cy-sy*(130 if dy else 0)),(cx-sx*(30 if dx else 0),cy-sy*(30 if dy else 0))],fill=(60,60,60),width=3)
    footer(d,'Print at 100% (actual size) on letter landscape. Image area 10 × 5 in (25.4 × 12.7 cm). Paint about 1 cm past the frame. Dashed blue boxes: leave blank for lettering.')
    d.text((M,PH-60),'Imprima al 100 % (tamaño real) en carta horizontal. Área de imagen: 25,4 × 12,7 cm. Pinte cerca de 1 cm más allá del marco. Recuadros azules punteados: déjelos en blanco para el texto.',font=F(30,i=True),fill=MUTE)
    return pg
def ref_page(key):
    s=S[key]; pg=page(); d=ImageDraw.Draw(pg)
    header(d,f'Modular Worlds · Chapter {s["n"]} · {s["title"]}','Colour reference / Referencia de color')
    im=Image.open(ART+key+'.jpg').convert('RGB').resize((3000,1500),Image.LANCZOS); pg.paste(im,((PW-3000)//2,430))
    footer(d,'My computer version, for composition and palette only. Your brushwork, colours and light are welcome to differ.')
    d.text((M,PH-60),'Mi versión por computador, solo como guía de composición y paleta. Su pincelada, sus colores y su luz pueden ser distintos.',font=F(30,i=True),fill=MUTE)
    return pg
def keep_page(key):
    s=S[key]; pg=page(); d=ImageDraw.Draw(pg)
    header(d,f'Modular Worlds · Chapter {s["n"]} · {s["title"]}','Keep exact / Mantener exacto')
    w,h=1500,750; im=Image.open(ART+key+'.jpg').convert('RGB').resize((w,h),Image.LANCZOS); x0,y0=M,260; pg.paste(im,(x0,y0))
    for i,(_,_,(cx,cy)) in enumerate(s['keep']):
        px,py=x0+cx*w/1600,y0+cy*h/800; r=34
        d.ellipse([px-r,py-r,px+r,py+r],fill=EMBER,outline='white',width=5); d.text((px,py),str(i+1),font=F(40,True),fill='white',anchor='mm')
    tx=x0+w+90; tw=PW-M-tx; y=y0
    d.text((tx,y),'Keep exact (this carries the math)',font=F(44,True),fill=EMBER); y+=60
    d.text((tx,y),'Mantener exacto (aquí está la matemática)',font=F(36,i=True),fill=MUTE); y+=70
    for i,(en,es,_) in enumerate(s['keep']):
        d.ellipse([tx,y+4,tx+46,y+50],fill=EMBER); d.text((tx+23,y+27),str(i+1),font=F(30,True),fill='white',anchor='mm')
        y=para(d,(tx+66,y),en,F(36),tw-66); y=para(d,(tx+66,y+4),es,F(32,i=True),tw-66,fill=MUTE)+30
    y=max(y,y0+h+60); x=M; tw2=PW-2*M
    if key=='ch5':
        d.text((x,y),'The sieve fields, plot by plot / Los campos de la criba, parcela por parcela',font=F(36,True),fill=INK); y+=60
        P={2,3,5,7,11,13,17,19,23,29}; cw=120
        for r in range(3):
            for c in range(10):
                n=r*10+c+1; bx,by=x+c*cw,y+r*cw
                d.rectangle([bx,by,bx+cw-10,by+cw-10],outline=(180,180,180),width=2); d.text((bx+10,by+8),str(n),font=F(26),fill=MUTE)
                if n in P: d.ellipse([bx+30,by+40,bx+cw-40,by+cw-25],outline=INK,width=5)
                else: d.line([(bx+32,by+42),(bx+cw-42,by+cw-28)],fill=INK,width=6); d.line([(bx+32,by+cw-28),(bx+cw-42,by+42)],fill=INK,width=6)
        sx=x+10*cw+60; yy=y
        yy=para(d,(sx,yy),'○ stone = prime (cannot be split)   ✕ cross = 1 or composite',F(32),PW-M-sx)
        yy=para(d,(sx,yy+10),'○ piedra = primo (no se puede partir)   ✕ cruz = 1 o compuesto',F(30,i=True),PW-M-sx,fill=MUTE)
        y+=3*cw+40
    d.text((x,y),'Free to change / Libre',font=F(40,True),fill=SEA); y+=58
    y=para(d,(x,y),s['free'][0],F(34),tw2); y=para(d,(x,y+2),s['free'][1],F(30,i=True),tw2,fill=MUTE)+26
    d.text((x,y),'Leave blank: lettering we add later / Dejar en blanco: el texto se añade después',font=F(40,True),fill=SEA); y+=58
    y=para(d,(x,y),s['letters'],F(34),tw2); y=para(d,(x,y+2),s['lettersES'],F(30,i=True),tw2,fill=MUTE)+26
    d.text((x,y),'Optional: moving parts on their own sheet (for the videos) / Opcional: partes que se mueven, en hoja aparte (para los videos)',font=F(40,True),fill=SEA); y+=58
    y=para(d,(x,y),s['moving'][0].upper()+s['moving'][1:]+'.',F(34),tw2); y=para(d,(x,y+2),s['movingES'][0].upper()+s['movingES'][1:]+'.',F(30,i=True),tw2,fill=MUTE)
    if s.get('pilot'):
        d.rounded_rectangle([PW-M-1150,PH-330,PW-M,PH-150],radius=24,fill=(250,236,210))
        para(d,(PW-M-1120,PH-310),'Pilot: please start with this one. The houses are where my version looks most digital.',F(32,True),1090)
        para(d,(PW-M-1120,PH-225),'Piloto: por favor empiece por esta. Las casas son donde mi versión se ve más digital.',F(30,i=True),1090,fill=MUTE)
    return pg

def brief():
    p1=page(); d=ImageDraw.Draw(p1)
    d.text((M,130),'Modular Worlds · Painting kit, batch 1',font=F(84,True),fill=SEA)
    d.text((M,240),'Kit de pintura, lote 1',font=F(64,i=True),fill=MUTE)
    y=380; tw=PW-2*M
    for en,es in [('Hi Roberto! Thank you for painting with us. Modular Worlds is a number theory course and web book that grew out of Math CEO’s Meeting 6, Modular Atoms. Its look follows your Mojadito watercolours, and now we would love the real thing: your hand on the paintings.',
                   '¡Hola, Roberto! Gracias por pintar con nosotros. Modular Worlds es un curso y libro web de teoría de números que nació de la reunión 6 de Math CEO, Modular Atoms. Su estilo sigue sus acuarelas de Mojadito, y ahora quisiéramos lo auténtico: su mano en las pinturas.'),
                  ('Each painting comes with a layout I made by computer. The layout fixes the parts that carry the math (counts, numbers, what lines up with what). Everything else is yours: brushwork, colour, light, small details. Please feel free to move a palm tree or change the sky.',
                   'Cada pintura viene con una plantilla hecha por computador. La plantilla fija las partes que llevan la matemática (cantidades, números, qué se alinea con qué). Todo lo demás es suyo: la pincelada, el color, la luz, los detalles. Puede mover una palma o cambiar el cielo con toda libertad.')]:
        y=para(p1 and d,(M,y),en,F(40),tw); y=para(d,(M,y+6),es,F(36,i=True),tw,fill=MUTE)+40
    d.text((M,y),'The five paintings / Las cinco pinturas',font=F(48,True),fill=INK); y+=80
    tw5=(PW-2*M-4*60)//5
    for i,k in enumerate(ORDER):
        im=Image.open(ART+k+'.jpg').convert('RGB'); im.thumbnail((tw5,tw5)); x=M+i*(tw5+60); p1.paste(im,(x,y))
        s=S[k]; yy=y+im.height+20
        yy=para(d,(x,yy),f'{i+1}. Chapter {s["n"]}: {s["title"]}'+(' (pilot)' if s.get('pilot') else ''),F(32,True),tw5)
        para(d,(x,yy+2),s['es'],F(28,i=True),tw5,fill=MUTE)
    footer(d,'Modular Worlds · UCI Math CEO · batch 1 · November 2026')
    p2=page(); d=ImageDraw.Draw(p2); header(d,'How to work / Cómo trabajar')
    y=200; cols=[(M,(PW-3*M)//2),(M*2+(PW-3*M)//2,(PW-3*M)//2)]
    blocks=[('In each kit (one PDF per painting)','En cada kit (un PDF por pintura)',['Page 1, Layout A: light lines, to print straight onto watercolour paper and paint over.','Page 2, Layout B: darker lines, to trace on a lightbox or a window.','Page 3: my colour version, for composition and palette.','Page 4: what to keep exact, what is free, and what to leave blank.'],['Página 1, plantilla A: líneas claras, para imprimir directamente sobre papel de acuarela y pintar encima.','Página 2, plantilla B: líneas más oscuras, para calcar con mesa de luz o en una ventana.','Página 3: mi versión a color, para composición y paleta.','Página 4: qué mantener exacto, qué es libre y qué dejar en blanco.']),
            ('Getting the layout onto paper','Pasar la plantilla al papel',['Print Layout A at 100% onto watercolour paper your printer accepts, or ask a print shop.','Or trace Layout B on a lightbox or a sunny window.','Or use graphite transfer paper. Faint lines are fine: they can stay as a pencil underdrawing.'],['Imprima la plantilla A al 100 % en un papel de acuarela que acepte su impresora, o en una papelería.','O calque la plantilla B con mesa de luz o en una ventana soleada.','O use papel de transferencia de grafito. Las líneas suaves pueden quedar como dibujo a lápiz.']),
            ('Paper and size','Papel y tamaño',['Cold-press watercolour paper, about 300 g/m².','Image area 10 × 5 in (25.4 × 12.7 cm), landscape. Paint about 1 cm past the frame so we can trim.','Larger is welcome if you keep the 2 : 1 shape.'],['Papel de acuarela prensado en frío (grano fino), de unos 300 g/m².','Área de imagen de 25,4 × 12,7 cm, horizontal. Pinte cerca de 1 cm más allá del marco para poder recortar.','Más grande también sirve, si mantiene la proporción 2 : 1.']),
            ('Leave lettering out','No pinte las letras',['Paint signs, plaques, pennants and coins as blank shapes (the dashed blue boxes).','We add the words digitally, so they stay sharp on phones and can be translated into Spanish.'],['Pinte letreros, placas, banderines y monedas como formas en blanco (los recuadros azules punteados).','Añadimos las palabras en digital: así se leen bien en celulares y se pueden traducir al español.']),
            ('Scanning and sending','Escanear y enviar',['Scan flat at 600 dpi, colour, with auto-enhance turned off. TIFF or PNG.','Leave some bare paper around the edge: it gives us a real paper texture.','No scanner? Photograph it flat in soft daylight, with no shadows, filling the frame.'],['Escanee plano a 600 dpi, a color, sin mejoras automáticas. TIFF o PNG.','Deje algo de papel sin pintar alrededor: nos da una textura de papel real.','¿Sin escáner? Fotografíela plana con luz de día suave, sin sombras, llenando el encuadre.']),
            ('Optional: moving parts','Opcional: partes que se mueven',['For the videos, paint things that will move (a boat, sparks, pennants) on a separate sheet. Page 4 of each kit suggests which.','No characters for now: the student crew joins in a later batch.'],['Para los videos, pinte en hoja aparte lo que se moverá (un barco, chispas, banderines). La página 4 de cada kit sugiere qué.','Por ahora sin personajes: el grupo de estudiantes llega en un lote posterior.'])]
    ys=[y,y]
    for bi,(h1,h2,en,es) in enumerate(blocks):
        c=bi%2; x,w=cols[c]; yy=ys[c]
        d.text((x,yy),h1,font=F(42,True),fill=SEA); yy+=56; d.text((x,yy),h2,font=F(34,i=True),fill=MUTE); yy+=56
        for a,b in zip(en,es):
            d.text((x,yy),'•',font=F(34),fill=INK); yy=para(d,(x+36,yy),a,F(32),w-36); yy=para(d,(x+36,yy),b,F(29,i=True),w-36,fill=MUTE)+14
        ys[c]=yy+40
    footer(d,'Thank you! Any question about the math in a picture, just ask. / ¡Gracias! Cualquier duda sobre la matemática de una imagen, con gusto la resolvemos.')
    return [p1,p2]

OUTD='/mnt/user-data/outputs/'
b=brief(); b[0].save(OUTD+'Modular Worlds painting kit - 0 Brief.pdf',save_all=True,append_images=b[1:],resolution=300)
for i,k in enumerate(ORDER):
    pages=[layout_page(k,False),layout_page(k,True),ref_page(k),keep_page(k)]
    s=S[k]; name=f'Modular Worlds painting kit - {i+1} Chapter {s["n"]} {s["title"].split(":")[0]}.pdf'
    pages[0].save(OUTD+name,save_all=True,append_images=pages[1:],resolution=300); print(name)
