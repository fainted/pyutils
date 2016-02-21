# -*- coding: utf-8 -*-
#
# file: client.py
# author: chenhaotian93@gmail.com
# date: 2016-01-16
#
# RPC(Thrift) client wrap,
# Call RPC interface by its name

try:
    from thrift import Thrift
    from thrift.protocol import TProtocol
    from thrift.protocol import TBinaryProtocol
    from thrift.transport import TSocket, TTransport
except:
    raise ImportError('Make sure have thrift-py installed.')


trans_base = (TTransport.TServerTransportBase, TTransport.CReadableTransport)
trans = TTransport.TFramedTransport
proto = TBinaryProtocol.TBinaryProtocol


class ThriftClient(object):
    """Before using, make sure you have thrift-py installed."""

    def __init__(self, ip, port, cls, transport=trans, protocol=proto):
        """Init thrift client.

        Args:
            ip (str): Thrift service's server IP address.
            port (int): Thrift service's server listening port.
            cls (type): Thrift client class.
            transport (optional type):
                Thrft transport type. Default `TFramedTransport`.
            protocol (optional type):
                Thrift protocol type. Default `TBinaryProtocol`.

        Returns:
            `ThriftClient` object if connect to thrift server OK, else None.

        Raises:
             AtrributeError: Invalid `cls`, `transport` or `protocol`.
             TypeError: Invalid `ip` or `port`
        """

        assert issubclass(trans, trans_base)
        assert issubclass(proto, TProtocol.TProtocolBase)

        try:
            self._transport = transport(TSocket.TSocket(ip, port))
            self._client = cls(protocol(self._transport))

            self._transport.open()
        except Thrift.TException:
            del self

    def __del__(self):
        # Close connection on destroy.
        if hasattr(self, '_transport'):
            self._transport.close()

    def call(self, name, *args):
        """Call thrift service's interfaces and return result.

        Args:
            name (str): RPC interfaces' name in string.
            *args (list): Interfaces' arguments list.

        Returns:
            Whatever Thrift service interfaces' returns.

        Raises:
            AttributeError: Client interface not found.
            AssertError: Invalid interface.
            TypeError: Argument list not fit RPC interface.
        """

        interface = getattr(self._client, name)

        assert callable(interface)
        return interface(*args)

