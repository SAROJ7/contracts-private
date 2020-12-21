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


# class TestTest(IconIntegrateTestBase):
#     TEST_HTTP_ENDPOINT_URI_V3 = "https://zicon.net.solidwallet.io/api/v3"

#     Address = "cxbe0bf2b10de1b47ac6db1d7e03046105a37b5db4"

#     def setUp(self):
#         super().setUp()
#         # WARNING: ICON service emulation is not working with IISS.
#         # You can stake and delegate but can't get any I-Score for reward.
#         # If you want to test IISS stuff correctly, set self.icon_service and send requests to the network

#         self.icon_service = IconService(HTTPProvider(self.TEST_HTTP_ENDPOINT_URI_V3))
#         # If you want to send requests to the network, uncomment next line and set self.TEST_HTTP_ENDPOINT_URI_V3

       

#     @retry(JSONRPCException, tries=10, delay=1, back_off=2)
#     def _get_tx_result(self,_tx_hash):
#         tx_result = self.icon_service.get_transaction_result(_tx_hash)
#         return tx_result

#     # Sends the call request
#     @retry(JSONRPCException, tries=10, delay=1, back_off=2)
#     def get_tx_result(self,_call):
#         tx_result = self.icon_service.call(_call)
#         return tx_result




#     def test_update_delegation1(self):
#         print('======================================================================')
#         print('Test Update Delegations for more than 100%')
#         print('----------------------------------------------------------------------')
#         params = {'_user_delegations':[{'_address': 'hxc5772df538f620e1f61ef2cc3cddcea9d6ff5063',  '_votes_in_per' : "50"},{'_address': 'hx7ce8e9c5e1ee02c6167b99b5bb4d00bdf63d0a30',  '_votes_in_per' : "50"},
#                                                                      {'_address': 'hxbdc3baae0632fad453d62130d3379900a323f5b4',  '_votes_in_per' : "50"}]}
#         call_transaction = CallTransactionBuilder() \
#             .from_(self._test1.get_address()) \
#             .to(self.Address) \
#             .nid(80) \
#             .step_limit(10000000) \
#             .nonce(100) \
#             .method('update_delegations') \
#             .params(params) \
#             .build()

#         # Returns the signed transaction object having a signature
#         signed_transaction = SignedTransaction(call_transaction, self._test1)

#         # process the transaction in zicon
#         tx_hash = self.icon_service.send_transaction(signed_transaction)

#         _tx_result= self._get_tx_result(tx_hash)
#         #check Transaction result
#         print (_tx_result)
#         self.assertRaises(AssertionError)


        
#     def test_update_delegation2(self):
#         print('======================================================================')
#         print('Test Update Delegations for less than 100%')
#         print('----------------------------------------------------------------------')
#         params = {'_user_delegations':[{'_address': 'hxc5772df538f620e1f61ef2cc3cddcea9d6ff5063',  '_votes_in_per' : "5"},{'_address': 'hx7ce8e9c5e1ee02c6167b99b5bb4d00bdf63d0a30',  '_votes_in_per' : "10"},
#                                                                      {'_address': 'hxbdc3baae0632fad453d62130d3379900a323f5b4',  '_votes_in_per' : "15"}]}
#         call_transaction = CallTransactionBuilder() \
#             .from_(self._test1.get_address()) \
#             .to(self.Address) \
#             .nid(80) \
#             .step_limit(10000000) \
#             .nonce(100) \
#             .method('update_delegations') \
#             .params(params) \
#             .build()

#         # Returns the signed transaction object having a signature
#         signed_transaction = SignedTransaction(call_transaction, self._test1)

#         # process the transaction in zicon
#         tx_hash = self.icon_service.send_transaction(signed_transaction)

#         _tx_result= self._get_tx_result(tx_hash)
#         #check Transaction result
#         print (_tx_result)
#         self.assertRaises(AssertionError)


    