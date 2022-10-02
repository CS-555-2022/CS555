# Yiwen Wang

from US30_31_file import *
import sys
import datetime

# List all living people over 30 who have never been married in a GEDCOM file
def list_single():
	file_name = sys.argv[1]
	info = get_info(file_name)
	alone_forever = []
	for ind in info['individuals']:
		birth = ind['birthday']
		dt = datetime.datetime.now() - datetime.timedelta(days=30*365)
		if birth < dt and ind['spouse'] == None:
			alone_forever.append(ind['id'])

	if len(alone_forever) == 0:
		return 1
	else:
		print(alone_forever)
	return 0
        
if __name__ == '__main__':
	list_single()