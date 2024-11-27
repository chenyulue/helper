from helper.models import ClaimModel

def test_claim_model(claims1):
    claim_model = ClaimModel(claims1)
    assert len(claim_model.claims) == 12

    for claim in claim_model.claims:
        if claim.number < 10:
            assert claims1[claim.start_pos] == str(claim.number)
        else:
            assert claims1[claim.start_pos : claim.start_pos+2] == str(claim.number)

    assert claim_model.claims[6].dependency == "4或6"
    assert claim_model.claims[6].title == "场效应晶体管"
    assert claim_model.claims[0].dependency is None