import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import importlib

import os
import sys

parpath = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
sys.path.append(parpath)

from notAllowedCode import *

def before():
    import matplotlib.pyplot as plt
    plt.switch_backend("Agg")
    lib.neutralizeFunction(plt.pause)
    # lib.neutralizeFunction(matplotlib.use)

def after():
    import matplotlib.pyplot as plt
    plt.switch_backend("TkAgg")
    importlib.reload(plt)

@t.test(0)
def hasworp_met_twee_dobbelstenen(test):

    # v---- Filter global code from source file -----

    global _fileName

    with open(_fileName, 'r') as f:
        tempfile = f"_{_fileName}.tmp"
        file_contents = f.readlines()
        
    with open(tempfile, 'w') as f:
        state = 0
        for line in file_contents:
            if state == 0:
                if line.startswith('def '):
                    state = 1
                f.write(line)
            elif state == 1:
                if not (line.strip() == '' or line.startswith(' ') or line.startswith("\t") or line.startswith("def ") or line.startswith("#")):
                    state = 2
                    continue
                f.write(line)
            elif state == 2:
                if line.startswith('def '):
                    f.write(line)
                    state = 1

    _fileName = tempfile

    # ^---- Filter global code from source file -----

    notAllowed = {"break": "break"}
    notAllowedCode(test, lib.source(_fileName), notAllowed)

    test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "worp_met_twee_dobbelstenen")
    test.description = lambda : "definieert de functie worp_met_twee_dobbelstenen"
    test.timeout = lambda : 60


@t.passed(hasworp_met_twee_dobbelstenen)
@t.test(10)
def correctDice(test):
	test.test = lambda : assertlib.between(lib.getFunction("worp_met_twee_dobbelstenen", _fileName)(), 2, 12)
	test.description = lambda : "returnt een correcte waarde voor een worp van twee dobbelstenen"
	test.timeout = lambda : 120


@t.passed(correctDice)
@t.test(20)
def hassimuleer_potjeAndsimuleer_groot_aantal_potjes_monopoly(test):

	def testMethod():
		test_potje = assertlib.fileContainsFunctionDefinitions(_fileName, "simuleer_potje_monopoly")
		test_groot_aantal_potjes = assertlib.fileContainsFunctionDefinitions(_fileName, "simuleer_groot_aantal_potjes_monopoly")
		info = ""
		if not test_potje:
			info = "de functie simuleer_potje_monopoly is nog niet gedefinieerd"
		elif not test_groot_aantal_potjes:
			info = "de functie simuleer_potje_monopoly is gedefinieerd :) \n  - de functie simuleer_groot_aantal_potjes_monopoly nog niet"
		return test_potje and test_groot_aantal_potjes, info



	test.test = lambda : testMethod()
	test.description = lambda : "definieert de functie simuleer_potje_monopoly en simuleer_groot_aantal_potjes_monopoly"
	test.timeout = lambda : 60


@t.passed(hassimuleer_potjeAndsimuleer_groot_aantal_potjes_monopoly)
@t.test(30)
def correctAverageTrump(test):

	def testMethod():
		nArguments = len(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName).arguments)

		# Trump mode
		if nArguments == 1:
			testInput = lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(2000)
			test.success = lambda info : "De code werkt correct zonder startgeld"
			if assertlib.sameType(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(100), None):
				test.fail = lambda info : "Zorg ervoor dat de functie simuleer_groot_aantal_potjes_monopoly het gemiddeld aan benodigde worpen returnt en ook alleen deze waarde returnt"

		# Startgeld, 1 speler
		elif nArguments == 2:
			twoArguments = True
			testInput = lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(2000, 1000000)
			if assertlib.sameType(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(100, 100), None):
				test.fail = lambda info : "Zorg ervoor dat de functie simuleer_groot_aantal_potjes_monopoly het gemiddeld aan benodigde worpen returnt en ook alleen deze waarde returnt"

		else:
			testInput = False
			test.fail = lambda info : "Zorg ervoor dat de functie simuleer_groot_aantal_potjes_monopoly bij Trump-mode 1 argument heeft en bij startgeld 2 argumenten"

		if 144 < testInput < 150:
			return True
		else:
			test.fail = lambda info: f"{testInput}"
			return False

	# test.test = lambda : testMethod(), 145, 149)
	test.test = lambda : testMethod()
	test.description = lambda : "Monopoly werkt voor Trump-mode"
	test.timeout = lambda : 120


@t.passed(correctAverageTrump)
@t.test(40)
def correctAverageStartgeld(test):

	def testMethod():
		nArguments = len(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName).arguments)

		if nArguments == 2:
			testInput = lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(5000, 1500)
			if assertlib.sameType(lib.getFunction("simuleer_groot_aantal_potjes_monopoly", _fileName)(10, 1500), None):
				test.fail = lambda info : "Zorg er voor dat de functie simuleer_groot_aantal_potjes_monopoly het gemiddeld aan benodigde worpen returnt en ook alleen deze waarde returnt"
			return testInput
		else:
			return 0

	test.test = lambda : assertlib.between(testMethod(), 184, 189)
	test.description = lambda : "Monopoly werkt met 1500 euro startgeld"
	test.timeout = lambda : 60
