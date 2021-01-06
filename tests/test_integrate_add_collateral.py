import os

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.icon_service import IconService
from tbears.libs.icon_integrate_test import IconIntegrateTestBase, SCORE_INSTALL_ADDRESS
from iconsdk.exception import JSONRPCException
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.transaction_builder import CallTransactionBuilder, TransactionBuilder, DeployTransactionBuilder
from iconsdk.wallet.wallet import KeyWallet
import time
from .repeater import retry

ADDRESS = ['staking1','staking2','staking3']

class TestTest(IconIntegrateTestBase):
    TEST_HTTP_ENDPOINT_URI_V3 = "https://zicon.net.solidwallet.io/api/v3"
    #Address of recently deployed contract


    def setUp(self):
        super().setUp()
        self.contracts = {}
        self.contracts['sicx1'] = "cx20fa65cffc720db31e78fba6db5d58f58babd933"
        self.contracts['staking1'] = "cx25c39ed0d27853e44af8ab2739d6af832f35d533"
        self.contracts['staking2'] = "cx8b250e76bc919f73068571c26cadecde69e63b46"
        self.contracts['staking3'] = "cx3502e9af253098d187578ca826fe71032f116e47"
        # WARNING: ICON service emulation is not working with IISS.
        # You can stake and delegate but can't get any I-Score for reward.
        # If you want to test IISS stuff correctly, set self.icon_service and send requests to the network
        self.icon_service = IconService(HTTPProvider(self.TEST_HTTP_ENDPOINT_URI_V3))
        private2="093f12dba9dc75da81ecafc88de73ef9b311b555939aeb5a875dc6ad8feef424"
        private3="167f6ec1694ab63243efdce98f6f6bfdcef0575cefbb86ffe3826f8373f12b85"
        self._test2 = KeyWallet.load(bytes.fromhex(private2))
        self._test3 = KeyWallet.load(bytes.fromhex(private3))

        #
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

    def test_add_collateral(self):
        print('======================================================================')
        print('Test Add Collateral')
        print('----------------------------------------------------------------------')
        settings = [
                    #{'name': 'Sending 30 ICX from test_account1', 'from' : self._test1.get_address(),'value':25 * 10 ** 18, 'params' : {'_to': self._test1.get_address()},'sign':self._test1},
                    #{'name': 'Sending 80 ICX from test_account1', 'from' : self._test1.get_address(),'value':40 * 10 ** 18, 'params' : {'_to': self._test1.get_address()},'sign': self._test1},
                    {'name': 'Sending 15 ICX from test_account2', 'from' : self._test2.get_address(),'value':15 * 10 ** 18, 'params' : {'_to': self._test2.get_address()},'sign': self._test2}
                    # {'name': 'Sending 15 ICX from test_account2', 'from' : self._test3.get_address(),'value':15 * 10 ** 18, 'params' : {'_to': self._test3.get_address()},'sign': self._test3}
                     ]

        for sett in settings:
            print('======================================================================')
            print(sett['name'])
            print('----------------------------------------------------------------------')

            transaction = CallTransactionBuilder() \
            .from_(sett['from']) \
            .to(self.contracts['staking1']) \
            .value (sett['value']) \
            .step_limit(10000000) \
            .nid(80) \
            .nonce(100) \
            .method('addCollateral') \
            .params(sett['params']) \
            .build()
            # Returns the signed transaction object having a signature
            signed_transaction = SignedTransaction(transaction, sett['sign'])

            # process the transaction in zicon
            tx_hash = self.icon_service.send_transaction(signed_transaction)
            _tx_result= self._get_tx_result(tx_hash)
             #check Transaction result
            print (_tx_result)
            self.assertTrue('status' in _tx_result)
            self.assertEqual(True, _tx_result['status'])
            # contract_delegation_call = CallBuilder().from_(sett['from']) \
            #     .to(self.contracts['staking1']) \
            #     .method("getDelegationFromNetwork") \
            #     .build()
            # response_delegation_contract = self.get_tx_result(contract_delegation_call)
            # print('----------------------------------------------------------------------')
            # print('Delegation List from Network')
            # print('----------------------------------------------------------------------')
            # delegation_from_contract = {}
            # #Iterating through contract delegations
            # for i in response_delegation_contract["delegations"]:
            #     delegation_from_contract[i['address']] = i['value']
            # print(delegation_from_contract)
            # check call result
            # if sett['name'] == 'Test Case 1.3':
            #     self.assertEqual(response_delegation,delegation_from_contract)

    # def test_update_delegation(self):
    #     print('======================================================================')
    #     print(' *******************Test Update Delegations***************************')
    #     print('----------------------------------------------------------------------')
    #     settings = [{'name': 'Test Case 1.1', 'wAddress':'staking3', 'params' : {'_user_delegations':[{'_address': 'hxc5772df538f620e1f61ef2cc3cddcea9d6ff5063',  '_votes_in_per' : "50"},
    #                                                               {'_address': 'hx7ce8e9c5e1ee02c6167b99b5bb4d00bdf63d0a30',  '_votes_in_per' : "50"}]}},
    #                 {'name': 'Test Case 2.1', 'wAddress':'staking1', "params" : {'_user_delegations':[{'_address': 'hxc5772df538f620e1f61ef2cc3cddcea9d6ff5063',  '_votes_in_per' : "5"},{'_address': 'hx7ce8e9c5e1ee02c6167b99b5bb4d00bdf63d0a30',  '_votes_in_per' : "10"},
    #                                                               {'_address': 'hxbdc3baae0632fad453d62130d3379900a323f5b4',  '_votes_in_per' : "15"}]}},
    #                 {'name': 'Test Case 2.2', 'wAddress':'staking1', 'params' : {'_user_delegations':[{'_address': 'hx95248f3757afcb50efa99f529183ba401a82273c',  '_votes_in_per' : "50"},{'_address': 'hx95248f3757afcb50efa99f529183ba401a82273c',  '_votes_in_per' : "50"},
    #                                                               {'_address': 'hxc89dfd4bf903b39ca98db905443ca9020f955e8c',  '_votes_in_per' : "50"}]}},
    #                 {'name': 'Test Case 2.3', 'wAddress':'staking1', 'params' : {}},
    #                 {'name': 'Test Case 2.4', 'wAddress':'staking1', 'params' : {'_user_delegations':[{'_address': 'hx4917005bf4b8188b9591da520fc1c6dab8fe717f',  '_votes_in_per' : "50"},
    #                                                               {'_address': 'hx9a24e7a53e031ab6aa7b831b1dbe4200bd3f9483',  '_votes_in_per' : "50"}]}},
    #                 {'name': 'Test Case 2.5', 'wAddress':'staking1', 'params' : {'_user_delegations':[{'_address': 'hx8573a132f3df5c34a292fc16cb33737ffe10b367',  '_votes_in_per' : "40"},{'_address': 'hx6bd3a3b1390e99194ced786725e0f0725fc1960b',  '_votes_in_per' : "15"},
    #                                                               {'_address': 'hx7cc2bb9d84ff3b5843f83d07818ebcff31be29e5',  '_votes_in_per' : "45"}]}},
    #                 {'name': 'Test Case 2.6', 'wAddress':'staking1', 'params' : {'_user_delegations':[{'_address': 'hx2d058aa34a76b2039e7cc59f18633aabd272d89f',  '_votes_in_per' : "100"}]}},
    #                 ]
    #     for sett in settings:
    #         print('======================================================================')
    #         print(sett['name'])
    #         print('----------------------------------------------------------------------')

    #         call_transaction = CallTransactionBuilder() \
    #             .from_(self._test1.get_address()) \
    #             .to(self.contracts[sett['wAddress']]) \
    #             .nid(80) \
    #             .step_limit(10000000) \
    #             .nonce(100) \
    #             .method('updateDelegations') \
    #             .params(sett['params']) \
    #             .build()
    #         # Returns the signed transaction object having a signature
    #         signed_transaction = SignedTransaction(call_transaction, self._test1)
    #         # process the transaction in zicon
    #         tx_hash = self.icon_service.send_transaction(signed_transaction)
    #         _tx_result= self._get_tx_result(tx_hash)
    #          #check Transaction result
    #         print (_tx_result)
    #         if sett['name'] == 'Test Case 1.1' or sett['name'] == 'Test Case 2.1' or sett['name'] == 'Test Case 2.2' or sett['name'] == 'Test Case 2.3':
    #             self.assertEqual(_tx_result,_tx_result)
    #         else:
    #             self.assertTrue('status' in _tx_result)
    #             self.assertEqual(True, _tx_result['status'])
    #             delegation_call = CallBuilder().from_(self._test1.get_address()) \
    #                 .to(self.contracts[sett['wAddress']]) \
    #                 .method("getPrepDelegations") \
    #                 .build()

    #             contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
    #                 .to(self.contracts[sett['wAddress']]) \
    #                 .method("getDelegationFromNetwork") \
    #                 .build()
    #             response_delegation = self.get_tx_result(delegation_call)
    #             response_delegation_contract = self.get_tx_result(contract_delegation_call)
    #             print('----------------------------------------------------------------------')
    #             print('Delegation List')
    #             print('----------------------------------------------------------------------')
    #             print (response_delegation)
    #             print('----------------------------------------------------------------------')
    #             print('Delegation List from Network')
    #             print('----------------------------------------------------------------------')
    #             delegation_from_contract = {}
    #             #Iterating through contract delegations
    #             for i in response_delegation_contract["delegations"]:
    #                 delegation_from_contract[i['address']] = i['value']
    #             print(delegation_from_contract)

    # def test_wclaim_iscore(self):
    #     print('======================================================================')
    #     print(' **********************Test Claim IScore*****************************')
    #     print('----------------------------------------------------------------------')

    #     transaction = CallTransactionBuilder() \
    #         .from_(self._test1.get_address()) \
    #         .to(self.contracts['staking1']) \
    #         .step_limit(10000000) \
    #         .nid(80) \
    #         .nonce(100) \
    #         .method('_claim_iscore') \
    #         .build()
    #     # # Returns the signed transaction object having a signature
    #     signed_transaction = SignedTransaction(transaction, self._test1)

    #     # # process the transaction in zicon
    #     tx_hash = self.icon_service.send_transaction(signed_transaction)
    #     _tx_result= self._get_tx_result(tx_hash)
    #     print (_tx_result)
    #     # #check Transaction result
    #     self.assertTrue('status' in _tx_result)
    #     self.assertEqual(True, _tx_result['status'])


    #     contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
    #         .to(self.contracts['staking1']) \
    #         .method("getLifetimeReward") \
    #         .build()
    #     response_delegation_contract = self.get_tx_result(contract_delegation_call)

    #     print('----------------------------------------------------------------------')
    #     print('Delegation List from Network')
    #     print('----------------------------------------------------------------------')
    #     delegation_from_contract = {}
    #     # #Iterating through contract delegations
    #     # for i in response_delegation_contract["delegations"]:
    #     #     delegation_from_contract[i['address']] = i['value']
    #     # print(delegation_from_contract)
    #     print(response_delegation_contract)


    # def test_tr(self):
    #     print('======================================================================')
    #     print(' *******************Test Update Delegations***************************')
    #     print('----------------------------------------------------------------------')
    #     settings = [{'name': 'Test Case 1.1', 'wAddress':'staking3', 'params' : {'_user_delegations':[{'_address': 'hxc5772df538f620e1f61ef2cc3cddcea9d6ff5063',  '_votes_in_per' : "50"},
    #                                                               {'_address': 'hx7ce8e9c5e1ee02c6167b99b5bb4d00bdf63d0a30',  '_votes_in_per' : "50"}]}},
    #                 {'name': 'Test Case 2.1', 'wAddress':'staking1', "params" : {'_user_delegations':[{'_address': 'hxc5772df538f620e1f61ef2cc3cddcea9d6ff5063',  '_votes_in_per' : "5"},{'_address': 'hx7ce8e9c5e1ee02c6167b99b5bb4d00bdf63d0a30',  '_votes_in_per' : "10"},
    #                                                               {'_address': 'hxbdc3baae0632fad453d62130d3379900a323f5b4',  '_votes_in_per' : "15"}]}},
    #                 {'name': 'Test Case 2.2', 'wAddress':'staking1', 'params' : {'_user_delegations':[{'_address': 'hx95248f3757afcb50efa99f529183ba401a82273c',  '_votes_in_per' : "50"},{'_address': 'hx95248f3757afcb50efa99f529183ba401a82273c',  '_votes_in_per' : "50"},
    #                                                               {'_address': 'hxc89dfd4bf903b39ca98db905443ca9020f955e8c',  '_votes_in_per' : "50"}]}},
    #                 {'name': 'Test Case 2.3', 'wAddress':'staking1', 'params' : {}},
    #                 {'name': 'Test Case 2.4', 'wAddress':'staking1', 'params' : {'_user_delegations':[{'_address': 'hx4917005bf4b8188b9591da520fc1c6dab8fe717f',  '_votes_in_per' : "50"},
    #                                                               {'_address': 'hx9a24e7a53e031ab6aa7b831b1dbe4200bd3f9483',  '_votes_in_per' : "50"}]}},
    #                 {'name': 'Test Case 2.5', 'wAddress':'staking1', 'params' : {'_user_delegations':[{'_address': 'hx8573a132f3df5c34a292fc16cb33737ffe10b367',  '_votes_in_per' : "40"},{'_address': 'hx6bd3a3b1390e99194ced786725e0f0725fc1960b',  '_votes_in_per' : "15"},
    #                                                               {'_address': 'hx7cc2bb9d84ff3b5843f83d07818ebcff31be29e5',  '_votes_in_per' : "45"}]}},
    #                 {'name': 'Test Case 2.6', 'wAddress':'staking1', 'params' : {'_user_delegations':[{'_address': 'hx23dfce82d36268f4cc3b943fa65d4c9632d23e76',  '_votes_in_per' : "100"}]}},
    #                 ]
    #     for sett in settings:
    #         print('======================================================================')
    #         print(sett['name'])
    #         print('----------------------------------------------------------------------')

    #         call_transaction = CallTransactionBuilder() \
    #             .from_(self._test1.get_address()) \
    #             .to(self.contracts[sett['wAddress']]) \
    #             .nid(80) \
    #             .step_limit(10000000) \
    #             .nonce(100) \
    #             .method('updateDelegations') \
    #             .params(sett['params']) \
    #             .build()
    #         # Returns the signed transaction object having a signature
    #         signed_transaction = SignedTransaction(call_transaction, self._test1)
    #         # process the transaction in zicon
    #         tx_hash = self.icon_service.send_transaction(signed_transaction)
    #         _tx_result= self._get_tx_result(tx_hash)
    #          #check Transaction result
    #         print (_tx_result)
    #         if sett['name'] == 'Test Case 1.1' or sett['name'] == 'Test Case 2.1' or sett['name'] == 'Test Case 2.2' or sett['name'] == 'Test Case 2.3':
    #             self.assertEqual(_tx_result,_tx_result)
    #         else:
    #             self.assertTrue('status' in _tx_result)
    #             self.assertEqual(True, _tx_result['status'])
    #             delegation_call = CallBuilder().from_(self._test1.get_address()) \
    #                 .to(self.contracts[sett['wAddress']]) \
    #                 .method("getPrepDelegations") \
    #                 .build()

    #             contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
    #                 .to(self.contracts[sett['wAddress']]) \
    #                 .method("getDelegationFromNetwork") \
    #                 .build()
    #             response_delegation = self.get_tx_result(delegation_call)
    #             response_delegation_contract = self.get_tx_result(contract_delegation_call)
    #             print('----------------------------------------------------------------------')
    #             print('Delegation List')
    #             print('----------------------------------------------------------------------')
    #             print (response_delegation)
    #             print('----------------------------------------------------------------------')
    #             print('Delegation List from Network')
    #             print('----------------------------------------------------------------------')
    #             delegation_from_contract = {}
    #             #Iterating through contract delegations
    #             for i in response_delegation_contract["delegations"]:
    #                 delegation_from_contract[i['address']] = i['value']
    #             print(delegation_from_contract)



    # def test_unstake(self):
    #     print('======================================================================')
    #     print('Test Unstake')
    #     print('----------------------------------------------------------------------')
    #     data = "{\"method\": \"unstake\"}".encode("utf-8")
    #     settings = [
    #                 # {'name': 'Test Case 1.1', 'from' : self._test1.get_address(), 'wAddress':'sicx1', 'params' : {'_to': self.contracts['staking1'],'_value': 20 * 10**18,'_data':data},'sign': self._test1,'delegation_address':'staking1'},
    #                 {'name': 'Test Case 1.2', 'from' : self._test2.get_address(), 'wAddress':'sicx1', 'params' : {'_to': self.contracts['staking1'], '_value': 20 * 10**18,'_data':data},'sign': self._test2,'delegation_address':'staking1'},
    #                 ]

    #     for sett in settings:
    #         print('======================================================================')
    #         print(sett['name'])
    #         print('----------------------------------------------------------------------')

    #         transaction = CallTransactionBuilder() \
    #         .from_(sett['from']) \
    #         .to(self.contracts[sett['wAddress']]) \
    #         .step_limit(10000000) \
    #         .nid(80) \
    #         .nonce(100) \
    #         .method('transfer') \
    #         .params(sett['params']) \
    #         .build()
    #         # Returns the signed transaction object having a signature
    #         signed_transaction = SignedTransaction(transaction, sett['sign'])

    #         # process the transaction in zicon
    #         tx_hash = self.icon_service.send_transaction(signed_transaction)
    #         _tx_result= self._get_tx_result(tx_hash)
    #          #check Transaction result
    #         print (_tx_result)
    #         self.assertTrue('status' in _tx_result)
    #         self.assertEqual(True, _tx_result['status'])
    #     # Address =[self._test1.get_address(),self._test2.get_address()]
    #     # for test in Address:
    #     #     contract_delegation_call = CallBuilder().from_(test) \
    #     #         .to(self.contracts[sett['delegation_address']]) \
    #     #         .method("getDelegationFromNetwork") \
    #     #         .build()
    #     #     response_delegation_contract = self.get_tx_result(contract_delegation_call)
    #     #     print('----------------------------------------------------------------------')
    #     #     print('Delegation List from Network')
    #     #     print('----------------------------------------------------------------------')
    #     #     delegation_from_contract = {}
    #     #     #Iterating through contract delegations
    #     #     for i in response_delegation_contract["delegations"]:
    #     #         delegation_from_contract[i['address']] = i['value']
    #     #     print(delegation_from_contract)
    #     # check call result
    #     # if sett['name'] == 'Test Case 1.3':
    #     #     self.assertEqual(response_delegation,delegation_from_contract)


    # def test_send_ICX(self):
    #     print('======================================================================')
    #     print('Test Send ICX')
    #     print('----------------------------------------------------------------------')
    #     settings = [
    #                 {'name': 'Test Case 1.1', 'from' : self._test1.get_address(), 'wAddress':'staking1', 'params' : {'_to': self._test2.get_address(),'_value': 800 }}
    #                 ]
    #     for sett in settings:
    #         print('======================================================================')
    #         print(sett['name'])
    #         print('----------------------------------------------------------------------')

    #         call_transaction = CallTransactionBuilder() \
    #             .from_(self._test1.get_address()) \
    #             .to(self.contracts[sett['wAddress']]) \
    #             .nid(80) \
    #             .step_limit(10000000) \
    #             .nonce(100) \
    #             .method('_send_ICX') \
    #             .params(sett['params']) \
    #             .build()
    #         # Returns the signed transaction object having a signature
    #         signed_transaction = SignedTransaction(call_transaction, self._test1)
    #         # process the transaction in zicon
    #         tx_hash = self.icon_service.send_transaction(signed_transaction)
    #         _tx_result= self._get_tx_result(tx_hash)
    #          #check Transaction result
    #         print (_tx_result)
    #         self.assertTrue('status' in _tx_result)
    #         self.assertEqual(True, _tx_result['status'])
    #         delegation_call = CallBuilder().from_(self._test1.get_address()) \
    #             .to(self.contracts[sett['wAddress']]) \
    #             .method("getPrepDelegations") \
    #             .build()

    #         contract_delegation_call = CallBuilder().from_(self._test1.get_address()) \
    #             .to(self.contracts[sett['wAddress']]) \
    #             .method("getDelegationFromNetwork") \
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
    



    def test_lifeTime(self):
        print('======================================================================')
        print('getLifetimeReward')
        print('----------------------------------------------------------------------')

        _call = CallBuilder().from_(self._test1.get_address()) \
            .to(self.contracts['staking1']) \
            .method("getLifetimeReward") \
            .build()

        response = self.get_tx_result(_call)
        # check call result
        print (response)
        

    def test_getRate(self):
        print('======================================================================')
        print('Test getRate ')
        print('----------------------------------------------------------------------')

        _call = CallBuilder().from_(self._test1.get_address()) \
            .to(self.contracts['staking1']) \
            .method("getRate") \
            .build()

        response = self.get_tx_result(_call)
        # check call result
        print (response)
        

    def test_getTodayRate(self):
        print('======================================================================')
        print('Test getTodayRate')
        print('----------------------------------------------------------------------')

        _call = CallBuilder().from_(self._test1.get_address()) \
            .to(self.contracts['staking1']) \
            .method("getTodayRate") \
            .build()

        response = self.get_tx_result(_call)
        # check call result
        print (response)
        
