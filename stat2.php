<?php
$con=mysqli_connect("database-service", "cryptouser", "123456", "cryptodb");
// Check connection
if (mysqli_connect_errno())
{
echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM logs order by log_id desc limit 10");
echo "<html><head><title>Cryptobot statistics</title></head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
</style>
</head>
<body bgcolor=#abcaf2><h2>Cryptobot Stats Page</h2>
<br><b>Stats</b><br>";


$result = mysqli_query($con,"SELECT * FROM markets where enabled = 1");


echo "<table border='1'>
<tr>
<th>Crypto name</th>
<th>MACD indicator</th>
<th>Candle Patterns Chart</th>
<th>Historical Chart for news, tweets, indicators</th>
<th>AI Historical Chart for machine learning predictions</th>
</tr>";

while($row = mysqli_fetch_array($result))
{
echo "<tr>";
echo "<td>" . $row['market'] . "</td>";
echo "<td><a href='images/". $row['market'] ."_macd_results.png'><img src='images/". $row['market'] ."_macd_results.png' width='1000px' height='700px'></td>";
echo "<td><a href='images/". $row['market'] ."_candlesticks.png'><img src='images/". $row['market'] ."_candlesticks.png' width='1000px' height='700px'></td>";
echo "<td><a href='images/". $row['market'] ."_history.png'><img src='images/". $row['market'] ."_history.png' width='1000px' height='700px'></td>";
echo "<td><a href='images/". $row['market'] ."_ai_history.png'><img src='images/". $row['market'] ."_ai_history.png' width='1000px' height='700px'></td>";

echo "</tr>";
}
echo "</table>";

mysqli_close($con);
?>
