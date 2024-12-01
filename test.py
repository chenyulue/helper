import timeit
from helper.models import ClaimModel

with open("./tests/claims_set/claims1.txt", "r", encoding="utf-8") as f:
    content = f.read()

claim_model = ClaimModel(content)

start_time = timeit.time.perf_counter()

result = claim_model._get_reference_path(12, claim_model.claims)

end_time = timeit.time.perf_counter()

print("权利要求11的引用路径 -> ", result)
print("花费时间 ->", end_time - start_time, "seconds")

    