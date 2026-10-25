# Eine Steckdose für KI: Was MCP für das Bauwesen bedeutet

25. Oktober 2026 · Martin Motlík

## Die KI, die Ihr Modell nicht öffnen kann

Ihr KI-Assistent entwirft die Antwort auf eine Rückfrage zu den Plänen, fasst einen Abschnitt der Leistungsbeschreibung zusammen und bringt das Besprechungsprotokoll in Form. Fragen Sie ihn aber, welcher Unterzug im 3. Geschoss die höchste Ausnutzung hat, dann rät er. Nicht, weil er nicht klug genug wäre, sondern weil er keinen Zugang zu Ihrem Modell hat.

Diese Lücke schließt sich. Das Model Context Protocol, kurz MCP, ist ein offener Standard, über den sich KI-Anwendungen mit der Software und den Daten verbinden, mit denen Ingenieure ohnehin arbeiten. Stellen Sie es sich als Steckdose für KI vor: eine genormte Steckdose, und jedes Werkzeug, das Sie einstecken, wird zu etwas, mit dem die KI tatsächlich arbeiten kann.

Ich betrachte das Thema von zwei Seiten. Durch meine Arbeit für Dlubal Software bewege ich mich in einem Umfeld, in dem MCP bereits Teil des Produkts ist, und ich entwickle einen eigenen Prototyp für die Modellprüfung auf Basis von IFC. Dieser Beitrag erklärt, was MCP ist, wofür es im Bauwesen taugt und warum es meist sinnvoller ist, unsere Werkzeuge mit den KI-Plattformen zu verbinden, die Ingenieure bereits nutzen, als einen weiteren Chatbot zu bauen.

## Was MCP ist: eine Steckdose, kein Gehirn

MCP macht KI nicht klüger. Es gibt der KI einen genormten Weg zu Dingen außerhalb ihrer selbst: zu Ihren Modellen, Ihren Berechnungsprogrammen, Ihren Projektdaten.

Denken Sie an den Baustromverteiler auf der Baustelle. Ihm ist es egal, ob Sie eine Säge, einen Winkelschleifer oder einen Baustrahler einstecken, denn jedes Werkzeug hat denselben Stecker. Vor MCP bedeutete die Anbindung einer KI an eine Anwendung eine eigene Verkabelung für jedes Paar: Fünf KI-Apps und zwanzig Programme ergaben bis zu hundert einzelne Integrationen. Mit MCP braucht jedes Programm einen Server und jede KI-App einen Client. Fünfundzwanzig Teile statt hundert, auch wenn jede Verbindung weiterhin die richtige Einrichtung und die passenden Berechtigungen braucht.

&#91;embedded content: Figure 1 · MCP architecture: hosts, the outlet, servers\]

Jede KI-Anwendung braucht einen Client und jedes Programm einen Server; den Rest erledigt der Standard in der Mitte.

Anthropic hat MCP im November 2024 als offenen Standard veröffentlicht. Im Dezember 2025 übergab das Unternehmen den Standard an die von OpenAI, Google, Microsoft, AWS und weiteren Unternehmen getragene [Agentic AI Foundation](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) unter dem Dach der Linux Foundation. Heute unterstützen ihn ChatGPT, Claude, Gemini, Microsoft Copilot, GitHub Copilot und Cursor.

**Drei Rollen, einfach erklärt:**

- **Host:** die KI-Anwendung, in die Sie Ihre Fragen eingeben, etwa ChatGPT, Gemini, Claude oder der eigene Chatbot Ihres Unternehmens.
- **Client:** der Konnektor im Host, der die Verbindung zu einem Server hält.
- **Server:** ein kleines Programm auf der Seite der Software, das der KI sagt, was es kann. RFEM, Revit oder ein Werkzeug zur IFC-Prüfung bekommen jeweils ihren eigenen.

**Was ein Server anbietet:**

- **Tools** sind Aktionen, die die KI aufrufen kann: ein Modell anhand der Datenanforderungen des Projekts prüfen, zwei Modellversionen vergleichen, eine Berechnung starten.
- **Resources** sind Daten, die die KI lesen kann: eine Modellübersicht, eine Liste der Lastfälle.
- **Prompts** sind vorbereitete Abläufe: „Prüfe die Änderungen zwischen den Versionen A und B.“

Entscheidend ist, wie die KI die Werkzeuge findet. Jedes Werkzeug bringt eine Beschreibung und eine strukturierte Definition seiner Eingaben mit. Wenn Sie eine Frage stellen, wählt die KI anhand dieser Angaben ein Werkzeug und liefert die Informationen, die es braucht. Niemand legt im Code fest, welcher Knopf gedrückt wird; welche Werkzeuge überhaupt verfügbar sind, entscheidet aber die Anwendung.

Ein Server kann lokal laufen, direkt neben Ihrer Desktop-Anwendung. Die Modelldatei bleibt auf Ihrem Rechner; an die KI gehen nur die Antworten, die die Werkzeuge zurückgeben. Oder er läuft remote, über HTTPS mit sauberer Authentifizierung; das passt zu Cloud-Plattformen. Wenn IFC die Art ist, wie ein Modell ein Gebäude beschreibt, dann ist MCP die Art, wie eine KI diesem Modell Fragen stellt.

## Warum das Bauwesen es braucht: raten oder rechnen

Mit MCP wird aus einer KI, die selbstbewusst rät, ein Koordinator, der jede Aufgabe an ein Werkzeug übergibt, dem Ingenieure bereits vertrauen. Dieser Unterschied zählt in unserer Branche mehr als fast überall sonst.

Ein universelles Sprachmodell sagt plausiblen Text voraus. Bitten Sie es, einen Träger nachzuweisen, und Sie bekommen eine sauber formatierte, selbstsichere Antwort, die schlicht falsch sein kann, weil nie gerechnet wurde. Mit MCP delegiert die KI: Die Berechnung geht an das Berechnungsprogramm, die Frage zum Modell geht an das Modell, und die KI macht, was sie wirklich gut kann. Sie versteht die Frage, führt die Schritte in der richtigen Reihenfolge aus und erklärt das Ergebnis verständlich. Sie kann trotzdem den falschen Filter wählen oder ein Ergebnis falsch deuten; deshalb macht die Verbindung allein eine Antwort nicht zuverlässig. Sie macht sie überprüfbar.

MCP ist nicht der einzige Weg, Projektinformationen in eine KI zu bringen, deshalb lohnt ein Blick darauf, wo es sich einordnet. Eine Ergebnistabelle in den Chat zu kopieren funktioniert, ist aber eine manuelle Momentaufnahme, die veraltet, sobald sich das Modell ändert. Retrieval-Augmented Generation (RAG) lässt die KI Dokumente durchsuchen, etwa eine Norm, einen BIM-Abwicklungsplan oder ein Produkthandbuch, und zitieren, was sie findet.

Das sind keine konkurrierenden Technologien. MCP ist die Verbindung; eine Dokumentensuche ist eine Art von Werkzeug, die Sie anschließen können. Sie kann genauso hinter einem MCP-Server sitzen wie ein Werkzeug, das ein geöffnetes Modell abfragt oder eine Prüfung startet. Der nützliche Unterschied liegt darin, was das jeweilige Werkzeug kann. Eine Dokumentensuche beantwortet die Frage „Was steht in der Norm?“. Ein Modellwerkzeug beantwortet die Frage „Was steht in meinem Modell, und besteht es die Prüfung?“. Die meisten ernsthaften Abläufe im Bauwesen werden beides nutzen.

Individuelle Integrationen, etwa ein im Programm eingebauter Assistent, greifen ebenfalls auf aktuelle Daten zu, aber jede verbindet genau eine KI mit genau einer Anwendung. Mit MCP lassen sich dieselben Werkzeuge in jeder KI-App wiederverwenden, die den Standard unterstützt, in den Grenzen, die die jeweilige App setzt. Die KI kann genau das, was die Werkzeuge erlauben, nicht mehr.

Wie sieht das in einem echten Projekt aus? Diese Anfragen sind mit heute verfügbaren Servern bereits möglich:

- **Modellabfragen:** „Finde alle Feuerschutztüren im 2. Geschoss ohne Beschlagsatz und wähle sie aus.“ Der offizielle Revit-Server von Autodesk kann das Modell durchsuchen und die Ergebnisse auswählen.
- **Mengen:** „Wie viele Kubikmeter Beton stecken in den Decken, Geschoss für Geschoss?“ Open-Source-Server lesen das direkt aus einer IFC-Datei, sofern das Modell verlässliche Mengen enthält.
- **Koordination:** „Welche Punkte aus der Koordinationsbesprechung der letzten Woche sind noch offen?“ Koordinationsplattformen wie Revizto bieten inzwischen MCP-Server an, und Community-Server greifen auf offene Punkte und Rückfragen in der Autodesk Construction Cloud zu.
- **Berechnungsergebnisse:** „Wie groß ist die maximale Durchbiegung der Deckenträger für die Lastfallkombinationen im Grenzzustand der Gebrauchstauglichkeit, und hält sie L/360 ein?“ Die Antwort kommt aus dem Berechnungsprogramm, nicht aus dem Gedächtnis der KI.

## Warum an die großen KI-Plattformen andocken, statt einen eigenen Chatbot zu bauen

Die KI-Firmen sollen sich um Sprache kümmern, die Bausoftware um das Ingenieurwesen. Alle paar Monate kündigt jemand in unserer Branche einen eigenen Assistenten an. Ein eigener Chatbot bedeutet aber kein eigenes Sprachmodell. Die meisten maßgeschneiderten Assistenten laufen auf denselben kommerziellen Modellen, nur hinter einer eigenen Oberfläche. Die eigentliche Frage ist, wo die Ingenieurwerkzeuge angesiedelt sind, und MCP hält sie wiederverwendbar, ganz gleich, welche Oberfläche Ihr Team am Ende nutzt. Für den Einstieg über die KI-Plattformen, die Ihr Team bereits verwendet, spricht meist Folgendes:

1. **Sie bekommen die leistungsfähigsten KI-Modelle, und die werden immer besser.** Kein Ingenieurbüro und kein Anbieter von Bausoftware kann mit den Forschungsbudgets von Anthropic, Google, OpenAI oder Microsoft mithalten. Mit besseren Modellen werden in der Regel auch die Werkzeugauswahl und die Erklärung der Ergebnisse besser. Das geschieht aber nicht bei jedem Ablauf von selbst, testen Sie deshalb erneut, was Ihnen wichtig ist, wenn sich das KI-Modell ändert.
2. **Ingenieure arbeiten schon dort.** Viele Büros zahlen bereits für Microsoft 365 Copilot, ChatGPT, Claude oder Gemini. Ein neuer eigenständiger Chatbot ist ein weiterer Zugang, den nach der zweiten Woche niemand mehr nutzt. Wenn der KI-Assistent, für den Ihr Büro schon zahlt, die nötige Verbindung unterstützt, erscheint ein MCP-Server dort, wo die Leute ohnehin arbeiten.
3. **Einmal bauen, überall einstecken.** Derselbe Server lässt sich in Claude, ChatGPT, Gemini, Copilot und in KI-Assistenten wiederverwenden, die ein Büro selbst baut. Jede App braucht weiterhin ihre eigene Einrichtung der Verbindung, und nicht jedes Produkt unterstützt jede Funktion. Wechselt Ihr Büro aber den KI-Anbieter, müssen die Ingenieurwerkzeuge nicht neu gebaut werden. Sogar direkte Konkurrenten wie OpenAI, Google und Microsoft unterstützen den Standard.
4. **Werkzeuge beginnen zusammenzuarbeiten.** In einem Gespräch lässt sich das Modell abfragen, eine Berechnung starten, eine Tabelle füllen und das Ergebnis im Dokumentenmanagement ablegen. Ein solcher werkzeugübergreifender Ablauf brauchte früher für jeden Schritt ein eigenes Skript.
5. **Ihr Fachwissen bleibt Ihres.** Der Anbieter behält den validierten Solver, die Normnachweise und das Datenmodell. Die KI-Plattform liefert die Gesprächsebene obendrauf. Das Fachwissen bleibt der Wettbewerbsvorteil, und so soll es auch sein.

Es gibt einen sechsten, leiseren Vorteil. Die großen Plattformen bringen eine Unternehmensinfrastruktur mit, die ein kleines Werkzeug für das Bauwesen nie selbst bauen würde: Freigabe von Konnektoren durch Administratoren, Bestätigungsabfragen vor dem Ausführen eines Werkzeugs und Anmeldung über Standardprotokolle. In Microsoft 365 Copilot und Gemini Enterprise kann ein IT-Administrator zum Beispiel einen eigenen MCP-Server einmal für die gesamte Organisation registrieren.

## Drei Arten von Zugriff

Die richtige Frage ist nicht, ob Sie die KI in Ihr Modell lassen, sondern was sie dort tun darf. Das entscheidet Ihr Büro, nicht die KI. MCP macht die Grenze sichtbar, weil jeder Server genau angibt, welche Werkzeuge es gibt. Entscheidend ist, was diese Werkzeuge können und welche Berechtigungen dahinterstehen, nicht das Etikett auf dem Server.

**Lesen.** Die KI fragt Modelle und Daten ab: Sie listet die Feuerschutztüren eines Geschosses auf oder ruft die Eigenschaften eines einzelnen Elements ab. Lesezugriff begrenzt Änderungen am Modell. Er macht die Informationen nicht weniger sensibel, und er verhindert keine irreführende Antwort.

**Prüfen.** Die KI führt Prüfungen aus: eine IDS-Validierung, einen Kollisionsbericht, einen Vergleich zwischen Revisionen. IDS ist ein Standard von buildingSMART, der ausgewählte Informationsanforderungen in maschinenprüfbarer Form beschreibt. Sie legen fest, welche Elemente welche Daten brauchen, und ein Prüfwerkzeug prüft das Modell anhand dieser Regeln. Es prüft die Informationen, nicht, ob das Gebäude richtig geplant ist. Die Ergebnisse fließen in Entscheidungen ein, deshalb prüft sie ein Mensch.

**Schreiben.** Die KI ändert das Modell selbst: Sie füllt Parameter aus, verschiebt Elemente oder erstellt neue. Das braucht kontrollierte Berechtigungen, eine Prüfung jeder Änderung und eine Möglichkeit, sie rückgängig zu machen.

Die Revit-Server von Autodesk zeigen, wie Anbieter diese Grenzen ziehen. Der erste [MCP-Server für Revit](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/), im Juni als Technical Preview veröffentlicht, war schreibgeschützt. Im September hat Autodesk einen Trusted-Write-Server [ergänzt](https://forums.autodesk.com/t5/revit-mep-forum/revit-mcp-server-tech-preview-launch/td-p/14262011), mit dem Sie jede Änderung eines Agenten prüfen können, sowie einen Experimental-Server mit weitergehenden Bearbeitungswerkzeugen, dessen Nutzung laut Autodesk auf eigenes Risiko erfolgt. Beide sind Technical Previews für Revit 2027. Für die meisten Büros ist Lesen der richtige Einstieg, und zwar an einem Testmodell, das das Büro freigegeben hat.

## Was ich gebaut habe: sechs Werkzeuge

Um zu sehen, wie hoch die Hürde wirklich ist, habe ich einen schreibgeschützten MCP-Server für den Prototyp zur Modellprüfung gebaut, den ich entwickle. Der Prototyp prüft IFC-Modelle bereits gegen IDS-Anforderungen und vergleicht Modellversionen. Die Validierung selbst ist nicht neu; das Prüfwerkzeug des Prototyps konnte sie schon vorher. Neu durch den Server ist die Möglichkeit, Folgefragen zu stellen, die Schritte zu verbinden und direkt zu den betroffenen Elementen zu springen.

*\[Figure 2: Code card. One complete MCP tool in about ten lines of Python.\]*

Der Server heißt `ifc-review` und stellt sechs Werkzeuge bereit, alle schreibgeschützt:

- `get_model_summary`: Projekt, Versionen, Geschosse, Anzahl der Elemente
- `list_elements`: Elemente nach IFC-Klasse, Geschoss oder dem Merkmal „tragend“ finden
- `get_properties`: Eigenschaftssätze, Mengen und Materialien eines Elements
- `run_ids_check`: eine Version gegen eine IDS-Datei validieren
- `compare_versions`: was zwischen zwei Versionen hinzugefügt, entfernt oder geändert wurde
- `get_viewer_link`: ein Link, der den 3D-Viewer öffnet und die betreffenden Elemente hervorhebt

*\[Figure 3: The tool list as ChatGPT shows it, with the descriptions the AI reads.\]*

Dann habe ich den Test an einem echten Modell durchgeführt: dem Konzeptmodell eines Wohngebäudes in Prag mit einer Garage auf Straßenebene, drei Wohngeschossen und einem Dachgeschoss, geprüft gegen eine IDS-Datei mit 14 Informationsanforderungen. Ich habe gefragt, welche Anforderungen nicht erfüllt sind und welche Elemente betroffen sind. Zwei Anforderungen waren nicht erfüllt, betroffen waren 13 Elemente: zwei Dachfenster ohne U-Wert und elf Türen ohne Feuerwiderstandsklasse. Laut den Türbezeichnungen wird die Feuerwiderstandsklasse erst im Brandschutzkonzept festgelegt. Das erklärt, warum der Wert fehlt. Es liefert ihn aber nicht, und ob der Wert in dieser Phase erforderlich ist, entscheidet das Projektteam.

Für den Test habe ich dann eine zweite Revision vorbereitet, in der ein Teil der Lücken geschlossen war, und die Frage gestellt, die jedes Team nach einer Revision stellt: Was wurde behoben, und was fehlt noch? Die KI rief die Vergleichs- und Validierungswerkzeuge auf, und die Ergebnisse wurden über die Element-ID abgeglichen. Zehn der dreizehn Elemente waren behoben. Drei Türen im 3. Wohngeschoss hatten weiterhin keine Feuerwiderstandsklasse. Anschließend gab mir die KI einen Link, der das Modell mit genau diesen drei Türen hervorgehoben öffnete.

*\[Figure 4: Main figure. The answer in chat on the left, the same three doors highlighted in the model on the right.\]*

*\[Figure 5: The tool call expanded: what the AI sent to the server and what came back.\]*

Die ganze Demo habe ich in zwei verschiedenen KI-Apps durchgespielt: in ChatGPT und in Gemini in Google Antigravity. In diesem Test kamen beide mit demselben Server und denselben Werkzeugen zu denselben Ergebnissen. Das heißt nicht, dass sich jede KI-App gleich verbindet; jedes Produkt hat seine eigene Einrichtung und eigene Grenzen. Aber der Server musste nicht wissen, welche KI fragt. Genau darum geht es bei einem Standard.

*\[Figure 6: ChatGPT and Gemini in Antigravity side by side, one server.\]*

Den Code zu schreiben war der einfache Teil. Drei Dinge waren wichtiger:

- **Werkzeugbeschreibungen sind die Benutzeroberfläche.** Die KI wählt Werkzeuge, indem sie deren Beschreibungen liest, also verdienen sie dieselbe Sorgfalt wie Beschriftungen von Schaltflächen.
- **Zusammenfassungen statt Datenberge.** Geben Sie Anzahlen und die wichtigsten Ergebnisse zurück, Details auf Anfrage. Wer der KI ein ganzes Modell schickt, überlastet ihr Arbeitsgedächtnis und verschlechtert die Antworten.
- **Einheiten und IDs, immer.** Jede Zahl trägt ihre Einheit und jedes Element seine GUID. Wo es mehrdeutig wird, fängt die KI wieder an zu raten.

Nichts davon ersetzt das Prüfwerkzeug. Es lässt sich nur leichter befragen.

## Wo die Branche steht

In weniger als zwei Jahren ist MCP von einem Experiment zu einer Funktion geworden, die große Anbieter von Bausoftware mit ihren Produkten ausliefern.

Anthropic hat den Standard im November 2024 veröffentlicht. Seitdem haben Anbieter von Bausoftware begonnen, MCP-Verbindungen auszuliefern, jede mit eigenem Umfang und eigenen Bedingungen:

- **Revit (Autodesk):** ein schreibgeschützter [MCP-Server](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/) seit Juni, zu dem im September [Trusted-Write- und Experimental-Server](https://forums.autodesk.com/t5/revit-mep-forum/revit-mcp-server-tech-preview-launch/td-p/14262011) hinzukamen. Alle sind Technical Previews für Revit 2027.
- **Revu (Bluebeam):** [verbindet sich über MCP mit Claude](https://support.bluebeam.com/revu/how-to/mcp-claude.html). Voraussetzung sind ein Bluebeam-Max-Abonnement, Revu 21.9 oder neuer und die Desktop-App von Claude.
- **SketchUp (Trimble):** ein [Claude-Konnektor](https://help.sketchup.com/en/sketchup-claude-connector), der aus einem Gespräch neue SketchUp-Modelle erstellt. Bestehende Dateien kann er nicht bearbeiten, und Claude ist derzeit der einzige unterstützte KI-Anbieter.
- **RFEM 6 (Dlubal Software):** seit Januar 2026 ein MCP-Server in der Standardinstallation, der über die Dlubal API arbeitet. Details stehen im [Knowledge-Base-Beitrag](https://www.dlubal.com/en/support-and-learning/support/knowledge-base/002032) und in der [API-Dokumentation](https://apidocs.dlubal.com/installation_mcp.html) von Dlubal.

Diese Produkte ändern sich schnell, prüfen Sie also die aktuellen Bedingungen, bevor Sie mit ihnen planen, und gehen Sie nicht davon aus, dass sich eines davon ohne Weiteres mit jeder KI-App verbindet.

Anbieter treffen auch unterschiedliche Designentscheidungen. Manche Server stellen wenige, eng gefasste Werkzeuge für bestimmte Zwecke bereit. Andere lassen die KI Skripte für die API des Programms schreiben, ähnlich wie ein Dynamo- oder Grasshopper-Skript, nur dass die KI es schreibt. Was möglich ist, hängt davon ab, was der Server freigibt und welche Berechtigungen dahinterstehen. Eng gefasste Werkzeuge geben allen sichere Standardeinstellungen; Skripting gibt erfahrenen Anwendern mehr Spielraum, um den Preis, dass sie den von der KI geschriebenen Code prüfen und testen müssen. Mein eigener Server steht klar am eng gefassten Ende.

Lang laufende Aufgaben, etwa eine große Berechnung oder eine aufwendige Modellprüfung, haben in MCP ein eigenes Muster: Tasks. Sie begannen als experimentelle Funktion, und die [Spezifikation vom Juli 2026](https://modelcontextprotocol.io/specification/2026-07-28/changelog) hat sie in eine offizielle Erweiterung überführt. Sie helfen nur, wenn sowohl die KI-App als auch der Server sie umsetzen.

## Was MCP nicht löst

MCP beseitigt die Reibung zwischen dem fachlichen Urteil des Ingenieurs und seiner Umsetzung. Es ersetzt das Urteil nicht, und es bringt ein paar eigene neue Risiken mit.

- **Die Verantwortung bleibt, wo sie ist.** Der Einsatz von KI nimmt dem Ingenieur nicht die Verantwortung, das Ergebnis zu prüfen. Die KI unterschreibt keine Pläne, und wie die Haftung verteilt ist, ist eine Frage für Ihre Verträge und Ihre Rechtsberatung.
- **Schlechte Daten rein, schlechte Ergebnisse raus, nur schneller.** MCP automatisiert einen chaotischen Prozess genauso treu wie einen geordneten. Uneinheitliche Parameter und fehlende Klassifikationscodes (UniFormat, OmniClass) tauchen früher auf, sie verschwinden nicht.
- **Von der KI geschriebener Code muss geprüft werden.** Wenn ein Server Skripte ausführt, die die KI schreibt, kann die KI auch ein fehlerhaftes schreiben. Prüfen Sie den Code, testen Sie an einer Kopie und halten Sie Berechnungsergebnisse unter Versionskontrolle.
- **Wissen Sie, wohin die Daten gehen.** Ein lokaler Server hält das Modell auf Ihrem Rechner, aber der KI-Host sieht weiterhin alles, was die Werkzeuge zurückgeben, und Lesezugriff ändert daran nichts. Prüfen Sie die Bedingungen Ihres KI-Anbieters zu Datenspeicherung und Training, bevor Sie laufende Projekte anbinden.
- **Modelldaten können Anweisungen enthalten.** Ein Eigenschaftswert oder ein Kommentar in einem Dokument kann Text enthalten, der versucht, die KI zu steuern. Lesezugriff begrenzt Änderungen am Modell; er verhindert weder irreführende Antworten noch den Abfluss von Daten. Beginnen Sie mit einem vertrauenswürdigen Server, eingeschränktem Zugriff und einem Testmodell, das Ihr Büro freigegeben hat.
- **Es ist nicht umsonst.** Planen Sie Budget für KI-Abonnements, API-Zugang oder Zusatzlizenzen auf der Softwareseite und für ausreichend leistungsfähige Workstations ein.

## So starten Sie am Montag

Fangen Sie klein an: ein Projekt, eine Aufgabe nur mit Lesezugriff, eine neugierige Person. Stellen Sie vorher Ihren Softwareanbietern fünf Fragen:

1. Liefern Sie einen MCP-Server, und ist er offiziell oder von der Community gebaut?
2. Ist er schreibgeschützt, oder kann er das Modell ändern? Sind beide Varianten getrennt?
3. Läuft er lokal oder in der Cloud, und wohin gehen die Projektdaten?
4. Mit welchen KI-Anwendungen haben Sie ihn getestet?
5. Wie wird er lizenziert und abgerechnet?

Starten Sie dann ein Pilotprojekt. Wählen Sie eine wiederkehrende Aufgabe und ein Testmodell, das Ihr Büro freigegeben hat, etwa die Prüfung einer Modellrevision anhand der Informationsanforderungen des Projekts. Vergleichen Sie Ihren heutigen Ablauf, einschließlich eines Prüfwerkzeugs, das Sie bereits nutzen, mit der KI-gestützten Variante. Erfassen Sie neben der eingesparten Zeit auch den Prüfaufwand, übersehene Probleme und Fehlalarme, und wiederholen Sie das an einer weiteren Revision, bevor Sie entscheiden. Dieser Vergleich sagt Ihnen mehr als jede Demo eines Anbieters.

## Eine Brücke, kein Ersatz

MCP plant kein Gebäude. Es lässt die KI aber an die Werkzeuge heran, die die Ingenieurarbeit schon erledigen, sodass die Stunden zwischen einer Frage und ihrer Antwort schrumpfen.

Stellen Sie sich den nächsten Schritt vor. Eine Steckdose findet die Elemente, die sich in der letzten Modellrevision geändert haben. Eine zweite schickt sie weiter an das nächste Werkzeug, ein Berechnungsprogramm oder eine Koordinationsplattform, sofern die Modelle und ihre Element-IDs verknüpft sind, was nach wie vor einer der schwierigsten Teile der Arbeit ist. Die KI verbindet die Schritte und legt das Ergebnis der Person vor, die entscheidet. Die Bausteine gibt es heute schon; jeder Schritt braucht aber weiterhin jemanden, der das Ergebnis prüft.

Die Bausoftware, auf die wir uns verlassen, ist stark in der Ingenieurarbeit. Die KI-Plattformen sind stark in Sprache und logischem Denken. MCP ist die Steckdose dazwischen, und es lohnt sich, zu verstehen, wie es funktioniert, bevor Ihre Wettbewerber es tun.

Meine Sicht: Wenn KI-Modelle Baudaten bekommen, lernen sie unsere Arbeit besser kennen, und ich vertraue diese Daten den großen US-Anbietern an. Welche Regeln für ein Projekt gelten, bestimmen aber weiterhin Ihre Verträge. In ein paar Jahren wird es so selbstverständlich sein, der KI Fragen zum Modell zu stellen, wie etwas zu googeln.

Lieber hören? Zu diesem Beitrag gibt es eine Folge des Insights-Podcasts (auf Englisch), die auf demselben Test aufbaut.

## Quellen
