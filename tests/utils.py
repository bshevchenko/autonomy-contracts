from consts import *
from brownie import web3, convert
import base58 as b58
import ipfshttpclient
from hashlib import sha256


def getEpoch(blockNum):
    return int(blockNum / BLOCKS_IN_EPOCH) * BLOCKS_IN_EPOCH


def getRandNum(seed):
    return web3.toInt(web3.eth.getBlock(seed).hash)


def getExecutor(asc, blockNum, stakers):
    epoch = getEpoch(blockNum)
    randNum = getRandNum(epoch)
    # i = randNum % len(stakers)
    i = asc.sm.getRemainder(randNum, len(stakers))
    print(randNum, epoch, i, stakers[i], stakers)
    return stakers[i], epoch


def getFirstIndexes(stakes, val, n):
    cntr = 0
    idxs = []

    for i in range(n):
        idx = stakes.index(val)
        idxs.append(idx)
        stakes[idx] = stakes[-1]
        stakes = stakes[:-1]


    # for i, el in enumerate(stakes):
    #     if el == val:
    #         idxs.append(i)
    #         cntr += 1
    #         if cntr == n:
    #             break
    
    
    # Shouldn't be a situation where fewer occurances are
    # found than expected
    assert len(idxs) == n

    return idxs


def getModStakes(stakes, staker, numStakes, isStaking):
    if isStaking:
        return stakes + ([staker] * numStakes)
    else:
        idxs = []
        newStakes = list(stakes)
        for i in range(numStakes):
            idx = newStakes.index(staker)
            idxs.append(idx)
            newStakes[idx] = newStakes[-1]
            newStakes = newStakes[:-1]

        assert len(idxs) == numStakes
        return idxs, newStakes


# Assumes a sha256 hash of (prefix + data + suffix) is the input
def getCID(hash):
    if type(hash) is not bytes:
        hash = convert.to_bytes(hash, 'bytes')
    cidBytes = CID_PREFIX_BYTES + hash
    return str(b58.b58encode(cidBytes), 'ascii')


def bytesToHex(b):
    return '0x' + b.hex()


def getHashBytesFromCID(CID):
    return b58.b58decode(CID)[2:]


def getHashFromCID(CID):
    return bytesToHex(b58.b58decode(CID)[2:])


def addToIpfs(asc, req):
    reqBytes = asc.r.getReqBytes(req)

    with ipfshttpclient.connect() as client:
        return client.add_bytes(reqBytes)


def getIpfsMetaData(asc, req):
    reqBytes = asc.r.getReqBytes(req)

    with ipfshttpclient.connect() as client:
        ipfsCID = client.add_bytes(reqBytes)
        ipfsBlock = client.block.get(ipfsCID)
    
    reqBytesIdx = ipfsBlock.index(reqBytes)
    dataPrefix = ipfsBlock[:reqBytesIdx]
    dataSuffix = ipfsBlock[reqBytesIdx + len(reqBytes) : ]

    return dataPrefix, dataSuffix


def addReqGetHashBytes(asc, req):
    return getHashBytesFromCID(addToIpfs(asc, req))