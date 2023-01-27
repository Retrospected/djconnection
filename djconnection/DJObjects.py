import logging

class DJFinding():
    def __init__(self, title = None, description = None, impact = None, mitigation = None, severity = None, verified = False):

        self.logger = logging.getLogger("DJFinding")

        if title is None:
            raise Exception("'title' argument of the DJFinding object is mandatory.")
        if description is None:
            raise Exception("'description' argument of the DJFinding object is mandatory.")
        if impact is None:
            raise Exception("'impact' argument of the DJFinding object is mandatory.")
        if severity is None:
            raise Exception("'severity' argument of the DJFinding object is mandatory.")
        if mitigation is None:
            raise Exception("'mitigation' argument of the DJFinding object is mandatory.")

        self.title = title
        self.impact = impact
        self.description = description
        self.severity = severity
        self.mitigation = mitigation
        self.verified = verified
