# import os

# from iconsdk.builder.transaction_builder import DeployTransactionBuilder
# from iconsdk.builder.call_builder import CallBuilder
# from iconsdk.libs.in_memory_zip import gen_deploy_data_content
# from iconsdk.signed_transaction import SignedTransaction
# from iconsdk.icon_service import IconService
# from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS
# from iconsdk.exception import JSONRPCException
# import json

# from iconsdk.providers.http_provider import HTTPProvider
# from iconsdk.builder.transaction_builder import CallTransactionBuilder, TransactionBuilder, DeployTransactionBuilder
# from iconsdk.wallet.wallet import KeyWallet
# from iconsdk.utils.convert_type import convert_hex_str_to_int
# import time
# from .repeater import retry
# from iconservice import Address

# DIR_PATH = os.path.abspath(os.path.dirname(__file__))
# DEPLOY = ['sicx','staking']




# class TestTest(IconIntegrateTestBase):
#     TEST_HTTP_ENDPOINT_URI_V3 = "https://zicon.net.solidwallet.io/api/v3"
#     SCORES = os.path.abspath(os.path.join(DIR_PATH, '..'))

#     def setUp(self):
#         super().setUp()
#         self.contracts = {}
#         private2="093f12dba9dc75da81ecafc88de73ef9b311b555939aeb5a875dc6ad8feef424"
#         self._test2 = KeyWallet.load(bytes.fromhex(private2))
#         # WARNING: ICON service emulation is not working with IISS.
#         # You can stake and delegate but can't get any I-Score for reward.
#         # If you want to test IISS stuff correctly, set self.icon_service and send requests to the network
#         # self.icon_service = None

#         self.icon_service = IconService(HTTPProvider(self.TEST_HTTP_ENDPOINT_URI_V3))
#         # If you want to send requests to the network, un   comment next line and set self.TEST_HTTP_ENDPOINT_URI_V3
#         # # install SCORE
#         # self._score_address = self._deploy_score()['scoreAddress']

#         # # Deploy SCORE
#         # for address in DEPLOY:
#         #     self.SCORE_PROJECT = self.SCORES + "/" + address
#         #     print(self.SCORE_PROJECT)
#         #     print('======================================================================')
#         #     print('Deploying '+ address + 'Contract in Testnet')
#         #     print('----------------------------------------------------------------------')
#         #     self.contracts[address] = self._deploy_score()['scoreAddress']
#         # self._setVariablesAndInterface()


#     #Process the transaction in pagoda testnet
#     @retry(JSONRPCException, tries=10, delay=1, back_off=2)
#     def _get_tx_result(self,_tx_hash):
#         tx_result = self.icon_service.get_transaction_result(_tx_hash)
#         return tx_result

#     @retry(JSONRPCException, tries=10, delay=1, back_off=2)
#     def get_tx_result(self,_call):
#         tx_result = self.icon_service.call(_call)
#         return tx_result    

#     def _setVariablesAndInterface(self):
#         print('======================================================================')
#         print('Set Variable and Interface')
#         print('----------------------------------------------------------------------')
#         settings = [{'contract': 'staking', 'method': 'setSicxAddress',
#                      'params': {'_address': self.contracts['sicx']}},
#                     {'contract': 'sicx', 'method': 'setAdmin',
#                      'params': {'_admin': self.contracts['staking']}}]
#         for sett in settings:

#             print('----------------------------------------------------------------------')
#             print(sett['method'])
#             print('----------------------------------------------------------------------')
#             transaction = CallTransactionBuilder() \
#                 .from_(self._test1.get_address()) \
#                 .to(self.contracts[sett['contract']]) \
#                 .value(0) \
#                 .step_limit(10000000) \
#                 .nid(80) \
#                 .nonce(100) \
#                 .method(sett['method']) \
#                 .params(sett['params']) \
#                 .build()
#             signed_transaction = SignedTransaction(transaction, self._test1)

#             tx_hash = self.icon_service.send_transaction(signed_transaction)

#             _tx_result= self._get_tx_result(tx_hash)

#             self.assertTrue('status' in _tx_result)
#             self.assertEqual(1, _tx_result['status'])


#     def _deploy_score(self, to: str = SCORE_INSTALL_ADDRESS, _type: str = 'install') -> dict:
#         params = {}
#         # Generates an instance of transaction for deploying SCORE.
#         transaction = DeployTransactionBuilder() \
#             .from_(self._test1.get_address()) \
#             .to(to) \
#             .step_limit(100_000_000_000) \
#             .nid(80) \
#             .nonce(100) \
#             .content_type("application/zip") \
#             .content(gen_deploy_data_content(self.SCORE_PROJECT)) \
#             .params(params) \
#             .build()

#         # Returns the signed transaction object having a signature
#         signed_transaction = SignedTransaction(transaction, self._test1)
#         # process the transaction
#         tx_hash = self.icon_service.send_transaction(signed_transaction)
#         _tx_result= self._get_tx_result(tx_hash)
#         print(_tx_result)
#         # checks Transaction result
#         self.assertEqual(True, _tx_result['status'])
#         self.assertTrue('scoreAddress' in _tx_result)
#         return _tx_result

#     def test_score_update(self):
#         # update SCORE
#         print('======================================================================')
#         print('Test Score Update')
#         print('----------------------------------------------------------------------')
#         self.SCORE_PROJECT = self.SCORES + "/" + 'staking'
#         SCORE_PROJECT = os.path.abspath(
#             os.path.join(DIR_PATH, '..')) + "/" + 'staking'
#         tx_result = self._deploy_score('cx25c39ed0d27853e44af8ab2739d6af832f35d533', 'update')
#         # self.assertEqual(
#         #     self.contracts['staking'], tx_result[Address.from_string('cxf73a09e1d4b2bf6c6bdb21a8673ad2420bfe01ff')])

#     # def test_get_sICX_address(self):
#     #     print('======================================================================')
#     #     print('Test Get sICX Address')
#     #     print('----------------------------------------------------------------------')

#     #     _call = CallBuilder().from_(self._test1.get_address()) \
#     #         .to(self.contracts['staking']) \
#     #         .method("getSicxAddress") \
#     #         .build()

#     #     response = self.get_tx_result(_call)
#     #     # check call result
#     #     print (response)
#     #     self.assertEqual(self.contracts['sicx'], response)

