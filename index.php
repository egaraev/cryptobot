<?php
$con=mysqli_connect("database-service","cryptouser","123456","cryptodb");
// Check connection
if (mysqli_connect_errno())
{
echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM logs order by log_id desc limit 10");
echo "<html><head><title>Cryptobot</title></head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
</style>
</head>
<body bgcolor=#abcaf2><h2>Cryptobot View Page</h2>
<br><b>Logs</b><br>";


echo "<table border='1'>
<tr>
<th>Date</th>
<th>Log entry</th>
</tr>";

while($row = mysqli_fetch_array($result))
{
echo "<tr>";
echo "<td>" . $row['date'] . "</td>";
echo "<td>" . $row['log_entry'] . "</td>";
echo "</tr>";
}
echo "</table>";

///mysqli_close($con);

//////////////
$result2 = mysqli_query($con,"SELECT * FROM orders where active = 1");
echo "<br><b>Current orders</b><br>";

echo "<table border='1'>
<tr>
<th>Date</th>
<th>Market</th>
<th>Quantity</th>
<th>Price</th>
<th>Current result %</th>
<th>Max %</th>
<th>Min %</th>
<th>Reasons and parameters used</th>
<th>Signal history</th>
<th>Sell signal</th>
</tr>";

while($row = mysqli_fetch_array($result2))
{
echo "<tr>";
echo "<td>" . $row['date'] . "</td>";
echo "<td>" . $row['market'] . "</td>";
echo "<td>" . $row['quantity'] . "</td>";
echo "<td>" . $row['price'] . "</td>";
echo "<td><b>" . $row['percent_serf'] . "</b></td>";
echo "<td>" . $row['percent_serf_max'] . "</td>";
echo "<td>" . $row['percent_serf_min'] . "</td>";
echo "<td>" . $row['params'] . "</td>";
echo "<td>" . $row['history'] . "</td>";
echo "<td>" . $row['sell'] . "</td>";
echo "</tr>";
}
echo "</table>";

////////////

$result3 = mysqli_query($con,"SELECT * FROM orders where active = 0");
echo "<br><b>Closed orders</b><br>";

echo "<table border='1'>
<tr>
<th>Date</th>
<th>Market</th>
<th>Price</th>
<th>Result %</th>
<th>Max %</th>
<th>Min %</th>
<th>Max % After</th>
<th>Min % After</th>
<th>Reason and Parameters used</th>
<th>Reason to sell</th>
<th>Signal history</th>
<th>SELL signal</th>
</tr>";

while($row = mysqli_fetch_array($result3))
{
echo "<tr>";
echo "<td>" . $row['date'] . "</td>";
echo "<td>" . $row['market'] . "</td>";
echo "<td>" . $row['price'] . "</td>";
echo "<td><b>" . $row['percent_serf'] . "</b></td>";
echo "<td>" . $row['percent_serf_max'] . "</td>";
echo "<td>" . $row['percent_serf_min'] . "</td>";
echo "<td>" . $row['aftercount'] . "</td>";
echo "<td>" . $row['aftercount_min'] . "</td>";
echo "<td>" . $row['params'] . "</td>";
echo "<td>" . $row['reason_close'] . "</td>";
echo "<td>" . $row['history'] . "</td>";
echo "<td>" . $row['sell'] . "</td>";
echo "</tr>";
}
echo "</table>";

//////
echo '<img src="images/crypto_results.png"  height="350" width="800">';
echo '<img src="images/crypto_results2.png"  height="350" width="800">';
echo '<img src="images/crypto_results3.png"  height="350" width="800">';
echo '<img src="images/crypto_results5.png"  height="350" width="800">';
echo '<img src="images/crypto_results4.png"  height="700" width="1600">';

/////

$result4 = mysqli_query($con,"SELECT * FROM markets where active = 1");
echo "<br><b>Market status</b><br>";

echo "<table border='1'>
<tr>
<th>Currency</th>
<th>AI price</th>
<th>AI trend</th>
<th>Current price</th>
<th>HA hour</th>
<th>HA 5h</th>
<th>HA day</th>
<th>HA time update</th>
<th>% change</th>
<th>Volume</th>
<th>Peak time</th>
<th>Candle 30m</th>
<th>Candle 1h</th>
</tr>";

while($row = mysqli_fetch_array($result4))
{
echo "<tr>";
echo "<td>" . $row['market'] . "</td>";
echo "<td>" . $row['ai_price'] . "</td>";
echo "<td>" . $row['ai_direction'] . "</td>";
echo "<td>" . $row['current_price'] . "</td>";
echo "<td>" . $row['ha_direction_hour'] . "</td>";
echo "<td>" . $row['ha_direction'] . "</td>";
echo "<td>" . $row['ha_direction_daily'] . "</td>";
echo "<td>" . $row['ha_time'] . "</td>";
echo "<td>" . $row['percent_chg'] . "</td>";
echo "<td>" . $row['volume'] . "</td>";
echo "<td>" . $row['strike_date'] . "</td>";
echo "<td>" . $row['candle_signal_short'] . "</td>";
echo "<td>" . $row['candle_signal_long'] . "</td>";
echo "</tr>";
}
echo "</table>";

///////

$result5 = mysqli_query($con,"SELECT * FROM parameters");
echo "<br><b>BTC price</b><br>";
$row = mysqli_fetch_array($result5);
echo $row['usdt_btc_price'];

///////

echo "<br><b>HA trend for Bitcoin</b><br>";
echo $row['btc_ha_direction_day'];

/////

$result6 = mysqli_query($con,"SELECT SUM(percent_serf)-COUNT(percent_serf)*0.5 FROM orders where active = 0");
echo "<br><b>Total summ %</b><br>";
$row = mysqli_fetch_array($result6);
echo $row['0'];



mysqli_close($con);
?>



