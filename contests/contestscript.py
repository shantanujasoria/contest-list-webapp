import requests
from time import gmtime, strftime

### Authentication Data
headers = {
	'Authorization':'ApiKey GT_18:b8c4d6c7c798976bfd8a9f84c7051c3dec355cbf'
}

### Current Date Time
cur_date = strftime("%Y-%m-%d",gmtime()) + "T" + strftime("%H",gmtime()) + "%3A" + strftime("%M",gmtime()) + "%3A" + strftime("%S",gmtime())

### Query URL
url = 'https://clist.by:443/api/v1/contest/?end__gte=' + cur_date + '&order_by=start'


### Response Result
res = requests.get(url, headers = headers).json()['objects']

### Platforms
Platforms = ['codeforces', 'codechef', 'hackerrank', 'hackerearth', 'atcoder', 'csacademy', 'topcoder']


### Type on HE
Type_on_HE = ['Easy', 'Circuits'] 

### Type on TC
Type_on_TC = ['SRM']

### Check for a valid contest
def check(contest):
	for pt in Platforms:
		if pt in contest['href']:
			if pt == 'hackerearth':
				for typ in Type_on_HE:
					if typ in contest['event']:
						return True
			elif pt == 'topcoder':
				for typ in Type_on_TC:
					if typ in contest['event']:
						return True
			else:
				return True
	return False

def get_contests():
	contest_list = []
	for i in res:
		if check(i):
			contest_list.append(i)
	return contest_list
