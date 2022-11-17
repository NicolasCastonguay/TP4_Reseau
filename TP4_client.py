"""\
GLO-2000 Travail pratique 4 - Client
Noms et numéros étudiants:
- Nicolas Castonguay 536 774 848
-
-
"""

import argparse
import getpass
import json
import socket
import sys
import getpass
import glosocket
import gloutils


class Client:
    """Client pour le serveur mail @glo2000.ca."""

    def __init__(self, destination: str) -> None:
        """
        Prépare et connecte le socket du client `_socket`.

        Prépare un attribut `_username` pour stocker le nom d'utilisateur
        courant. Laissé vide quand l'utilisateur n'est pas connecté.
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(destination, gloutils.APP_PORT)
        self._username = ""

    def _register(self) -> None:
        """
        Demande un nom d'utilisateur et un mot de passe et les transmet au
        serveur avec l'entête `AUTH_REGISTER`.

        Si la création du compte s'est effectuée avec succès, l'attribut
        `_username` est mis à jour, sinon l'erreur est affichée.
        """
        input_username = input("Entrez votre nom d'utilisateur : ")
        self._password = getpass.getpass("Entrez votre mot de passe : ")
        auth_payload = gloutils.AuthPayload(input_username, self._password)
        glosocket.send_msg(self._socket, gloutils.GloMessage(
            gloutils.Headers.AUTH_REGISTER, auth_payload))
        msg_received = json.load(glosocket.recv_msg(self._socket))
        if msg_received["header"] == gloutils.Headers.OK:
            self._username = input_username
        else:
            print(msg_received["payload"])

    def _login(self) -> None:
        """
        Demande un nom d'utilisateur et un mot de passe et les transmet au
        serveur avec l'entête `AUTH_LOGIN`.

        Si la connexion est effectuée avec succès, l'attribut `_username`
        est mis à jour, sinon l'erreur est affichée.
        """
        input_username = input("Entrez votre nom d'utilisateur : ")
        self._password = getpass.getpass("Entrez votre mot de passe : ")
        auth_payload = gloutils.AuthPayload(input_username, self._password)
        glosocket.send_msg(self._socket, gloutils.GloMessage(
            gloutils.Headers.AUTH_LOGIN, auth_payload))
        msg_received = json.load(glosocket.recv_msg(self._socket))
        if msg_received["header"] == gloutils.Headers.OK:
            self._username = input_username
        else:
            print(msg_received["payload"])

    def _quit(self) -> None:
        """
        Préviens le serveur de la déconnexion avec l'entête `BYE` et ferme le
        socket du client.
        """
        glosocket.send_msg(
            self._socket, gloutils.GloMessage(gloutils.Headers.BYE))

    def _read_email(self) -> None:
        """
        Demande au serveur la liste de ses courriels avec l'entête
        `INBOX_READING_REQUEST`.

        Affiche la liste des courriels puis transmet le choix de l'utilisateur
        avec l'entête `INBOX_READING_CHOICE`.

        Affiche le courriel à l'aide du gabarit `EMAIL_DISPLAY`.

        S'il n'y a pas de courriel à lire, l'utilisateur est averti avant de
        retourner au menu principal.
        """
        glosocket.send_msg(self._socket, gloutils.GloMessage(
            gloutils.Headers.INBOX_READING_REQUEST))
        msg_received = json.loads(glosocket.recv_msg(self._socket))
        email_list = msg_received["payload"]
        if email_list.lenght() == 0:
            sys.exit(1)
        for email in email_list:
            print(email)
        choice = input("Entrez le numéro du courriel désiré : ")
        glosocket.send_msg(self._socket, gloutils.GloMessage(
            gloutils.Headers.INBOX_READING_CHOICE, choice))
        email_received = json.loads(
            glosocket.recv_msg(self._socket))["payload"]
        email_info = json.loads(email_received)
        print(gloutils.EMAIL_DISPLAY.format(email_info))

    def _send_email(self) -> None:
        """
        Demande à l'utilisateur respectivement:
        - l'adresse email du destinataire,
        - le sujet du message,
        - le corps du message.

        La saisie du corps se termine par un point seul sur une ligne.

        Transmet ces informations avec l'entête `EMAIL_SENDING`.
        """
        dest = input("Entrez l'email du destinataire : ")
        subject = input("Entrez le sujet du email : ")
        print("Entrez le contenu de votre courriel : ")
        body = ""
        while True:
            line = input()
            if line == ".":
                break
            body += line + "\n"
        glosocket.send_msg(self._socket, json.dumps(gloutils.GloMessage(header=gloutils.Headers.EMAIL_SENDING,
                                                                        payload=gloutils.EmailContentPayload(date=gloutils.get_current_utc_time(), subject=subject, content=body, destination=dest, sender=self._username))))

    def _check_stats(self) -> None:
        """
        Demande les statistiques au serveur avec l'entête `STATS_REQUEST`.

        Affiche les statistiques à l'aide du gabarit `STATS_DISPLAY`.
        """

    def _logout(self) -> None:
        """
        Préviens le serveur avec l'entête `AUTH_LOGOUT`.

        Met à jour l'attribut `_username`.
        """

    def run(self) -> None:
        """Point d'entrée du client."""
        should_quit = False

        while not should_quit:
            if not self._username:
                # Authentication menu
                pass
            else:
                # Main menu
                pass


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destination", action="store",
                        dest="dest", required=True,
                        help="Adresse IP/URL du serveur.")
    args = parser.parse_args(sys.argv[1:])
    client = Client(args.dest)
    client.run()
    return 0


if __name__ == '__main__':
    sys.exit(_main())
