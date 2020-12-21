# from staking.staking import Staking
# from sicx.sicx import StakedICX
# from tbears.libs.scoretest.score_test_case import ScoreTestCase
# from iconservice import Address

# class TestStaking(ScoreTestCase):

#     def setUp(self):
#         super().setUp()
        
#         params = {}
#         self.staking = self.get_score_instance(Staking,self.test_account1,params)
#         self.stakedICX = self.get_score_instance(StakedICX,self.test_account1,params)

#         #Setting up test accounts
#         self.test_account3 = Address.from_string(f"hx{'12345'*8}")
#         self.test_account4 = Address.from_string(f"hx{'1234'*10}")

#         account_info = {
#             self.test_account3: 10 ** 21,
#             self.test_account4: 10 ** 21
#         }
#         self.initialize_accounts(account_info)

#         #Setting the initial attribute for PrepDelegations
#         # PrepDelegations = {
#         #     "hx95248f3757afcb50efa99f529183ba401a82273c": 5 
#         # }

#         # Setting interfaces for the staking
#         self.staking.set_sICX_address(self.stakedICX.address)

#     def test_get_sICX_address(self):
#          self.set_msg(self.test_account1,0)
#          self.assertEqual(self.staking.get_sICX_address(),self.stakedICX.address)

#     # def test_add_collatoral(self):
#     #     self.set_msg(self.test_account1,5)
#     #     self.staking.add_collateral(self.test_account1,[{"hx95248f3757afcb50efa99f529183ba401a82273c": "5" }])
    