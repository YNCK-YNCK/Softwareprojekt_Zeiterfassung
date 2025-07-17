
![web_ui](https://github.com/user-attachments/assets/a6fcf407-36df-43ed-a072-e8c859c8abb3)


# Softwareprojekt_Zeiterfassung
Repo zur Bearbeitung des Softwareprojekts im Fach Softwareentwicklung im Studiengang LL.M. Rechtsinformatik

Ich habe mich bei der Umsetzung für eine Webbasierte Schnittstelle entschieden, da ich ein schönes UI haben wollte und gleichzeitig die Konnektivität über eine API sicherstellen wollte. Da die Aufgabenstellung eine MVC-Struktur ("Model-View-Controller") voraussetzt habe ich dies versucht nach meinen Möglichkeiten zu berücksichtigen. Das Model übernimmt hierbei wesentlich time_tracking_controller.py; Die View wird durch die Webanwendung umgesetzt, wobei Flask gleichzeitig Controller ist und die View ausliefert (wie ein braver Webserver das tut). Die Anwendung basiert auf einer Flask-API die eine Benutzeroberfläche (Web-Ansicht) und eine API nach Außen hin anbietet/ausliefert. Die Daten, die über die Flask-API eingegeben werden, werden durch die dahinterliegende Arbeitszeiterfassung verarbeitet. Die Speicherung der Daten erfolgt wie gefordert in Excel-Tabellen.

# Berücksichtigte und umgesetzte Requirements:

## Arbeitgeber (Employer)
Registriert mit der eindeutigen ID 001.
Erstellen neuer Mitarbeiter mit automatischer Nummerngenerierung und einer bestimmten Anzahl von Stunden pro Woche.
Verwaltung von Mitarbeitern.
Überwachung der Arbeitszeiten aller Mitarbeiter in einer Excel-Datei.
Anzeige aller Arbeitsstunden pro Jahr sowie der wöchentlichen Arbeitsstunden der aktuellen Woche für jeden Mitarbeiter.
Überwachung von Warnungen und Hervorhebungen aus der Excel-Datei.
NHR: Individuelle Begrenzung der Arbeitszeiten der Mitarbeiter durch Nachrichten, falls Kürzungen der Arbeitszeit erforderlich sind.

## Mitarbeiter (Employee)
Registrierung mit einer eindeutigen Nummer (beginnt mit 1XY).
Eingabe der Arbeitsstunden für einen bestimmten Tag.
Live-Tracking der Arbeitszeiten (mit Start/Stopp-Mechanismus).
NHR: Automatische Abzug der gesetzlich vorgeschriebenen Pause (§4 ArbZG).
Verschiedene Warnungen bei Überschreitung von 8 Stunden Arbeit und automatisches Stoppen der Aufzeichnung nach 11 Stunden.
Speicherung der gesammelten Daten in einer Excel-Tabelle.
Anzeige aller gearbeiteten Stunden an jedem Tag in der Tabelle.
Hervorhebung der Arbeit an Wochenenden oder Feiertagen.
Hervorhebung (Event-Logging) von automatisch gestoppten Aufnahmen.

## Allgemeine Funktionalitäten
Verwendung einer MVC-Struktur für das Projekt.
Effiziente und verständliche Erfassung der Arbeitszeiten durch Mitarbeiter.
Überwachung der verbleibenden Zeit und bereits gearbeiteten Zeit täglich.
Verwaltung und Überwachung der Arbeitszeiten durch Arbeitgeber.

## Nice to Have Requirements (NHR)
Automatische Abzug der gesetzlich vorgeschriebenen Pause (§4 ArbZG).
Individuelle Begrenzung der Arbeitszeiten der Mitarbeiter durch Nachrichten, falls Kürzungen der Arbeitszeit erforderlich sind.

# Sicherheitshinweis
Die Flask-API ist nur für den Testbetrieb bestimmt und konfiguriert. Es wird keine Authentifizierung vorgenommen - d.h. jeder, der die IP der API kennt, kann hierauf zugreifen. Daten werden unverschlüsselt gespeichert. Nicht für den Realgebrauch vorgesehen oder ausgelegt.

# API Test
Das API_Test.py Skript kann dazu genutzt werden um die API-Calls zu testen. Hierzu muss die Flask-API aber bereits laufen -> ggfs. zweites Terminal nutzen.

# Learnings und Room for Improvement
Ich habe beim Lesen der Requirements gedacht, dass ich dieses Projekt in ein Paar Stunden werde bearbeiten können. -> Anfängerfehler!
Bei den Datums- und Zeitformaten habe ich tatsächlich einige Probleme gehabt, da durch das Überführen in ein xlsx-Dokument und die spätere Formatierung (Hervorhebung von Arbeit an Feiertagen oder Wochenenden etc.) alles recht schnell unübersichtlich wurde. Auch hatte ich anfangs versucht die verschiedenen Klassen: time_tracking_controller, employee und employer deutlicher voneinander zu trennen. Das hat dann aber nach einiger Zeit mehr Probleme verursacht, als es vermeiden sollte, weshalb ich das ganze Tracking der Arbeitszeiten in time_tracking_controller umgezogen hatte. Das Event-Logging für reduzierte Arbeitsstunden verblieb beim employee. 
Die Implementierung der automatischen Pausenzeiten war ebenfalls schwierig, da bei Stückweisem Tracking, zu viele Pausenzeiten abgezogen wurden. Nun wird bei Erreichen der 6-h-Marke zunächst eine 30-Minuten-Pause abgezogen und eine Pausen-Flag gesetzt, die doppelte Abzüge an dem Kalendertag verhindert. Erreicht der MA dann sogar 9h am Tag, werden zusätzliche 15 Minuten Pause abgezogen. 
Hierbei habe ich die "staticmethod" kennengelern: "Eine staticmethod in Python ist eine Methode, die innerhalb einer Klasse definiert ist, aber weder auf Instanzvariablen noch auf Klassenvariablen zugreift. Sie wird mit dem @staticmethod-Dekorator gekennzeichnet. Diese Methode kann ohne die Notwendigkeit einer Klasseninstanz aufgerufen werden und verhält sich ähnlich wie eine reguläre Funktion außerhalb der Klasse." 

```python
@staticmethod
def calculate_break_time(total_hours, has_break_logged):
    if total_hours > 9:
        return 15 if has_break_logged else 45
    elif total_hours > 6:
        return 0 if has_break_logged else 30
    return 0
```

Der Kampf mit den Datentypen und Formaten beim import-export usw. mit pandas und openpyxl, sowie das Handling der Feiertage und Wochenenden aus der deutschlang.feiertage.api hat mir wirklich Probleme bereitet. Ich vermute, dass ich im Code vermutlich 30-50% der type-conversions weglassen könnte, aber am Ende hab ich das einfach überall reingepackt, bis es verlässlich lief. 

# Fazit
Das Projekt hat echt Spaß gemacht und war eine gute Übung um mal ein kleines aber Mehrteiliges Softwareprodukt zu bauen. Ich habe den Zeitaufwand definitiv unterschätzt, da ich für die Fehlersuche immer sehr lange gebraucht habe. Viele der Fehler sind mir aber dank- oder vielleicht auch nur aufgrund der Implementierung der API aufgefallen, weil man hierbei die Nutzerinputs etc. gedanklich antizipieren muss. Ich würde das Programm gerne einmal mit SQL im Hintergrund bauen und eine vernünftige Benutezrauthentifizierung implementieren. UND ich würde dafür gerne noch eine mini-GUI bauen, das in der Taskleiste bleibt und Start/Stopp des Tracking streamlined.
