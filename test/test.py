#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from djconnection import DJConnection
from djconnection.DJObjects import DJFinding


def test_finding_creation():

    # TEST PREPARATION

    logger = logging.getLogger("MAIN")
    logging.basicConfig(format='%(name)-11s | %(asctime)s - %(levelname)-5s - %(message)s', level=logging.DEBUG)


    # TEST DATA

    findings = [
        DJFinding(title="New kerberoastable RC4 encrypted TGS",
        description="Following hashes were found:\n- abc\n- def\n- ghi",
        impact="Kerberoastable TGS tickets are susceptible for offline bruteforce attacks.\n Additionally RC4 is a weak algoritm.",
        severity="High",
        mitigation="If this TGS is crackable:\n- rotate password\n- upgrade encryption algoritm to AES"),
        DJFinding(title="New kerberoastable AES encrypted TGS",
        description="Following hashes were found:\n- jkl\n- mno\n- pkr",
        impact="Kerberoastable TGS tickets are susceptible for offline bruteforce attacks.\n Additionally RC4 is a weak algoritm.",
        severity="Medium",
        mitigation="If this TGS is crackable:\n- rotate password")
    ]

    test_findings = []

    # TEST RUN 1 - TestTool unverified issues

    djclient = DJConnection.Client(os.environ['API_ENDPOINT'], os.environ['API_KEY'])

    logger.info(f"DJConnection {djclient.__version__} - Test Script")

    tool = "TestTool_individual"

    for finding in findings:
        findingId = djclient.create_finding(tool, finding).id
        logger.info(f"Created finding with ID: {str(findingId)}")
        test_findings.append(findingId)

    # TEST RUN 2 - TestTool verified issues

    tool = "TestTool_verified"

    findings = [
        DJFinding(title="New AS-REP roastable account found.",
        description="Following account was found: abcdef",
        impact="AS-REP roastable accounts are susceptible for offline bruteforce attacks.",
        severity="High",
        mitigation="Make sure there are no accounts configured with \"Do not require Kerberos preauthentication\".",
        verified=True)
    ]

    for finding in findings:
        findingId = djclient.create_finding(tool, finding).id
        logger.info(f"Created finding with ID: {str(findingId)}")
        test_findings.append(findingId)

    # Testing retrieval of previously added findings based on their ID's

    for findingId in test_findings:
        finding = djclient.get_finding(findingId)
        logger.info(f"Succesfully retrieved finding with:")
        logger.info(f"ID: {finding.id}")
        logger.info(f"TITLE: {finding.title}")
    

if __name__ == "__main__":

    test_finding_creation()
