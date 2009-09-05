#!/usr/bin/env python

######################################################################
#  Copyright (c) 2000, Sean Reifschneider, tummy.com, ltd.
#  All Rights Reserved
#
#  High-level classes for implementing command/response clients and
#  servers in Python.  Though the server is much more highly developed
#  than the client at this point.
#
#  ftp://ftp.tummy.com/pub/tummy/cccheck/
######################################################################
#
# The contents of this file are subject to the Mozilla Public License
# Version 1.0 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
#
# The Original Code is cccheck.py, released October 16, 2000
# The Initial Developer of the Original Code is tummy.com, ltd.
# Portions created by tummy.com, ltd. are Copyright (C) 2000
# tummy.com, ltd. All Rights Reserved.
#
# Contributor(s): ______________________________________. 
#
######################################################################


revision = "$Revision: 1.1.1.1 $"
rcsid = "$Id: cccheck.py,v 1.1.1.1 2000/10/16 22:35:25 jafo Exp $"

__doc__ = '''Module for dealing with credit card numbers.

This module implements several methods for dealing with credit card
numbers.  In particular, checking for legal numbers (based on the
check digit) and generating the check digit.

Example:

	import cccheck

	number = '21310000000000'
	number = number + cccheck.genMod10(number)
	print 'Generated: ', number
	print 'Verify: ', cccheck.verifyCardNumber(number)
'''

###################
def verifyMod10(s):
	'''Check a credit card number for validity using the mod10 algorithm.

	RETURNS: True if the card number is valid, false otherwise.
	ARGUMENTS:
		- s -- (String) Card number to verify.  Must only contain digits.
	'''
	double = 0
	sum = 0
	for i in range(len(s) - 1, -1, -1):
		for c in str((double + 1) * int(s[i])): sum = sum + int(c)
		double = (double + 1) % 2
	return((sum % 10) == 0)


################
def genMod10(s):
	'''Generate a mod-10 check digit.

	RETURNS: (String) Check digit.
	ARGUMENTS:
		- s -- (String) Card number to generate check from (should not include
				check digit).  Must only contain digits.
	'''
	double = 1
	sum = 0
	for i in range(len(s) - 1, -1, -1):
		for c in str((double + 1) * int(s[i])): sum = sum + int(c)
		double = (double + 1) % 2
	return(str(10 - (sum % 10)))


####################
def stripCardNum(s):
	'''Return card number with all non-digits stripped.

	RETURNS: (String) String consisting only of digits in input string.
	ARGUMENTS:
		- s -- (String) String to remove non-digits from.
	'''
	import re
	return(re.sub(r'[^0-9]', '', s))


########################
def verifyCardNumber(s):
	'''Return card type string if legal, None otherwise.
	Check the card number and return a string representing the card type if
	it could be a valid card number.

	RETURNS: (String) Credit card type string if legal.
			(None) if invalid.
	ARGUMENTS:
		- s -- (String) Card number to check.  Any non-digits are stripped out.
	'''
	s = stripCardNum(s)
	for name, prefix, length, algorithm in ccInfo:
		if len(s) == length and s[:len(prefix)] == prefix:
			if algorithm(s):
				return(name)
			break
	return(None)


##########################################
#  table with credit card type information
ccInfo = (
	#  type, prefix, length, verify algorithm
	( 'Visa', '4', 16, verifyMod10 ),
	( 'Visa', '4', 13, verifyMod10 ),
	( 'Mastercard', '51', 16, verifyMod10 ),
	( 'Mastercard', '52', 16, verifyMod10 ),
	( 'Mastercard', '53', 16, verifyMod10 ),
	( 'Mastercard', '54', 16, verifyMod10 ),
	( 'Mastercard', '55', 16, verifyMod10 ),
	( 'Discover', '6011', 16, verifyMod10 ),
	( 'American Express', '34', 15, verifyMod10 ),
	( 'American Express', '37', 15, verifyMod10 ),
	( 'Diners Club/Carte Blanche', '300', 14, verifyMod10 ),
	( 'Diners Club/Carte Blanche', '301', 14, verifyMod10 ),
	( 'Diners Club/Carte Blanche', '302', 14, verifyMod10 ),
	( 'Diners Club/Carte Blanche', '303', 14, verifyMod10 ),
	( 'Diners Club/Carte Blanche', '304', 14, verifyMod10 ),
	( 'Diners Club/Carte Blanche', '305', 14, verifyMod10 ),
	( 'Diners Club/Carte Blanche', '36', 14, verifyMod10 ),
	( 'Diners Club/Carte Blanche', '38', 14, verifyMod10 ),
	( 'JCB', '3', 16, verifyMod10 ),
	( 'JCB', '2131', 15, verifyMod10 ),
	( 'JCB', '1800', 15, verifyMod10 ),
	)

##########################
if __name__ == '__main__':
	number = '21310000000000'
	number = number + genMod10(number)
	print 'Generated: ', number
	print 'Verify: ', verifyCardNumber(number)
	print 'strip:', stripCardNum('4234-5678.9012/3456')
	print 'strip:', stripCardNum('4234 5678 9012 3456')
	print 'verify:', verifyCardNumber('4234 5678/9012-3456')
	print 'verify:', verifyCardNumber('5123456789012346')
	print 'verify:', verifyCardNumber('4992739871600')
	print 'verify:', verifyCardNumber('4992739871600008')
	print 'verify:', verifyCardNumber('6011000000000004')
	print 'verify:', verifyCardNumber('340000000000009')
	print 'verify:', verifyCardNumber('370000000000002')
	print 'verify:', verifyCardNumber('30000000000004')
	print 'verify:', verifyCardNumber('3100000000000003')
