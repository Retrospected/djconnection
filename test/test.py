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
    logger.info("DJConnection v0.1")

    # TEST DATA

    findings = [
        DJFinding(title="New kerberoastable RC4 encrypted TGS",
        description="Following hashes were found:\n- abc\n- def\n- ghi",
        impact="Kerberoastable TGS tickets are suscetible for offline bruteforce attacks.\n Additionally RC4 is a weak algoritm.",
        severity="High",
        mitigation="If this TGS is crackable:\n- rotate password\n- upgrade encryption algoritm to AES"),
        DJFinding(title="New kerberoastable AES encrypted TGS",
        description="Following hashes were found:\n- jkl\n- mno\n- pkr",
        impact="Kerberoastable TGS tickets are suscetible for offline bruteforce attacks.\n Additionally RC4 is a weak algoritm.",
        severity="Medium",
        mitigation="If this TGS is crackable:\n- rotate password")
    ]

    # TEST RUN 1 - TestTool_1

    djclient = DJConnection.Client(os.environ['API_ENDPOINT'], os.environ['API_KEY'])

    tool = "TestTool_1"

    djclient.create_findings(tool, findings)

    # TEST RUN 2 - TestTool_2

    tool = "TestTool_2"

    for finding in findings:
        djclient.create_finding(tool, finding)


if __name__ == "__main__":

    test_finding_creation()
