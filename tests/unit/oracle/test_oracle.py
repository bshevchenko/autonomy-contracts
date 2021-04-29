from consts import *
from brownie import chain, reverts, web3
from brownie.test import given, strategy
from utils import *


def test_constructor(asc):
    assert asc.o.getPriceOracle() == asc.po
    assert asc.o.getASCPerUSD() == INIT_ASC_PER_USD
    assert asc.o.getETHPerUSD() == INIT_ETH_PER_USD
    assert asc.o.getGasPriceFast() == INIT_GAS_PRICE_FAST
    assert asc.o.owner() == asc.DEPLOYER


def test_getRandNum(asc):
    for i in range(1000):
        chain.mine(1)
        assert getRandNum(i) == asc.o.getRandNum(i)


# Test with a new price oracle so we can test that getASCPerETH
# properly reads the new price
def test_setPriceOracle(asc, PriceOracle):
    newASCRate = 17
    newETHRate = 15
    newGasPriceFast = 3 * 10**9
    newPriceOracle = asc.DEPLOYER.deploy(PriceOracle, newASCRate, newETHRate, newGasPriceFast)

    asc.o.setPriceOracle(newPriceOracle, asc.FR_DEPLOYER)
    
    assert asc.o.getASCPerUSD() == newASCRate
    assert asc.o.getETHPerUSD() == newETHRate
    assert asc.o.getGasPriceFast() == newGasPriceFast
    assert asc.o.owner() == asc.DEPLOYER


@given(newPriceOracle=strategy('address'))
def test_setPriceOracle_rand(asc, newPriceOracle):
    asc.o.setPriceOracle(newPriceOracle, asc.FR_DEPLOYER)
    
    assert asc.o.getPriceOracle() == newPriceOracle
    assert asc.o.owner() == asc.DEPLOYER


@given(
    newPriceOracle=strategy('address'),
    sender=strategy('address')
)
def test_setPriceOracle_rev_owner(asc, newPriceOracle, sender):
    if sender != asc.DEPLOYER:
        with reverts(REV_MSG_OWNER):
            asc.o.setPriceOracle(newPriceOracle, {'from': sender})