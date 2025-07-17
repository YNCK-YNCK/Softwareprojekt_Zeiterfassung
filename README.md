# Softwareprojekt_Zeiterfassung
Repo zur Bearbeitung des Softwareprojekts im Fach Softwareentwicklung im Studiengang LL.M. Rechtsinformatik

Die Anwendung basiert auf einer Flask-API die eine Benutzeroberfläche (Web-Ansicht) und eine API nach Außen hin anbietet/ausliefert. Die Daten, die über die Flask-API eingegeben werden, werden durch die dahinterliegende Arbeitszeiterfassung verarbeitet. Die Speicherung der Daten erfolgt wie gefordert in Excel-Tabellen.

# Berücksichtigte und umgesetzte Requirements:

# Arbeitgeber (Employer)
Registriert mit der eindeutigen ID 001.
Erstellen neuer Mitarbeiter mit automatischer Nummerngenerierung und einer bestimmten Anzahl von Stunden pro Woche.
Verwaltung von Mitarbeitern.
Überwachung der Arbeitszeiten aller Mitarbeiter in einer Excel-Datei.
Anzeige aller Arbeitsstunden pro Jahr sowie der wöchentlichen Arbeitsstunden der aktuellen Woche für jeden Mitarbeiter.
Überwachung von Warnungen und Hervorhebungen aus der Excel-Datei.
NHR: Individuelle Begrenzung der Arbeitszeiten der Mitarbeiter durch Nachrichten, falls Kürzungen der Arbeitszeit erforderlich sind.

# Mitarbeiter (Employee)
Registrierung mit einer eindeutigen Nummer (beginnt mit 1XY).
Eingabe der Arbeitsstunden für einen bestimmten Tag.
Live-Tracking der Arbeitszeiten (mit Start/Stopp-Mechanismus).
NHR: Automatische Abzug der gesetzlich vorgeschriebenen Pause (§4 ArbZG).
Verschiedene Warnungen bei Überschreitung von 8 Stunden Arbeit und automatisches Stoppen der Aufzeichnung nach 11 Stunden.
Speicherung der gesammelten Daten in einer Excel-Tabelle.
Anzeige aller gearbeiteten Stunden an jedem Tag in der Tabelle.
Hervorhebung der Arbeit an Wochenenden oder Feiertagen.
Hervorhebung (Event-Logging) von automatisch gestoppten Aufnahmen.

# Allgemeine Funktionalitäten
Verwendung einer MVC-Struktur für das Projekt.
Effiziente und verständliche Erfassung der Arbeitszeiten durch Mitarbeiter.
Überwachung der verbleibenden Zeit und bereits gearbeiteten Zeit täglich.
Verwaltung und Überwachung der Arbeitszeiten durch Arbeitgeber.

# Nice to Have Requirements (NHR)
Automatische Abzug der gesetzlich vorgeschriebenen Pause (§4 ArbZG).
Individuelle Begrenzung der Arbeitszeiten der Mitarbeiter durch Nachrichten, falls Kürzungen der Arbeitszeit erforderlich sind.
