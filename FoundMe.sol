// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {

    // safe math library check uint256 for integer overflows
    using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountFunded;

    address[] public funders;

    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    function fund() public payable {
        uint256 minimumUSD = 20 * 10 ** 18;
        require(getConversionRate(msg.value) >= minimumUSD, "Errror: You need to spend more eth!");
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e);
        ( /* uint80 roundID */,
            int price,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/) = priceFeed.latestRoundData();
        return uint256(price * 10000000000);
    }

    // function decimals() public view returns (uint8) {
    //     AggregatorV3Interface priceFeed = AggregatorV3Interface(0xD4a33860578De61DBAbDc8BFdb98FD742fA7028e);
    //     return priceFeed.decimals(); // 8 decimals
    // }

    function getConversionRate(uint256 _ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * _ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    function withdraw() payable onlyOwner public {
        msg.sender.transfer(address(this).balance);
        for(uint256 funderIndex; funderIndex < funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0);
    }
}
