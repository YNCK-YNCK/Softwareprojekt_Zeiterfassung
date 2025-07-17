import requests
import json

# Basis-URL der API - Stellen Sie sicher, dass der Server läuft!
# Standardmäßig läuft Flask auf Port 5000
BASE_URL = "http://127.0.0.1:5000/api"

def check_server_availability():
    """Überprüft, ob der Server verfügbar ist"""
    try:
        response = requests.get(BASE_URL + "/employees")
        if response.status_code == 200:
            print("Server ist verfügbar und antwortet!")
            return True
        else:
            print(f"Server ist verfügbar, aber es gab einen Fehler: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Verbinden mit dem Server: {e}")
        print("\nMögliche Lösungen:")
        print("1. Stellen Sie sicher, dass der Flask-Server läuft.")
        print("2. Überprüfen Sie, ob die URL korrekt ist (Standard: http://127.0.0.1:5000/api oder http://localhost:5000/api)")
        print("3. Falls der Server auf einem anderen Port läuft, aktualisieren Sie die BASE_URL-Variable")
        print("4. Falls der Server auf einem anderen Host läuft, aktualisieren Sie die URL entsprechend")
        return False

def dokumentation():
    """
    Dokumentation der API-Funktionen mit Beispielcode
    """
    print("Dokumentation der Zeiterfassungs-API")
    print("=" * 50)
    print("Alle API-Endpunkte erwarten die employee_id als Parameter in der URL.")
    print("Es wird angenommen, dass die employee_id geheim ist und als Authentifizierung dient. Deshalb gibt es keinen Auth-Token.")
    print("\nVerfügbare Endpunkte:")

    # Überprüfen, ob der Server verfügbar ist
    if not check_server_availability():
        print("\nDie API ist nicht verfügbar. Bitte starten Sie zuerst den Flask-Server.")
        print("Verwenden Sie dazu den Befehl: python app.py")
        return

    # 1. Alle Mitarbeiter abrufen
    def get_all_employees():
        """Beispiel: Alle Mitarbeiter abrufen"""
        print("\n1. GET /employees - Alle Mitarbeiter abrufen")
        url = f"{BASE_URL}/employees"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                employees = response.json()
                print("Erfolgreich abgerufen:")
                print(json.dumps(employees, indent=2))
            else:
                print(f"Fehler: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Aufruf: {e}")

    # 2. Einzelnen Mitarbeiter abrufen
    def get_employee(employee_id="101"):
        """Beispiel: Einzelnen Mitarbeiter abrufen"""
        print(f"\n2. GET /employees/{employee_id} - Einzelnen Mitarbeiter abrufen")
        url = f"{BASE_URL}/employees/{employee_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                employee = response.json()
                print("Erfolgreich abgerufen:")
                print(json.dumps(employee, indent=2))
            else:
                print(f"Fehler: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Aufruf: {e}")

    # 3. Zeiterfassung starten
    def start_tracking(employee_id="101"):
        """Beispiel: Zeiterfassung starten"""
        print(f"\n3. POST /employees/{employee_id}/tracking/start - Zeiterfassung starten")
        url = f"{BASE_URL}/employees/{employee_id}/tracking/start"
        try:
            response = requests.post(url)
            if response.status_code == 200:
                result = response.json()
                print("Erfolgreich gestartet:")
                print(json.dumps(result, indent=2))
            else:
                print(f"Fehler: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Aufruf: {e}")

    # 4. Zeiterfassung stoppen
    def stop_tracking(employee_id="101"):
        """Beispiel: Zeiterfassung stoppen"""
        print(f"\n4. POST /employees/{employee_id}/tracking/stop - Zeiterfassung stoppen")
        url = f"{BASE_URL}/employees/{employee_id}/tracking/stop"
        try:
            response = requests.post(url)
            if response.status_code == 200:
                result = response.json()
                print("Erfolgreich gestoppt:")
                print(json.dumps(result, indent=2))
            else:
                print(f"Fehler: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Aufruf: {e}")

    # 5. Arbeitsstunden eintragen
    def log_hours(employee_id="101", date_str="2023-10-01", hours=8):
        """Beispiel: Arbeitsstunden eintragen"""
        print(f"\n5. POST /employees/{employee_id}/hours - Arbeitsstunden eintragen")
        url = f"{BASE_URL}/employees/{employee_id}/hours"
        data = {
            "date": date_str,
            "hours": hours
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print("Erfolgreich eingetragen:")
                print(json.dumps(result, indent=2))
            else:
                print(f"Fehler: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Aufruf: {e}")

    # 6. Arbeitsstunden abrufen
    def get_hours(employee_id="101"):
        """Beispiel: Arbeitsstunden abrufen"""
        print(f"\n6. GET /employees/{employee_id}/hours - Arbeitsstunden abrufen")
        url = f"{BASE_URL}/employees/{employee_id}/hours"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                hours_data = response.json()
                print("Erfolgreich abgerufen:")
                print(json.dumps(hours_data, indent=2))
            else:
                print(f"Fehler: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Aufruf: {e}")

    # 7. Warnungen überprüfen
    def check_warnings(employee_id="101"):
        """Beispiel: Warnungen überprüfen"""
        print(f"\n7. GET /employees/{employee_id}/check_warnings - Warnungen überprüfen")
        url = f"{BASE_URL}/employees/{employee_id}/check_warnings"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                warnings = response.json()
                print("Warnungsstatus:")
                print(json.dumps(warnings, indent=2))
            else:
                print(f"Fehler: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Aufruf: {e}")

    # Beispielaufrufe
    get_all_employees()
    get_employee()
    start_tracking()
    stop_tracking()
    log_hours()
    get_hours()
    check_warnings()

def main():
    """Hauptfunktion zur Ausführung der API-Dokumentation"""
    dokumentation()

if __name__ == "__main__":
    main()
