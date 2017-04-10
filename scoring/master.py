from __future__ import print_function
import config
from scoring import celery_app, Session
from scoring.models import Team, Service, TeamService, Check
from datetime import datetime
from time import sleep
from thread import start_new_thread, allocate_lock
import random
import requests
import importlib
import os

"""
ScoringEngine

Responsible for creating new CheckRound objects
at specific intervals
"""


printLock = allocate_lock()

class Master(object):
	def __init__(self, round=0, only_queue=False):
		self.started = datetime.utcnow()
		self.round = round
		self.only_queue = only_queue

	def run(self):
		while True:
			self.round += 1

			start_new_thread(self.new_round, (self.round,))

			sleep(60)

	def new_round(self, round):
		# Make a new session for this thread
		session = Session()

		# Get all the active teams for this round
		teams = []
		for team in session.query(Team).filter(Team.enabled == True):
			teams.append({
				'id': team.id,
				'name': team.name
			})

		# Get all active services for this round
		services = []
		for service in session.query(Service).filter(Service.enabled == True):
			services.append({
				'id': service.id,
				'name': service.name,
				'group': service.group,
				'check': service.check
			})

		# Close the session
		session.close()

		# Start the checks!
		for team in teams:
			for service in services:
				if self.only_queue:
					self.new_check_task.delay(team, service, round)
				else:
					start_new_thread(self.new_check, (team, service, round))


	@staticmethod
	@celery_app.task
	def new_check_task(*args, **kwargs):
		return Master.new_check(*args, **kwargs)

	@staticmethod
	def new_check(team, service, round, dryRun=False):
		check = ServiceCheck(team, service)

		check.run()

		if dryRun:
			printLock.acquire()
			print("---------[ TEAM: {} | SERVICE: {}".format(team["name"], service["name"]))
			for line in check.getOutput():
				print(line)
			print("---------[ PASSED: {}".format(check.getPassed()))
			printLock.release()
		else:
			session = Session()
			session.add(Check(team["id"], service["id"], round, check.getPassed(), "\n".join(check.getOutput())))
			session.commit()
			session.close()

			# Print out some data
			printLock.acquire()
			print("Round: {:04d} | {} | Service: {} | Passed: {}".format(round, team["name"].ljust(8), service["name"].ljust(15), check.getPassed()))
			printLock.release()

			# Tell the Bank API to give some money
			if check.getPassed() and config.BANK["ENABLED"]:
				r = requests.post("http://{}/internalGiveMoney".format(config.BANK["SERVER"]), data={'username': config.BANK["USER"], 'password': config.BANK["PASS"], 'team': team["id"]})

class ServiceCheck(object):
	def __init__(self, team, service):
		self.team = team
		self.service = service

		self.passed = False
		self.output = []

	def run(self):
		# Get all the service data for this check
		session = Session()
		checkDataDB = session.query(TeamService)\
					.filter(TeamService.team_id == self.team["id"])\
					.filter(TeamService.service_id == self.service["id"])\
					.order_by(TeamService.order)
		session.close()

		checkDataInitial = {}
		
		for data in checkDataDB:
			if data.key not in checkDataInitial:
				checkDataInitial[data.key] = []

			checkDataInitial[data.key].append(data.value)

		checkData = {}
		for key, value in checkDataInitial.iteritems():
			if len(value) == 1:
				checkData[key] = value[0]
			else:
				checkData[key] = random.choice(checkDataInitial[key])

		# Special handling of "USERPASS"
		if "USERPASS" in checkData:
			(checkData["USER"], checkData["PASS"]) = checkData["USERPASS"].split("||")

			del checkData["USERPASS"]

		# Call it!
		self.getCheck()(self, checkData)

	def getCheck(self):
		group = importlib.import_module('scoring.checks.{}'.format(self.service["group"]))

		return getattr(group, self.service["check"])

	def addOutput(self, message):
		self.output.append(message)

	def getOutput(self):
		return self.output

	def setPassed(self):
		self.passed = True

	def getPassed(self):
		return self.passed

	def getTeamName(self):
		return self.team["name"]

	def getServiceName(self):
		return self.service["name"]
