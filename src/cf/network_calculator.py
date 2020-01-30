"""
NetworkCalculator.

Lambda backend for CloudFormation custom resources that do networking
related caclulations like the subnet size in bits of a given network cidr
for a specific number of subnets.
"""
from math import log2

from cf.custom_resource import CustomResourceHandler


class NetworkCalculator(CustomResourceHandler):
    """Methods for doing network related calculations."""

    def __init__(self):
        """Override the operations registry with new methods."""
        super().__init__()
        self.operations = {"SubnetSize": self.get_subnet_size}

    @staticmethod
    def get_subnet_size(netmask_bits, subnets):
        """
        Get the subnet size in bits.

        Get the size in bits of a subnet based on the size in bits of
        the network with evenly sized subnets and rounded down to leave
        space in the network if there are an uneven number of subnets
        i.e. not a power of 2.
        """
        subnetmask_bits = netmask_bits + int(log2(subnets))
        return 32 - subnetmask_bits

    def execute(self, operator, operands):
        """Override."""
        if operator not in self.operations.keys():
            raise ValueError("unknown operator")

        if len(operands) < 2:
            raise ValueError("missing input")

        operation = self.operations[operator]
        netmask_bits = int(operands[0])
        subnets = int(operands[1])

        return operation(netmask_bits, subnets)


handler = NetworkCalculator()
