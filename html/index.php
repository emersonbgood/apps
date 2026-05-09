<h2>Index of <?php echo $_SERVER['REQUEST_URI']; ?></h2>
<ul>
<?php
$files = scandir('.');
foreach($files as $file) {
    if($file !== "." && $file !== "index.php") {
        echo "<li><a href='$file'>$file</a></li>";
    }
}
?>
</ul>
