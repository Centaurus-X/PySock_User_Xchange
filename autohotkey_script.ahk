user_name_1: philipp
password_1: test_123
user_name_2: michael
password_2: hallo321
user_name_3: sebastian
password_3: test_123
user_name_4: bubbie
password_4: blabla

code test balablabla
dsfopdospfkoppü
adslökfaslpdk
dslfm,alpdfm,
irgend ein code bnalalöfmskmfklfmfskmd







"""


; Funktion zum Lesen der Benutzerdaten aus der Textdatei
ReadUserCredentials() {
    FileRead, user_data, user_data.txt
    Loop, parse, user_data, `n, `r
    {
        user := A_LoopField
        StringSplit, user_info, user, :
        user_data_array[user_info1] := user_info2
    }
}

; Funktion zur Überprüfung der Benutzeranmeldung
CheckUserCredentials(username, password) {
    if (user_data_array.HasKey(username)) {
        if (user_data_array[username] = password) {
            MsgBox, Benutzeranmeldung erfolgreich!
            return
        }
    }
    MsgBox, Falscher Benutzername oder Passwort!
}

; Benutzerdaten aus der Textdatei lesen
ReadUserCredentials()

; Benutzer zur Eingabe von Benutzername und Passwort auffordern
InputBox, username, Benutzername, Bitte geben Sie Ihren Benutzernamen ein:
InputBox, password, Passwort, Bitte geben Sie Ihr Passwort ein:, Hide

; Überprüfen der Benutzeranmeldung
CheckUserCredentials(username, password)



"""