<head><body bgcolor=#abcaf2></head>
<?php
$con=mysqli_connect("database-service", "cryptouser", "123456", "cryptodb");
// Check connection
if (mysqli_connect_errno())
{
echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$market=$_GET["market"];
echo $market;
  
$result = mysqli_query($con,"SELECT * FROM history where market = '" . $market . "'");



echo "<table border='1'>
<tr>
<th>Market</th>
<th>Date</th>
<th>Price</th>
<th>Candle Score</th>
<th>Pos.tweets</th>
<th>Neg.tweets</th>
<th>Twitter ratio</th>
<th>News score</th>
<th>MACD signal</th>
<th>OBV signal</th>
<th>HeikinAshi trend</th>
<th>Candle pattern</th>
<th>Volume change</th>
</tr>";

while($row = mysqli_fetch_array($result))
{
echo "<tr>";
echo "<td>" . $row['market'] . "</td>";
echo "<td>" . $row['date'] . "</td>";
echo "<td>" . $row['price'] . "</td>";
echo "<td>" . $row['candle_score'] . "</td>";
echo "<td>" . $row['positive_tweets'] . "</td>";
echo "<td>" . $row['negative_tweets'] . "</td>";
$tweet_ratio=($row['positive_tweets']/$row['negative_tweets']);
$tweets_ratio = number_format($tweet_ratio, 2, '.', '');
echo "<td>" . $tweets_ratio . "</td>";        
echo "<td>" . $row['news_score'] . "</td>";
echo "<td>" . $row['macd_signal'] . "</td>";
echo "<td>" . $row['obv_signal'] . "</td>";
echo "<td>" . $row['ha_day'] . "</td>";
echo "<td>" . $row['candle_pattern'] . "</td>";
echo "<td>" . $row['volume_chg'] . "</td>";

echo "</tr>";
}
echo "</table>";

mysqli_close($con);
?>
