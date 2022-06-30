from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb
)
from cdk_dynamo_table_view import TableViewer

from diagrams import Cluster, Node
from diagrams.aws.database import Dynamodb
from diagrams.aws.compute import Lambda


class HitCounter(Construct):
    """Construct that uses a DynamoDB table to log the hits to a downstream lambda function.

    includes:
      - a TableViewer for DynamoDB using an API gateway + lambda function (external package)
      - a diagram of the infrastructure components
    """

    @property
    def handler(self) -> _lambda.IFunction:
        return self._handler

    @property
    def table(self) -> ddb.ITable:
        return self._table

    def __init__(self, scope: Construct, _id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, _id, **kwargs)

        self._table = ddb.Table(
            self, "Hits",
            partition_key=ddb.Attribute(name='path', type=ddb.AttributeType.STRING)
        )

        self._handler = _lambda.Function(
            self, 'HitCountHandler',
            code=_lambda.Code.from_asset('lambda'),
            handler='hitcount.handler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            environment={
                "HITS_TABLE_NAME": self.table.table_name,
                "DOWNSTREAM_FUNCTION_NAME": downstream.function_name
            }
        )

        TableViewer(
            self, "YiewHitCounter",
            title="Hits on 'Hello' Lambda",
            table=self.table,
            sort_by='-hits'
        )

        # Allow our handler to read/write to the DynamoDB
        self.table.grant_read_write_data(self.handler)

        # Allow the handler to invoke the downstream function
        downstream.grant_invoke(self.handler)

    @staticmethod
    def diagram(cluster_name: str) -> Node:
        """returns a diagram of the infrastructure components"""
        with Cluster(cluster_name, direction="TB"):
            _lambda_downstream = Lambda("HitCounterHandler")
            _ddb = Dynamodb("Hits")
            return _lambda_downstream >> _ddb
