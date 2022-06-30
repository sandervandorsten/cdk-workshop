from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as api_gw
)
from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.database import Dynamodb

from .hitcounter import HitCounter


class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello_hit_counter_id = "HelloHitCounter"
        lambda_id = "HelloHandler"
        rest_api_id = "RestAPIEndpoint"

        my_lambda = _lambda.Function(
            self, lambda_id,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',
            runtime=_lambda.Runtime.PYTHON_3_9,
        )

        hello_with_counter = HitCounter(
            self, hello_hit_counter_id,
            downstream=my_lambda
        )

        api_gw.LambdaRestApi(
            self, rest_api_id,
            handler=hello_with_counter.handler
        )



        # Manual Diagram Creation
        with Diagram("API Hello World", show=False, filename="images/hello_world_lambda"):

            APIGateway(rest_api_id) >> hello_with_counter.diagram(cluster_name=hello_hit_counter_id) >> Lambda(lambda_id)
