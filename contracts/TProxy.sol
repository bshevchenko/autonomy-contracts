pragma solidity 0.8.6;


import "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";


contract TProxy is TransparentUpgradeableProxy {

    constructor(
        address _logic,
        address admin_,
        bytes memory _data
    ) payable TransparentUpgradeableProxy(_logic, admin_, _data) {}

}