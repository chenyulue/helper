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
# claim_model.check_all_reference_basis(4)

# pprint(claim_model.reference_basis[8])
result = claim_model._reference_has_basis(claim_model.claims[7], "纳米线第二", 43, claim_model.claims)

claim_model.get_all_reference_paths()

pprint(claim_model.reference_path)