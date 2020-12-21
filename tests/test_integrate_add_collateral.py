import os

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.icon_service import IconService
from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS
from iconsdk.exception import JSONRPCException
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.transaction_builder import CallTransactionBuilder, TransactionBuilder, DeployTransactionBuilder

from .repeater import retry


class TestTest(IconIntegrateTestBase):
    TEST_HTTP_ENDPOINT_URI_V3 = "https://zicon.net.solidwallet.io/api/v3"

    #Address of recently deployed contract
    Address1 = "cx0d82da4cacf5b823ff922e6b8130f0d89d12213a"
    Address2 = "cxf1a8a787847544877496dd73813cca0efb759418"
    Address3 = "cxe26bd62e91d7bb366f09381e5a2c56485f44910d"

    def setUp(self):
        super().setUp()
        # WARNING: ICON service emulation is not working with IISS.
        # You can stake and delegate but can't get any I-Score for reward.
        # If you want to test IISS stuff correctly, set self.icon_service and send requests to the network

        self.icon_service = IconService(HTTPProvider(self.TEST_HTTP_ENDPOINT_URI_V3))
        # If you want to send requests to the network, uncomment next line and set self.TEST_HTTP_ENDPOINT_URI_V3

       

    @retry(JSONRPCException, tries=10, delay=1, back_off=2)
    def _get_tx_result(self,_tx_hash):
        tx_result = self.icon_service.get_transaction_result(_tx_hash)
        return tx_result 

    # Sends the call request
    @retry(JSONRPCException, tries=10, delay=1, back_off=2)
    def get_tx_result(self,_call):
        tx_result = self.icon_service.call(_call)
        return tx_result
    

#     def test_add_collateral1(self):
#         #Calling add_collateral from test_account2
#         params = {'_to': self._test1.get_address(),'_user_delegations':[{'_address': 'hx95248f3757afcb50efa99f529183ba401a82273c',  '_votes_in_per' : "50"},
#                                                                     {'_address': 'hxc89dfd4bf903b39ca98db905443ca9020f955e8c',  '_votes_in_per' : "100"}]}

#         transaction = CallTransactionBuilder() \
#             .from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .value (10 * 10 ** 18) \
#             .step_limit(10000000) \
#             .nid(80) \
#             .nonce(100) \
#             .method('add_collateral') \
#             .params(params) \
#             .build()
#         # # Returns the signed transaction object having a signature
#         signed_transaction = SignedTransaction(transaction, self._test1)

#         # # process the transaction in zicon
#         tx_hash = self.icon_service.send_transaction(signed_transaction)

#         print('======================================================================')
#         print('Test for votes more than 100% (add_collateral)')
#         print('----------------------------------------------------------------------')
#         _tx_result= self._get_tx_result(tx_hash)
#         #check Transaction result
#         print (_tx_result)
#         self.assertRaises(AssertionError)

#     def test_add_collateral2(self):
#         #Calling add_collateral from test_account2
#         params = {'_to': self._test1.get_address(),'_user_delegations':[{'_address': 'hx95248f3757afcb50efa99f529183ba401a82273c',  '_votes_in_per' : "25"},
#                                                                     {'_address': 'hxc89dfd4bf903b39ca98db905443ca9020f955e8c',  '_votes_in_per' : "50"}]}

#         transaction = CallTransactionBuilder() \
#             .from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .value (10 * 10 ** 18) \
#             .step_limit(10000000) \
#             .nid(80) \
#             .nonce(100) \
#             .method('add_collateral') \
#             .params(params) \
#             .build()
#         # # Returns the signed transaction object having a signature
#         signed_transaction = SignedTransaction(transaction, self._test1)

#         # # process the transaction in zicon
#         tx_hash = self.icon_service.send_transaction(signed_transaction)

#         print('======================================================================')
#         print('Test for votes less than 100% (add_collateral)')
#         print('----------------------------------------------------------------------')
#         _tx_result= self._get_tx_result(tx_hash)
#         #check Transaction result
#         print (_tx_result)
#         self.assertRaises(AssertionError)

    def test_add_collateral3(self):
        #Calling add_collateral from test_account1
        params = {'_to': self._test1.get_address(),'_user_delegations':[{'_address': 'hx4917005bf4b8188b9591da520fc1c6dab8fe717f',  '_votes_in_per' : "50"},
                                                                    {'_address': 'hx7cc2bb9d84ff3b5843f83d07818ebcff31be29e5',  '_votes_in_per' : "50"}]}

        transaction = CallTransactionBuilder() \
            .from_(self._test1.get_address()) \
            .to(self.Address1) \
            .value (10 * 10 ** 18) \
            .step_limit(10000000) \
            .nid(80) \
            .nonce(100) \
            .method('addCollateral') \
            .params(params) \
            .build()
        # # Returns the signed transaction object having a signature
        signed_transaction = SignedTransaction(transaction, self._test1)

        # # process the transaction in zicon
        tx_hash = self.icon_service.send_transaction(signed_transaction)

        _tx_result= self._get_tx_result(tx_hash)
        print('======================================================================')
        print('Test for delegating two preps with 50% votes each (add_collateral)')
        print('----------------------------------------------------------------------')
        print (_tx_result)
        # #check Transaction result
        self.assertTrue('status' in _tx_result)
        self.assertEqual(True, _tx_result['status'])

        params = {"address": self.Address1}
        delegation_call = CallBuilder().from_(self._test1.get_address()) \
            .to(self.Address1) \
            .method("getPrepDelegations") \
            .build()
        
        contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
            .to(self.Address1) \
            .method("getDelegationFromNetwork") \
            .params(params) \
            .build()
        response_delegation = self.get_tx_result(delegation_call)
        response_delegation_contract = self.get_tx_result(contract_delegation_call)

        print('----------------------------------------------------------------------')
        print('Delegation List')
        print('----------------------------------------------------------------------')
        print (response_delegation)
        print('----------------------------------------------------------------------')
        print('Delegation List from Network')
        print('----------------------------------------------------------------------')
        delegation_from_contract = {}
        #Iterating through contract delegations
        for i in response_delegation_contract["delegations"]:
            delegation_from_contract[i['address']] = i['value']
        print(delegation_from_contract)

        # check call result
        self.assertEqual(response_delegation,delegation_from_contract)
        
#     def test_add_collateral4(self):
#         #Calling add_collateral from test_account1
#         params = {'_to': self._test1.get_address(),'_user_delegations':[{'_address': 'hx9a24e7a53e031ab6aa7b831b1dbe4200bd3f9483',  '_votes_in_per' : "50"},
#                                                                     {'_address': 'hx8573a132f3df5c34a292fc16cb33737ffe10b367',  '_votes_in_per' : "50"}]}

#         transaction = CallTransactionBuilder() \
#             .from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .value (10 * 10 ** 18) \
#             .step_limit(10000000) \
#             .nid(80) \
#             .nonce(100) \
#             .method('add_collateral') \
#             .params(params) \
#             .build()
#         # # Returns the signed transaction object having a signature
#         signed_transaction = SignedTransaction(transaction, self._test1)

#         # # process the transaction in zicon
#         tx_hash = self.icon_service.send_transaction(signed_transaction)

#         print('======================================================================')
#         print('Test for delegating two preps with 50% votes each (add_collateral)')
#         print('----------------------------------------------------------------------')
#         _tx_result= self._get_tx_result(tx_hash)
#         print (_tx_result)
#         # #check Transaction result
#         self.assertTrue('status' in _tx_result)
#         self.assertEqual(True, _tx_result['status'])

#         params = {"address": self.Address1}
#         delegation_call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .method("get_prep_delegations") \
#             .build()
        
#         contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .method("get_delegation_from_network") \
#             .params(params) \
#             .build()
#         response_delegation = self.get_tx_result(delegation_call)
#         response_delegation_contract = self.get_tx_result(contract_delegation_call)

#         print('----------------------------------------------------------------------')
#         print('Delegation List')
#         print('----------------------------------------------------------------------')
#         print (response_delegation)
#         print('----------------------------------------------------------------------')
#         print('Delegation List from Network')
#         print('----------------------------------------------------------------------')
#         delegation_from_contract = {}
#         #Iterating through contract delegations
#         for i in response_delegation_contract["delegations"]:
#             delegation_from_contract[i['address']] = i['value']
#         print(delegation_from_contract)

#         print(list(delegation_from_contract.keys()))
#         print(list(response_delegation.keys()))
#         # check call result
#         for i in list(delegation_from_contract.keys()):
#             self.assertTrue(i in list(response_delegation.keys()))

#     def test_add_collateral5(self):
#         #Calling add_collateral from test_account1
#         params = {'_to': self._test1.get_address(),'_user_delegations':[{'_address': 'hx91de10325dd4b9a104c94ebc2ad9ceca279da8b6',  '_votes_in_per' : "50"},
#                                                                     {'_address': 'hx8573a132f3df5c34a292fc16cb33737ffe10b367',  '_votes_in_per' : "50"}]}

#         transaction = CallTransactionBuilder() \
#             .from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .value (10 * 10 ** 18) \
#             .step_limit(10000000) \
#             .nid(80) \
#             .nonce(100) \
#             .method('add_collateral') \
#             .params(params) \
#             .build()
#         # # Returns the signed transaction object having a signature
#         signed_transaction = SignedTransaction(transaction, self._test1)

#         # # process the transaction in zicon
#         tx_hash = self.icon_service.send_transaction(signed_transaction)

#         print('======================================================================')
#         print('Test for delegating two preps with 50% votes each (add_collateral) *one is outside TOP 20')
#         print('----------------------------------------------------------------------')
#         _tx_result= self._get_tx_result(tx_hash)
#         print (_tx_result)
#         # #check Transaction result
#         self.assertTrue('status' in _tx_result)
#         self.assertEqual(True, _tx_result['status'])

#         params = {"address": self.Address1}
#         delegation_call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .method("get_prep_delegations") \
#             .build()
        
#         contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .method("get_delegation_from_network") \
#             .params(params) \
#             .build()
#         response_delegation = self.get_tx_result(delegation_call)
#         response_delegation_contract = self.get_tx_result(contract_delegation_call)

#         print('----------------------------------------------------------------------')
#         print('Delegation List')
#         print('----------------------------------------------------------------------')
#         print (response_delegation)
#         print('----------------------------------------------------------------------')
#         print('Delegation List from Network')
#         print('----------------------------------------------------------------------')
#         delegation_from_contract = {}
#         #Iterating through contract delegations
#         for i in response_delegation_contract["delegations"]:
#             delegation_from_contract[i['address']] = i['value']
#         print(delegation_from_contract)

#         print(list(delegation_from_contract.keys()))
#         print(list(response_delegation.keys()))
#         # check call result
#         self.assertTrue('hx8573a132f3df5c34a292fc16cb33737ffe10b367' in list(delegation_from_contract.keys()))
#         self.assertTrue('hx91de10325dd4b9a104c94ebc2ad9ceca279da8b6' not in list(delegation_from_contract.keys()))
#         self.assertTrue(hex(15750000000000000000) in list(delegation_from_contract.values()))
#         self.assertTrue(hex(750000000000000000) in list(delegation_from_contract.values()))

        
#     def test_add_collateral6(self):
#         #Calling add_collateral from test_account1
#         params = {'_to': self._test1.get_address()}
#         transaction = CallTransactionBuilder() \
#             .from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .value (10 * 10 ** 18) \
#             .step_limit(10000000) \
#             .nid(80) \
#             .nonce(100) \
#             .method('add_collateral') \
#             .params(params) \
#             .build()
#         # # Returns the signed transaction object having a signature
#         signed_transaction = SignedTransaction(transaction, self._test1)

#         # # process the transaction in zicon
#         tx_hash = self.icon_service.send_transaction(signed_transaction)

#         print('======================================================================')
#         print('Test for add_collateral without params information')
#         print('----------------------------------------------------------------------')
#         _tx_result= self._get_tx_result(tx_hash)
#         print (_tx_result)
#         # #check Transaction result
#         self.assertTrue('status' in _tx_result)
#         self.assertEqual(True, _tx_result['status'])

#         params = {"address": self.Address1}
#         delegation_call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .method("get_prep_delegations") \
#             .build()
        
#         contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .method("get_delegation_from_network") \
#             .params(params) \
#             .build()
#         response_delegation = self.get_tx_result(delegation_call)
#         response_delegation_contract = self.get_tx_result(contract_delegation_call)

#         print('----------------------------------------------------------------------')
#         print('Delegation List')
#         print('----------------------------------------------------------------------')
#         print (response_delegation)
#         print('----------------------------------------------------------------------')
#         print('Delegation List from Network')
#         print('----------------------------------------------------------------------')
#         delegation_from_contract = {}
#         #Iterating through contract delegations
#         for i in response_delegation_contract["delegations"]:
#             delegation_from_contract[i['address']] = i['value']
#         print(delegation_from_contract)

#         # check call result
#         self.assertTrue(hex(1000000000000000000) in list(delegation_from_contract.values()))
        
    def test_add_collateral7(self):
        #Calling add_collateral from test_account1
        params = {'_to': self._test1.get_address()}
        transaction = CallTransactionBuilder() \
            .from_(self._test1.get_address()) \
            .to(self.Address2) \
            .value (10 * 10 ** 18) \
            .step_limit(10000000) \
            .nid(80) \
            .nonce(100) \
            .method('addCollateral') \
            .params(params) \
            .build()
        # # Returns the signed transaction object having a signature
        signed_transaction = SignedTransaction(transaction, self._test1)

        # # process the transaction in zicon
        tx_hash = self.icon_service.send_transaction(signed_transaction)

        print('======================================================================')
        print('Test for add_collateral without params information at the beginning')
        print('----------------------------------------------------------------------')
        _tx_result= self._get_tx_result(tx_hash)
        print (_tx_result)
        # #check Transaction result
        self.assertTrue('status' in _tx_result)
        self.assertEqual(True, _tx_result['status'])

        params = {"address": self.Address2}
        delegation_call = CallBuilder().from_(self._test1.get_address()) \
            .to(self.Address2) \
            .method("getPrepDelegations") \
            .build()
        
        contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
            .to(self.Address2) \
            .method("getDelegationFromNetwork") \
            .params(params) \
            .build()
        response_delegation = self.get_tx_result(delegation_call)
        response_delegation_contract = self.get_tx_result(contract_delegation_call)

        print('----------------------------------------------------------------------')
        print('Delegation List')
        print('----------------------------------------------------------------------')
        print (response_delegation)
        print('----------------------------------------------------------------------')
        print('Delegation List from Network')
        print('----------------------------------------------------------------------')
        delegation_from_contract = {}
        #Iterating through contract delegations
        for i in response_delegation_contract["delegations"]:
            delegation_from_contract[i['address']] = i['value']
        print(delegation_from_contract)

      
        print(list(delegation_from_contract.keys()))
        print(list(response_delegation.keys()))
        # check call result
        self.assertTrue(hex('500000000000000000') in list(delegation_from_contract.values()))

#     def test_add_collateral8(self):
#         #Calling add_collateral from test_account1
#         params = {'_to': self._test1.get_address(),'_user_delegations':[{'_address': 'hx91de10325dd4b9a104c94ebc2ad9ceca279da8b6',  '_votes_in_per' : "50"},
#                                                                     {'_address': 'hx8573a132f3df5c34a292fc16cb33737ffe10b367',  '_votes_in_per' : "50"}]}

#         transaction = CallTransactionBuilder() \
#             .from_(self._test1.get_address()) \
#             .to(self.Address3) \
#             .value (10 * 10 ** 18) \
#             .step_limit(10000000) \
#             .nid(80) \
#             .nonce(100) \
#             .method('add_collateral') \
#             .params(params) \
#             .build()
#         # # Returns the signed transaction object having a signature
#         signed_transaction = SignedTransaction(transaction, self._test1)

#         # # process the transaction in zicon
#         tx_hash = self.icon_service.send_transaction(signed_transaction)

#         _tx_result= self._get_tx_result(tx_hash)
#         print('======================================================================')
#         print('Test for delegating two preps with 50% votes each at the beginning (add_collateral) *one is outside TOP 20')
#         print('----------------------------------------------------------------------')
#         print (_tx_result)
#         # #check Transaction result
#         self.assertTrue('status' in _tx_result)
#         self.assertEqual(True, _tx_result['status'])

#         params = {"address": self.Address3}
#         delegation_call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address3) \
#             .method("get_prep_delegations") \
#             .build()
        
#         contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address3) \
#             .method("get_delegation_from_network") \
#             .params(params) \
#             .build()
#         response_delegation = self.get_tx_result(delegation_call)
#         response_delegation_contract = self.get_tx_result(contract_delegation_call)

#         print('----------------------------------------------------------------------')
#         print('Delegation List')
#         print('----------------------------------------------------------------------')
#         print (response_delegation)
#         print('----------------------------------------------------------------------')
#         print('Delegation List from Network')
#         print('----------------------------------------------------------------------')
#         delegation_from_contract = {}
#         #Iterating through contract delegations
#         for i in response_delegation_contract["delegations"]:
#             delegation_from_contract[i['address']] = i['value']
#         print(delegation_from_contract)
#         print('======================================================================')

#         # check call result
#         self.assertTrue('hx8573a132f3df5c34a292fc16cb33737ffe10b367' in list(delegation_from_contract.keys()))
#         self.assertTrue('hx91de10325dd4b9a104c94ebc2ad9ceca279da8b6' not in list(delegation_from_contract.keys()))
        
        

#     def test_get_address_delegations(self):
#         print('======================================================================')
#         print('Test Get Address Delegations')
#         print('----------------------------------------------------------------------')
#         params = {"_address": "hxe7af5fcfd8dfc67530a01a0e403882687528dfcb"}
#         _call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .method("get_address_delegations") \
#             .params(params) \
#             .build()
#         # Sends the call request
#         response = self.get_tx_result(_call)
#         # check call result
#         self.assertTrue(hex(50000000000000000000) in list(response.values()))
   

#     def test_get_total_stake(self):
#         print('======================================================================')
#         print('Test Get Total Stake')
#         print('----------------------------------------------------------------------')
#         _call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .method("get_total_stake") \
#             .build()

#         #Sending the call request
#         response = self.get_tx_result(_call)
#         params = {"_address": self.Address1}
#         _call = CallBuilder().from_(self._test1.get_address()) \
#             .to(self.Address1) \
#             .method("get_stake_from_network") \
#             .params(params) \
#             .build()

#         response_from_contract = self.get_tx_result(_call)
#         # check call result
#         # print(int(response['stake'],16))
#         self.assertEqual(response,response_from_contract['stake']                                                                                                                                                                                                                               )    

    
