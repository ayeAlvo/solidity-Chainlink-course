// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase {
    address payable[] public players;
    uint256 public usdEnterFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    uint256 public fee;
    bytes32 public keyhash;
    address payable public recentWinner;
    uint256 public randomness;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTTERY_STATE public lottery_state;

    // events
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _linkToken,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _linkToken) {
        usdEnterFee = 50 * (10 ** 18); // wei
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery is not open!");
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustPrice = uint256(price) * 10 ** 10; // 18 decimals
        uint256 costToEnter = (usdEnterFee * 10 ** 18) / adjustPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Lottery is already open!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner onlyOwner {
        // forma incorrecta de manejar numeros aleatorios
        // uint256(
        //     keccak256(
        //         abi.encodePacked(
        //             nonce, // predecible, numero de la transaccion
        //             msg.sender, // es predecible
        //             block.difficulty, // puede ser manipulado por los mineros
        //             block.timestamp // es predecible
        //         )
        //     )
        // ) % players.length;
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(
        bytes32 _requestId,
        uint256 _randomness
    ) internal override {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You aren't there yet!"
        );
        require(_randomness > 0, "random-not-found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        // // Reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
