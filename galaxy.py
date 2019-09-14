import pygame,sys,os,random
pygame.init()

###### TEMEL AYARLAR #####
width = 960
height = 540

boyut = (width,height)

##########################

level = 1



#Klasorler#
klasor = os.path.dirname(__file__)
resimKlasoru = os.path.join(klasor,"resimler")
sesKlasoru = os.path.join(klasor,"sesler")
###########

#### Patlama Klasoru #####

patlamaKlasoru = os.path.join(klasor,"patlama")
patlamaResimleri = []
for i in range(1,10):
    patlamaResimleri.append("{}.png".format(i))


##########################

#### Carpma Efektleri #####
carpmaEfektleri = ["hefect1.wav","hefect2.wav","hefect3.wav"]



#################  Resimler  #####################################################
background = pygame.image.load(os.path.join(resimKlasoru,"background.png"))
fire = pygame.image.load(os.path.join(resimKlasoru,"fire.png"))
ship = pygame.transform.scale(pygame.image.load(os.path.join(resimKlasoru,"ship.png")),(50,50))

##################################################################################

#################   Muzik ########################################################
pygame.mixer.music.load(os.path.join(sesKlasoru,"starblast.mp3"))
pygame.mixer.music.play()
####################### ##########################################################



#################   Efektler ########################################################
hitEffect = pygame.mixer.Sound(os.path.join(sesKlasoru,"hit.ogg"))
fireEffect = pygame.mixer.Sound(os.path.join(sesKlasoru,"laser1.wav"))
####################### ############################################################


####################### AYARLAR ##########################################################
pencere = pygame.display.set_mode(boyut)

clock = pygame.time.Clock()

font = pygame.font.SysFont("Helvetica",50)

score = 0

asteroidler = ["asteroid.png","asteroid2.png","asteroid3.png","asteroid4.png",
               "asteroid.png", "asteroid2.png", "asteroid3.png", "asteroid4.png",
               "asteroid.png", "asteroid2.png", "asteroid3.png", "asteroid4.png",
               "asteroid.png", "asteroid2.png", "asteroid3.png", "asteroid4.png",
               "asteroidcan.png","asteroidcan.png"]

####################### ################################################################


######   UZAY GEMİSİ   #######

class Parca(pygame.sprite.Sprite):
    def __init__(self,x = width /2,y = height / 2):
        super().__init__()
        self.image = ship.convert()
        self.can = 3
        self.image.set_colorkey((0,0,0))
        #self.image.fill((0,130,255))
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)
        self.rect.x = 0
        self.rect.y = y
        self.kalkan = 100
        self.mermiDelay = 250
        self.sonAtes = pygame.time.get_ticks()
        self.hider_timer = 1500
        self.isHide = False
        self.lastHide = pygame.time.get_ticks()

    def hide(self):
        self.isHide = True
        self.lastHide = pygame.time.get_ticks()
        self.rect.center = (-200,height/2)

    def update(self, *args):
        up,down,right,left,shoot = args

        if self.isHide and pygame.time.get_ticks() - self.lastHide > self.hider_timer:
            self.isHide = False
            self.rect.x = 0
            self.rect.y = height/2


        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y + self.rect.size[1] > height:
            self.rect.y = height - self.rect.size[1]

        if up:
            self.rect.y -= 10
        if down:
            self.rect.y += 10

        if shoot:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.sonAtes > self.mermiDelay:
            self.sonAtes = now
            fireEffect.play()
            fuze = Fuze(self.rect.y)
            all_sprites.add(fuze)
            fuzeler.add(fuze)


######   UZAY GEMİSİ  BİTİŞ #######


##### METEOR ######

class Mermi(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.secim = random.choice(asteroidler)
        asteroid = pygame.image.load(os.path.join(resimKlasoru, self.secim))
        self.image = asteroid.convert()
        self.orijinal_resim = self.image
        self.image.set_colorkey((0,0,0))
        #self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.radius = int( (self.rect.width * 0.70) / 2)
        #pygame.draw.circle(self.image,(255,0,0),self.rect.center,self.radius)

        self.rect.y = random.randrange(height-self.rect.height)
        self.rect.x = random.randrange(width+40,width+100)
        self.speedx = random.randrange(3,10)
        self.speedy = random.randrange(-2,2)

        self.rot = 0
        self.rotateSpeed = random.randrange(-20,20)
        self.lastUpdate = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > 50:
            self.lastUpdate = now
            self.rot = (self.rot + self.rotateSpeed) % 360
            new_image = pygame.transform.rotate(self.orijinal_resim,self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self, *args):
        self.rotate()
        self.rect.x -= self.speedx
        self.rect.y += self.speedy

        if self.rect.right < 0:
            self.rect.y = random.randrange(height - self.rect.height)
            self.rect.x = random.randrange(width + 40, width + 100)
            self.speedx = random.randrange(10,13)
            self.speedy = random.randrange(-3, 3)
            global score
            score += 1

##### METEOR BİTİŞ ######

#### Patlama Sınıfı #####

class Patlama(pygame.sprite.Sprite):
    def __init__(self,meteor,klasor,liste):
        super().__init__()
        self.meteor = meteor
        self.klasor = klasor
        self.liste = liste
        self.sayac = 1
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(klasor,self.liste[self.sayac])),self.meteor.image.get_size())
        self.rect = self.image.get_rect()
        self.rect.center = self.meteor.rect.center
        self.delay = 75
        self.sonDegisim = pygame.time.get_ticks()

    def update(self, *args):
        now = pygame.time.get_ticks()
        if now - self.sonDegisim > self.delay:
            self.sonDegisim = now
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(self.klasor,self.liste[self.sayac])),self.meteor.image.get_size())
            self.rect = self.image.get_rect()
            self.rect.center = self.meteor.rect.center
            self.sayac += 1

        if self.sayac == len(self.liste):
            self.kill()










#########################


##### ATEŞ ETME ######

class Fuze(pygame.sprite.Sprite):
    def __init__(self,parcay):
        super().__init__()
        self.image = fire
        #self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = 30
        self.rect.y = parcay + 20

    def update(self, *args):
        self.rect.x += 8

        if self.rect.left > width:
            self.kill()

##### ATEŞ ETME BİTİŞ ######

sayacSifirlama = True

# GRUPLAR
all_sprites = pygame.sprite.Group()
mermiler = pygame.sprite.Group()
fuzeler = pygame.sprite.Group()

#Mermi Sayısı
for i in range(15):
    mermi = Mermi()
    all_sprites.add(mermi)
    mermiler.add(mermi)





parca1 = Parca()
all_sprites.add(parca1)


## KALKAN GORSEL ##

def kalkanCiz(pencere,x,y,deger):
    if deger < 0:
        deger = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = ( deger /100 ) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(pencere,(255,255,255),outline_rect,3)

    if deger >= 60:
        pygame.draw.rect(pencere,(0,255,0),fill_rect)
    elif deger >= 30 and deger < 60:
        pygame.draw.rect(pencere, (204, 204, 0), fill_rect)
    elif deger < 30:
        pygame.draw.rect(pencere,(255,0,0),fill_rect)

######CAN GORSEL ########

def canCiz(pencere,x,y,can):
    img = pygame.transform.scale(pygame.image.load(os.path.join(resimKlasoru,"canShip.png")),(20,15))
    img_rect = img.get_rect()
    for i in range(can):
        img_rect.x = x + (40*i)
        img_rect.y = y
        pencere.blit(img,img_rect)




#########################


### OYUN LOOP ###
while True:
    pencere.fill((255, 255, 255))
    pencere.blit(background,background.get_rect())
    mermiSayisi = len(mermiler)

    keys = pygame.key.get_pressed()

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()



    up,down,right,left,shoot = keys[pygame.K_UP],keys[pygame.K_DOWN],keys[pygame.K_RIGHT],keys[pygame.K_LEFT],keys[pygame.K_SPACE]
    all_sprites.update(up,down,right,left,shoot)

    fontScore = font.render("Kalan Mermi : {}".format(mermiSayisi),1,(0,0,0))

    all_sprites.draw(pencere)

    pencere.blit(fontScore, (width - fontScore.get_size()[0], height - fontScore.get_size()[1]))

    #### Asteroid ile uzay gemisinin çarpismasi #####
    durum = pygame.sprite.spritecollide(parca1,mermiler,True,collided=pygame.sprite.collide_circle)


    ####Mermiler ile asteroid carpismasi ####
    isHit = pygame.sprite.groupcollide(fuzeler,mermiler,True,True)

    if isHit:
        hitEffect.play()
        for meteorlar in isHit.values():
            for meteor in meteorlar:
                kaboom = Patlama(meteor,patlamaKlasoru,patlamaResimleri)
                all_sprites.add(kaboom)
                if meteor.secim == "asteroidcan.png":
                    if parca1.kalkan + 10 < 100:
                        parca1.kalkan += 10
                    else:
                        parca1.kalkan = 100



    if durum:
        #pygame.mixer.Sound(random.choice(carpmaEfektleri)).play()
        for meteor in durum:
            boom = Patlama(meteor,patlamaKlasoru,patlamaResimleri)
            all_sprites.add(boom)
            parca1.kalkan -= meteor.radius * 3

    kalkanCiz(pencere,5,5,parca1.kalkan)
    canCiz(pencere,5,25,parca1.can)

    if durum or mermiSayisi == 0:
        if parca1.kalkan <= 0:
            pygame.mixer.music.load(os.path.join(sesKlasoru, "explode.mp3"))
            pygame.mixer.music.play()
            parca1.can -=1
            parca1.hide()


            if parca1.can == 0:
                pencere.fill((0, 0, 0))
                pencere.blit(pygame.font.SysFont("Helvetica", 50).render("Game Over", 1, (255, 0, 0)), (300, 350))
                pygame.display.update()
                pygame.time.wait(1000)
                sys.exit()

            parca1.kalkan = 100

        if mermiSayisi == 0:
            if sayacSifirlama:
                bitisDegeri = pygame.time.get_ticks()
                sayacSifirlama = False
                levelYaziFont = pygame.font.SysFont("Helvetica",50)
                yazi = levelYaziFont.render("Level {}".format(level+1),1,(0,255,0))

            pencere.blit(yazi,(10,20))

            if pygame.time.get_ticks() - bitisDegeri > 4000:
                sayacSifirlama = True
                level += 1
                for i in range(level * 15):
                    mermi = Mermi()
                    all_sprites.add(mermi)
                    mermiler.add(mermi)




    pygame.display.update()
