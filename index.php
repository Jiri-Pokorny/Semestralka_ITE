<!DOCTYPE html>
<html lang='cs'>
  <head>
    <title></title>
    <meta charset='utf-8'>
    <style>
      body
      {
          text-align:center;
          background:black;
          color:white;
      }
      article
      {
          position:fixed;
          min-width:100%;
          min-height: 100%;
          top:40%;
      }
      h1
      {
          font-size:100px;
          margin:10px;
          cursor:default;
      }
      header
      {
          font-size:70px;
          position:fixed;
          left:30%;
          top:5%;
          text-align:center;
          padding:10px;
          margin:30px;
      }
      #vratny_odkaz
      {
          position:fixed;
          top:40%;
          left:27%;
          color:white;
          font-size:50px;
      }
      table
      {
          border: none;
        
      }
      th
      {
          border: none;
          
      }
      td
      {
        border: none;
        width:20px;
        height:15px;
      }
      input
      {
          text-align:center;
      }
      #ssid, #passwd
      {
          border-radius:7px;
          padding:15px;
          margin:10px;
          margin-bottom:20px;
          font-size:20px;
      }
      button
      {
          border: none;
          border-radius: 3px;
          background: transparent;
          color: white;
          padding-left: 100px;
          padding-right: 100px;
          padding-top: 15px;
          padding-bottom: 15px;
          margin-top: 0px;
          font-size: 20px;
          cursor: pointer;
      }
      button:hover
      {
          background:rgb(89,89,89);
          cursor:pointer;
      }
    </style>
  </head>
  <body>
  <article>
  <h1>ESP-Black</h1>
    <form action="index.php" method="post">
        <input id="ssid" type="text" name="ssid" placeholder="wifi ssid"><br>
        <input id="passwd" type="password" name="password" placeholder="password"><br>
        <button id="ok" type="submit" name="ok">SUBMIT</button>
    </form>
  </article>
  </body>
  <?php
      echo "PHP";
      $host = "";
      $port = 80;
      set_time_limit(0);

      $socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
      $result = socket_connect($socket, $host, $port) or die("Could not connect toserver\n");
      echo "Socket connected";
      if (isset($_POST["ok"])) {
        $message = $_POST["ssid"] + " " + $_POST["password"];
        echo $message;
        socket_write($socket, $message, strlen($message)) or die("Could not send data to server\n");
        $result = socket_read($socket, 1024) or die("Could not read server response\n");
        echo "Reply From Server  :".$result;
      }
      socket_close($socket);
    ?>
</html>