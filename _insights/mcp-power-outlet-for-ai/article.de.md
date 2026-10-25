# Eine Steckdose für KI: Was MCP für AEC bedeutet

22. Oktober 2026 · Martin Motlík

## Die KI, die Ihr Modell nicht öffnen kann

Ihr KI-Assistent entwirft die Antwort auf eine RFI, fasst einen Abschnitt der Leistungsbeschreibung zusammen und bringt das Besprechungsprotokoll in Form. Fragen Sie ihn aber, welcher Unterzug im 3. Geschoss die höchste Ausnutzung hat, und er rät. Nicht, weil er nicht klug genug wäre, sondern weil er keinen Zugang zu Ihrem Modell hat.

Diese Lücke schließt sich. Model Context Protocol, kurz MCP, ist ein offener Standard, über den sich KI-Anwendungen mit der Software und den Daten verbinden, mit denen Ingenieure ohnehin arbeiten. Stellen Sie es sich als Steckdose für KI vor: eine genormte Steckdose, und jedes Werkzeug, das Sie einstecken, wird zu etwas, mit dem die KI tatsächlich arbeiten kann.

Ich betrachte das Thema von zwei Seiten. Durch meine Arbeit für Dlubal Software bin ich in einem Umfeld, in dem MCP bereits Teil des Produkts ist, und ich entwickle einen eigenen Prototyp für die Modellprüfung auf Basis von IFC. Dieser Beitrag erklärt, was MCP ist, wofür es im AEC-Bereich taugt und warum es meist sinnvoller ist, unsere Werkzeuge mit den KI-Plattformen zu verbinden, die Ingenieure bereits nutzen, als noch einen weiteren Chatbot zu bauen.

## Was MCP ist: eine Steckdose, kein Gehirn

MCP macht KI nicht klüger. Es gibt der KI einen genormten Weg zu Dingen außerhalb ihrer selbst: zu Ihren Modellen, Ihren Berechnungsprogrammen, Ihren Projektdaten.

Denken Sie an den Baustromverteiler auf der Baustelle. Ihm ist es egal, ob Sie eine Säge, einen Winkelschleifer oder einen Strahler einstecken, denn jedes Werkzeug hat denselben Stecker. Vor MCP bedeutete die Anbindung einer KI an eine Anwendung eine eigene Verkabelung für jedes Paar: Fünf KI-Apps und zwanzig Programme ergaben bis zu hundert einzelne Integrationen. Mit MCP baut jedes Programm einen Server und jede KI-App einen Client. Fünfundzwanzig Teile statt hundert, auch wenn jede Verbindung weiterhin die richtige Einrichtung und Berechtigungen braucht.

&#91;embedded content: Figure 1 · MCP architecture: hosts, the outlet, servers\]

Jede KI-Anwendung braucht einen Client und jedes Programm einen Server; den Rest erledigt der Standard in der Mitte.

Anthropic hat MCP im November 2024 als offenen Standard veröffentlicht. Im Dezember 2025 übergab das Unternehmen den Standard an die [Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) unter dem Dach der Linux Foundation, die unter anderem von OpenAI, Google, Microsoft und AWS getragen wird. Heute unterstützen ihn ChatGPT, Claude, Gemini, Microsoft Copilot, GitHub Copilot und Cursor.

**Drei Rollen, einfach erklärt:**

- **Host:** die KI-Anwendung, in die Sie tippen, etwa ChatGPT, Gemini, Claude oder der eigene Chatbot Ihres Unternehmens.
- **Client:** der Konnektor im Host, der die Verbindung zu einem Server hält.
- **Server:** ein kleines Programm auf der Seite der Software, das der KI sagt, was es kann. RFEM, Revit oder ein Werkzeug zur IFC-Prüfung bekommen jeweils ihren eigenen.

**Was ein Server anbietet:**

- **Tools** sind Aktionen, die die KI aufrufen kann: ein Modell gegen die Datenanforderungen des Projekts prüfen, zwei Modellversionen vergleichen, eine Berechnung starten.
- **Resources** sind Daten, die die KI lesen kann: eine Modellübersicht, eine Liste der Lastfälle.
- **Prompts** sind vorbereitete Abläufe: „Prüfe die Änderungen zwischen Version A und B.“

Entscheidend ist, wie die KI die Werkzeuge findet. Jedes Werkzeug bringt eine Beschreibung und eine strukturierte Definition seiner Eingaben mit. Wenn Sie eine Frage stellen, wählt die KI anhand dieser Angaben ein Werkzeug und liefert die Informationen, die es braucht. Niemand programmiert fest, welcher Knopf gedrückt wird, aber welche Werkzeuge verfügbar sind, entscheidet die Anwendung.

Ein Server kann lokal laufen, direkt neben Ihrer Desktop-Anwendung. Die Modelldatei bleibt auf Ihrem Rechner; an die KI gehen nur die Antworten, die die Werkzeuge zurückgeben. Oder er läuft entfernt über HTTPS mit einer ordentlichen Anmeldung, was zu Cloud-Plattformen passt. Wenn IFC die Art ist, wie ein Modell ein Gebäude beschreibt, dann ist MCP die Art, wie eine KI diesem Modell Fragen stellt.

## Warum AEC es braucht: raten oder rechnen

MCP macht aus der KI statt eines selbstbewussten Ratenden einen Koordinator, der jede Aufgabe an ein Werkzeug übergibt, dem Ingenieure bereits vertrauen. Dieser Unterschied zählt in unserer Branche mehr als fast überall sonst.

Ein universelles Sprachmodell sagt plausiblen Text voraus. Bitten Sie es, einen Träger nachzuweisen, und Sie bekommen eine sauber formatierte, selbstsichere Antwort, die schlicht falsch sein kann, weil nie gerechnet wurde. Mit MCP delegiert die KI: Die Berechnung geht an das Berechnungsprogramm, die Frage zum Modell geht an das Modell, und die KI macht, was sie wirklich gut kann. Sie versteht die Frage, führt die Schritte in der richtigen Reihenfolge aus und erklärt das Ergebnis verständlich. Sie kann trotzdem den falschen Filter wählen oder ein Ergebnis falsch lesen, deshalb macht die Verbindung allein eine Antwort nicht zuverlässig. Sie macht sie überprüfbar.

MCP ist nicht der einzige Weg, Projektinformationen in eine KI zu bringen, deshalb hilft es zu sehen, wo es hingehört. Eine Ergebnistabelle in den Chat zu kopieren funktioniert, ist aber eine manuelle Momentaufnahme, die veraltet, sobald sich das Modell ändert. Retrieval-augmented Generation (RAG) lässt die KI Dokumente durchsuchen, etwa eine Norm, einen BIM-Abwicklungsplan oder ein Produkthandbuch, und zitieren, was sie findet.

Das sind keine konkurrierenden Technologien. MCP ist die Verbindung; eine Dokumentensuche ist eine Art von Werkzeug, die Sie anschließen können. Sie kann genauso hinter einem MCP-Server sitzen wie ein Werkzeug, das ein laufendes Modell abfragt oder eine Prüfung startet. Der nützliche Unterschied liegt darin, was das jeweilige Werkzeug kann. Eine Dokumentensuche beantwortet „Was steht in der Norm?“. Ein Modellwerkzeug beantwortet „Was sagt mein Modell, und ist es in Ordnung?“. Die meisten ernsthaften Abläufe im AEC-Bereich werden beides nutzen.

Individuelle Integrationen, etwa ein im Programm eingebauter Assistent, erreichen ebenfalls Live-Daten, aber jede verbindet genau eine KI mit genau einer Anwendung. MCP macht dieselben Werkzeuge in jeder KI-App wiederverwendbar, die es unterstützt, im Rahmen der Einrichtung der jeweiligen App. Die KI kann genau das, was die Werkzeuge erlauben, nicht mehr.

Wie sieht das in einem echten Projekt aus? Diese Anfragen sind mit heute verfügbaren Servern bereits möglich:

- **Modellabfragen:** „Finde alle Feuerschutztüren im 2. Geschoss ohne Beschlagsatz und wähle sie aus.“ Der offizielle Revit-Server von Autodesk kann das Modell durchsuchen und die Ergebnisse auswählen.
- **Mengen:** „Wie viele Kubikmeter Beton stecken in den Decken, Geschoss für Geschoss?“ Open-Source-Server lesen das direkt aus einer IFC-Datei, sofern das Modell verlässliche Mengen enthält.
- **Koordination:** „Welche Punkte aus der Koordinationsbesprechung der letzten Woche sind noch offen?“ Koordinationsplattformen wie Revizto bieten inzwischen MCP-Server an, und Community-Server erreichen Issues und RFIs in Autodesk Construction Cloud.
- **Berechnungsergebnisse:** „Wie groß ist die maximale Durchbiegung der Deckenträger unter den Kombinationen im Grenzzustand der Gebrauchstauglichkeit, und liegt sie innerhalb von L/360?“ Die Antwort kommt aus dem Berechnungsprogramm, nicht aus dem Gedächtnis der KI.

## Warum an die großen KI-Plattformen andocken, statt einen eigenen Chatbot zu bauen

Die KI-Firmen sollen sich um Sprache kümmern, die AEC-Software um das Ingenieurwesen. Alle paar Monate kündigt jemand in unserer Branche einen eigenen Assistenten an. Ein eigener Chatbot bedeutet aber kein eigenes Sprachmodell. Die meisten maßgeschneiderten Assistenten laufen auf denselben kommerziellen Modellen, nur hinter einer eigenen Oberfläche. Die eigentliche Frage ist, wo die Ingenieurwerkzeuge leben, und MCP hält sie wiederverwendbar, ganz gleich, welche Oberfläche Ihr Team am Ende nutzt. Deshalb ist es meist sinnvoll, mit den KI-Plattformen zu beginnen, die Ihr Team bereits nutzt.

1. **Sie bekommen die leistungsfähigsten KI-Modelle, und die werden immer besser.** Kein Ingenieurbüro und kein Anbieter von AEC-Software kann mit den Forschungsbudgets von Anthropic, Google, OpenAI oder Microsoft mithalten. Mit besseren Modellen werden in der Regel auch die Werkzeugauswahl und die Erklärung der Ergebnisse besser. Das geschieht aber nicht bei jedem Ablauf von selbst, testen Sie also erneut, was Ihnen wichtig ist, wenn sich das Modell ändert.
2. **Ingenieure arbeiten schon dort.** Viele Büros zahlen bereits für Microsoft 365 Copilot, ChatGPT, Claude oder Gemini. Ein neuer eigenständiger Chatbot ist ein weiteres Login, das nach der zweiten Woche niemand mehr öffnet. Wenn der Assistent die nötige Verbindung unterstützt, erscheint ein MCP-Server dort, wo die Leute ohnehin arbeiten.
3. **Einmal bauen, überall einstecken.** Derselbe Server lässt sich in Claude, ChatGPT, Gemini, Copilot und in KI-Assistenten wiederverwenden, die ein Büro selbst baut. Jede App braucht weiterhin ihre eigene Einrichtung der Verbindung, und nicht jedes Produkt unterstützt jede Funktion. Wechselt Ihr Büro aber den KI-Anbieter, müssen die Ingenieurwerkzeuge nicht neu gebaut werden. Sogar direkte Konkurrenten wie OpenAI, Google und Microsoft unterstützen den Standard.
4. **Werkzeuge beginnen zusammenzuarbeiten.** In einem Gespräch lässt sich das Modell abfragen, eine Berechnung starten, eine Tabelle füllen und das Ergebnis im Dokumentenmanagement ablegen. Ein solcher werkzeugübergreifender Ablauf brauchte früher für jeden Schritt ein eigenes Skript.
5. **Ihr Fachwissen bleibt Ihres.** Der Anbieter behält den validierten Solver, die Nachweise nach Normen und das Datenmodell. Die KI-Plattform liefert die Gesprächsebene obendrauf. Fachwissen bleibt der Wettbewerbsvorteil, und genau dort gehört es hin.

Es gibt einen sechsten, leiseren Vorteil. Die großen Plattformen bringen eine Unternehmensinfrastruktur mit, die ein kleines AEC-Werkzeug nie selbst bauen würde: Freigabe von Konnektoren durch Administratoren, Rückfragen vor dem Ausführen eines Werkzeugs und Anmeldung über Standardprotokolle. In Microsoft 365 Copilot und Gemini Enterprise kann ein IT-Administrator zum Beispiel einen eigenen MCP-Server einmal für die gesamte Organisation registrieren.

## Drei Arten von Zugriff

Die richtige Frage ist nicht, ob Sie die KI in Ihr Modell lassen, sondern was sie dort tun darf. Das entscheidet Ihr Büro, nicht die KI. MCP macht die Grenze sichtbar, weil jeder Server genau angibt, welche Werkzeuge es gibt. Entscheidend ist, was diese Werkzeuge können und welche Berechtigungen dahinterstehen, nicht das Etikett auf dem Server.

**Lesen.** Die KI fragt Modelle und Daten ab: Sie listet die Feuerschutztüren eines Geschosses auf oder ruft die Eigenschaften eines einzelnen Elements ab. Lesezugriff begrenzt Änderungen am Modell. Er macht die Informationen nicht weniger sensibel, und er verhindert keine irreführende Antwort.

**Prüfen.** Die KI führt Prüfungen aus: eine IDS-Validierung, einen Kollisionsbericht, einen Vergleich zwischen Revisionen. IDS ist ein Standard von buildingSMART, der ausgewählte Informationsanforderungen in maschinenprüfbarer Form beschreibt. Sie legen fest, welche Elemente welche Daten brauchen, und ein Prüfwerkzeug testet das Modell gegen diese Regeln. Es prüft die Informationen, nicht, ob das Gebäude richtig geplant ist. Die Ergebnisse fließen in Entscheidungen ein, deshalb prüft sie ein Mensch.

**Schreiben.** Die KI ändert das Modell selbst: Sie füllt Parameter aus, verschiebt Elemente oder erstellt neue. Das braucht kontrollierte Berechtigungen, eine Prüfung jeder Änderung und eine Möglichkeit, sie rückgängig zu machen.

Die Revit-Server von Autodesk zeigen, wie Anbieter diese Grenzen ziehen. Der erste [MCP-Server für Revit](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/), im Juni als Technical Preview veröffentlicht, war schreibgeschützt. Im September hat Autodesk einen Trusted-Write-Server [ergänzt](https://forums.autodesk.com/t5/revit-mep-forum/revit-mcp-server-tech-preview-launch/td-p/14262011), mit dem Sie jede Änderung eines Agenten prüfen können, sowie einen Experimental-Server mit weitergehenden Bearbeitungswerkzeugen, den Autodesk als Nutzung auf eigenes Risiko beschreibt. Beide sind Technical Previews für Revit 2027. Für die meisten Büros ist Lesen der richtige Einstieg, und zwar an einem Testmodell, das das Büro freigegeben hat.

## Was ich gebaut habe und die sechs Werkzeuge

Um zu sehen, wie hoch die Hürde wirklich ist, habe ich einen schreibgeschützten MCP-Server für den Prototyp zur Modellprüfung gebaut, den ich entwickle. Der Prototyp prüft IFC-Modelle bereits gegen IDS-Anforderungen und vergleicht Modellversionen. Die Validierung selbst ist nicht neu; das Prüfwerkzeug des Prototyps konnte sie schon vorher. Der Server ergänzt die Möglichkeit, Rückfragen zu stellen, die Schritte zu verbinden und direkt zu den betroffenen Elementen zu springen.

*\[Figure 2: Code card. One complete MCP tool in about ten lines of Python.\]*

Der Server heißt `ifc-review` und stellt sechs Werkzeuge bereit, alle schreibgeschützt:

- `get_model_summary`: Projekt, Versionen, Geschosse, Anzahl der Elemente
- `list_elements`: Elemente nach IFC-Klasse, Geschoss oder Tragwerksmerkmal finden
- `get_properties`: Eigenschaftssätze, Mengen und Materialien eines Elements
- `run_ids_check`: eine Version gegen eine IDS-Datei validieren
- `compare_versions`: was zwischen zwei Versionen hinzugekommen, entfernt oder geändert ist
- `get_viewer_link`: ein Link, der den 3D-Viewer mit den betreffenden Elementen hervorgehoben öffnet

*\[Figure 3: The tool list as ChatGPT shows it, with the descriptions the AI reads.\]*

Dann habe ich den Test an einem echten Modell durchgeführt: dem Konzeptmodell eines Wohngebäudes in Prag mit Garage auf Straßenniveau, drei Wohngeschossen und einem Dachgeschoss, geprüft gegen eine IDS-Datei mit 14 Informationsanforderungen. Ich habe gefragt, welche Anforderungen nicht erfüllt sind und welche Elemente betroffen sind. Zwei Anforderungen schlugen fehl, an 13 Elementen: zwei Dachfenster ohne Wärmedurchgangswert und elf Türen ohne Feuerwiderstandsklasse. Laut den Türbezeichnungen sollte die Feuerwiderstandsklasse im Brandschutzkonzept festgelegt werden. Das erklärt, warum der Wert fehlt. Es liefert ihn aber nicht, und ob der Wert in dieser Phase erforderlich ist, entscheidet das Projektteam.

Für den Test habe ich dann eine zweite Revision vorbereitet, in der ein Teil der Lücken gefüllt war, und die Frage gestellt, die jedes Team nach einer Revision stellt: Was wurde behoben, und was fehlt noch? Die KI rief die Vergleichs- und Validierungswerkzeuge auf, und die Ergebnisse wurden über die Element-ID abgeglichen. Zehn der dreizehn Elemente waren behoben. Drei Türen im 3. Wohngeschoss hatten weiterhin keine Feuerwiderstandsklasse. Dann gab mir die KI einen Link, der das Modell mit genau diesen drei Türen hervorgehoben öffnete.

*\[Figure 4: Main figure. The answer in chat on the left, the same three doors highlighted in the model on the right.\]*

*\[Figure 5: The tool call expanded: what the AI sent to the server and what came back.\]*

Die ganze Demo habe ich in zwei verschiedenen KI-Apps durchgespielt: in ChatGPT und in Gemini in Google Antigravity. In diesem Test kamen beide mit demselben Server und denselben Werkzeugen zu denselben Ergebnissen. Das heißt nicht, dass sich jede KI-App gleich verbindet; jedes Produkt hat seine eigene Einrichtung und eigene Grenzen. Aber der Server musste nicht wissen, welche KI fragt. Genau darum geht es bei einem Standard.

*\[Figure 6: ChatGPT and Gemini in Antigravity side by side, one server.\]*

Den Code zu schreiben war der einfache Teil. Drei Dinge waren wichtiger:

- **Werkzeugbeschreibungen sind die Benutzeroberfläche.** Die KI wählt Werkzeuge, indem sie deren Beschreibungen liest, also verdienen sie dieselbe Sorgfalt wie Beschriftungen von Schaltflächen.
- **Zusammenfassungen schlagen Datenberge.** Geben Sie Anzahlen und die wichtigsten Ergebnisse zurück, Details auf Anfrage. Wer der KI ein ganzes Modell schickt, überlastet ihr Arbeitsgedächtnis und verschlechtert die Antworten.
- **Einheiten und IDs, immer.** Jede Zahl trägt ihre Einheit und jedes Element seine GUID. Wo es mehrdeutig wird, fängt die KI wieder an zu raten.

Nichts davon ersetzt das Prüfwerkzeug. Es lässt sich nur leichter befragen.

## Wo die Branche steht

In weniger als zwei Jahren ist MCP von einem Experiment zu einer Funktion geworden, die große AEC-Anbieter mit ihren Produkten ausliefern.

Anthropic hat den Standard im November 2024 veröffentlicht. Seitdem haben AEC-Anbieter begonnen, MCP-Verbindungen auszuliefern, jede mit eigenem Umfang und eigenen Bedingungen:

- **Revit (Autodesk):** ein schreibgeschützter [MCP-Server](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/) seit Juni, zu dem im September [Trusted-Write- und Experimental-Server](https://forums.autodesk.com/t5/revit-mep-forum/revit-mcp-server-tech-preview-launch/td-p/14262011) hinzukamen. Alle sind Technical Previews für Revit 2027.
- **Revu (Bluebeam):** [verbindet sich über MCP mit Claude](https://support.bluebeam.com/revu/how-to/mcp-claude.html). Voraussetzung sind ein Bluebeam-Max-Abonnement, Revu 21.9 oder neuer und die Desktop-App von Claude.
- **SketchUp (Trimble):** ein [Claude-Konnektor](https://help.sketchup.com/en/sketchup-claude-connector), der aus einem Gespräch neue SketchUp-Modelle erstellt. Bestehende Dateien kann er nicht bearbeiten, und Claude ist derzeit der einzige unterstützte KI-Anbieter.
- **RFEM 6 (Dlubal Software):** ein MCP-Server in der Standardinstallation seit Januar 2026, der über die Dlubal API arbeitet. Details stehen im [Knowledge-Base-Beitrag](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/002032) und in der [API-Dokumentation](https://apidocs.dlubal.com/installation_mcp.html) von Dlubal.

Diese Produkte ändern sich schnell, prüfen Sie also die aktuellen Bedingungen, bevor Sie mit ihnen planen, und gehen Sie nicht davon aus, dass sich eines davon ohne Weiteres mit jeder KI-App verbindet.

Anbieter treffen auch unterschiedliche Designentscheidungen. Manche Server stellen wenige, eng gefasste Werkzeuge für bestimmte Zwecke bereit. Andere lassen die KI Skripte gegen die API des Programms schreiben, ähnlich wie ein Dynamo- oder Grasshopper-Skript, nur dass die KI es schreibt. Die Reichweite hängt davon ab, was der Server freigibt und welche Berechtigungen dahinterstehen. Eng gefasste Werkzeuge geben allen sichere Standardeinstellungen; Skripting gibt erfahrenen Nutzern mehr Reichweite, um den Preis, den von der KI geschriebenen Code zu prüfen und zu testen. Mein eigener Server steht klar am eng gefassten Ende.

Lang laufende Aufgaben, etwa eine große Berechnung oder eine aufwendige Modellprüfung, haben in MCP ein eigenes Muster: Tasks. Sie begannen als experimentelle Funktion, und die [Spezifikation vom Juli 2026](https://modelcontextprotocol.io/specification/2026-07-28/changelog) hat sie in eine offizielle Erweiterung überführt. Sie helfen nur, wenn sowohl die KI-App als auch der Server sie umsetzen.

## Was MCP nicht löst

MCP beseitigt die Reibung zwischen ingenieurmäßigem Urteil und seiner Umsetzung. Es ersetzt das Urteil nicht, und es bringt ein paar eigene neue Risiken mit.

- **Die Verantwortung bleibt, wo sie ist.** Der Einsatz von KI nimmt dem Ingenieur nicht die Verantwortung, das Ergebnis zu prüfen. Die KI stempelt keine Pläne, und wie die Haftung verteilt ist, ist eine Frage für Ihre Verträge und Ihre Rechtsberatung.
- **Was man hineingibt, kommt heraus, nur schneller.** MCP automatisiert einen chaotischen Prozess genauso treu wie einen geordneten. Uneinheitliche Parameter und fehlende Klassifikationscodes (UniFormat, OmniClass) tauchen früher auf, sie verschwinden nicht.
- **Von der KI geschriebener Code muss geprüft werden.** Wenn ein Server Skripte ausführt, die das Modell schreibt, kann das Modell ein falsches schreiben. Prüfen Sie den Code, testen Sie an einer Kopie und halten Sie Berechnungsergebnisse unter Versionskontrolle.
- **Wissen Sie, wohin die Daten gehen.** Ein lokaler Server hält das Modell auf Ihrem Rechner, aber der KI-Host sieht weiterhin alles, was die Werkzeuge zurückgeben, und Lesezugriff ändert daran nichts. Prüfen Sie die Bedingungen Ihres KI-Anbieters zu Datenspeicherung und Training, bevor Sie laufende Projekte anbinden.
- **Modelldaten können Anweisungen enthalten.** Ein Eigenschaftswert oder ein Kommentar in einem Dokument kann Text enthalten, der versucht, die KI zu steuern. Lesezugriff begrenzt Änderungen am Modell; er verhindert weder irreführende Antworten noch den Abfluss von Daten. Beginnen Sie mit einem vertrauenswürdigen Server, eingeschränktem Zugriff und einem Testmodell, das Ihr Büro freigegeben hat.
- **Es ist nicht umsonst.** Planen Sie Budget für KI-Abonnements, API-Zugang oder Zusatzlizenzen auf der Softwareseite und für Workstations ein, die mithalten.

## So starten Sie am Montag

Fangen Sie klein an: ein Projekt, eine Aufgabe nur mit Lesezugriff, eine neugierige Person. Stellen Sie vorher Ihren Softwareanbietern fünf Fragen:

1. Liefern Sie einen MCP-Server, und ist er offiziell oder von der Community gebaut?
2. Ist er schreibgeschützt, oder kann er das Modell ändern? Sind beide Varianten getrennt?
3. Läuft er lokal oder in der Cloud, und wohin gehen die Projektdaten?
4. Mit welchen KI-Anwendungen haben Sie ihn getestet?
5. Wie wird er lizenziert und abgerechnet?

Starten Sie dann ein Pilotprojekt. Wählen Sie eine wiederkehrende Aufgabe und ein Testmodell, das Ihr Büro freigegeben hat, etwa die Prüfung einer Modellrevision gegen die Informationsanforderungen des Projekts. Vergleichen Sie Ihren heutigen Ablauf, einschließlich eines Prüfwerkzeugs, das Sie bereits nutzen, mit der KI-gestützten Variante. Zählen Sie neben der gesparten Zeit auch den Prüfaufwand, übersehene Probleme und Fehlalarme, und wiederholen Sie das an einer weiteren Revision, bevor Sie entscheiden. Dieser Vergleich sagt Ihnen mehr als jede Demo eines Anbieters.

## Eine Brücke, kein Ersatz

MCP plant kein Gebäude. Es lässt die KI aber an die Werkzeuge heran, die die Ingenieurarbeit schon erledigen, sodass die Stunden zwischen einer Frage und ihrer Antwort schrumpfen.

Stellen Sie sich den nächsten Schritt vor. Eine Steckdose findet die Elemente, die sich in der letzten Modellrevision geändert haben. Eine zweite schickt sie weiter an das nächste Werkzeug, ein Berechnungsprogramm oder eine Koordinationsplattform, sofern die Modelle und ihre Element-IDs verknüpft sind, was nach wie vor einer der schwierigsten Teile der Arbeit ist. Die KI verbindet die Schritte und legt das Ergebnis der Person vor, die entscheidet. Die Bausteine gibt es heute schon; jeder Schritt braucht aber weiterhin jemanden, der das Ergebnis prüft.

Die AEC-Software, auf die wir uns verlassen, ist hervorragend im Ingenieurwesen. Die KI-Plattformen sind hervorragend in Sprache und Schlussfolgern. MCP ist die Steckdose dazwischen, und es lohnt sich, zu verstehen, wie es funktioniert, bevor Ihre Wettbewerber es tun.

Meine Sicht: Wenn KI-Modelle Baudaten bekommen, werden sie besser in unserer Arbeit, und ich vertraue diese Daten den großen US-Anbietern an. Die Regeln für jedes Projekt bestimmen aber weiterhin Ihre Verträge. In ein paar Jahren wird eine Frage an die KI zum Modell so selbstverständlich sein wie eine Google-Suche.

Lieber hören? Zu diesem Beitrag gibt es eine Folge des Insights-Podcasts (auf Englisch), die auf demselben Test aufbaut.

## Quellen
