import urllib.request
mysql = {'host': 'gamedata.cwrmsieis5r4.us-west-2.rds.amazonaws.com',
         'user': 'kyler',
         'passwd': 'koolio5589',
         'db': 'gamedata'}
webhost = {'host':urllib.request.urlopen("http://169.254.169.254/latest/meta-data/public-ipv4").read()
           }
