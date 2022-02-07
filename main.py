from timeit import default_timer as timer

def EdmondKarpuv(zacatek, konec, sousedi, kapacity):
	'''
	Edmond-Karpův algoritmus
	Řeší hledání největšího toku v orientovaném ohodnoceném grafu
	'''
	
	def BFS(zacatek, konec, sousedi, kapacity, odtoky):
		'''
		BFS algoritmus na procházení grafu přes vrcholy.
		Hledám nejkratší cestu přes vrcholy, kterým ještě zbývá kapacita.
		Každá cesta je využitá co nejvíc to jednotlivé části dovolí - tok přes cestu nikdy nemůže být víc něž nejmenší tok někde na cestě.
		'''
		fronta = [zacatek]							#algoritmus BFS na prochazeni grafu
		cesty = {zacatek:[]}						#pro kazdy vrchol si ulozim jak se k nemu co nejkratsi cestou dostat

		while len(fronta) > 0:
			vrchol = fronta.pop(0)
			for soused in sousedi[vrchol]:
				#pro kazdeho souseda vrcholu
				#pokud zbyva nejaky volny tok od vrcholu do souseda a zaroven jsem souseda jeste nenavstivil
				if (kapacity[vrchol][soused] - odtoky[vrchol][soused]) > 0 and soused not in cesty:
					#ulozim si, ze cesta do souseda vede pres vrchol
					cesty[soused] = cesty[vrchol] + [(vrchol, soused)]
					
					#koncim az najdu konec, jinak pokracuji pridanim souseda do fronty
					if soused == konec:
							return cesty[soused]
					else:
						fronta.append(soused)
		
		return None

	odtoky = [[0 for i in range(len(sousedi))] for j in range(len(sousedi))]
	#vytvorim si pole poli o velikosti pocet vrcholu * pocet vrcholu, ve kterem si uchovavam pro kazdy vrchol kolik kam odtece do jinych vrcholu

	#v promenne nalezena cesta mam nalezenou cestu od vrcholu zacatek do vrcholu konec
	nalezena_cesta = []
	while True:
		nalezena_cesta = BFS(zacatek, konec, sousedi, kapacity, odtoky)
		if nalezena_cesta == None:
			break
		
		tok = min(kapacity[vrchol][soused] - odtoky[vrchol][soused] for (vrchol, soused) in nalezena_cesta)
		#spocitam si kolik max muze protect - nejmensi prutok mezi kazdym vrcholem --> sousedem
		#ulozim si prutok pres jednotlive vrcholy 
		for (vrchol, soused) in nalezena_cesta:
			odtoky[vrchol][soused] += tok

	
	return sum(odtoky[zacatek][i] for i in range(len(sousedi)))

def Goldberguv(graf, zacatek, konec, sousedi):
	def zvedni_vrchol(a):
		'''
		Funkce na zvedani vrcholu
		'''
		for b in sousedi[a]:
			if graf[a][b] - pouzita_kapacita[a][b] > 0:
				mensi = min(vyska[a], vyska[b])
				vyska[a] = mensi + 1

	def vyprazdni(a):
		'''
		Funkce na odstaneni a premisteni prebytku
		'''
		while prebytek[a] > 0:
			if vyzkousen[a] < N:
				b = vyzkousen[a]
				if vyska[a] > vyska[b] and graf[a][b] - pouzita_kapacita[a][b] > 0:		#existuje soused, kteremu muzu premistit prebytek, tak to zkusim
					posli = min(prebytek[a], graf[a][b] - pouzita_kapacita[a][b])
		
					pouzita_kapacita[a][b] += posli
					prebytek[a] -= posli
		
					pouzita_kapacita[b][a] -= posli
					prebytek[b] += posli
				else:
					vyzkousen[a] += 1
			else:																		#pokud takovy soused neni, zvedam vrchol
				zvedni_vrchol(a)
				vyzkousen[a] = 0
		
	
	N = len(graf)
	pouzita_kapacita = [[0] * N for _ in range(N)]					#2D pole na ulozeni uz pouzite kapacity u kazdeho vrcholu od vsech ostatnich

	vyska = [0] * N						#pole na ulozeni vysek jednotlivych vrcholu
	vyska[zacatek] = N					#zacatek ve vysce N, ostatni ve vysce 0

	prebytek = [0] * N					#vytvorime pocatecni vlnu - vsechny hrany ze zacatku na maximum, ostatni na 0 
	prebytek[zacatek] = float('inf')	#jednoduchy zpusob zapsani maxima
	for vrchol in sousedi[zacatek]:
		posli = min(prebytek[zacatek], graf[zacatek][vrchol] - pouzita_kapacita[zacatek][vrchol])		#zkousim premistit prebytek na vsechny vrcholy spojene s "zacatecnim" vrcholem
		
		pouzita_kapacita[zacatek][vrchol] += posli
		prebytek[zacatek] -= posli
		
		pouzita_kapacita[vrchol][zacatek] -= posli
		prebytek[vrchol] += posli

	vyzkousen = [0] * N				#pole, kde si ukladam kolik vrcholu jsem uz vyzkousel pro kazdy vrchol I na indexu I
	seznam_vrcholu   = [i for i in range(N) if i != zacatek and i != konec]			#seznam vrcholu, ktere musime prochazet - zacatek a konec neprochazime
	

	i = 0
	while i < N-2:						#prochazime seznam vrcholu
		vrchol = seznam_vrcholu[i]
		vyska_pred = vyska[vrchol]
		vyprazdni(vrchol)				#odstranim prebytek vrcholu

		if vyska[vrchol] > vyska_pred:							#vyska se zmenila - je potreba zacit prochazet seznam od zacatku
			seznam_vrcholu.insert(0, seznam_vrcholu.pop(i))
			i = 0
		i += 1													#jinak pokracuji dal

	return -sum([pouzita_kapacita[konec][i] for i in range(N)])

def nactiGraf(nazev_souboru):
	'''
	Funkce na načtení grafu.

	Vstup - název souboru, kde je graf reprezentovan pomocí matice sousednosti s hodnocením.

	Výstup - seznam kapacity, kde pro vrchol i na indexu i je seznam délky počtu všech vrcholů, na každém indexu je maximální kapacita průtoku od vrcholu i do daného vrcholu. Dále slovník sousedů, kde pro každý vrchol reprezentovaný jako klíč je uložen seznam všech jeho sousedů.
	'''
	with open(nazev_souboru, "r") as f:
		kapacity = []
		sousedi = {}

		for radek in f.readlines():
			kapacity.append([int(i) for i in radek.split(",")])
		
		for vrchol in range(len(kapacity)):
			sousedi[vrchol] = []
		
		pomocna = 0
		for vrchol_hrany in kapacity:
			for i in range(len(vrchol_hrany)):
				if vrchol_hrany[i] > 0:
					sousedi[pomocna].append(i)
					sousedi[i].append(pomocna)
			pomocna += 1
	
	ok = False
	while ok != True:
		try:

			zacatek = int(input("Číslo počátečního bodu: "))
			konec = int(input("Číslo koncového bodu: "))
			
			if zacatek == konec:
				print("Začátek a konec jsou stejné vrcholy!")
			elif zacatek < 0 or zacatek >= len(sousedi):
				print("Chyba v zadáni počátečního bodu!")
			elif konec < 0 or konec >= len(sousedi):
				print("Chyba v zadání koncového bodu!")
			else:
				ok = True

		except:
			ok = False
			print("Chyba v zadávání!")

	return kapacity, sousedi, zacatek, konec

menu = {
		1: "Edmond-Karpův algoritmus",
		2: "Goldbergův algoritmus",
		3: "Rozdíl v době běhu"
	}
while True:
	for klic in menu.keys():
		print(str(klic) + " --> " + menu[klic])
	
	nazev_souboru = "graf_toku.txt"
	
	vstup = int(input("Vyberte číslo algoritmu: "))
	if vstup == 1:
		kapacity, sousedi, zacatek, konec = nactiGraf(nazev_souboru)
		print("Maximální tok:", EdmondKarpuv(zacatek, konec, sousedi, kapacity))
	elif vstup == 2:
		kapacity, sousedi, zacatek, konec = nactiGraf(nazev_souboru)
		print("Maximální tok: ", Goldberguv(kapacity, zacatek, konec, sousedi))
	elif vstup == 3:
		kapacity, sousedi, zacatek, konec = nactiGraf(nazev_souboru)
		
		zacatek1 = timer()
		vysledek1 = EdmondKarpuv(zacatek, konec, sousedi, kapacity)
		konec1 = timer()

		zacatek2 = timer()
		vysledek2 = Goldberguv(kapacity, zacatek, konec, sousedi)
		konec2 = timer()

		if vysledek1 == vysledek2:
			print("Doba běhu 1: ", (konec1 - zacatek1))
			print("Doba běhu 2: ", (konec2 - zacatek2))
		else:
			print("Rozdílný výsledek v max toku !!!")

	else:
		print("Chybný vstup")