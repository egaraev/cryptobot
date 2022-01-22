<html>
<head>
<title>
Cryptobot
</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.css" />
</head>
<body>



<?php
$con=mysqli_connect("database-service", "cryptouser", "123456", "cryptodb");
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
<body bgcolor=#abcaf2><h2>Cryptobot`s View Page</h2>
<a href='stat2.php'><font size='+2'><b>Link to candle analyze and history statistics page</b></font></a><br>
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
echo "<td><pre>" . $row['log_entry'] . "</pre></td>";
echo "</tr>";
}
echo "</table>";

///mysqli_close($con);

//////////////


$result2 = mysqli_query($con,"SELECT * FROM markets where  enabled=1");
echo "<br><b>Current stocks</b><br>";

echo "<table border='1'>
<tr>
<th>Stock name</th>
<th>Current price</th>
<th>Two weeks chart</th>
<th>Tweeter sentiments</th>
<th>Predicted price</th>
<th>AI Predicted chart for 1 month</th>
<th>AI forecast directtion</th>
<th>Heikin_ashi direction chart</th>
<th>OBV chart</th>
<th>MACD direction</th>
<th>Candle patterns chart</th>
<th>Heikin_ashi direction</th>
<th>Trend</th>
<th>Candle pattern</th>
<th>Candle score</th>
<th>Hour candle</th>
<th>Day candle</th>
<th>MACD signal</th>
<th>OBV signal</th>
</tr>";

while($row = mysqli_fetch_array($result2))
{
echo "<tr>";
//echo "<td>" . $row['name'] . "</td>";
echo "<td><a href='history2.php?market=". $row['market'] ."'>". $row['market'] ."</a></td>";
echo "<td>" . $row['current_price'] . "</td>";
echo "<td><a href='images/". $row['market'] ."_chart.png'><img src='images/". $row['market'] ."_chart.png' width='300px' height='250px'></td>";
echo "<td><a href='images/". $row['market'] ."_tweets.png'><img src='images/". $row['market'] ."_tweets.png' width='250px' height='250px'></td>";
echo "<td><b>" . $row['predicted_price'] . "</b></td>";
echo "<td><a href='images/". $row['market'] ."_result.png'><img src='images/". $row['market'] ."_result.png' width='250px' height='250px'></td>";
echo "<td><b>" . $row['ai_direction'] . "</b></td>";
echo "<td><a href='images/". $row['market'] ."_hachart.png'><img src='images/". $row['market'] ."_hachart.png' width='280px' height='250px'></td>";
//echo "<td><a href='images/". $row['market'] ."_kov_results.png'><img src='images/". $row['market'] ."_kov_results.png' width='280px' height='250px'></td>";
echo "<td><a href='images/cryptobot/". $row['market'] ."_obv_results.png'><img src='images/cryptobot/". $row['market'] ."_obv_results.png' width='280px' height='250px'></td>";
echo "<td><a href='images/". $row['market'] ."_macd_results.png'><img src='images/". $row['market'] ."_macd_results.png' width='280px' height='250px'></td>";
echo "<td><a href='images/". $row['market'] ."_candlesticks.png'><img src='images/". $row['market'] ."_candlesticks.png' width='280px' height='250px'></td>";
echo "<td>" . $row['ha_day'] . "</td>";
echo "<td>" . $row['trend'] . "</td>";
echo "<td>" . $row['candle_pattern'] . "</td>";
echo "<td>" . $row['candle_score'] . "</td>";
echo "<td>" . $row['hour_candle_direction'] . "</td>";
echo "<td>" . $row['candle_direction'] . "</td>";
echo "<td>" . $row['macd_signal'] . "</td>";
//echo "<td>" . $row['kov_signal'] . "</td>";
echo "<td>" . $row['obv_signal'] . "</td>";
//echo "<td><pre>" . $row['news'] . "</pre></td>";
//echo "<td><pre><p><a href='#". $row['market'] ."' rel='modal:open'>Open details</a></p></pre></td>";
echo "</tr>";
}
echo "</table>";
$result2 = mysqli_query($con,"SELECT * FROM markets where enabled = 1");
while($row = mysqli_fetch_array($result2))
{
	echo'<div id="'.$row['market'].'" class="modal">'.
  $row['news_text'].'
  <a href="#" rel="modal:close">Close</a>
</div>';
}


//////////////
$result3 = mysqli_query($con,"SELECT * FROM orders where active = 1");
echo "<br><b>Current orders</b><br>";

echo "<table border='1'>
<tr>
<th>Date</th>
<th>market</th>
<th>Price</th>
<th>Current result %</th>
<th>Max %</th>
<th>Min %</th>
<th>Reason_and_Parameters_used</th>
<th>Danger order</th>
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
echo "<td>" . $row['params'] . "</td>";
echo "<td>" . $row['danger_order'] . "</td>";
echo "</tr>";
}
echo "</table>";


////////////
echo "<br>";
echo "<td><a href='images/crypto_results.png'><img src='images/crypto_results.png' width='800px' height='400px'></a></td>";
echo "<td><a href='images/crypto_results2.png'><img src='images/crypto_results2.png' width='800px' height='400px'></a></td>";


$result5 = mysqli_query($con,"SELECT SUM(percent_serf) FROM orders where active = 0");
echo "<br><b>Total summ %</b><br>";
$row = mysqli_fetch_array($result5);
#echo $row['0'];
echo "<td>" . $row['0'] . "</td>";
echo "<br>";
//////


$result4 = mysqli_query($con,"SELECT * FROM orders where active = 0");
echo "<br><b>Closed orders</b><br>";

echo "<table border='1'>
<tr>
<th>Date</th>
<th>Market</th>
<th>Price</th>
<th>Result %</th>
<th>Max %</th>
<th>Min %</th>
<th>Aftercount Max %</th>
<th>Aftercount Min %</th>
<th>Reason_and_Parameters_used</th>
<th>Reason_to_sell</th>

</tr>";

while($row = mysqli_fetch_array($result4))
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

echo "</tr>";
}
echo "</table>";




mysqli_close($con);
?>

<!-- Remember to include jQuery :) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0/jquery.min.js"></script>

<!-- jQuery Modal -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.js"></script>
</body>

</html>