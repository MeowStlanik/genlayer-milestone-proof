import json
import unittest
from contract_harness import Harness, UserError, Address, Return

class MilestoneTests(unittest.TestCase):
    def setUp(self):
        self.h=Harness('milestone-proof','MilestoneProof');self.c=self.h.contract
        self.rubric=json.dumps([{'criterion':'A published English API guide with 3 runnable examples.','weight_bps':10000}])
        self.c.create('grant',Address('builder'),self.rubric)
        self.case=lambda:json.loads(self.c.get_case('grant'))

    def activate(self):
        self.h.gl.message.sender_address=Address('builder')
        self.c.accept('grant',self.case()['rubric_hash'])

    def test_requires_builder_and_matching_rubric(self):
        with self.assertRaises(UserError):self.c.accept('grant',self.case()['rubric_hash'])
        self.h.gl.message.sender_address=Address('builder')
        with self.assertRaises(UserError):self.c.accept('grant','wrong hash')

    def test_rejects_mutation_and_invalid_weights(self):
        with self.assertRaises(UserError):self.c.create('grant',Address('builder'),self.rubric)
        with self.assertRaises(UserError):self.c.create('bad',Address('builder'),self.rubric.replace('10000','9999'))

    def test_consensus_disagreement_does_not_pass(self):
        self.activate();self.c.submit('grant','Published guide contains three executable API examples.')
        self.h.respond({'checks':[{'status':'MET','quote':'three executable API examples'}]},
                       {'checks':[{'status':'UNKNOWN','quote':''}]})
        with self.assertRaisesRegex(UserError,'consensus rejected'):self.c.evaluate('grant')
        self.assertEqual(self.case()['state'],'SUBMITTED')
        self.assertEqual(len(self.c.receipts),0)

    def test_missing_evidence_is_unknown_then_revision_can_pass(self):
        self.activate();self.c.submit('grant','The work will be completed next week.')
        self.h.respond({'checks':[{'status':'UNKNOWN','quote':''}]});self.c.evaluate('grant')
        self.assertEqual(self.case()['state'],'UNKNOWN')
        self.c.submit('grant','Published guide contains three executable API examples.')
        self.h.respond({'checks':[{'status':'MET','quote':'three executable API examples'}]});self.c.evaluate('grant')
        self.assertEqual(self.case()['state'],'PASSED')
        self.assertEqual(json.loads(self.c.get_receipt('grant',2))['satisfied_bps'],10000)
        self.assertEqual(json.loads(self.c.get_receipt('grant',1))['state'],'UNKNOWN')
        with self.assertRaises(UserError):self.c.submit('grant','change accepted evidence')

    def test_fabricated_quote_and_incomplete_coverage_rejected(self):
        self.activate();self.c.submit('grant','A promise to implement everything.')
        for output in [{'checks':[{'status':'MET','quote':'fabricated proof'}]},{'checks':[]}]:
            self.h.outputs=[output]
            with self.assertRaises(UserError):self.c.evaluate('grant')

    def test_revision_budget(self):
        self.activate()
        for _ in range(3):
            self.c.submit('grant','Unclear delivery progress.')
            self.h.respond({'checks':[{'status':'UNKNOWN','quote':''}]});self.c.evaluate('grant')
        with self.assertRaises(UserError):self.c.submit('grant','another revision')

if __name__ == '__main__': unittest.main()
