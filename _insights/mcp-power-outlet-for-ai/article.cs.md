# Zásuvka pro AI: co znamená MCP pro stavebnictví

25. října 2026 · Martin Motlík

## AI, která neotevře váš model

Váš AI asistent umí připravit odpověď na dotaz k projektové dokumentaci, shrnout kapitolu technické specifikace a učesat zápis z porady. Zeptejte se ho ale, který průvlak ve 3. podlaží má nejvyšší využití únosnosti, a začne hádat. Ne proto, že by na to nestačil, ale proto, že do vašeho modelu nemá přístup.

Tahle mezera se zavírá. Model Context Protocol, zkráceně MCP, je otevřený standard, přes který se AI aplikace připojí k softwaru a datům, se kterými inženýři už pracují. Představte si ho jako zásuvku pro AI: jedna standardní zásuvka a každý nástroj, který do ní zapojíte, se stane něčím, s čím AI opravdu umí pracovat.

Na MCP se dívám ze dvou stran. Díky práci pro Dlubal Software jsem v prostředí, kde je MCP už součástí produktu, a zároveň stavím vlastní prototyp pro kontrolu modelů nad formátem IFC. V tomhle článku vysvětluji, co MCP je, k čemu se hodí ve stavebnictví a proč napojit naše nástroje na AI platformy, které inženýři už používají, obvykle dává větší smysl než stavět další chatbot.

## Co je MCP: zásuvka, ne mozek

MCP nedělá AI chytřejší. Dává jí standardní cestu k věcem mimo ni samotnou: k vašim modelům, výpočetním programům a projektovým datům.

Vzpomeňte si na staveništní rozvaděč. Je mu jedno, jestli do něj zapojíte pilu, úhlovou brusku nebo světlo, protože každý nástroj má stejnou zástrčku. Před MCP znamenalo propojení AI s aplikací zvláštní kabeláž pro každou dvojici: pět AI aplikací a dvacet programů dávalo až sto jednorázových integrací. S MCP stačí každému programu jeden server a každé AI aplikaci jeden klient. Dvacet pět dílů místo sta, i když každé spojení pořád potřebuje správné nastavení a oprávnění.

&#91;embedded content: Figure 1 · MCP architecture: hosts, the outlet, servers\]

Každá AI aplikace potřebuje jednoho klienta a každý program jeden server; zbytek zařídí standard uprostřed.

Anthropic uvolnil MCP jako otevřený standard v listopadu 2024. V prosinci 2025 ho předal nadaci [Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation), která spadá pod Linux Foundation a kterou mimo jiné podporují OpenAI, Google, Microsoft a AWS. Dnes s ním pracují ChatGPT, Claude, Gemini, Microsoft Copilot, GitHub Copilot i Cursor.

**Tři role, jednoduše řečeno:**

- **Host:** AI aplikace, do které píšete, třeba ChatGPT, Gemini, Claude nebo vlastní chatbot vaší firmy.
- **Klient:** konektor uvnitř hostitelské aplikace, který drží spojení s jedním serverem.
- **Server:** malý program na straně softwaru, který AI říká, co umí. Svůj server má RFEM, Revit i nástroj pro kontrolu IFC.

**Co server nabízí:**

- **Nástroje** jsou akce, které AI může spustit: zkontrolovat model podle datových požadavků projektu, porovnat dvě verze modelu, spustit výpočet.
- **Zdroje** jsou data, která AI může číst: souhrn modelu, seznam zatěžovacích stavů.
- **Prompty** jsou připravené postupy: „projdi změny mezi verzemi A a B“.

Klíčové je, jak AI nástroje najde. Každý nástroj má popis a strukturovanou definici svých vstupů. Když položíte otázku, AI podle nich vybere nástroj a doplní informace, které nástroj potřebuje. Nikdo napevno neprogramuje, které tlačítko se má stisknout; o tom, které nástroje jsou k dispozici, ale rozhoduje aplikace.

Server může běžet lokálně, přímo vedle vaší desktopové aplikace. Soubor modelu zůstává ve vašem počítači; do AI odcházejí jen odpovědi, které nástroje vrátí. Nebo může běžet vzdáleně přes HTTPS s řádným přihlášením, což se hodí pro cloudové platformy. Jestliže je IFC způsob, jakým model popisuje budovu, pak MCP je způsob, jakým se AI na ten model ptá.

## Proč ho stavebnictví potřebuje: hádání, nebo výpočet

MCP dělá z AI, která sebevědomě hádá, koordinátora, který každý úkol předá nástroji, kterému inženýři už věří. Na tom rozdílu záleží v našem oboru víc než skoro kdekoli jinde.

Univerzální jazykový model předpovídá pravděpodobný text. Požádejte ho o posouzení nosníku a dostanete úhledně naformátovanou, sebejistou odpověď, která může být prostě špatně, protože nic nespočítal. S MCP předává AI práci dál: výpočet jde do výpočetního programu, otázka na model jde do modelu a AI dělá to, v čem je opravdu dobrá. Pochopí otázku, provede kroky ve správném pořadí a vysvětlí výsledek srozumitelně. Pořád ale může zvolit špatný filtr nebo výsledek špatně přečíst, takže samotné spojení odpověď spolehlivou neudělá. Udělá ji ověřitelnou.

MCP není jediný způsob, jak dostat projektové informace do AI, a proto je dobré vědět, kam zapadá. Zkopírovat tabulku výsledků do chatu funguje, ale je to ruční snímek, který zastará ve chvíli, kdy se model změní. Retrieval-augmented generation (RAG) umožňuje AI prohledávat dokumenty, třeba normu, plán realizace BIM (BEP) nebo uživatelskou příručku, a citovat, co v nich najde.

Nejde o technologie, které si konkurují. MCP je spojení; vyhledávání v dokumentech je jen jeden druh nástroje, který můžete připojit. Může být připojené přes MCP server stejně dobře jako nástroj, který se ptá živého modelu nebo spouští kontrolu. Užitečný rozdíl je v tom, co který nástroj umí. Vyhledávání v dokumentech odpoví na „co říká norma?“. Nástroj nad modelem odpoví na „co říká můj model a projde kontrolou?“. Většina vyspělých pracovních postupů ve stavebnictví bude používat obojí.

Integrace na míru, třeba asistent zabudovaný přímo v programu, se k živým datům dostanou také, ale každá z nich propojuje jednu AI s jednou aplikací. Díky MCP lze stejné nástroje znovu použít v jakékoli AI aplikaci, která ho podporuje, v mezích jejího nastavení. AI dokáže přesně to, co nástroje dovolí, nic víc.

Jak to vypadá na skutečném projektu? Tyhle požadavky už dnes zvládnou existující servery:

- **Dotazy na model:** „Najdi všechny požárně odolné dveře ve 2. podlaží bez sady kování a vyber je.“ Oficiální server Autodesku pro Revit umí model prohledat a výsledky vybrat.
- **Výkazy:** „Kolik metrů krychlových betonu je v deskách, podlaží po podlaží?“ Open-source servery to čtou přímo ze souboru IFC, pokud model obsahuje spolehlivé výkazy.
- **Koordinace:** „Které body z minulé koordinační porady jsou pořád otevřené?“ Koordinační platformy jako Revizto už nabízejí MCP servery a komunitní servery se dostanou k připomínkám a dotazům v Autodesk Construction Cloud.
- **Výsledky výpočtu:** „Jaký je maximální průhyb stropních nosníků pro kombinace mezního stavu použitelnosti a vyhoví mezní hodnotě L/360?“ Odpověď přichází z výpočetního programu, ne z paměti AI.

## Proč se napojit na velké AI platformy a nestavět vlastní chatbot

Ať se AI firmy starají o jazyk a stavební software o inženýrství. Každých pár měsíců někdo v našem oboru ohlásí vlastního asistenta. Vlastní chatbot ale neznamená vlastní jazykový model. Většina asistentů na míru běží na stejných komerčních modelech, jen s vlastním rozhraním. Skutečná otázka je, kde budou inženýrské nástroje běžet, a MCP zajistí, že půjdou znovu použít, ať váš tým nakonec zvolí jakékoli rozhraní. Tady je pět důvodů, proč obvykle dává smysl začít s AI platformami, které už váš tým používá.

1. **Dostanete nejschopnější AI modely a ty se dál zlepšují.** Žádná inženýrská firma ani dodavatel stavebního softwaru nemá výzkumné rozpočty jako Anthropic, Google, OpenAI nebo Microsoft. Jak se modely zlepšují, obvykle lépe vybírají nástroje a vysvětlují výsledky. U každého postupu to ale není zaručené, takže po změně AI modelu znovu otestujte, na čem vám záleží.
2. **Inženýři už tam pracují.** Mnoho firem už platí Microsoft 365 Copilot, ChatGPT, Claude nebo Gemini. Nový samostatný chatbot je další aplikace s vlastním přihlášením, kterou po druhém týdnu nikdo neotevře. Pokud AI asistent, za kterého už platíte, podporuje potřebné spojení, objeví se MCP server tam, kde lidé už pracují.
3. **Jednou postavit, zapojit kamkoli.** Stejný server lze znovu použít v Claude, ChatGPT, Gemini, Copilotu i v AI asistentech, které si firma postaví sama. Každá aplikace pořád potřebuje vlastní nastavení spojení a ne každý produkt podporuje každou funkci. Když ale vaše firma změní dodavatele AI, inženýrské nástroje se nemusejí stavět znovu. Standard podporují i přímí konkurenti jako OpenAI, Google a Microsoft.
4. **Nástroje začnou spolupracovat.** V jedné konverzaci se dá dotázat modelu, spustit výpočet, vyplnit tabulku a uložit výsledek do systému pro správu dokumentů. Takový postup napříč nástroji dřív vyžadoval skript na míru pro každý krok.
5. **Vaše know-how zůstává vaše.** Dodavatel si ponechává ověřený řešič, posudky podle norem a datový model. AI platforma k tomu dodává konverzační vrstvu. Odborné znalosti zůstávají konkurenční výhodou, a tak to má být.

Je tu i šestá, nenápadnější výhoda. Velké hostitelské platformy přinášejí firemní infrastrukturu, kterou by malý nástroj pro stavebnictví sám nikdy nepostavil: schvalování konektorů administrátorem, dotaz na povolení před spuštěním nástroje a přihlášení přes standardní protokoly. V Microsoft 365 Copilot a Gemini Enterprise například může IT administrátor zaregistrovat vlastní MCP server jednou pro celou organizaci.

## Tři druhy přístupu

Správná otázka nezní, jestli AI do modelu pustit, ale co v něm smí dělat. O tom rozhoduje vaše firma, ne AI. MCP tu hranici zviditelní, protože každý server přesně deklaruje, jaké nástroje nabízí. Podstatné je, co ty nástroje umějí a jaká oprávnění za nimi stojí, ne nálepka na serveru.

**Čtení.** AI se dotazuje modelů a dat: vypíše požárně odolné dveře v podlaží nebo načte vlastnosti jednoho prvku. Přístup jen pro čtení omezuje změny v modelu. Informace tím ale nejsou méně citlivé a zavádějící odpovědi to nezabrání.

**Kontrola.** AI spouští kontroly: validaci podle IDS, zprávu o kolizích, porovnání revizí. IDS je standard buildingSMART, který vybrané informační požadavky zapisuje ve strojově kontrolovatelné podobě. Určíte, které prvky potřebují která data, a kontrolní nástroj podle těchto pravidel model otestuje. Kontroluje informace, ne to, zda je budova správně navržená. Zjištění slouží jako podklad pro rozhodnutí, a proto je kontroluje člověk.

**Zápis.** AI mění samotný model: doplňuje parametry, přesouvá prvky nebo vytváří nové. To vyžaduje řízená oprávnění, kontrolu každé změny a možnost ji vrátit.

Servery Autodesku pro Revit ukazují, jak dodavatelé tyto hranice vymezují. První [MCP server pro Revit](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/), vydaný v červnu jako zkušební verze (technical preview), byl jen pro čtení. V září Autodesk [přidal](https://forums.autodesk.com/t5/revit-mep-forum/revit-mcp-server-tech-preview-launch/td-p/14262011) server Trusted-Write, u kterého zkontrolujete každou změnu, kterou agent udělá, a server Experimental s širšími editačními nástroji, jehož použití je podle Autodesku na vlastní riziko. Oba jsou zkušební verze pro Revit 2027. Pro většinu firem je správné začít čtením, a to na testovacím modelu, který firma schválila.

## Co jsem postavil: šest nástrojů

Abych zjistil, jak vysoká ta bariéra doopravdy je, postavil jsem MCP server jen pro čtení pro prototyp kontroly modelů, který vyvíjím. Prototyp už kontroluje modely IFC podle požadavků IDS a porovnává verze modelu. Samotná validace nová není; kontrolní nástroj prototypu ji uměl už předtím. Server přidává možnost klást doplňující otázky, propojit jednotlivé kroky a skočit rovnou na dotčené prvky.

*\[Figure 2: Code card. One complete MCP tool in about ten lines of Python.\]*

Server se jmenuje `ifc-review` a nabízí šest nástrojů, všechny jen pro čtení:

- `get_model_summary`: projekt, verze, podlaží, počty prvků
- `list_elements`: hledání prvků podle třídy IFC, podlaží nebo příznaku nosnosti
- `get_properties`: sady vlastností, výkazy a materiály jednoho prvku
- `run_ids_check`: validace verze podle souboru IDS
- `compare_versions`: co přibylo, ubylo nebo se změnilo mezi dvěma verzemi
- `get_viewer_link`: odkaz, který otevře 3D prohlížeč se zvýrazněnými příslušnými prvky

*\[Figure 3: The tool list as ChatGPT shows it, with the descriptions the AI reads.\]*

Pak jsem test spustil na skutečném modelu: koncepčním modelu bytového domu v Praze s garáží v úrovni ulice, třemi obytnými podlažími a podkrovím, kontrolovaném podle souboru IDS se 14 informačními požadavky. Zeptal jsem se, které požadavky neprošly a kterých prvků se to týká. Neprošly dva požadavky a týkaly se 13 prvků: dvě střešní okna bez součinitele prostupu tepla a jedenáct dveří bez požární odolnosti. Podle názvů dveří měla být požární odolnost stanovena v požárně bezpečnostním řešení. To vysvětluje, proč hodnota chybí. Hodnotu to ale nedoplní a o tom, zda je v této fázi povinná, rozhoduje projektový tým.

Pro test jsem pak připravil druhou revizi, ve které byla část chybějících údajů doplněná, a položil otázku, kterou si po revizi klade každý tým: co se opravilo a co pořád chybí? AI zavolala nástroje pro porovnání a validaci a výsledky se spárovaly podle ID prvků. Opraveno bylo deset ze třinácti prvků. Troje dveře ve 3. obytném podlaží pořád neměly požární odolnost. Pak mi AI dala odkaz, který otevřel model se zvýrazněnými právě těmi trojími dveřmi.

*\[Figure 4: Main figure. The answer in chat on the left, the same three doors highlighted in the model on the right.\]*

*\[Figure 5: The tool call expanded: what the AI sent to the server and what came back.\]*

Celé demo jsem spustil ve dvou různých AI aplikacích: v ChatGPT a v Gemini v Google Antigravity. V tomto testu došly obě se stejným serverem a stejnými nástroji ke stejným zjištěním. To neznamená, že se každá AI aplikace připojuje stejně; každý produkt má vlastní nastavení a omezení. Server ale nepotřeboval vědět, která AI se ptá. Přesně o tom standard je.

*\[Figure 6: ChatGPT and Gemini in Antigravity side by side, one server.\]*

Napsat kód bylo to nejjednodušší. Víc záleželo na třech věcech:

- **Popisy nástrojů jsou uživatelské rozhraní.** AI vybírá nástroje podle toho, co si o nich přečte, takže si popisy zaslouží stejnou péči jako popisky tlačítek.
- **Souhrny jsou lepší než výpisy dat.** Vracejte počty a nejdůležitější výsledky, podrobnosti až na vyžádání. Když AI pošlete celý model, zahltíte její pracovní paměť a odpovědi se zhorší.
- **Jednotky a ID, vždycky.** Každé číslo nese svou jednotku a každý prvek svůj GUID. Kde je nejasnost, tam AI začne znovu hádat.

Nic z toho nenahrazuje kontrolní nástroj. Jen se ho dá snáz ptát.

## Kde obor stojí

Za necelé dva roky se MCP změnil z experimentu ve funkci, kterou velcí výrobci stavebního softwaru dodávají se svými produkty.

Anthropic standard uvolnil v listopadu 2024. Od té doby začali dodavatelé stavebního softwaru nabízet MCP propojení, každé s vlastním rozsahem a podmínkami:

- **Revit (Autodesk):** [MCP server](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/) jen pro čtení od června, ke kterému v září přibyly [servery Trusted-Write a Experimental](https://forums.autodesk.com/t5/revit-mep-forum/revit-mcp-server-tech-preview-launch/td-p/14262011). Všechny jsou zkušební verze pro Revit 2027.
- **Revu (Bluebeam):** [připojuje se ke Claude přes MCP](https://support.bluebeam.com/revu/how-to/mcp-claude.html). Vyžaduje tarif Bluebeam Max, Revu 21.9 nebo novější a desktopovou aplikaci Claude.
- **SketchUp (Trimble):** [konektor pro Claude](https://help.sketchup.com/en/sketchup-claude-connector), který z konverzace vytváří nové modely SketchUp. Existující soubory upravovat neumí a jediným podporovaným poskytovatelem AI je zatím Claude.
- **RFEM 6 (Dlubal Software):** MCP server je od ledna 2026 součástí standardní instalace a pracuje přes Dlubal API. Podrobnosti najdete v [článku znalostní báze](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/002032) a v [dokumentaci API](https://apidocs.dlubal.com/installation_mcp.html) Dlubalu.

Tyto produkty se rychle mění, takže si před plánováním ověřte aktuální podmínky a nepředpokládejte, že se kterýkoli z nich rovnou připojí ke každé AI aplikaci.

Dodavatelé se také rozhodují pro různá řešení. Některé servery nabízejí několik úzce zaměřených nástrojů. Jiné nechávají AI psát skripty nad API programu, podobně jako skript v Dynamu nebo Grasshopperu, jen ho píše AI. Dosah závisí na tom, co server zpřístupní a jaká oprávnění za ním stojí. Úzce zaměřené nástroje dávají všem bezpečné výchozí nastavení; skriptování dává pokročilým uživatelům větší dosah za cenu kontroly a testování kódu, který AI napíše. Můj vlastní server jednoznačně patří k těm úzce zaměřeným.

Dlouho běžící úlohy, jako rozsáhlý výpočet nebo náročná kontrola modelu, mají v MCP vlastní mechanismus: Tasks. Tasks začínaly jako experimentální funkce a [specifikace z července 2026](https://modelcontextprotocol.io/specification/2026-07-28/changelog) je přesunula do oficiálního rozšíření. Pomohou jen tehdy, když je implementuje AI aplikace i server.

## Co MCP nevyřeší

MCP odstraňuje tření mezi inženýrským úsudkem a jeho provedením. Úsudek nenahrazuje a přináší i pár vlastních nových rizik.

- **Odpovědnost zůstává, kde byla.** Použití AI inženýra nezbavuje povinnosti výsledek zkontrolovat. AI výkresy nerazítkuje. Jak se rozdělí odpovědnost, je otázka pro vaše smlouvy a právní poradce.
- **Co do systému vložíte, to z něj dostanete, jen rychleji.** MCP automatizuje chaotický proces stejně věrně jako uspořádaný. Nejednotné parametry a chybějící klasifikační kódy (UniFormat, OmniClass) vyplavou na povrch dřív, ale nezmizí.
- **Kód napsaný AI je potřeba zkontrolovat.** Když server spouští skripty, které píše AI, může AI napsat i chybný skript. Kód zkontrolujte, otestujte na kopii modelu a výsledky výpočtů držte ve správě verzí.
- **Mějte přehled, kam data odcházejí.** Lokální server drží model ve vašem počítači, ale AI host pořád vidí vše, co nástroje vrátí, a přístup jen pro čtení na tom nic nemění. Než připojíte živé projekty, ověřte si podmínky uchovávání dat a jejich využití k trénování u svého poskytovatele AI.
- **Data modelu mohou nést pokyny.** Hodnota vlastnosti nebo komentář v dokumentu může obsahovat text, který se snaží AI navést. Přístup jen pro čtení omezuje změny v modelu; nezabrání zavádějícím odpovědím ani úniku dat. Začněte s důvěryhodným serverem, omezeným přístupem a testovacím modelem, který vaše firma schválila.
- **Není to zadarmo.** Počítejte s předplatným AI, přístupem k API nebo doplňkovými licencemi na straně softwaru a s dostatečně výkonnými pracovními stanicemi.

## Jak začít v pondělí

Začněte v malém: jeden projekt, jedna úloha jen pro čtení, jeden zvědavý člověk. Předtím položte svým dodavatelům softwaru pět otázek:

1. Dodáváte MCP server a je oficiální, nebo ho vytvořila komunita?
2. Je jen pro čtení, nebo může model měnit? Jsou čtení a zápis oddělené?
3. Běží lokálně, nebo v cloudu, a kam odcházejí projektová data?
4. S jakými AI aplikacemi jste ho testovali?
5. Jak se licencuje a účtuje?

Pak spusťte pilotní projekt. Vyberte jednu opakující se úlohu, třeba kontrolu revize modelu podle informačních požadavků projektu, a testovací model, který vaše firma schválila. Porovnejte svůj současný postup, včetně kontrolního nástroje, který už používáte, s verzí s podporou AI. Kromě ušetřeného času započítejte i čas strávený kontrolou, přehlédnuté problémy a falešné poplachy. Před rozhodnutím srovnání zopakujte na další revizi. Takové srovnání vám řekne víc než jakékoli demo dodavatele.

## Most, ne náhrada

MCP budovu nenavrhne. Umožní ale AI dosáhnout na nástroje, které inženýrskou práci už dělají, takže se zkrátí čas mezi otázkou a odpovědí.

Představte si další krok. Jedna zásuvka najde prvky, které se v poslední revizi modelu změnily. Druhá je předá dalšímu nástroji, třeba výpočetnímu programu nebo koordinační platformě, pokud jsou modely a ID jejich prvků propojené, což je pořád jedna z nejtěžších částí práce. AI propojí jednotlivé kroky a výsledek předloží člověku, který rozhoduje. Jednotlivé díly už dnes existují; každý krok ale pořád potřebuje někoho, kdo výsledek zkontroluje.

Stavební software, na který spoléháme, vyniká v inženýrských výpočtech. AI platformy vynikají v práci s jazykem a v uvažování. MCP je zásuvka mezi nimi a vyplatí se pochopit, jak funguje, dřív než vaše konkurence.

Můj pohled: sdílení stavebních dat s modely AI je cesta, jak se modely v naší práci zlepší, a velkým americkým poskytovatelům je svěřuji bez obav. Jaká pravidla pro projekt platí, ale dál určují vaše smlouvy. Za pár let bude dotaz na model přes AI stejně běžný jako hledání na Googlu.

Raději posloucháte? K tomuto článku patří díl podcastu Insights (v angličtině), který vychází ze stejného testu.

## Zdroje
