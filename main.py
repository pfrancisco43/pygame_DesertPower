import pygame as pg
from sys import exit
from random import randint

import pygame.time


def heroiAnimation():
    global heroiInd, heroiImg
    heroiInd += 0.4
    if heroiInd >= len(herois):
        heroiInd = 0
    heroiImg = herois[int(heroiInd)]

def helisAnimation():
    global helisInd, helisImg
    helisInd += 0.4
    if helisInd >= len(helis):
        helisInd = 0
    helisImg = helis[int(helisInd)]

def tanqueAnimation():
    global tanqueInd, tanqueImg
    tanqueInd += 0.05
    if tanqueInd >= len(tanques):
        tanqueInd = 0
    tanqueImg = tanques[int(tanqueInd)]

def movimentoHeroi():
    global rodando, acabou
    keys=pg.key.get_pressed()
    velocidade=4
    if keys[pg.K_UP]:
        heroiRec.top -= velocidade
        if heroiRec.top <= teto:
            heroiRec.top=teto
    if keys[pg.K_DOWN]:
        heroiRec.bottom += velocidade
        if heroiRec.bottom >= chao:
            #heroiRec.bottom=700
            acabou=True
            rodando=False
    if keys[pg.K_LEFT]:
        heroiRec.left -= velocidade
        if heroiRec.left <= 0:
            heroiRec.left=0

    if keys[pg.K_RIGHT]:
        heroiRec.right += velocidade
        if heroiRec.right >= 800:
            heroiRec.right=800

def atirar(listaTiros):
    global pontos
    velocidadeTiro=6
    qi=len(listaTiros)
    if listaTiros:
        for umTiroRec in listaTiros:
            umTiroRec.x += velocidadeTiro
            tela.blit(tiroImg,umTiroRec)
        #atualizar a lista
        listaTiros =[rec for rec in listaTiros if rec.left < 850]
        qf=len(listaTiros)
        if qi != qf:
            dif =qi-qf
            pontos -= (dif)*5
            if pontos < 0:
                pontos =0

        return listaTiros
    else:
        return []
    return []

def bombardear(listaBombas):
    global pontos
    velocidadeTiro=5
    qi=len(listaBombas)
    if listaBombas:
        for umTiroRec in listaBombas:
            umTiroRec.y += velocidadeTiro
            tela.blit(bombaImg,umTiroRec)
        #atualizar a lista
        listaBombas =[rec for rec in listaBombas if rec.bottom < chao]
        qf = len(listaBombas)
        if qi != qf:
            dif = qi - qf
            pontos -= (dif) * 5
            if pontos < 0:
                pontos = 0
        return listaBombas
    else:
        return []
    return []

def tiroDestroiInimigo(listaTiros,listaInimigos):
    global pontos, listaEsplosoes, listaTempoEsplosao
    #verirfica se um tiro acertou em algum inimigo
    if listaTiros:
        tiroCerteiro=False
        for umTiro in listaTiros:
            if listaInimigos:
                inimigoDestuido = False
                for umInimigo in listaInimigos:
                    if umTiro.colliderect(umInimigo):
                        pontos += 10
                        inimigoDestuido=umInimigo
                        som=pg.mixer.Sound('sons/explosao.wav')
                        som.play()
                        listaEsplosoes.append(esploImg.get_rect(center=umInimigo.center))
                        listaTempoEsplosao.append(1)
                        break
                if inimigoDestuido:
                    listaInimigos.remove(inimigoDestuido)
                    tiroCerteiro=umTiro
                    break
        if tiroCerteiro:
            listaTiros.remove(tiroCerteiro)
    return listaTiros,listaInimigos

def bombaDestroiInimigo(listaBombas,listaInimigos):
    global pontos
    #verirfica se um tiro acertou em algum inimigo
    if listaBombas:
        tiroCerteiro=False
        for umTiro in listaBombas:
            if listaInimigos:
                inimigoDestuido = False
                for umInimigo in listaInimigos:
                    if umTiro.colliderect(umInimigo):
                        pontos += 10
                        inimigoDestuido=umInimigo
                        som = pg.mixer.Sound('sons/explosao.wav')
                        som.play()
                        listaEsplosoes.append(esploImg.get_rect(center=umInimigo.center))
                        listaTempoEsplosao.append(1)
                        break
                if inimigoDestuido:
                    listaInimigos.remove(inimigoDestuido)
                    tiroCerteiro=umTiro
                    break
        if tiroCerteiro:
            listaBombas.remove(tiroCerteiro)
    return listaBombas,listaInimigos

def detectaColisao():
    global rodando, acabou
    if listaInimigos:
        for umInimigo in listaInimigos:
            if heroiRec.colliderect(umInimigo):
                rodando=False
                acabou=True
                break

def movimentaInimigo(listaInimigos):
    velocidade=velocidadeInimigo
    global invasores
    qi= len(listaInimigos)
    if listaInimigos:
        for umInimigo in listaInimigos:
            umInimigo.left -= velocidade
            if umInimigo.bottom < chao:
                tela.blit(helisImg,umInimigo)
            else:
                tela.blit(tanqueImg, umInimigo)
        listaInimigos = [rec for rec in listaInimigos if rec.left > -100]
        qf=len(listaInimigos)
        dif=qi-qf
        if dif > 0:
            invasores += dif
        return listaInimigos
    return []

def estadoInicial():
    global pontos,listaTiros,listaBombas,rodando,listaInimigos,acabou,invasores,velocidadeInimigo,listaEsplosoes
    acabou=False
    pontos=0
    invasores=0
    velocidadeInimigo=3
    rodando=True
    heroiRec.midleft=(0,300)
    listaTiros=[]
    listaBombas=[]
    listaInimigos=[]
    listaEsplosoes=[]
    somAviao.play(loops=-1)
    somAviao.set_volume(0.1)

def esplode(listaEsplosoes):
    global listaTempoEsplosao
    red=0.01
    if listaEsplosoes:
        for i in range(len(listaEsplosoes)):
            uma=listaEsplosoes[i]
            if listaTempoEsplosao[i] > 0:
                listaTempoEsplosao[i]-=red
                tela.blit(esploImg,uma)



## inicio
pg.init()
clock=pg.time.Clock()
somFundo=pg.mixer.Sound('sons/music.wav')
#pg.mixer.Channel(0).play(somFundo)
somFundo.play(loops=-1)
somFundo.set_volume(0.2)

chao=600
teto=100

#tela principal
tela=pg.display.set_mode((800,700))
pg.display.set_caption('Desert Power')

#Heroi
heroi1=pg.image.load('imagens/heroi1.png')
heroi2=pg.image.load('imagens/heroi2.png')
herois=[heroi1,heroi2]
heroiInd=1
heroiImg=herois[heroiInd]
heroiRec=heroiImg.get_rect(midleft=(0,300))
somAviao=pg.mixer.Sound('sons/voando.wav')


#INIMIGOS
heli1=pg.image.load('imagens/heli2.png')
heli2=pg.image.load('imagens/heli3.png')
helis=[heli1,heli2]
helisInd=1
helisImg=helis[helisInd]

tanque1=pg.image.load('imagens/tanque1.png')
tanque2=pg.image.load('imagens/tanque2.png')
tanques=[tanque1,tanque2]
tanqueInd=1
tanqueImg=tanques[tanqueInd]

listaInimigos=[]

#esplosoes
esploImg=pg.image.load('imagens/esplode.png')
listaEsplosoes=[]
listaTempoEsplosao=[]


#armas
tiroImg=pg.image.load('imagens/tiro.png').convert_alpha()
listaTiros=[]
bombaImg=pg.image.load('imagens/bomba.png').convert_alpha()
listaBombas=[]
somMissel=pg.mixer.Sound('sons/missel.mp3')
somMissel.set_volume(0.1)
somBomba=pg.mixer.Sound('sons/bomba.wav')
somBomba.set_volume(0.5)

#Fundo - deserto
areia=pg.image.load('imagens/areia.png')
areia=pg.transform.scale(areia,(800,600))
#Fundo - ceu
ceu=pg.image.load('imagens/ceuNoturno.jpg')
ceu=pg.transform.scale(ceu,(800,600))

pontos=0
invasores=0
velocidadeInimigo=3
#Textos
fontA=pg.font.Font('font/Pixeltype.ttf',60)
textoPontos=fontA.render(f'Score: {pontos}',False,'black')
textoPontoRec=textoPontos.get_rect(center=(400,50))

rodando=False
soltaInimigo = pg.USEREVENT+1
pygame.time.set_timer(soltaInimigo,2000)

aumentaVelocidadeInimigo = pg.USEREVENT+2
pygame.time.set_timer(aumentaVelocidadeInimigo,5000)

acabou=False
ceuRec=ceu.get_rect(topleft=(0,100))

while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            exit()
        if rodando:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    tiroRec = tiroImg.get_rect(midleft=heroiRec.midright)
                    listaTiros.append(tiroRec)
                    somMissel.play()
                    somMissel.set_volume(1)
                if event.key == pg.K_LCTRL:
                    bombaRec = bombaImg.get_rect(midbottom=heroiRec.midbottom)
                    listaBombas.append(bombaRec)
                    somBomba.play()
            if event.type == soltaInimigo:
                if randint (0,3)>0:
                    inimigo = helisImg.get_rect(midleft=(randint(900, 1100), randint(teto+50, chao-100)))
                else:
                    inimigo = tanqueImg.get_rect(midleft=(randint(900, 1100), chao))
                listaInimigos.append(inimigo)
            if event.type==aumentaVelocidadeInimigo:
                velocidadeInimigo +=1
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    estadoInicial()

    if rodando:
        tela.fill('aquamarine')
        pg.draw.rect(tela,'aquamarine4',(0,0,800,100),10)

        #ceuRec.x-=1

        tela.blit(ceu, ceuRec)

        tela.blit(areia,(0,100))

        textoPontos = fontA.render(f'Score: {pontos}', False, 'black')
        tela.blit(textoPontos,textoPontoRec)
        textoInvasores = fontA.render(f'Invasores: {invasores:02d}/05', False, 'black')
        r=textoInvasores.get_rect(bottomright=(800,700))
        tela.blit(textoInvasores,r)

        heroiAnimation()
        movimentoHeroi()
        listaTiros=atirar(listaTiros)
        listaBombas = bombardear(listaBombas)
        tela.blit(heroiImg,heroiRec)

        helisAnimation()
        tanqueAnimation()
        listaInimigos = movimentaInimigo(listaInimigos)

        listaTiros,listaInimigos=tiroDestroiInimigo(listaTiros,listaInimigos)
        listaBombas, listaInimigos = bombaDestroiInimigo(listaBombas, listaInimigos)

        esplode(listaEsplosoes)

        detectaColisao()

        if invasores >= 5:
            acabou=True
            rodando=False

    else:
        tela.fill((94, 128, 162))
        heroiRec.midleft = (0, 300)
        textoBoasVindas=fontA.render('Desert Power',False,'black')
        tela.blit(textoBoasVindas,textoBoasVindas.get_rect(center=(400,100)))
        if acabou:
            textoBoasVindas = fontA.render(f'Score: {pontos}', False, 'black')
        else:
            textoBoasVindas = fontA.render('press Space to run', False, 'black')
        tela.blit(textoBoasVindas, textoBoasVindas.get_rect(center=(400, 500)))

        tela.blit(heroiImg,heroiRec)
        heroiAnimation()


    pg.display.update()
    clock.tick(60)


