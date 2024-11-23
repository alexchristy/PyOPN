from pyopn import OPNsenseAPI

opn = OPNsenseAPI("https://192.168.199.1", api_key_file="OPNsense.localdomain_apikey.txt")

print(opn.kea.dhcpv4.search_reservation())