import djclient
from djclient.rest import ApiException
from pprint import pprint
import logging
import datetime
import time
from djconnection.DJObjects import DJFinding

class Client:
    def __init__(self, API_ENDPOINT, API_KEY):

        self.product_name = "MAC"
        self.product_description = "Testing this"
        self.dj_user_id = 1 # user ID (user of which the API key belongs to)
        self.limit = 1000000
        self.logger = logging.getLogger("Client")
        self.logger.info("STARTED")
        self.configuration = djclient.Configuration()
        # Configure API key authorization: api_key
        self.configuration.api_key['Authorization'] = API_KEY
        
        #Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
        self.configuration.api_key_prefix['Authorization'] = 'Token'

        # Defining host is optional and default to http://localhost:8080/api/v2
        self.configuration.host = API_ENDPOINT

    def create_findings(self, tool, findings):
        test_id = self.get_test(tool)
        for finding in findings:
            self.create_finding(tool, finding, test_id)

    def create_finding(self, tool, finding, test_id = None):
        self.logger.info(f"Creating finding for tool: {tool}")

        api_instance = djclient.FindingsApi(djclient.ApiClient(self.configuration))
        if not test_id:
            test_id = self.get_test(tool)
        
        if finding.severity.lower() == "low":
            numerical_severity = "S1"
        elif finding.severity.lower() == "medium":
            numerical_severity = "S2"
        elif finding.severity.lower() == "high":
            numerical_severity = "S3"
        elif finding.severity.lower() == "critical":
            numerical_severity = "S4"
        else:
            numerical_severity = "S0"
        
        try:
            finding = djclient.FindingCreate(test=test_id, 
            found_by=[self.dj_user_id], 
            mitigation=finding.mitigation, 
            title=finding.title, 
            severity=finding.severity, 
            description=finding.description, 
            impact=finding.impact,
            active=True,
            verified=False,
            numerical_severity=numerical_severity)
            
            api_response = api_instance.findings_create(finding)
        except ApiException as e:
            self.logger.error("Exception when calling FindingsApi->findings_create: %s\n" % e)

    def get_test(self, tool):

        self.logger.info(f"Getting Test ID for tool: {tool}")
        # get test based on Tool and Date, if the combination doesn't exist, create test!

        engagement_id = self.get_engagement()

        api_instance = djclient.TestsApi(djclient.ApiClient(self.configuration))
        tests_list = api_instance.tests_list(limit=self.limit, engagement=engagement_id)

        for test in tests_list.results:            
            target_start = datetime.date.today()
            target_end = datetime.date.today()

            if test.engagement == engagement_id and test.title == tool and test.target_start.date() == target_start and test.target_end.date() == target_end:
                self.logger.info(f"Test found with ID: {str(test.id)}")
                return test.id

        # create test
        
        test_type_id = self.get_test_type()

        target_start = datetime.datetime.now()
        target_end = datetime.datetime.now()
        
        try:
            test = djclient.TestCreate(engagement=engagement_id,title=tool,target_start=target_start,target_end=target_end,test_type=test_type_id)
            api_response = api_instance.tests_create(test)
            self.logger.info(f"Test created with ID: {str(api_response.id)}")
            return api_response.id

        except ApiException as e:
            self.logger.error("Exception when calling TestsApi->tests_create: %s\n" % e)

    def get_test_type(self):
        self.logger.info(f"Getting Test Type ID for: "+self.product_name)
        
        api_instance = djclient.TestTypesApi(djclient.ApiClient(self.configuration))
        test_types_list = api_instance.test_types_list(limit=self.limit)

        for test_type in test_types_list.results:
            if test_type.name == self.product_name:
                self.logger.info(f"Test type found with ID: {str(test_type.id)}")
                return test_type.id

        try:
            test_type = djclient.TestType(name=self.product_name)
            api_response = api_instance.test_types_create(test_type)
            self.logger.info(f"Test type created with ID: {str(api_response.id)}")
            return api_response.id

        except ApiException as e:
            self.logger.error("Exception when calling TestTypesApi->test_types_create: %s\n" % e)

    def get_engagement(self):
        today = datetime.date.today()      
        year = today.year

        self.logger.info(f"Getting Engagement ID for year: {str(year)}")       
        
        product_id = self.get_product()

        # get engagement based on year in the product "CAM"
        # if it doesn't exist, create engagement

        api_instance = djclient.EngagementsApi(djclient.ApiClient(self.configuration))

        engagements_list = api_instance.engagements_list(limit=self.limit)

        for engagement in engagements_list.results:
            if engagement.name == str(year) and engagement.product == product_id:
                self.logger.info(f"Engagement found with ID: {str(engagement.id)}")
                return engagement.id

        # create engagement
        self.logger.info(f"Engagement not found, creating engagement for year: {year}")
        

        target_start = f"{year}-01-01" #being of {year}, format: 2022-11-07T12:59:51.223Z
        target_end = f"{year}-12-31" #end of {year}, format: 2022-11-07T12:59:51.223Z
        status = 'In Progress'
        try:
            engagement = djclient.Engagement(name=str(year),product=product_id,target_start=target_start,target_end=target_end,status=status) 
            api_response = api_instance.engagements_create(engagement)
            self.logger.info(f"Engagement created with ID: {str(api_response.id)}")

            return api_response.id

        except ApiException as e:
            self.logger.error("Exception when calling EngagementsApi->engagements_create: %s\n" % e)

    def get_product(self):
        self.logger.info(f"Getting Product ID for Product: {self.product_name}")

        api_instance = djclient.ProductsApi(djclient.ApiClient(self.configuration))

        products_list = api_instance.products_list(limit=self.limit)

        for product in products_list.results:
            if product.name == self.product_name:
                self.logger.info(f"Product found with ID: {str(product.id)}")
                return product.id

        try:        
            product = djclient.Product(name=self.product_name,description=self.product_description,prod_type=2)

            api_response = api_instance.products_create(product)
            self.logger.info(f"Product created with ID: {str(api_response.id)}")

            return api_response.id

        except ApiException as e:
            self.logger.debug("Exception when calling ProductsApi->products_create: %s\n" % e)