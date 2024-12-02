import timeit
from helper.models import ClaimModel
from pprint import pprint

with open("./tests/claims_set/claims1.txt", "r", encoding="utf-8") as f:
    content = f.read()

claim_model = ClaimModel(content)

start_time = timeit.time.perf_counter()

result = claim_model._get_reference_path(12, claim_model.claims)

end_time = timeit.time.perf_counter()

claim_model.check_all_reference_basis(3)
claim_model.check_all_reference_basis(5)

pprint(claim_model.reference_basis)

    