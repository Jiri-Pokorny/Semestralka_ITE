try:
  import usocket as socket
except:
  import socket

import network
import machine
import sys

import esp
esp.osdebug(None)

class AP:

  def __init__(self) -> None:
    print("AP - init...")
    self.data_recieved = False
    self.ssid = 'ESP-Black'
    self.password = '123456789'
    self.ap = network.WLAN(network.AP_IF)
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.file = 'network.txt'

  def start_ap(self):
    print("AP - start_ap...")
    self.ap.active(True)
    self.ap.config(essid=self.ssid, password=self.password)
    print('AP is running')
    print(self.ap.ifconfig())
    return 0
  
  def start_socket(self):
    print("AP - start_socket...")
    self.s.bind(('', 80))
    self.s.listen(5)
    return 0

  def web_page(self, page) -> str:
    print("AP - web_page...")
    html = ""
    with open(page) as f:
      html += f.read()
    return html

  def parse_data_recieved(self, data):
    print("AP - data recieved...")
    data = str(data, "UTF-8")
    print(data)
    if('password' in data and 'ssid' in data):
      data = data.replace('?', '#')
      data = data.replace('=', '#')
      data = data.replace('&', '#')
      split_data = data.split('#')
      ssid = split_data[split_data.index('ssid')+1]
      passwd = split_data[split_data.index('password')+1]
      if len(ssid)>0:
        print("Data valid")
        self.write_data_to_file(ssid, passwd)
        self.data_recieved = True
    return 0

  def write_data_to_file(self, ssid, passwd):
    print("AP - write_data_to_file...")
    with open(self.file) as f:
      print('ssid + "\n" + passwd')
      f.write(ssid + "\n" + passwd)
    return 0

  def run(self):
    try:
      print("AP - run...")
      self.start_ap()
      while self.ap.active() == False:
        pass
      self.start_socket()
      
      while True:
        conn, addr = self.s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        #print('Content = %s' % str(request))
        self.parse_data_recieved(request)
        if self.data_recieved:
          print("success response...")
          response = self.web_page('success.html')
          conn.write(response)
          conn.close()
          break
        response = self.web_page('index.html')
        conn.write(response)
        print("End of loop")
        conn.close()
      self.ap.active(False)
      self.data_recieved = False
      print("Exiting AP")
      return
    except Exception:
      machine.reset()
  