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

def EdmondKarpuv(zacatek, konec, sousedi, kapacity):
	'''
	Edmond-Karpův algoritmus
	Řeší hledání největšího toku v orientovaném ohodnoceném grafu
	'''
	if zacatek == konec:
		print("Zacate a konec jsou stejne vrcholy!")
		return -1
	if zacatek < 0 or zacatek > len(sousedi):
		print("Chyba v zadani pocatecniho bodu!")
		return -1
	if konec < 0 or konec > len(sousedi):
		print("Chyba v zadani koncoveho bodu!")
		return -1

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
			ok = True
		except:
			ok = False
			print("Chyba!")

	return kapacity, sousedi, zacatek, konec

def Goldberguv():
	return "Neimplementováno"





menu = {
		1: "Edmond-Karpův algoritmus",
		2: "Goldbergův algoritmus"
	}
while True:
	for klic in menu.keys():
		print(str(klic) + " --> " + menu[klic])
	
	nazev_souboru = "graf_toku.txt"
	
	vstup = int(input("Vyberte číslo algoritmu: "))
	if vstup == 1:
		kapacity, sousedi, zacatek, konec = nactiGraf(nazev_souboru)
		print("Maximální tok:",EdmondKarpuv(zacatek, konec, sousedi, kapacity))
	elif vstup == 2:
		kapacity, sousedi, zacatek, konec = nactiGraf(nazev_souboru)
		print(Goldberguv())
	else:
		print("Chybný vstup")

	

	
