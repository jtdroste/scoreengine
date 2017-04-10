###########################################################
###############  DO NOT EDIT THIS SECTION!  ###############
###########################################################

import os

class Service:
	def __init__(self, name, group, check, *data):
		self.name = name
		self.group = group
		self.check = check
		self.data = data


class Data:
	def __init__(self, key, value, **kwargs):
		self.key = key
		self.value = value
		self.kwargs = kwargs


###########################################################
####################  EDIT BELOW HERE  ####################
###########################################################

# Database configuration
DATABASE_URI = "mysql://user:pass@localhost:3306/scoreengine"
DATABASE_EXTRA = {
	"pool_size": 40,
	"max_overflow": 60,
}

# Bank-API configuration
BANK = {
	"ENABLED": False,
	"SERVER": "localhost",
	"USER": "username",
	"PASS": "password"
}

# Configuration for our task queue
CELERY = {
	"BROKER": "pyamqp://guest@localhost//",  # None is safe to use if unavailable
	"WORKER": {
		"concurrency": 20,
		"loglevel": "INFO",
		"traceback": True
	}
}

# This section is for overriding check-specific
# configuration
CHECKS = {
	"icmp": {
		"timeout": 5
	}
}

# Amount of teams.  As a note, MAX_NUM is not
# inclusive
TEAMS = {
	"MIN_NUM": 1,
	"MAX_NUM": 11,
}

# All the services. Woah!
SERVICES = [
	# ICMP Ping
	Service(
		"Ubuntu Clients",
		"icmp",
		"check_icmp",
		Data("IP", "10.{team}.1.10", edit=False),
		Data("IP", "10.{team}.1.20", edit=False)
	),

	# ICMP Ping
	Service(
		"Windows Clients",
		"icmp",
		"check_icmp",
		Data("IP", "10.{team}.1.30", edit=False),
		Data("IP", "10.{team}.1.40", edit=False)
	),

	# Active Directory
	Service(
		"AD",
		"ldap",
		"check_ldap_lookup",
		Data("HOST", "10.{team}.1.50", order=0),
		Data("DOMAIN", "loribird{team}.win", edit=False, order=1),
		Data("USERPASS", "jgeistBird||Changeme123!", order=2),
		Data("USERPASS", "jdrosteBird||Changeme123!", order=2)
	),

	# DNS
	Service(
		"DNS",
		"dns",
		"check_dns",
		Data("HOST", "10.{team}.1.50", order=0),
		Data("LOOKUP", "loribird{team}.win", order=1),
		Data("TYPE", "A", order=2),
		Data("EXPECTED", "10.{team}.1.50", order=3)
	),

	# Wordpress
	Service(
		"HTTP Web",
		"http",
		"check_wordpress",
		Data("HOST", "10.{team}.2.2", order=0),
		Data("PORT", "80", order=1),
		Data("USERPASS", "BirdMan||changeme", order=2),
	),

	# HTTP Mail Client
	Service(
		"HTTP Mail",
		"http",
		"check_http",
		Data("HOST", "10.{team}.2.4", order=0),
		Data("PORT", "80", order=1)
	),

	# FTP
	Service(
		"FTP",
		"ftp",
		"check_upload_download",
		Data("HOST", "10.{team}.2.5", order=0),
		Data("USERPASS", "bigbird||Lorirox123", order=1)
	),

	# IMAP
	Service(
		"IMAP",
		"imap",
		"check_imap_login",
		Data("HOST", "10.{team}.2.4", order=0),
		Data("PORT", "143", order=1),
		Data("USERPASS", "backups||changeme", order=2)
	),

	# MySQL
	Service(
		"DB",
		"mysql",
		"check_wordpress",
		Data("HOST", "10.{team}.2.3", order=0),
		Data("PORT", "3306", order=1),
		Data("USER", "MariaBird", order=2),
		Data("PASS", "lori4prez", order=3),
		Data("DB_LOOKUP", "wordpress", order=4),
		Data("BLOG_NAME", "Lori Bird 4 Prez 2k17", order=5)
	),
]
