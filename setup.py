import config
from scoring import engine, Session
from scoring.models import *


try:
	# Initialize DB
	session = Session()
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

	# Create teams
	teams = {}
	for i in range(config.TEAMS["MIN_NUM"], config.TEAMS["MAX_NUM"]):
		teams[i] = Team("Team %d" % i)
		session.add(teams[i])

	# Create services
	for sname, sconfig in config.SERVICES.iteritems():
		service = Service(sname, sconfig.group, sconfig.check)
		session.add(service)

		# Assign service to teams
		for i in teams:
			session.add_all([
				TeamService(
					teams[i],
					service,
					datum.key,
					datum.value % {"team": i},
					**datum.kwargs
				)
				for datum in sconfig.data
			])

	# We're done! Commit (and hope it works...)
	session.commit()

except Exception as e:
	print "Error: %s" % e
	session.rollback()

	import traceback
	traceback.print_exc()

finally:
	session.close()
