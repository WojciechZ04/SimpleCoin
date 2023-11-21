from chain import Chain

chain = Chain(10)

for i in range(6):
    # data = input("Add somthing to the chain: ")
    chain.add_to_pool(str(i))
    chain.mine()
