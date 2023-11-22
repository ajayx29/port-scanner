import socket
import re


def get_open_ports(target, port_range, verbose=False):
  ip = ""
  open_ports = []
  try:
    ip = socket.gethostbyname(target)
    for port in range(port_range[0], port_range[1]):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      socket.setdefaulttimeout(1)
      result = s.connect_ex((ip, port))
      if result == 0:
        open_ports.append(port)
      s.close()

  except KeyboardInterrupt:
    return "Exiting program"
  except socket.gaierror:
    if (re.search('[a-zA-Z]', target)):
      return "Error: Invalid hostname"
    return "Error: Invalid IP address"
  except socket.error:
    return "Error: Invalid IP address"

  host = None
  try:
    host = socket.gethostbyaddr(ip)[0]
  except socket.herror:
    host = None

  final_string = "Open ports for"
  if host is not None:
    final_string += " {url} ({ip})".format(url=host, ip=ip)
  else:
    final_string += " {ip}".format(ip=ip)
  final_string += '\n'
  if verbose:
    header = "PORT    SERVICE\n"
    body = ""
    for port in open_ports:
      body += "{p}".format(p=port) + "  "*(9 - len(str(port))) + "{sn}".format(sn=socket.getservbyport(port))
      
      if (open_ports[len(open_ports) - 1] != port):
        body += "\n"
    return final_string + header + body

  return (open_ports)
