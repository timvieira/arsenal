<?php
//$to      = "danielhschreiber@gmail.com,timsfanmail@gmail.com,dan.muriello@gmail.com";
$to      = "timsfanmail@gmail.com";
$subject = "Email Spoofing is fun!";
$body    = "Hooray, Email pranks galore.";
//$headers = "From: danielhschreiber@gmail.com\r\n" . "X-Mailer: php";
$headers = "From: tim.f.vieira@gmail.com\r\n" . "X-Mailer: php";

if (mail($to, $subject, $body, $headers)) {
  echo("<p>Message sent!</p>");
} else {
  echo("<p>Message delivery failed...</p>");
}
?>