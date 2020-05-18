from mp_classes import GetMPMatches, GetMPUser

x = GetMPUser('psn', 'spelamedtobbe')
x.fetch_user()
y = x.get_kd()

print(y)